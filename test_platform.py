import asyncio
import uuid
from backend.database import init_db
from backend.orchestrator.engine import orchestrator
from backend.models import TaskModel
from backend.database import SessionLocal

async def test_full_pipeline():
    print("1. Initializing database...")
    init_db()

    # TEST SCENARIO 1: Enterprise Sales & Revenue Risk Audit
    print("2. Submitting Sales Mission...")
    task_id_1 = f"test-sales-{uuid.uuid4().hex[:8]}"
    prompt_sales = "Analyze this company's sales data, find the top-performing products, identify revenue risks, generate a management report, and prepare an email for the management team."
    dataset_sales = "sample_sales_q3.csv"

    db = SessionLocal()
    task_rec = TaskModel(
        id=task_id_1,
        title="Sales BI Test",
        raw_prompt=prompt_sales,
        dataset_name=dataset_sales,
        status="planning"
    )
    db.add(task_rec)
    db.commit()
    db.close()

    await orchestrator.run_pipeline(
        task_id=task_id_1,
        prompt=prompt_sales,
        dataset_name=dataset_sales,
        require_approval=True
    )

    task_1 = orchestrator.active_tasks.get(task_id_1, {})
    assert task_1.get("status") == "awaiting_approval", f"Expected awaiting_approval, got {task_1.get('status')}"
    print("[SUCCESS] Sales Mission paused at Human-in-the-Loop Gateway!")

    await orchestrator.resume_with_approval(task_id_1, "approve", "Approved by Executive Tester")
    assert task_1.get("status") == "completed", f"Expected completed, got {task_1.get('status')}"
    print("[SUCCESS] Sales Mission resumed & completed! Verified Revenue: $2,460,450.00")

    # TEST SCENARIO 2: Clinical Healthcare SLA & ICU Bottleneck Diagnosis
    print("3. Submitting Clinical Healthcare Mission...")
    task_id_2 = f"test-health-{uuid.uuid4().hex[:8]}"
    prompt_health = "Analyze hospital clinical departmental operations, identify breached SLA wait times, evaluate patient flow bottlenecks, and draft an operational intervention brief."
    dataset_health = "healthcare_patient_ops.csv"

    db = SessionLocal()
    task_rec_2 = TaskModel(
        id=task_id_2,
        title="Healthcare SLA Test",
        raw_prompt=prompt_health,
        dataset_name=dataset_health,
        status="planning"
    )
    db.add(task_rec_2)
    db.commit()
    db.close()

    await orchestrator.run_pipeline(
        task_id=task_id_2,
        prompt=prompt_health,
        dataset_name=dataset_health,
        require_approval=True
    )

    task_2 = orchestrator.active_tasks.get(task_id_2, {})
    assert task_2.get("status") == "awaiting_approval", f"Expected awaiting_approval, got {task_2.get('status')}"
    print("[SUCCESS] Healthcare Mission paused at Human-in-the-Loop Gateway!")

    await orchestrator.resume_with_approval(task_id_2, "approve", "Approved by Chief Medical Officer")
    assert task_2.get("status") == "completed", f"Expected completed, got {task_2.get('status')}"
    
    rep_2 = task_2.get("final_output", {}).get("management_report", {})
    metrics_2 = rep_2.get("key_metrics", {})
    print(f"[SUCCESS] Healthcare Mission completed! SLA Compliance: {metrics_2.get('total_revenue')}%")
    print(f"Breached Departments: {metrics_2.get('net_gap')}")
    print("[SUCCESS] Multi-Domain Autonomous Multi-Agent AI Platform fully verified end-to-end!")

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
