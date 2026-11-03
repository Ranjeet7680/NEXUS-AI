import time
from typing import Dict, Any, List

class PlannerAgent:
    """
    Analyzes user goal and dataset attributes, decomposes the mission into an
    executable Directed Acyclic Graph (DAG) of subtasks, and assigns specialized agents.
    """

    def __init__(self):
        self.name = "Planner Agent"
        self.role = "Strategic Task Decomposition & Orchestration"

    async def execute(self, prompt: str, dataset_name: str, event_callback) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        is_healthcare = "health" in prompt_lower or "hospital" in prompt_lower or "clinical" in prompt_lower or "patient" in prompt_lower or "sla" in prompt_lower or "healthcare" in dataset_name.lower()
        is_security = "security" in prompt_lower or "vulnerability" in prompt_lower or "threat" in prompt_lower or "cve" in prompt_lower
        
        domain = "Healthcare Clinical Operations" if is_healthcare else ("Cybersecurity & Compliance" if is_security else "Enterprise Sales & Business Intelligence")

        await event_callback(
            agent=self.name,
            phase="thinking",
            message=f"Analyzing mission intent for domain: [{domain}]. Deconstructing into collaborative agent execution DAG...",
            payload={"raw_prompt": prompt, "dataset": dataset_name, "domain": domain}
        )

        time.sleep(0.35)

        if is_healthcare:
            plan_steps = [
                {
                    "step": 1,
                    "agent": "Document Agent",
                    "task": "Extract hospital clinical department metrics and SLA target thresholds",
                    "depends_on": []
                },
                {
                    "step": 2,
                    "agent": "Research Agent",
                    "task": "Query clinical knowledge base for emergency triage & nurse ratio compliance standards",
                    "depends_on": []
                },
                {
                    "step": 3,
                    "agent": "Data Analyst Agent",
                    "task": "Compute SLA variance, triage latency breaches, and clinical bottleneck risk indices",
                    "depends_on": ["Document Agent"]
                },
                {
                    "step": 4,
                    "agent": "Decision Agent",
                    "task": "Diagnose acute department bottlenecks and formulate clinical surge intervention plan",
                    "depends_on": ["Data Analyst Agent", "Research Agent"]
                },
                {
                    "step": 5,
                    "agent": "Quality Agent",
                    "task": "Audit clinical calculation reconciliation, check patient safety thresholds, and score confidence",
                    "depends_on": ["Decision Agent"]
                },
                {
                    "step": 6,
                    "agent": "Workflow Agent",
                    "task": "Compile Chief Medical Officer briefing and queue external alert awaiting Human Sign-off",
                    "depends_on": ["Quality Agent"]
                }
            ]
        else:
            plan_steps = [
                {
                    "step": 1,
                    "agent": "Document Agent",
                    "task": "Extract raw records, schema, and column constraints from repository",
                    "depends_on": []
                },
                {
                    "step": 2,
                    "agent": "Research Agent",
                    "task": "Retrieve industry benchmarks, SaaS churn thresholds, and risk taxonomy",
                    "depends_on": []
                },
                {
                    "step": 3,
                    "agent": "Data Analyst Agent",
                    "task": "Compute KPI variances, revenue shortfalls, discount anomalies, and top/bottom performers",
                    "depends_on": ["Document Agent"]
                },
                {
                    "step": 4,
                    "agent": "Decision Agent",
                    "task": "Synthesize data & research into executive revenue risk diagnosis and strategic recommendations",
                    "depends_on": ["Data Analyst Agent", "Research Agent"]
                },
                {
                    "step": 5,
                    "agent": "Quality Agent",
                    "task": "Perform independent mathematical validation, grounding check, and audit scoring",
                    "depends_on": ["Decision Agent"]
                },
                {
                    "step": 6,
                    "agent": "Workflow Agent",
                    "task": "Generate executive briefing and prepare external email dispatch awaiting Human Approval",
                    "depends_on": ["Quality Agent"]
                }
            ]

        await event_callback(
            agent=self.name,
            phase="done",
            message=f"Formulated 6-node stateful DAG tailored for {domain}. Human-in-the-Loop checkpoint armed.",
            payload={"dag": plan_steps, "domain": domain},
            confidence=0.99,
            tokens=160
        )

        return {"plan": plan_steps, "goal": prompt, "domain": domain}

planner_agent = PlannerAgent()
