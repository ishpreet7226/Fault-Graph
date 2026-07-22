---
id: failures/e192-diagnostic-code-192
type: failure
name: E192 — Diagnostic Code 192
error_code: E192
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

# E192 — Diagnostic Code 192

## Symptoms
- Synthetic industrial fault pattern 192 observed in the field.
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
Inspect the assembly and confirm the expected range for code E192.

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
Operating window 192 to 232

## Expected Sensor Values
Expected sensor value 202 to 242
