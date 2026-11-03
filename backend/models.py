from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQLAlchemy ORM Models
class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(String(64), primary_key=True)
    title = Column(String(255), nullable=False)
    raw_prompt = Column(Text, nullable=False)
    dataset_name = Column(String(255), nullable=True)
    status = Column(String(50), default="pending")  # pending, planning, in_progress, awaiting_approval, completed, failed
    plan_dag = Column(JSON, default=list)
    final_output = Column(JSON, default=dict)
    total_tokens = Column(Integer, default=0)
    total_latency_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class AgentExecutionModel(Base):
    __tablename__ = "agent_executions"

    id = Column(String(64), primary_key=True)
    task_id = Column(String(64), nullable=False, index=True)
    agent_name = Column(String(100), nullable=False)
    step_number = Column(Integer, default=1)
    phase = Column(String(50), default="completed")
    message = Column(Text, nullable=True)
    payload = Column(JSON, default=dict)
    confidence_score = Column(Float, default=1.0)
    tokens_consumed = Column(Integer, default=0)
    latency_ms = Column(Integer, default=0)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ApprovalModel(Base):
    __tablename__ = "approvals"

    id = Column(String(64), primary_key=True)
    task_id = Column(String(64), nullable=False, index=True)
    action_type = Column(String(100), nullable=False)
    recipient = Column(String(255), nullable=True)
    subject = Column(String(500), nullable=True)
    preview_content = Column(Text, nullable=False)
    status = Column(String(50), default="pending")  # pending, approved, rejected
    reviewer_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    reviewed_at = Column(DateTime, nullable=True)

class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id = Column(String(64), primary_key=True)
    task_id = Column(String(64), nullable=True)
    actor = Column(String(100), nullable=False)
    action = Column(String(255), nullable=False)
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Pydantic Schemas for API
class TaskCreateRequest(BaseModel):
    prompt: str = Field(..., description="Goal or instruction for the multi-agent system")
    dataset_name: Optional[str] = Field("sample_sales_q3.csv", description="Dataset identifier")
    require_approval: bool = Field(True, description="Enforce human approval before sensitive actions")

class TaskStatusResponse(BaseModel):
    id: str
    title: str
    status: str
    plan_dag: List[Dict[str, Any]]
    final_output: Optional[Dict[str, Any]] = None
    total_tokens: int
    total_latency_ms: int
    created_at: str

class ApprovalDecisionRequest(BaseModel):
    decision: str = Field(..., pattern="^(approve|reject)$")
    notes: Optional[str] = Field("", description="Reviewer justification or comments")

class AgentEvent(BaseModel):
    task_id: str
    agent: str
    phase: str  # start, thinking, action, review, done, approval_needed, error
    message: str
    confidence: Optional[float] = 1.0
    payload: Optional[Dict[str, Any]] = None
    tokens: Optional[int] = 0
    latency_ms: Optional[int] = 0
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
