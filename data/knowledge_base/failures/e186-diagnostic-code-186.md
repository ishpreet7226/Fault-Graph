---
id: failures/e186-diagnostic-code-186
type: failure
name: E186 — Diagnostic Code 186
error_code: E186
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

# E186 — Diagnostic Code 186

## Symptoms
- Synthetic industrial fault pattern 186 observed in the field.
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
Inspect the assembly and confirm the expected range for code E186.

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
Operating window 186 to 226

## Expected Sensor Values
Expected sensor value 196 to 236
