---
id: sops/sop-refrigerant-leak-check
type: sop
name: "SOP-Refrigerant-Leak-Check"
sop_number: "SOP-REF-002"
version: "3.1"
effective_date: "2024-03-01"
review_date: "2025-03-01"
category: "Refrigeration Safety / Environmental Compliance"
severity: critical
applicable_failures:
  - failures/U0-refrigerant-loss
  - failures/E3-high-pressure-trip
  - failures/E5-high-discharge-temp
applicable_assets:
  - assets/chiller-carrier-30rap
  - assets/chiller-york-yvaa
ppe_required:
  - "Safety glasses"
  - "Refrigerant-rated gloves"
  - "Self-contained breathing apparatus (SCBA) if >1000 ppm refrigerant detected"
tools_required:
  - "Electronic refrigerant leak detector (calibrated)"
  - "UV dye injection kit"
  - "UV blacklight"
  - "Nitrogen tank with pressure regulator"
  - "Bubble solution (for confirmation)"
regulatory_compliance:
  - "EPA Section 608 (Clean Air Act)"
  - "ASHRAE Standard 15-2022"
  - "OSHA 29 CFR 1910.147"
tags: [SOP, refrigerant, leak, detection, EPA, environmental, compliance, mandatory]
---

# SOP-Refrigerant-Leak-Check (SOP-REF-002)

## Purpose
This procedure defines the mandatory process for refrigerant leak detection, confirmation, documentation, and repair following a [[failures/U0-refrigerant-loss]] alarm or any suspected refrigerant loss event.

## ⚠️ PRE-WORK HAZARD ASSESSMENT
> **ENVIRONMENTAL HAZARD**: It is ILLEGAL under EPA Section 608 to knowingly vent refrigerant. All refrigerant must be captured per federal regulations.
>
> **HEALTH HAZARD**: High refrigerant concentrations can displace oxygen. If refrigerant odor is detected in enclosed spaces, evacuate immediately and ventilate before entering.

## Regulatory Context
- R-410A GWP: 2088 (high global warming potential — regulated)
- R-134a GWP: 1430 (regulated)
- EPA Section 608 requires documentation of all refrigerant releases >5 lbs

## Step-by-Step Leak Detection Procedure

### Phase 1: Preparation
1. Follow [[sops/sop-high-pressure-lockout]] if system pressure is present
2. Calibrate electronic leak detector against known concentration standard
3. Verify facility ventilation is adequate; open doors/vents if in enclosed room
4. Review previous maintenance records for prior leak history

### Phase 2: Electronic Leak Detection
5. Set detector to appropriate refrigerant type (R-410A or R-134a)
6. Allow detector to warm up (60 seconds minimum)
7. Begin systematic scan at **lowest points first** (refrigerant is heavier than air)
8. Scan all brazed joints: evaporator headers, condenser headers, distributor fittings
9. Scan all service valves, Schrader ports, and flare connections
10. Scan filter dryer connections and liquid line fittings
11. Note all locations where detector alarm activates (>10 ppm trigger)

### Phase 3: Confirmation Testing
12. Apply soap bubble solution to all detector alarm locations
13. For difficult-to-access areas, inject UV dye and use UV blacklight
14. Photograph all confirmed leak locations

### Phase 4: Repair and Verification
15. Recover all remaining refrigerant before opening any connections (EPA requirement)
16. Repair leak using appropriate method:
    - Brazed joints: re-braze with nitrogen flow purge
    - Flare fittings: re-flare or replace
    - Service valves: replace packing or valve core
17. Pressure test with dry nitrogen at 150 psig for 24 hours (R-410A) / 100 psig (R-134a)
18. Pull vacuum to <500 microns, hold for 30 minutes to verify integrity
19. Recharge refrigerant to factory weight or target subcooling specification

### Phase 5: Documentation
20. Complete EPA Section 608 refrigerant log:
    - Date, technician, unit ID, refrigerant type
    - Quantity recovered, quantity added
    - Leak location and repair method
21. Update facility maintenance management system (CMMS)
