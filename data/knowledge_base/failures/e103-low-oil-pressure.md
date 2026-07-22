---
id: failures/e103-low-oil-pressure
type: failure
name: E103 — Low Oil Pressure
error_code: E103
severity: critical
tags:
- failure
- hvac
affected_components:
- components/compressor
- components/oil-pressure-switch
- components/oil-separator
connected_sops:
- sops/sop-oil-analysis
- sops/sop-compressor-replacement
---

# E103 — Low Oil Pressure

## Symptoms
- Insufficient lubrication causes compressor damage.
- Repeated alarms reported by site operators

## Severity
critical

## Likely Causes
- Low oil level
- Pump failure
- Control fault

## Engineering Explanation
This code represents a field-observed pattern that should be validated against the asset configuration and connected sensor values.

## Repair Procedure
Confirm oil level, inspect pump, and verify pressure switch operation.

## Safety
- Isolate electrical power before service
- Follow refrigerant handling rules and site permit controls

## Affected Components
- Compressor
- Oil Pressure Switch
- Oil Separator

## Related SOPs
- [[sops/sop-oil-analysis]]
- [[sops/sop-compressor-replacement]]

## Configuration Limits
Oil pressure 40-70 psig

## Expected Sensor Values
Oil temp 95-120°F
