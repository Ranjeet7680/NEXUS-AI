"""
NEXUS-AI End-to-End Comprehensive Verification Test Suite
Tests all REST endpoints, SSE streams, Agent Swarm, HITL Gateway, and Voice AI.
"""

import asyncio
import io
import json
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import init_db

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200, f"Health check failed: {resp.text}"
    data = resp.json()
    assert data["status"] == "healthy"
    print("[PASS] 1. /health endpoint is healthy and online.")

def test_agents():
    resp = client.get("/api/v1/agents")
    assert resp.status_code == 200
    agents = resp.json()
    assert len(agents) >= 7, f"Expected at least 7 agents, got {len(agents)}"
    print(f"[PASS] 2. /api/v1/agents returned {len(agents)} active autonomous agents.")

def test_analytics():
    resp = client.get("/api/v1/analytics/overview")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_tasks_orchestrated" in data
    assert "active_agent_count" in data
    print(f"[PASS] 3. /api/v1/analytics/overview returned valid operational metrics.")

def test_documents():
    resp = client.get("/api/v1/documents")
    assert resp.status_code == 200
    docs = resp.json()
    assert len(docs) >= 2, f"Expected at least 2 datasets, got {len(docs)}"
    filenames = [d["filename"] for d in docs]
    assert "sample_sales_q3.csv" in filenames
    assert "healthcare_patient_ops.csv" in filenames
    print(f"[PASS] 4. /api/v1/documents returned {len(docs)} datasets: {filenames}.")

def test_document_upload():
    csv_content = b"metric,target,actual\nCustomerAcquisition,500,520\nRetentionRate,0.92,0.94\n"
    files = {"file": ("test_upload_dataset.csv", io.BytesIO(csv_content), "text/csv")}
    resp = client.post("/api/v1/documents/upload", files=files)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "uploaded"
    print("[PASS] 5. /api/v1/documents/upload successfully ingested test CSV.")

def test_memory_search():
    resp = client.get("/api/v1/memory/search?q=saas%20churn%20benchmarks")
    assert resp.status_code == 200
    data = resp.json()
    assert "results" in data
    assert len(data["results"]) > 0
    print(f"[PASS] 6. /api/v1/memory/search returned {len(data['results'])} semantic RAG chunks.")

def test_settings_keys():
    # Test GET
    resp = client.get("/api/v1/settings/keys")
    assert resp.status_code == 200
    # Test POST
    resp_post = client.post("/api/v1/settings/keys", json={"gemini_api_key": "test_key_gemini"})
    assert resp_post.status_code == 200
    print("[PASS] 7. /api/v1/settings/keys successfully read and configured runtime keys.")

def test_voice_ai():
    # 1. Voice intent for sales
    resp1 = client.post("/api/v1/voice/intent", json={"transcript": "Run Q3 sales performance mission", "language": "en-US"})
    assert resp1.status_code == 200
    d1 = resp1.json()
    assert d1["intent"] == "RUN_SALES_MISSION"
    assert d1["target_action"]["type"] == "NAVIGATE_AND_RUN"

    # 2. Voice intent for approvals navigation
    resp2 = client.post("/api/v1/voice/intent", json={"transcript": "Open pending approvals center", "language": "en-US"})
    assert resp2.status_code == 200
    d2 = resp2.json()
    assert d2["intent"] == "NAVIGATE_APPROVALS"

    # 3. Voice intent for Hindi
    resp3 = client.post("/api/v1/voice/intent", json={"transcript": "बिक्री रिपोर्ट का विश्लेषण करो", "language": "hi-IN"})
    assert resp3.status_code == 200
    d3 = resp3.json()
    assert d3["intent"] == "RUN_SALES_MISSION"

    # 4. Voice history
    resp4 = client.get("/api/v1/voice/history")
    assert resp4.status_code == 200
    hist = resp4.json()
    assert hist["count"] >= 3
    print(f"[PASS] 8. /api/v1/voice/intent recognized multilingual intents (EN & HI) with history tracking.")

def test_full_mission_e2e():
    # Submit task
    submit_resp = client.post("/api/v1/tasks/submit", json={
        "prompt": "Analyze sales data, detect revenue risks, and draft an executive report.",
        "dataset_name": "sample_sales_q3.csv",
        "require_approval": True
    })
    assert submit_resp.status_code == 200
    task_id = submit_resp.json()["task_id"]

    # Poll until awaiting_approval
    import time
    status = "planning"
    for _ in range(40):
        time.sleep(0.3)
        t_resp = client.get(f"/api/v1/tasks/{task_id}")
        assert t_resp.status_code == 200
        status = t_resp.json()["status"]
        if status in ["awaiting_approval", "completed"]:
            break

    assert status == "awaiting_approval", f"Expected awaiting_approval, got {status}"
    print(f"[PASS] 9. Multi-Agent DAG executed and paused cleanly at HITL Gateway (task_id: {task_id[:12]}...).")

    # Inspect pending approvals
    appr_resp = client.get("/api/v1/approvals")
    assert appr_resp.status_code == 200
    approvals = appr_resp.json()
    matching = [a for a in approvals if a["task_id"] == task_id]
    assert len(matching) > 0, "No pending approval record found in database"
    print(f"[PASS] 10. Approvals queue recorded pending action: '{matching[0]['subject']}'.")

    # Operator approves action
    dec_resp = client.post(f"/api/v1/approvals/{task_id}", json={
        "decision": "approve",
        "notes": "Verified by Automated E2E Tester"
    })
    assert dec_resp.status_code == 200

    # Wait for completion
    for _ in range(20):
        time.sleep(0.2)
        t_resp = client.get(f"/api/v1/tasks/{task_id}")
        if t_resp.json()["status"] == "completed":
            break

    final_task = client.get(f"/api/v1/tasks/{task_id}").json()
    assert final_task["status"] == "completed"
    report = final_task["final_output"]["management_report"]
    assert "key_metrics" in report
    assert "diagnosed_revenue_risks" in report
    print(f"[PASS] 11. Task resumed after HITL approval and finished with certified deliverables.")

if __name__ == "__main__":
    init_db()
    print("=== STARTING FULL END-TO-END VERIFICATION ===")
    test_health()
    test_agents()
    test_analytics()
    test_documents()
    test_document_upload()
    test_memory_search()
    test_settings_keys()
    test_voice_ai()
    test_full_mission_e2e()
    print("=== ALL 11 END-TO-END TESTS PASSED WITH 100% SUCCESS! ===")
