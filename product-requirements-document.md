# Product Requirements Document (PRD)

**Title:** SAP Presales Briefing Consultant Agent  
**Date:** 2026-11-15  
**Owner:** Solution Architecture / Presales Practice  
**Solution Category:** AI Agent

---

## Product Purpose & Value Proposition

**Elevator Pitch:**  
Solution architects today spend 4–8 hours per engagement manually researching SAP products, justifying BOM items, and assembling customer briefings. This agent eliminates that effort — it takes the customer's to-be architecture, BOM list, meeting notes, and entitlement data, enriches them with SAP knowledge and One360 customer intelligence, and produces a ready-to-use briefing document in under 30 minutes.

**Business Need:**  
There is no current tooling that combines SAP best-practice product knowledge, live customer context from One360, and architect-supplied inputs (BOM, architecture documents, transcripts) into a single consistent briefing output. The result is inconsistent briefing quality, missed entitlement highlights, weak integration narratives, and significant time lost to manual preparation before each customer engagement.

**Expected Value:**  
- Briefing preparation time reduced from 4–8 hours to under 30 minutes
- Entitlement highlights systematically surfaced for every BOM item, closing commercial gaps
- Integration layer narratives grounded in SAP best-practice patterns — not improvised per architect
- Adoption target of 70%+ of presales engagements using agent-generated briefings within 9 months

**Product Objectives (Prioritised):**
1. Eliminate manual briefing research — agent handles SAP knowledge retrieval and customer context enrichment automatically
2. Guarantee data completeness transparency — architect always knows what is present and what is missing before the briefing is generated
3. Produce dual-purpose output — document usable independently by the customer AND as a live talking-points guide for the architect
4. Surface entitlement and integration value reliably — no SKU's embedded entitlements or integration examples left undocumented

---

## Business Metrics

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Time to produce a customer briefing document | ~4–8 hours (manual) | < 30 minutes with agent | 3–6 months post-deployment | Presales engagement / Opportunity to Quote | agent-derived |
| Briefing acceptance rate (no major rework) | ~50% (estimated) | ≥ 80% used without significant revision | 6 months post-deployment | Solution quality / Customer Quotation Management | agent-derived |
| Agent adoption in presales engagements | 0% (no agent today) | ≥ 70% of opportunities use agent-generated briefing as starting point | 6–9 months post-deployment | Sales enablement / Opportunity Management | agent-derived |

---

## User Profiles & Personas

### Primary Persona: Alex — Solution Architect

Alex is a 38-year-old senior solution architect at an SAP partner or regional SAP team. He works across 4–6 active customer opportunities at any given time, each requiring a tailored briefing document before the key decision-making meeting. Alex has deep SAP product knowledge but spends a disproportionate share of his week in research and document assembly rather than customer-facing work. He is confident with technical tools but frustrated by the lack of automation in the presales process. He needs a tool that does the research and structuring work for him — he wants to review and refine, not build from scratch.

**Goals:**
- Produce a customer-specific briefing document in under 30 minutes
- Be certain every BOM item is justified with SAP best practices
- Never miss an entitlement that strengthens the business case
- Walk into a customer meeting with a document he can both hand over and present live

**Pain Points:**
- Manually cross-referencing SAP product knowledge per SKU is time-consuming and inconsistent
- Entitlement data embedded in SKUs is rarely surfaced in briefings — it is often overlooked
- Integration layer sections are frequently underdeveloped due to time pressure
- Briefing quality varies significantly depending on how much prep time is available

### Secondary Persona: Dana — Presales Consultant

Dana is a 31-year-old presales consultant who supports Alex in customer-facing engagements. She consumes the briefing document produced by Alex and uses it during product demonstrations and value workshops. Dana needs the document to be structured as a presentation guide — clear sections, quotable justifications, and flagged talking points. She is not the one building the document but relies on its quality directly.

### Other User Types

- **Account Executive** — uses the briefing output to reinforce the commercial business case with the customer's procurement and finance stakeholders
- **Practice Lead / Reviewer** — reviews briefing documents for quality assurance before customer delivery

---

## User Goals & Tasks

### For Alex (Solution Architect):

**Goals:**
- Start a briefing session by providing whatever inputs are available (BOM, architecture doc, transcripts) and receive a complete data checklist before any output is generated
- Upload missing data items in response to the agent's completeness report and confirm readiness to proceed
- Receive a structured briefing document that covers all required sections with inline flags for any remaining gaps

**Key Tasks:**
1. Initiate agent session and provide initial inputs (BOM list, architecture document, meeting notes, entitlement sheet — any combination)
2. Review the data completeness report produced by the agent
3. Upload missing files or explicitly skip unavailable items
4. Confirm readiness to proceed
5. Review the generated briefing document
6. Use the briefing as both a customer-facing document and a live presentation guide

### For Dana (Presales Consultant):

**Goals:**
- Receive a briefing document that is structured for live use, not just reading
- Understand which sections are fully researched and which are flagged as partial

**Key Tasks:**
1. Review the briefing document section by section before a customer meeting
2. Use flagged sections as prompts to follow up with Alex on missing data
3. Present key justifications and entitlement highlights during the customer session

---

## Product Principles

1. **Data gate before output** — the agent never generates a briefing with silent gaps. Every session starts with a completeness check; output only begins after the architect confirms inputs.
2. **Transparency over completeness** — a partial briefing with clear inline flags is always preferable to a complete-looking briefing with unacknowledged gaps.
3. **SAP knowledge first** — all product justifications, entitlement highlights, and integration examples are grounded in SAP Knowledge Connector content, not LLM inference.
4. **Customer-specific, not generic** — One360 customer intelligence must be incorporated into every briefing. A generic briefing is not an acceptable output.
5. **Dual-purpose output** — every briefing must work as a standalone document for the customer and as a structured talking-points guide for the architect.

---

## Business Context

**Current State:**  
Solution architects manually research SAP product documentation, best practices, and entitlement details per engagement. Customer context is gathered informally from meeting notes and CRM records. There is no unified tooling. Briefing quality depends entirely on individual effort and available time. Integration layer sections are frequently underwritten. Entitlement highlights are routinely missed.

**Strategic Alignment:**  
This agent directly supports the SAP Opportunity to Quote process (BPS-360_001 — Sell Products and Services, Lead to Cash E2E). It accelerates presales velocity, improves win rate through stronger business cases, and reduces the cost of engagement preparation.

---

## Goals and Non-Goals

### Goals (In Scope)

- Data completeness gate: audit all inputs before generating any output and present a structured checklist to the architect
- Accept all combinations of: BOM list, to-be architecture document, meeting notes/transcripts, entitlement reference sheet (manual uploads where no connector exists)
- Query SAP Knowledge Connector for product descriptions, best-practice justifications, and integration guidance per BOM item
- Query One360 Connector for customer account intelligence (history, landscape, strategic priorities)
- Generate a structured briefing document with: BOM explanation, justification, entitlement highlights, integration layer narrative with examples
- Inline flag any section built on incomplete or missing input data
- Produce output suitable for both standalone customer reading and live presentation use

### Non-Goals (Out of Scope)

- Generating commercial proposals, pricing sheets, or contracts
- Direct integration with CRM opportunity management systems (e.g. SAP Sales Cloud) in this release
- Real-time entitlement data retrieval via API (Entitlement Management APIs are not in the connected landscape; entitlement data is supplied manually)
- Building or modifying the customer's BOM — the agent explains and justifies it, it does not create or edit it
- Multi-language output (English only in initial release)

---

## Requirements

### Must-Have Requirements

**R01: Data Completeness Gate**

- **Problem to Solve**: Architects have no visibility into which data is missing before a briefing is generated, resulting in silently incomplete outputs.
- **User Story**: As a solution architect, I need the agent to audit my inputs and show me exactly what is missing before generating any content, so that I can decide what to upload and what to skip.
- **Acceptance Criteria**:
  - Given the architect initiates a session, when any required data domain is absent, then the agent presents a completeness report listing each domain as present (✅), missing (⚠️), or connected (connector live); the LeanIX Connector is queried automatically — if no data exists for the customer account, it is reported as "⚠️ No LeanIX data found for this account" with the option to upload a manual export
  - Given the completeness report is presented, when the architect uploads a missing file, then the agent updates the report to reflect the new input
  - Given the completeness report is presented, when the architect types "skip [item name]", then the agent marks that domain as skipped and proceeds without it
  - Given all items are either provided or explicitly skipped, when the architect confirms to proceed, then and only then does the agent begin briefing generation
- **Maps to Objective**: Objective 2 — guarantee data completeness transparency
- **Priority Rank**: 1

**R02: SAP Knowledge Retrieval per BOM Item**

- **Problem to Solve**: Architects spend hours manually looking up SAP product descriptions, best practices, and entitlement details per SKU.
- **User Story**: As a solution architect, I need the agent to automatically retrieve SAP best-practice content, justification rationale, and entitlement details for each item in the BOM, so that I do not have to research these manually.
- **Acceptance Criteria**:
  - Given a BOM list is provided, when the agent processes it, then it queries the SAP Knowledge Connector for each BOM item and retrieves: product description, SAP best-practice justification, and any entitlements embedded in that SKU
  - Given a BOM item returns no entitlement data from the knowledge connector, when generating the briefing, then the agent flags that item inline with "⚠️ Entitlement data not available — please supply an entitlement reference sheet"
- **Maps to Objective**: Objective 1 — eliminate manual briefing research
- **Priority Rank**: 2

**R03: Customer Enterprise Architecture Enrichment via LeanIX**

- **Problem to Solve**: The integration layer and to-be architecture sections of the briefing are generic because the agent has no visibility into the customer's actual application landscape, existing interfaces, or capability gaps.
- **User Story**: As a solution architect, I need the agent to automatically query LeanIX for the customer's enterprise architecture data, so that the integration layer justification and to-be architecture narrative reflect the customer's real environment rather than a generic SAP reference model.
- **Acceptance Criteria**:
  - Given the customer name or account ID is provided, when the agent runs Phase 1, then it automatically queries the LeanIX Connector to check whether architecture data exists for that customer account
  - Given LeanIX data is found, when generating the briefing, then the integration layer and to-be architecture sections incorporate the customer's actual application landscape, existing interfaces, and identified capability gaps from LeanIX
  - Given LeanIX returns no data for the customer account, then the agent reports "⚠️ No LeanIX data found for this account" in the completeness report and offers the architect the option to upload a manually exported LeanIX summary or proceed without it
  - Given the architect uploads a manual LeanIX export, then the agent parses and uses it as a substitute for live connector data
  - Given neither LeanIX data nor a manual export is available, then the integration layer and to-be architecture sections are flagged inline as "partial — based on SAP reference model only, not customer-specific landscape"
- **Maps to Objective**: Objective 3 — dual-purpose output grounded in customer reality; Objective 4 — integration layer explanation with examples
- **Priority Rank**: 3

**R04: Customer Intelligence Enrichment via One360**

- **Problem to Solve**: Briefings are generic and not tailored to the specific customer's landscape, history, or strategic priorities.
- **User Story**: As a solution architect, I need the agent to pull the customer's account intelligence from One360 and incorporate it into the briefing, so that every section is contextualised to that specific customer.
- **Acceptance Criteria**:
  - Given the customer name or account ID is provided, when the agent runs, then it queries the One360 Connector and retrieves: account history, current landscape, known strategic priorities, and relevant relationship context
  - Given One360 data is retrieved, when generating the briefing, then customer-specific context is woven into the BOM justification and integration sections
  - Given One360 is unreachable, then the agent flags the customer intelligence section as partial and proceeds with available data
- **Maps to Objective**: Objective 1 — eliminate manual research; Objective 3 — dual-purpose output
- **Priority Rank**: 4

**R05: Structured Briefing Document Generation**

- **Problem to Solve**: There is no consistent structure or format for briefing documents across the presales team.
- **User Story**: As a solution architect, I need the agent to produce a structured briefing document with all required sections, so that I can hand it to the customer and present it live without reformatting.
- **Acceptance Criteria**:
  - Given all data gate conditions are met, when the agent generates the briefing, then it produces a document containing all of the following sections:
    1. Customer overview (from One360)
    2. BOM item explanations (plain language, per SKU)
    3. Justification for each BOM item (SAP best practices rationale)
    4. Entitlement highlights per SKU (what is included within a given product bundle)
    5. Integration layer explanation with examples, grounded in LeanIX customer landscape data where available
  - Given any section is built on incomplete data, then it is flagged inline with a clear warning and the reason
  - Given the document is complete, then it is formatted to serve both independent reading and live presentation use
- **Maps to Objective**: Objectives 1, 3, 4
- **Priority Rank**: 5

**R06: Manual File Upload Fallback for Missing Connectors**

- **Problem to Solve**: Several required data domains (entitlement reference, to-be architecture, BOM list, meeting notes) have no available Joule Desktop Hub connector, meaning data cannot be retrieved automatically.
- **User Story**: As a solution architect, I need to be able to upload missing data files manually at runtime, so that the agent can still produce a complete briefing even when connectors are unavailable.
- **Acceptance Criteria**:
  - Given the completeness report lists a missing item with no connector, when the architect uploads a file (PDF, DOCX, CSV, Excel, plain text), then the agent parses and incorporates it into the briefing
  - Given an uploaded file cannot be parsed, then the agent notifies the architect with the reason and requests an alternative format
- **Maps to Objective**: Objective 2 — data completeness transparency
- **Priority Rank**: 6

### High-Want Requirements

**R07: Inline Gap Flags in Final Document**

- **Problem to Solve**: Architects and consultants need to know at a glance which sections of the briefing are fully researched versus which are partial.
- **User Story**: As a presales consultant, I need incomplete sections to be clearly marked in the document, so that I know what to follow up on before a customer meeting.
- **Acceptance Criteria**:
  - Each section built on incomplete data includes a visible inline flag with the reason and a suggested action (e.g. "upload entitlement reference sheet")
- **Priority Rank**: 1

**R08: Input Templates for Manual Uploads**

- **Problem to Solve**: Manual uploads vary in format and quality, reducing the agent's ability to extract useful context.
- **User Story**: As a solution architect, I need the agent to provide recommended input templates for each manual upload type, so that I can format my inputs in a way the agent can reliably parse.
- **Acceptance Criteria**:
  - Agent provides a downloadable or displayable template for: BOM list, entitlement reference sheet, meeting notes, and to-be architecture summary
- **Priority Rank**: 2

---

## Non-Functional Requirements

### Performance
- **Latency**: Briefing generation (Phase 2) must complete within 3 minutes for a BOM of up to 20 line items
- **Throughput**: Agent must support concurrent sessions for at least 10 architects simultaneously

### Reliability
- **Availability**: 99.5% uptime during business hours (UTC 06:00–20:00)
- **Fallback**: If SAP Knowledge Connector is unavailable, the agent notifies the architect and halts generation — it does not produce a briefing without the primary knowledge source

### Explainability
- **Traceability**: Each briefing section must be traceable to its source (knowledge connector response, One360 data, or uploaded file)
- **Uncertainty Communication**: Incomplete sections are always flagged inline with source and reason

---

## Solution Architecture

**Architecture Overview:**  
A Python-based AI agent deployed on SAP AI Core (A2A protocol). The agent operates in two strict phases: a data completeness gate (Phase 1) and briefing generation (Phase 2). It integrates with SAP Knowledge Connector and One360 Connector as primary MCP tools, and accepts manual file uploads for data domains without available connectors.

**Key Components:**

- **Presales Briefing Agent** — core Python agent (A2A protocol), orchestrates both phases, manages tool calls and file parsing
- **SAP Knowledge Connector** (MCP) — primary source for SAP product descriptions, best practices, entitlement data, and integration guidance
- **One360 Connector** (MCP) — customer 360 intelligence source (account history, landscape, strategic priorities)
- **LeanIX Connector** (MCP) — customer enterprise architecture source (application landscape, capability map, interface inventory, technology portfolio); queried automatically when LeanIX data exists for the customer account; provides the most accurate basis for integration layer justification and to-be architecture contextualisation
- **File Ingestion Module** — parses architect-uploaded files (PDF, DOCX, CSV, Excel, plain text) for: BOM list, to-be architecture, entitlement reference sheet, meeting notes
- **Briefing Document Generator** — assembles the structured output document from all retrieved and parsed data, applies inline gap flags where data is missing

**Integration Points:**

| System | Purpose | Direction | Connector Available |
|--------|---------|-----------|---------------------|
| SAP Knowledge Connector | Product knowledge, best practices, entitlements, integration guidance | Read | Yes — Joule Desktop Hub |
| One360 Connector | Customer 360 intelligence | Read | Yes — Joule Desktop Hub |
| LeanIX Connector | Customer enterprise architecture — application landscape, capability map, interface inventory, technology portfolio | Read | Yes — if LeanIX is configured and customer account data exists; agent checks automatically and falls back to manual upload or partial flag if no data found |
| S/4HANA BOM API (`sap.s4:apiResource:API_BILL_OF_MATERIAL_SRV_0002:v2`) | Live BOM lookup (secondary, future) | Read | Partial — API available, no MCP server yet |
| Manual file upload | BOM list, to-be architecture, entitlement sheet, meeting notes, LeanIX export (if connector returns no data) | Inbound | No connector — manual upload fallback |

### Agent Extensibility & Instrumentation

**Agent Extensibility:**
- The agent is designed with extension points to support future capability additions without core rewrites:
  - **New connector extension point** — additional MCP connectors (e.g. future Entitlement Management connector, SAP CPQ connector) can be registered as tools without modifying the core orchestration logic
  - **New briefing section extension point** — additional output sections (e.g. competitive comparison, pricing narrative) can be added as modular generation steps
  - **New input type extension point** — additional file formats or live API sources can be added to the file ingestion module independently
- All agent business logic steps are instrumented with structured log statements (see Milestones section) to support observability in SAP AI Core

**Business Step Instrumentation:**
- All key business logic steps emit structured log statements following the pattern: `[MILESTONE_ID].[achieved|missed]: [description]`
- Logs are emitted in real-time as each milestone is reached or skipped
- Instrumentation enables monitoring of agent behaviour, debugging of incomplete runs, and future analytics on briefing quality and input patterns

### Automation & Agent Behaviour

**Automation Level:** Autonomous agent with mandatory human confirmation gate

**Actions the agent performs without human approval:**
- Querying SAP Knowledge Connector for each BOM item
- Querying One360 Connector for customer intelligence
- Parsing uploaded files
- Assembling the structured briefing document

**Actions that require human review or approval:**
- Proceeding past the data completeness gate — architect must explicitly confirm (or skip items) before briefing generation begins
- Deciding which incomplete sections to flag versus skip — architect controls this via the "skip [item name]" command

**Model / engine used:** SAP Generative AI Hub (GPT-4o or equivalent) via SAP AI Core

**Knowledge & data sources accessed:**

| Source | Purpose | Data Stewardship |
|--------|---------|-----------------|
| SAP Knowledge Connector | SAP product descriptions, best practices, entitlements, integration patterns | SAP-managed |
| One360 Connector | Customer account history, landscape, strategic priorities | SAP-managed (internal sales intelligence) |
| LeanIX Connector | Customer application landscape, capability map, interface inventory, technology portfolio — used to ground the to-be architecture and integration layer sections in the customer's real environment | Customer-managed (LeanIX instance); agent queries automatically and falls back gracefully if no data found for the account |
| Architect-uploaded files | BOM list, to-be architecture, entitlement reference, meeting notes, LeanIX export (manual fallback) | Architect-owned; session-scoped only |

**Guardrails & fail-safes:**
- Agent MUST NOT generate any briefing content before the data completeness gate is cleared by the architect
- Agent MUST NOT invent or infer entitlement data if no entitlement source is provided — it must flag the gap
- If SAP Knowledge Connector is unavailable, agent halts and notifies the architect — it does not fall back to LLM-generated product knowledge
- Uploaded files are used only within the current session and are not persisted
- Agent does not write to any external system — all outputs are read-only documents returned to the architect

### Configuration & Data

**Configuration Scope:**
- SAP Knowledge Connector and One360 Connector must be configured as registered MCP tools in Joule Desktop Hub before deployment
- Agent session configuration: customer name/account ID (required for One360 query), BOM item list (required or uploaded)

**Data Handling:**
- No customer PII is stored beyond the current session
- Uploaded files are treated as session-scoped inputs and not persisted after the session ends

---

## Goals and Non-Goals

### Goals (In Scope)
- Data completeness gate with architect confirmation before output
- SAP Knowledge Connector integration for BOM item knowledge retrieval
- One360 Connector integration for customer intelligence
- Manual file upload fallback for all data domains without connectors
- Structured briefing document with inline gap flags
- Dual-purpose output (standalone document + presentation guide)

### Non-Goals (Out of Scope)
- Commercial proposal or pricing generation
- CRM opportunity record creation or update
- Real-time entitlement API integration (deferred to future release when connector becomes available)
- BOM creation or modification
- Multi-language output (English only, initial release)

---

## Milestones

### M1: Data Completeness Gate

- **Description**: Agent audits all inputs and presents the architect with a structured completeness report covering all required data domains
- **Achieved when**: Completeness report is generated and presented to the architect, listing each domain as connected, provided, missing, or skipped
- **Log on achievement**: `M1.achieved: data completeness gate report generated — [N] domains connected, [N] provided, [N] missing, [N] skipped`
- **Log on miss**: `M1.missed: data completeness gate did not complete — agent halted before report generation`

### M2: Architect Confirmation Received

- **Description**: Architect has reviewed the completeness report, uploaded missing items or explicitly skipped them, and confirmed readiness to proceed
- **Achieved when**: Architect sends confirmation signal after addressing the completeness report
- **Log on achievement**: `M2.achieved: architect confirmed readiness to proceed — all domains resolved (provided, connected, or skipped)`
- **Log on miss**: `M2.missed: architect confirmation not received — briefing generation blocked`

### M3: SAP Knowledge Retrieval Complete

- **Description**: Agent has queried SAP Knowledge Connector for all BOM items and retrieved product descriptions, best-practice justifications, and entitlement data
- **Achieved when**: All BOM items have been processed through the knowledge connector; items with no entitlement data are flagged
- **Log on achievement**: `M3.achieved: SAP knowledge retrieved for [N] BOM items — [N] with entitlement data, [N] flagged as missing entitlement`
- **Log on miss**: `M3.missed: SAP Knowledge Connector unavailable or returned no results — briefing generation halted`

### M4: LeanIX Enterprise Architecture Retrieved

- **Description**: LeanIX Connector queried for the customer account; enterprise architecture data (applications, capabilities, interfaces) retrieved and staged for use in the integration layer and to-be architecture sections
- **Achieved when**: LeanIX returns data for the customer account and it is successfully parsed
- **Log on achievement**: `M4.achieved: LeanIX architecture data retrieved — [N] applications, [N] interfaces, [N] capability gaps identified for customer account`
- **Log on miss**: `M4.missed: no LeanIX data found for customer account — integration layer and to-be architecture sections will use SAP reference model only`

### M5: Customer Context Enriched via One360

- **Description**: One360 Connector queried and customer intelligence incorporated into briefing context
- **Achieved when**: One360 returns account data that is successfully parsed and staged for briefing assembly
- **Log on achievement**: `M5.achieved: customer context enriched from One360 — account history, landscape, and strategic priorities incorporated`
- **Log on miss**: `M5.missed: One360 data unavailable or not provided — customer intelligence section will be flagged as partial`

### M6: Briefing Document Generated and Delivered

- **Description**: All data is assembled, the structured briefing document is generated with inline flags for any gaps, and delivered to the architect
- **Achieved when**: Final document is returned containing all required sections; all incomplete sections are flagged inline
- **Log on achievement**: `M6.achieved: briefing document generated — [N] sections complete, [N] sections flagged as partial`
- **Log on miss**: `M6.missed: briefing generation failed — document not produced`

---

## Risks, Assumptions, and Dependencies

### Risks

- **Entitlement data completeness**: No Entitlement Management connector exists in Joule Desktop Hub. If the architect does not supply an entitlement reference sheet, entitlement highlights will be absent for all BOM items. Mitigation: agent clearly prompts for the file during the data completeness gate.
- **Manual input quality**: Uploaded files (especially meeting notes and architecture documents) vary in structure. Poor-quality inputs will reduce briefing depth. Mitigation: agent provides recommended input templates per data type.
- **Knowledge connector coverage**: If SAP Knowledge Connector does not cover a specific SKU or product version, justification for that item will be shallow. Mitigation: agent flags the gap and architect can supplement with manual reference material.
- **One360 data currency**: One360 intelligence reflects account data as of the last sync. Stale data may produce outdated customer context. Mitigation: briefing notes the date of the One360 data retrieved.
- **LeanIX data availability**: Not all customers will have LeanIX data in the connected instance. When absent, the integration layer falls back to the SAP reference model. Mitigation: agent clearly flags this in the completeness report and offers a manual LeanIX export upload as an alternative.
- **LeanIX data completeness**: Even when LeanIX is available, not all customers maintain up-to-date fact sheets. Partial LeanIX data (e.g. applications catalogued but interfaces not mapped) will still improve the briefing but should be noted as potentially incomplete. Mitigation: agent notes the LeanIX data snapshot date and coverage level in the briefing.

### Assumptions (Validate These)

- SAP Knowledge Connector is available and configured in Joule Desktop Hub at time of deployment
- One360 Connector is available and configured in Joule Desktop Hub at time of deployment
- LeanIX Connector is available and configured in Joule Desktop Hub; LeanIX data availability is customer-dependent — the agent handles gracefully when no data exists for a given account
- Architects will have access to an entitlement reference sheet (SKU-to-entitlement mapping) exportable from SAP's price list or CPQ for manual upload
- S/4HANA BOM API will be made MCP-enabled in a future release, replacing the manual BOM upload fallback

### Dependencies

- Joule Desktop Hub connector configuration: SAP Knowledge Connector, One360 Connector, and LeanIX Connector must be registered before the agent is usable
- SAP AI Core availability for agent runtime
- Architect access to customer account in One360 (account-level access control applies)

---

## Open Questions

- When the S/4HANA BOM API (`sap.s4:apiResource:API_BILL_OF_MATERIAL_SRV_0002:v2`) gains an MCP server, should it replace or complement the manual BOM upload fallback?
- Should the agent support a "re-run" capability where the architect can upload additional files after reviewing a partial briefing and regenerate specific sections only?
- Is there a target document format for the briefing output (e.g. Markdown, Word-compatible, PDF-ready)?

---

## Appendix

### Glossary

- **BOM (Bill of Materials)**: A list of SAP SKUs and products proposed as part of a customer solution
- **SKU**: A specific purchasable SAP product or service line item
- **Entitlement**: A product right or capability that is included within a given SKU at no additional cost
- **One360**: SAP's internal customer 360 intelligence platform, used by SAP sellers and partners to view account history, landscape, and strategic context
- **SAP Knowledge Connector**: A Joule Desktop Hub connector providing access to SAP's product knowledge base, best practices, and reference architecture content
- **Data Completeness Gate**: The mandatory first phase of every agent session in which inputs are audited and gaps are reported to the architect before any briefing content is generated
- **LeanIX**: SAP's enterprise architecture management platform. It holds the customer's application landscape, business capability map, interface inventory, and technology portfolio. Used by the agent to ground the integration layer and to-be architecture sections in the customer's real environment rather than a generic SAP reference model.
- **A2A Protocol**: Agent-to-Agent protocol used by SAP AI Core for Python-based agent deployment

### References

- SAP Reference Business Architecture — Lead to Cash, BPS-360_001 (Sell Products and Services)
- SAP AI Core documentation
- Joule Desktop Hub connector configuration guide
- SAP Knowledge Graph — product capability fit-gap analysis results
