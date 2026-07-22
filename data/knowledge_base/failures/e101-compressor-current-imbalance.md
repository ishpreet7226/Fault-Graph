---
id: failures/e101-compressor-current-imbalance
type: failure
name: E101 — Compressor Current Imbalance
error_code: E101
severity: high
tags:
- failure
- hvac
affected_components:
- components/electrical-panel
- components/compressor
- components/contactor
connected_sops:
- sops/sop-electrical-safety
- sops/sop-compressor-replacement
---

# E101 — Compressor Current Imbalance

## Symptoms
- Current imbalance across phases causes overheating and nuisance trips.
- Repeated alarms reported by site operators

## Severity
high

## Likely Causes
- Phase loss
- Loose terminal
- Worn contactor

## Engineering Explanation
This code represents a field-observed pattern that should be validated against the asset configuration and connected sensor values.

## Repair Procedure
Inspect phase currents, verify motor balance, and inspect contactors.

## Safety
- Isolate electrical power before service
- Follow refrigerant handling rules and site permit controls

## Affected Components
- Electrical panel
- Compressor
- Contactor

## Related SOPs
- [[sops/sop-electrical-safety]]
- [[sops/sop-compressor-replacement]]

## Configuration Limits
Voltage 460V +/- 10%, current imbalance < 10%

## Expected Sensor Values
RMS current 58-62A
