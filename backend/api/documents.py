import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

@router.get("")
def list_datasets() -> List[Dict[str, Any]]:
    datasets = []
    if os.path.exists(DATA_DIR):
        for f in os.listdir(DATA_DIR):
            if f.endswith(".csv") or f.endswith(".json"):
                fpath = os.path.join(DATA_DIR, f)
                datasets.append({
                    "filename": f,
                    "size_bytes": os.path.getsize(fpath),
                    "is_preset": f in ["sample_sales_q3.csv", "healthcare_patient_ops.csv"]
                })
    return datasets

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith((".csv", ".json", ".txt")):
        raise HTTPException(status_code=400, detail="Only CSV, JSON, and text datasets are supported for RAG ingestion.")

    target_path = os.path.join(DATA_DIR, file.filename)
    with open(target_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "uploaded",
        "filename": file.filename,
        "path": target_path
    }
