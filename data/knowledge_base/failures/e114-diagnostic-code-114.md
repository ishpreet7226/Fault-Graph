---
id: failures/e114-diagnostic-code-114
type: failure
name: E114 — Diagnostic Code 114
error_code: E114
severity: critical
tags:
- failure
- hvac
affected_components:
- components/compressor
- components/control-board
- components/pressure-sensor
connected_sops:
- sops/sop-electrical-safety
---

# E114 — Diagnostic Code 114

## Symptoms
- Synthetic industrial fault pattern 114 observed in the field.
- Repeated alarms reported by site operators

## Severity
critical

## Likely Causes
- component wear
- environmental stress
- sensor offset

## Engineering Explanation
This code represents a field-observed pattern that should be validated against the asset configuration and connected sensor values.

## Repair Procedure
Inspect the assembly and confirm the expected range for code E114.

## Safety
- Isolate electrical power before service
- Follow refrigerant handling rules and site permit controls

## Affected Components
- Compressor
- Control Board
- Pressure Sensor

## Related SOPs
- [[sops/sop-electrical-safety]]

## Configuration Limits
Operating window 114 to 154

## Expected Sensor Values
Expected sensor value 124 to 164
