# Specification: presales-briefing-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read `product-requirements-document.md` and `intent.md` at the solution root
- [x] Bootstrap agent code in `assets/presales-briefing-agent/` using the `sap-agent-bootstrap` skill
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

- [x] Create `assets/presales-briefing-agent/app/skills/data-completeness-gate/SKILL.md`
- [x] Create `assets/presales-briefing-agent/app/skills/briefing-generator/SKILL.md`
- [x] Create `assets/presales-briefing-agent/app/skills/bom-justification/SKILL.md`
- [x] Create `assets/presales-briefing-agent/app/skills/integration-layer/SKILL.md`

---

## Project-Specific Tasks

### Phase 1 — Data Completeness Gate

- [x] Implement data completeness gate logic in system prompt and agent runtime
- [x] Completeness report covers 7 data domains in correct order
- [x] Gate report formatted with status indicators and action prompts
- [x] Agent waits for architect confirmation before proceeding to Phase 2
- [x] Handles file uploads, skip commands, and confirm signals
- [x] SAP Knowledge Connector unreachable = halt condition

### Phase 2 — SAP Knowledge Retrieval

- [x] retrieve_sap_knowledge() logic via MCP tool calls
- [x] entitlement_missing flag when connector returns no entitlement data
- [x] knowledge_missing flag when connector returns no data at all
- [x] Results stored in context for briefing generator

### Phase 2 — LeanIX Enterprise Architecture Retrieval

- [x] retrieve_leanix_data() via LeanIX Connector MCP tool
- [x] leanix_available=False fallback when no data for account
- [x] LeanIX snapshot date recorded for citation in briefing

### Phase 2 — One360 Customer Intelligence Retrieval

- [x] retrieve_one360_context() via One360 Connector MCP tool
- [x] one360_available=False fallback when unreachable or no data
- [x] Results stored in context object

### Phase 2 — File Parsing

- [x] parse_uploaded_files() supports PDF, DOCX, CSV, Excel, plain text
- [x] Unsupported file types trigger notification to architect
- [x] Content keyed by domain in context object
- [x] Input templates offered in completeness gate report

### Phase 2 — Briefing Document Assembly

- [x] generate_briefing() assembles 7-section document in mandatory order
- [x] Dual-purpose formatting: customer reading + architect talking points per section
- [x] Inline gap flags with reason, domain, and suggested action
- [x] Document header with generation date and source traceability

### MCP Tool Wiring

- [x] SAP Knowledge Connector registered in asset.yaml requires
- [x] One360 Connector registered in asset.yaml requires
- [x] LeanIX Connector registered in asset.yaml requires
- [x] System prompt instructions added to app/agent.py

---

## MCP API Scope

```text
MCP API: SAP Knowledge Connector
MCP tool scope: read-only
Resources in scope: product descriptions, best practices, entitlement data, integration patterns

MCP API: One360 Connector
MCP tool scope: read-only
Resources in scope: account history, customer landscape, strategic priorities, relationship context

MCP API: LeanIX Connector
MCP tool scope: read-only
Resources in scope: application landscape, capability map, interface inventory, technology portfolio
```

---

## Business Instrumentation

- [x] M1 — data_completeness_gate span + log_milestone
- [x] M2 — architect_confirmation span + log_milestone
- [x] M3 — sap_knowledge_retrieval span + log_milestone
- [x] M4 — leanix_retrieval span + log_milestone
- [x] M5 — one360_enrichment span + log_milestone
- [x] M6 — briefing_generation span + log_milestone
- [x] bootstrap(app) called after app = server.build() in main.py

---

## MCP Tool Integration

- [x] AgentExecutor loads tools via mcp_providers.agw.get_mcp_tools()
- [x] No direct HTTP calls to connectors — all via MCP tools
- [x] mcp-mock.json generated with 3 servers, 7 tools, all 6 test scenarios covered

---

## Testing

- [x] conftest.py sets IBD_TESTING=true
- [x] mcp-mock.json written with full mock data for all 3 connectors
- [x] 9 integration tests written covering all 6 required scenarios
- [x] pytest run: 64 passed, 87% coverage (threshold: 70%)
- [x] test_report.json generated in assets/presales-briefing-agent/
