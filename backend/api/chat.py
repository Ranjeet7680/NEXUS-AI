import asyncio
import json
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend.models import TaskCreateRequest, TaskModel
from backend.database import get_db, SessionLocal
from backend.orchestrator.engine import orchestrator
from backend.intelligence.guardrails import guardrails

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])

@router.post("/submit")
async def submit_task(payload: TaskCreateRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # 1. Sanitize input with guardrails
    valid, message = guardrails.sanitize_input(payload.prompt)
    if not valid:
        raise HTTPException(status_code=400, detail=message)

    task_id = str(uuid.uuid4())
    dataset_name = payload.dataset_name or "sample_sales_q3.csv"

    # 2. Persist task record
    task_rec = TaskModel(
        id=task_id,
        title=payload.prompt[:80] + ("..." if len(payload.prompt) > 80 else ""),
        raw_prompt=payload.prompt,
        dataset_name=dataset_name,
        status="planning"
    )
    db.add(task_rec)
    db.commit()

    # 3. Schedule async orchestrator execution
    asyncio.create_task(
        orchestrator.run_pipeline(
            task_id=task_id,
            prompt=payload.prompt,
            dataset_name=dataset_name,
            require_approval=payload.require_approval
        )
    )

    return {
        "task_id": task_id,
        "status": "initiated",
        "dataset": dataset_name,
        "stream_url": f"/api/v1/tasks/{task_id}/events"
    }

@router.get("")
def list_tasks(limit: int = 20, db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).order_by(TaskModel.created_at.desc()).limit(limit).all()
    return [
        {
            "id": t.id,
            "title": t.title,
            "raw_prompt": t.raw_prompt,
            "dataset_name": t.dataset_name,
            "status": orchestrator.active_tasks.get(t.id, {}).get("status", t.status),
            "total_tokens": orchestrator.active_tasks.get(t.id, {}).get("total_tokens", t.total_tokens),
            "total_latency_ms": orchestrator.active_tasks.get(t.id, {}).get("total_latency_ms", t.total_latency_ms),
            "created_at": t.created_at.isoformat() if t.created_at else None
        }
        for t in tasks
    ]

@router.get("/{task_id}")
def get_task(task_id: str, db: Session = Depends(get_db)):
    task_rec = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task_rec:
        raise HTTPException(status_code=404, detail="Task not found")

    in_memory = orchestrator.active_tasks.get(task_id, {})
    return {
        "id": task_rec.id,
        "title": task_rec.title,
        "raw_prompt": task_rec.raw_prompt,
        "dataset_name": task_rec.dataset_name,
        "status": in_memory.get("status", task_rec.status),
        "plan": in_memory.get("plan", task_rec.plan_dag),
        "final_output": in_memory.get("final_output", task_rec.final_output),
        "total_tokens": in_memory.get("total_tokens", task_rec.total_tokens),
        "total_latency_ms": in_memory.get("total_latency_ms", task_rec.total_latency_ms),
        "pending_approval": in_memory.get("pending_approval")
    }

@router.get("/{task_id}/events")
async def stream_task_events(task_id: str):
    """
    Server-Sent Events (SSE) stream for real-time live agent updates.
    """
    sub_q = asyncio.Queue()

    # Preload past events already emitted for this task
    if task_id in orchestrator.active_tasks:
        for past_evt in list(orchestrator.active_tasks[task_id].get("events", [])):
            sub_q.put_nowait(past_evt)

    orchestrator.register_subscriber(task_id, sub_q)

    async def event_generator():
        try:
            while True:
                try:
                    event = await asyncio.wait_for(sub_q.get(), timeout=20.0)
                    yield f"data: {json.dumps(event)}\n\n"

                    # If task has completed or rejected, terminate stream after yielding final event
                    if event.get("phase") in ["completed", "rejected"]:
                        await asyncio.sleep(0.1)
                        break
                except asyncio.TimeoutError:
                    # Keep-alive heartbeat
                    yield f": keep-alive\n\n"
        finally:
            orchestrator.unregister_subscriber(task_id, sub_q)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
