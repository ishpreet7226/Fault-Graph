---
id: sops/sop-high-pressure-lockout
type: sop
name: "SOP-High-Pressure-Lockout"
sop_number: "SOP-REF-001"
version: "2.3"
effective_date: "2024-01-15"
review_date: "2025-01-15"
category: "Refrigeration Safety"
severity: critical
applicable_failures:
  - failures/E3-high-pressure-trip
  - failures/E5-high-discharge-temp
  - failures/U0-refrigerant-loss
applicable_assets:
  - assets/chiller-carrier-30rap
  - assets/chiller-york-yvaa
ppe_required:
  - "Safety glasses / face shield"
  - "Refrigerant-rated gloves (cryogenic)"
  - "Refrigerant recovery equipment"
tools_required:
  - "Manifold gauge set (R-410A or R-134a rated)"
  - "Digital refrigerant scale"
  - "Lockout/Tagout (LOTO) kit"
tags: [SOP, lockout, refrigerant, pressure, safety, critical, mandatory]
---

# SOP-High-Pressure-Lockout (SOP-REF-001)

## Purpose
This procedure establishes mandatory safety requirements for working on or near high-pressure refrigerant systems after a high-pressure lockout event (fault codes [[failures/E3-high-pressure-trip]], [[failures/E5-high-discharge-temp]], or [[failures/U0-refrigerant-loss]]).

## ⚠️ PRE-WORK HAZARD ASSESSMENT
> **DANGER**: High-pressure refrigerant systems operate at pressures up to 650 psig. Uncontrolled release can cause severe injury or death from pressure blast, cryogenic burns, or asphyxiation.

## Applicable Equipment
- [[assets/chiller-carrier-30rap]] (R-410A, max 650 psig)
- [[assets/chiller-york-yvaa]] (R-134a, max 280 psig)

## Required PPE
| Item | Specification |
|------|--------------|
| Eye protection | ANSI Z87.1 rated safety glasses + face shield |
| Gloves | Cryogenic-rated refrigerant handling gloves |
| Clothing | No loose clothing; long sleeves required |

## Step-by-Step Lockout Procedure

### Phase 1: System Shutdown Verification
1. Confirm unit is in fault/lockout state via controller display
2. Place unit master switch in the **OFF** position
3. **DO NOT reset** the fault until root cause investigation is complete
4. Allow system pressures to equalize and temperatures to cool (minimum 30 minutes)
5. Verify discharge pressure has dropped below 150 psig before approaching compressor

### Phase 2: LOTO Execution
6. Notify operations/facility manager of unit shutdown
7. Apply **Lockout/Tagout** on the unit main disconnect switch
   - One lock per technician working on the unit
   - Tag must include: technician name, date, reason, contact number
8. Verify zero energy state — attempt to restart from controller (should not respond)
9. Install manifold gauge set on low and high service ports
10. Verify pressure readings on gauges before opening any refrigerant connections

### Phase 3: Work Authorization
11. Complete work permit if required by facility procedures
12. Verify refrigerant recovery equipment is on-site and operational
13. Proceed with diagnostic or repair work per applicable procedure

### Phase 4: System Restore
14. Remove all tools, manifold gauges, and foreign materials
15. Remove LOTO devices only by the technician who applied them
16. Restore unit main disconnect switch
17. Investigate and document root cause before resetting fault
18. Reset fault at controller only after verifying root cause is resolved
19. Monitor unit for minimum 2 hours after restart

## Documentation Requirements
- Record fault code, date/time, ambient conditions
- Log all refrigerant quantities added or recovered
- Complete maintenance work order with findings and actions taken
