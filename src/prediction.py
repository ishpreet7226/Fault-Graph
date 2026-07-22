"""
prediction.py — Rule-based failure prediction for proactive maintenance.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


LOGS_PATH = Path(__file__).parent.parent / "data" / "logs" / "maintenance_logs.json"

# Cost estimates per error code (INR downtime cost)
DOWNTIME_COST = {
    "E3": 28000, "E5": 35000, "U0": 45000, "103": 12000, "A6": 18000,
    "F1": 85000, "F2": 15000, "F3": 95000, "L1": 40000, "E1": 8000,
}
DEFAULT_COST = 22000

# Hours to failure estimate by severity pattern
FAILURE_HOURS = {
    "critical": (12, 72),
    "high": (24, 120),
    "medium": (72, 336),
    "low": (168, 720),
}


def _load_logs() -> list:
    if not LOGS_PATH.exists():
        return []
    with open(LOGS_PATH) as f:
        return json.load(f).get("logs", [])


def compute_failure_prediction(
    error_code: Optional[str],
    model: Optional[str],
    severity: str = "medium",
    asset_id: Optional[str] = None,
) -> dict:
    """
    Rule-based failure prediction using maintenance log history.
    Returns risk score, time-to-failure estimate, downtime, and cost.
    """
    logs = _load_logs()
    now = datetime.now()

    risk_score = 35.0
    factors = []

    if not error_code:
        return {
            "risk_score": 0,
            "risk_level": "unknown",
            "failure_in_hours": None,
            "estimated_downtime_hours": 0,
            "estimated_cost_inr": 0,
            "factors": ["No error code — cannot predict"],
            "recommendation": "Upload panel image or enter error code for prediction",
        }

    ec = error_code.upper()

    # Factor 1: Recent repeat failures for this code
    recent_logs = [
        l for l in logs
        if l.get("error_code") == ec
        and l.get("timestamp")
        and datetime.fromisoformat(l["timestamp"]) > now - timedelta(days=90)
    ]
    if len(recent_logs) >= 5:
        risk_score += 25
        factors.append(f"{len(recent_logs)} occurrences of {ec} in last 90 days")
    elif len(recent_logs) >= 2:
        risk_score += 15
        factors.append(f"{len(recent_logs)} recent {ec} events detected")

    # Factor 2: Unresolved outcomes
    unresolved = [l for l in recent_logs if "RESOLVED" not in l.get("outcome", "")]
    if unresolved:
        risk_score += 20
        factors.append(f"{len(unresolved)} unresolved {ec} incidents")

    # Factor 3: Same model history
    if model:
        model_logs = [l for l in recent_logs if l.get("model") == model]
        if len(model_logs) >= 3:
            risk_score += 12
            factors.append(f"Repeated {ec} on {model} fleet")

    # Factor 4: Cascade-prone codes
    cascade_codes = {"E3", "A6", "U0", "103", "F1", "E5"}
    if ec in cascade_codes:
        risk_score += 10
        factors.append(f"{ec} has known cascade failure risk")

    # Factor 5: Severity boost
    sev_boost = {"critical": 15, "high": 10, "medium": 5, "low": 0}
    risk_score += sev_boost.get(severity.lower(), 5)

    risk_score = min(round(risk_score, 1), 95.0)

    # Time to failure
    h_min, h_max = FAILURE_HOURS.get(severity.lower(), (48, 168))
    if risk_score >= 80:
        failure_hours = h_min
    elif risk_score >= 60:
        failure_hours = (h_min + h_max) // 2
    else:
        failure_hours = h_max

    # Downtime estimate
    repair_hours = {
        "E3": 2.0, "E5": 3.5, "U0": 6.0, "103": 1.0, "A6": 2.0,
        "F1": 8.0, "F2": 2.0, "F3": 10.0, "L1": 5.0,
    }.get(ec, 3.0)

    cost = DOWNTIME_COST.get(ec, DEFAULT_COST)
    if risk_score >= 75:
        cost = int(cost * 1.3)

    risk_level = "critical" if risk_score >= 75 else "high" if risk_score >= 55 else "medium" if risk_score >= 35 else "low"

    recommendations = {
        "critical": f"Immediate service required — {ec} poses cascade failure risk within ~{failure_hours}h",
        "high": f"Schedule service within 24h — estimated failure in ~{failure_hours}h if unresolved",
        "medium": f"Monitor closely — plan maintenance within 1 week",
        "low": f"Low immediate risk — include in next scheduled PM",
    }

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "failure_in_hours": failure_hours,
        "failure_in_label": f"~{failure_hours} hours" if failure_hours < 168 else f"~{failure_hours // 24} days",
        "estimated_downtime_hours": repair_hours,
        "estimated_cost_inr": cost,
        "factors": factors or ["Baseline risk for error code category"],
        "recommendation": recommendations[risk_level],
    }
