---
id: failures/e130-diagnostic-code-130
type: failure
name: E130 — Diagnostic Code 130
error_code: E130
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

# E130 — Diagnostic Code 130

## Symptoms
- Synthetic industrial fault pattern 130 observed in the field.
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
Inspect the assembly and confirm the expected range for code E130.

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
Operating window 130 to 170

## Expected Sensor Values
Expected sensor value 140 to 180
