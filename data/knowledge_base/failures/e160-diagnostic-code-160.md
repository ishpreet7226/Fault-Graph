---
id: failures/e160-diagnostic-code-160
type: failure
name: E160 — Diagnostic Code 160
error_code: E160
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

# E160 — Diagnostic Code 160

## Symptoms
- Synthetic industrial fault pattern 160 observed in the field.
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
Inspect the assembly and confirm the expected range for code E160.

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
Operating window 160 to 200

## Expected Sensor Values
Expected sensor value 170 to 210
