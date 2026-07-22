---
id: failures/e105-valve-stuck-open
type: failure
name: E105 — Valve Stuck Open
error_code: E105
severity: high
tags:
- failure
- hvac
affected_components:
- components/expansion-valve
- components/refrigerant-circuit
- components/filter-dryer
connected_sops:
- sops/sop-txv-replacement
- sops/sop-leak-pressure-test
---

# E105 — Valve Stuck Open

## Symptoms
- A stuck valve allows unmetered refrigerant flow and poor efficiency.
- Repeated alarms reported by site operators

## Severity
high

## Likely Causes
- Mechanical obstruction
- Electrical coil failure
- Contamination

## Engineering Explanation
This code represents a field-observed pattern that should be validated against the asset configuration and connected sensor values.

## Repair Procedure
Isolate the valve, inspect coil, and replace if necessary.

## Safety
- Isolate electrical power before service
- Follow refrigerant handling rules and site permit controls

## Affected Components
- Expansion Valve
- Refrigerant Circuit
- Filter Dryer

## Related SOPs
- [[sops/sop-txv-replacement]]
- [[sops/sop-leak-pressure-test]]

## Configuration Limits
Superheat 8-12°F

## Expected Sensor Values
Subcooling 8-12°F
