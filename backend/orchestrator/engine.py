import asyncio
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from backend.models import TaskModel, AgentExecutionModel, ApprovalModel, AuditLogModel
from backend.database import SessionLocal
from backend.agents.planner_agent import planner_agent
from backend.agents.document_agent import document_agent
from backend.agents.research_agent import research_agent
from backend.agents.analyst_agent import analyst_agent
from backend.agents.decision_agent import decision_agent
from backend.agents.quality_agent import quality_agent
from backend.agents.workflow_agent import workflow_agent
from backend.integrations.tool_sandbox import tool_gateway

class OrchestratorEngine:
    """
    Stateful Multi-Agent Orchestrator (LangGraph Pattern).
    Executes collaborative agents, handles checkpointing, coordinates human approval,
    and streams real-time telemetry via event queues.
    """

    def __init__(self):
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.event_queues: Dict[str, asyncio.Queue] = {}
        self.subscribers: Dict[str, List[asyncio.Queue]] = {}

    def get_or_create_queue(self, task_id: str) -> asyncio.Queue:
        if task_id not in self.event_queues:
            self.event_queues[task_id] = asyncio.Queue()
        return self.event_queues[task_id]

    def register_subscriber(self, task_id: str, queue: asyncio.Queue):
        if task_id not in self.subscribers:
            self.subscribers[task_id] = []
        self.subscribers[task_id].append(queue)

    def unregister_subscriber(self, task_id: str, queue: asyncio.Queue):
        if task_id in self.subscribers and queue in self.subscribers[task_id]:
            self.subscribers[task_id].remove(queue)

    async def emit_event(self, task_id: str, agent: str, phase: str, message: str, payload: Optional[Dict[str, Any]] = None, confidence: float = 1.0, tokens: int = 0, latency_ms: int = 0):
        event = {
            "task_id": task_id,
            "agent": agent,
            "phase": phase,
            "message": message,
            "payload": payload or {},
            "confidence": confidence,
            "tokens": tokens,
            "latency_ms": latency_ms,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        # Put on legacy queue for backwards compatibility
        queue = self.get_or_create_queue(task_id)
        await queue.put(event)

        # Fan-out to active SSE subscribers
        for sub_q in list(self.subscribers.get(task_id, [])):
            try:
                sub_q.put_nowait(event)
            except Exception:
                pass

        # Update in-memory state
        if task_id in self.active_tasks:
            self.active_tasks[task_id]["events"].append(event)
            self.active_tasks[task_id]["total_tokens"] += tokens
            self.active_tasks[task_id]["total_latency_ms"] += latency_ms

        # Persist execution record in DB
        db = SessionLocal()
        try:
            exec_rec = AgentExecutionModel(
                id=str(uuid.uuid4()),
                task_id=task_id,
                agent_name=agent,
                phase=phase,
                message=message,
                payload=payload or {},
                confidence_score=confidence,
                tokens_consumed=tokens,
                latency_ms=latency_ms
            )
            db.add(exec_rec)
            db.commit()
        except Exception as e:
            print(f"[Orchestrator DB Error] {e}")
        finally:
            db.close()

    async def run_pipeline(self, task_id: str, prompt: str, dataset_name: str, require_approval: bool = True):
        start_time = time.time()
        self.active_tasks[task_id] = {
            "task_id": task_id,
            "prompt": prompt,
            "dataset_name": dataset_name,
            "status": "in_progress",
            "events": [],
            "total_tokens": 0,
            "total_latency_ms": 0,
            "require_approval": require_approval,
            "pending_approval": None,
            "final_output": None
        }

        async def callback(agent, phase, message, payload=None, confidence=1.0, tokens=0, latency_ms=0):
            await self.emit_event(task_id, agent, phase, message, payload, confidence, tokens, latency_ms)

        try:
            # 1. PLANNER AGENT
            plan_res = await planner_agent.execute(prompt, dataset_name, callback)
            self.active_tasks[task_id]["plan"] = plan_res["plan"]
            domain = plan_res.get("domain", "General Enterprise")

            # 2. DOCUMENT AGENT (Data Ingestion)
            dataset_path = os.path.join(os.path.dirname(__file__), "..", "data", dataset_name)
            if not os.path.exists(dataset_path) and os.path.exists(os.path.join("/tmp/data", dataset_name)):
                dataset_path = os.path.join("/tmp/data", dataset_name)
            doc_res = await document_agent.execute(dataset_path, callback)
            self.active_tasks[task_id]["doc_data"] = doc_res

            # 3. RESEARCH AGENT (Context & Benchmarks)
            research_res = await research_agent.execute(domain, callback)
            self.active_tasks[task_id]["research_data"] = research_res

            # 4. DATA ANALYST AGENT (Quantitative & Statistical Analysis)
            analyst_res = await analyst_agent.execute(doc_res, domain, callback)
            self.active_tasks[task_id]["analyst_data"] = analyst_res

            # 5. DECISION AGENT (Synthesis & Strategic Recommendations)
            decision_res = await decision_agent.execute(analyst_res, research_res, domain, callback)
            self.active_tasks[task_id]["decision_data"] = decision_res

            # 6. QUALITY & EVALUATOR AGENT (Verification & Grounding Check)
            quality_res = await quality_agent.execute(analyst_res, decision_res, callback)
            self.active_tasks[task_id]["quality_data"] = quality_res

            # 7. WORKFLOW AGENT (Deliverables & Action Planning)
            workflow_res = await workflow_agent.execute(
                task_id, decision_res, analyst_res, quality_res, require_approval, domain, callback
            )
            self.active_tasks[task_id]["workflow_data"] = workflow_res

            # Check if Human Approval is needed
            if require_approval and workflow_res.get("action", {}).get("requires_human_approval"):
                self.active_tasks[task_id]["status"] = "awaiting_approval"
                self.active_tasks[task_id]["pending_approval"] = workflow_res["action"]

                # Create approval record in DB
                db = SessionLocal()
                try:
                    approval_rec = ApprovalModel(
                        id=task_id,
                        task_id=task_id,
                        action_type=workflow_res["action"]["action_type"],
                        recipient=workflow_res["action"].get("recipient"),
                        subject=workflow_res["action"].get("subject"),
                        preview_content=workflow_res["action"].get("body", ""),
                        status="pending"
                    )
                    task_rec = db.query(TaskModel).filter(TaskModel.id == task_id).first()
                    if task_rec:
                        task_rec.status = "awaiting_approval"
                    db.add(approval_rec)
                    db.commit()
                finally:
                    db.close()
                return

            # If no approval needed, complete immediately
            await self._complete_task(task_id, workflow_res)

        except Exception as e:
            self.active_tasks[task_id]["status"] = "failed"
            await self.emit_event(task_id, "Orchestrator", "error", f"Execution error: {str(e)}")
            db = SessionLocal()
            try:
                task_rec = db.query(TaskModel).filter(TaskModel.id == task_id).first()
                if task_rec:
                    task_rec.status = "failed"
                    db.commit()
            finally:
                db.close()

    async def resume_with_approval(self, task_id: str, decision: str, notes: str = ""):
        """
        Resumes the paused state machine once the human operator provides decision.
        """
        task_info = self.active_tasks.get(task_id)
        if not task_info:
            return {"error": "Task not found in active memory"}

        db = SessionLocal()
        try:
            approval_rec = db.query(ApprovalModel).filter(ApprovalModel.task_id == task_id).first()
            if approval_rec:
                approval_rec.status = "approved" if decision == "approve" else "rejected"
                approval_rec.reviewer_notes = notes
                approval_rec.reviewed_at = datetime.now(timezone.utc)
            db.commit()
        finally:
            db.close()

        if decision == "approve":
            await self.emit_event(
                task_id=task_id,
                agent="Human Approval Gateway",
                phase="resumed",
                message=f"Human operator APPROVED sensitive action. Executing external dispatch via sandbox gateway.",
                payload={"reviewer_notes": notes}
            )

            # Execute tool action
            pending = task_info.get("pending_approval", {})
            action_result = tool_gateway.execute_action(pending.get("action_type", ""), pending)

            await self.emit_event(
                task_id=task_id,
                agent="Tool Execution Sandbox",
                phase="action_dispatched",
                message=f"Action '{pending.get('action_type')}' successfully dispatched. Message ID: {action_result.get('message_id', 'ACK')}",
                payload={"result": action_result}
            )

            # Complete task
            await self._complete_task(task_id, task_info.get("workflow_data", {}))
        else:
            task_info["status"] = "rejected"
            await self.emit_event(
                task_id=task_id,
                agent="Human Approval Gateway",
                phase="rejected",
                message=f"Human operator REJECTED action. Reason: '{notes}'. Halting external dispatch.",
                payload={"reviewer_notes": notes}
            )

            db = SessionLocal()
            try:
                task_rec = db.query(TaskModel).filter(TaskModel.id == task_id).first()
                if task_rec:
                    task_rec.status = "rejected"
                    db.commit()
            finally:
                db.close()

    async def _complete_task(self, task_id: str, workflow_data: Dict[str, Any]):
        task_info = self.active_tasks[task_id]
        task_info["status"] = "completed"
        final_deliverable = {
            "management_report": workflow_data.get("report", {}),
            "summary": "Multi-agent autonomous collaboration successfully completed with verified outputs.",
            "total_tokens": task_info["total_tokens"],
            "total_latency_ms": task_info["total_latency_ms"]
        }
        task_info["final_output"] = final_deliverable

        await self.emit_event(
            task_id=task_id,
            agent="Orchestrator",
            phase="completed",
            message="Autonomous mission completed. Management report, risk matrix, and action audit generated.",
            payload=final_deliverable,
            confidence=0.99
        )

        db = SessionLocal()
        try:
            task_rec = db.query(TaskModel).filter(TaskModel.id == task_id).first()
            if task_rec:
                task_rec.status = "completed"
                task_rec.final_output = final_deliverable
                task_rec.total_tokens = task_info["total_tokens"]
                task_rec.total_latency_ms = task_info["total_latency_ms"]
                db.commit()
        finally:
            db.close()

orchestrator = OrchestratorEngine()
