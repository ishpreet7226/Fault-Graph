---
id: "FAIL-MIT-E4"
type: "failure_mode"
name: "E4 Signal Error"
severity: "high"
equipment_type: "Split AC"
manufacturer: "Mitsubishi"
error_code: "E4"
subsystems: ["communication", "control_board"]
components: ["comm_cable", "indoor_pcb", "outdoor_pcb"]
---

# E4 Signal Error

**Mitsubishi E4** indicates a signal transmission error between the indoor and outdoor units.

## Root Causes
1. **Wiring Issue**: The signal wire (typically S3) is broken, disconnected, or crossed with power wires.
2. **Interference**: Strong electromagnetic interference is disrupting the signal.
3. **PCB Failure**: The indoor or outdoor communication circuit has failed.

## Safety Warnings
- ⚠️ Disconnect power before servicing.
- ⚠️ High voltage is present on the terminal block; use caution.

## Repair Steps
1. Disconnect power to the system.
2. Verify the wiring between the indoor and outdoor units, specifically the signal wire.
3. Restore power and measure fluctuating DC voltage on the signal terminal relative to neutral.
4. Check for any sources of electromagnetic interference.
5. If the wiring is correct and voltage is not fluctuating as expected, replace the outdoor or indoor PCB.
