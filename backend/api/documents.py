import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Any

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])
BASE_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def get_data_dir() -> str:
    if os.getenv("VERCEL"):
        tmp_dir = "/tmp/data"
        os.makedirs(tmp_dir, exist_ok=True)
        if os.path.exists(BASE_DATA_DIR):
            for fname in os.listdir(BASE_DATA_DIR):
                src = os.path.join(BASE_DATA_DIR, fname)
                dst = os.path.join(tmp_dir, fname)
                if os.path.isfile(src) and not os.path.exists(dst):
                    shutil.copy2(src, dst)
        return tmp_dir
    return BASE_DATA_DIR

@router.get("")
def list_datasets() -> List[Dict[str, Any]]:
    datasets = []
    data_dir = get_data_dir()
    if os.path.exists(data_dir):
        for f in os.listdir(data_dir):
            if f.endswith(".csv") or f.endswith(".json"):
                fpath = os.path.join(data_dir, f)
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

    data_dir = get_data_dir()
    target_path = os.path.join(data_dir, file.filename)
    with open(target_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "uploaded",
        "filename": file.filename,
        "path": target_path
    }
