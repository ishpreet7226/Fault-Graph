---
id: FAIL-SAM-C154
type: failure_mode
name: C154 Indoor Fan Motor Error
severity: high
equipment_type: Split AC
manufacturer: Samsung
error_code: C154
subsystems:
- air_handling
- control_board
components:
- indoor_fan_motor
- pcb
---

# C154 Indoor Fan Motor Error

**Samsung C154** signifies a failure in the indoor unit's fan motor rotation feedback. The PCB is sending power to the motor but not receiving RPM feedback pulses.

## Root Causes
1. **Motor Failure**: The BLDC fan motor has failed mechanically or electronically.
2. **Obstruction**: Something is physically blocking the blower wheel from turning.
3. **PCB Failure**: The motor driver on the PCB is damaged.

## Safety Warnings
- Fan motor operates at high voltage (often 310V DC). Ensure unit is fully discharged before touching motor terminals.

## Repair Steps
1. Disconnect power to the unit.
2. Try spinning the indoor blower wheel by hand. It should spin freely. Remove any obstructions.
3. Inspect the motor wiring harness and connector on the PCB.
4. Measure the voltage at the PCB fan motor terminal (check manual for exact pinout, usually Vdc, Vcc, Vsp, FG, GND).
5. If power is supplied but the motor does not spin, replace the fan motor.
6. If the motor still doesn't spin after replacement, replace the main PCB.
