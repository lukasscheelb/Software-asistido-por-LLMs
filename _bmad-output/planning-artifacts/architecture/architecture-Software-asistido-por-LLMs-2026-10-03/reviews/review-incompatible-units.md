# Architecture Spine Review — Incompatible Units Attack

## Verdict

Pass after closing two ownership gaps. F4, F1 and verification cannot obey the current ADs while creating independent vocabularies or a second mutable queue state.

## Attack Cases

1. **F4 and F1 declare separate outcome/status enums.** Initially possible because dependency direction alone did not name the owner. Fixed by AD-13: `domain` owns shared outcomes, statuses, priorities, explanation and reason schema.
2. **F1 persists a mutable queue row while another module derives state from Interventions.** Initially possible and would create two sources of truth. Fixed by AD-14: Bandeja is a read projection and cannot be mutated directly.
3. **Web serializes `90,01` while domain consumes `90.01`.** Fixed by the Serialization convention: canonical decimal strings use a point; comma is display-only.
4. **Two writers update one human decision.** Blocked by AD-4 and AD-5: one application command, expected version check, transaction and append-only record.
5. **F4 and tests read different clocks or Policy values.** Blocked by AD-3, AD-6 and AD-7.

## Residual Items

- Reason values remain a product/UX choice, but their schema and technical ownership no longer diverge.
- p95 and PX-08 remain acceptance-definition gaps, not module-boundary gaps.

No critical or high incompatibility remains.
