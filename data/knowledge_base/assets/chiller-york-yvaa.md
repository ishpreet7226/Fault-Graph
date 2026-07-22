---
id: asset/chiller-york-yvaa
type: asset
name: York YVAA Air-Cooled Chiller
model: York YVAA
manufacturer: York International
capacity: 150-350 tons
refrigerant: R-134a
severity: critical
installed_date: '2020-01-15'
health_score: 66
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
- failures/L1-low-refrigerant-pressure
- failures/L2-low-oil-level
- failures/P1-power-supply-fault
---

# York YVAA Air-Cooled Chiller

## Overview
The **York YVAA** manufactured by **York International** is a production HVAC asset
with capacity **150-350 tons** using **R-134a** refrigerant.

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
- [[failures/l1-low-refrigerant-pressure]]
- [[failures/l2-low-oil-level]]
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
