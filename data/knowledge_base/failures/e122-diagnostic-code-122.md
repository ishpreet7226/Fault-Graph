---
id: failures/e122-diagnostic-code-122
type: failure
name: E122 — Diagnostic Code 122
error_code: E122
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

# E122 — Diagnostic Code 122

## Symptoms
- Synthetic industrial fault pattern 122 observed in the field.
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
Inspect the assembly and confirm the expected range for code E122.

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
Operating window 122 to 162

## Expected Sensor Values
Expected sensor value 132 to 172
