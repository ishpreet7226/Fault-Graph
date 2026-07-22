---
id: failures/e135-diagnostic-code-135
type: failure
name: E135 — Diagnostic Code 135
error_code: E135
severity: low
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

# E135 — Diagnostic Code 135

## Symptoms
- Synthetic industrial fault pattern 135 observed in the field.
- Repeated alarms reported by site operators

## Severity
low

## Likely Causes
- component wear
- environmental stress
- sensor offset

## Engineering Explanation
This code represents a field-observed pattern that should be validated against the asset configuration and connected sensor values.

## Repair Procedure
Inspect the assembly and confirm the expected range for code E135.

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
Operating window 135 to 175

## Expected Sensor Values
Expected sensor value 145 to 185
