---
id: failure_chains/condensor-fan-fouling
type: failure_chain
name: "Failure Chain — Condenser Fouling → Fan Motor Stress → High Pressure Trip"
severity: high
tags: [failure-chain, condenser, fan, high-pressure]
---

# Failure Chain: Condenser Fouling -> Fan Motor Stress -> E3 High Pressure Trip

Summary:

A heavily fouled condenser reduces heat rejection causing elevated head pressure. Over time this increases fan motor load and may result in fan motor faults (A6) or bearing failures, which further reduce airflow and can trigger high-pressure trip (E3).

Sequence:

1. [[assets/chiller-carrier-30rap]] — condenser coil becomes fouled (debris, cottonwood)
2. Reduced airflow increases head pressure — [[failures/E3-high-pressure-trip]]
3. Fan motor stalls or overloads — [[failures/A6-fan-motor-fault]]
4. If fan motor not repaired, repeated E3 events and compressor stress may occur

Recommended controls:

- Add condenser coil inspection to monthly PM during cottonwood season
- Replace or repair fan motor at first sign of abnormal amperage
- Follow [[sops/sop-high-pressure-lockout]] and [[sops/sop-electrical-safety]]
