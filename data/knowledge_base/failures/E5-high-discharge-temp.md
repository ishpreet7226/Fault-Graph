---
id: failures/E5-high-discharge-temp
type: failure
name: E5 — High Discharge Temperature
error_code: E5
severity: critical
affected_models:
- Carrier 30RAP
- York YVAA
affected_subsystems:
- subsystems/compressor-unit
- subsystems/refrigerant-circuit
- subsystems/condenser-assembly
affected_components:
- components/discharge-temperature-sensor
- components/high-pressure-switch
root_causes:
- Low refrigerant charge (high superheat)
- Condenser fouling / inadequate heat rejection
- TXV/EEV malfunction (low flow)
- Compressor valve failure (internal bypass)
- Excessive suction superheat
- Defective discharge temperature sensor
connected_sops:
- sops/sop-high-pressure-lockout
- sops/sop-refrigerant-leak-check
tags:
- e5
- discharge-temperature
- thermal
- compressor
- overheating
- critical
---

# E5 — High Discharge Temperature

## Description
Error code **E5** indicates that the compressor discharge gas temperature has exceeded the protective shutdown setpoint (typically **240°F** for R-410A systems). High discharge temperatures cause oil breakdown, compressor valve damage, and motor winding degradation. This is a **manual reset** fault.

## ⚠️ SAFETY ALERT
> **WARNING**: Allow the compressor to cool for at least 30 minutes before any service work. Discharge line temperatures can exceed 250°F immediately after trip.
>
> **MANDATORY PROCEDURE**: [[sops/sop-high-pressure-lockout]] required before refrigerant system work.

## Root Cause Analysis

| Priority | Root Cause | Diagnostic Test |
|----------|-----------|----------------|
| 1 (Most Common) | Low refrigerant charge | Measure suction superheat (>15°F = undercharged) |
| 2 | Condenser fouling | Clean coil, check discharge pressure |
| 3 | TXV/EEV malfunction | Measure superheat differential |
| 4 | Compressor valve failure | Check compression ratio, oil dilution |
| 5 | Faulty sensor | Verify with reference thermometer |

## Step-by-Step Repair Guide
1. **Allow cool-down** — minimum 30 minutes after shutdown
2. Follow [[sops/sop-high-pressure-lockout]] protocol
3. Connect manifold gauges — record suction and discharge pressures
4. Calculate suction superheat: `Tsuction_actual - Tsat_suction`
5. If superheat >15°F → undercharge → perform [[sops/sop-refrigerant-leak-check]]
6. Check condenser coil and fans — address [[failures/E3-high-pressure-trip]] if concurrent
7. Verify [[components/discharge-temperature-sensor]] accuracy vs. reference probe
8. If compressor valve failure suspected → send oil sample for lab analysis
9. Recharge refrigerant to spec subcooling/superheat if leak source repaired
10. Reset fault and monitor discharge temperature closely for first 2 hours of operation

## Affected Systems
- [[subsystems/compressor-unit]] — Primary affected system
- [[subsystems/refrigerant-circuit]] — Undercharge most common root cause
- [[subsystems/condenser-assembly]] — Secondary contributing factor
