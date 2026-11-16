---
name: bom-justification
description: |
  [WHAT] Generates per-SKU BOM item explanations, SAP best-practice justifications, and entitlement highlights using SAP Knowledge Connector data.
  [WHEN] Use during Phase 2 briefing generation for each BOM item in the architect's list.
  [NOT] Do not use before the data completeness gate is cleared. Do not use for integration layer content — use integration-layer instead.
  Key terms: BOM, SKU, justification, entitlement, best practice, product description.
allowed-tools:
  - Read
metadata:
  version: 1.0.0
  tags:
    - presales
    - bom
    - justification
    - entitlement
---

# BOM Justification

## Purpose

This skill drives the core content generation for BOM items in the briefing document. For each SKU in the BOM list, it retrieves SAP knowledge connector data and produces three distinct outputs: a plain-language explanation, a SAP best-practice justification, and entitlement highlights showing what is included within the product bundle.

## When to use

- During Phase 2, for each BOM item after the data completeness gate is cleared
- When the architect asks "explain this SKU" or "what's included in this product"
- When generating the BOM Explanations, BOM Justification, and Entitlement Highlights sections of the briefing

## When NOT to use

- Before the data completeness gate is cleared
- For integration layer content — use integration-layer skill instead
- For customer overview content — that comes from One360

---

## Instructions

### Step 1 — Process each BOM item

For each item in the BOM list:
1. Call the SAP Knowledge Connector MCP tool to retrieve: product name, description, best-practice use cases, recommended architecture position, and entitlement data (what is included in the SKU bundle)
2. Record the result: data retrieved / knowledge_missing / entitlement_missing

### Step 2 — Generate plain-language explanation

For each BOM item where knowledge was retrieved, write a plain-language explanation that:
- Avoids SAP internal jargon where possible; explain abbreviations on first use
- Answers: "What does this product do?" in 2-3 sentences a business stakeholder can understand
- States the primary business problem it solves

### Step 3 — Generate SAP best-practice justification

For each BOM item, write a justification paragraph that:
- References the specific SAP best-practice rationale for including this product in the proposed architecture
- Connects the product to the customer's stated business goals (from One360 or meeting notes if available)
- Explains why this product is recommended over alternatives where applicable
- Cites the relevant SAP reference architecture or solution bundle where applicable

### Step 4 — Generate entitlement highlights

For each BOM item:
- If entitlement data was retrieved: list the embedded entitlements in bullet format. Frame each as: "[Entitlement name]: [what it enables the customer to do without additional licensing]"
- If NO entitlement data was retrieved: insert the following inline flag exactly:
  "WARNING Entitlement data not available for this SKU — please supply an entitlement reference sheet for a complete entitlement view of this product."

### Step 5 — Apply dual-purpose formatting

For each BOM item, structure the output as:
```
### [Product Name] ([SKU code if available])

**What it does** (customer reading)
[Plain-language explanation — 2-3 sentences]

**Why it is recommended** (customer reading)
[SAP best-practice justification — 1-2 paragraphs]

**Talking points** (architect guide)
- [Key point 1]
- [Key point 2]
- [Key point 3]

**Entitlements included in this SKU**
- [Entitlement 1]: [what it enables]
- [Entitlement 2]: [what it enables]
[or WARNING flag if data unavailable]
```

### Step 6 — Flag knowledge gaps

For any BOM item where the SAP Knowledge Connector returned no data at all, insert:
"WARNING SAP Knowledge Connector returned no data for [SKU name]. This section requires manual review. Please provide product documentation or contact your SAP representative."

---

## Gotchas

- **Never fabricate entitlement data** — if the knowledge connector does not return entitlement information, use the WARNING flag. Do not infer, guess, or extrapolate entitlements from product descriptions.
- **Dual-purpose formatting is mandatory** — every BOM item section must include both the customer-facing paragraphs and the architect talking-point bullets. Do not omit either format.
- **Missing BOM items are not skippable** — if the BOM list is empty or was skipped in the gate, this skill cannot run. Return to the gate and request the BOM list before proceeding.
