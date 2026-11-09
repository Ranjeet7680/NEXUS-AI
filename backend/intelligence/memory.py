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
            },
            {
                "topic": "FinTech AML & Fraud Velocity",
                "content": "Transaction velocity exceeding 5 actions/hour with risk score > 0.70 triggers mandatory AML hold and Tier-2 HITL compliance review under FinCEN & BSA guidelines.",
                "tags": ["fintech", "fraud", "aml", "compliance", "banking"]
            },
            {
                "topic": "Supply Chain Port Dwell SLA",
                "content": "Port container dwell time exceeding 72 hours triggers demurrage penalties and rail corridor rerouting to avoid supply chain cascade failures.",
                "tags": ["supply_chain", "logistics", "freight", "port", "reroute"]
            },
            {
                "topic": "Cyber Incident CVSS Severity",
                "content": "CVSS scores >= 8.5 on production endpoints mandate automated session invalidation, pod isolation, and SOC Tier-3 incident response escalation within 15 minutes.",
                "tags": ["cybersecurity", "threat", "mitre", "soc", "infosec"]
            },
            {
                "topic": "Net Dollar Retention (NDR) Targets",
                "content": "Best-in-class enterprise SaaS NDR exceeds 110%. NDR below 95% indicates scale contraction, requiring immediate customer success executive intervention.",
                "tags": ["saas", "mrr", "ndr", "retention", "expansion"]
            },
            {
                "topic": "Clinical Trial P-Value Significance",
                "content": "FDA Phase III efficacy requires two-tailed p-value < 0.01 with retention rate > 90%. Severe adverse event rates > 5% require Data Safety Monitoring Board (DSMB) review.",
                "tags": ["clinical", "pharma", "fda", "trials", "efficacy"]
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
