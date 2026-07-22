---
id: components/refrigerant-level-sensor
type: component
name: Refrigerant Level / Suction Pressure Transducer
part_numbers:
- RPT-0-500-4T
- RPT-0-300-4T
sensor_type: piezoelectric pressure transducer
signal_type: 4-20mA
range_psi:
  R-410A:
  - 0
  - 500
  R-134a:
  - 0
  - 300
alarm_setpoint_psi:
  R-410A_low: 68
  R-134a_low: 25
severity: high
tags:
- pressure
- transducer
- refrigerant
- suction
- level
- sensor
parent_subsystems:
- subsystems/refrigerant-circuit
- subsystems/electrical-control-panel
connected_failures:
- failures/U0-refrigerant-loss
connected_sops:
- sops/sop-refrigerant-leak-check
---

# Refrigerant Level / Suction Pressure Transducer

## Overview
The suction pressure transducer provides a continuous 4-20mA signal proportional to refrigerant suction pressure, which the controller uses to:
1. Calculate suction saturation temperature
2. Monitor refrigerant charge level (indirect method)
3. Detect low refrigerant conditions triggering [[failures/U0-refrigerant-loss]]

## Specifications

| Parameter | R-410A | R-134a |
|-----------|--------|--------|
| Range | 0–500 psig | 0–300 psig |
| Output | 4-20mA | 4-20mA |
| Low alarm | <68 psig (≈30°F sat.) | <25 psig (≈20°F sat.) |
| Accuracy | ±1% FS | ±1% FS |

## Diagnostic Procedure
1. Connect calibrated pressure gauge to Schrader access valve
2. Compare gauge reading to controller displayed suction pressure
3. If deviation >5 psi, recalibrate or replace transducer
4. Check 4-20mA signal with clamp meter at controller input terminals
5. Inspect transducer body for refrigerant wetting (indicates seal failure)

## Connected Failures
- [[failures/U0-refrigerant-loss]] — Activated when suction pressure falls below low alarm threshold

## Safety
- [[sops/sop-refrigerant-leak-check]] — Required when inspecting transducer connections
