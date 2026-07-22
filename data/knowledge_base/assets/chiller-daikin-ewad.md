---
id: asset/chiller-daikin-ewad
type: asset
name: Daikin EWAD Air-Cooled Chiller
model: Daikin EWAD
manufacturer: Daikin Applied
capacity: 80-450 tons
refrigerant: R-410A
severity: critical
installed_date: '2020-01-15'
health_score: 80
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
- failures/A6-fan-motor-fault
- failures/E7-outdoor-unit-overload
- failures/E8-discharge-pipe-overheat
---

# Daikin EWAD Air-Cooled Chiller

## Overview
The **Daikin EWAD** manufactured by **Daikin Applied** is a production HVAC asset
with capacity **80-450 tons** using **R-410A** refrigerant.

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
- [[failures/a6-fan-motor-fault]]
- [[failures/e7-outdoor-unit-overload]]
- [[failures/e8-discharge-pipe-overheat]]

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
