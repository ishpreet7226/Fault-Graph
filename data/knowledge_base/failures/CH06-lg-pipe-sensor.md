---
id: "FAIL-LG-CH06"
type: "failure_mode"
name: "CH06 Indoor Pipe Sensor Error"
severity: "medium"
equipment_type: "Split AC/VRF"
manufacturer: "LG"
error_code: "CH06"
subsystems: ["sensors", "control_board"]
components: ["indoor_pipe_sensor", "indoor_pcb"]
---

# CH06 Indoor Pipe Sensor Error

**LG CH06** indicates a failure with the indoor pipe temperature sensor, which is crucial for monitoring evaporator coil temperature.

## Root Causes
1. **Sensor Failure**: The pipe sensor has drifted out of range or failed (short/open).
2. **Wiring Issue**: Loose connection or damaged wire to the indoor PCB.
3. **PCB Failure**: The indoor PCB analog input circuit is malfunctioning.

## Safety Warnings
- ⚠️ Disconnect power before touching PCB or sensors.

## Repair Steps
1. Disconnect power to the indoor unit.
2. Locate the pipe sensor attached to the evaporator coil.
3. Inspect the sensor wiring and connector at the PCB.
4. Measure the sensor resistance and compare against LG's thermistor table.
5. Replace the sensor if it reads open, short, or significantly out of range.
