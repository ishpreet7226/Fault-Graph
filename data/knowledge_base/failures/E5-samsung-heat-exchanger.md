---
id: "FAIL-SAM-E5"
type: "failure_mode"
name: "E5 Heat Exchanger Sensor Error"
severity: "high"
equipment_type: "Split AC"
manufacturer: "Samsung"
error_code: "E5"
subsystems: ["sensors", "refrigeration_circuit"]
components: ["pipe_thermistor", "heat_exchanger"]
---

# E5 Heat Exchanger Sensor Error

**Samsung E5** indicates an abnormality with the indoor heat exchanger (pipe) temperature sensor, commonly used for freeze protection or defrost logic.

## Root Causes
1. **Sensor Fault**: Pipe thermistor is open or shorted.
2. **Refrigerant Issue**: Low refrigerant causing the coil to freeze, sending the temperature out of normal operating range.
3. **Airflow Restriction**: Dirty filters or blower failure causing the coil to freeze.

## Safety Warnings
- High pressure lockout SOP might apply if checking refrigerant.
- Disconnect power before replacing sensors.

## Repair Steps
1. Power off the unit. Check the indoor air filters for severe blockages.
2. Inspect the indoor coil for ice build-up.
3. Locate the pipe thermistor attached to the copper return bend on the indoor coil.
4. Disconnect and measure resistance (typically 10 kOhms at 25°C). Replace if out of range.
5. If the sensor is good, perform a leak check and measure system pressures to ensure adequate refrigerant charge.
