from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter(prefix="/api/v1/agents", tags=["Agents"])

AGENTS_METADATA = [
    {
        "id": "planner",
        "name": "Planner Agent",
        "role": "Strategic Task Decomposition",
        "capabilities": ["Goal Parsing", "DAG Generation", "Agent Routing"],
        "status": "ready",
        "model": "gemini-1.5-flash / nexus-hybrid",
        "avatar": "brain"
    },
    {
        "id": "document",
        "name": "Document Agent",
        "role": "Data Ingestion & Schema Extraction",
        "capabilities": ["CSV/PDF Parsing", "Schema Validation", "Format Normalization"],
        "status": "ready",
        "model": "nexus-parser-v2",
        "avatar": "file-text"
    },
    {
        "id": "research",
        "name": "Research Agent",
        "role": "Semantic Context & Market Benchmarks",
        "capabilities": ["Vector Search", "Benchmark Retrieval", "Domain Grounding"],
        "status": "ready",
        "model": "text-embedding-004 + gemini",
        "avatar": "search"
    },
    {
        "id": "analyst",
        "name": "Data Analyst Agent",
        "role": "Statistical & Financial Calculation",
        "capabilities": ["Variance Analysis", "KPI Aggregation", "Deficit Diagnosis"],
        "status": "ready",
        "model": "nexus-math-core",
        "avatar": "bar-chart-2"
    },
    {
        "id": "decision",
        "name": "Decision Agent",
        "role": "Synthesis & Strategic Recommendations",
        "capabilities": ["Risk Scoring", "Root-Cause Analysis", "Mitigation Roadmap"],
        "status": "ready",
        "model": "gemini-1.5-pro / gpt-4o",
        "avatar": "compass"
    },
    {
        "id": "quality",
        "name": "Quality Agent",
        "role": "Independent Audit & Verification",
        "capabilities": ["Math Reconciliation", "Hallucination Check", "Confidence Scoring"],
        "status": "ready",
        "model": "nexus-guardrail-v1",
        "avatar": "check-circle"
    },
    {
        "id": "workflow",
        "name": "Workflow Agent",
        "role": "Action Execution & Human Governance",
        "capabilities": ["Executive Deliverables", "Tool Integration", "Approval Gatekeeping"],
        "status": "ready",
        "model": "nexus-orchestrator",
        "avatar": "zap"
    }
]

@router.get("")
def list_agents() -> List[Dict[str, Any]]:
    return AGENTS_METADATA
