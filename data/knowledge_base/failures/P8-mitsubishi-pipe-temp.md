---
id: "FAIL-MIT-P8"
type: "failure_mode"
name: "P8 Pipe Temperature Error"
severity: "medium"
equipment_type: "VRF/Split"
manufacturer: "Mitsubishi"
error_code: "P8"
subsystems: ["sensors", "refrigeration_circuit"]
components: ["pipe_thermistor"]
---

# P8 Pipe Temperature Error

**Mitsubishi P8** indicates an abnormality with the pipe temperature sensor on the indoor unit.

## Root Causes
1. **Sensor Fault**: Thermistor is open or shorted.
2. **Refrigerant Issue**: Low refrigerant leading to abnormal coil temperatures.

## Safety Warnings
- Turn off main power before opening the unit.

## Repair Steps
1. Power off the system.
2. Locate the pipe temperature thermistor on the indoor coil.
3. Check the connector on the control board.
4. Measure sensor resistance and compare with the manufacturer's thermistor table.
5. Replace if faulty.
