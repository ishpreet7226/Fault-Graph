---
id: components/discharge-temperature-sensor
type: component
name: Compressor Discharge Temperature Sensor
part_numbers:
- DTS-NTC-10K
- DTS-PT100-3W
sensor_type: NTC thermistor / PT100 RTD
temperature_range_f:
- -40
- 300
alarm_setpoint_f: 220
trip_setpoint_f: 240
severity: high
tags:
- temperature
- sensor
- discharge
- compressor
- thermistor
- rtd
parent_subsystems:
- subsystems/compressor-unit
- subsystems/electrical-control-panel
connected_failures:
- failures/E5-high-discharge-temp
connected_sops:
- sops/sop-electrical-safety
---

# Compressor Discharge Temperature Sensor

## Overview
The discharge temperature sensor is installed in the compressor discharge line within 6–12 inches of the compressor outlet. It monitors the refrigerant gas temperature to protect the compressor from overheating caused by low refrigerant charge, high load, or inadequate heat rejection.

## Specifications

| Parameter | NTC Thermistor | PT100 RTD |
|-----------|----------------|-----------|
| Range | -40°F to 300°F | -40°F to 300°F |
| Accuracy | ±2°F | ±0.5°F |
| Signal type | Resistance (10kΩ @ 77°F) | 4-20mA / voltage |
| Alarm setpoint | 220°F | 220°F |
| Trip setpoint | 240°F | 240°F |

## Diagnostic Procedure
1. Use calibrated reference thermometer to verify sensor accuracy
2. Measure sensor resistance and compare against thermistor curve chart
3. Check wiring continuity from sensor to controller analog input
4. Inspect sensor well for proper thermal paste contact
5. Replace sensor if drift >5°F from reference

## Connected Failures
- [[failures/E5-high-discharge-temp]] — Triggered when sensor reading exceeds trip setpoint

## Safety
- [[sops/sop-electrical-safety]] — Required before disconnecting sensor wiring
