---
name: briefing-generator
description: |
  [WHAT] Orchestrates the full structured briefing document assembly from all retrieved and uploaded data, applying dual-purpose formatting and inline gap flags.
  [WHEN] Use after the data completeness gate is cleared and all data retrieval is complete. This is the final assembly step.
  [NOT] Do not use before the gate is cleared. Do not use for individual section content — use bom-justification and integration-layer skills for those.
  Key terms: briefing, document, assembly, output, dual-purpose, gap flags, sections.
allowed-tools:
  - Read
metadata:
  version: 1.0.0
  tags:
    - presales
    - briefing
    - document
    - output
---

# Briefing Generator

## Purpose

This skill assembles the final structured briefing document from all data retrieved and processed by the other skills. It enforces section order, applies dual-purpose formatting, adds inline gap flags, and produces a document header with source traceability.

## When to use

- After the data completeness gate is cleared (Phase 2 start)
- After SAP Knowledge Connector, One360, and LeanIX retrieval are complete
- As the final assembly step before delivering the document to the architect

## When NOT to use

- Before the data completeness gate is cleared
- As a replacement for bom-justification or integration-layer — those skills generate section content; this skill assembles it

---

## Instructions

### Step 1 — Build the document header

Always include a header at the top of every briefing:

```
PRESALES BRIEFING DOCUMENT
-----------------------------------------------------------
Customer:        [Customer name from One360 or architect input]
Prepared by:     SAP Presales Briefing Agent
Date:            [Current date]
-----------------------------------------------------------
DATA SOURCES USED
SAP Knowledge Connector:      [Connected / Partial - [N] items missing knowledge data]
One360 Customer Intelligence: [Connected / Partial - data unavailable]
LeanIX Architecture Data:     [Data found - snapshot date: [date] / No data for account / Not available]
Manual uploads:               [List of uploaded files, or None]
Skipped domains:              [List of skipped items, or None]
-----------------------------------------------------------
NOTE: Sections marked with WARNING are partial due to missing data. The suggested action for each is noted inline.
-----------------------------------------------------------
```

### Step 2 — Assemble sections in mandatory order

The briefing document MUST contain these sections in this exact order:

1. **Customer Overview**
   - Source: One360 Connector
   - Content: account summary, current known landscape, strategic priorities, relationship history
   - If One360 unavailable: "WARNING Customer intelligence unavailable. One360 Connector did not return data for this account. This section requires manual completion."

2. **Solution Summary**
   - Source: LeanIX (if available) + SAP Knowledge Connector + BOM list
   - Content: 1-2 paragraph narrative of the proposed to-be architecture and how it fits the customer's environment
   - If LeanIX unavailable: flag as partial (based on SAP reference model)

3. **Bill of Materials — Item Explanations**
   - Source: SAP Knowledge Connector (via bom-justification skill)
   - Content: one subsection per SKU with plain-language explanation
   - Flag any SKU where knowledge connector returned no data

4. **BOM Justification**
   - Source: SAP Knowledge Connector (via bom-justification skill)
   - Content: per-SKU SAP best-practice rationale
   - Flag any SKU where knowledge connector returned no data

5. **Entitlement Highlights**
   - Source: SAP Knowledge Connector (via bom-justification skill)
   - Content: per-SKU entitlements embedded in the product bundle
   - Flag any SKU with missing entitlement data

6. **Integration Layer**
   - Source: LeanIX + SAP Knowledge Connector (via integration-layer skill)
   - Content: how proposed products connect, with concrete examples
   - If LeanIX unavailable: flag as partial (SAP reference model only)

7. **Customer Context and Meeting History**
   - Source: Meeting notes/transcripts + One360
   - Content: key themes, agreed priorities, prior commitments from previous meetings
   - If meeting notes skipped: "WARNING Meeting notes not provided. This section is based on One360 account intelligence only."
   - If both skipped: "WARNING Neither meeting notes nor One360 data were available. This section could not be generated."

### Step 3 — Apply dual-purpose formatting

Every section must contain both:
- A **customer-facing paragraph** (narrative prose, suitable for reading independently)
- An **architect talking-points block** (bullet list, suitable for live presentation reference)

Label these clearly:
```
[Customer reading]
[paragraph text]

[Architect talking points]
- Point 1
- Point 2
- Point 3
```

### Step 4 — Apply inline gap flags

For every partial section, insert the gap flag at the TOP of that section (not the bottom):
```
WARNING [Reason for partial data] — [Suggested action to complete this section]
```

Examples:
- "WARNING Entitlement data not available for SAP S/4HANA Cloud Public Edition — please supply an entitlement reference sheet for a complete view."
- "WARNING Integration layer based on SAP reference model only, not customer-specific landscape — please provide LeanIX data for a customer-grounded integration narrative."
- "WARNING One360 data unavailable — customer overview is incomplete. Please verify account access in One360."

### Step 5 — Close the document

End every briefing with:
```
-----------------------------------------------------------
END OF BRIEFING DOCUMENT
Next steps:
- Review all WARNING sections and supply missing data for a complete briefing
- This document is intended for use as both a customer-facing document and a live presentation guide
- For questions about SAP best practices or entitlement details, contact your SAP account team
-----------------------------------------------------------
```

---

## Gotchas

- **Section order is mandatory** — do not reorder sections even if the architect requests it. The order is designed for logical flow from context to solution to justification to integration.
- **Dual-purpose formatting applies to every section** — do not omit the talking-points block for any section, even partial ones.
- **Gap flags go at the TOP of the partial section** — placing them at the bottom means the architect may miss them when skimming. Always flag at the top.
- **The document header must always be generated** — even if all sections are partial, the header with source traceability must be present.
