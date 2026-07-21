---
id: "FAIL-SAMSUNG-E4"
type: "failure_mode"
name: "E4 Room Temperature Sensor Error"
severity: "medium"
equipment_type: "Split AC"
manufacturer: "Samsung"
error_code: "E4"
subsystems: ["sensors", "control_board"]
components: ["room_temp_sensor", "indoor_pcb"]
---

# E4 Room Temperature Sensor Error

**Samsung E4** indicates an error with the room temperature sensor (often a short or open circuit).

## Root Causes
1. **Sensor Failure**: The room temperature sensor has failed.
2. **Wiring Issue**: Loose or broken wire at the sensor or PCB terminal.
3. **PCB Failure**: The PCB is no longer properly interpreting the sensor signal.

## Safety Warnings
- ⚠️ Disconnect power before touching PCB or sensors.

## Repair Steps
1. Disconnect power to the unit.
2. Locate the room temperature sensor, usually on the front of the indoor coil.
3. Check the wiring harness connecting it to the PCB.
4. Measure sensor resistance and compare with the manufacturer's data chart.
5. Replace the sensor if it is out of specification.
