---
id: subsystems/compressor-unit
type: subsystem
name: "Compressor Unit"
parent_assets:
  - assets/chiller-carrier-30rap
  - assets/chiller-york-yvaa
severity: critical
components:
  - components/discharge-temperature-sensor
  - components/high-pressure-switch
tags: [compressor, scroll, screw, compression, refrigeration-cycle]
connected_failures:
  - failures/E3-high-pressure-trip
  - failures/E5-high-discharge-temp
  - failures/U0-refrigerant-loss
connected_sops:
  - sops/sop-high-pressure-lockout
  - sops/sop-refrigerant-leak-check
---

# Compressor Unit

## Overview
The compressor is the heart of the refrigeration cycle, raising refrigerant pressure from the evaporator suction side to the high-pressure discharge side. Carrier 30RAP units use scroll compressors arranged in tandem banks; York YVAA units use a single-screw design with an integrated VFD.

## Components

- [[components/discharge-temperature-sensor]] — Measures compressor discharge gas temperature (target: <220°F for R-410A)
- [[components/high-pressure-switch]] — Hard cutout at ~650 psig for R-410A / ~260 psig for R-134a

## Common Failure Modes

| Failure | Root Cause | Effect |
|---------|-----------|--------|
| [[failures/E5-high-discharge-temp]] | Low refrigerant charge, high load, blocked condenser | Compressor thermal trip |
| [[failures/E3-high-pressure-trip]] | Excessive load, condenser fault | Hard lockout |
| [[failures/U0-refrigerant-loss]] | Refrigerant leak, valve failure | Low suction pressure, high superheat |

## Diagnostic Approach
1. Check suction and discharge pressures against refrigerant PT chart
2. Measure discharge temperature with calibrated probe
3. Verify oil level (screw compressors) — oil sight glass should be half full
4. Check motor winding resistance for each compressor phase
5. Review compressor operating hours for scheduled replacement threshold

## Safety
- [[sops/sop-high-pressure-lockout]] — Mandatory before any compressor refrigerant work
- [[sops/sop-refrigerant-leak-check]] — After any refrigerant system opening
