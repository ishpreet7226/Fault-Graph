---
id: asset/vrf-samsung-dvm
type: asset
name: Samsung DVM VRF System
model: Samsung DVM
manufacturer: Samsung HVAC
capacity: 8-48 HP
refrigerant: R-410A
severity: critical
installed_date: '2020-01-15'
health_score: 71
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
- failures/E1-sensor---thermistor-fault
- failures/E2-indoor-thermistor-error
- failures/E3-high-pressure-trip
- failures/E4-signal---communication-er
- failures/E5-high-discharge-temperatur
- failures/C154-bldc-fan-motor-fault
---

# Samsung DVM VRF System

## Overview
The **Samsung DVM** manufactured by **Samsung HVAC** is a production HVAC asset
with capacity **8-48 HP** using **R-410A** refrigerant.

## Major Subsystems
- [[subsystems/condenser-assembly]]
- [[subsystems/compressor-unit]]
- [[subsystems/refrigerant-circuit]]
- [[subsystems/electrical-control-panel]]
- [[subsystems/evaporator-coil]]
- [[subsystems/expansion-valve]]

## Known Failure Modes
- [[failures/e1-sensor---thermistor-fault]]
- [[failures/e2-indoor-thermistor-error]]
- [[failures/e3-high-pressure-trip]]
- [[failures/e4-signal---communication-error]]
- [[failures/e5-high-discharge-temperature]]
- [[failures/c154-bldc-fan-motor-fault]]

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
