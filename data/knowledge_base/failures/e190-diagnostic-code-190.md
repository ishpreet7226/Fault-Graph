---
id: failures/e190-diagnostic-code-190
type: failure
name: E190 — Diagnostic Code 190
error_code: E190
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

# E190 — Diagnostic Code 190

## Symptoms
- Synthetic industrial fault pattern 190 observed in the field.
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
Inspect the assembly and confirm the expected range for code E190.

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
Operating window 190 to 230

## Expected Sensor Values
Expected sensor value 200 to 240
