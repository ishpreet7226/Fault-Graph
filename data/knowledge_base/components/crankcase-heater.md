---
id: components/crankcase-heater
type: component
name: "Crankcase Heater"
component_type: heater
model_compatibility: ["Carrier 30RAP", "York YVAA"]
severity: high
tags: [compressor, heater, cold-start]
---

# Crankcase Heater

The crankcase heater prevents refrigerant migration into the compressor oil during low ambient conditions. Heater open-circuit or low power can lead to oil dilution, which often manifests as elevated discharge temperatures and compressor damage.

Inspection guidance:

- Measure heater resistance against manufacturer spec (example: 1840 ohms ±10%).
- Verify heater draws rated current and is receiving control power.
- If a heater failure is suspected, follow the [[sops/sop-crankcase-heater]] procedure and monitor oil condition.

Related failures:

- [[failures/103-prestart-temp-alert]]
- [[failures/E5-high-discharge-temp]]
- [[incident_reports/story-3-crankcase-heater-failure]]
