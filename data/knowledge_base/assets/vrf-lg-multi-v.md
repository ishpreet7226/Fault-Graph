---
id: asset/vrf-lg-multi-v
type: asset
name: LG Multi V VRF System
model: LG Multi V
manufacturer: LG Electronics
capacity: 6-48 HP
refrigerant: R-410A
severity: critical
installed_date: '2020-01-15'
health_score: 70
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
- failures/CH01-lg-sensor-open-circuit
- failures/CH02-lg-sensor-short-circuit
- failures/CH03-lg-communication-error
- failures/CH04-lg-drain-pump-fault
- failures/CH05-lg-communication-timeout
- failures/CH06-lg-pipe-sensor-error
---

# LG Multi V VRF System

## Overview
The **LG Multi V** manufactured by **LG Electronics** is a production HVAC asset
with capacity **6-48 HP** using **R-410A** refrigerant.

## Major Subsystems
- [[subsystems/condenser-assembly]]
- [[subsystems/compressor-unit]]
- [[subsystems/refrigerant-circuit]]
- [[subsystems/electrical-control-panel]]
- [[subsystems/evaporator-coil]]
- [[subsystems/expansion-valve]]

## Known Failure Modes
- [[failures/ch01-lg-sensor-open-circuit]]
- [[failures/ch02-lg-sensor-short-circuit]]
- [[failures/ch03-lg-communication-error]]
- [[failures/ch04-lg-drain-pump-fault]]
- [[failures/ch05-lg-communication-timeout]]
- [[failures/ch06-lg-pipe-sensor-error]]

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
