---
id: failures/E3-high-pressure-trip
type: failure
name: E3 — High Pressure Trip
error_code: E3
severity: critical
affected_models:
- Carrier 30RAP
- York YVAA
affected_subsystems:
- subsystems/condenser-assembly
- subsystems/compressor-unit
- subsystems/refrigerant-circuit
affected_components:
- components/high-pressure-switch
root_causes:
- Fouled or blocked condenser coil
- Condenser fan motor failure (see A6)
- High ambient temperature (>115°F)
- Refrigerant overcharge
- Non-condensable gases in refrigerant circuit
- Blocked/restricted liquid line
connected_sops:
- sops/sop-high-pressure-lockout
- sops/sop-refrigerant-leak-check
tags:
- e3
- high-pressure
- trip
- lockout
- critical
- compressor
---

# E3 — High Pressure Trip

## Description
Error code **E3** indicates the refrigerant discharge pressure has exceeded the high pressure safety switch setpoint (650 psig for R-410A / 280 psig for R-134a), triggering a hard compressor lockout. This is a **manual reset** fault — the unit will not restart automatically.

## ⚠️ SAFETY ALERT
> **DANGER**: High pressure refrigerant systems can cause severe injury. Do NOT reset this fault without identifying and correcting the root cause. Repeated resets without diagnosis can cause catastrophic compressor failure.
>
> **MANDATORY PROCEDURE**: [[sops/sop-high-pressure-lockout]] must be followed before any service work.

## Root Cause Analysis

| Priority | Root Cause | Diagnostic Test |
|----------|-----------|----------------|
| 1 (Most Common) | Fouled condenser coil | Visual inspection + pressure drop test |
| 2 | Fan motor failure | Measure amperage on all fan legs |
| 3 | High ambient temp | Check weather station data |
| 4 | Refrigerant overcharge | Measure subcooling (target: 8–14°F) |
| 5 | Non-condensable gases | System recovery and recharge |
| 6 | Blocked liquid line | Measure temperature drop across filter-dryer |

## Step-by-Step Repair Guide
1. **DO NOT RESET** — Follow [[sops/sop-high-pressure-lockout]] first
2. Record ambient temperature and time of fault from controller event log
3. Inspect condenser coil — clean with coil cleaner if fouled (>25% blockage)
4. Check all condenser fan motors — verify rotation direction and amperage
5. Connect refrigerant manifold gauges to service ports
6. Measure discharge pressure and subcooling temperature
7. If pressure >500 psig at 85°F ambient → suspect overcharge or non-condensables
8. Address root cause, then manually reset the [[components/high-pressure-switch]]
9. Restart unit and monitor discharge pressure for 30 minutes

## Affected Systems
- [[subsystems/condenser-assembly]] — Primary heat rejection path
- [[subsystems/compressor-unit]] — Protected by this fault
- [[subsystems/refrigerant-circuit]] — May indicate overcharge or contamination
