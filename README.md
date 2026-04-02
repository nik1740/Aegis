# Aegis — The Semantic Spend Orchestrator

> A decentralized Multi-Agent System anchored by **Graph-Based RAG (GraphRAG)** for deterministic policy enforcement, featuring autonomous negotiation protocols for resolving expense discrepancies without human intervention.

---

## 🏗️ Architecture

Aegis replaces linear OCR → rule-check pipelines with a **graph-traversal + adversarial multi-agent** architecture that structurally eliminates policy hallucinations.

### Core Components

| Layer | Service | Description |
|-------|---------|-------------|
| **Layer 1** | `gateway/` | FastAPI ingestion service — VLM extraction, Pydantic schemas, entity resolution |
| **Layer 2** | `knowledge_graph/` | Neo4j policy knowledge graph — Cypher traversal, graph construction |
| **Layer 3** | `agents/` | LangGraph multi-agent orchestration — Supervisor, Auditor, Fraud Detective, Compliance Judge |
| **Layer 4** | `agents/nodes/remediation.py` | Autonomous negotiation protocol with CRM validation |
| **ML** | `fraud_detection/` | Isolation Forest anomaly detection + CLIP image duplicate detection |
| **UI** | `dashboard/` | Streamlit finance manager dashboard |

### Tech Stack

- **Backend**: Python 3.11+ / FastAPI
- **Agent Orchestration**: LangGraph ^0.3
- **LLM Utilities**: LangChain ^0.3 (inside LangGraph nodes)
- **Graph DB**: Neo4j 5.x Community
- **Primary DB**: PostgreSQL 16
- **Vector Store**: ChromaDB ^0.5
- **Cache / Broker**: Redis 7
- **Task Queue**: Celery ^5.4
- **Dashboard**: Streamlit ^1.40
- **ML**: scikit-learn (Isolation Forest) + CLIP (image embeddings)
- **Observability**: LangSmith

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Poetry

### 1. Clone & Configure

```bash
git clone https://github.com/nik1740/Aegis.git
cd Aegis
cp .env.example .env
# Edit .env with your API keys
```

### 2. Start All Services

```bash
docker compose up --build
```

This starts:
- **Gateway API**: http://localhost:8000
- **Agent Server**: http://localhost:8100
- **Streamlit Dashboard**: http://localhost:8501
- **Neo4j Browser**: http://localhost:7474
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **ChromaDB**: localhost:8200

### 3. Seed Sample Data

```bash
poetry install
poetry run python scripts/seed_neo4j.py
poetry run python scripts/generate_test_data.py
```

### 4. Run Tests

```bash
poetry run pytest --cov
```

---

## 📁 Project Structure

```
aegis/
├── docker-compose.yml          # Full-stack deployment manifest
├── pyproject.toml              # Poetry dependency management
├── .env.example                # API keys template
├── README.md
│
├── gateway/                    # Layer 1 — FastAPI ingestion service
│   ├── Dockerfile
│   ├── main.py
│   ├── routes/
│   │   ├── expenses.py
│   │   └── webhooks.py
│   ├── extractors/
│   │   ├── vlm_extractor.py
│   │   ├── schemas.py
│   │   └── entity_resolver.py
│   └── tests/
│
├── knowledge_graph/            # Layer 2 — Neo4j policy graph
│   ├── Dockerfile
│   ├── policy_parser.py
│   ├── graph_builder.py
│   ├── graph_queries.py
│   ├── seed_data/
│   │   └── sample_policy.json
│   └── tests/
│
├── agents/                     # Layer 3 — LangGraph multi-agent system
│   ├── Dockerfile
│   ├── graph.py
│   ├── state.py
│   ├── server.py
│   ├── nodes/
│   │   ├── supervisor.py
│   │   ├── contextual_auditor.py
│   │   ├── fraud_detective.py
│   │   ├── compliance_judge.py
│   │   └── remediation.py
│   ├── tools/
│   │   ├── neo4j_tools.py
│   │   ├── crm_tools.py
│   │   └── notification.py
│   ├── prompts/
│   │   ├── auditor_system.md
│   │   ├── judge_system.md
│   │   └── remediation_system.md
│   └── tests/
│
├── fraud_detection/            # ML-based anomaly detection
│   ├── models/
│   │   ├── isolation_forest.py
│   │   └── image_embeddings.py
│   ├── training/
│   │   └── train_anomaly.py
│   └── tests/
│
├── dashboard/                  # Streamlit UI
│   ├── Dockerfile
│   ├── app.py
│   ├── pages/
│   │   ├── expense_review.py
│   │   ├── policy_explorer.py
│   │   └── audit_trail.py
│   └── components/
│       ├── receipt_viewer.py
│       └── graph_visualizer.py
│
├── scripts/
│   ├── init_db.sql
│   ├── seed_neo4j.py
│   └── generate_test_data.py
│
└── docs/
    ├── system_design.md
    ├── executive_summary.md
    ├── api_reference.md
    ├── security_architecture.md
    ├── fraud_detection_engine.md
    ├── testing_strategy.md
    └── operational_runbook.md
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/expenses/submit` | Submit a new expense (multipart) |
| `GET` | `/api/v1/expenses/:id` | Fetch expense record + decision |
| `GET` | `/api/v1/expenses` | List expenses with filters |
| `PATCH` | `/api/v1/expenses/:id` | Update expense metadata |
| `POST` | `/api/v1/expenses/:id/resubmit` | Resubmit after remediation |
| `GET` | `/api/v1/expenses/:id/trace` | Full audit trail |
| `GET` | `/api/v1/expenses/:id/policy` | Applied policy subgraph |
| `GET` | `/api/v1/health` | Liveness + readiness probe |

---

## 📝 License

Proprietary — Cymonic Technologies

---

*Aegis: Deterministic policy enforcement through graph-traversal + adversarial multi-agent architecture.*
