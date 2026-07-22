---
id: asset/ahu-trane-tam
type: asset
name: Trane TAM Air Handling Unit
model: Trane TAM
manufacturer: Trane Technologies
capacity: 5000-50000 CFM
refrigerant: N/A
severity: critical
installed_date: '2020-01-15'
health_score: 67
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
- failures/A1-supply-fan-fault
- failures/A2-return-fan-fault
- failures/A3-damper-fault
- failures/F1-compressor-overcurrent
- failures/H1-high-pressure-sensor-faul
---

# Trane TAM Air Handling Unit

## Overview
The **Trane TAM** manufactured by **Trane Technologies** is a production HVAC asset
with capacity **5000-50000 CFM** using **N/A** refrigerant.

## Major Subsystems
- [[subsystems/condenser-assembly]]
- [[subsystems/compressor-unit]]
- [[subsystems/refrigerant-circuit]]
- [[subsystems/electrical-control-panel]]
- [[subsystems/evaporator-coil]]
- [[subsystems/expansion-valve]]

## Known Failure Modes
- [[failures/a1-supply-fan-fault]]
- [[failures/a2-return-fan-fault]]
- [[failures/a3-damper-fault]]
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
