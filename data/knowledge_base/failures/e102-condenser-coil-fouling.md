---
id: failures/e102-condenser-coil-fouling
type: failure
name: E102 — Condenser Coil Fouling
error_code: E102
severity: medium
tags:
- failure
- hvac
affected_components:
- components/condenser
- components/fan-motor
- components/filter
connected_sops:
- sops/sop-coil-cleaning
- sops/sop-fan-motor-service
---

# E102 — Condenser Coil Fouling

## Symptoms
- Accumulated debris reduces airflow and raises head pressure.
- Repeated alarms reported by site operators

## Severity
medium

## Likely Causes
- Dirty coil
- Blocked intake
- Failed fan

## Engineering Explanation
This code represents a field-observed pattern that should be validated against the asset configuration and connected sensor values.

## Repair Procedure
Clean coil, inspect fan operation, and verify static pressure.

## Safety
- Isolate electrical power before service
- Follow refrigerant handling rules and site permit controls

## Affected Components
- Condenser
- Fan Motor
- Filter

## Related SOPs
- [[sops/sop-coil-cleaning]]
- [[sops/sop-fan-motor-service]]

## Configuration Limits
Ambient 95°F max, static pressure < 0.8 in wg

## Expected Sensor Values
Head pressure 450-520 psig
