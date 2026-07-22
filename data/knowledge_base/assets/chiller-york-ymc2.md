---
id: asset/chiller-york-ymc2
type: asset
name: York YMC2 Centrifugal Chiller
model: York YMC2
manufacturer: York International
capacity: 300-1000 tons
refrigerant: R-134a
severity: critical
installed_date: '2020-01-15'
health_score: 73
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
- failures/L1-low-refrigerant-pressure
- failures/H1-high-pressure-sensor-faul
- failures/P1-power-supply-fault
---

# York YMC2 Centrifugal Chiller

## Overview
The **York YMC2** manufactured by **York International** is a production HVAC asset
with capacity **300-1000 tons** using **R-134a** refrigerant.

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
- [[failures/l1-low-refrigerant-pressure]]
- [[failures/h1-high-pressure-sensor-fault]]
- [[failures/p1-power-supply-fault]]

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
