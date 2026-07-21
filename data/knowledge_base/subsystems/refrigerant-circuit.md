---
id: subsystems/refrigerant-circuit
type: subsystem
name: "Refrigerant Circuit"
parent_assets:
  - assets/chiller-carrier-30rap
  - assets/chiller-york-yvaa
severity: critical
components:
  - components/refrigerant-level-sensor
  - components/high-pressure-switch
tags: [refrigerant, R-410A, R-134a, circuit, leak, TXV, EEV]
connected_failures:
  - failures/U0-refrigerant-loss
  - failures/E3-high-pressure-trip
  - failures/E5-high-discharge-temp
connected_sops:
  - sops/sop-refrigerant-leak-check
  - sops/sop-high-pressure-lockout
---

# Refrigerant Circuit

## Overview
The refrigerant circuit forms the closed-loop thermodynamic cycle that transfers heat from the building load (evaporator) to the outside air (condenser). It includes the compressor, condenser, expansion device (TXV or EEV), evaporator, filter dryer, sight glass, service valves, and refrigerant charge.

## Components

- [[components/refrigerant-level-sensor]] — Suction pressure transducer providing indirect refrigerant charge status
- [[components/high-pressure-switch]] — Safety cutout protecting the high-pressure side

## Common Failure Modes

| Failure | Root Cause | Effect |
|---------|-----------|--------|
| [[failures/U0-refrigerant-loss]] | Mechanical leak at joints, valve packing, Schrader cores | System underperformance, compressor overheating |
| [[failures/E3-high-pressure-trip]] | Non-condensable gases, overcharge, condenser blockage | Hard lockout |
| [[failures/E5-high-discharge-temp]] | Undercharge causing high superheat | Compressor thermal damage |

## Diagnostic Approach
1. Check sight glass — should show clear, bubble-free refrigerant flow
2. Measure subcooling at condenser outlet (target: 8–14°F)
3. Measure superheat at compressor inlet (target: 8–15°F)
4. Perform electronic leak detection at all brazed fittings, service valves, and coil headers
5. Recover, evacuate, and recharge if leak confirmed (EPA Section 608)

## Safety
- [[sops/sop-refrigerant-leak-check]] — Mandatory for any suspected leak
- [[sops/sop-high-pressure-lockout]] — Required before opening any refrigerant connection
