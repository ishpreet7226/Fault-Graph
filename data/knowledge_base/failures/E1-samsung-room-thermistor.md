---
id: FAIL-SAM-E1
type: failure_mode
name: E1 Room Thermistor Sensor Error
severity: medium
equipment_type: Split AC
manufacturer: Samsung
error_code: E1
subsystems:
- sensors
- control_board
components:
- room_thermistor
- pcb
---

# E1 Room Thermistor Sensor Error

**Samsung E1** indicates that the room temperature thermistor sensor is either open or shorted. The main PCB cannot read the indoor temperature.

## Root Causes
1. **Sensor Disconnected**: Wiring from the thermistor to the PCB is loose or broken.
2. **Sensor Fault**: Thermistor is defective (resistance is out of range).
3. **PCB Fault**: The sensor input circuit on the main board is damaged.

## Safety Warnings
- Ensure power is disconnected before touching PCB components.
- Refer to SOP-ELC-001: Electrical-Safety.

## Repair Steps
1. Power off the unit and wait 3 minutes for capacitors to discharge.
2. Open the indoor unit cover and locate the room thermistor (usually black wire with a black epoxy head near the coils).
3. Inspect the wiring and connector for damage. Ensure it's firmly plugged into the PCB.
4. Disconnect the sensor and measure its resistance with a multimeter. A healthy thermistor typically reads around 10 kOhms at 25°C (77°F).
5. If resistance is infinite or zero, replace the thermistor.
6. If the thermistor is good, inspect the PCB for burn marks or replace the PCB.
