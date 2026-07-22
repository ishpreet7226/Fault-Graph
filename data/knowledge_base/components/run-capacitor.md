---
id: components/run-capacitor
type: component
name: "Run Capacitor (Condenser Fan Motors)"
component_type: capacitor
model_compatibility: ["Carrier 30RAP", "Generic Fan Motor 1HP"]
severity: medium
tags: [electrical, capacitor, motor-start]
---

# Run Capacitor — Condenser Fan Motors

Run capacitors support condenser fan motor operation by providing the necessary phase shift for efficient motor torque and reduced current draw. Common failure modes include reduced capacitance, open circuits, and dielectric breakdown.

Common symptoms:

- Fan motor fails to reach rated RPM
- Higher-than-normal motor current
- Audible humming from the motor

Mitigation and checks:

- Measure capacitance with an LCR meter and compare to nameplate value (e.g., 25µF).
- Replace with same-rated voltage and microfarad value.
- Check motor start/run circuit and motor bearings for combined issues.

Related knowledge:

- [[components/fan-motor]]
- [[failures/A6-fan-motor-fault]]
- [[assets/chiller-carrier-30rap]]
