import os
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.intelligence.llm_engine import llm_engine

router = APIRouter(prefix="/api/v1/settings", tags=["Settings"])

class KeyConfigPayload(BaseModel):
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

@router.get("/keys")
def get_key_status():
    has_gemini = bool(os.getenv("GEMINI_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "gemini_configured": has_gemini,
        "openai_configured": has_openai,
        "active_mode": llm_engine.mode,
        "governance": "RBAC + Zero-Trust Sandbox"
    }

@router.post("/keys")
def save_keys(payload: KeyConfigPayload):
    if payload.gemini_api_key and payload.gemini_api_key.strip():
        os.environ["GEMINI_API_KEY"] = payload.gemini_api_key.strip()
        llm_engine.gemini_key = payload.gemini_api_key.strip()
        llm_engine.mode = "gemini"

    if payload.openai_api_key and payload.openai_api_key.strip():
        os.environ["OPENAI_API_KEY"] = payload.openai_api_key.strip()
        llm_engine.openai_key = payload.openai_api_key.strip()
        if not llm_engine.gemini_key:
            llm_engine.mode = "openai"

    return {
        "status": "updated",
        "active_mode": llm_engine.mode,
        "message": "AI model credentials updated in runtime environment."
    }
