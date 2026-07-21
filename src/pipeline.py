"""
pipeline.py — LangChain Orchestration Pipeline for NexusOps AI
Connects OCR -> NetworkX Graph lookup -> ChromaDB RAG retrieval -> LLM synthesis
Produces structured diagnostic reports with safety warnings and repair steps.
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field

from src.graph_builder import get_graph, get_repair_context, find_failure_node
from src.ocr_parser import extract_from_image, extract_from_text_input, structure_ocr_result
from src.vector_store import (
    get_chroma_client, initialize_stores,
    query_knowledge_base, query_maintenance_logs
)

logger = logging.getLogger(__name__)


@dataclass
class DiagnosticReport:
    """Structured output from the NexusOps AI diagnostic pipeline."""
    error_code: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    severity: str = "unknown"
    failure_name: str = "Unknown Fault"
    
    # Safety warnings (always from graph, deterministic)
    safety_warnings: list[str] = field(default_factory=list)
    required_sops: list[dict] = field(default_factory=list)
    required_ppe: list[str] = field(default_factory=list)
    
    # Root cause analysis (from RAG + LLM)
    root_cause_summary: str = ""
    probable_root_causes: list[str] = field(default_factory=list)
    affected_subsystems: list[str] = field(default_factory=list)
    affected_components: list[str] = field(default_factory=list)
    
    # Repair guidance (from LLM synthesis)
    repair_steps: list[str] = field(default_factory=list)
    estimated_repair_time_hours: Optional[float] = None
    tools_required: list[str] = field(default_factory=list)
    
    # Supporting evidence
    similar_cases: list[dict] = field(default_factory=list)
    knowledge_sources: list[str] = field(default_factory=list)
    
    # Metadata
    ocr_confidence: str = "unknown"
    ocr_raw_text: str = ""
    llm_used: bool = False
    fallback_mode: bool = False
    diagnosis_notes: str = ""

    def to_dict(self) -> dict:
        return {
            "error_code": self.error_code,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "severity": self.severity,
            "failure_name": self.failure_name,
            "safety_warnings": self.safety_warnings,
            "required_sops": self.required_sops,
            "required_ppe": self.required_ppe,
            "root_cause_summary": self.root_cause_summary,
            "probable_root_causes": self.probable_root_causes,
            "affected_subsystems": self.affected_subsystems,
            "affected_components": self.affected_components,
            "repair_steps": self.repair_steps,
            "estimated_repair_time_hours": self.estimated_repair_time_hours,
            "tools_required": self.tools_required,
            "similar_cases": self.similar_cases,
            "knowledge_sources": self.knowledge_sources,
            "ocr_confidence": self.ocr_confidence,
            "llm_used": self.llm_used,
            "fallback_mode": self.fallback_mode,
            "diagnosis_notes": self.diagnosis_notes,
        }


# ─── Safety Data (hardcoded for determinism, no LLM override) ─────────────────

SAFETY_DATABASE = {
    "E3": {
        "warnings": [
            "🚨 DANGER: High pressure refrigerant system — discharge pressure may exceed 650 psig",
            "⚠️ DO NOT reset fault without identifying root cause — repeated resets risk catastrophic failure",
            "⚠️ Allow 30 minutes for system to cool before approaching compressor area",
        ],
        "ppe": ["Safety glasses / face shield", "Cryogenic-rated refrigerant gloves", "FR clothing"],
        "sops": ["SOP-REF-001: High-Pressure-Lockout"],
        "repair_time_hours": 2.0,
        "tools": ["Manifold gauge set (R-410A rated)", "LOTO kit", "Coil cleaner spray"],
    },
    "E5": {
        "warnings": [
            "🚨 DANGER: Discharge line temperature may exceed 250°F — severe burn risk",
            "⚠️ Allow minimum 30 minutes cool-down before any service work",
            "⚠️ High superheat indicates undercharge — check for refrigerant leak before recharging",
        ],
        "ppe": ["Heat-resistant gloves", "Safety glasses", "Cryogenic-rated gloves for refrigerant work"],
        "sops": ["SOP-REF-001: High-Pressure-Lockout", "SOP-REF-002: Refrigerant-Leak-Check"],
        "repair_time_hours": 3.5,
        "tools": ["Manifold gauge set", "Thermometer probe", "Leak detector", "Refrigerant scale"],
    },
    "U0": {
        "warnings": [
            "🚨 ENVIRONMENTAL HAZARD: EPA Section 608 — illegal to vent refrigerant to atmosphere",
            "🚨 ASPHYXIATION RISK: R-410A/R-134a displaces oxygen — ensure adequate ventilation",
            "⚠️ Do NOT add refrigerant without first locating and repairing the leak source",
        ],
        "ppe": ["Safety glasses", "Cryogenic-rated gloves", "SCBA if >1000 ppm detected"],
        "sops": ["SOP-REF-002: Refrigerant-Leak-Check", "SOP-REF-001: High-Pressure-Lockout"],
        "repair_time_hours": 6.0,
        "tools": ["Electronic leak detector", "UV dye kit", "Nitrogen tank", "Refrigerant recovery unit", "Vacuum pump"],
    },
    "103": {
        "warnings": [
            "⚠️ Verify crankcase heater operation before any startup attempt in cold ambient",
            "⚠️ Cold startup without proper oil temperature risks compressor damage from oil dilution",
            "ℹ️ Allow minimum 8-hour pre-heat if crankcase heater was non-functional",
        ],
        "ppe": ["Safety glasses", "Insulated electrical gloves"],
        "sops": ["SOP-ELC-001: Electrical-Safety"],
        "repair_time_hours": 1.0,
        "tools": ["Multimeter (CAT III)", "Non-contact thermometer"],
    },
    "A6": {
        "warnings": [
            "🚨 DANGER: Fan motors operate at 460VAC/3Ph — risk of electrocution and arc flash",
            "⚠️ Full LOTO required on main disconnect before accessing fan motors",
            "⚠️ A6 fault can cascade to E3 within 15-30 minutes — treat as urgent",
        ],
        "ppe": ["Arc flash PPE (CAT 2, 8 cal/cm²)", "Insulated rubber gloves (Class 00)", "Face shield"],
        "sops": ["SOP-ELC-001: Electrical-Safety"],
        "repair_time_hours": 2.0,
        "tools": ["Multimeter (CAT III, 600V)", "Megohmmeter", "Capacitor meter", "LOTO kit", "Clamp meter"],
    },
}


# ─── Graph Lookup (deterministic) ─────────────────────────────────────────────

def run_graph_lookup(error_code: str) -> dict:
    """
    Run deterministic graph lookup for an error code.
    Returns structured context from the knowledge graph.
    """
    G = get_graph()
    ctx = get_repair_context(error_code, G)
    safety = SAFETY_DATABASE.get(error_code.upper(), {})

    return {
        "graph_context": ctx,
        "safety_warnings": safety.get("warnings", []),
        "required_ppe": safety.get("ppe", []),
        "required_sops_display": safety.get("sops", []),
        "repair_time_hours": safety.get("repair_time_hours"),
        "tools_required": safety.get("tools", []),
    }


# ─── RAG Retrieval ────────────────────────────────────────────────────────────

def run_rag_retrieval(error_code: str, model: Optional[str] = None) -> dict:
    """
    Retrieve relevant KB documents and maintenance log examples.
    """
    client = get_chroma_client()

    query = f"{error_code} fault diagnosis repair procedure root cause"
    if model:
        query = f"{model} {query}"

    kb_results = query_knowledge_base(
        query, n_results=4, filter_error_code=error_code, client=client
    )

    # Also get SOP documents
    sop_results = query_knowledge_base(
        f"safety procedure {error_code}", n_results=2,
        filter_type="sop", client=client
    )

    # Maintenance log examples
    log_results = query_maintenance_logs(
        query, n_results=3, filter_error_code=error_code, client=client
    )

    # If no filtered results, try broader search
    if not kb_results:
        kb_results = query_knowledge_base(query, n_results=4, client=client)
    if not log_results:
        log_results = query_maintenance_logs(query, n_results=3, client=client)

    return {
        "kb_results": kb_results,
        "sop_results": sop_results,
        "log_results": log_results,
    }


# ─── LLM Synthesis ────────────────────────────────────────────────────────────

def build_diagnosis_prompt(
    error_code: str,
    model: Optional[str],
    graph_ctx: dict,
    rag_results: dict,
) -> str:
    """
    Build the LangChain synthesis prompt from graph + RAG context.
    """
    # Format graph context
    failure_name = graph_ctx["graph_context"].get("failure_name", "Unknown Fault")
    severity = graph_ctx["graph_context"].get("severity", "unknown")
    subsystems = [s["name"] for s in graph_ctx["graph_context"].get("subsystems", [])]
    components = [c["name"] for c in graph_ctx["graph_context"].get("components", [])]
    content_snippet = graph_ctx["graph_context"].get("content_snippet", "")

    # Format RAG context
    kb_context = "\n\n".join([
        f"[KB Doc: {r['metadata'].get('name', 'unknown')}]\n{r['document'][:400]}"
        for r in rag_results.get("kb_results", [])
    ])

    log_context = "\n\n".join([
        f"[Log {r['metadata'].get('log_id', '?')} | {r['metadata'].get('model', '')} | Outcome: {r['metadata'].get('outcome', '')}]\n{r['document'][:300]}"
        for r in rag_results.get("log_results", [])
    ])

    prompt = f"""You are NexusOps AI, an expert industrial chiller diagnostic assistant.

FAULT DETECTED:
- Error Code: {error_code}
- Fault Name: {failure_name}
- Asset Model: {model or "Unknown"}
- Severity: {severity.upper()}

KNOWLEDGE GRAPH CONTEXT:
- Affected Subsystems: {', '.join(subsystems) if subsystems else 'See KB docs below'}
- Affected Components: {', '.join(components) if components else 'See KB docs below'}
- Graph Content: {content_snippet[:300]}

KNOWLEDGE BASE DOCUMENTS:
{kb_context or "No specific KB documents found for this error code."}

SIMILAR MAINTENANCE LOG CASES:
{log_context or "No similar historical cases found in the maintenance logs."}

TASK: Generate a structured diagnostic report for this fault. You MUST:
1. Identify the TOP 3 most probable root causes (ranked by likelihood)
2. Provide a clear, step-by-step repair guide (minimum 5 steps)
3. Include any special tool requirements
4. Estimate repair time
5. Note any cascade risks (if this fault can lead to other faults)

Format your response as valid JSON with this structure:
{{
    "root_cause_summary": "One paragraph summary of most likely root cause and mechanism",
    "probable_root_causes": ["cause 1 (most likely)", "cause 2", "cause 3"],
    "repair_steps": [
        "Step 1: ...",
        "Step 2: ...",
        "Step 3: ...",
        "Step 4: ...",
        "Step 5: ..."
    ],
    "cascade_risks": ["risk 1", "risk 2"],
    "estimated_repair_time_hours": 2.0,
    "diagnosis_notes": "Any additional notes for the technician"
}}

Respond ONLY with the JSON object, no additional text."""

    return prompt


def call_llm(prompt: str) -> Optional[dict]:
    """
    Call LLM via LangChain. Tries multiple providers in order:
    1. OpenAI (if OPENAI_API_KEY set)
    2. Google Gemini (if GOOGLE_API_KEY set)
    3. Anthropic (if ANTHROPIC_API_KEY set)
    Returns parsed JSON dict or None if all fail.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    # Try OpenAI
    if api_key:
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.messages import HumanMessage

            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, api_key=api_key)
            response = llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            # Strip markdown code fences if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            return json.loads(content)
        except Exception as e:
            logger.warning(f"[LLM] OpenAI failed: {e}")

    # Try Google Gemini
    if google_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.messages import HumanMessage

            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", temperature=0.1, google_api_key=google_key
            )
            response = llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            return json.loads(content)
        except Exception as e:
            logger.warning(f"[LLM] Gemini failed: {e}")

    # Try Anthropic
    if anthropic_key:
        try:
            from langchain_anthropic import ChatAnthropic
            from langchain_core.messages import HumanMessage

            llm = ChatAnthropic(
                model="claude-3-haiku-20240307", temperature=0.1, api_key=anthropic_key
            )
            response = llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            return json.loads(content)
        except Exception as e:
            logger.warning(f"[LLM] Anthropic failed: {e}")

    logger.warning("[LLM] No LLM API keys configured — using fallback templates")
    return None


def generate_fallback_diagnosis(error_code: str, graph_ctx: dict, rag_results: dict) -> dict:
    """
    Rule-based fallback when no LLM API key is configured.
    Uses the knowledge graph content directly as the diagnosis.
    """
    content = graph_ctx["graph_context"].get("content_snippet", "")
    failure_name = graph_ctx["graph_context"].get("failure_name", "Unknown Fault")
    subsystems = [s["name"] for s in graph_ctx["graph_context"].get("subsystems", [])]

    # Extract repair steps from KB results
    repair_steps = []
    kb_docs = rag_results.get("kb_results", [])
    for doc in kb_docs[:2]:
        text = doc.get("document", "")
        # Extract numbered steps from KB content
        import re
        steps = re.findall(r"\d+\.\s+\*\*[^*]+\*\*[^|\n]+", text)
        repair_steps.extend(steps[:4])

    if not repair_steps:
        repair_steps = [
            f"Step 1: Follow mandatory safety procedures for {error_code} fault",
            f"Step 2: Inspect {', '.join(subsystems[:2]) if subsystems else 'affected subsystems'}",
            "Step 3: Connect manifold gauges to measure system pressures",
            "Step 4: Identify and address the root cause before resetting fault",
            "Step 5: Monitor system for 2 hours after restart to confirm resolution",
        ]

    # Get similar cases from logs
    similar = []
    for log in rag_results.get("log_results", []):
        similar.append({
            "log_id": log["metadata"].get("log_id", ""),
            "model": log["metadata"].get("model", ""),
            "outcome": log["metadata"].get("outcome", ""),
            "snippet": log["document"][:200],
        })

    return {
        "root_cause_summary": (
            f"Based on knowledge graph analysis: {failure_name} is typically caused by "
            f"issues in {', '.join(subsystems[:2]) if subsystems else 'the affected subsystems'}. "
            f"Review the detailed OKF failure documentation for this error code."
        ),
        "probable_root_causes": [
            "Root cause 1: See knowledge base failure documentation",
            "Root cause 2: Check connected subsystems listed in graph context",
            "Root cause 3: Review similar historical cases below",
        ],
        "repair_steps": repair_steps[:7],
        "cascade_risks": [],
        "estimated_repair_time_hours": SAFETY_DATABASE.get(error_code.upper(), {}).get("repair_time_hours", 2.0),
        "diagnosis_notes": (
            "⚠️ Running in template mode — configure an LLM API key (OPENAI_API_KEY, "
            "GOOGLE_API_KEY, or ANTHROPIC_API_KEY) in .env for AI-powered diagnosis synthesis."
        ),
    }


# ─── Main Pipeline ────────────────────────────────────────────────────────────

def run_diagnostic_pipeline(
    image_source=None,
    manual_text: Optional[str] = None,
    manual_error_code: Optional[str] = None,
    manual_model: Optional[str] = None,
) -> DiagnosticReport:
    """
    Full NexusOps AI diagnostic pipeline:
    1. OCR extraction (or manual input)
    2. Graph-based safety lookup (deterministic)
    3. RAG retrieval from ChromaDB
    4. LLM synthesis (or fallback templates)
    
    Args:
        image_source: Image bytes or path for OCR
        manual_text: Raw text for parsing (if no image)
        manual_error_code: Override error code (skips OCR parsing)
        manual_model: Override model name
        
    Returns:
        DiagnosticReport dataclass
    """
    report = DiagnosticReport()

    # ── Step 1: OCR / Input Parsing ──────────────────────────────────────────
    if manual_error_code:
        report.error_code = manual_error_code.upper()
        report.model = manual_model
        report.ocr_confidence = "manual"
    elif image_source is not None:
        ocr_result = extract_from_image(image_source)
        report.error_code = ocr_result.get("error_code")
        report.model = ocr_result.get("model")
        report.manufacturer = ocr_result.get("manufacturer")
        report.ocr_confidence = ocr_result.get("confidence", "unknown")
        report.ocr_raw_text = ocr_result.get("raw_text", "")
    elif manual_text:
        ocr_result = extract_from_text_input(manual_text)
        report.error_code = ocr_result.get("error_code")
        report.model = ocr_result.get("model")
        report.manufacturer = ocr_result.get("manufacturer")
        report.ocr_confidence = ocr_result.get("confidence", "unknown")
        report.ocr_raw_text = manual_text

    if not report.error_code:
        report.failure_name = "No error code detected"
        report.diagnosis_notes = (
            "Could not detect an error code from the provided input. "
            "Please manually enter the error code displayed on the control panel."
        )
        report.fallback_mode = True
        return report

    # ── Step 2: Graph Lookup (deterministic, always runs) ────────────────────
    logger.info(f"[pipeline] Running graph lookup for {report.error_code}")
    graph_lookup = run_graph_lookup(report.error_code)
    graph_ctx = graph_lookup["graph_context"]

    report.severity = graph_ctx.get("severity", "unknown")
    report.failure_name = graph_ctx.get("failure_name", f"Error {report.error_code}")
    report.safety_warnings = graph_lookup["safety_warnings"]
    report.required_ppe = graph_lookup["required_ppe"]
    report.required_sops = [
        {"name": s, "id": s.lower().replace(" ", "-").replace(":", "")}
        for s in graph_lookup["required_sops_display"]
    ]
    report.tools_required = graph_lookup["tools_required"]
    report.estimated_repair_time_hours = graph_lookup["repair_time_hours"]
    report.affected_subsystems = [s["name"] for s in graph_ctx.get("subsystems", [])]
    report.affected_components = [c["name"] for c in graph_ctx.get("components", [])]

    # ── Step 3: RAG Retrieval ─────────────────────────────────────────────────
    logger.info(f"[pipeline] Running RAG retrieval for {report.error_code}")
    try:
        rag_results = run_rag_retrieval(report.error_code, report.model)
        report.knowledge_sources = [
            r["metadata"].get("name", r["metadata"].get("node_id", ""))
            for r in rag_results.get("kb_results", [])
        ]
        report.similar_cases = [
            {
                "log_id": r["metadata"].get("log_id", ""),
                "model": r["metadata"].get("model", ""),
                "outcome": r["metadata"].get("outcome", ""),
                "event_type": r["metadata"].get("event_type", ""),
                "relevance": r.get("relevance_score", 0),
                "snippet": r["document"][:200],
            }
            for r in rag_results.get("log_results", [])
        ]
    except Exception as e:
        logger.error(f"[pipeline] RAG retrieval failed: {e}")
        rag_results = {"kb_results": [], "sop_results": [], "log_results": []}

    # ── Step 4: LLM Synthesis ─────────────────────────────────────────────────
    prompt = build_diagnosis_prompt(
        report.error_code, report.model, graph_lookup, rag_results
    )

    llm_result = call_llm(prompt)
    report.llm_used = llm_result is not None

    if not llm_result:
        logger.info("[pipeline] Using fallback template diagnosis")
        report.fallback_mode = True
        llm_result = generate_fallback_diagnosis(
            report.error_code, graph_lookup, rag_results
        )

    # Apply LLM results to report
    report.root_cause_summary = llm_result.get("root_cause_summary", "")
    report.probable_root_causes = llm_result.get("probable_root_causes", [])
    report.repair_steps = llm_result.get("repair_steps", [])
    if llm_result.get("estimated_repair_time_hours"):
        report.estimated_repair_time_hours = llm_result["estimated_repair_time_hours"]
    report.diagnosis_notes = llm_result.get("diagnosis_notes", "")

    logger.info(
        f"[pipeline] Diagnosis complete for {report.error_code} | "
        f"LLM: {report.llm_used} | Severity: {report.severity}"
    )
    return report


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=== NexusOps AI Diagnostic Pipeline Test ===\n")

    # First, ensure stores are initialized
    print("Initializing vector stores...")
    initialize_stores()

    # Test with manual error code
    print("\nRunning diagnosis for error code E3...")
    report = run_diagnostic_pipeline(
        manual_error_code="E3",
        manual_model="Carrier 30RAP"
    )

    print(f"\n{'='*60}")
    print(f"DIAGNOSTIC REPORT — {report.failure_name}")
    print(f"{'='*60}")
    print(f"Error Code: {report.error_code}")
    print(f"Severity: {report.severity.upper()}")
    print(f"\n🚨 SAFETY WARNINGS:")
    for w in report.safety_warnings:
        print(f"  {w}")
    print(f"\n📋 REQUIRED SOPs: {[s['name'] for s in report.required_sops]}")
    print(f"\n🔍 ROOT CAUSE: {report.root_cause_summary[:200]}...")
    print(f"\n🔧 REPAIR STEPS:")
    for step in report.repair_steps[:5]:
        print(f"  {step}")
    print(f"\n⏱  Estimated Time: {report.estimated_repair_time_hours}h")
    print(f"LLM Used: {report.llm_used} | Fallback: {report.fallback_mode}")
