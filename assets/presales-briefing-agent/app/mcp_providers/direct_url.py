"""Direct URL MCP provider.

Connects to MCP servers that are reachable by URL but not yet registered in
Agent Gateway. Tools are loaded once per request, same lifecycle as agw.py.

Servers are configured via the DIRECT_MCP_SERVERS environment variable:
    DIRECT_MCP_SERVERS='[
        {"name": "ical-knowledge", "url": "https://prod-ical-mcpserver.c-86fbf98.kyma.ondemand.com/mcp", "token": "<bearer-token>"}
    ]'

Each entry:
  - name   : short slug used as tool name prefix (e.g. "ical-knowledge")
  - url    : full MCP endpoint URL (must accept POST on the given path)
  - token  : bearer token for authentication (optional — omit if server is public)

In local / test mode (IBD_TESTING=1) this provider returns an empty list so that
mcp-mock.json tools from agw.py remain the sole source of mock tools during tests.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from langchain_core.tools import BaseTool, StructuredTool
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from pydantic import Field, create_model

logger = logging.getLogger(__name__)


def _get_server_configs() -> list[dict]:
    """Read server configs from DIRECT_MCP_SERVERS env var."""
    raw = os.environ.get("DIRECT_MCP_SERVERS", "")
    if not raw:
        return []
    try:
        configs = json.loads(raw)
        if isinstance(configs, list):
            return configs
    except Exception:
        logger.warning("Failed to parse DIRECT_MCP_SERVERS — expected JSON array")
    return []


def _schema_to_langchain_model(tool_name: str, input_schema: dict) -> type:
    """Convert a JSON Schema object to a Pydantic model for LangChain StructuredTool."""
    props = input_schema.get("properties", {})
    required_fields = set(input_schema.get("required", []))
    field_defs: dict[str, Any] = {}

    for field_name, field_info in props.items():
        json_type = field_info.get("type", "string")
        if json_type == "integer":
            python_type: type = int
        elif json_type == "number":
            python_type = float
        elif json_type == "boolean":
            python_type = bool
        else:
            python_type = str

        desc = field_info.get("description", "")
        if field_name in required_fields:
            field_defs[field_name] = (python_type, Field(description=desc))
        else:
            field_defs[field_name] = (python_type, Field(default=None, description=desc))

    return create_model(f"{tool_name}_args", **field_defs) if field_defs else create_model(f"{tool_name}_args")


async def _load_tools_from_server(name: str, url: str, token: str | None) -> list[BaseTool]:
    """Connect to one MCP server URL and return its tools as LangChain tools."""
    tools: list[BaseTool] = []

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        async with streamable_http_client(url, headers=headers) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.list_tools()

                for mcp_tool in result.tools:
                    tool_name = f"{name}__{mcp_tool.name}"
                    description = mcp_tool.description or ""
                    input_schema = (
                        mcp_tool.inputSchema.model_dump()
                        if hasattr(mcp_tool.inputSchema, "model_dump")
                        else (mcp_tool.inputSchema if isinstance(mcp_tool.inputSchema, dict) else {})
                    )
                    args_schema = _schema_to_langchain_model(tool_name, input_schema)

                    # Capture loop variables for the closure
                    _session = session
                    _mcp_tool_name = mcp_tool.name

                    async def _call(
                        _s: ClientSession = _session,
                        _t: str = _mcp_tool_name,
                        **kwargs: Any,
                    ) -> str:
                        call_result = await _s.call_tool(_t, arguments=kwargs)
                        if call_result.content:
                            parts = []
                            for c in call_result.content:
                                if hasattr(c, "text"):
                                    parts.append(c.text)
                                else:
                                    parts.append(str(c))
                            return "\n".join(parts)
                        return "{}"

                    tools.append(
                        StructuredTool(
                            name=tool_name,
                            description=description,
                            args_schema=args_schema,
                            coroutine=_call,
                            handle_tool_error=True,
                        )
                    )

        logger.info("Loaded %d tool(s) from direct MCP server '%s' (%s)", len(tools), name, url)

    except Exception:
        logger.exception("Failed to load tools from direct MCP server '%s' (%s)", name, url)

    return tools


async def get_direct_mcp_tools() -> list[BaseTool]:
    """Return tools from all directly configured MCP server URLs.

    Returns empty list in test mode (IBD_TESTING=1) or when DIRECT_MCP_SERVERS is not set.
    Failures per server are logged but do not raise — the agent continues with fewer tools.
    """
    if os.environ.get("IBD_TESTING") == "1":
        return []

    configs = _get_server_configs()
    if not configs:
        return []

    all_tools: list[BaseTool] = []
    for cfg in configs:
        server_name = cfg.get("name", "direct")
        server_url = cfg.get("url", "")
        server_token = cfg.get("token")

        if not server_url:
            logger.warning("Direct MCP server '%s' has no URL — skipping", server_name)
            continue

        tools = await _load_tools_from_server(server_name, server_url, server_token)
        all_tools.extend(tools)

    return all_tools
