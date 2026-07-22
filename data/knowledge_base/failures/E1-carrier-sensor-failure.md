---
id: FAIL-CAR-E1
type: failure_mode
name: E1 Sensor / Board Failure
severity: high
equipment_type: Chiller
manufacturer: Carrier
error_code: E1
subsystems:
- sensors
- control_board
components:
- thermistor
- main_board
---

# E1 Sensor / Board Failure

**Carrier E1** error typically points to a primary sensor failure or a main board input failure on certain chiller models.

## Root Causes
1. **Sensor Fault**: A primary temperature sensor has gone out of range (open or short).
2. **Board Fault**: The main control board ADC is failing to read the sensor.
3. **Wiring Issue**: Loose connection at the board terminal.

## Safety Warnings
- Lock out and tag out the chiller before opening the main control panel.

## Repair Steps
1. Access the main control panel.
2. Locate the primary sensor inputs.
3. Check the wiring harness for secure connections.
4. Measure the sensor resistance and compare with the Carrier sensor chart.
5. If the sensor is good, the main board may need replacement.
