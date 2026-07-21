---
id: components/fan-motor
type: component
name: "Condenser Fan Motor"
part_numbers:
  - "CFM-460-1HP-ODP"
  - "CFM-460-2HP-TEFC"
  - "CFM-EC-VSD-0.75kW"
motor_types: [ODP, TEFC, EC-Brushless]
voltage: ["460V/3Ph", "208-230V/1Ph"]
hp_range: [0.75, 1.0, 1.5, 2.0]
rpm: [850, 1075, 1140]
severity: high
tags: [fan, motor, condenser, electrical, EC, ODP, TEFC]
parent_subsystems:
  - subsystems/condenser-assembly
  - subsystems/electrical-control-panel
connected_failures:
  - failures/A6-fan-motor-fault
  - failures/E3-high-pressure-trip
connected_sops:
  - sops/sop-electrical-safety
---

# Condenser Fan Motor

## Overview
Condenser fan motors drive the propeller fans that move ambient air across the condenser coil to reject heat from the refrigerant. Multiple fan motors may be staged or speed-controlled (EC motors with VFD) depending on the chiller model and ambient conditions.

## Motor Types

| Type | Enclosure | Application |
|------|-----------|-------------|
| ODP (Open Drip-Proof) | Indoor/protected locations | Legacy Carrier 30RAP units |
| TEFC (Totally Enclosed Fan-Cooled) | Outdoor exposure | Standard industrial spec |
| EC Brushless | Variable-speed | York YVAA, high-efficiency units |

## Diagnostic Procedure
1. **Visual inspection**: Check for blade damage, shaft wobble, bearing noise
2. **Amperage check**: Measure motor amps on each phase, compare to nameplate FLA
3. **Winding resistance**: Use megohmmeter — winding-to-ground >1MΩ at 500VDC
4. **Capacitor check** (single-phase): Test run and start capacitor with capacitor meter
5. **Bearing temperature**: Use IR thermometer — >180°F indicates bearing failure
6. **EC motor**: Check drive communication status and fault codes on controller

## Connected Failures
- [[failures/A6-fan-motor-fault]] — Primary failure mode of this component
- [[failures/E3-high-pressure-trip]] — Cascade failure when fan motor fails

## Safety
- [[sops/sop-electrical-safety]] — Full LOTO before any motor access or replacement
