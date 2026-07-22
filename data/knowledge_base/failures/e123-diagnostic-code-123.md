---
id: failures/e123-diagnostic-code-123
type: failure
name: E123 — Diagnostic Code 123
error_code: E123
severity: medium
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

# E123 — Diagnostic Code 123

## Symptoms
- Synthetic industrial fault pattern 123 observed in the field.
- Repeated alarms reported by site operators

## Severity
medium

## Likely Causes
- component wear
- environmental stress
- sensor offset

## Engineering Explanation
This code represents a field-observed pattern that should be validated against the asset configuration and connected sensor values.

## Repair Procedure
Inspect the assembly and confirm the expected range for code E123.

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
Operating window 123 to 163

## Expected Sensor Values
Expected sensor value 133 to 173
