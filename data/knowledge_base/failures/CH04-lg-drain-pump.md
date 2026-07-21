---
id: "FAIL-LG-CH04"
type: "failure_mode"
name: "CH04 Drain Pump Error"
severity: "high"
equipment_type: "VRF/Split"
manufacturer: "LG"
error_code: "CH04"
subsystems: ["drainage", "control_board"]
components: ["drain_pump", "float_switch", "indoor_pcb"]
---

# CH04 Drain Pump Error

**LG CH04** indicates a failure in the condensate drainage system, usually triggered when the float switch detects a high water level for too long.

## Root Causes
1. **Clogged Drain**: The condensate drain line is obstructed.
2. **Pump Failure**: The condensate drain pump has failed mechanically or electrically.
3. **Float Switch Issue**: The float switch is stuck or defective.

## Safety Warnings
- ⚠️ Disconnect power before servicing the drain pump to avoid electric shock.
- ⚠️ Beware of water spillage when accessing the drain pan.

## Repair Steps
1. Disconnect power to the indoor unit.
2. Check the drain pan for standing water.
3. Inspect and clear any blockages in the condensate drain line.
4. Check the float switch operation (it should move freely and break/make contact properly).
5. Verify voltage is reaching the drain pump. If voltage is present but the pump does not run, replace the pump.
