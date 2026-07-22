---
id: asset/vrf-mitsubishi-citymulti
type: asset
name: Mitsubishi City Multi VRF
model: Mitsubishi CityMulti
manufacturer: Mitsubishi Electric
capacity: 8-60 HP
refrigerant: R-410A
severity: critical
installed_date: '2020-01-15'
health_score: 92
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
- failures/E6-indoor-outdoor-communicat
- failures/E9-outdoor-communication-err
- failures/P8-pipe-temperature-anomaly
---

# Mitsubishi City Multi VRF

## Overview
The **Mitsubishi CityMulti** manufactured by **Mitsubishi Electric** is a production HVAC asset
with capacity **8-60 HP** using **R-410A** refrigerant.

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
- [[failures/e6-indoor-outdoor-communication]]
- [[failures/e9-outdoor-communication-error]]
- [[failures/p8-pipe-temperature-anomaly]]

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
