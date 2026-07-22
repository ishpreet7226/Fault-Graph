---
id: FAIL-SAMSUNG-E3
type: failure_mode
name: E3 Indoor Fan Motor Error
severity: high
equipment_type: Split AC
manufacturer: Samsung
error_code: E3
subsystems:
- fan
- control_board
components:
- indoor_fan_motor
- indoor_pcb
---

# E3 Indoor Fan Motor Error

**Samsung E3** indicates an error with the indoor fan motor rotation, such as a locked rotor or failure to reach target RPM.

## Root Causes
1. **Motor Failure**: The indoor fan motor has failed internally.
2. **Obstruction**: The fan blower wheel is physically blocked from turning.
3. **PCB Failure**: The fan control circuit on the PCB has failed.

## Safety Warnings
- ⚠️ Disconnect power before servicing.
- ⚠️ Ensure the blower wheel has completely stopped before touching it.

## Repair Steps
1. Disconnect power to the unit.
2. Manually spin the indoor blower wheel to check for mechanical binding or obstruction.
3. Inspect the motor wiring harness and PCB connections.
4. Check the fan motor capacitor (if applicable) and motor windings with a multimeter.
5. Replace the fan motor or PCB depending on the diagnostic results.
