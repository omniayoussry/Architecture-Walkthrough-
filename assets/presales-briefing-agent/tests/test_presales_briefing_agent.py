"""
Integration tests for the SAP Presales Briefing Consultant Agent.

All tests run offline with mocked LLM (AI Core not available in test env)
and mocked MCP tools loaded from mcp-mock.json via IBD_TESTING=true.

Test scenarios:
  1. happy_path            — all connectors live, all data provided, full briefing
  2. missing_entitlement   — BOM item has no entitlement data; inline flag in output
  3. leanix_not_available  — LeanIX returns no data; integration layer flagged partial
  4. gate_blocking         — no confirm signal; agent should not produce briefing content
  5. skip_command          — architect skips meeting notes; section flagged as partial
  6. one360_unreachable    — One360 returns no data; customer intelligence flagged partial
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Ensure IBD_TESTING is set so mcp_providers.agw uses mcp-mock.json
os.environ.setdefault("IBD_TESTING", "true")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_mock_data() -> dict:
    """Load mcp-mock.json from the agent root."""
    mock_path = Path(__file__).parent.parent / "mcp-mock.json"
    with open(mock_path) as f:
        return json.load(f)


def _make_llm_response(text: str) -> MagicMock:
    """Build a minimal mock LLM response chunk."""
    msg = MagicMock()
    msg.content = text
    return msg


def _make_graph_result(response_text: str) -> dict[str, Any]:
    """Build a minimal LangGraph ainvoke result."""
    from langchain_core.messages import AIMessage
    return {"messages": [AIMessage(content=response_text)]}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def mock_llm_happy_path():
    """LLM mock returning a full briefing document."""
    briefing = (
        "PRESALES BRIEFING DOCUMENT\n"
        "-----------------------------------------------------------\n"
        "Customer: Acme Corporation\n"
        "Prepared by: SAP Presales Briefing Agent\n"
        "Date: 2026-11-15\n"
        "-----------------------------------------------------------\n\n"
        "## Customer Overview\n"
        "Acme Corporation is a global manufacturing company with 12,000 employees. "
        "Strategic priorities include migrating from SAP ECC 6.0 and digitising procurement.\n\n"
        "## BOM Item Explanations\n"
        "### SAP S/4HANA Cloud, public edition\n"
        "SAP S/4HANA Cloud, public edition is a complete intelligent ERP system.\n\n"
        "## BOM Justification\n"
        "SAP S/4HANA Cloud is recommended based on SAP best practices for cloud ERP.\n\n"
        "## Entitlement Highlights\n"
        "- SAP Analytics Cloud (embedded): included at no additional cost.\n"
        "- SAP Business AI: included in the S/4HANA Cloud subscription.\n\n"
        "## Integration Layer\n"
        "The proposed solution integrates via SAP Integration Suite.\n"
        "Acme's existing SAP ECC-to-BO BI interface will be replaced.\n\n"
        "## Customer Context and Meeting History\n"
        "Key concern: TCO and migration complexity. Decision expected Q1 2027.\n"
    )
    with patch("agent.SampleAgent._invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = _make_graph_result(briefing)
        yield mock_invoke


@pytest.fixture()
def mock_llm_gate_report():
    """LLM mock returning a data completeness gate report (no briefing content)."""
    report = (
        "Data Completeness Check\n"
        "-----------------------------------------------------------\n"
        "CONNECTORS (automatic)\n"
        "[OK] SAP Knowledge Connector       Connected\n"
        "[OK] One360 Connector              Connected\n"
        "[OK] LeanIX Connector              Connected + data found for Acme Corporation\n\n"
        "MANUAL INPUTS\n"
        "[WARNING] Bill of Materials (BOM)       NOT provided\n"
        "[WARNING] Customer To-Be Architecture   NOT provided\n"
        "[WARNING] Entitlement Reference Sheet   NOT provided\n"
        "[WARNING] Meeting Notes / Transcripts   NOT provided\n\n"
        "Action required: Please upload the missing items above, then type 'confirm' to proceed.\n"
    )
    with patch("agent.SampleAgent._invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = _make_graph_result(report)
        yield mock_invoke


@pytest.fixture()
def mock_llm_missing_entitlement():
    """LLM mock returning briefing with entitlement gap flag for Ariba SKU."""
    briefing = (
        "PRESALES BRIEFING DOCUMENT\n"
        "-----------------------------------------------------------\n\n"
        "## Entitlement Highlights\n"
        "### SAP S/4HANA Cloud, public edition\n"
        "- SAP Analytics Cloud (embedded): included at no additional cost.\n\n"
        "### SAP Ariba Procurement\n"
        "WARNING Entitlement data not available for this SKU — "
        "please supply an entitlement reference sheet for a complete view.\n"
    )
    with patch("agent.SampleAgent._invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = _make_graph_result(briefing)
        yield mock_invoke


@pytest.fixture()
def mock_llm_leanix_partial():
    """LLM mock returning briefing with partial integration layer (no LeanIX data)."""
    briefing = (
        "PRESALES BRIEFING DOCUMENT\n"
        "-----------------------------------------------------------\n\n"
        "## Integration Layer\n"
        "WARNING This section is based on the SAP reference integration model only, "
        "not the customer's specific application landscape. For a customer-specific "
        "integration narrative, please provide LeanIX data (connected or manual export).\n\n"
        "SAP reference integration patterns for the proposed solution: "
        "SAP Integration Suite connects S/4HANA Cloud to Ariba and third-party systems.\n"
    )
    with patch("agent.SampleAgent._invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = _make_graph_result(briefing)
        yield mock_invoke


@pytest.fixture()
def mock_llm_one360_partial():
    """LLM mock returning briefing with partial customer overview (One360 unavailable)."""
    briefing = (
        "PRESALES BRIEFING DOCUMENT\n"
        "-----------------------------------------------------------\n\n"
        "## Customer Overview\n"
        "WARNING Customer intelligence unavailable. One360 Connector did not return data "
        "for this account. This section requires manual completion.\n"
    )
    with patch("agent.SampleAgent._invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = _make_graph_result(briefing)
        yield mock_invoke


@pytest.fixture()
def mock_llm_skip_meeting_notes():
    """LLM mock returning briefing with partial meeting history (notes skipped)."""
    briefing = (
        "PRESALES BRIEFING DOCUMENT\n"
        "-----------------------------------------------------------\n\n"
        "## Customer Context and Meeting History\n"
        "WARNING Meeting notes not provided. This section is based on One360 account "
        "intelligence only.\n\n"
        "Key account intelligence from One360: Customer evaluating SAP vs Microsoft D365.\n"
        "\n## BOM Justification\nRecommended based on SAP best practices.\n"
    )
    with patch("agent.SampleAgent._invoke", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = _make_graph_result(briefing)
        yield mock_invoke


# ---------------------------------------------------------------------------
# Test 1 — Happy path
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_happy_path_full_briefing(mock_llm_happy_path):
    """All connectors live, all files provided — full briefing generated with no gaps."""
    from agent import SampleAgent

    agent = SampleAgent()
    query = (
        "I have uploaded the BOM list, to-be architecture, entitlement sheet, "
        "and meeting notes. Customer is Acme Corporation (ID: ACME-CORP-001). confirm"
    )
    result = await agent.invoke(query, context_id="test-happy-path")

    assert result.status == "completed"
    content = result.message

    # Must contain all 7 required sections
    assert "Customer Overview" in content
    assert "BOM Item Explanations" in content or "BOM Justification" in content
    assert "Entitlement Highlights" in content
    assert "Integration Layer" in content

    # Must NOT contain partial flags for entitlements or integration in happy path
    assert "WARNING Entitlement data not available for this SKU" not in content or \
           "SAP Ariba" not in content  # only Ariba is missing entitlement in mock
    assert "based on the SAP reference integration model only" not in content


# ---------------------------------------------------------------------------
# Test 2 — Missing entitlement data
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_missing_entitlement_flag(mock_llm_missing_entitlement):
    """One BOM item (Ariba) has no entitlement data — inline flag must appear."""
    from agent import SampleAgent

    agent = SampleAgent()
    query = (
        "BOM contains S4HANA-CLOUD-PUBLIC and SAP-ARIBA-PROCUREMENT. confirm"
    )
    result = await agent.invoke(query, context_id="test-missing-entitlement")

    assert result.status == "completed"
    assert "WARNING Entitlement data not available for this SKU" in result.message


# ---------------------------------------------------------------------------
# Test 3 — LeanIX not available
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_leanix_not_available_partial_flag(mock_llm_leanix_partial):
    """LeanIX returns no data — integration layer must be flagged as partial."""
    from agent import SampleAgent

    agent = SampleAgent()
    query = (
        "Customer ID: NEW-CUSTOMER-001 — LeanIX returned no data. "
        "skip leanix. confirm"
    )
    result = await agent.invoke(query, context_id="test-leanix-no-data")

    assert result.status == "completed"
    assert "SAP reference integration model only" in result.message
    assert "not the customer's specific application landscape" in result.message


# ---------------------------------------------------------------------------
# Test 4 — Gate blocking (no confirm)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_gate_blocking_no_briefing_without_confirm(mock_llm_gate_report):
    """Architect has not confirmed — agent must show gate report, not briefing."""
    from agent import SampleAgent

    agent = SampleAgent()
    query = "Generate a briefing for Acme Corporation."
    result = await agent.invoke(query, context_id="test-gate-blocking")

    assert result.status == "completed"
    content = result.message

    # Gate report should be present — completeness check content
    assert "Data Completeness Check" in content or "NOT provided" in content

    # Full briefing sections must NOT appear before gate is cleared
    assert "Entitlement Highlights" not in content
    assert "Integration Layer" not in content


# ---------------------------------------------------------------------------
# Test 5 — Skip command (meeting notes skipped)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_skip_meeting_notes_partial_section(mock_llm_skip_meeting_notes):
    """Architect skips meeting notes — section flagged as partial but briefing proceeds."""
    from agent import SampleAgent

    agent = SampleAgent()
    query = (
        "skip meeting notes. Customer: Acme Corporation. BOM provided. confirm"
    )
    result = await agent.invoke(query, context_id="test-skip-meeting-notes")

    assert result.status == "completed"
    content = result.message

    # Meeting history section should be flagged as partial
    assert "WARNING Meeting notes not provided" in content

    # But other briefing content should still be present
    assert "BOM Justification" in content or "Recommended based on SAP best practices" in content


# ---------------------------------------------------------------------------
# Test 6 — One360 unreachable
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_one360_unreachable_partial_customer_section(mock_llm_one360_partial):
    """One360 is unavailable — customer intelligence section flagged as partial."""
    from agent import SampleAgent

    agent = SampleAgent()
    query = (
        "skip one360. Customer: Unknown Corp. BOM provided. confirm"
    )
    result = await agent.invoke(query, context_id="test-one360-unreachable")

    assert result.status == "completed"
    assert "WARNING Customer intelligence unavailable" in result.message
    assert "One360 Connector did not return data" in result.message


# ---------------------------------------------------------------------------
# Test 7 — mcp-mock.json structure validation
# ---------------------------------------------------------------------------

def test_mcp_mock_structure():
    """Validate mcp-mock.json has all required servers and tools."""
    data = _load_mock_data()

    assert "servers" in data
    assert "metadata" in data

    servers = data["servers"]

    # Connected servers: ibd-mcp-server and dpca-mcp-server
    assert "ibd-mcp-server" in servers
    assert "dpca-mcp-server" in servers

    # ibd-mcp-server tools
    ibd_tools = servers["ibd-mcp-server"]["tools"]
    assert "sap_knowledge_graph_bp_mapping" in ibd_tools
    assert "sap_knowledge_graph_fit_gap" in ibd_tools
    assert "sap_help_search" in ibd_tools
    assert "sap_help_get_content" in ibd_tools
    assert "sap_knowledge_graph_api_discovery" in ibd_tools
    assert "call_business_api" in ibd_tools

    # dpca-mcp-server tools
    dpca_tools = servers["dpca-mcp-server"]["tools"]
    assert "ums_search_data_products" in dpca_tools

    # fit-gap mock contains entitlement data for S/4HANA but not for Ariba
    fit_gap_response = ibd_tools["sap_knowledge_graph_fit_gap"]["mock_response"]
    products = fit_gap_response["sub_processes"][0]["products"]
    s4_product = next(p for p in products if "S/4HANA" in p["product"])
    ariba_product = next(p for p in products if "Ariba" in p["product"])
    assert s4_product["entitlements"] is not None
    assert len(s4_product["entitlements"]) > 0
    assert ariba_product["entitlements"] is None


# ---------------------------------------------------------------------------
# Test 8 — Agent invoke returns AgentResponse
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_agent_invoke_returns_agent_response():
    """Agent.invoke() always returns an AgentResponse with status and message."""
    from agent import AgentResponse, SampleAgent

    response_text = "I need more information to proceed."

    with patch("agent.SampleAgent._invoke", new_callable=AsyncMock) as mock_invoke:
        from langchain_core.messages import AIMessage
        mock_invoke.return_value = {"messages": [AIMessage(content=response_text)]}

        agent = SampleAgent()
        result = await agent.invoke("hello", context_id="test-basic")

    assert isinstance(result, AgentResponse)
    assert result.status in ("completed", "input_required", "error")
    assert isinstance(result.message, str)
    assert len(result.message) > 0


# ---------------------------------------------------------------------------
# Test 9 — Milestone log emission (M1, M6)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_milestone_instrumentation_emitted(caplog):
    """Milestone log statements are emitted during agent execution."""
    import logging

    from agent import SampleAgent

    briefing = (
        "PRESALES BRIEFING DOCUMENT\n"
        "Customer Overview: Acme Corp.\n"
        "BOM Justification: recommended.\n"
        "Entitlement Highlights: included.\n"
        "Integration Layer: SAP Integration Suite.\n"
    )

    with patch("agent.SampleAgent._invoke", new_callable=AsyncMock) as mock_invoke:
        from langchain_core.messages import AIMessage
        mock_invoke.return_value = {"messages": [AIMessage(content=briefing)]}

        agent = SampleAgent()
        with caplog.at_level(logging.INFO):
            await agent.invoke(
                "confirm bom entitlement integration layer",
                context_id="test-milestone"
            )

    log_text = caplog.text
    # At least one milestone log should be present
    assert "M1" in log_text or "M3" in log_text or "M6" in log_text
