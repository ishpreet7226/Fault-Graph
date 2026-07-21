---
id: "FAIL-MIT-E2"
type: "failure_mode"
name: "E2 Sensor Error"
severity: "medium"
equipment_type: "Split AC"
manufacturer: "Mitsubishi"
error_code: "E2"
subsystems: ["sensors", "control_board"]
components: ["temperature_sensor", "indoor_pcb"]
---

# E2 Sensor Error

**Mitsubishi E2** indicates a general sensor error on the indoor unit, often related to the room temperature or coil temperature thermistor.

## Root Causes
1. **Sensor Failure**: The thermistor is open or shorted.
2. **Wiring Issue**: Loose connection at the PCB terminal.
3. **PCB Failure**: The PCB cannot read the sensor correctly.

## Safety Warnings
- ⚠️ Disconnect power before handling internal components.

## Repair Steps
1. Disconnect power to the unit.
2. Identify the faulty sensor (room or coil) based on specific sub-codes or by testing both.
3. Inspect the wiring harnesses for the sensors.
4. Measure resistance using a multimeter and compare with Mitsubishi service data.
5. Replace the sensor if it is out of tolerance.
