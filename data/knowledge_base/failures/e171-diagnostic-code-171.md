---
id: failures/e171-diagnostic-code-171
type: failure
name: E171 — Diagnostic Code 171
error_code: E171
severity: high
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

# E171 — Diagnostic Code 171

## Symptoms
- Synthetic industrial fault pattern 171 observed in the field.
- Repeated alarms reported by site operators

## Severity
high

## Likely Causes
- component wear
- environmental stress
- sensor offset

## Engineering Explanation
This code represents a field-observed pattern that should be validated against the asset configuration and connected sensor values.

## Repair Procedure
Inspect the assembly and confirm the expected range for code E171.

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
Operating window 171 to 211

## Expected Sensor Values
Expected sensor value 181 to 221
