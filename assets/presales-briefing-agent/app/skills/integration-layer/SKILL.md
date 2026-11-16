---
name: integration-layer
description: |
  [WHAT] Generates the integration layer section of the briefing, grounding integration recommendations in the customer's real application landscape from LeanIX and SAP best-practice integration patterns from the SAP Knowledge Connector.
  [WHEN] Use during Phase 2 when generating the Integration Layer section of the briefing document.
  [NOT] Do not use for BOM item explanations or entitlement content — use bom-justification instead.
  Key terms: integration, LeanIX, interfaces, application landscape, integration patterns, to-be architecture.
allowed-tools:
  - Read
metadata:
  version: 1.0.0
  tags:
    - presales
    - integration
    - leanix
    - architecture
---

# Integration Layer

## Purpose

This skill generates the integration layer section of the briefing document. It uses LeanIX enterprise architecture data (when available) to contextualise integration recommendations against the customer's real application landscape and existing interfaces. When LeanIX data is unavailable, it falls back to SAP reference architecture patterns and clearly flags the limitation.

## When to use

- During Phase 2, when generating the Integration Layer section of the briefing
- When the architect asks "how do these products integrate?" or "explain the integration architecture"

## When NOT to use

- Before the data completeness gate is cleared
- For BOM item content — use bom-justification instead

---

## Instructions

### Step 1 — Assess available integration data sources

The integration narrative is built from two sources in priority order:

| Source | What it provides | How to use |
|--------|-----------------|------------|
| Architect-uploaded to-be architecture document | Customer's specific target landscape, existing systems, planned integrations | Primary — use if provided |
| ibd-mcp-server (sap_knowledge_graph_fit_gap + sap_help_search) | SAP-recommended integration patterns, pre-built content, best practices | Always available — use as foundation or sole source if no document uploaded |

If neither a to-be architecture document nor meeting notes were provided, base the integration section entirely on SAP reference patterns from ibd-mcp-server and flag it:
"Note: This integration narrative is based on SAP reference architecture. For a customer-specific integration view, upload the customer's to-be architecture document."

### Step 2 — Map proposed BOM products to integration touchpoints

For each pair of products in the BOM that have a direct integration relationship:
1. Identify the integration pattern from SAP Knowledge Connector (e.g. SAP Integration Suite, direct API, event-based, embedded)
2. If LeanIX data is available: identify the customer's existing systems that the proposed products will connect to or replace
3. Describe the data flow direction and frequency

### Step 3 — Generate integration narrative

Structure the integration layer section as:

**When LeanIX data IS available:**
```
### Integration Architecture

**Current landscape context**
[2-3 sentences describing the customer's existing relevant applications and interfaces from LeanIX, 
naming specific systems where available]

**How the proposed solution integrates**
For each key integration point:
- [Product A] ↔ [Product B / existing system]: [integration pattern], [data flow], [SAP best practice rationale]

**Integration examples**
[Concrete example 1: describe a specific business transaction flowing across the integration, 
naming the systems and the data exchanged]
[Concrete example 2: another transaction example]

**Talking points** (architect guide)
- [Key integration talking point 1]
- [Key integration talking point 2]
- [Key integration talking point 3]
```

**When LeanIX data is NOT available:**
```
### Integration Architecture

WARNING This section is based on the SAP reference integration model only, not the customer's specific application landscape. For a customer-specific integration narrative, please provide LeanIX data (connected or manual export).

**SAP reference integration patterns for the proposed solution**
[Describe the standard SAP integration patterns for the BOM products, 
using SAP Knowledge Connector content only]

**Talking points** (architect guide)
- [Key integration talking point 1]
- [Key integration talking point 2]
```

### Step 4 — Add integration advisory note

Always append a note at the end of the section:
"For a detailed integration assessment, SAP Integration Advisory (available through SAP Integration Suite) provides a structured methodology to map integration requirements to the customer's specific landscape."

---

## Gotchas

- **Never invent customer system names or interfaces** — only reference systems that appear in LeanIX data or uploaded architecture documents. If a system is not in the data, do not name it.
- **The partial flag is mandatory when LeanIX is absent** — do not omit it or bury it at the end. It must appear at the top of the integration section.
- **SAP Knowledge Connector is still required** — even when LeanIX data is available, the SAP best-practice integration patterns must come from the knowledge connector, not from LLM inference.
