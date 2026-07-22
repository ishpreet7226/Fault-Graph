---
id: asset/chiller-carrier-30rap
type: asset
name: Carrier 30RAP Air-Cooled Chiller
model: Carrier 30RAP
manufacturer: Carrier
capacity: 50-130 tons
refrigerant: R-410A
severity: critical
installed_date: '2020-01-15'
health_score: 72
tags:
- asset
- hvac
- industrial
connected_subsystems:
- subsystems/condenser-assembly
- subsystems/compressor-unit
- subsystems/refrigerant-circuit
- subsystems/electrical-control-panel
- subsystems/evaporator-coil
- subsystems/expansion-valve
known_error_codes:
- failures/E3-high-pressure-trip
- failures/E5-high-discharge-temperatur
- failures/U0-refrigerant-loss---low-ch
- failures/103-prestart-temperature-aler
- failures/A6-fan-motor-fault
- failures/E1-sensor---thermistor-fault
- failures/E2-indoor-thermistor-error
- failures/F1-compressor-overcurrent
- failures/H1-high-pressure-sensor-faul
---

# Carrier 30RAP Air-Cooled Chiller

## Overview
The **Carrier 30RAP** manufactured by **Carrier Corporation** is a production HVAC asset
with capacity **50-130 tons** using **R-410A** refrigerant.

## Major Subsystems
- [[subsystems/condenser-assembly]]
- [[subsystems/compressor-unit]]
- [[subsystems/refrigerant-circuit]]
- [[subsystems/electrical-control-panel]]
- [[subsystems/evaporator-coil]]
- [[subsystems/expansion-valve]]

## Known Failure Modes
- [[failures/e3-high-pressure-trip]]
- [[failures/e5-high-discharge-temperature]]
- [[failures/u0-refrigerant-loss---low-charge]]
- [[failures/103-prestart-temperature-alert]]
- [[failures/a6-fan-motor-fault]]
- [[failures/e1-sensor---thermistor-fault]]
- [[failures/e2-indoor-thermistor-error]]
- [[failures/f1-compressor-overcurrent]]
- [[failures/h1-high-pressure-sensor-fault]]

## Maintenance Schedule
| Interval | Task |
|----------|------|
| Monthly  | Visual inspection, filter check, alarm log review |
| Quarterly| Refrigerant check, electrical connections, fan amperage |
| Annually | Full system audit, oil analysis, coil cleaning |

## Safety Requirements
- [[sops/sop-high-pressure-lockout]]
- [[sops/sop-refrigerant-leak-check]]
- [[sops/sop-electrical-safety]]
