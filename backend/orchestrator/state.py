from typing import TypedDict, List, Dict, Any, Optional

class AgentEventDict(TypedDict):
    agent: str
    phase: str  # start, thinking, action, done, approval_needed, completed
    message: str
    confidence: Optional[float]
    payload: Optional[Dict[str, Any]]
    tokens: Optional[int]
    latency_ms: Optional[int]
    timestamp: str

class TaskState(TypedDict):
    task_id: str
    prompt: str
    dataset_name: str
    status: str
    plan: List[Dict[str, Any]]
    events: List[AgentEventDict]
    doc_data: Optional[Dict[str, Any]]
    research_data: Optional[Dict[str, Any]]
    analyst_data: Optional[Dict[str, Any]]
    decision_data: Optional[Dict[str, Any]]
    quality_data: Optional[Dict[str, Any]]
    workflow_data: Optional[Dict[str, Any]]
    pending_approval: Optional[Dict[str, Any]]
    require_approval: bool
    total_tokens: int
    total_latency_ms: int
