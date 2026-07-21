---
id: sops/sop-electrical-safety
type: sop
name: "SOP-Electrical-Safety"
sop_number: "SOP-ELC-001"
version: "4.0"
effective_date: "2024-06-01"
review_date: "2025-06-01"
category: "Electrical Safety"
severity: critical
applicable_failures:
  - failures/A6-fan-motor-fault
  - failures/103-prestart-temp-alert
applicable_assets:
  - assets/chiller-carrier-30rap
  - assets/chiller-york-yvaa
ppe_required:
  - "Arc flash rated PPE (minimum CAT 2: 8 cal/cm²)"
  - "Insulated rubber gloves (Class 00 minimum, 500V rated)"
  - "Safety glasses with side shields"
  - "Arc flash face shield"
  - "Flame-resistant (FR) clothing"
tools_required:
  - "Lockout/Tagout (LOTO) kit"
  - "Calibrated digital multimeter (CAT III 600V minimum)"
  - "Non-contact voltage tester"
  - "Insulated hand tools"
  - "Megohmmeter (500VDC / 1000VDC)"
regulatory_compliance:
  - "NFPA 70E Standard for Electrical Safety in the Workplace (2024)"
  - "OSHA 29 CFR 1910.147 (LOTO)"
  - "OSHA 29 CFR 1910.303"
tags: [SOP, electrical, safety, LOTO, arc-flash, NFPA-70E, mandatory]
---

# SOP-Electrical-Safety (SOP-ELC-001)

## Purpose
This procedure establishes mandatory lockout/tagout (LOTO) and arc flash safety requirements for all electrical work on chiller control panels, fan motor circuits, and associated electrical equipment.

## ⚠️ PRE-WORK HAZARD ASSESSMENT
> **DANGER — ARC FLASH / ELECTROCUTION HAZARD**: Chiller units operate at 460VAC / 480VAC, 3-phase. Contact with energized conductors can cause severe burns, cardiac arrest, or death. NFPA 70E compliance is mandatory.

## Arc Flash Hazard Assessment
| Equipment | Incident Energy | PPE Category |
|-----------|----------------|-------------|
| Main unit disconnect | Up to 12 cal/cm² | CAT 2+ |
| Fan motor contactor | 4-8 cal/cm² | CAT 2 |
| Control panel (120VAC) | <1.2 cal/cm² | CAT 1 |

## Step-by-Step Electrical Safety Procedure

### Phase 1: Pre-Work Preparation
1. Obtain arc flash hazard assessment for specific equipment from facility documentation
2. Don required PPE BEFORE approaching the panel — minimum CAT 2 (8 cal/cm²)
3. Verify test equipment rating: multimeter must be CAT III minimum at working voltage
4. Notify facility operations of planned work and expected duration

### Phase 2: Lockout/Tagout Execution (OSHA 29 CFR 1910.147)
5. Identify ALL energy sources for the equipment:
   - Main electrical disconnect
   - Control power transformer (CPT)
   - Any UPS or backup power source
6. Place all energy-isolation devices (disconnects, breakers) in the **OFF** position
7. Apply personal LOTO lock and tag to each isolation point
   - Tag must show: Name, Date, Reason, Contact
8. **Test for Zero Energy State**:
   - Use non-contact voltage tester first
   - Then use calibrated multimeter to verify 0VAC at work point (Phase-to-Phase, Phase-to-Ground)
   - Attempt normal start — equipment must not energize
9. If stored energy exists (capacitors in VFDs) — wait minimum 5 minutes for discharge, then verify <50VDC

### Phase 3: Work Execution
10. Perform required electrical work with insulated tools only
11. Never work on energized circuits unless required and covered by energized electrical work permit (EEWP)
12. Keep work area clear of unauthorized personnel
13. Do not remove covers that expose other circuits not included in LOTO scope

### Phase 4: Return to Service
14. Verify all work is complete and no tools/materials are left in the panel
15. Replace all covers and guards
16. Remove LOTO devices — only the technician who applied them may remove their own lock
17. Announce "restoring power" and ensure clear zone before energizing
18. Restore power and verify operation
19. Complete and file work order documentation

## Emergency Response
- If electrical contact occurs: **DO NOT TOUCH THE VICTIM** — cut power first
- Call emergency services (911)
- Use AED if cardiac arrest is suspected
- Emergency contacts posted at equipment location
