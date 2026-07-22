---
id: failures/e129-diagnostic-code-129
type: failure
name: E129 — Diagnostic Code 129
error_code: E129
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

# E129 — Diagnostic Code 129

## Symptoms
- Synthetic industrial fault pattern 129 observed in the field.
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
Inspect the assembly and confirm the expected range for code E129.

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
Operating window 129 to 169

## Expected Sensor Values
Expected sensor value 139 to 179
