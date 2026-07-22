---
id: FAIL-MIT-E3
type: failure_mode
name: E3 Remote Controller Communication Error
severity: medium
equipment_type: Split AC
manufacturer: Mitsubishi
error_code: E3
subsystems:
- communication
- control_board
components:
- remote_controller
- comm_cable
- indoor_pcb
---

# E3 Remote Controller Communication Error

**Mitsubishi E3** indicates a loss of communication between the wired remote controller and the indoor unit.

## Root Causes
1. **Wiring Issue**: The communication cable is damaged or disconnected.
2. **Interference**: Electrical noise is disrupting the communication signal.
3. **Hardware Failure**: The remote controller or indoor PCB communication circuit has failed.

## Safety Warnings
- ⚠️ Disconnect power before working on communication or power wiring.

## Repair Steps
1. Verify the remote controller screen is on (if it has power).
2. Check the communication cable for continuity and secure connections at both the remote and indoor PCB.
3. Measure the DC voltage on the communication terminals to ensure signal is present.
4. Ensure the communication wire is shielded or routed away from high-voltage lines.
5. Replace the remote controller or indoor PCB if the wiring is intact but communication fails.
