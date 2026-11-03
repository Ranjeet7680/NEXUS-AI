import math
from typing import List, Dict, Any, Optional

class MemoryStore:
    """
    Tiered memory architecture:
    1. Working Memory: Active task context
    2. Episodic Memory: Past task executions & decisions
    3. Semantic Memory & RAG: Domain knowledge retrieval using vector similarity
    """

    def __init__(self):
        self.working_memory: Dict[str, Any] = {}
        self.episodic_history: List[Dict[str, Any]] = []
        self.knowledge_base: List[Dict[str, Any]] = [
            {
                "topic": "SaaS Churn Benchmarks",
                "content": "Enterprise SaaS target churn rate is < 2% annually. Churn above 5% per quarter signals onboarding friction or critical product-market misalignment.",
                "tags": ["saas", "churn", "metrics", "finance"]
            },
            {
                "topic": "Revenue Risk Classification",
                "content": "Revenue shortfall exceeding 15% of quarterly forecast requires immediate executive escalation and operational realignment. Margin drops over 10% indicate excessive discounting.",
                "tags": ["revenue", "risk", "finance", "executive"]
            },
            {
                "topic": "Healthcare SLA Thresholds",
                "content": "Emergency department triage exceeding 20 minutes triggers immediate clinical surge protocol. ICU nurse-to-patient ratio must remain 2:1 or higher.",
                "tags": ["healthcare", "sla", "patient_safety"]
            },
            {
                "topic": "Approval Thresholds",
                "content": "Actions communicating outside company boundary (client emails, board memos, automated external tool dispatches) mandate Tier-1 Human Approval.",
                "tags": ["governance", "approval", "compliance"]
            }
        ]

    def add_episodic(self, task_id: str, summary: str, results: Dict[str, Any]):
        self.episodic_history.append({
            "task_id": task_id,
            "summary": summary,
            "results": results
        })

    def search_semantic_memory(self, query: str, limit: int = 2) -> List[Dict[str, Any]]:
        query_words = set(query.lower().split())
        scored = []
        for item in self.knowledge_base:
            doc_words = set(item["content"].lower().split()) | set(item["topic"].lower().split()) | set(item.get("tags", []))
            common = len(query_words.intersection(doc_words))
            score = common / (len(query_words) + 1)
            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in scored[:limit]]

memory_store = MemoryStore()
