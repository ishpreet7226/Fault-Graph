---
id: FAIL-SAMSUNG-E2
type: failure_mode
name: E2 Indoor Coil Thermistor Error
severity: medium
equipment_type: Split AC
manufacturer: Samsung
error_code: E2
subsystems:
- sensors
- control_board
components:
- indoor_coil_thermistor
- indoor_pcb
---

# E2 Indoor Coil Thermistor Error

**Samsung E2** is a failure indicating a problem with the indoor coil temperature sensor (thermistor), often showing open or short circuit.

## Root Causes
1. **Sensor Failure**: The thermistor itself has failed or is out of range.
2. **Wiring Issue**: The connection between the thermistor and the indoor PCB is loose or broken.
3. **PCB Failure**: The indoor PCB is failing to read the sensor correctly.

## Safety Warnings
- ⚠️ Disconnect power before touching PCB or sensors.
- ⚠️ Ensure the system is completely powered down before replacing components.

## Repair Steps
1. Disconnect power to the unit.
2. Access the indoor unit control board and locate the indoor coil thermistor connection.
3. Inspect the thermistor wiring for any visible damage or loose connections.
4. Measure the resistance of the thermistor with a multimeter and compare to the Samsung specification chart.
5. If resistance is out of range, replace the thermistor. If it is within range, the indoor PCB may need replacement.
