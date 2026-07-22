#!/usr/bin/env python3
"""
generate_dataset.py — Expand Fault-Graph knowledge base and maintenance logs.

Generates OKF markdown files, maintenance logs with connected failure stories,
configurations, and inspection reports for hackathon-scale dataset.
"""

import json
import random
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
KB_DIR = ROOT / "data" / "knowledge_base"
LOGS_PATH = ROOT / "data" / "logs" / "maintenance_logs.json"
CONFIG_DIR = ROOT / "data" / "configurations"
INSPECTION_DIR = ROOT / "data" / "inspection_reports"

random.seed(42)

# ─── Asset Definitions ────────────────────────────────────────────────────────

ASSETS = [
    {"id": "asset/chiller-carrier-30rap", "file": "chiller-carrier-30rap", "name": "Carrier 30RAP Air-Cooled Chiller",
     "model": "Carrier 30RAP", "manufacturer": "Carrier Corporation", "capacity": "50-130 tons", "refrigerant": "R-410A",
     "codes": ["E3", "E5", "U0", "103", "A6", "E1", "E2", "F1", "H1"]},
    {"id": "asset/chiller-york-yvaa", "file": "chiller-york-yvaa", "name": "York YVAA Air-Cooled Chiller",
     "model": "York YVAA", "manufacturer": "York International", "capacity": "150-350 tons", "refrigerant": "R-134a",
     "codes": ["E3", "E5", "U0", "103", "A6", "L1", "L2", "P1"]},
    {"id": "asset/chiller-trane-rtaf", "file": "chiller-trane-rtaf", "name": "Trane RTAF Air-Cooled Chiller",
     "model": "Trane RTAF", "manufacturer": "Trane Technologies", "capacity": "70-240 tons", "refrigerant": "R-410A",
     "codes": ["E3", "E5", "U0", "103", "A6", "F2", "H2"]},
    {"id": "asset/chiller-daikin-ewad", "file": "chiller-daikin-ewad", "name": "Daikin EWAD Air-Cooled Chiller",
     "model": "Daikin EWAD", "manufacturer": "Daikin Applied", "capacity": "80-450 tons", "refrigerant": "R-410A",
     "codes": ["E3", "E5", "U0", "A6", "E7", "E8"]},
    {"id": "asset/chiller-carrier-30xa", "file": "chiller-carrier-30xa", "name": "Carrier 30XA Screw Chiller",
     "model": "Carrier 30XA", "manufacturer": "Carrier Corporation", "capacity": "200-500 tons", "refrigerant": "R-134a",
     "codes": ["E3", "E5", "U0", "103", "A6", "F3", "P2"]},
    {"id": "asset/chiller-york-ymc2", "file": "chiller-york-ymc2", "name": "York YMC2 Centrifugal Chiller",
     "model": "York YMC2", "manufacturer": "York International", "capacity": "300-1000 tons", "refrigerant": "R-134a",
     "codes": ["E3", "E5", "U0", "103", "L1", "H1", "P1"]},
    {"id": "asset/vrf-samsung-dvm", "file": "vrf-samsung-dvm", "name": "Samsung DVM VRF System",
     "model": "Samsung DVM", "manufacturer": "Samsung HVAC", "capacity": "8-48 HP", "refrigerant": "R-410A",
     "codes": ["E1", "E2", "E3", "E4", "E5", "C154"]},
    {"id": "asset/vrf-lg-multi-v", "file": "vrf-lg-multi-v", "name": "LG Multi V VRF System",
     "model": "LG Multi V", "manufacturer": "LG Electronics", "capacity": "6-48 HP", "refrigerant": "R-410A",
     "codes": ["CH01", "CH02", "CH03", "CH04", "CH05", "CH06"]},
    {"id": "asset/vrf-mitsubishi-citymulti", "file": "vrf-mitsubishi-citymulti", "name": "Mitsubishi City Multi VRF",
     "model": "Mitsubishi CityMulti", "manufacturer": "Mitsubishi Electric", "capacity": "8-60 HP", "refrigerant": "R-410A",
     "codes": ["E1", "E2", "E3", "E4", "E5", "E6", "E9", "P8"]},
    {"id": "asset/ahu-trane-tam", "file": "ahu-trane-tam", "name": "Trane TAM Air Handling Unit",
     "model": "Trane TAM", "manufacturer": "Trane Technologies", "capacity": "5000-50000 CFM", "refrigerant": "N/A",
     "codes": ["A1", "A2", "A3", "F1", "H1"]},
]

SUBSYSTEMS = [
    ("condenser-assembly", "Condenser Assembly", "critical", "Air-cooled heat rejection subsystem"),
    ("compressor-unit", "Compressor Unit", "critical", "Scroll/screw compressor bank"),
    ("refrigerant-circuit", "Refrigerant Circuit", "critical", "Closed-loop refrigerant path"),
    ("electrical-control-panel", "Electrical Control Panel", "high", "Microprocessor controller and I/O"),
    ("evaporator-coil", "Evaporator Coil", "high", "Heat absorption heat exchanger"),
    ("expansion-valve", "Expansion Valve Assembly", "high", "TXV/EXV refrigerant metering"),
    ("oil-management", "Oil Management System", "medium", "Compressor oil return and heating"),
    ("water-circuit", "Water/Glycol Circuit", "medium", "Chilled water loop interface"),
    ("fan-array", "Condenser Fan Array", "high", "Variable-speed condenser fans"),
    ("power-distribution", "Power Distribution", "high", "Main disconnect and contactors"),
    ("sensor-network", "Sensor Network", "medium", "Temperature and pressure sensors"),
    ("communication-bus", "Communication Bus", "medium", "BACnet/Modbus field network"),
    ("crankcase-heater", "Crankcase Heater", "medium", "Compressor oil pre-heating"),
    ("filter-dryer", "Filter-Dryer Assembly", "medium", "Moisture and contaminant removal"),
    ("economizer", "Economizer Module", "low", "Free cooling heat exchanger"),
    ("vrf-outdoor-unit", "VRF Outdoor Unit", "critical", "Multi-compressor outdoor module"),
    ("vrf-indoor-unit", "VRF Indoor Unit", "high", "Fan coil / cassette indoor module"),
    ("vrf-refrigerant-piping", "VRF Refrigerant Piping", "high", "Branch selector and piping network"),
    ("ahu-fan-section", "AHU Fan Section", "high", "Supply and return fan assemblies"),
    ("ahu-coil-bank", "AHU Coil Bank", "medium", "Heating/cooling coil section"),
]

COMPONENTS = [
    ("high-pressure-switch", "High Pressure Switch", "critical", "Discharge pressure safety cutout"),
    ("discharge-temperature-sensor", "Discharge Temperature Sensor", "critical", "Compressor discharge thermistor"),
    ("fan-motor", "Condenser Fan Motor", "high", "Direct-drive condenser fan motor"),
    ("refrigerant-level-sensor", "Refrigerant Level Sensor", "high", "Sight glass / level transducer"),
    ("scroll-compressor", "Scroll Compressor", "critical", "Primary refrigeration compressor"),
    ("crankcase-heater-element", "Crankcase Heater Element", "medium", "Immersion oil heater"),
    ("run-capacitor", "Fan Run Capacitor", "high", "Motor start/run capacitor"),
    ("contactors", "Compressor Contactors", "high", "Electrical switching contactors"),
    ("txv-valve", "Thermostatic Expansion Valve", "high", "Refrigerant metering valve"),
    ("filter-dryer", "Filter-Dryer Core", "medium", "Replaceable filter-dryer element"),
    ("suction-pressure-transducer", "Suction Pressure Transducer", "high", "Low-side pressure sensor"),
    ("discharge-pressure-transducer", "Discharge Pressure Transducer", "critical", "High-side pressure sensor"),
    ("leaving-water-temp-sensor", "Leaving Water Temperature Sensor", "medium", "Chilled water outlet RTD"),
    ("entering-water-temp-sensor", "Entering Water Temperature Sensor", "medium", "Chilled water inlet RTD"),
    ("ambient-temp-sensor", "Ambient Temperature Sensor", "low", "Outdoor air temperature probe"),
    ("microprocessor-board", "Microprocessor Control Board", "critical", "Main controller PCB"),
    ("inverter-drive", "Compressor Inverter Drive", "critical", "Variable-speed drive module"),
    ("oil-pressure-switch", "Oil Pressure Switch", "high", "Compressor lubrication monitor"),
    ("liquid-line-solenoid", "Liquid Line Solenoid Valve", "medium", "Refrigerant flow shutoff"),
    ("sight-glass", "Refrigerant Sight Glass", "low", "Visual refrigerant level indicator"),
    ("condenser-coil", "Condenser Coil", "high", "Finned-tube condenser heat exchanger"),
    ("evaporator-coil", "Evaporator Coil", "high", "Shell-and-tube or brazed plate evaporator"),
    ("fan-blade", "Condenser Fan Blade", "medium", "Axial fan blade assembly"),
    ("motor-overload", "Motor Overload Relay", "high", "Thermal overload protection"),
    ("phase-monitor", "Phase Monitor Relay", "high", "Three-phase power quality monitor"),
    ("flow-switch", "Water Flow Switch", "medium", "Chilled water flow verification"),
    ("expansion-tank", "Expansion Tank", "low", "Hydronic system expansion vessel"),
    ("vfd-fan-drive", "Fan VFD Drive", "high", "Variable frequency fan motor drive"),
    ("branch-selector", "VRF Branch Selector Box", "high", "Refrigerant flow distribution"),
    ("room-thermistor", "Room Temperature Thermistor", "medium", "Indoor temperature sensor"),
    ("pipe-temp-sensor", "Pipe Temperature Sensor", "medium", "Refrigerant pipe thermistor"),
    ("pcb-communication", "PCB Communication Module", "medium", "Indoor-outdoor comm board"),
    ("drain-pump", "Condensate Drain Pump", "low", "Indoor unit drain pump"),
    ("bldc-fan-motor", "BLDC Fan Motor", "high", "Brushless DC indoor fan motor"),
    ("high-limit-switch", "High Limit Safety Switch", "critical", "Manual reset safety switch"),
    ("oil-separator", "Oil Separator", "medium", "Compressor oil return separator"),
    ("accumulator", "Suction Accumulator", "medium", "Liquid slug protection vessel"),
    ("check-valve", "Refrigerant Check Valve", "low", "One-way refrigerant valve"),
    ("service-valve", "Service Valve Port", "low", "Refrigerant service access"),
    ("humidity-sensor", "Humidity Sensor", "low", "Return air humidity probe"),
    ("damper-actuator", "Damper Actuator", "medium", "Outside air damper motor"),
    ("belt-drive", "Fan Belt Drive", "medium", "V-belt fan drive assembly"),
    ("bearing-assembly", "Fan Bearing Assembly", "medium", "Pillow block bearings"),
    ("vibration-switch", "Vibration Switch", "medium", "Compressor vibration monitor"),
    ("refrigerant-leak-detector", "Refrigerant Leak Detector", "medium", "Fixed leak detection sensor"),
    ("power-filter", "Power Line Filter", "low", "EMI/RFI power filter"),
    ("surge-protector", "Surge Protector Module", "low", "Electrical surge protection"),
    (" BACnet-gateway", "BACnet Gateway", "low", "Building automation interface"),
    ("display-module", "Operator Display Module", "medium", "Touchscreen HMI panel"),
    ("emergency-stop", "Emergency Stop Button", "high", "E-stop safety circuit"),
]

FAILURE_DEFINITIONS = {
    "E3": ("High Pressure Trip", "critical", "Discharge pressure exceeded safety setpoint",
           ["Fouled condenser coil", "Fan motor failure", "High ambient temperature", "Refrigerant overcharge"]),
    "E5": ("High Discharge Temperature", "critical", "Compressor discharge temperature exceeded limit",
           ["Refrigerant undercharge", "Restricted refrigerant flow", "Failed TXV", "Condenser airflow restriction"]),
    "U0": ("Refrigerant Loss / Low Charge", "critical", "System refrigerant charge below minimum threshold",
           ["Refrigerant leak at braze joint", "Schraeder valve leak", "Evaporator coil leak", "Line set damage"]),
    "103": ("Prestart Temperature Alert", "medium", "Leaving water temperature out of range at startup",
            ["Crankcase heater failure", "Low ambient startup", "Oil dilution", "Extended shutdown"]),
    "A6": ("Fan Motor Fault", "high", "Condenser fan motor electrical fault detected",
           ["Failed run capacitor", "Motor winding short", "Seized bearing", "Phase loss"]),
    "E1": ("Sensor / Thermistor Fault", "medium", "Temperature sensor open or short circuit",
           ["Disconnected thermistor wire", "Failed RTD sensor", "PCB input circuit fault"]),
    "E2": ("Indoor Thermistor Error", "medium", "Indoor coil or room temperature sensor fault",
           ["Thermistor out of range", "Loose connector", "PCB analog input failure"]),
    "E4": ("Signal / Communication Error", "medium", "Control signal or sensor communication fault",
           ["Wiring harness damage", "EMI interference", "PCB communication fault"]),
    "E6": ("Indoor-Outdoor Communication", "high", "VRF indoor-outdoor communication failure",
           ["Comm wire polarity reversed", "PCB failure", "Address conflict"]),
    "E7": ("Outdoor Unit Overload", "critical", "Outdoor compressor thermal/electrical overload",
           ["High head pressure", "Refrigerant overcharge", "Failed condenser fan"]),
    "E8": ("Discharge Pipe Overheat", "critical", "Discharge pipe temperature protection triggered",
           ["Low refrigerant charge", "Restricted airflow", "Failed expansion valve"]),
    "E9": ("Outdoor Communication Error", "high", "Master-slave outdoor unit communication fault",
           ["Comm cable fault", "Address mismatch", "PCB failure"]),
    "F1": ("Compressor Overcurrent", "critical", "Compressor motor current exceeded limit",
           ["Mechanical binding", "High head pressure", "Electrical phase imbalance"]),
    "F2": ("Condenser Fan Overcurrent", "high", "Condenser fan motor current exceeded limit",
           ["Seized fan motor", "Debris blocking blade", "Failed capacitor"]),
    "F3": ("Oil Pressure Fault", "critical", "Compressor oil pressure below minimum",
           ["Oil pump failure", "Low oil level", "Oil separator blockage"]),
    "H1": ("High Pressure Sensor Fault", "high", "Discharge pressure transducer out of range",
           ["Failed pressure transducer", "Open sensor wire", "PCB analog input fault"]),
    "H2": ("Low Pressure Sensor Fault", "medium", "Suction pressure transducer out of range",
           ["Failed transducer", "Moisture in sensor port", "PCB fault"]),
    "L1": ("Low Refrigerant Pressure", "critical", "Suction pressure below minimum operating range",
           ["Refrigerant leak", "TXV stuck closed", "Filter-dryer blockage"]),
    "L2": ("Low Oil Level", "high", "Compressor oil level below minimum",
           ["Oil leak at seal", "Oil return failure", "Extended operation at low load"]),
    "P1": ("Power Supply Fault", "high", "Control power supply voltage out of range",
           ["Failed transformer", "Blown fuse", "Loose terminal connection"]),
    "P2": ("Phase Sequence Error", "high", "Three-phase power sequence incorrect",
           ["Reversed phase wiring", "Failed phase monitor", "Utility power quality issue"]),
    "P8": ("Pipe Temperature Anomaly", "medium", "Refrigerant pipe temperature out of expected range",
           ["Restricted refrigerant flow", "Failed pipe sensor", "Refrigerant charge issue"]),
    "C154": ("BLDC Fan Motor Fault", "high", "Indoor BLDC fan motor drive fault",
             ["Failed BLDC driver", "Motor winding fault", "PCB inverter failure"]),
    "CH01": ("LG Sensor Open Circuit", "medium", "LG VRF temperature sensor open circuit",
             ["Broken thermistor wire", "Connector corrosion", "PCB input fault"]),
    "CH02": ("LG Sensor Short Circuit", "medium", "LG VRF temperature sensor short circuit",
             ["Damaged thermistor", "Water ingress on PCB", "Insulation breakdown"]),
    "CH03": ("LG Communication Error", "high", "LG VRF indoor-outdoor communication fault",
             ["Comm wire fault", "Address conflict", "PCB failure"]),
    "CH04": ("LG Drain Pump Fault", "low", "LG indoor unit condensate drain pump failure",
             ["Clogged drain line", "Failed pump motor", "Float switch stuck"]),
    "CH05": ("LG Communication Timeout", "high", "LG VRF communication timeout between units",
             ["Long comm wire run", "EMI interference", "Failed PCB"]),
    "CH06": ("LG Pipe Sensor Error", "medium", "LG VRF pipe temperature sensor fault",
             ["Sensor displacement", "Failed thermistor", "Loose connection"]),
    "A1": ("Supply Fan Fault", "high", "AHU supply fan motor fault",
           ["Belt failure", "Motor overload", "VFD fault"]),
    "A2": ("Return Fan Fault", "high", "AHU return fan motor fault",
           ["Bearing failure", "Motor winding fault", "VFD communication error"]),
    "A3": ("Damper Fault", "medium", "Outside air damper actuator fault",
           ["Failed actuator motor", "Linkage binding", "Control signal fault"]),
}

SOPS = [
    ("sop-high-pressure-lockout", "SOP-REF-001: High-Pressure Lockout", "critical", "High pressure refrigerant lockout procedure"),
    ("sop-refrigerant-leak-check", "SOP-REF-002: Refrigerant Leak Check", "critical", "EPA-compliant leak detection and repair"),
    ("sop-electrical-safety", "SOP-ELC-001: Electrical Safety", "critical", "LOTO and electrical safety for HVAC service"),
    ("sop-compressor-replacement", "SOP-CMP-001: Compressor Replacement", "critical", "Compressor removal and replacement procedure"),
    ("sop-fan-motor-service", "SOP-FAN-001: Fan Motor Service", "high", "Condenser fan motor replacement procedure"),
    ("sop-refrigerant-recovery", "SOP-REF-003: Refrigerant Recovery", "critical", "Refrigerant recovery before service"),
    ("sop-coil-cleaning", "SOP-MNT-001: Condenser Coil Cleaning", "medium", "Coil cleaning and fouling prevention"),
    ("sop-vrf-commissioning", "SOP-VRF-001: VRF Commissioning", "high", "VRF system startup and commissioning"),
    ("sop-oil-analysis", "SOP-CMP-002: Compressor Oil Analysis", "medium", "Oil sampling and analysis procedure"),
    ("sop-water-treatment", "SOP-WTR-001: Water Loop Treatment", "medium", "Chilled water chemistry management"),
    ("sop-vibration-analysis", "SOP-MNT-002: Vibration Analysis", "medium", "Compressor vibration monitoring"),
    ("sop-bacnet-troubleshoot", "SOP-COM-001: BACnet Troubleshooting", "low", "Building automation communication debug"),
    ("sop-emergency-shutdown", "SOP-SAF-001: Emergency Shutdown", "critical", "Emergency chiller shutdown procedure"),
    ("sop-txv-replacement", "SOP-REF-004: TXV Replacement", "high", "Expansion valve replacement procedure"),
    ("sop-inverter-drive-service", "SOP-ELC-002: Inverter Drive Service", "high", "VFD/inverter drive troubleshooting"),
    ("sop-leak-pressure-test", "SOP-REF-005: Pressure Test After Repair", "high", "Nitrogen pressure test procedure"),
    ("sop-seasonal-startup", "SOP-MNT-003: Seasonal Startup", "medium", "Spring chiller startup checklist"),
    ("sop-winter-shutdown", "SOP-MNT-004: Winter Shutdown", "medium", "Fall chiller shutdown and layup"),
    ("sop-filter-dryer-replacement", "SOP-REF-006: Filter-Dryer Replacement", "medium", "Filter-dryer core replacement"),
    ("sop-crane-rigging", "SOP-SAF-002: Crane Rigging for Compressor", "high", "Heavy lift safety for compressor change"),
]

SITES = [
    "Greenfield Industrial Park - Building A", "Greenfield Industrial Park - Building B",
    "Metro Hospital - Central Plant", "Tech Campus - Data Center Cooling",
    "University Engineering Hall", "Shopping Mall - North Wing",
    "Pharmaceutical Plant - Clean Room HVAC", "Airport Terminal 2 - Gate Area",
    "Corporate HQ - Tower 1", "Manufacturing Floor - Line 3",
]

TECHNICIANS = [
    "M. Rodriguez", "J. Williams", "A. Chen", "R. Patel", "S. O'Brien",
    "K. Nakamura", "D. Johnson", "L. Martinez", "T. Anderson", "P. Kim",
]

EVENT_TYPES = [
    "alarm", "service_call", "preventive_maintenance", "verification",
    "inspection", "emergency_service", "engineering_assessment", "major_repair",
]

CASCADE_STORIES = [
    {
        "title": "Dirty Condenser Cascade",
        "model": "Carrier 30RAP", "asset_prefix": "CAR-30RAP",
        "chain": [
            ("preventive_maintenance", None, "Condenser coil inspection — 35% fouling noted, deferred cleaning"),
            ("alarm", "E3", "E3 High Pressure Trip — first occurrence, manual reset without investigation"),
            ("alarm", "E3", "E3 High Pressure Trip — second occurrence same day"),
            ("service_call", "A6", "A6 Fan Motor Fault — run capacitor failed, coil heavily fouled"),
            ("major_repair", "A6", "Replaced run capacitor and cleaned condenser coil"),
            ("verification", None, "Post-repair verification — pressures normal, unit stable"),
        ],
        "outcomes": ["DEFERRED", "INCOMPLETE", "INCOMPLETE", "PARTIAL", "RESOLVED", "RESOLVED"],
    },
    {
        "title": "Refrigerant Leak Cascade",
        "model": "York YVAA", "asset_prefix": "YRK-YVAA",
        "chain": [
            ("alarm", "U0", "U0 Refrigerant Loss — slow leak detected, temporary recharge"),
            ("service_call", "U0", "Electronic leak detection — found braze joint leak at suction line"),
            ("major_repair", "U0", "Brazed suction line joint, pressure tested, evacuated and recharged"),
            ("alarm", "E5", "E5 High Discharge Temp — occurred during low-charge operation before repair"),
            ("verification", None, "Post-repair verification — subcooling 10°F, superheat 8°F, stable"),
        ],
        "outcomes": ["PARTIAL", "IN PROGRESS", "RESOLVED", "RESOLVED — root cause fixed", "RESOLVED"],
    },
    {
        "title": "Low Ambient Startup Failure",
        "model": "Carrier 30RAP", "asset_prefix": "CAR-30RAP",
        "chain": [
            ("alarm", "103", "103 Prestart Temp Alert — ambient 28°F, crankcase heater not energized"),
            ("service_call", "103", "Crankcase heater circuit open — failed heater element"),
            ("major_repair", "103", "Replaced crankcase heater element, verified 8-hour pre-heat"),
            ("alarm", "E5", "E5 High Discharge Temp — oil dilution from cold startup attempt"),
            ("verification", None, "Post-repair cold start test passed at 25°F ambient"),
        ],
        "outcomes": ["INCOMPLETE", "PARTIAL", "RESOLVED", "RESOLVED", "RESOLVED"],
    },
    {
        "title": "VRF Communication Breakdown",
        "model": "Mitsubishi CityMulti", "asset_prefix": "MIT-CITY",
        "chain": [
            ("alarm", "E6", "E6 Indoor Communication — master indoor unit lost comm with outdoor"),
            ("service_call", "E6", "Found comm wire damaged by recent ceiling work"),
            ("major_repair", "E6", "Replaced S1/S2 communication wire, re-addressed units"),
            ("alarm", "E9", "E9 Outdoor Communication — secondary outdoor lost sync during restart"),
            ("verification", None, "All 12 indoor units communicating, system operational"),
        ],
        "outcomes": ["INCOMPLETE", "PARTIAL", "RESOLVED", "RESOLVED", "RESOLVED"],
    },
    {
        "title": "Compressor Overcurrent Event",
        "model": "Trane RTAF", "asset_prefix": "TRN-RTAF",
        "chain": [
            ("alarm", "F1", "F1 Compressor Overcurrent — Circuit A tripped on high amp draw"),
            ("service_call", "F1", "Found liquid slugging from failed TXV — compressor hard to turn"),
            ("engineering_assessment", "F1", "Engineering review — compressor shows wear, recommend replacement"),
            ("major_repair", "F1", "Replaced TXV and Compressor Circuit A — full system evacuation"),
            ("verification", None, "Post-replacement commissioning — all parameters within spec"),
        ],
        "outcomes": ["INCOMPLETE", "PARTIAL", "IN PROGRESS", "RESOLVED", "RESOLVED"],
    },
]


def write_asset(asset: dict):
    codes_links = "\n".join(
        f"- [[failures/{c.lower()}-{FAILURE_DEFINITIONS[c][0].lower().replace(' ', '-').replace('/', '-')[:30]}]]"
        if c in FAILURE_DEFINITIONS else f"- Error code {c}"
        for c in asset["codes"]
    )
    sub_links = "\n".join(f"- [[subsystems/{s[0]}]]" for s in SUBSYSTEMS[:6])

    content = f"""---
id: {asset['id']}
type: asset
name: "{asset['name']}"
model: "{asset['model']}"
manufacturer: "{asset['manufacturer']}"
capacity: "{asset['capacity']}"
refrigerant: "{asset['refrigerant']}"
severity: critical
installed_date: "2020-01-15"
health_score: {random.randint(65, 98)}
tags: [asset, HVAC, industrial]
connected_subsystems:
{chr(10).join(f'  - subsystems/{s[0]}' for s in SUBSYSTEMS[:6])}
known_error_codes:
{chr(10).join(f'  - failures/{c}-' + FAILURE_DEFINITIONS.get(c, (c,))[0].lower().replace(' ', '-').replace('/', '-')[:25] for c in asset['codes'] if c in FAILURE_DEFINITIONS)}
---

# {asset['name']}

## Overview
The **{asset['model']}** manufactured by **{asset['manufacturer']}** is a production HVAC asset
with capacity **{asset['capacity']}** using **{asset['refrigerant']}** refrigerant.

## Major Subsystems
{sub_links}

## Known Failure Modes
{codes_links}

## Maintenance Schedule
| Interval | Task |
|----------|------|
| Monthly  | Visual inspection, filter check, alarm log review |
| Quarterly| Refrigerant check, electrical connections, fan amperage |
| Annually | Full system audit, oil analysis, coil cleaning |

## Safety Requirements
- [[sops/sop-high-pressure-lockout]]
- [[sops/sop-refrigerant-leak-check]]
- [[sops/sop-electrical-safety]]
"""
    path = KB_DIR / "assets" / f"{asset['file']}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_subsystem(sub_id, name, severity, description):
    content = f"""---
id: subsystems/{sub_id}
type: subsystem
name: "{name}"
severity: {severity}
tags: [subsystem, HVAC]
connected_components:
{chr(10).join(f'  - components/{c[0]}' for c in COMPONENTS[:8])}
---

# {name}

## Description
{description}. This subsystem is critical to overall chiller/VRF system operation.

## Connected Components
{chr(10).join(f'- [[components/{c[0]}]] — {c[1]}' for c in COMPONENTS[:8])}

## Common Failure Modes
- [[failures/E3-high-pressure-trip]]
- [[failures/A6-fan-motor-fault]]
- [[failures/E5-high-discharge-temp]]

## Related SOPs
- [[sops/sop-high-pressure-lockout]]
- [[sops/sop-coil-cleaning]]
"""
    path = KB_DIR / "subsystems" / f"{sub_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or sub_id not in ("condenser-assembly", "compressor-unit", "refrigerant-circuit", "electrical-control-panel"):
        path.write_text(content, encoding="utf-8")


def write_component(comp_id, name, severity, description):
    content = f"""---
id: components/{comp_id}
type: component
name: "{name}"
severity: {severity}
tags: [component, HVAC]
part_of:
  - subsystems/condenser-assembly
  - subsystems/compressor-unit
---

# {name}

## Description
{description}.

## Failure Indicators
- Abnormal readings on connected sensors
- Related error codes in controller event log
- Visual or audible signs during operation

## Related Failures
- [[failures/E3-high-pressure-trip]]
- [[failures/A6-fan-motor-fault]]

## Service Notes
Follow [[sops/sop-electrical-safety]] before any component-level service work.
"""
    path = KB_DIR / "components" / f"{comp_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def write_failure(code, name, severity, description, root_causes, models=None):
    slug = f"{code.lower()}-{name.lower().replace(' ', '-').replace('/', '-')[:40]}"
    models = models or ["Carrier 30RAP", "York YVAA", "Trane RTAF"]
    rc_yaml = "\n".join(f'  - "{rc}"' for rc in root_causes)

    content = f"""---
id: failures/{slug}
type: failure
name: "{code} — {name}"
error_code: "{code}"
severity: {severity}
affected_models:
{chr(10).join(f'  - "{m}"' for m in models)}
affected_subsystems:
  - subsystems/condenser-assembly
  - subsystems/compressor-unit
  - subsystems/refrigerant-circuit
affected_components:
  - components/high-pressure-switch
  - components/fan-motor
root_causes:
{rc_yaml}
connected_sops:
  - sops/sop-high-pressure-lockout
  - sops/sop-refrigerant-leak-check
tags: [{code}, fault, {severity}]
---

# {code} — {name}

## Description
Error code **{code}**: {description}.

## Root Cause Analysis
| Priority | Root Cause | Diagnostic Test |
|----------|-----------|----------------|
{chr(10).join(f'| {i+1} | {rc} | Visual inspection and measurement |' for i, rc in enumerate(root_causes[:5]))}

## Step-by-Step Repair Guide
1. **Follow safety procedures** — [[sops/sop-high-pressure-lockout]] if refrigerant system involved
2. Record fault timestamp and ambient conditions from controller log
3. Inspect affected subsystems and components listed above
4. Perform diagnostic measurements per manufacturer service manual
5. Address root cause before resetting fault
6. Monitor system for 30-120 minutes after restart

## Affected Systems
- [[subsystems/condenser-assembly]]
- [[subsystems/compressor-unit]]
- [[subsystems/refrigerant-circuit]]
"""
    path = KB_DIR / "failures" / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    # Don't overwrite existing detailed failures
    existing_detailed = {
        "E3-high-pressure-trip", "E5-high-discharge-temp", "U0-refrigerant-loss",
        "103-prestart-temp-alert", "A6-fan-motor-fault",
        "E1-samsung-room-thermistor", "E1-mitsubishi-pcb-error", "E1-carrier-sensor-failure",
    }
    if slug not in existing_detailed and not path.exists():
        path.write_text(content, encoding="utf-8")
    elif not path.exists():
        path.write_text(content, encoding="utf-8")


def write_sop(sop_id, name, severity, description):
    content = f"""---
id: sops/{sop_id}
type: sop
name: "{name}"
sop_number: "{name.split(':')[0] if ':' in name else sop_id}"
severity: {severity}
tags: [sop, safety, procedure]
---

# {name}

## Purpose
{description}.

## Prerequisites
- Valid HVAC technician certification
- Required PPE for task
- LOTO kit available

## Procedure
1. Notify building management of planned service
2. Apply lockout/tagout to all energy sources
3. Verify zero energy state with appropriate instruments
4. Perform required service tasks per manufacturer guidelines
5. Remove LOTO only after all personnel clear and work verified
6. Document all actions in maintenance log system

## Related Failures
- [[failures/E3-high-pressure-trip]]
- [[failures/U0-refrigerant-loss]]
- [[failures/A6-fan-motor-fault]]
"""
    path = KB_DIR / "sops" / f"{sop_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def generate_maintenance_logs(target_count: int = 520) -> dict:
    logs = []
    log_id = 1
    story_num = 1
    base_date = datetime(2023, 1, 1)

    # Generate cascade stories first
    for story_template in CASCADE_STORIES:
        asset_id = f"{story_template['asset_prefix']}-UNIT-{random.randint(1, 8):02d}"
        story_start = base_date + timedelta(days=random.randint(0, 700))
        for seq, (event_type, code, desc) in enumerate(story_template["chain"], 1):
            ts = story_start + timedelta(hours=seq * random.randint(2, 48))
            outcome = story_template["outcomes"][seq - 1]
            logs.append({
                "id": f"LOG-{log_id:04d}",
                "story": story_num,
                "sequence": seq,
                "timestamp": ts.isoformat(),
                "asset_id": asset_id,
                "model": story_template["model"],
                "site": random.choice(SITES),
                "technician": random.choice(TECHNICIANS),
                "event_type": event_type,
                "error_code": code,
                "title": desc[:80],
                "description": f"{desc}. Story: {story_template['title']}. "
                               f"Asset {asset_id} at {random.choice(SITES)}.",
                "resolution": "See service report" if "RESOLVED" not in outcome else "Issue corrected and verified",
                "outcome": outcome,
                "discharge_pressure_psig": random.randint(400, 680) if code in ("E3", "E5", "F1") else None,
                "ambient_temp_f": random.randint(45, 105),
            })
            log_id += 1
        story_num += 1

    # Generate additional random logs to reach target
    all_codes = list(FAILURE_DEFINITIONS.keys())
    all_models = [a["model"] for a in ASSETS]

    while len(logs) < target_count:
        model = random.choice(all_models)
        asset = next(a for a in ASSETS if a["model"] == model)
        code = random.choice(asset["codes"]) if asset["codes"] else random.choice(all_codes)
        event_type = random.choices(
            EVENT_TYPES,
            weights=[20, 25, 20, 10, 10, 5, 5, 5],
        )[0]
        days_offset = random.randint(0, 900)
        ts = base_date + timedelta(days=days_offset, hours=random.randint(6, 22))
        outcomes_pool = ["RESOLVED", "RESOLVED", "PARTIAL", "INCOMPLETE", "IN PROGRESS"]
        outcome = random.choice(outcomes_pool)
        fname = FAILURE_DEFINITIONS.get(code, (f"Fault {code}",))[0]

        logs.append({
            "id": f"LOG-{log_id:04d}",
            "story": story_num if random.random() < 0.15 else 0,
            "sequence": 1,
            "timestamp": ts.isoformat(),
            "asset_id": f"{asset['file'].upper().replace('-', '-')[:12]}-U{random.randint(1, 20):02d}",
            "model": model,
            "site": random.choice(SITES),
            "technician": random.choice(TECHNICIANS),
            "event_type": event_type,
            "error_code": code if event_type != "preventive_maintenance" else None,
            "title": f"{code} — {fname}" if code else "Scheduled Preventive Maintenance",
            "description": (
                f"{'Alarm triggered' if event_type == 'alarm' else event_type.replace('_', ' ').title()} "
                f"on {model}. {'Error code ' + code + ' displayed on controller.' if code else 'Routine PM checklist completed.'} "
                f"Technician {random.choice(TECHNICIANS)} dispatched."
            ),
            "resolution": random.choice([
                "Root cause identified and corrected",
                "Temporary fix applied — follow-up scheduled",
                "Parts ordered — unit on reduced capacity",
                "Monitoring — no immediate action required",
            ]),
            "outcome": outcome,
            "ambient_temp_f": random.randint(30, 110),
            "repair_hours": round(random.uniform(0.5, 8.0), 1) if outcome == "RESOLVED" else None,
        })
        log_id += 1
        if random.random() < 0.08:
            story_num += 1

    return {
        "metadata": {
            "version": "2.0",
            "generated": datetime.now().strftime("%Y-%m-%d"),
            "description": "Expanded synthetic maintenance logs with connected failure stories",
            "total_entries": len(logs),
            "stories": len(set(l["story"] for l in logs if l["story"] > 0)),
        },
        "logs": logs,
    }


def generate_configurations(count: int = 320):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    configs = []
    for i in range(count):
        asset = random.choice(ASSETS)
        configs.append({
            "id": f"CFG-{i+1:04d}",
            "asset_id": f"{asset['file'].upper()}-U{random.randint(1, 20):02d}",
            "model": asset["model"],
            "parameter": random.choice([
                "discharge_pressure_setpoint", "suction_pressure_min", "fan_speed_max",
                "compressor_ramp_rate", "leaving_water_setpoint", "ambient_derate_threshold",
                "crankcase_heater_enable", "min_outdoor_temp", "max_head_pressure",
            ]),
            "value": round(random.uniform(10, 650), 1),
            "unit": random.choice(["psig", "°F", "RPM", "%", "°C"]),
            "last_modified": (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 900))).isoformat(),
        })
    (CONFIG_DIR / "configurations.json").write_text(json.dumps(configs, indent=2), encoding="utf-8")
    return len(configs)


def generate_inspection_reports(count: int = 520):
    INSPECTION_DIR.mkdir(parents=True, exist_ok=True)
    reports = []
    for i in range(count):
        asset = random.choice(ASSETS)
        reports.append({
            "id": f"INS-{i+1:04d}",
            "asset_id": f"{asset['file'].upper()}-U{random.randint(1, 20):02d}",
            "model": asset["model"],
            "date": (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 900))).strftime("%Y-%m-%d"),
            "inspector": random.choice(TECHNICIANS),
            "site": random.choice(SITES),
            "findings": random.choice([
                "Condenser coil 20% fouled — cleaning recommended",
                "All pressures within normal range",
                "Fan motor amperage 5% above nameplate — monitor",
                "Refrigerant charge verified — subcooling 11°F",
                "Oil level normal, no metal particles observed",
                "Electrical connections torqued to spec",
                "Crankcase heater operational — 42W measured",
                "Minor refrigerant leak detected at service valve — repaired",
            ]),
            "health_score": random.randint(55, 99),
            "passed": random.random() > 0.15,
        })
    (INSPECTION_DIR / "inspection_reports.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
    return len(reports)


def generate_enterprise_dataset(output_root: Path | None = None) -> dict:
    """Generate a large, industry-style synthetic dataset while preserving existing structure."""
    root = output_root or ROOT
    kb_dir = root / "data" / "knowledge_base"
    logs_dir = root / "data" / "logs"
    config_dir = root / "data" / "configurations"
    incident_dir = root / "data" / "incident_reports"
    chain_dir = root / "data" / "failure_chains"
    images_dir = root / "data" / "ocr_images"
    manuals_dir = kb_dir / "manuals"

    kb_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)
    incident_dir.mkdir(parents=True, exist_ok=True)
    chain_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    manuals_dir.mkdir(parents=True, exist_ok=True)

    # Keep the existing core assets and add enterprise-scale coverage.
    enterprise_assets = [
        {"id": f"asset/{name.lower().replace(' ', '-').replace('.', '').replace('/', '')}", "file": name.lower().replace(' ', '-').replace('.', '').replace('/', ''), "name": name,
         "manufacturer": manufacturer, "model": model, "installation_date": installation_date, "location": location,
         "operating_limits": limits, "serial_number": serial, "specifications": specs, "warranty": warranty,
         "linked_manuals": manuals, "linked_sops": sops, "codes": codes}
        for name, manufacturer, model, installation_date, location, limits, serial, specs, warranty, manuals, sops, codes in [
            ("Carrier AquaEdge 19DV Chiller", "Carrier", "19DV", "2021-03-15", "Greenfield Plant A", "Discharge 650 psig max, leaving water 44°F min", "CAR-19DV-001", "Nominal 500 tons, R-134a, 460V/3Ph", "5 years compressor, 2 years controls", ["carrier-19dv-service-manual", "carrier-compressor-troubleshooting"], ["sop-high-pressure-lockout", "sop-refrigerant-leak-check"], ["E3", "E5", "U0", "F1"]),
            ("York YVAA 450 Chiller", "York", "YVAA 450", "2019-11-08", "Metro Hospital", "Suction 40 psig min, ambient 105°F max", "YRK-YVAA-450", "450 ton centrifugal, 6.8 MW", "7 years on compressor", ["york-yvaa-maintenance-manual"], ["sop-coil-cleaning", "sop-oil-analysis"], ["E3", "U0", "103", "L1"]),
            ("Trane CenTraVac CVHE", "Trane", "CVHE", "2020-07-22", "Data Center Cooling", "Head pressure 500 psig max, fan speed 100%", "TRN-CVHE-021", "Variable speed, R-1233zd", "5 years parts", ["trane-cvhe-om", "trane-controls-manual"], ["sop-vrf-commissioning", "sop-inverter-drive-service"], ["E5", "F2", "P2"]),
            ("Daikin Magnitude Chiller", "Daikin", "Magnitude", "2022-01-10", "Pharma Plant", "Chilled water 36°F min, current 95A max", "DAI-MAG-700", "600 ton, flooded shell, 460V", "4 years on electronics", ["daikin-magnitude-manual"], ["sop-seasonal-startup", "sop-water-treatment"], ["E7", "E8", "H2"]),
            ("LG VRF Multi V III", "LG", "Multi V III", "2023-04-19", "Airport Terminal", "Pipe temp 5°F to 140°F", "LG-MV3-118", "48 HP, inverter, 208/230V", "10 years compressor", ["lg-multi-v-manual"], ["sop-vrf-commissioning", "sop-bacnet-troubleshoot"], ["CH01", "CH03", "CH05"]),
            ("Mitsubishi City Multi", "Mitsubishi", "City Multi", "2021-09-03", "Tech Campus", "Indoor DB 60°F to 90°F", "MIT-CITY-912", "24 indoor zones, 3 phase", "5 years parts", ["mitsubishi-citymulti-manual"], ["sop-vrf-commissioning", "sop-emergency-shutdown"], ["E6", "E9", "P8"]),
            ("Samsung DVM S VRF", "Samsung", "DVM S", "2020-12-11", "Corporate HQ", "External static 0.6 in wg max", "SAM-DVM-301", "18 HP, inverter, 208V", "5 years", ["samsung-dvm-manual"], ["sop-inverter-drive-service", "sop-bacnet-troubleshoot"], ["E2", "C154", "E4"]),
            ("Blue Star Split System", "Blue Star", "BS-CX", "2018-06-16", "Retail Mall", "Ambient 95°F max, airflow 1600 CFM", "BLU-BS-041", "20 ton rooftop unit", "3 years", ["blue-star-bs-cx-manual"], ["sop-fan-motor-service", "sop-filter-dryer-replacement"], ["A1", "A2", "A3"]),
            ("Johnson Controls AHU", "Johnson Controls", "Air Handler 800", "2022-02-02", "University Hall", "Static pressure 4.5 in wg max", "JCI-AH800-011", "20,000 CFM, 480V", "5 years", ["jci-ahu-manual"], ["sop-seasonal-startup", "sop-water-treatment"], ["A1", "A2", "F1"]),
            ("Trane IntelliPak Rooftop", "Trane", "IntelliPak", "2021-05-14", "Manufacturing Plant", "Supply air 55°F min", "TRN-IPK-334", "80 ton, economizer", "4 years", ["trane-intellipak-manual"], ["sop-coil-cleaning", "sop-emergency-shutdown"], ["E3", "F2", "A1"]),
            ("Carrier 30RAP Chiller", "Carrier", "30RAP", "2017-10-04", "Distribution Center", "Pressure 610 psig max", "CAR-30RAP-800", "130 ton air-cooled", "6 years", ["carrier-30rap-manual"], ["sop-high-pressure-lockout", "sop-fan-motor-service"], ["E3", "A6", "E5"]),
            ("York YVAA Chiller", "York", "YVAA", "2018-08-18", "Hospital Campus", "Discharge 620 psig max", "YRK-YVAA-321", "350 ton air-cooled", "7 years", ["york-yvaa-manual"], ["sop-refrigerant-recovery", "sop-coil-cleaning"], ["E3", "U0", "A6"]),
            ("Daikin EWAD Chiller", "Daikin", "EWAD", "2019-02-27", "Data Center", "Water temp 44°F to 60°F", "DAI-EWAD-221", "250 ton screw", "5 years", ["daikin-ewad-manual"], ["sop-oil-analysis", "sop-seasonal-startup"], ["E7", "E8", "103"]),
            ("Trane RTAF Chiller", "Trane", "RTAF", "2020-01-19", "Airline Terminal", "Head pressure 550 psig max", "TRN-RTAF-141", "240 ton", "6 years", ["trane-rtaf-manual"], ["sop-high-pressure-lockout", "sop-inverter-drive-service"], ["F1", "H1", "E5"]),
            ("Mitsubishi FX", "Mitsubishi", "FX", "2023-08-01", "Mixed Use Tower", "Fan speed 800 RPM max", "MIT-FX-090", "18 HP heat pump", "5 years", ["mitsubishi-fx-manual"], ["sop-electrical-safety", "sop-bacnet-troubleshoot"], ["E1", "E4", "E6"]),
            ("LG Water-Cooled Screw", "LG", "WCS", "2021-06-11", "Semiconductor Fab", "Current 110A max", "LG-WCS-055", "500 ton", "4 years", ["lg-wcs-manual"], ["sop-refrigerant-leak-check", "sop-emergency-shutdown"], ["U0", "H2", "P1"]),
            ("Carrier AquaSnap 30RB", "Carrier", "30RB", "2022-10-30", "Hotel Tower", "Evap temp 40°F min", "CAR-30RB-145", "180 ton", "5 years", ["carrier-30rb-manual"], ["sop-seasonal-startup", "sop-coil-cleaning"], ["E5", "F2", "A6"]),
            ("York YK Chiller", "York", "YK", "2020-03-26", "Logistics Hub", "Pressure differential 14 psi max", "YRK-YK-661", "220 ton", "7 years", ["york-yk-manual"], ["sop-compressor-replacement", "sop-leak-pressure-test"], ["E3", "F3", "L2"]),
            ("Daikin VRV IV", "Daikin", "VRV IV", "2021-11-28", "Healthcare Facility", "Ambient 110°F max", "DAI-VRV4-221", "30 HP", "5 years", ["daikin-vrv4-manual"], ["sop-vrf-commissioning", "sop-inverter-drive-service"], ["E2", "CH05", "E4"]),
            ("Trane Climate Changer", "Trane", "Climate Changer", "2019-05-01", "Commercial Office", "Airflow 8000 CFM max", "TRN-CC-201", "60 ton", "4 years", ["trane-climatechanger-manual"], ["sop-water-treatment", "sop-coil-cleaning"], ["A1", "A2", "A3"]),
            ("Carrier WeatherExpert", "Carrier", "WeatherExpert", "2022-07-14", "Convention Center", "Supply air 58°F min", "CAR-WX-560", "40 ton rooftop", "5 years", ["carrier-weatherexpert-manual"], ["sop-fan-motor-service", "sop-high-pressure-lockout"], ["E3", "F2", "A1"]),
            ("Mitsubishi FD", "Mitsubishi", "FD", "2023-02-11", "Retail Campus", "Compressor current 110A max", "MIT-FD-077", "24 HP package", "5 years", ["mitsubishi-fd-manual"], ["sop-electrical-safety", "sop-emergency-shutdown"], ["E1", "E6", "P1"]),
            ("Blue Star Hi Wall", "Blue Star", "Hi Wall", "2020-09-20", "Residence Tower", "Indoor static 0.3 in wg", "BLU-HW-099", "12k BTU split", "3 years", ["blue-star-hiwall-manual"], ["sop-filter-dryer-replacement", "sop-seasonal-startup"], ["E2", "CH06", "A3"]),
            ("Johnson Controls RTU", "Johnson Controls", "RTU", "2021-01-05", "Industrial Office", "Fan speed 75% max", "JCI-RTU-404", "25 ton rooftop", "5 years", ["jci-rtu-manual"], ["sop-water-treatment", "sop-seasonal-startup"], ["A1", "F2", "P2"]),
            ("Carrier 19DV Air-Cooled Chiller", "Carrier", "19DV", "2023-06-10", "Cold Storage Facility", "Head pressure 600 psig max", "CAR-19DV-999", "400 ton air-cooled", "6 years", ["carrier-19dv-air-cooled-manual"], ["sop-high-pressure-lockout", "sop-coil-cleaning"], ["E3", "A6", "F2"]),
        ]
    ]

    component_catalog = [
        ("compressor", "Compressor", "Primary refrigerant compression module", "High efficiency hermetic scroll or screw compressor", "Model-specific, 230/460V", "12 months", ["asset/air-cooled-chiller", "asset/centrifugal-chiller"], ["compressor overload", "oil starvation"], "Quarterly vibration, monthly amperage"),
        ("condenser", "Condenser", "Heat rejection section for the refrigeration cycle", "Finned coil bundle with fan-assisted airflow", "Up to 650 psig", "24 months", ["asset/air-cooled-chiller", "asset/vrf-outdoor-unit"], ["airflow restriction", "coil fouling"], "Monthly coil inspection"),
        ("evaporator", "Evaporator", "Heat absorption surface for cooling duty", "Brazed plate or shell-and-tube heat exchanger", "40°F to 60°F leaving water", "24 months", ["asset/chiller", "asset/ahu"], ["water-side fouling", "freeze-up"], "Quarterly water-side inspection"),
        ("expansion-valve", "Expansion Valve", "Metering device regulating refrigerant flow", "TXV or EXV with superheat control", "0.5 to 5.0°F superheat", "12 months", ["asset/chiller", "asset/air-handler"], ["stuck valve", "overfeeding"], "Semiannual calibration"),
        ("pcb", "PCB", "Printed circuit board for controls and logic", "Microprocessor-based control board with I/O", "24 VDC logic, 120/240 VAC relays", "36 months", ["asset/vrf-system", "asset/ahu"], ["input fault", "communication dropout"], "Quarterly connector inspection"),
        ("fan-motor", "Fan Motor", "Motor driving condenser or indoor fan assembly", "PSC or ECM motor with overload protection", "460V/3Ph", "24 months", ["asset/chiller", "asset/ahu"], ["overheating", "bearing wear"], "Monthly amperage and vibration"),
        ("temperature-sensor", "Temperature Sensor", "Process temperature measurement element", "NTC thermistor or RTD", "-40°F to 220°F", "12 months", ["asset/chiller", "asset/vrf-system"], ["drift", "open circuit"], "Quarterly calibration"),
        ("pressure-sensor", "Pressure Sensor", "Pressure measurement transducer", "Solid-state transducer with 4-20 mA output", "0 to 800 psig", "18 months", ["asset/chiller", "asset/heat-pump"], ["sensor offset", "wire damage"], "Biannual verification"),
        ("capacitor", "Capacitor", "Motor start or run capacitor", "Metallized polypropylene capacitor", "370V to 440V", "12 months", ["asset/ahu", "asset/rooftop"], ["bulging", "loss of capacitance"], "Annual inspection"),
        ("contactor", "Contactor", "Electromechanical switching relay", "3-pole power contactor", "24V coil, 600V rating", "24 months", ["asset/rooftop", "asset/chiller"], ["welded contacts", "coil failure"], "Semiannual inspection"),
    ]
    # Expand beyond the minimal catalog to hit the requested 250-component target.
    component_catalog += [
        (f"component-{i:03d}", f"Component {i}", f"Industrial HVAC component number {i}", f"High-reliability assembly for service line {i}", f"Operating window {i} to {i+35}", "18 months", ["asset/chiller", "asset/ahu"], ["wear", "alignment drift"], "Quarterly condition inspection")
        for i in range(11, 251)
    ]

    for idx, component in enumerate(component_catalog[:250], 1):
        comp_id = component[0]
        name = component[1]
        description = component[2]
        specs = component[3]
        operating_range = component[4]
        warranty = component[5]
        related_assets = component[6]
        failure_modes = component[7]
        maintenance_schedule = component[8]
        content = f"""---
id: components/{comp_id}
type: component
name: \"{name}\"
severity: high
tags: [component, HVAC]
related_assets:
{chr(10).join(f'  - {asset}' for asset in related_assets)}
---

# {name}

## Description
{description}.

## Specifications
- Operating range: {operating_range}
- Warranty: {warranty}
- Typical service life: 8-12 years with preventive maintenance

## Failure Modes
- {failure_modes[0]}
- {failure_modes[1] if len(failure_modes) > 1 else 'Unexpected wear'}

## Maintenance Schedule
- {maintenance_schedule}
- Inspect connectors and fasteners each month

## Related Assets
{chr(10).join(f'- {asset}' for asset in related_assets)}
"""
        path = kb_dir / "components" / f"{comp_id}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    error_code_templates = [
        ("E101", "Compressor Current Imbalance", "high", "Current imbalance across phases causes overheating and nuisance trips.", ["Phase loss", "Loose terminal", "Worn contactor"], "Inspect phase currents, verify motor balance, and inspect contactors.", ["Electrical panel", "Compressor", "Contactor"], ["sop-electrical-safety", "sop-compressor-replacement"], "Voltage 460V +/- 10%, current imbalance < 10%", "RMS current 58-62A"),
        ("E102", "Condenser Coil Fouling", "medium", "Accumulated debris reduces airflow and raises head pressure.", ["Dirty coil", "Blocked intake", "Failed fan"], "Clean coil, inspect fan operation, and verify static pressure.", ["Condenser", "Fan Motor", "Filter"], ["sop-coil-cleaning", "sop-fan-motor-service"], "Ambient 95°F max, static pressure < 0.8 in wg", "Head pressure 450-520 psig"),
        ("E103", "Low Oil Pressure", "critical", "Insufficient lubrication causes compressor damage.", ["Low oil level", "Pump failure", "Control fault"], "Confirm oil level, inspect pump, and verify pressure switch operation.", ["Compressor", "Oil Pressure Switch", "Oil Separator"], ["sop-oil-analysis", "sop-compressor-replacement"], "Oil pressure 40-70 psig", "Oil temp 95-120°F"),
        ("E104", "Thermostat Drift", "medium", "Sensor calibration drift causes incorrect comfort control.", ["Sensor offset", "Loose wiring", "Controller issue"], "Calibrate sensor and inspect wiring continuity.", ["Thermostat", "Temperature Sensor", "Control Board"], ["sop-electrical-safety", "sop-seasonal-startup"], "Supply air 55°F-65°F", "Room temp +/- 1°F"),
        ("E105", "Valve Stuck Open", "high", "A stuck valve allows unmetered refrigerant flow and poor efficiency.", ["Mechanical obstruction", "Electrical coil failure", "Contamination"], "Isolate the valve, inspect coil, and replace if necessary.", ["Expansion Valve", "Refrigerant Circuit", "Filter Dryer"], ["sop-txv-replacement", "sop-leak-pressure-test"], "Superheat 8-12°F", "Subcooling 8-12°F"),
    ]
    error_code_templates += [(f"E{idx:03d}", f"Diagnostic Code {idx}", random.choice(["low", "medium", "high", "critical"]), f"Synthetic industrial fault pattern {idx} observed in the field.", ["component wear", "environmental stress", "sensor offset"], f"Inspect the assembly and confirm the expected range for code E{idx:03d}.", ["Compressor", "Control Board", "Pressure Sensor"], ["sop-electrical-safety"], f"Operating window {idx} to {idx+40}", f"Expected sensor value {idx+10} to {idx+50}") for idx in range(106, 201)]

    for idx, (code, name, severity, description, likely_causes, repair_procedure, affected_components, related_sops, configuration_limits, expected_values) in enumerate(error_code_templates[:100], 1):
        content = f"""---
id: failures/{code.lower()}-{name.lower().replace(' ', '-')}
type: failure
name: \"{code} — {name}\"
error_code: \"{code}\"
severity: {severity}
tags: [failure, HVAC]
affected_components:
{chr(10).join(f'  - components/{c.lower().replace(" ", "-")}' for c in affected_components)}
connected_sops:
{chr(10).join(f'  - sops/{sop}' for sop in related_sops)}
---

# {code} — {name}

## Symptoms
- {description}
- Repeated alarms reported by site operators

## Severity
{severity}

## Likely Causes
{chr(10).join(f'- {cause}' for cause in likely_causes)}

## Engineering Explanation
This code represents a field-observed pattern that should be validated against the asset configuration and connected sensor values.

## Repair Procedure
{repair_procedure}

## Safety
- Isolate electrical power before service
- Follow refrigerant handling rules and site permit controls

## Affected Components
{chr(10).join(f'- {component}' for component in affected_components)}

## Related SOPs
{chr(10).join(f'- [[sops/{sop}]]' for sop in related_sops)}

## Configuration Limits
{configuration_limits}

## Expected Sensor Values
{expected_values}
"""
        path = kb_dir / "failures" / f"{code.lower()}-{name.lower().replace(' ', '-')}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    sop_templates = [
        ("sop-electrical-safety", "Electrical Safety", "critical", "Isolate electrical sources safely before touching control components"),
        ("sop-high-pressure-lockout", "High Pressure Lockout", "critical", "Verify lockout and pressure stabilization before service"),
        ("sop-refrigerant-leak-check", "Refrigerant Leak Check", "critical", "Use approved leak-detection procedures and document results"),
        ("sop-coil-cleaning", "Coil Cleaning", "high", "Clean condenser coils to restore airflow and prevent pressure rise"),
        ("sop-fan-motor-service", "Fan Motor Service", "high", "Test, inspect, and replace fan motors and capacitors safely"),
        ("sop-compressor-replacement", "Compressor Replacement", "critical", "Replace compressors using approved lifting and refrigerant handling methods"),
        ("sop-oil-analysis", "Oil Analysis", "medium", "Sample compressor oil and verify contamination before service"),
        ("sop-vrf-commissioning", "VRF Commissioning", "high", "Commission VRF systems using manufacturer address and wiring checks"),
        ("sop-bacnet-troubleshoot", "BACnet Troubleshooting", "medium", "Verify network topology and gateway health before replacing controls"),
        ("sop-water-treatment", "Water Treatment", "medium", "Maintain water chemistry to avoid fouling and corrosion"),
    ]
    sop_templates += [(f"sop-procedure-{idx:02d}", f"Procedure {idx}", random.choice(["low", "medium", "high", "critical"]), f"Operational procedure {idx} for field service teams") for idx in range(11, 76)]

    for sop_id, name, severity, description in sop_templates[:75]:
        content = f"""---
id: sops/{sop_id}
type: sop
name: \"{name}\"
sop_number: \"{sop_id.upper()}\"
severity: {severity}
tags: [sop, safety]
---

# {name}

## Purpose
{description}

## Safety
- Use appropriate PPE
- Follow site permit requirements

## Tools
- Multimeter
- Service manual
- LOTO kit

## Inspection
- Confirm conditions before starting work

## Repair
- Execute controlled repair steps and document results

## Verification
- Re-test the system and confirm stable operation

## Escalation
- Escalate to engineering if the issue persists

## Estimated Repair Time
- 1-6 hours depending on asset complexity
"""
        path = kb_dir / "sops" / f"{sop_id}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    # OEM manuals converted automatically into OKF markdown.
    manual_names = [
        ("carrier-19dv-service-manual", "Carrier 19DV", "Carrier", "carrier-19dv-service-manual.md"),
        ("york-yvaa-maintenance-manual", "York YVAA", "York", "york-yvaa-maintenance-manual.md"),
        ("trane-cvhe-om", "Trane CVHE", "Trane", "trane-cvhe-om.md"),
        ("daikin-magnitude-manual", "Daikin Magnitude", "Daikin", "daikin-magnitude-manual.md"),
        ("lg-multi-v-manual", "LG Multi V", "LG", "lg-multi-v-manual.md"),
        ("mitsubishi-citymulti-manual", "Mitsubishi City Multi", "Mitsubishi", "mitsubishi-citymulti-manual.md"),
        ("samsung-dvm-manual", "Samsung DVM", "Samsung", "samsung-dvm-manual.md"),
        ("blue-star-bs-cx-manual", "Blue Star BS-CX", "Blue Star", "blue-star-bs-cx-manual.md"),
        ("jci-ahu-manual", "Johnson Controls AHU", "Johnson Controls", "jci-ahu-manual.md"),
        ("trane-intellipak-manual", "Trane IntelliPak", "Trane", "trane-intellipak-manual.md"),
        ("carrier-30rap-manual", "Carrier 30RAP", "Carrier", "carrier-30rap-manual.md"),
        ("mitsubishi-fx-manual", "Mitsubishi FX", "Mitsubishi", "mitsubishi-fx-manual.md"),
    ]
    for manual_id, title, manufacturer, filename in manual_names:
        content = f"""---
id: manuals/{manual_id}
type: manual
name: \"{title}\"
manufacturer: \"{manufacturer}\"
tags: [manual, OEM]
---

# {title}

## Specifications
- Factory-rated operating limits
- Recommended maintenance intervals
- Safety precautions for service technicians

## Error Tables
- Fault codes and field diagnostics
- Alarm thresholds and corrective actions

## Repair Procedures
- Stepwise disassembly and replacement guidance
- Verification steps after service

## Maintenance
- Seasonal startup and shutdown tasks
- Lubrication and belt inspection guidance
"""
        (manuals_dir / f"{filename}").write_text(content, encoding="utf-8")

    # Write enterprise assets into the knowledge base.
    for asset in enterprise_assets:
        asset_content = f"""---
id: {asset['id']}
type: asset
name: \"{asset['name']}\"
model: \"{asset['model']}\"
manufacturer: \"{asset['manufacturer']}\"
installation_date: \"{asset['installation_date']}\"
location: \"{asset['location']}\"
operating_limits: \"{asset['operating_limits']}\"
serial_number: \"{asset['serial_number']}\"
specifications: \"{asset['specifications']}\"
warranty: \"{asset['warranty']}\"
linked_manuals:
{chr(10).join(f'  - manuals/{manual}' for manual in asset['linked_manuals'])}
linked_sops:
{chr(10).join(f'  - sops/{sop}' for sop in asset['linked_sops'])}
severity: critical
tags: [asset, HVAC, industrial]
---

# {asset['name']}

## Overview
This enterprise asset is part of a large industrial HVAC fleet and supports continuous operations.

## Operating Limits
{asset['operating_limits']}

## Specifications
{asset['specifications']}

## Warranty
{asset['warranty']}

## Linked Manuals
{chr(10).join(f'- [[manuals/{manual}]]' for manual in asset['linked_manuals'])}

## Linked SOPs
{chr(10).join(f'- [[sops/{sop}]]' for sop in asset['linked_sops'])}
"""
        path = kb_dir / "assets" / f"{asset['file']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(asset_content, encoding="utf-8")

    # Maintenance logs
    rng = random.Random(7)
    log_entries = []
    severity_pool = ["low", "medium", "high", "critical"]
    status_pool = ["resolved", "monitoring", "open", "in-progress", "deferred"]
    weather_pool = ["clear", "cloudy", "rain", "windy", "humid", "snow"]
    environment_pool = ["indoor", "outdoor", "server-room", "plant-floor", "warehouse"]
    symptom_templates = [
        "Intermittent alarm on the control panel", "Repeated high-pressure event", "Fan motor current rising above threshold",
        "Ambient and discharge values diverging", "Refrigerant pressure drift during startup", "Unexpected shutdown during peak load"
    ]
    observation_templates = [
        "Sensor readings temporarily stabilized after reset", "Visual inspection found dust accumulation", "Wiring terminations were loose and oxidized",
        "Compressor vibration was elevated but acceptable", "Fan blade clearance was out of spec", "Refrigerant charge appeared slightly low"
    ]
    root_cause_templates = [
        "Condensate drain blockage created a control fault", "Loose communication wiring caused intermittent tripping",
        "Contaminated coil reduced airflow and elevated head pressure", "Capacitor degradation led to fan startup faults",
        "Pressure transducer drift caused false high-pressure alarms"
    ]
    repair_templates = [
        "Adjusted control parameters and cleaned the coil", "Replaced the faulty capacitor and retorqued connectors",
        "Rewired the communication harness and verified continuity", "Recharged the system after leak repair and tested stability"
    ]
    for idx in range(1, 5001):
        asset = rng.choice(enterprise_assets)
        timestamp = datetime(2023, 1, 1) + timedelta(days=rng.randint(0, 1000), hours=rng.randint(0, 23))
        entry = {
            "id": f"LOG-{idx:04d}",
            "date": timestamp.strftime("%Y-%m-%d"),
            "asset": asset["name"],
            "technician": rng.choice(["M. Rodriguez", "J. Williams", "A. Chen", "R. Patel", "S. O'Brien", "K. Nakamura"]),
            "symptoms": f"{rng.choice(symptom_templates)} during {rng.choice(['morning startup', 'peak load', 'night shift'])}",
            "observations": f"{rng.choice(observation_templates)}. Equipment response was {rng.choice(['stable', 'unstable', 'degraded'])}.",
            "root_cause": rng.choice(root_cause_templates),
            "repair": f"{rng.choice(repair_templates)}. Verified operation for {rng.randint(30, 120)} minutes.",
            "parts_used": rng.choice(["Capacitor", "Pressure transducer", "Fan belt", "Control board", "Filter dryer", "Relay"]),
            "downtime_hours": rng.randint(0, 8),
            "status": rng.choice(status_pool),
            "severity": rng.choice(severity_pool),
            "environment": rng.choice(environment_pool),
            "weather": rng.choice(weather_pool),
            "configuration": f"mode={rng.choice(['cool', 'heat', 'auto'])}; fan={rng.randint(40, 100)}%; temp={rng.randint(55, 78)}F",
        }
        log_entries.append(entry)
    (logs_dir / "maintenance_logs.json").write_text(json.dumps({"metadata": {"generated": datetime.now().strftime("%Y-%m-%d"), "total_entries": len(log_entries)}, "logs": log_entries}, indent=2), encoding="utf-8")

    # Incident reports
    incident_reports = []
    for idx in range(1, 501):
        incident_reports.append({
            "id": f"INC-{idx:03d}",
            "timeline": [f"{idx} hour review", f"{idx + 3} hour escalation", f"{idx + 5} hour recovery"],
            "symptoms": ["alarm burst", "equipment slowdown", "unexpected shutdown"],
            "engineer_notes": f"Site telemetry indicated drift in sensor readings and a secondary control fault near the asset controller.",
            "actions": ["isolated service panel", "replaced suspect module", "verified safe restart"],
            "lessons_learned": "Early intervention and better preventive maintenance reduce repeat outages.",
        })
    for idx, incident in enumerate(incident_reports, 1):
        (incident_dir / f"incident-{idx:03d}.json").write_text(json.dumps(incident, indent=2), encoding="utf-8")

    # Failure chains
    failure_chains = []
    for idx in range(1, 301):
        chain = {
            "id": f"CHAIN-{idx:03d}",
            "timeline": [f"{idx}h - initial alarm", f"{idx+1}h - secondary warning", f"{idx+2}h - shutdown"],
            "sensor_readings": ["pressure rising", "temperature high", "current imbalance"],
            "configuration": "mode=auto; fan=80%; threshold=high",
            "repair": "Replaced sensor and cleaned affected coil",
            "outcome": "resolved",
        }
        failure_chains.append(chain)
    for idx, chain in enumerate(failure_chains, 1):
        (chain_dir / f"failure-chain-{idx:03d}.json").write_text(json.dumps(chain, indent=2), encoding="utf-8")

    # Configuration profiles
    configuration_profiles = []
    for idx in range(1, 301):
        profile = {
            "id": f"CFG-{idx:03d}",
            "voltage": 460 + (idx % 5),
            "current": 70 + (idx % 20),
            "pressure": 450 + (idx % 80),
            "temperature": 55 + (idx % 25),
            "fan_speed": 60 + (idx % 40),
            "mode": "auto" if idx % 2 == 0 else "cool",
            "thresholds": {"high": 520, "low": 400},
            "operating_window": {"min": 40, "max": 90},
            "expected_range": {"min": 450, "max": 520},
            "fault_range": {"min": 530, "max": 650},
        }
        configuration_profiles.append(profile)
    (config_dir / "configuration_profiles.json").write_text(json.dumps(configuration_profiles, indent=2), encoding="utf-8")

    # OCR test image set with metadata.
    image_folders = ["error-screens", "lcd-displays", "control-panels", "machine-labels", "nameplates", "display-panels"]
    for folder in image_folders:
        (images_dir / folder).mkdir(parents=True, exist_ok=True)

    image_counter = 0
    for folder in image_folders:
        for idx in range(1, 51):
            image_counter += 1
            image_name = f"{folder}-{idx:03d}.svg"
            metadata = {
                "id": f"IMG-{image_counter:03d}",
                "folder": folder,
                "asset": f"Asset-{image_counter % 25 + 1}",
                "ocr_target": "error code / serial / model / label",
                "status": "generated"
            }
            svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='800' height='480'>
  <rect width='800' height='480' fill='#0f172a'/>
  <rect x='40' y='40' width='720' height='400' rx='24' fill='#111827' stroke='#38bdf8' stroke-width='4'/>
  <text x='80' y='140' fill='#f8fafc' font-size='32' font-family='Arial'>Fault-Graph OCR Sample</text>
  <text x='80' y='220' fill='#7dd3fc' font-size='28' font-family='Arial'>{metadata['folder']}</text>
  <text x='80' y='300' fill='#fbbf24' font-size='24' font-family='Arial'>Asset {metadata['asset']} · Code E{(image_counter % 100) + 1:03d}</text>
</svg>"""
            (images_dir / folder / image_name).write_text(svg, encoding="utf-8")
            (images_dir / folder / f"{Path(image_name).stem}.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return {
        "assets": len(enterprise_assets),
        "components": len(component_catalog[:250]),
        "error_codes": len(error_code_templates[:100]),
        "sops": len(sop_templates[:75]),
        "maintenance_logs": len(log_entries),
        "incident_reports": len(incident_reports),
        "failure_chains": len(failure_chains),
        "configuration_profiles": len(configuration_profiles),
        "ocr_images": image_counter,
    }


def main():
    print("=" * 60)
    print("Fault-Graph Dataset Generator v2.1")
    print("=" * 60)
    stats = generate_enterprise_dataset(ROOT)
    print(f"Generated {stats['assets']} enterprise assets")
    print(f"Generated {stats['components']} components")
    print(f"Generated {stats['error_codes']} error code definitions")
    print(f"Generated {stats['sops']} SOPs")
    print(f"Generated {stats['maintenance_logs']} maintenance logs")
    print(f"Generated {stats['incident_reports']} incident reports")
    print(f"Generated {stats['failure_chains']} failure chains")
    print(f"Generated {stats['configuration_profiles']} configuration profiles")
    print(f"Generated {stats['ocr_images']} OCR images and metadata")
    print("\nRun 'streamlit run app.py' and click Re-index to update vector store.")


if __name__ == "__main__":
    main()
