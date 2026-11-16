# SAP Presales Briefing Consultant Agent

SAP Presales Briefing Consultant Agent — an AI agent that helps solution architects generate tailored, customer-specific briefing documents for proposed SAP solution BOM items.

## Business Challenge

Solution architects spend 4–8 hours manually researching SAP products, justifying BOM items, and synthesising customer context before each presales engagement. There is no automated way to combine SAP best practice knowledge, customer history (meeting notes, transcripts), the customer's to-be architecture, and One360 intelligence into a structured, presentation-ready briefing document. This results in inconsistent quality, missed entitlement highlights, and weak integration-layer explanations that undermine the business case.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Time to produce a customer briefing document | ~4–8 hours (manual research + writing) | < 30 minutes with agent | 3–6 months post-deployment | Presales engagement / Opportunity to Quote | agent-derived |
| Briefing acceptance rate (no major rework by architect) | ~50% (estimated) | ≥ 80% of briefings used without significant revision | 6 months post-deployment | Solution quality / Customer Quotation Management | agent-derived |
| Agent adoption in presales engagements | 0% (no agent today) | ≥ 70% of presales opportunities use agent-generated briefing as starting point | 6–9 months post-deployment | Sales enablement / Opportunity Management | agent-derived |

## Key Milestones

1. **Data completeness check** — Before any processing, the agent reviews all inputs received and produces a clear checklist of what is present and what is missing across all required data domains (BOM list, to-be architecture, meeting notes/transcripts, entitlement reference sheet). The agent MUST NOT proceed to any subsequent step until the architect has either uploaded the missing items or explicitly confirmed they are unavailable.
2. **Input ingestion complete** — Agent successfully parses all uploaded and connector-sourced inputs. For each missing item the architect confirmed as unavailable, the agent marks the corresponding briefing section as "partial — limited input" rather than skipping it silently.
3. **SAP knowledge retrieval** — Agent queries SAP Knowledge Connector and retrieves relevant product descriptions, best practice justifications, and entitlement details for each BOM item.
4. **Customer context enriched** — One360 connector called and customer-specific intelligence (account history, current landscape, strategic initiatives) incorporated into the briefing context.
5. **Briefing document generated** — Agent produces a structured document with all required sections: BOM explanation, justification, entitlement highlights, and integration layer narrative. Sections with incomplete data are clearly flagged inline.
6. **Document delivered to architect** — Briefing is returned in a format suitable for both independent customer reading and use as a live presentation guide.

## Business Architecture (RBA)

### End-to-End Process

Lead to Cash — Standard B2B

### Process Hierarchy

```
Lead to Cash (Standard B2B)
└── Opportunity to Quote
    └── Sell Products and Services (BPS-360_001)
        └── Manage sales proposals, bids, and quotes
        └── Justify and document proposed solution BOM items
        └── Highlight entitlements embedded in SKUs
        └── Explain integration layer with examples
```

### Summary

The agent's primary purpose maps to the "Opportunity to Quote" phase of the Lead to Cash E2E process, specifically the sub-process of selling products and services (BPS-360_001). It automates the creation of customer-facing briefing materials that justify BOM proposals — a critical activity in SAP solution sales.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|-------------------------|------------|-------------------|--------------------|--------------------|---------------------|------|---------------------|
| Access SAP product best practices and BOM descriptions | SAP Knowledge Connector (internal) | — | — | — | — | — | No | SAP knowledge connector used as primary MCP source; no external API ORD ID discoverable |
| Retrieve customer 360 context (account, history, initiatives) | SAP One360 Connector | — | — | — | — | — | No | One360 is SAP's internal customer intelligence platform; connector used directly by agent |
| Parse customer to-be architecture / BOM input | Custom agent input handling | — | — | — | — | — | No | Agent accepts free-text or structured document input from architect at runtime |
| Parse meeting notes / transcripts | Custom agent input handling | — | — | — | — | — | No | Agent processes uploaded or pasted transcript text as context |
| Retrieve BOM / Bill of Materials data | Bills of Material (S/4HANA) | `sap.s4:apiResource:API_BILL_OF_MATERIAL_SRV_0002:v2` | — | — | — | — | Maybe | No MCP server found; API available in landscape; BOM context may come from architect input rather than live query |
| Generate structured briefing document | AI Agent (custom) | — | — | — | — | — | No | Core agent capability; no standard SAP product covers automated briefing generation |
| Justify BOM items with SAP best practices | SAP Knowledge Connector | — | — | — | — | — | No | Agent uses SAP knowledge graph and best practice content via knowledge connector |
| Highlight entitlements embedded in SKUs | SAP Knowledge Connector + agent reasoning | — | — | — | — | — | Maybe | Entitlement APIs not available in connected landscape; agent must derive from knowledge sources |
| Explain integration layer with examples | Agent reasoning + SAP Integration Advisory | — | — | — | — | — | Maybe | No dedicated integration advisory API found; agent uses SAP knowledge to construct examples |

### Key findings

- SAP's internal **Knowledge Connector**, **One360 Connector**, and **LeanIX Connector** are the three primary data sources and must be configured as MCP tools for the agent where available.
- All Entitlement Management APIs and Customer Master Data APIs are **not in the connected system** — the agent must derive entitlement highlights from SAP knowledge content rather than live API queries.
- The BOM API (`sap.s4:apiResource:API_BILL_OF_MATERIAL_SRV_0002:v2`) is available but has no MCP server; it can be used as a secondary lookup if the architect needs to retrieve live BOM data from S/4HANA.
- Integration layer explanations will rely on the agent's reasoning over SAP best-practice knowledge, as no dedicated integration advisory API is available.
- The agent must handle multiple input types at runtime (documents, BOM lists, transcript text) and produce a single coherent briefing output.
- Output format must serve dual purpose: standalone customer document and architect talking-points guide.
- LeanIX data, when available for the customer, provides the most accurate basis for integration layer justification and to-be architecture contextualisation — it should be queried automatically before falling back to manual upload or generic knowledge connector content.

### Data Completeness & Connector Strategy

The table below defines each data domain required by the agent, the expected Joule Desktop Hub connector, and the fallback approach when no connector is available.

| Data Domain | What Would Be Incomplete Without It | Joule Desktop Hub Connector | Connector Available? | Fallback (if no connector) |
|-------------|-------------------------------------|-----------------------------|----------------------|----------------------------|
| **SAP Product Best Practices & Knowledge** | BOM item descriptions, justification rationale, and SAP reference architecture context would be missing or generic | SAP Knowledge Connector | Yes | N/A — connector is available and mandatory |
| **Customer 360 Intelligence** | Account history, strategic priorities, existing landscape, and relationship context would be absent — briefing becomes generic rather than tailored | One360 Connector | Yes | N/A — connector is available and mandatory |
| **SAP Entitlement Data per SKU** | Entitlement highlights embedded in a given SKU (e.g. what is included "for free" within a product bundle) would be incomplete or missed entirely | No dedicated Entitlement connector available in Joule Desktop Hub | No | Architect manually uploads an entitlement reference sheet (e.g. SKU-to-entitlement mapping exported from SAP's price list or CPQ) as a file input before running the agent |
| **Customer To-Be Architecture** | Integration layer narrative and BOM justification cannot be contextualised to the customer's target landscape | No dedicated architecture connector available in Joule Desktop Hub | No | Architect uploads the to-be architecture document (PDF, DOCX, or plain text) as a file input at agent runtime |
| **Customer Bill of Materials (BOM)** | Agent cannot explain or justify specific SKUs if none are provided; output defaults to generic SAP product descriptions | No dedicated BOM connector in Joule Desktop Hub; S/4HANA BOM API available but no MCP server | Partial — API exists (`sap.s4:apiResource:API_BILL_OF_MATERIAL_SRV_0002:v2`) but not yet MCP-enabled | Architect pastes or uploads the BOM list (CSV, Excel, or plain text) as a manual input; S/4HANA API can be used as a secondary live lookup once an MCP translation file is built |
| **Meeting Notes & Transcripts** | Customer-specific pain points, agreed priorities, and prior commitments from previous meetings would not be reflected in the briefing | No dedicated meeting notes connector available in Joule Desktop Hub | No | Architect uploads or pastes meeting notes / call transcripts as a text file input at runtime |
| **SAP Integration Advisory Content** | Integration layer explanations would lack concrete examples and SAP-recommended patterns; rationale would be superficial | SAP Knowledge Connector (partial coverage) | Partial — knowledge connector covers some integration guidance | Where knowledge connector does not cover a specific integration scenario, architect uploads relevant SAP integration reference materials or integration assessment outputs manually |
| **Customer Enterprise Architecture (LeanIX)** | Without the customer's actual application landscape, capability map, and interface inventory from LeanIX, the to-be architecture justification and integration layer narrative will be generic and disconnected from the customer's real environment | SAP LeanIX Connector | Yes — if LeanIX is configured in the customer's landscape and data exists for that account | If no LeanIX data exists for the customer, architect uploads a manually exported architecture summary or the agent proceeds without it (section flagged as partial) |

## Recommendations

### AI Presales Briefing Consultant Agent

#### Executive Summary

An AI agent that turns BOM inputs and customer context into ready-to-use briefing docs.

#### Recommended Solution

A Python-based AI agent (A2A protocol) that operates in two mandatory phases before producing any output:

**Phase 1 — Data Completeness Gate (mandatory, blocking):**
Before doing anything else, the agent audits all inputs received against the full list of required data domains and presents the architect with a structured completeness report, for example:

```
Data Completeness Check
───────────────────────────────────────────────────────
✅ SAP Knowledge Connector          Connected
✅ One360 Customer Intelligence     Connected
⚠️  Bill of Materials (BOM)         NOT provided — please upload a BOM list (CSV, Excel, or plain text)
⚠️  Customer To-Be Architecture     NOT provided — please upload your architecture document (PDF, DOCX, or text)
⚠️  Entitlement Reference Sheet     NOT provided — please upload a SKU-to-entitlement mapping
⚠️  Meeting Notes / Transcripts     NOT provided — please upload notes or paste transcript text

Action required: Upload the missing items above, then confirm to proceed.
If an item is unavailable, type "skip [item name]" and the corresponding briefing section will be marked as partial.
───────────────────────────────────────────────────────
```

The agent waits for the architect's response. It does NOT generate any briefing content until the architect either uploads the missing files or explicitly skips them.

**Phase 2 — Briefing Generation:**
Once the data gate is cleared, the agent queries the SAP Knowledge Connector for product best practices, entitlement details, and integration guidance, enriches with One360 customer intelligence, and generates a structured briefing document covering: plain-language BOM item explanations, SAP best practice justifications, entitlement highlights embedded in SKUs, and integration layer narratives with examples. Any section with incomplete data is flagged inline (e.g. "⚠️ Entitlement data not available for this SKU — please supply an entitlement reference sheet for a complete view"). The output is formatted to serve both as a customer-facing document and an architect's presentation guide.

#### Problem Statement

Solution architects invest 4–8 hours per engagement manually assembling briefing materials, leading to inconsistent quality, missed commercial opportunities (unreported entitlements), and weakly justified integration recommendations. There is no tooling today that connects SAP product knowledge, customer history, and best practices into a single automated output.

#### Affected User Roles

- Solution Architects (primary users — create briefings per engagement)
- Presales Consultants (consume and present briefings to customers)
- Account Executives (use briefing outcomes to strengthen business case)

#### Important factors

##### Blocking data completeness gate ensures no silent gaps
The agent always audits inputs first and presents a clear checklist of what is missing before doing any work. The architect must either upload the missing items or explicitly skip them — the agent never proceeds silently with incomplete data. Sections built on incomplete input are always flagged inline in the final document.

##### Reduces manual preparation time through automation
The agent automates the research and writing phases of briefing preparation, cutting time from hours to minutes and allowing architects to focus on customer dialogue.

##### Improves commercial completeness through entitlement visibility
By systematically querying SAP knowledge for entitlements embedded in SKUs, the agent surfaces commercial value that is frequently overlooked in manual processes.

##### Personalises content through customer intelligence integration
One360 connector provides account-specific context (strategic priorities, existing landscape, relationship history) ensuring the briefing is tailored rather than generic.

##### Enables consistent integration storytelling
The agent applies SAP best-practice integration patterns to construct coherent integration layer explanations with concrete examples — a common weakness in manually prepared briefings.

#### Potential risks

##### Accuracy of entitlement data
No dedicated Entitlement connector exists in Joule Desktop Hub. The agent relies on a manually uploaded entitlement reference sheet (SKU-to-entitlement mapping). If the architect does not provide this file, entitlement highlights in the briefing will be incomplete. Mitigation: the agent explicitly flags which BOM items have no entitlement data loaded and prompts the architect to supply it.

##### Manual input dependency for several data domains
Four data domains — entitlement data, to-be architecture, BOM list, and meeting notes — have no available connector and depend on manual file upload by the architect. If any of these are missing at runtime, the corresponding briefing section will be partial. The agent must clearly communicate which sections are complete versus which are based on limited input.

##### Quality of transcript and document parsing
Free-form meeting notes, transcripts, and architecture documents vary in structure and completeness. The agent's ability to extract meaningful customer context depends on the quality of what is uploaded. Mitigation: agent provides a recommended input template for each document type.

##### Knowledge connector and integration advisory coverage gaps
If the SAP Knowledge Connector does not cover a specific BOM item, product version, or integration scenario, the agent's justification for those items will be shallower. Mitigation: architect can supplement with manually uploaded SAP reference materials (e.g. integration assessment output, product sheets).

#### Recommended solution category

AI Agent

#### Intent fit
88%
