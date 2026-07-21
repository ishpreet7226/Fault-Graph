---
id: "FAIL-LG-CH02"
type: "failure_mode"
name: "CH02 Indoor Pipe Thermistor Open/Short"
severity: "high"
equipment_type: "VRF/Split"
manufacturer: "LG"
error_code: "CH02"
subsystems: ["sensors", "refrigeration_circuit"]
components: ["pipe_thermistor"]
---

# CH02 Indoor Pipe Thermistor Open/Short

**LG CH02** indicates an issue with the indoor unit pipe temperature sensor. It is crucial for electronic expansion valve (EEV) control and freeze protection.

## Root Causes
1. **Sensor Fault**: Pipe thermistor is shorted or open.
2. **Wiring Issue**: Harness is damaged.

## Safety Warnings
- Power off unit before servicing internal components.

## Repair Steps
1. Power off the indoor unit.
2. Access the evaporator coil and locate the pipe sensor inserted into the copper well.
3. Check the wiring and connector on the PCB.
4. Measure the sensor resistance (typically 5 kOhms at 25°C for LG pipe sensors).
5. Replace sensor if it reads open (infinite) or short (0 Ohms).
