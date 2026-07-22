import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data_integration import validate_dataset
from src.graph_builder import build_graph, parse_markdown_file


def test_validate_dataset_reports_expected_counts():
    report = validate_dataset(ROOT)
    assert report["status"] in {"passed", "needs-attention"}
    assert report["counts"]["assets"] >= 25
    assert report["counts"]["components"] >= 250
    assert report["counts"]["sops"] >= 75
    assert report["counts"]["maintenance_logs"] >= 5000
    assert report["counts"]["incident_reports"] >= 500
    assert report["counts"]["failure_chains"] >= 300
    assert report["counts"]["configuration_profiles"] >= 300
    assert report["graph_stats"]["nodes"] > 0
    assert report["vector_stats"]["knowledge_documents"] > 0


def test_frontmatter_lists_are_parsed_as_graph_links():
    component_doc = parse_markdown_file(ROOT / "data" / "knowledge_base" / "components" / "capacitor.md")
    assert "asset/ahu" in component_doc["wikilinks"]
    assert "asset/rooftop" in component_doc["wikilinks"]


def test_graph_contains_frontmatter_linked_nodes():
    graph = build_graph(ROOT / "data" / "knowledge_base")
    assert "asset/ahu-trane-tam" in graph
    assert "components/capacitor" in graph
    assert "subsystems/compressor-unit" in graph
    assert graph.has_edge("components/capacitor", "asset/ahu-trane-tam") or graph.has_edge("components/capacitor", "asset/ahu-trane-tam")
