from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models import TaskModel, AgentExecutionModel, ApprovalModel
from backend.database import get_db

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])

@router.get("/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    total_tasks = db.query(TaskModel).count()
    completed_tasks = db.query(TaskModel).filter(TaskModel.status == "completed").count()
    awaiting_approvals = db.query(TaskModel).filter(TaskModel.status == "awaiting_approval").count()
    
    total_tokens = db.query(func.sum(TaskModel.total_tokens)).scalar() or 0
    total_latency = db.query(func.avg(TaskModel.total_latency_ms)).scalar() or 0

    success_rate = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 100.0

    return {
        "total_tasks_orchestrated": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_human_approvals": awaiting_approvals,
        "success_rate_pct": success_rate,
        "total_tokens_consumed": int(total_tokens),
        "avg_latency_ms": int(total_latency),
        "active_agent_count": 7,
        "governance_mode": "Strict RBAC + Human-in-the-Loop Gateway"
    }
