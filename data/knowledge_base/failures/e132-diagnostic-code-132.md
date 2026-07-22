---
id: failures/e132-diagnostic-code-132
type: failure
name: E132 — Diagnostic Code 132
error_code: E132
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

# E132 — Diagnostic Code 132

## Symptoms
- Synthetic industrial fault pattern 132 observed in the field.
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
Inspect the assembly and confirm the expected range for code E132.

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
Operating window 132 to 172

## Expected Sensor Values
Expected sensor value 142 to 182
