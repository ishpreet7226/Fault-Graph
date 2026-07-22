---
id: asset/chiller-trane-rtaf
type: asset
name: Trane RTAF Air-Cooled Chiller
model: Trane RTAF
manufacturer: Trane Technologies
capacity: 70-240 tons
refrigerant: R-410A
severity: critical
installed_date: '2020-01-15'
health_score: 82
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
- failures/F2-condenser-fan-overcurrent
- failures/H2-low-pressure-sensor-fault
---

# Trane RTAF Air-Cooled Chiller

## Overview
The **Trane RTAF** manufactured by **Trane Technologies** is a production HVAC asset
with capacity **70-240 tons** using **R-410A** refrigerant.

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
- [[failures/f2-condenser-fan-overcurrent]]
- [[failures/h2-low-pressure-sensor-fault]]

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
