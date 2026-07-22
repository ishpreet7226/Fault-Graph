"""Utilities to normalize, validate, and report on the enterprise dataset."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import networkx as nx
import yaml

from src.graph_builder import build_graph, parse_markdown_file
from src.vector_store import initialize_stores

ROOT_DIR = Path(__file__).parent.parent
KB_DIR = ROOT_DIR / "data" / "knowledge_base"
LOGS_PATH = ROOT_DIR / "data" / "logs" / "maintenance_logs.json"
INCIDENTS_DIR = ROOT_DIR / "data" / "incident_reports"
CHAINS_DIR = ROOT_DIR / "data" / "failure_chains"
CONFIG_PATH = ROOT_DIR / "data" / "configurations" / "configuration_profiles.json"
REPORT_PATH = ROOT_DIR / "DATASET_REPORT.md"


def _normalize_severity(value: Any) -> str:
    if not value:
        return "unknown"
    normalized = str(value).strip().lower()
    mapping = {
        "critical": "critical",
        "high": "high",
        "medium": "medium",
        "low": "low",
        "unknown": "unknown",
        "info": "low",
        "warning": "medium",
    }
    return mapping.get(normalized, normalized)


def _normalize_tags(tags: Any) -> list[str]:
    if isinstance(tags, str):
        tags = [tags]
    elif not isinstance(tags, list):
        return []
    cleaned = []
    for tag in tags:
        if not tag:
            continue
        normalized = str(tag).strip().lower().replace(" ", "-")
        if normalized not in cleaned:
            cleaned.append(normalized)
    return cleaned


def _normalize_manufacturer(value: Any) -> str:
    if not value:
        return ""
    text = str(value).strip()
    mapping = {"carrier corporation": "Carrier", "carrier": "Carrier", "york": "York", "trane": "Trane", "daikin": "Daikin", "lg": "LG", "mitsubishi": "Mitsubishi", "samsung": "Samsung", "blue star": "Blue Star", "johnson controls": "Johnson Controls"}
    return mapping.get(text.lower(), text)


def _normalize_model(value: Any) -> str:
    if not value:
        return ""
    return str(value).strip()


def _normalize_timestamp(value: Any) -> str:
    if not value:
        return ""
    if isinstance(value, str):
        text = value.strip()
        if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
            return text
        if re.match(r"^\d{4}-\d{2}-\d{2}T", text):
            return text.split("T", 1)[0]
        return text
    return str(value)


def _rewrite_markdown_frontmatter(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not fm_match:
        return
    frontmatter = yaml.safe_load(fm_match.group(1)) or {}
    if not isinstance(frontmatter, dict):
        return

    if "severity" in frontmatter:
        frontmatter["severity"] = _normalize_severity(frontmatter.get("severity"))
    if "tags" in frontmatter:
        frontmatter["tags"] = _normalize_tags(frontmatter.get("tags"))
    if "manufacturer" in frontmatter:
        frontmatter["manufacturer"] = _normalize_manufacturer(frontmatter.get("manufacturer"))
    if "model" in frontmatter:
        frontmatter["model"] = _normalize_model(frontmatter.get("model"))
    if "installation_date" in frontmatter:
        frontmatter["installation_date"] = _normalize_timestamp(frontmatter.get("installation_date"))
    if "date" in frontmatter:
        frontmatter["date"] = _normalize_timestamp(frontmatter.get("date"))

    updated = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True)
    body = text[fm_match.end():]
    path.write_text(f"---\n{updated}---\n\n{body}", encoding="utf-8")


def normalize_dataset(root: Path = ROOT_DIR) -> None:
    kb_dir = root / "data" / "knowledge_base"
    if kb_dir.exists():
        for md_file in sorted(kb_dir.rglob("*.md")):
            _rewrite_markdown_frontmatter(md_file)

    logs_path = root / "data" / "logs" / "maintenance_logs.json"
    if logs_path.exists():
        data = json.loads(logs_path.read_text(encoding="utf-8"))
        logs = data.get("logs", [])
        for log in logs:
            log["severity"] = _normalize_severity(log.get("severity"))
            log["status"] = str(log.get("status", "")).strip().lower()
            log["date"] = _normalize_timestamp(log.get("date"))
            log["asset"] = str(log.get("asset", "")).strip()
            log["weather"] = str(log.get("weather", "")).strip().lower()
            log["environment"] = str(log.get("environment", "")).strip().lower()
        logs_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    incident_dir = root / "data" / "incident_reports"
    if incident_dir.exists():
        for incident_file in sorted(incident_dir.glob("*.json")):
            payload = json.loads(incident_file.read_text(encoding="utf-8"))
            payload["id"] = payload.get("id", incident_file.stem)
            incident_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    chain_dir = root / "data" / "failure_chains"
    if chain_dir.exists():
        for chain_file in sorted(chain_dir.glob("*.json")):
            payload = json.loads(chain_file.read_text(encoding="utf-8"))
            payload["id"] = payload.get("id", chain_file.stem)
            chain_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    config_path = root / "data" / "configurations" / "configuration_profiles.json"
    if config_path.exists():
        payload = json.loads(config_path.read_text(encoding="utf-8"))
        for profile in payload:
            profile["mode"] = str(profile.get("mode", "")).strip().lower()
        config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_graph_stats(graph: nx.DiGraph) -> dict[str, Any]:
    if graph.number_of_nodes() == 0:
        return {
            "nodes": 0,
            "edges": 0,
            "connected_components": 0,
            "average_degree": 0.0,
            "density": 0.0,
            "most_connected_assets": [],
            "most_connected_failures": [],
        }

    undirected = graph.to_undirected()
    degree_map = dict(graph.degree())
    asset_nodes = [node for node, attrs in graph.nodes(data=True) if attrs.get("node_type") == "asset"]
    failure_nodes = [node for node, attrs in graph.nodes(data=True) if attrs.get("node_type") == "failure"]

    most_connected_assets = [
        {"id": node, "degree": degree_map[node], "name": graph.nodes[node].get("name", node)}
        for node in sorted(asset_nodes, key=lambda n: degree_map[n], reverse=True)[:5]
    ]
    most_connected_failures = [
        {"id": node, "degree": degree_map[node], "name": graph.nodes[node].get("name", node)}
        for node in sorted(failure_nodes, key=lambda n: degree_map[n], reverse=True)[:5]
    ]

    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "connected_components": nx.number_connected_components(undirected),
        "average_degree": round(sum(degree_map.values()) / max(1, graph.number_of_nodes()), 3),
        "density": round(nx.density(graph), 3),
        "most_connected_assets": most_connected_assets,
        "most_connected_failures": most_connected_failures,
    }


def validate_dataset(root: Path = ROOT_DIR) -> dict[str, Any]:
    normalize_dataset(root)

    kb_dir = root / "data" / "knowledge_base"
    graph = build_graph(kb_dir)
    stats = build_graph_stats(graph)

    # Build a quick inventory for validation.
    md_files = sorted(kb_dir.rglob("*.md"))
    asset_ids = [doc["node_id"] for doc in (parse_markdown_file(path) for path in md_files) if doc["frontmatter"].get("type") == "asset"]
    component_ids = [doc["node_id"] for doc in (parse_markdown_file(path) for path in md_files) if doc["frontmatter"].get("type") == "component"]
    sop_ids = [doc["node_id"] for doc in (parse_markdown_file(path) for path in md_files) if doc["frontmatter"].get("type") == "sop"]
    failure_ids = [doc["node_id"] for doc in (parse_markdown_file(path) for path in md_files) if doc["frontmatter"].get("type") == "failure"]

    issues: list[str] = []
    duplicates = [item for item, count in Counter(asset_ids + component_ids + sop_ids + failure_ids).items() if count > 1]
    if duplicates:
        issues.append(f"Duplicate IDs detected: {', '.join(sorted(duplicates[:10]))}")

    orphan_nodes = [node for node in graph.nodes() if graph.degree(node) == 0]
    if orphan_nodes:
        issues.append(f"Orphan nodes detected: {', '.join(orphan_nodes[:10])}")

    for md_file in md_files:
        doc = parse_markdown_file(md_file)
        for target in doc["wikilinks"]:
            if target and target not in graph:
                issues.append(f"Broken wikilink in {doc['node_id']}: {target}")

    cycles = [list(cycle) for cycle in nx.simple_cycles(graph) if len(cycle) > 2]
    if cycles:
        issues.append(f"Circular references detected: {len(cycles)}")

    missing_metadata = []
    for md_file in md_files:
        doc = parse_markdown_file(md_file)
        frontmatter = doc["frontmatter"]
        if frontmatter.get("type") == "asset" and not frontmatter.get("manufacturer"):
            missing_metadata.append(doc["node_id"])
        if frontmatter.get("type") == "component" and not frontmatter.get("name"):
            missing_metadata.append(doc["node_id"])
        if frontmatter.get("type") == "sop" and not frontmatter.get("sop_number"):
            missing_metadata.append(doc["node_id"])
    if missing_metadata:
        issues.append(f"Invalid metadata detected in: {', '.join(missing_metadata[:10])}")

    # Maintenance logs and incident reports validation.
    logs_data = []
    if LOGS_PATH.exists():
        logs_data = json.loads(LOGS_PATH.read_text(encoding="utf-8")).get("logs", [])
    log_asset_names = {log.get("asset", "") for log in logs_data if log.get("asset")}
    if not log_asset_names:
        issues.append("No maintenance logs were found")

    incident_files = sorted(INCIDENTS_DIR.glob("*.json")) if INCIDENTS_DIR.exists() else []
    if len(incident_files) == 0:
        issues.append("No incident reports were found")

    chain_files = sorted(CHAINS_DIR.glob("*.json")) if CHAINS_DIR.exists() else []
    if len(chain_files) == 0:
        issues.append("No failure chains were found")

    config_payload = []
    if CONFIG_PATH.exists():
        config_payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if len(config_payload) == 0:
        issues.append("No configuration profiles were found")

    # Rebuild vector store and gather index statistics.
    kb_collection, logs_collection = initialize_stores()
    vector_stats = {
        "knowledge_documents": int(kb_collection.count()),
        "maintenance_logs": int(logs_collection.count()),
    }

    report = {
        "counts": {
            "assets": len(asset_ids),
            "components": len(component_ids),
            "sops": len(sop_ids),
            "failures": len(failure_ids),
            "maintenance_logs": len(logs_data),
            "incident_reports": len(incident_files),
            "failure_chains": len(chain_files),
            "configuration_profiles": len(config_payload),
        },
        "graph_stats": stats,
        "vector_stats": vector_stats,
        "issues": issues,
        "status": "passed" if not issues else "needs-attention",
    }

    write_dataset_report(report)
    return report


def write_dataset_report(report: dict[str, Any], output_path: Path = REPORT_PATH) -> None:
    lines = [
        "# Dataset Report",
        "",
        "## Dataset Counts",
        "",
    ]
    for key, value in report["counts"].items():
        lines.append(f"- {key.replace('_', ' ').title()}: {value}")

    lines.extend([
        "",
        "## Graph Statistics",
        "",
        f"- Nodes: {report['graph_stats']['nodes']}",
        f"- Edges: {report['graph_stats']['edges']}",
        f"- Connected Components: {report['graph_stats']['connected_components']}",
        f"- Average Degree: {report['graph_stats']['average_degree']}",
        f"- Density: {report['graph_stats']['density']}",
        "- Most Connected Assets:",
    ])
    for item in report["graph_stats"]["most_connected_assets"]:
        lines.append(f"  - {item['id']} ({item['degree']} degree)")
    lines.append("- Most Connected Failures:")
    for item in report["graph_stats"]["most_connected_failures"]:
        lines.append(f"  - {item['id']} ({item['degree']} degree)")

    lines.extend([
        "",
        "## Vector Statistics",
        "",
        f"- Knowledge Documents: {report['vector_stats']['knowledge_documents']}",
        f"- Maintenance Logs: {report['vector_stats']['maintenance_logs']}",
        "",
        "## Validation Report",
        "",
        f"- Status: {report['status']}",
    ])
    if report["issues"]:
        lines.append("- Issues:")
        for issue in report["issues"]:
            lines.append(f"  - {issue}")
    else:
        lines.append("- Issues: none")

    lines.extend([
        "",
        "## Known Limitations",
        "",
        "- The dataset is synthetic and designed to represent realistic industrial HVAC telemetry patterns.",
        "- Some retrieval scores depend on the local embedding model and the available runtime environment.",
    ])

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
