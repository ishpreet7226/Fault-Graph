# ⚡ Fault-Graph AI

**Hybrid Graph-RAG Diagnostic Assistant for Industrial HVAC Assets**

> A production-ready AI diagnostic system that combines deterministic knowledge graphs with vector semantic search and LLM synthesis to diagnose industrial chiller faults — from a simple panel photo to a full structured repair guide.

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Fault-Graph AI Pipeline                         │
│                                                                     │
│  📸 Panel Photo                                                     │
│      ↓                                                              │
│  OCR Parser (EasyOCR / pytesseract)                                 │
│      ↓ error_code, model                                            │
│  ┌──────────────────┐    ┌──────────────────────────┐              │
│  │  NetworkX Graph  │    │      ChromaDB Vector      │              │
│  │  (deterministic) │    │  Store (semantic search)  │              │
│  │  • Safety SOPs   │    │  • OKF KB documents       │              │
│  │  • Subsystems    │    │  • Maintenance logs       │              │
│  │  • Components    │    │  • Repair procedures      │              │
│  └────────┬─────────┘    └────────────┬─────────────┘              │
│           └──────────────┬────────────┘                             │
│                          ↓                                           │
│              LangChain Synthesis Prompt                              │
│              (OpenAI / Gemini / Anthropic)                          │
│                          ↓                                           │
│          Structured Diagnostic Report                                │
│  • Safety warnings  • Root cause analysis                            │
│  • Repair steps     • Similar historical cases                       │
└─────────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/ishpreet7226/Fault-Graph.git
cd Fault-Graph
```

### 2. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment (optional — for AI synthesis)
```bash
cp .env.example .env
# Edit .env and add your LLM API key (OpenAI, Google, or Anthropic)
```

> **Without an API key:** The app runs in **Template Mode** using knowledge graph + RAG context directly. No AI required for graph lookup and safety SOP retrieval.

### 5. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
Fault-Graph-AI/
├── data/
│   ├── knowledge_base/          # OKF Markdown files (18 files)
│   │   ├── assets/              # Chiller assets (Carrier 30RAP, York YVAA)
│   │   ├── subsystems/          # Condenser, compressor, refrigerant circuit, control panel
│   │   ├── components/          # HPS, discharge sensor, refrigerant sensor, fan motor
│   │   ├── failures/            # E3, E5, U0, 103, A6 failure modes
│   │   └── sops/                # Safety SOPs (High-Pressure, Refrigerant-Leak, Electrical)
│   ├── logs/
│   │   └── maintenance_logs.json  # 27 synthetic log entries in 3 failure stories
│   └── chroma_db/               # Auto-created ChromaDB persistent storage
├── src/
│   ├── __init__.py
│   ├── graph_builder.py         # OKF parser → NetworkX DiGraph
│   ├── ocr_parser.py            # EasyOCR + regex → structured JSON
│   ├── vector_store.py          # ChromaDB indexing and semantic search
│   └── pipeline.py              # LangChain orchestration pipeline
├── app.py                       # Streamlit multi-tab dashboard
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## 🖥 Features

### Tab 1: ⚡ Diagnostic Hub
- **Photo upload** → OCR extracts error code and model from control panel image
- **Manual input** → Select error code and model from dropdowns
- **Deterministic graph lookup** → Always retrieves safety SOPs and subsystem context from knowledge graph
- **RAG retrieval** → Finds similar historical cases and KB procedures via ChromaDB
- **AI synthesis** → LLM generates ranked root causes and step-by-step repair guide
- **Feedback loop** → "Resolved / Not Resolved" buttons for outcome tracking

### Tab 2: 🕸 Knowledge Graph Explorer
- Interactive `streamlit-agraph` visualization of the OKF knowledge graph
- Filter by node type (asset, subsystem, component, failure, SOP)
- Highlight error code subgraphs
- Click any node to view full metadata and content

### Tab 3: 📊 System Logs & Inspector
- Browse all 27 maintenance log entries with filtering by story, error code, and event type
- Inspect all 18 OKF knowledge base files with YAML frontmatter viewer
- ChromaDB collection status and re-index button

---

## 🔌 LLM Configuration

The pipeline tries LLM providers in this order:

| Provider | Model Used | Env Variable |
|----------|-----------|--------------|
| OpenAI | `gpt-4o-mini` | `OPENAI_API_KEY` |
| Google | `gemini-1.5-flash` | `GOOGLE_API_KEY` |
| Anthropic | `claude-3-haiku` | `ANTHROPIC_API_KEY` |
| None | Template Mode | *(no key required)* |

---

## 🛡 Error Codes Covered

| Code | Name | Severity | Asset |
|------|------|----------|-------|
| `E3` | High Pressure Trip | 🔴 Critical | Carrier 30RAP, York YVAA |
| `E5` | High Discharge Temp | 🔴 Critical | Carrier 30RAP, York YVAA |
| `U0` | Refrigerant Loss | 🔴 Critical | Carrier 30RAP, York YVAA |
| `103` | Prestart Temp Alert | 🔵 Medium | Carrier 30RAP |
| `A6` | Fan Motor Fault | 🟠 High | Carrier 30RAP, York YVAA |

---

## 📦 Key Dependencies

- `streamlit` — Web application framework
- `networkx` — Knowledge graph engine
- `chromadb` — Local vector database
- `sentence-transformers` — Local embedding model (all-MiniLM-L6-v2)
- `easyocr` — OCR text extraction
- `langchain` — LLM orchestration
- `streamlit-agraph` — Interactive graph visualization
- `pyyaml` — YAML frontmatter parsing
- `pillow` — Image processing

---

## 📋 License

MIT License — See LICENSE file for details.

---

*Built with ⚡ by Fault-Graph AI — Graph-RAG Industrial Diagnostic System*
