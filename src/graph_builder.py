"""
graph_builder.py — OKF Knowledge Graph Builder for NexusOps AI
Parses all Markdown files with YAML frontmatter and [[wikilinks]] into a
directed NetworkX graph for deterministic graph-based lookups.
"""

import os
import re
import yaml
import networkx as nx
from pathlib import Path
from typing import Optional


KB_DIR = Path(__file__).parent.parent / "data" / "knowledge_base"


def parse_markdown_file(filepath: Path) -> dict:
    """
    Parse a single OKF Markdown file and return a dict with:
    - frontmatter: dict of YAML metadata
    - content: the raw markdown body text
    - wikilinks: list of [[target]] wikilink strings extracted from content
    - node_id: the canonical `id` from frontmatter (e.g. 'failures/E3-high-pressure-trip')
    """
    text = filepath.read_text(encoding="utf-8")

    # Extract YAML frontmatter between ---
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    frontmatter = {}
    if fm_match:
        try:
            frontmatter = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError as e:
            print(f"[WARN] YAML parse error in {filepath}: {e}")

    # Body content (after frontmatter)
    content = text[fm_match.end():] if fm_match else text

    # Extract all [[wikilinks]]
    wikilinks = re.findall(r"\[\[(.*?)\]\]", content + str(frontmatter))

    # Also extract from YAML string values that contain [[...]]
    fm_str = fm_match.group(1) if fm_match else ""
    fm_wikilinks = re.findall(r"\[\[(.*?)\]\]", fm_str)
    wikilinks = list(set(wikilinks + fm_wikilinks))

    node_id = frontmatter.get("id", str(filepath.relative_to(KB_DIR).with_suffix("")))

    return {
        "node_id": node_id,
        "frontmatter": frontmatter,
        "content": content,
        "wikilinks": wikilinks,
        "filepath": str(filepath),
    }


def build_graph(kb_dir: Path = KB_DIR) -> nx.DiGraph:
    """
    Parse all .md files in the knowledge base directory tree and build
    a directed NetworkX graph where:
    - Nodes: each OKF document (id from YAML frontmatter)
    - Edges: directed from source node to each [[wikilink]] target
    
    Node attributes include all YAML frontmatter fields plus content.
    """
    G = nx.DiGraph()
    parsed_docs = []

    for md_file in sorted(kb_dir.rglob("*.md")):
        doc = parse_markdown_file(md_file)
        parsed_docs.append(doc)

        node_id = doc["node_id"]
        fm = doc["frontmatter"]

        # Add node with all frontmatter as attributes
        G.add_node(
            node_id,
            name=fm.get("name", node_id),
            node_type=fm.get("type", "unknown"),
            severity=fm.get("severity", "unknown"),
            error_code=fm.get("error_code", None),
            tags=fm.get("tags", []),
            content=doc["content"][:500],  # truncate for memory efficiency
            filepath=doc["filepath"],
            **{k: v for k, v in fm.items() if k not in
               ("id", "name", "type", "severity", "error_code", "tags")
               and isinstance(v, (str, int, float, bool))}
        )

    # Second pass: add directed edges for wikilinks
    for doc in parsed_docs:
        source = doc["node_id"]
        for target in doc["wikilinks"]:
            target = target.strip()
            if target and target != source:
                # Add target node as placeholder if it doesn't exist
                if not G.has_node(target):
                    G.add_node(target, name=target, node_type="reference",
                               severity="unknown")
                G.add_edge(source, target, link_type="wikilink")

    print(f"[graph_builder] Built graph: {G.number_of_nodes()} nodes, "
          f"{G.number_of_edges()} edges from {len(parsed_docs)} documents")
    return G


def get_subsystem_for_error(error_code: str, G: nx.DiGraph) -> list[str]:
    """
    Given an error code string (e.g. 'E3'), return a list of subsystem node IDs
    that are linked from the corresponding failure node.
    """
    results = []
    error_code_upper = error_code.upper()
    for node_id, attrs in G.nodes(data=True):
        ec = attrs.get("error_code")
        if ec and str(ec).upper() == error_code_upper:
            # Find edges to subsystem nodes
            for _, target in G.out_edges(node_id):
                target_attrs = G.nodes[target]
                if target_attrs.get("node_type") == "subsystem":
                    results.append(target)
    return results


def get_sops_for_error(error_code: str, G: nx.DiGraph) -> list[dict]:
    """
    Given an error code string (e.g. 'E3'), return a list of SOP node dicts
    reachable from the corresponding failure node.
    """
    sops = []
    error_code_upper = error_code.upper()
    for node_id, attrs in G.nodes(data=True):
        ec = attrs.get("error_code")
        if ec and str(ec).upper() == error_code_upper:
            # BFS from this failure node to find all SOP nodes
            for _, target in G.out_edges(node_id):
                target_attrs = G.nodes[target]
                if target_attrs.get("node_type") == "sop":
                    sops.append({
                        "id": target,
                        "name": target_attrs.get("name", target),
                        "sop_number": target_attrs.get("sop_number", ""),
                        "severity": target_attrs.get("severity", ""),
                    })
    return sops


def get_connected_nodes(node_id: str, G: nx.DiGraph, depth: int = 2) -> list[dict]:
    """
    Return all nodes reachable from node_id within `depth` hops,
    along with their attributes (for context retrieval).
    """
    if node_id not in G:
        return []

    connected = []
    visited = {node_id}
    frontier = [node_id]

    for _ in range(depth):
        next_frontier = []
        for n in frontier:
            for _, neighbor in G.out_edges(n):
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_frontier.append(neighbor)
                    attrs = G.nodes[neighbor]
                    connected.append({
                        "id": neighbor,
                        "name": attrs.get("name", neighbor),
                        "type": attrs.get("node_type", "unknown"),
                        "severity": attrs.get("severity", "unknown"),
                        "error_code": attrs.get("error_code"),
                    })
        frontier = next_frontier

    return connected


def find_failure_node(error_code: str, G: nx.DiGraph) -> Optional[str]:
    """Find the primary failure node ID for a given error code."""
    error_code_upper = str(error_code).upper()
    for node_id, attrs in G.nodes(data=True):
        ec = attrs.get("error_code")
        if ec and str(ec).upper() == error_code_upper:
            return node_id
    return None


def get_repair_context(error_code: str, G: nx.DiGraph) -> dict:
    """
    Full context lookup for a given error code — returns failure node info,
    connected subsystems, SOPs, and components.
    """
    failure_node = find_failure_node(error_code, G)
    if not failure_node:
        return {
            "error_code": error_code,
            "failure_node": None,
            "failure_name": f"Unknown error code: {error_code}",
            "severity": "unknown",
            "subsystems": [],
            "sops": [],
            "components": [],
            "connected_nodes": [],
        }

    attrs = G.nodes[failure_node]
    connected = get_connected_nodes(failure_node, G, depth=2)

    subsystems = [n for n in connected if n["type"] == "subsystem"]
    sops = [n for n in connected if n["type"] == "sop"]
    components = [n for n in connected if n["type"] == "component"]

    return {
        "error_code": error_code,
        "failure_node": failure_node,
        "failure_name": attrs.get("name", failure_node),
        "severity": attrs.get("severity", "unknown"),
        "content_snippet": attrs.get("content", ""),
        "subsystems": subsystems,
        "sops": sops,
        "components": components,
        "connected_nodes": connected,
    }


# Singleton graph instance for reuse
_graph_instance: Optional[nx.DiGraph] = None


def get_graph() -> nx.DiGraph:
    """Return a cached graph instance, building it on first call."""
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = build_graph()
    return _graph_instance


if __name__ == "__main__":
    G = build_graph()
    print("\n--- Graph Summary ---")
    print(f"Nodes: {list(G.nodes())[:10]}...")
    print(f"\nRepair context for E3:")
    import json
    ctx = get_repair_context("E3", G)
    print(json.dumps(ctx, indent=2, default=str))
