---
id: failures/A6-fan-motor-fault
type: failure
name: A6 — Fan Motor Fault
error_code: A6
severity: high
affected_models:
- Carrier 30RAP
- York YVAA
affected_subsystems:
- subsystems/condenser-assembly
- subsystems/electrical-control-panel
affected_components:
- components/fan-motor
root_causes:
- Motor winding failure (thermal overload)
- Bearing seizure
- Run/start capacitor failure (single-phase motors)
- Contactor failure or welded contacts
- Overload relay nuisance trip
- Phase imbalance or undervoltage
- EC motor drive communication fault (YVAA)
- Fan blade damage causing motor overload
connected_sops:
- sops/sop-electrical-safety
cascade_failures:
- failures/E3-high-pressure-trip
tags:
- a6
- fan
- motor
- fault
- contactor
- overload
- ec
- capacitor
- electrical
---

# A6 — Fan Motor Fault

## Description
Error code **A6** indicates a condenser fan motor fault has been detected by the unit controller. Depending on the unit configuration (number of fan circuits), this may cause a partial or full reduction in condenser airflow capacity, which can quickly cascade into [[failures/E3-high-pressure-trip]] if not addressed promptly.

## ⚠️ SAFETY ALERT
> **DANGER — ELECTRICAL HAZARD**: Fan motors operate at 460VAC or 208-230VAC. Full lockout/tagout is required before any motor service.
>
> **MANDATORY PROCEDURE**: [[sops/sop-electrical-safety]] must be followed before accessing any fan motor or wiring.

## Root Cause Analysis

| Priority | Root Cause | Diagnostic Test |
|----------|-----------|----------------|
| 1 | Capacitor failure | Capacitor meter test (±5% of rating) |
| 2 | Motor winding failure | Megohmmeter winding-to-ground test |
| 3 | Contactor/overload fault | Visual inspection + continuity test |
| 4 | Phase imbalance | Measure voltage on all 3 phases |
| 5 | EC drive fault | Check controller communication error code |
| 6 | Blade/fan damage | Physical inspection |

## Step-by-Step Repair Guide
1. Follow [[sops/sop-electrical-safety]] — LOTO before any work
2. Identify which fan circuit is faulted from controller event log (Fan #1, #2, etc.)
3. Inspect motor visually — look for burned smell, blade damage, seized shaft
4. Check contactor contacts for pitting; verify overload relay trip current setting
5. Measure motor winding resistance (all phases should be equal, within 5%)
6. Perform megohmmeter test (500VDC): >1MΩ = acceptable; <1MΩ = replace motor
7. For single-phase motors: test run and start capacitors with capacitor meter
8. Restore power temporarily and check motor amperage vs. nameplate FLA
9. For EC motors (YVAA): check controller error code for drive fault, update firmware
10. Replace motor if testing confirms winding failure; verify replacement specs match

## Cascade Risk
This fault can trigger [[failures/E3-high-pressure-trip]] within 15–30 minutes depending on ambient temperature and chiller load. **Treat A6 as an urgent service call.**

## Affected Systems
- [[subsystems/condenser-assembly]] — Direct fan failure
- [[subsystems/electrical-control-panel]] — Contactor and control circuit
