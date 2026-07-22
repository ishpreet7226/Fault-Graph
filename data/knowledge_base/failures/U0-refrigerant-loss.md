---
id: failures/U0-refrigerant-loss
type: failure
name: U0 — Refrigerant Loss / Low Charge
error_code: U0
severity: critical
affected_models:
- Carrier 30RAP
- York YVAA
affected_subsystems:
- subsystems/refrigerant-circuit
- subsystems/compressor-unit
affected_components:
- components/refrigerant-level-sensor
- components/high-pressure-switch
root_causes:
- Refrigerant leak at brazed joint or flare fitting
- Schrader valve core leak
- Service valve packing leak
- Evaporator or condenser coil micro-leak
- Improper refrigerant recovery/recharge procedure
connected_sops:
- sops/sop-refrigerant-leak-check
- sops/sop-high-pressure-lockout
tags:
- u0
- refrigerant
- loss
- leak
- undercharge
- low-pressure
- r-410a
- r-134a
regulatory_requirements:
- EPA Section 608 - Refrigerant Recovery Required
- ASHRAE 15 - Safety Standard
- Local refrigerant handling regulations
---

# U0 — Refrigerant Loss / Low Charge

## Description
Error code **U0** indicates the refrigerant charge level has dropped below the minimum operating threshold, detected via suction pressure monitoring by the [[components/refrigerant-level-sensor]]. Operating with insufficient refrigerant causes the compressor to overheat, and may result in catastrophic compressor failure if not addressed.

## ⚠️ SAFETY ALERT
> **DANGER — ENVIRONMENTAL HAZARD**: Refrigerant release is regulated under EPA Section 608. It is ILLEGAL to knowingly vent refrigerant to atmosphere.
>
> **DANGER — ASPHYXIATION RISK**: R-410A is heavier than air and can displace oxygen in confined spaces. Ensure adequate ventilation before entering equipment rooms.
>
> **MANDATORY PROCEDURE**: [[sops/sop-refrigerant-leak-check]] must be followed for all U0 events.

## Root Cause Analysis

| Priority | Root Cause | Diagnostic Method |
|----------|-----------|------------------|
| 1 | Brazed joint leak | Electronic leak detector, UV dye |
| 2 | Schrader valve leak | Soap bubbles / electronic detector |
| 3 | Service valve packing | Visual inspection under pressure |
| 4 | Coil micro-leak | Nitrogen pressure test |
| 5 | Recharge procedure error | Compare charge vs. factory spec |

## Step-by-Step Repair Guide
1. **Do NOT add refrigerant without finding the leak first**
2. Follow [[sops/sop-refrigerant-leak-check]] — use calibrated electronic leak detector
3. Inspect all brazed fittings (prioritize: service valves, filter dryer connections, evaporator headers)
4. Check all Schrader access valve cores with valve core tool
5. If leak rate is high — recover refrigerant per EPA Section 608, repair leak
6. Perform nitrogen pressure test at 150 psig (R-410A systems) to confirm repair
7. Pull deep vacuum (<500 microns) before recharging
8. Recharge to manufacturer specifications (weight charge or by subcooling target)
9. Verify system performance and monitor for recurrence

## Regulatory Compliance
This fault requires mandatory documentation:
- Leak location and quantity released (if any)
- Repair method and verification test
- Refrigerant added (EPA Section 608 log)

## Affected Systems
- [[subsystems/refrigerant-circuit]] — Primary affected system
- [[subsystems/compressor-unit]] — Secondary damage risk from overheating
