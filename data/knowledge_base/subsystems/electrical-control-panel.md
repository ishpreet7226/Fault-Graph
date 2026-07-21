---
id: subsystems/electrical-control-panel
type: subsystem
name: "Electrical Control Panel"
parent_assets:
  - assets/chiller-carrier-30rap
  - assets/chiller-york-yvaa
severity: high
components:
  - components/fan-motor
  - components/discharge-temperature-sensor
  - components/refrigerant-level-sensor
tags: [control-panel, microprocessor, Pro-Dialog, Microgateway, electrical, BMS]
connected_failures:
  - failures/A6-fan-motor-fault
  - failures/103-prestart-temp-alert
connected_sops:
  - sops/sop-electrical-safety
---

# Electrical Control Panel

## Overview
The electrical control panel houses the chiller microprocessor controller, variable frequency drives (if equipped), contactors, overloads, fuses, control transformers, and all monitoring/sensor wiring. Carrier units use the **Pro-Dialog Plus** controller; York units use the **Microgateway+** controller with optional BACnet/Modbus communication modules.

## Components

- [[components/fan-motor]] — Fan motor contactors, overloads, and wiring terminations
- [[components/discharge-temperature-sensor]] — Sensor signal conditioning and analog input wiring
- [[components/refrigerant-level-sensor]] — Pressure transducer 4-20mA signal processing

## Common Failure Modes

| Failure | Root Cause | Effect |
|---------|-----------|--------|
| [[failures/A6-fan-motor-fault]] | Overload trip, wiring fault, contactor failure | Fan motor shutoff → heat rejection loss |
| [[failures/103-prestart-temp-alert]] | Low ambient startup, sensor calibration drift | Delayed startup or lockout |

## Diagnostic Approach
1. Verify incoming power voltage and phase balance (<2% imbalance)
2. Check all control fuses and circuit breakers
3. Inspect contactor contacts for pitting or burning
4. Verify sensor calibration against known references
5. Check controller firmware version and event log

## Safety
- [[sops/sop-electrical-safety]] — All panel work requires LOTO procedure compliance
