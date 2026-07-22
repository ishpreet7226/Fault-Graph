---
id: FAIL-MIT-E6
type: failure_mode
name: E6 Indoor/Outdoor Communication Error
severity: critical
equipment_type: VRF/Split
manufacturer: Mitsubishi
error_code: E6
subsystems:
- communication
- control_board
components:
- comm_cable
- indoor_pcb
- outdoor_pcb
---

# E6 Indoor/Outdoor Communication Error

**Mitsubishi E6** signifies a failure in communication between the indoor and outdoor units, specifically no signal reception at the indoor unit.

## Root Causes
1. **Wiring Issue**: Communication cable is broken or disconnected.
2. **Power Issue**: The outdoor unit is not powered on.
3. **PCB Failure**: The communication circuit on the PCB has failed.

## Safety Warnings
- Ensure both indoor and outdoor power supplies are off before touching comm terminals.

## Repair Steps
1. Verify both indoor and outdoor units have correct power.
2. Check the S1, S2, S3 terminals for secure connections.
3. Measure the DC voltage between S2 and S3; it should fluctuate (typically 12-24V DC).
4. Inspect the communication cable for breaks or shorts.
5. Replace the indoor or outdoor PCB if wiring is verified good.
