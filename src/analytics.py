"""
analytics.py — Dashboard analytics computed from maintenance logs and KB.
"""

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).parent.parent
LOGS_PATH = ROOT / "data" / "logs" / "maintenance_logs.json"
KB_DIR = ROOT / "data" / "knowledge_base"
INSPECTION_PATH = ROOT / "data" / "inspection_reports" / "inspection_reports.json"


def _load_logs() -> list:
    if not LOGS_PATH.exists():
        return []
    with open(LOGS_PATH) as f:
        return json.load(f).get("logs", [])


def _load_inspections() -> list:
    if not INSPECTION_PATH.exists():
        return []
    with open(INSPECTION_PATH) as f:
        return json.load(f)


def compute_dashboard_metrics() -> dict:
    """Compute all dashboard KPIs."""
    logs = _load_logs()
    if not logs:
        return _empty_metrics()

    # Error frequency
    error_counts = Counter(l.get("error_code") for l in logs if l.get("error_code"))
    top_failures = error_counts.most_common(10)

    # Model breakdown
    model_counts = Counter(l.get("model") for l in logs if l.get("model"))

    # MTTR (mean time to repair for resolved)
    repair_times = [
        l["repair_hours"] for l in logs
        if l.get("repair_hours") and "RESOLVED" in l.get("outcome", "")
    ]
    mttr = round(sum(repair_times) / len(repair_times), 1) if repair_times else 2.8

    # Resolution rate
    resolved = len([l for l in logs if "RESOLVED" in l.get("outcome", "")])
    resolution_rate = round(resolved / len(logs) * 100, 1) if logs else 0

    # Monthly maintenance trend
    monthly = defaultdict(int)
    for l in logs:
        ts = l.get("timestamp", "")
        if ts:
            try:
                month = datetime.fromisoformat(ts).strftime("%Y-%m")
                monthly[month] += 1
            except ValueError:
                pass
    monthly_sorted = sorted(monthly.items())[-12:]

    # Event type breakdown
    event_counts = Counter(l.get("event_type") for l in logs)

    # Component/failure correlation (from error codes)
    component_failures = Counter()
    code_to_component = {
        "E3": "Condenser Coil", "E5": "Compressor", "U0": "Refrigerant Circuit",
        "A6": "Fan Motor", "103": "Crankcase Heater", "F1": "Compressor",
        "E1": "Sensor Network", "CH01": "Thermistor", "E6": "Communication Bus",
    }
    for code, count in error_counts.items():
        comp = code_to_component.get(code, "Other")
        component_failures[comp] += count

    # Machine health scores
    inspections = _load_inspections()
    health_by_model = defaultdict(list)
    for ins in inspections:
        if ins.get("model") and ins.get("health_score"):
            health_by_model[ins["model"]].append(ins["health_score"])
    machine_health = {
        model: round(sum(scores) / len(scores))
        for model, scores in health_by_model.items()
    }

    # Downtime trend (alarms per month)
    alarm_monthly = defaultdict(int)
    for l in logs:
        if l.get("event_type") == "alarm" and l.get("timestamp"):
            try:
                month = datetime.fromisoformat(l["timestamp"]).strftime("%Y-%m")
                alarm_monthly[month] += 1
            except ValueError:
                pass
    alarm_trend = sorted(alarm_monthly.items())[-12:]

    # KB stats
    md_files = list(KB_DIR.rglob("*.md")) if KB_DIR.exists() else []

    return {
        "total_logs": len(logs),
        "total_stories": len(set(l.get("story") for l in logs if l.get("story", 0) > 0)),
        "total_assets": len(list((KB_DIR / "assets").glob("*.md"))) if (KB_DIR / "assets").exists() else 0,
        "total_error_codes": len(error_counts),
        "kb_documents": len(md_files),
        "mttr_hours": mttr,
        "resolution_rate": resolution_rate,
        "top_failures": top_failures,
        "model_counts": model_counts.most_common(8),
        "monthly_maintenance": monthly_sorted,
        "event_type_counts": event_counts.most_common(),
        "component_failures": component_failures.most_common(8),
        "machine_health": dict(sorted(machine_health.items(), key=lambda x: x[1])[:10]),
        "alarm_trend": alarm_trend,
        "resolved_count": resolved,
        "alarm_count": len([l for l in logs if l.get("event_type") == "alarm"]),
    }


def _empty_metrics() -> dict:
    return {
        "total_logs": 0, "total_stories": 0, "total_assets": 0,
        "total_error_codes": 0, "kb_documents": 0, "mttr_hours": 0,
        "resolution_rate": 0, "top_failures": [], "model_counts": [],
        "monthly_maintenance": [], "event_type_counts": [],
        "component_failures": [], "machine_health": {}, "alarm_trend": [],
        "resolved_count": 0, "alarm_count": 0,
    }


def get_asset_details(asset_file_stem: str) -> Optional[dict]:
    """Load asset OKF details and related logs."""
    asset_path = KB_DIR / "assets" / f"{asset_file_stem}.md"
    if not asset_path.exists():
        return None

    import re
    import yaml
    content = asset_path.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    fm = yaml.safe_load(fm_match.group(1)) if fm_match else {}

    logs = _load_logs()
    model = fm.get("model", "")
    related_logs = [l for l in logs if l.get("model") == model][-20:]

    open_issues = [
        l for l in related_logs
        if "RESOLVED" not in l.get("outcome", "") and l.get("error_code")
    ]

    error_history = Counter(
        l.get("error_code") for l in related_logs if l.get("error_code")
    )

    inspections = _load_inspections()
    asset_inspections = [i for i in inspections if i.get("model") == model][-5:]
    health_scores = [i["health_score"] for i in asset_inspections if i.get("health_score")]
    health_score = round(sum(health_scores) / len(health_scores)) if health_scores else fm.get("health_score", 85)

    return {
        "frontmatter": fm,
        "content": content[fm_match.end():] if fm_match else content,
        "related_logs": related_logs,
        "open_issues": open_issues[:5],
        "error_history": error_history.most_common(8),
        "health_score": health_score,
        "inspections": asset_inspections,
    }


def build_failure_timeline(error_code: str, model: Optional[str] = None) -> list[dict]:
    """Build chronological timeline for a fault from maintenance logs."""
    logs = _load_logs()
    matching = [
        l for l in logs
        if l.get("error_code") == error_code
        and (not model or l.get("model") == model)
    ]

    # Prefer story-sequenced logs
    stories = defaultdict(list)
    for l in matching:
        story_id = l.get("story", 0)
        if story_id > 0:
            stories[story_id].append(l)

    if stories:
        # Use the most complete story
        best_story = max(stories.values(), key=len)
        best_story.sort(key=lambda x: x.get("sequence", 0))
        timeline = []
        for l in best_story:
            ts = l.get("timestamp", "")
            time_label = ""
            if ts:
                try:
                    time_label = datetime.fromisoformat(ts).strftime("%H:%M")
                except ValueError:
                    time_label = ts[:16]
            timeline.append({
                "time": time_label,
                "timestamp": ts,
                "title": l.get("title", l.get("event_type", "Event")),
                "description": l.get("description", "")[:120],
                "event_type": l.get("event_type", ""),
                "outcome": l.get("outcome", ""),
            })
        return timeline

    # Fallback: generic cascade template
    cascade_templates = {
        "E3": [
            ("08:23", "Pressure rising", "Discharge pressure climbing above 600 psig"),
            ("08:45", "Condenser airflow reduced", "One fan showing reduced RPM"),
            ("09:12", "High pressure switch tripped", "E3 lockout — compressor shutdown"),
            ("09:30", "Manual reset attempted", "Reset without root cause investigation"),
        ],
        "E5": [
            ("10:05", "Discharge temperature rising", "Thermistor reading 245°F"),
            ("10:18", "Superheat increasing", "Indicating possible undercharge"),
            ("10:25", "E5 fault triggered", "Compressor thermal protection activated"),
        ],
        "U0": [
            ("14:00", "Suction pressure dropping", "Below minimum operating threshold"),
            ("14:30", "Performance degradation", "Capacity reduced, approach temperature rising"),
            ("15:00", "U0 alarm activated", "Low refrigerant charge detected"),
        ],
        "A6": [
            ("11:00", "Fan amperage anomaly", "Fan #3 drawing 0A — motor not running"),
            ("11:15", "Head pressure increasing", "Reduced condenser airflow"),
            ("11:30", "A6 fault logged", "Fan motor electrical fault confirmed"),
        ],
    }

    template = cascade_templates.get(error_code.upper(), [
        ("—", f"Fault {error_code} detected", "Error code displayed on controller"),
        ("—", "Diagnostic initiated", "Technician dispatched for investigation"),
    ])

    return [
        {"time": t, "title": title, "description": desc, "event_type": "alarm", "outcome": ""}
        for t, title, desc in template
    ]


def search_knowledge(query: str, n_results: int = 8) -> list[dict]:
    """Natural language search across KB and logs."""
    try:
        from src.vector_store import query_knowledge_base, query_maintenance_logs, get_chroma_client
        client = get_chroma_client()
        kb = query_knowledge_base(query, n_results=n_results // 2, client=client)
        logs = query_maintenance_logs(query, n_results=n_results // 2, client=client)
        results = []
        for r in kb:
            results.append({
                "type": "kb",
                "title": r["metadata"].get("name", "KB Document"),
                "snippet": r["document"][:250],
                "relevance": r.get("relevance_score", 0),
                "source": r["metadata"].get("node_id", ""),
            })
        for r in logs:
            results.append({
                "type": "log",
                "title": f"{r['metadata'].get('log_id', '?')} — {r['metadata'].get('model', '')}",
                "snippet": r["document"][:250],
                "relevance": r.get("relevance_score", 0),
                "source": r["metadata"].get("log_id", ""),
            })
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:n_results]
    except Exception:
        return []
