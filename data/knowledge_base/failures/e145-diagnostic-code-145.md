---
id: failures/e145-diagnostic-code-145
type: failure
name: E145 — Diagnostic Code 145
error_code: E145
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

# E145 — Diagnostic Code 145

## Symptoms
- Synthetic industrial fault pattern 145 observed in the field.
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
Inspect the assembly and confirm the expected range for code E145.

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
Operating window 145 to 185

## Expected Sensor Values
Expected sensor value 155 to 195
