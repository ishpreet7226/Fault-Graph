---
id: "FAIL-LG-CH03"
type: "failure_mode"
name: "CH03 Remote Control Communication Error"
severity: "medium"
equipment_type: "Split AC/VRF"
manufacturer: "LG"
error_code: "CH03"
subsystems: ["communication", "control_board"]
components: ["remote_controller", "comm_cable", "indoor_pcb"]
---

# CH03 Remote Control Communication Error

**LG CH03** is an error indicating that the wired remote controller is failing to communicate with the indoor unit.

## Root Causes
1. **Wiring Issue**: The communication wire between the remote and the indoor unit is severed or loose.
2. **Interference**: Electromagnetic interference on the communication wire.
3. **Component Failure**: The remote controller or the indoor unit PCB has failed.

## Safety Warnings
- ⚠️ Disconnect power before servicing.
- ⚠️ Do not mix high voltage power and low voltage communication lines.

## Repair Steps
1. Power cycle the system to see if the communication resets.
2. Inspect the communication wire between the wired remote and the indoor unit.
3. Check for proper voltage on the communication terminals at the indoor unit.
4. Ensure the communication wire is routed away from high voltage sources to avoid interference.
5. Replace the wired remote or the indoor PCB if wiring is verified good.
