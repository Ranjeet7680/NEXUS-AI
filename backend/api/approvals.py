from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import ApprovalDecisionRequest, ApprovalModel
from backend.database import get_db
from backend.orchestrator.engine import orchestrator

router = APIRouter(prefix="/api/v1/approvals", tags=["Approvals"])

@router.get("")
def list_approvals(status: str = None, db: Session = Depends(get_db)):
    query = db.query(ApprovalModel)
    if status:
        query = query.filter(ApprovalModel.status == status)
    approvals = query.order_by(ApprovalModel.created_at.desc()).limit(20).all()
    return [
        {
            "id": a.id,
            "task_id": a.task_id,
            "action_type": a.action_type,
            "recipient": a.recipient,
            "subject": a.subject,
            "preview_content": a.preview_content,
            "status": a.status,
            "created_at": a.created_at.isoformat() if a.created_at else None
        }
        for a in approvals
    ]

@router.get("/{task_id}")
def get_approval_status(task_id: str, db: Session = Depends(get_db)):
    approval = db.query(ApprovalModel).filter(ApprovalModel.task_id == task_id).first()
    if not approval:
        raise HTTPException(status_code=404, detail="No pending approval found for this task")
    return {
        "id": approval.id,
        "task_id": approval.task_id,
        "action_type": approval.action_type,
        "recipient": approval.recipient,
        "subject": approval.subject,
        "preview_content": approval.preview_content,
        "status": approval.status,
        "created_at": approval.created_at.isoformat() if approval.created_at else None
    }

@router.post("/{task_id}")
async def submit_approval_decision(task_id: str, payload: ApprovalDecisionRequest):
    result = await orchestrator.resume_with_approval(task_id, payload.decision, payload.notes or "")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return {
        "status": "success",
        "task_id": task_id,
        "decision": payload.decision,
        "message": f"Workflow resumed with decision: {payload.decision}"
    }
