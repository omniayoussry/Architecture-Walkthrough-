---
name: data-completeness-gate
description: |
  [WHAT] Audits all required data domains for a presales briefing session and presents a structured completeness report to the architect before any briefing content is generated.
  [WHEN] Use at the very start of every briefing session, before any other skill is invoked. Mandatory blocking step.
  [NOT] Do not use for generating briefing content — use briefing-generator instead.
  Key terms: completeness, data gate, missing data, upload, skip, connectors.
allowed-tools:
  - Read
metadata:
  version: 1.0.0
  tags:
    - presales
    - data-completeness
    - gate
---

# Data Completeness Gate

## Purpose

This skill enforces the mandatory Phase 1 gate for every presales briefing session. It audits all required data domains, reports their status to the architect, and blocks Phase 2 (briefing generation) until all domains are resolved. No briefing content may be produced before this skill completes and the architect confirms.

## When to use

- At the start of every briefing session, before any briefing content is generated
- When the architect provides new inputs mid-session that may change the completeness status
- When the architect asks "what data do you need?" or "what is missing?"

## When NOT to use

- After the gate has already been cleared and the architect has confirmed — proceed to briefing-generator
- For generating briefing sections — use briefing-generator, bom-justification, or integration-layer skills

---

## Instructions

### Step 1 — Check connector availability

The following MCP servers are connected in this tenant:

| Connector | What it provides | Status |
|-----------|-----------------|--------|
| ibd-mcp-server | SAP knowledge graph, best practices, fit-gap analysis, SAP Help docs, API discovery | Always Connected |
| dpca-mcp-server | SAP data products in the tenant | Always Connected |

If ibd-mcp-server is unreachable: HALT. Do not proceed. Notify the architect:
"ibd-mcp-server is unreachable. This is the primary SAP knowledge source and is required to proceed."

Note: LeanIX and One360 are NOT connected in this tenant. Customer context comes entirely from architect-uploaded inputs (meeting notes, to-be architecture document).

### Step 2 — Check uploaded/provided inputs

Check what the architect has already provided in this session:

| Data Domain | Check |
|-------------|-------|
| Bill of Materials (BOM) | Was a BOM list uploaded or pasted (CSV, Excel, plain text)? |
| Customer To-Be Architecture | Was an architecture document uploaded (PDF, DOCX, text)? |
| Entitlement Reference Sheet | Was a SKU-to-entitlement mapping uploaded? |
| Meeting Notes / Transcripts | Were notes or transcript text uploaded or pasted? |

### Step 3 — Build and present the completeness report

Present the report in this exact format:

```
Data Completeness Check
-----------------------------------------------------------
CONNECTED MCP SERVERS (automatic)
[OK] ibd-mcp-server     SAP knowledge graph, best practices, fit-gap, Help docs
[OK] dpca-mcp-server    SAP data products in tenant

MANUAL INPUTS
[status] Bill of Materials (BOM)       [Provided / NOT provided]
[status] Customer To-Be Architecture   [Provided / NOT provided]
[status] Meeting Notes / Transcripts   [Provided / NOT provided]
[status] Entitlement Reference Sheet   [Provided / NOT provided — optional, fit-gap covers standard entitlements]

-----------------------------------------------------------
[If any items are NOT provided:]
Action required: Please upload the missing items above, then type "confirm" to proceed.

For each missing item, use:
- BOM list: Upload a CSV, Excel, or plain text file with product names and SKUs
- Architecture document: Upload a PDF, DOCX, or text description of the to-be landscape
- Entitlement reference sheet: Upload a SKU-to-entitlement mapping (CSV or Excel)
- Meeting notes: Upload a file or paste transcript text directly

To skip an unavailable item, type: skip [item name]
(e.g. "skip meeting notes" — the corresponding section will be flagged as partial in the output)

When all items are addressed, type "confirm" to generate the briefing.
-----------------------------------------------------------
```

### Step 4 — Wait for architect response

After presenting the report, STOP and wait. Do not generate any briefing content.

Handle responses:

| Response | Action |
|----------|--------|
| File uploaded | Parse the file, update the corresponding domain to Provided, refresh the report |
| "skip [item name]" | Mark that domain as Skipped, refresh the report |
| "confirm" | If all domains are resolved (Connected, Provided, or Skipped) → set gate_cleared = True and hand off to briefing-generator. If unresolved items remain → re-present the report with remaining items highlighted |
| Any other message | Re-present the report and remind the architect of the required actions |

### Step 5 — Record gate outcome

Once the gate is cleared, record the final state of all domains for use by downstream skills:
- Which connectors are live
- Which files were uploaded and their parsed content
- Which items were skipped (these become partial flags in the output)
- LeanIX data availability for the customer account

---

## Gotchas

- **SAP Knowledge Connector is the only hard blocker** — all other missing items result in partial sections, not a halt. Only an unreachable SAP Knowledge Connector stops the session entirely.
- **LeanIX no-data is not a failure** — if LeanIX is reachable but has no data for the customer account, this is a valid state. Report it clearly and offer the manual upload option. Do not treat it as an error.
- **Never infer gate clearance** — the architect must explicitly type "confirm". Do not infer confirmation from other messages or proceed after a file upload without waiting for explicit confirmation.
