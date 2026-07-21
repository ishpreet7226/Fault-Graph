---
id: "FAIL-MIT-E9"
type: "failure_mode"
name: "E9 Indoor/Outdoor Communication Error"
severity: "critical"
equipment_type: "VRF/Split"
manufacturer: "Mitsubishi"
error_code: "E9"
subsystems: ["communication", "control_board"]
components: ["comm_cable", "indoor_pcb", "outdoor_pcb"]
---

# E9 Indoor/Outdoor Communication Error

**Mitsubishi E9** signifies a communication error between indoor and outdoor units, specifically no signal reception at the outdoor unit (often seen in multi-split or VRF systems).

## Root Causes
1. **Wiring Issue**: Communication cable is broken or miswired.
2. **Power Issue**: Indoor unit(s) are not powered on.
3. **Addressing**: Incorrect addressing on VRF systems.
4. **PCB Failure**: The communication circuit on the outdoor PCB has failed.

## Safety Warnings
- Disconnect power to all units before servicing communication lines.

## Repair Steps
1. Verify all indoor units have power.
2. Check the S1/S2/S3 communication wiring for continuity.
3. Verify system addressing if it's a VRF/CityMulti system.
4. Check DC voltage on the comm line.
5. Replace faulty PCBs if wiring and addressing are correct.
