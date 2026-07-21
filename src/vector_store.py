"""
vector_store.py — ChromaDB Vector Store for NexusOps AI
Indexes OKF Markdown files and maintenance logs with metadata filters.
Uses sentence-transformers for local embeddings (no API key required).
"""

import json
import logging
import hashlib
from pathlib import Path
from typing import Optional

import chromadb
from chromadb.config import Settings

logger = logging.getLogger(__name__)

# Paths
ROOT_DIR = Path(__file__).parent.parent
KB_DIR = ROOT_DIR / "data" / "knowledge_base"
LOGS_DIR = ROOT_DIR / "data" / "logs"
CHROMA_DIR = ROOT_DIR / "data" / "chroma_db"

# Collection names
COLLECTION_KB = "nexusops_knowledge_base"
COLLECTION_LOGS = "nexusops_maintenance_logs"


def get_chroma_client() -> chromadb.PersistentClient:
    """Initialize and return a persistent ChromaDB client."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False)
    )
    return client


def get_embedding_function():
    """
    Return ChromaDB-compatible embedding function.
    Uses sentence-transformers (local, no API key) via chromadb's built-in.
    Falls back to chromadb default if sentence-transformers not installed.
    """
    try:
        from chromadb.utils import embedding_functions
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    except Exception as e:
        logger.warning(f"SentenceTransformer not available ({e}), using default embedding")
        return None


def _stable_id(text: str) -> str:
    """Generate a stable, short ID from text content."""
    return hashlib.md5(text.encode()).hexdigest()[:16]


def index_knowledge_base(client: chromadb.PersistentClient) -> chromadb.Collection:
    """
    Parse all OKF Markdown files and index them into ChromaDB
    with metadata for filtering by type, error_code, severity, etc.
    
    Returns the ChromaDB collection.
    """
    import re
    import yaml

    ef = get_embedding_function()
    collection = client.get_or_create_collection(
        name=COLLECTION_KB,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"}
    )

    documents = []
    metadatas = []
    ids = []

    for md_file in sorted(KB_DIR.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")

        # Extract frontmatter
        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        frontmatter = {}
        if fm_match:
            try:
                frontmatter = yaml.safe_load(fm_match.group(1)) or {}
            except yaml.YAMLError:
                pass

        # Content without frontmatter
        content = text[fm_match.end():] if fm_match else text

        # Clean wikilinks for embedding (convert [[target]] -> target)
        clean_content = re.sub(r"\[\[(.*?)\]\]", r"\1", content)
        clean_content = clean_content[:2000]  # Limit for embedding

        node_id = frontmatter.get("id", str(md_file.relative_to(KB_DIR).with_suffix("")))
        doc_id = _stable_id(node_id)

        # Build metadata (ChromaDB only accepts str/int/float/bool)
        meta = {
            "node_id": str(node_id),
            "name": str(frontmatter.get("name", node_id)),
            "doc_type": str(frontmatter.get("type", "unknown")),
            "severity": str(frontmatter.get("severity", "unknown")),
            "error_code": str(frontmatter.get("error_code", "")),
            "filepath": str(md_file),
            "category": str(md_file.parent.name),  # assets/subsystems/etc
        }

        # Add tags as comma-joined string
        tags = frontmatter.get("tags", [])
        meta["tags"] = ",".join(str(t) for t in tags) if isinstance(tags, list) else str(tags)

        # Add sop_number if SOP
        if "sop_number" in frontmatter:
            meta["sop_number"] = str(frontmatter["sop_number"])

        documents.append(clean_content)
        metadatas.append(meta)
        ids.append(doc_id)

    if documents:
        # Upsert in batches of 50
        batch_size = 50
        for i in range(0, len(documents), batch_size):
            collection.upsert(
                documents=documents[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size],
                ids=ids[i:i+batch_size],
            )
        logger.info(f"[vector_store] Indexed {len(documents)} KB documents")

    return collection


def index_maintenance_logs(client: chromadb.PersistentClient) -> chromadb.Collection:
    """
    Index maintenance log JSON entries into ChromaDB for semantic search.
    """
    ef = get_embedding_function()
    collection = client.get_or_create_collection(
        name=COLLECTION_LOGS,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"}
    )

    logs_file = LOGS_DIR / "maintenance_logs.json"
    if not logs_file.exists():
        logger.warning(f"[vector_store] Maintenance logs not found at {logs_file}")
        return collection

    with open(logs_file, encoding="utf-8") as f:
        data = json.load(f)

    logs = data.get("logs", [])
    documents = []
    metadatas = []
    ids = []

    for log in logs:
        # Build searchable text from log fields
        doc_text = f"""
Asset: {log.get('model', '')} ({log.get('asset_id', '')})
Site: {log.get('site', '')}
Error Code: {log.get('error_code', 'None')}
Title: {log.get('title', '')}
Description: {log.get('description', '')}
Resolution: {log.get('resolution', '')}
Outcome: {log.get('outcome', '')}
        """.strip()

        log_id = str(log.get("id", _stable_id(doc_text)))

        meta = {
            "log_id": str(log.get("id", "")),
            "story": int(log.get("story", 0)),
            "model": str(log.get("model", "")),
            "asset_id": str(log.get("asset_id", "")),
            "error_code": str(log.get("error_code", "")),
            "event_type": str(log.get("event_type", "")),
            "outcome": str(log.get("outcome", "")),
            "timestamp": str(log.get("timestamp", "")),
            "site": str(log.get("site", "")),
        }

        documents.append(doc_text[:1500])
        metadatas.append(meta)
        ids.append(log_id)

    if documents:
        collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )
        logger.info(f"[vector_store] Indexed {len(documents)} maintenance log entries")

    return collection


def initialize_stores() -> tuple[chromadb.Collection, chromadb.Collection]:
    """
    Initialize ChromaDB client and index all data.
    Returns (kb_collection, logs_collection).
    """
    client = get_chroma_client()
    kb_col = index_knowledge_base(client)
    logs_col = index_maintenance_logs(client)
    return kb_col, logs_col


def query_knowledge_base(
    query: str,
    n_results: int = 4,
    filter_type: Optional[str] = None,
    filter_error_code: Optional[str] = None,
    client: Optional[chromadb.PersistentClient] = None,
) -> list[dict]:
    """
    Semantic search over the knowledge base.
    
    Args:
        query: Natural language query string
        n_results: Number of results to return
        filter_type: Optional doc_type filter ('failure', 'sop', 'subsystem', etc.)
        filter_error_code: Optional error_code filter (e.g. 'E3')
        client: Optional pre-initialized ChromaDB client
        
    Returns:
        List of result dicts with document, metadata, and distance
    """
    if client is None:
        client = get_chroma_client()

    ef = get_embedding_function()
    collection = client.get_or_create_collection(
        name=COLLECTION_KB, embedding_function=ef,
        metadata={"hnsw:space": "cosine"}
    )

    # Build where clause
    where = {}
    if filter_type and filter_error_code:
        where = {"$and": [
            {"doc_type": {"$eq": filter_type}},
            {"error_code": {"$eq": filter_error_code}}
        ]}
    elif filter_type:
        where = {"doc_type": {"$eq": filter_type}}
    elif filter_error_code:
        where = {"error_code": {"$eq": filter_error_code}}

    query_kwargs = {
        "query_texts": [query],
        "n_results": min(n_results, max(1, collection.count())),
        "include": ["documents", "metadatas", "distances"],
    }
    if where:
        query_kwargs["where"] = where

    results = collection.query(**query_kwargs)

    output = []
    if results["documents"]:
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            output.append({
                "document": doc,
                "metadata": meta,
                "distance": dist,
                "relevance_score": round(1 - dist, 3),
            })

    return output


def query_maintenance_logs(
    query: str,
    n_results: int = 4,
    filter_error_code: Optional[str] = None,
    filter_model: Optional[str] = None,
    client: Optional[chromadb.PersistentClient] = None,
) -> list[dict]:
    """
    Semantic search over maintenance logs.
    
    Args:
        query: Natural language query
        n_results: Number of results
        filter_error_code: Optional error code filter
        filter_model: Optional model name filter (partial match not supported by ChromaDB)
        
    Returns:
        List of result dicts
    """
    if client is None:
        client = get_chroma_client()

    ef = get_embedding_function()
    collection = client.get_or_create_collection(
        name=COLLECTION_LOGS, embedding_function=ef,
        metadata={"hnsw:space": "cosine"}
    )

    where = {}
    if filter_error_code and filter_model:
        where = {"$and": [
            {"error_code": {"$eq": filter_error_code}},
            {"model": {"$eq": filter_model}}
        ]}
    elif filter_error_code:
        where = {"error_code": {"$eq": filter_error_code}}
    elif filter_model:
        where = {"model": {"$eq": filter_model}}

    query_kwargs = {
        "query_texts": [query],
        "n_results": min(n_results, max(1, collection.count())),
        "include": ["documents", "metadatas", "distances"],
    }
    if where:
        query_kwargs["where"] = where

    results = collection.query(**query_kwargs)

    output = []
    if results["documents"]:
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            output.append({
                "document": doc,
                "metadata": meta,
                "distance": dist,
                "relevance_score": round(1 - dist, 3),
            })

    return output


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Initializing NexusOps AI vector stores...")
    kb_col, logs_col = initialize_stores()
    print(f"\nKB collection: {kb_col.count()} documents")
    print(f"Logs collection: {logs_col.count()} documents")

    print("\n--- KB Query: E3 high pressure ---")
    results = query_knowledge_base("E3 high pressure trip repair procedure", n_results=3)
    for r in results:
        print(f"  [{r['relevance_score']:.3f}] {r['metadata']['name']} ({r['metadata']['doc_type']})")

    print("\n--- Logs Query: fan motor fault resolution ---")
    log_results = query_maintenance_logs("fan motor fault resolution steps", n_results=3)
    for r in log_results:
        print(f"  [{r['relevance_score']:.3f}] {r['metadata']['log_id']}: {r['metadata']['error_code']} - {r['metadata']['outcome']}")
