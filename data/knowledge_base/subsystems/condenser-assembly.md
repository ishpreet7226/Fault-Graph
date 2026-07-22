---
id: subsystems/condenser-assembly
type: subsystem
name: Condenser Assembly
parent_assets:
- assets/chiller-carrier-30rap
- assets/chiller-york-yvaa
severity: high
components:
- components/high-pressure-switch
- components/fan-motor
tags:
- condenser
- heat-rejection
- air-cooled
- fan
- coil
connected_failures:
- failures/E3-high-pressure-trip
- failures/A6-fan-motor-fault
connected_sops:
- sops/sop-high-pressure-lockout
- sops/sop-electrical-safety
---

# Condenser Assembly

## Overview
The condenser assembly is responsible for rejecting heat absorbed from the refrigerant circuit to the ambient air. In air-cooled chillers, this is accomplished via finned-tube or micro-channel heat exchanger coils, driven by one or more direct-drive condenser fan motors.

## Components

- [[components/high-pressure-switch]] — Monitors refrigerant discharge pressure; trips the circuit on over-pressure events
- [[components/fan-motor]] — Drives condenser fan blade rotation for forced-convection heat rejection

## Common Failure Modes

| Failure | Root Cause | Effect |
|---------|-----------|--------|
| [[failures/E3-high-pressure-trip]] | Dirty coils, high ambient, fan failure | Compressor lockout |
| [[failures/A6-fan-motor-fault]] | Motor winding failure, capacitor failure, overload | Reduced heat rejection → E3 cascade |

## Diagnostic Approach
1. Verify ambient temperature within unit operating range (<115°F for most units)
2. Inspect condenser coil for fouling, debris, or bent fins
3. Confirm all fan motors are rotating (check amperage on each leg)
4. Test high-pressure switch continuity with calibrated gauge
5. Check refrigerant charge and subcooling temperatures

## Safety
All condenser work requires:
- [[sops/sop-high-pressure-lockout]] — Before any refrigerant-side work
- [[sops/sop-electrical-safety]] — Before fan motor or wiring work
