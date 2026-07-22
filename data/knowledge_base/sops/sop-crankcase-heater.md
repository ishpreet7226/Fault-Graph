---
id: sops/sop-crankcase-heater
type: sop
name: "SOP — Crankcase Heater Inspection and Replacement"
sop_number: "SOP-CH-001"
severity: high
tags: [sop, heater, compressor, cold-start]
---

# SOP: Crankcase Heater Inspection & Replacement

Purpose:

Ensure crankcase heater integrity to prevent refrigerant migration into compressor oil.

Procedure:

1. Lockout and tagout per [[sops/sop-electrical-safety]].
2. Measure heater circuit voltage and resistance. Expected resistance: ~1840Ω (varies by model).
3. If open or out of tolerance, replace with manufacturer-approved heater.
4. After replacement, perform 8–16 hour pre-heat per manufacturer guidance and monitor oil temperature.
5. If oil contamination suspected, follow [[sops/sop-oil-analysis]] and consult engineering.

References:

- [[components/crankcase-heater]]
- [[failures/103-prestart-temp-alert]]
- [[failures/E5-high-discharge-temp]]
