---
id: asset/chiller-york-yvaa
type: asset
name: "York YVAA Variable-Speed Air-Cooled Screw Chiller"
model: "York YVAA"
manufacturer: "Johnson Controls / York"
capacity_tons: [120, 150, 180, 200, 250]
refrigerant: R-134a
voltage: "480V/3Ph/60Hz"
severity: critical
tags: [chiller, air-cooled, variable-speed, screw-compressor, industrial]
connected_subsystems:
  - subsystems/condenser-assembly
  - subsystems/compressor-unit
  - subsystems/refrigerant-circuit
  - subsystems/electrical-control-panel
known_error_codes:
  - failures/E3-high-pressure-trip
  - failures/E5-high-discharge-temp
  - failures/U0-refrigerant-loss
  - failures/A6-fan-motor-fault
---

# York YVAA Variable-Speed Air-Cooled Screw Chiller

## Overview
The **York YVAA** series represents York's flagship variable-speed air-cooled screw chiller platform. It uses a single-screw compressor with an integrated variable-frequency drive (VFD) on both the compressor and condenser fans, achieving industry-leading part-load efficiencies (IPLV).

## Major Subsystems

- [[subsystems/condenser-assembly]] — Variable-speed EC fan array with aluminum micro-channel coils
- [[subsystems/compressor-unit]] — Single-screw compressor with integrated VFD and oil management
- [[subsystems/refrigerant-circuit]] — R-134a refrigerant circuit with electronic expansion valve (EEV)
- [[subsystems/electrical-control-panel]] — York Microgateway+ controller with BACnet/Modbus integration

## Known Failure Modes

- [[failures/E3-high-pressure-trip]] — High side pressure lockout during peak ambient conditions
- [[failures/E5-high-discharge-temp]] — VFD-compressor thermal protection activation
- [[failures/U0-refrigerant-loss]] — Refrigerant undercharge detected via suction pressure monitoring
- [[failures/A6-fan-motor-fault]] — EC fan motor drive fault or communication loss

## Maintenance Schedule
| Interval | Task |
|----------|------|
| Monthly  | Check VFD cooling fan operation, inspect micro-channel coil fouling |
| Quarterly| Verify EEV superheat control, inspect oil level/quality |
| Semi-annually | VFD firmware update, compressor vibration analysis |
| Annually | Full leak check, motor insulation resistance test |

## Safety Requirements
- [[sops/sop-high-pressure-lockout]]
- [[sops/sop-refrigerant-leak-check]]
- [[sops/sop-electrical-safety]]
