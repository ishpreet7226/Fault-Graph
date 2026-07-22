---
id: components/high-pressure-switch
type: component
name: High Pressure Safety Switch
part_numbers:
- HPS-410A-650
- HPS-134A-280
pressure_setpoint_psi:
  R-410A: 650
  R-134a: 280
auto_reset: false
severity: critical
tags:
- pressure
- safety
- cutout
- refrigerant
- switch
parent_subsystems:
- subsystems/condenser-assembly
- subsystems/compressor-unit
- subsystems/refrigerant-circuit
connected_failures:
- failures/E3-high-pressure-trip
connected_sops:
- sops/sop-high-pressure-lockout
---

# High Pressure Safety Switch

## Overview
The high pressure safety switch (HPSS) is a normally-closed, manual-reset refrigerant pressure switch installed in the discharge line between the compressor outlet and condenser inlet. When discharge pressure exceeds the set point, the switch opens, de-energizing the compressor contactor coil.

**Manual reset is required** — the fault condition must be investigated and cleared before the switch can be reset.

## Specifications

| Parameter | R-410A Units | R-134a Units |
|-----------|-------------|-------------|
| Trip setpoint | 650 psig | 280 psig |
| Reset differential | 50 psig | 20 psig |
| Contact rating | 15A / 250VAC | 15A / 250VAC |
| Connection | 1/4" SAE flare | 1/4" SAE flare |

## Diagnostic Procedure
1. Verify the discharge pressure gauge reading at time of trip
2. Allow system to cool / pressure to reduce before reset
3. Test switch continuity with multimeter (should be closed below trip point)
4. Replace if switch trips below rated setpoint (indicating drift)

## Connected Failures
- [[failures/E3-high-pressure-trip]] — Triggered by this component's operation

## Safety
- [[sops/sop-high-pressure-lockout]] — Required before any work on or near this switch
