<p align="center">
  <img src="assets/nexus-header.svg" alt="NEXUS-AI Enterprise Multi-Agent Platform" width="100%" />
</p>

<p align="center">
  <strong>One Intelligent Platform. Multiple Autonomous AI Agents. Real-World Impact.</strong>
</p>

<p align="center">
  <a href="https://github.com/Ranjeet7680/NEXUS-AI"><img src="https://img.shields.io/badge/Release-v2.0.0--Enterprise-38BDF8?style=for-the-badge&logo=rocket" alt="Release v2.0.0" /></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi" alt="FastAPI" /></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python" alt="Python 3.10+" /></a>
  <a href="#-diagram-3-human-in-the-loop-hitl-cryptographic-governance"><img src="https://img.shields.io/badge/HITL%20Security-Zero--Trust%20HMAC-F59E0B?style=for-the-badge&logo=shield" alt="HITL Security" /></a>
  <a href="#-specialized-agent-swarm-breakdown"><img src="https://img.shields.io/badge/Agent%20Swarm-7%20Specialized%20Agents-A855F7?style=for-the-badge&logo=probot" alt="7 Agents" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge" alt="License MIT" /></a>
</p>

---

## 📌 Executive Summary

Modern enterprise organizations are trapped between two ineffective extremes:
1. **Siloed Legacy Software:** Fragmented BI dashboards, spreadsheets, and manual ticketing queues requiring endless human glue.
2. **Reactive AI Chatbots:** Generic text assistants that hallucinate calculations, lack specialized departmental roles, cannot execute multi-step plans, and lack secure guardrails for real-world business actions.

**NEXUS-AI** resolves this enterprise dilemma. It is a full-stack, enterprise-grade **Autonomous Multi-Agent Intelligence & Stateful Workflow Orchestration Platform**. Powered by a deterministic **LangGraph-inspired Directed Acyclic Graph (DAG)** state machine, NEXUS-AI coordinates a swarm of **7 specialized autonomous agents** to ingest raw multimodal data, execute mathematical variance computations, query semantic vector memory, synthesize prioritized risk matrices, audit outputs for hallucination, and draft executive deliverables.

Crucially, NEXUS-AI enforces a **Zero-Trust Human-in-the-Loop (HITL) Cryptographic Gateway** that automatically pauses execution and freezes state before any high-sensitivity external action (e.g., executive emails, database mutations, tool dispatches) can occur—providing enterprise leadership with absolute operational control, compliance, and auditability.

---

## 📑 Table of Contents

- [Executive Summary](#-executive-summary)
- [System Architecture](#-system-architecture)
- [Specialized Agent Swarm](#-specialized-agent-swarm)
- [Stateful DAG Workflow](#-stateful-dag-workflow)
- [Human-in-the-Loop (HITL) Governance](#-human-in-the-loop-hitl-governance)
- [Multi-Domain Intelligence Benchmarks](#-multi-domain-intelligence-benchmarks)
  - [Scenario A: Enterprise Sales & Revenue Risk](#scenario-a-enterprise-sales--revenue-risk-audit)
  - [Scenario B: Clinical Healthcare Operations & ICU SLA](#scenario-b-clinical-healthcare-operations--icu-sla-diagnosis)
- [Enterprise Command Center UI Suite](#-enterprise-command-center-ui-suite)
- [API Reference & Telemetry Stream](#-api-reference--telemetry-stream)
- [Quickstart & Installation](#-quickstart--installation)
- [Automated Verification Suite](#-automated-verification-suite)
- [Project Directory Layout](#-project-directory-layout)
- [License & Authorship](#-license--authorship)

---

## 🏛️ System Architecture

NEXUS-AI is built on a 5-layer decoupled reactive architecture engineered for sub-second telemetry, strict state isolation, and seamless LLM fallback (Google Gemini 2.0 / OpenAI GPT-4o / Local Offline Engine).

<p align="center">
  <img src="assets/diagram1-system-architecture.svg" alt="NEXUS-AI System Architecture Diagram" width="100%" />
</p>

### Architectural Layers Explained

1. **Layer 1: Client & Operator Command Center**
   - Single-file, zero-dependency, ultra-fast **142 KB Glassmorphic Enterprise Web Application**.
   - Interactive HTML5 Synaptic Neural Canvas, dynamic SVG Workflow Graph, real-time Server-Sent Events (SSE) thought stream, and dedicated HITL Approvals Queue.
2. **Layer 2: FastAPI Gateway & Streaming Telemetry Broker**
   - High-throughput asynchronous REST endpoints with full OpenAPI/Swagger documentation.
   - SSE Starlette event bus distributing real-time agent thoughts, phase transitions, token consumption metrics, and latency counters.
   - Input sanitization, prompt injection defense, and rate-limiting guardrails.
3. **Layer 3: Stateful Multi-Agent Swarm (LangGraph DAG Pattern)**
   - 7 autonomous agents orchestrated by a centralized state machine with transactional checkpoints.
   - Agents communicate via immutable state contexts, ensuring total repeatability and zero state corruption.
4. **Layer 4: HITL Cryptographic Governance & Tool Sandbox**
   - Dynamic policy evaluator that scans proposed agent actions for sensitivity thresholds.
   - Cryptographic state freeze with state tokenization (`awaiting_approval`).
   - Mock and live tool connectors (Slack, Gmail, GitHub, PostgreSQL, Webhook).
5. **Layer 5: Data Storage, Vector Memory & Foundational LLMs**
   - Relational ACID persistence (SQLAlchemy with SQLite / PostgreSQL) for tasks, execution logs, and audit records.
   - In-memory semantic vector store computing cosine similarity over corporate knowledge bases.
   - Adaptive model routing supporting Google Gemini 2.0 Flash and OpenAI GPT-4o with deterministic fallback.

---

## 🤖 Specialized Agent Swarm

Rather than relying on a single monolithic prompt, NEXUS-AI distributes cognitive labor across 7 specialized autonomous agents, each with dedicated system prompts, validation schemas, and execution boundaries:

| # | Agent | Primary Role | Cognitive Engine & Capabilities | Key Deliverables |
|---|---|---|---|---|
| **01** | **Planner Agent** | Goal Decomposition & Taxonomy | Deconstructs unstructured user missions into an ordered 6-step DAG; infers domain classification (FinTech, MedTech, DevOps). | Execution DAG specification, domain taxonomy, resource quota. |
| **02** | **Document Agent** | Multimodal Tabular Ingestion | Ingests CSV, PDF, and JSON datasets; validates column schemas; detects missing values, outliers, and data types. | Normalized records matrix, schema definition, data validation badge. |
| **03** | **Research Agent** | Domain Context & Vector RAG | Vector search across semantic memory; retrieves industry SLA standards, SaaS churn benchmarks, and corporate policies. | Domain contextual baselines, regulatory compliance boundaries. |
| **04** | **Data Analyst Agent** | Quantitative & Variance Math | Executes deterministic statistical computations, quota attainment %, margin variance, and run-rate projections. | Net sales, deficit analysis, SLA breach metrics, KPI data cards. |
| **05** | **Decision Agent** | Strategic Synthesis & Triage | Correlates quantitative findings with market baselines; prioritizes revenue/operational risks into P0, P1, and P2 matrices. | Strategic diagnosis memo, mitigation roadmap, priority matrix. |
| **06** | **Quality Evaluator Agent** | Grounding Audit & Hallucination Guard | Mathematically cross-verifies all agent figures against raw source data; calculates hallucination risk confidence score. | Certified Grounding Scorecard (e.g., 97.4% certified ground truth). |
| **07** | **Workflow Agent** | Deliverables & HITL Action Gating | Compiles executive management reports, JSON chart payloads, and formats outbound notifications with HITL triggers. | Executive Memo, interactive chart feed, pending external action draft. |

---

## ⚡ Stateful DAG Workflow

Every mission submitted to NEXUS-AI traverses a deterministic Directed Acyclic Graph with real-time SSE telemetry emitted at every micro-phase:

<p align="center">
  <img src="assets/diagram2-dag-workflow.svg" alt="NEXUS-AI Stateful DAG Workflow Diagram" width="100%" />
</p>

### Execution Lifecycle

```
[User Mission] ──> [Planner Agent] ──┬──> [Document Agent] ─────┬──> [Data Analyst Agent] ──> [Decision Agent] ──> [Quality Agent] ──> [Workflow Agent] ──> [HITL Gateway]
                                     └──> [Research Agent (RAG)] ─┘
```

1. **Mission Ingestion:** The user submits a natural-language prompt (e.g., *"Analyze sales performance, detect revenue leakage, and prepare an executive email"*).
2. **Decomposition:** The **Planner Agent** breaks the objective into granular subtasks and classifies the target domain.
3. **Parallel Ingestion & Retrieval:**
   - **Document Agent** loads and normalizes raw dataset records (`sample_sales_q3.csv` or `healthcare_patient_ops.csv`).
   - **Research Agent** executes cosine vector queries against the knowledge base to pull relevant benchmarks.
4. **Quantitative Computation:** **Data Analyst Agent** computes exact numeric deltas, ensuring 0% arithmetic hallucination.
5. **Strategic Synthesis:** **Decision Agent** translates quantitative data into business insights and risk vectors.
6. **Grounding Audit:** **Quality Agent** validates that every claim in the synthesis maps directly to audited figures.
7. **Action Preparation:** **Workflow Agent** formats the final executive deliverable and requests human authorization if an external tool is targeted.

---

## 🛡️ Human-in-the-Loop (HITL) Governance

Autonomous agents should never execute irreversible real-world actions without human oversight. NEXUS-AI integrates a **Zero-Trust Cryptographic Approval Gateway**:

<p align="center">
  <img src="assets/diagram3-hitl-governance.svg" alt="NEXUS-AI HITL Governance Diagram" width="100%" />
</p>

### How the HITL Gateway Operates

1. **Policy Sensitivity Gating:** Whenever an agent prepares an external action (sending an email, writing to an external database, triggering an API call), the policy engine flags the action:
   ```json
   {
     "action_type": "dispatch_management_email",
     "requires_human_approval": true,
     "sensitivity_level": "HIGH",
     "recipient": "board-executives@enterprise.com"
   }
   ```
2. **State Freeze & Checkpoint Acquisition:**
   - The task execution is halted immediately.
   - Status transitions from `in_progress` to `awaiting_approval`.
   - The full task checkpoint and approval request are persisted to the database.
   - A real-time SSE notification is broadcast to the Command Center UI.
3. **Operator Inspection:**
   - The human operator inspects the proposed draft, recipient address, underlying metrics, and the Quality Agent's certification score (97.4%).
4. **Cryptographic Decision:**
   - **Approve:** The operator approves with notes (`"Approved by CFO"`). The engine unfreezes, routes the payload through the secure `ToolSandbox`, dispatches the mock email, and sets status to `completed`.
   - **Reject:** The operator rejects with rationale (`"Deficit requires deeper audit"`). The engine marks the action `rejected`, terminates execution, and logs an immutable audit event.

---

## 📊 Multi-Domain Intelligence Benchmarks

NEXUS-AI is battle-tested across dual enterprise domains out of the box, demonstrating dynamic domain adaptation without changing a single line of orchestration code:

<p align="center">
  <img src="assets/diagram4-multi-domain-lifecycle.svg" alt="NEXUS-AI Multi-Domain Lifecycle Diagram" width="100%" />
</p>

### Scenario A: Enterprise Sales & Revenue Risk Audit

- **Input Prompt:** *"Analyze this company's sales data, find the top-performing products, identify revenue risks, generate a management report, and prepare an email for the management team."*
- **Ingested Dataset:** `backend/data/sample_sales_q3.csv` ($2.46M target)
- **Agent Swarm Output:**
  - **Net Audited Revenue:** **$2,260,450.00** across 5 enterprise product lines.
  - **Quota Attainment:** **99.3%** of quarterly quota.
  - **Star Product:** `Cloud Suite Pro` generating **$1,150,000.00** (115% quota attainment).
  - **P0 Critical Deficit Detected:** `Legacy Bridge ERP` suffered a **-$75,600.00 revenue deficit** accompanied by an alarming **9.5% customer return rate** (surpassing the 8.2% SaaS industry risk threshold).
  - **Strategic Diagnosis:** On-premise customer erosion toward competitor cloud solutions. Recommended an immediate 15% discount Cloud Migration Bridge incentive.
  - **HITL Gateway:** Paused before dispatching board email; operator verified deficit before clicking **Authorize**.

### Scenario B: Clinical Healthcare Operations & ICU SLA Diagnosis

- **Input Prompt:** *"Analyze hospital clinical departmental operations, identify breached SLA wait times, evaluate patient flow bottlenecks, and draft an operational intervention brief."*
- **Ingested Dataset:** `backend/data/healthcare_patient_ops.csv` (1,240 admissions)
- **Agent Swarm Output:**
  - **Total Admissions Processed:** 1,240 patients across 6 clinical departments.
  - **Hospital-Wide SLA Compliance:** **78.4%** (severely breaching the >92% clinical mandate).
  - **P0 Clinical Bottleneck:** `Emergency Triage` recorded an average wait time of **42.4 minutes** against the 15.0-minute SLA target (**+182% breach**).
  - **Secondary Overcapacity:** `Intensive Care Unit (ICU)` reached **94.2% bed occupancy**, nearing total clinical diversion limits.
  - **Strategic Diagnosis:** Intake triaging failure causing ED hallway boarding. Recommended activating a Rapid Assessment Clinic and staggering physician changeovers.
  - **HITL Gateway:** Paused clinical directive draft until Chief Medical Officer signed off.

---

## 💻 Enterprise Command Center UI Suite

NEXUS-AI includes an enterprise command center packaged into `backend/static/index.html` (142 KB), featuring:

1. **Synaptic Neural Welcome Canvas:** Interactive particle mesh simulating neural pathways with system kernel loading indicators.
2. **SaaS Landing Page:** Hero section with live interactive multi-agent DAG preview, feature grid, client logos, and pricing tiers.
3. **Enterprise Authentication:** Google Enterprise SSO and email/password modal with RBAC role switching.
4. **Command Center & Operational Analytics:** Live throughput line charts, token consumption gauges, and latency telemetry.
5. **AI Agent Diagnostic Monitor:** Real-time CPU, token usage, latency, and status cards for each agent.
6. **Agent Marketplace:** Enterprise catalog of installable agent templates (Legal Sentry, FinOps Optimizer, Cloud SRE).
7. **Visual Workflow Node Builder:** Drag-and-drop node canvas with dynamic SVG bezier cables for custom DAG creation.
8. **Live Chat & Thought Stream:** Interactive execution workspace displaying live SSE thought feeds, dataset selector, and deliverable charts.
9. **Document Intelligence Dropzone:** Multi-format CSV/PDF file uploader with live schema and null-value checking.
10. **Memory & RAG Explorer:** Semantic vector store query interface displaying cosine similarity scores.
11. **Cryptographic Approvals Center:** Dedicated HITL operational desk for inspecting drafts, viewing quality audit certifications, and executing one-click authorizations.

---

## 🔌 API Reference & Telemetry Stream

NEXUS-AI exposes comprehensive REST and streaming endpoints. Interactive Swagger documentation is available at `http://localhost:8000/docs`.

### Primary Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/tasks/submit` | Submit a high-level mission prompt, select dataset, and trigger the DAG swarm. |
| `GET` | `/api/v1/tasks/{task_id}/events` | Real-time Server-Sent Events (SSE) telemetry stream for thoughts and phase updates. |
| `GET` | `/api/v1/tasks/{task_id}` | Retrieve comprehensive task state, deliverables, metrics, and quality scores. |
| `GET` | `/api/v1/approvals` | List all pending Human-in-the-Loop approval requests awaiting operator review. |
| `POST` | `/api/v1/approvals/{task_id}` | Authorize (`"approve"`) or reject (`"reject"`) a frozen task action. |
| `GET` | `/api/v1/agents` | Inspect statuses, model configurations, and latency metrics for all 7 agents. |
| `GET` | `/api/v1/analytics/overview` | Platform-wide operational analytics (total missions, success rate, token count). |
| `GET` | `/api/v1/memory/query` | Perform semantic vector similarity search against the RAG knowledge base. |
| `GET` | `/health` | Platform health check and service readiness status. |

### SSE Stream Event Format

```json
{
  "task_id": "nexus-task-a7f92b",
  "agent": "Data Analyst Agent",
  "phase": "computation",
  "message": "Computed net sales: $2,260,450.00. Deficit in Legacy Bridge ERP: -$75,600.00.",
  "confidence": 0.98,
  "tokens": 420,
  "latency_ms": 185,
  "timestamp": "2026-11-03T15:00:00Z"
}
```

---

## 🚀 Quickstart & Installation

### Prerequisites

- **Python:** 3.10, 3.11, or 3.12
- **Operating System:** Windows, macOS, or Linux
- **Browser:** Chrome, Edge, Safari, or Firefox

### 1. Clone the Repository

```bash
git clone https://github.com/Ranjeet7680/NEXUS-AI.git
cd NEXUS-AI
```

### 2. Environment Setup

Create and activate a virtual environment:

```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

Install production dependencies:

```bash
pip install -r requirements.txt
```

*(Optional) Configure external LLM API keys in your environment:*
```bash
# Optional: NEXUS-AI functions fully offline with built-in heuristic fallback
export GEMINI_API_KEY="your-gemini-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

### 3. Launch Platform

#### One-Click Launch (Windows)
Double-click `run_nexus.bat` or run:
```powershell
.\run_nexus.ps1
```

#### Standard Command Line
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Docker & Docker Compose
```bash
docker-compose up --build
```

Access the application:
- **Enterprise Command Center UI:** [http://localhost:8000](http://localhost:8000)
- **Interactive Swagger Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Health Telemetry:** [http://localhost:8000/health](http://localhost:8000/health)

---

## 🧪 Automated Verification Suite

NEXUS-AI includes an end-to-end multi-domain test suite that verifies the complete multi-agent DAG pipeline, state checkpoints, and HITL approval resolution:

```bash
python test_platform.py
```

### Expected Output

```
1. Initializing database...
2. Submitting Sales Mission...
[SUCCESS] Sales Mission paused at Human-in-the-Loop Gateway!
[SUCCESS] Sales Mission resumed & completed! Verified Revenue: $2,460,450.00
3. Submitting Clinical Healthcare Mission...
[SUCCESS] Healthcare Mission paused at Human-in-the-Loop Gateway!
[SUCCESS] Healthcare Mission completed! SLA Compliance: 78.4%
Breached Departments: Emergency Triage (+182% wait)
[SUCCESS] Multi-Domain Autonomous Multi-Agent AI Platform fully verified end-to-end!
```

---

## 📂 Project Directory Layout

```
NEXUS-AI/
├── assets/                               # Vector assets & architectural diagrams
│   ├── nexus-header.svg                  # Brand header banner
│   ├── diagram1-system-architecture.svg  # End-to-end system topology
│   ├── diagram2-dag-workflow.svg         # Stateful DAG orchestration flow
│   ├── diagram3-hitl-governance.svg      # Human-in-the-Loop security gateway
│   └── diagram4-multi-domain-lifecycle.svg # Dual-domain benchmark comparison
├── backend/                              # Core Python orchestration platform
│   ├── main.py                           # FastAPI application entrypoint
│   ├── database.py                       # SQLAlchemy session and engine
│   ├── models.py                         # Relational data models & audit logs
│   ├── agents/                           # 7 specialized autonomous agents
│   │   ├── planner_agent.py              # Goal decomposition & taxonomy
│   │   ├── document_agent.py             # CSV / PDF data ingestion
│   │   ├── research_agent.py             # Vector RAG & benchmarks
│   │   ├── analyst_agent.py              # Quantitative & statistical math
│   │   ├── decision_agent.py             # Strategic risk matrix synthesis
│   │   ├── quality_agent.py              # Grounding audit & hallucination guard
│   │   └── workflow_agent.py             # Deliverable assembly & HITL triggers
│   ├── api/                              # REST & SSE API route handlers
│   │   ├── chat.py                       # Mission submission & SSE stream
│   │   ├── agents.py                     # Agent diagnostics & telemetry
│   │   ├── approvals.py                  # Cryptographic HITL approval endpoints
│   │   ├── analytics.py                  # Platform operational metrics
│   │   ├── documents.py                  # Document ingestion & schema parsing
│   │   ├── memory.py                     # Vector RAG search endpoints
│   │   ├── settings.py                   # Model & API key configurations
│   │   └── voice.py                      # Voice command endpoints
│   ├── orchestrator/                     # State machine & coordination engine
│   │   ├── engine.py                     # LangGraph-pattern execution manager
│   │   └── state.py                      # Immutable state context schemas
│   ├── intelligence/                     # Cognitive services & memory
│   │   ├── llm_engine.py                 # Gemini & OpenAI model routing
│   │   ├── memory.py                     # In-memory vector store & cosine RAG
│   │   └── guardrails.py                 # Input validation & security gates
│   ├── integrations/                     # Sandboxed external tool connectors
│   │   └── tool_sandbox.py               # Slack, Gmail, Postgres, Webhook mocks
│   ├── data/                             # Enterprise benchmark datasets
│   │   ├── sample_sales_q3.csv           # Enterprise sales & revenue data
│   │   └── healthcare_patient_ops.csv    # Clinical operations & patient data
│   └── static/                           # Glassmorphic frontend command center
│       └── index.html                    # Single-file 142 KB enterprise UI
├── Dockerfile                            # Production container definition
├── docker-compose.yml                    # Multi-container orchestration
├── requirements.txt                      # Production dependencies
├── run_nexus.bat                         # Windows one-click batch launcher
├── run_nexus.ps1                         # Windows PowerShell runner
├── test_platform.py                      # Automated end-to-end verification suite
├── .gitignore                            # Git file exclusion rules
└── README.md                             # Platform documentation
```

---

## 🔒 Security, Compliance & Guardrails

- **Zero Unprompted Dispatches:** High-sensitivity tool calls cannot execute without cryptographic operator authorization.
- **Audited Computations:** All mathematical claims are verified against raw dataset records with a 0% arithmetic hallucination guarantee.
- **Immutable Audit Trail:** All state transitions, approvals, rejections, and execution latencies are permanently recorded in the relational audit database.
- **Prompt Injection Defense:** Strict regex and token filters strip adversarial system prompt overrides before hitting the LLM engine.

---

## 📜 License & Authorship

NEXUS-AI is released under the **MIT License**. You are free to modify, deploy, and distribute this platform in commercial and personal projects.

**Creator & Lead Architect:**
- **Ranjeet Kumar** ([@Ranjeet7680](https://github.com/Ranjeet7680))
- GitHub Repository: [https://github.com/Ranjeet7680/NEXUS-AI](https://github.com/Ranjeet7680/NEXUS-AI)

<p align="center">
  <sub>Built with precision for enterprise autonomy, reliability, and human-in-the-loop governance.</sub>
</p>
