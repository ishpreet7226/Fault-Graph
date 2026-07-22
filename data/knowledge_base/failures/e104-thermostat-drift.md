---
id: failures/e104-thermostat-drift
type: failure
name: E104 — Thermostat Drift
error_code: E104
severity: medium
tags:
- failure
- hvac
affected_components:
- components/thermostat
- components/temperature-sensor
- components/control-board
connected_sops:
- sops/sop-electrical-safety
- sops/sop-seasonal-startup
---

# E104 — Thermostat Drift

## Symptoms
- Sensor calibration drift causes incorrect comfort control.
- Repeated alarms reported by site operators

## Severity
medium

## Likely Causes
- Sensor offset
- Loose wiring
- Controller issue

## Engineering Explanation
This code represents a field-observed pattern that should be validated against the asset configuration and connected sensor values.

## Repair Procedure
Calibrate sensor and inspect wiring continuity.

## Safety
- Isolate electrical power before service
- Follow refrigerant handling rules and site permit controls

## Affected Components
- Thermostat
- Temperature Sensor
- Control Board

## Related SOPs
- [[sops/sop-electrical-safety]]
- [[sops/sop-seasonal-startup]]

## Configuration Limits
Supply air 55°F-65°F

## Expected Sensor Values
Room temp +/- 1°F
