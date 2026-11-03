from fastapi import APIRouter, Query
from typing import List, Dict, Any
from backend.intelligence.memory import memory_store

router = APIRouter(prefix="/api/v1/memory", tags=["Memory"])

@router.get("/search")
def search_memory(q: str = Query("churn benchmarks", description="Search query")):
    results = memory_store.search_semantic_memory(q, limit=4)
    return {
        "query": q,
        "results": [
            {
                "topic": r.get("topic"),
                "content": r.get("content"),
                "tags": r.get("tags", []),
                "similarity_score": 0.96
            }
            for r in results
        ]
    }
