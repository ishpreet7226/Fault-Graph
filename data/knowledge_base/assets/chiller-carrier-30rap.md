---
id: asset/chiller-carrier-30rap
type: asset
name: "Carrier 30RAP Air-Cooled Chiller"
model: "Carrier 30RAP"
manufacturer: "Carrier Corporation"
capacity_tons: [50, 60, 75, 90, 110, 130]
refrigerant: R-410A
voltage: "460V/3Ph/60Hz"
severity: critical
tags: [chiller, air-cooled, HVAC, industrial]
connected_subsystems:
  - subsystems/condenser-assembly
  - subsystems/compressor-unit
  - subsystems/refrigerant-circuit
  - subsystems/electrical-control-panel
known_error_codes:
  - failures/E3-high-pressure-trip
  - failures/E5-high-discharge-temp
  - failures/U0-refrigerant-loss
  - failures/103-prestart-temp-alert
  - failures/A6-fan-motor-fault
---

# Carrier 30RAP Air-Cooled Chiller

## Overview
The **Carrier 30RAP** is a high-efficiency air-cooled scroll chiller designed for commercial and light industrial HVAC applications. It employs multiple scroll compressors, direct-drive condenser fans, and an advanced microprocessor control system (Carrier Pro-Dialog Plus).

## Major Subsystems

The chiller integrates the following core subsystems:

- [[subsystems/condenser-assembly]] — Air-cooled finned-tube coils with variable-speed fans
- [[subsystems/compressor-unit]] — Tandem or single scroll compressor banks
- [[subsystems/refrigerant-circuit]] — R-410A refrigerant loop with TXV and filter dryer
- [[subsystems/electrical-control-panel]] — Pro-Dialog Plus controller with alarm management

## Known Failure Modes

The following fault codes are documented for this asset:

- [[failures/E3-high-pressure-trip]] — High refrigerant discharge pressure event
- [[failures/E5-high-discharge-temp]] — Compressor discharge temperature exceeded limit
- [[failures/U0-refrigerant-loss]] — Low refrigerant / system pressure anomaly
- [[failures/103-prestart-temp-alert]] — Leaving water temperature alert during startup
- [[failures/A6-fan-motor-fault]] — Condenser fan motor electrical fault

## Maintenance Schedule
| Interval | Task |
|----------|------|
| Monthly  | Inspect condenser coil cleanliness, check refrigerant sight glass |
| Quarterly| Verify fan motor amperage, test high-pressure cutout switch |
| Annually | Full refrigerant system check, electrical connection torque verification |

## Safety Requirements
All work on this asset requires compliance with:
- [[sops/sop-high-pressure-lockout]]
- [[sops/sop-refrigerant-leak-check]]
- [[sops/sop-electrical-safety]]
