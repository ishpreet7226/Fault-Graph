---
id: failures/e149-diagnostic-code-149
type: failure
name: E149 — Diagnostic Code 149
error_code: E149
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

# E149 — Diagnostic Code 149

## Symptoms
- Synthetic industrial fault pattern 149 observed in the field.
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
Inspect the assembly and confirm the expected range for code E149.

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
Operating window 149 to 189

## Expected Sensor Values
Expected sensor value 159 to 199
