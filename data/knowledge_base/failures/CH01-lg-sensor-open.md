---
id: "FAIL-LG-CH01"
type: "failure_mode"
name: "CH01 Room Air Thermistor Open/Short"
severity: "medium"
equipment_type: "VRF/Split"
manufacturer: "LG"
error_code: "CH01"
subsystems: ["sensors"]
components: ["room_thermistor"]
---

# CH01 Room Air Thermistor Open/Short

**LG CH01** indicates that the indoor room air temperature sensor (thermistor) is reading either an open circuit or a short circuit.

## Root Causes
1. **Sensor Disconnected**: The connector is unplugged from the indoor PCB.
2. **Sensor Failed**: The thermistor is damaged.
3. **PCB Damaged**: The ADC circuit on the indoor main board has failed.

## Safety Warnings
- Power off the unit at the disconnect switch before servicing.
- Refer to SOP-ELC-001: Electrical-Safety.

## Repair Steps
1. Power down the indoor unit.
2. Remove the front cover to access the control board and return air sensor.
3. Check CN-TH1 (or similar thermistor connector) for a secure connection.
4. Measure sensor resistance; standard value is 10 kOhms at 25°C.
5. Replace the sensor if resistance is out of tolerance.
