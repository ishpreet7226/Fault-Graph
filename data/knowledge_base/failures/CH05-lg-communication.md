---
id: "FAIL-LG-CH05"
type: "failure_mode"
name: "CH05 Indoor/Outdoor Communication Error"
severity: "critical"
equipment_type: "VRF/Split"
manufacturer: "LG"
error_code: "CH05"
subsystems: ["communication", "control_board"]
components: ["comm_cable", "indoor_pcb", "outdoor_pcb"]
---

# CH05 Indoor/Outdoor Communication Error

**LG CH05** is a critical failure indicating communication has been lost between the indoor and outdoor units.

## Root Causes
1. **Wiring Issue**: Communication cable is broken, loose, or swapped with power lines.
2. **Power Supply**: Indoor or outdoor unit is not receiving power.
3. **Interference**: Electromagnetic interference on the comm line.
4. **PCB Failure**: The communication circuit on either the indoor or outdoor PCB has failed.

## Safety Warnings
- Do not mix high voltage power and low voltage communication lines.
- Verify L1/L2 and Com terminal voltages with a multimeter.

## Repair Steps
1. Verify both indoor and outdoor units are powered on.
2. Check the communication cable (usually terminal 3 on LG) for continuity and secure connections at both ends.
3. Measure DC voltage between the communication terminal and neutral. It should fluctuate between 0 and 75 VDC (or specified range for the model).
4. Check for electrical interference (ensure comm cables are shielded or routed away from high voltage lines).
5. If wiring is good and voltage does not fluctuate, replace the suspected PCB (often the outdoor PCB).
