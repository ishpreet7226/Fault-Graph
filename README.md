

# ⚡ Fault-Graph AI

## Enterprise Hybrid Graph-RAG Diagnostic Platform for Industrial HVAC Systems

> **Fault-Graph AI** is an enterprise-grade AI-powered industrial diagnostics platform that combines **Knowledge Graphs, Retrieval-Augmented Generation (Graph-RAG), OCR, Machine Learning, Predictive Analytics, and Explainable AI** to diagnose, explain, and predict HVAC equipment failures from control-panel images, maintenance history, and technical documentation.

Designed as a production-ready industrial AI platform, Fault-Graph AI enables technicians and maintenance engineers to move from **fault detection** to **root-cause analysis**, **repair planning**, and **predictive maintenance** in seconds.

---

# 🚀 Key Highlights

* Hybrid **Knowledge Graph + Graph-RAG** architecture
* Industrial OCR for control panel fault codes
* Enterprise-scale HVAC knowledge base
* Multi-brand equipment support
* Predictive maintenance engine
* Explainable AI diagnostics
* Maintenance log intelligence
* Failure propagation analysis
* Interactive knowledge graph visualization
* Local-first deployment
* Works with or without LLM APIs

---

# 🏗 System Architecture

```
                 📷 Control Panel Image
                           │
                           ▼
                    OCR + Vision Parser
        (EasyOCR / Tesseract / Vision Models)
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
 Knowledge Graph                     Chroma Vector DB
 (NetworkX)                          (Semantic Search)
        │                                     │
        │                                     │
 Components                       Manuals
 Fault Codes                      SOPs
 Assets                           Repair Guides
 Sensors                          Maintenance Logs
 Failure Chains                   Incident Reports
 Configurations                   OEM Documentation
        └──────────────────┬──────────────────┘
                           ▼
                 LangChain Graph-RAG Pipeline
                           ▼
                  Explainable AI Engine
                           ▼
        Root Cause + Risk + SOP + Repair Plan
                           ▼
            Predictive Maintenance Analytics
```

---

# 🧠 AI Capabilities

## Graph-RAG Diagnosis

* Deterministic knowledge graph traversal
* Semantic retrieval using ChromaDB
* Context-aware LLM reasoning
* Safety-first repair recommendations

---

## Industrial OCR

Supports

* Panel displays
* Error code labels
* Equipment nameplates
* Serial numbers
* Model identification

---

## Explainable AI

Instead of returning only an answer, Fault-Graph AI explains:

* Why the failure occurred
* Supporting evidence
* Knowledge graph path
* Similar historical cases
* Confidence score

---

## Predictive Maintenance

Predicts

* Failure probability
* Remaining useful life
* Recurring faults
* Maintenance recommendations

---

# 📂 Enterprise Dataset

The project now contains an industrial-scale synthetic enterprise dataset.

### Assets

* 25 HVAC systems

### Components

* 250+ industrial components

### Failure Codes

* 100+

### Safety SOPs

* 75+

### Maintenance Logs

* 5000+

### Incident Reports

* 500+

### Failure Chains

* 300+

### Configuration Profiles

* 300+

### OCR Benchmark Images

* Hundreds of synthetic panel displays
* Equipment nameplates
* Metadata annotations

---

# 📁 Project Structure

```
Fault-Graph/
│
├── app.py
├── requirements.txt
├── README.md
├── DATASET_REPORT.md
│
├── scripts/
│   └── generate_dataset.py
│
├── src/
│   ├── analytics.py
│   ├── prediction.py
│   ├── explainability.py
│   ├── data_integration.py
│   ├── graph_builder.py
│   ├── pipeline.py
│   ├── vector_store.py
│   └── ocr_parser.py
│
├── tests/
│   ├── test_dataset_expansion.py
│   └── test_data_integration.py
│
└── data/
    ├── knowledge_base/
    ├── configurations/
    ├── failure_chains/
    ├── incident_reports/
    ├── logs/
    ├── ocr_images/
    └── chroma_db/
```

---

# 🖥 Dashboard Modules

## ⚡ Diagnostic Hub

* Image upload
* OCR parsing
* Manual fault lookup
* Knowledge graph traversal
* Semantic RAG retrieval
* AI-generated repair guide
* Technician feedback

---

## 🕸 Knowledge Graph Explorer

* Interactive graph visualization
* Node filtering
* Asset exploration
* Failure propagation
* Component relationships

---

## 📊 Maintenance Intelligence

* 5000+ maintenance logs
* Incident analytics
* Search and filtering
* Failure history

---

## 📈 Predictive Maintenance

* Risk estimation
* Failure trends
* Remaining useful life
* Maintenance scheduling

---

## 🧠 Explainability Dashboard

Displays

* Root cause reasoning
* Evidence chain
* Knowledge graph traversal
* Retrieved documents
* Confidence scores

---

# 🤖 Supported LLM Providers

| Provider            | Model            |
| ------------------- | ---------------- |
| OpenAI              | GPT-4o Mini      |
| Google              | Gemini 1.5 Flash |
| Anthropic           | Claude 3 Haiku   |
| Local Template Mode | No API Required  |

---

# 🛠 Tech Stack

### Backend

* Python
* LangChain
* ChromaDB
* NetworkX
* Sentence Transformers

### AI

* Graph-RAG
* Knowledge Graphs
* OCR
* Explainable AI
* Predictive Analytics

### Frontend

* Streamlit
* Streamlit-Agraph

### OCR

* EasyOCR
* Tesseract

---

# 📈 Roadmap

* Industrial Vision-Language Models
* Live IoT sensor integration
* Real-time fault streaming
* Digital Twin simulation
* Multi-agent maintenance planning
* Cloud deployment
* Docker & Kubernetes
* REST API
* Mobile-responsive dashboard

---

# ⭐ Why Fault-Graph AI?

Unlike traditional RAG systems, Fault-Graph AI combines:

* **Knowledge Graph reasoning** for deterministic safety-critical retrieval.
* **Semantic RAG** for contextual document search.
* **Explainable AI** for transparent diagnostics.
* **Predictive analytics** for proactive maintenance.
* **Industrial OCR** for image-based fault detection.
* **Enterprise-scale synthetic datasets** for realistic evaluation.

This hybrid approach delivers a production-oriented diagnostic platform suitable for industrial HVAC maintenance, technical support, and predictive asset management.

---

This version is significantly stronger than the original README and better reflects the current state of your project. It also presents the project in a way that's more compelling for hackathon judges and recruiters reviewing your GitHub repository.
