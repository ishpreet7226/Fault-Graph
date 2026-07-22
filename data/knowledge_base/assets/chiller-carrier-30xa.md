---
id: asset/chiller-carrier-30xa
type: asset
name: Carrier 30XA Screw Chiller
model: Carrier 30XA
manufacturer: Carrier
capacity: 200-500 tons
refrigerant: R-134a
severity: critical
installed_date: '2020-01-15'
health_score: 79
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
- failures/F3-oil-pressure-fault
- failures/P2-phase-sequence-error
---

# Carrier 30XA Screw Chiller

## Overview
The **Carrier 30XA** manufactured by **Carrier Corporation** is a production HVAC asset
with capacity **200-500 tons** using **R-134a** refrigerant.

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
- [[failures/f3-oil-pressure-fault]]
- [[failures/p2-phase-sequence-error]]

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
