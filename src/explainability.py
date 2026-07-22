"""
explainability.py — Build reasoning chains and evidence for diagnostic transparency.
"""

from typing import Optional


def compute_confidence_score(
    ocr_confidence: str,
    knowledge_sources: list,
    similar_cases: list,
    llm_used: bool,
    graph_match: bool,
) -> float:
    """Compute overall diagnosis confidence (0-100)."""
    score = 50.0

    ocr_scores = {"high": 20, "medium": 12, "low": 5, "manual": 25, "unknown": 0}
    score += ocr_scores.get(ocr_confidence, 0)

    score += min(len(knowledge_sources) * 4, 16)
    score += min(len(similar_cases) * 5, 15)

    if similar_cases:
        avg_rel = sum(c.get("relevance", 0) for c in similar_cases) / len(similar_cases)
        score += avg_rel * 10

    if llm_used:
        score += 8
    if graph_match:
        score += 10

    return min(round(score, 1), 99.0)


def build_reasoning_chain(
    error_code: Optional[str],
    model: Optional[str],
    brand: Optional[str],
    ocr_confidence: str,
    failure_name: str,
    knowledge_sources: list,
    similar_cases: list,
    required_sops: list,
    affected_subsystems: list,
    llm_used: bool,
    graph_match: bool,
) -> list[dict]:
    """Build vertical explainability pipeline steps."""
    chain = []

    # Step 1: OCR / Input
    if ocr_confidence == "manual":
        chain.append({
            "step": 1,
            "icon": "⌨️",
            "title": "Manual Input Received",
            "detail": f"Technician entered error code {error_code}",
            "status": "complete",
        })
    else:
        conf_label = ocr_confidence.upper()
        chain.append({
            "step": 1,
            "icon": "📷",
            "title": "OCR Image Analysis",
            "detail": f"Extracted panel text with {conf_label} confidence",
            "status": "complete" if ocr_confidence in ("high", "medium", "manual") else "warning",
        })

    # Step 2: Error code detection
    if error_code:
        chain.append({
            "step": 2,
            "icon": "🔍",
            "title": f"Detected Error Code: {error_code}",
            "detail": failure_name,
            "status": "complete",
        })

    # Step 3: Asset matching
    asset_label = f"{brand or ''} {model or 'Unknown Asset'}".strip()
    chain.append({
        "step": 3,
        "icon": "🏭",
        "title": f"Matched Asset: {asset_label or 'Generic HVAC'}",
        "detail": "Cross-referenced model against knowledge base assets",
        "status": "complete" if model else "warning",
    })

    # Step 4: Graph traversal
    if graph_match and error_code:
        subs = ", ".join(affected_subsystems[:3]) if affected_subsystems else "failure node"
        chain.append({
            "step": 4,
            "icon": "🕸",
            "title": "Traversed Knowledge Graph",
            "detail": f"Found connected subsystems: {subs}",
            "status": "complete",
        })
    elif error_code:
        chain.append({
            "step": 4,
            "icon": "🕸",
            "title": "Knowledge Graph Lookup",
            "detail": "Partial match — error code not fully mapped in graph",
            "status": "warning",
        })

    # Step 5: SOP retrieval
    if required_sops:
        sop_names = ", ".join(s["name"] for s in required_sops[:2])
        chain.append({
            "step": 5,
            "icon": "📋",
            "title": "Retrieved Safety SOPs",
            "detail": sop_names,
            "status": "complete",
        })

    # Step 6: Historical logs
    if similar_cases:
        log_ids = ", ".join(c.get("log_id", "?") for c in similar_cases[:3])
        chain.append({
            "step": 6,
            "icon": "📂",
            "title": "Retrieved Historical Incidents",
            "detail": f"Matched logs: {log_ids}",
            "status": "complete",
        })
    else:
        chain.append({
            "step": 6,
            "icon": "📂",
            "title": "Historical Log Search",
            "detail": "No closely matching maintenance logs found",
            "status": "warning",
        })

    # Step 7: KB documents
    if knowledge_sources:
        sources = ", ".join(knowledge_sources[:3])
        chain.append({
            "step": 7,
            "icon": "📚",
            "title": "Retrieved Knowledge Base Docs",
            "detail": sources,
            "status": "complete",
        })

    # Step 8: Synthesis
    chain.append({
        "step": 8,
        "icon": "🤖" if llm_used else "📋",
        "title": "Generated Diagnosis",
        "detail": "AI synthesis complete" if llm_used else "Template-based diagnosis (set API key for AI)",
        "status": "complete",
    })

    return chain


def build_evidence_items(
    report,
    graph_match: bool,
) -> list[dict]:
    """Build structured evidence checklist."""
    items = []

    for sop in report.required_sops:
        items.append({
            "type": "sop",
            "label": sop.get("name", "Safety SOP"),
            "icon": "📋",
            "verified": True,
        })

    for src in report.knowledge_sources[:5]:
        items.append({
            "type": "kb",
            "label": src,
            "icon": "📚",
            "verified": True,
        })

    for case in report.similar_cases[:3]:
        items.append({
            "type": "log",
            "label": f"Maintenance Log {case.get('log_id', '?')} — {case.get('outcome', '')[:25]}",
            "icon": "📂",
            "verified": True,
        })

    if graph_match:
        items.append({
            "type": "graph",
            "label": "Knowledge graph path verified",
            "icon": "🕸",
            "verified": True,
        })

    if report.affected_subsystems:
        items.append({
            "type": "sensor",
            "label": f"Affected: {', '.join(report.affected_subsystems[:2])}",
            "icon": "⚙️",
            "verified": True,
        })

    if report.ocr_confidence in ("high", "medium"):
        items.append({
            "type": "ocr",
            "label": f"OCR extraction ({report.ocr_confidence} confidence)",
            "icon": "📷",
            "verified": True,
        })

    return items
