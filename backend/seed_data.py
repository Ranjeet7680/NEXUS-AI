import uuid
from datetime import datetime, timezone, timedelta
from backend.models import TaskModel, AgentExecutionModel, ApprovalModel, AuditLogModel

def seed_database(db):
    """
    Pre-seeds the database with rich historical audit records and verified agent executions
    if the curated tasks are missing. Ensures zero blank voids on first launch.
    """
    if db.query(TaskModel).filter(TaskModel.id == "task-audit-sales-8801").first():
        return

    now = datetime.now(timezone.utc)

    # 1. Q3 Enterprise Sales Shortfall & Churn Risk
    t1_id = "task-audit-sales-8801"
    t1 = TaskModel(
        id=t1_id,
        title="Q3 Enterprise ARR Shortfall & Churn Vulnerability Deep-Dive",
        raw_prompt="Audit Q3 sales pipeline, calculate total revenue vs forecast target, identify high-risk product lines, and recommend automated mitigation steps.",
        dataset_name="sample_sales_q3.csv",
        status="completed",
        plan_dag=[
            {"step": 1, "agent": "Planner Agent", "action": "Goal decomposition & analytical state graph", "status": "completed"},
            {"step": 2, "agent": "Document Agent", "action": "Ingest and schema-validate sample_sales_q3.csv", "status": "completed"},
            {"step": 3, "agent": "Research Agent", "action": "Retrieve enterprise SaaS churn and discount benchmarks", "status": "completed"},
            {"step": 4, "agent": "Data Analyst Agent", "action": "Execute quantitative revenue delta and variance matrix", "status": "completed"},
            {"step": 5, "agent": "Decision Agent", "action": "Formulate executive risk synthesis and remediation strategy", "status": "completed"},
            {"step": 6, "agent": "Quality Agent", "action": "100% mathematical grounding and citation verification", "status": "completed"},
            {"step": 7, "agent": "Workflow Agent", "action": "Publish executive briefing and dispatch mitigation actions", "status": "completed"}
        ],
        final_output={
            "summary": "Full Q3 sales intelligence audit completed. Total revenue verified at $2,467,450 vs $2,440,000 baseline with 2 critical churn risks flagged.",
            "total_tokens": 18420,
            "total_latency_ms": 1420,
            "management_report": {
                "title": "Executive Briefing: Q3 Revenue Optimization & Customer Retention Strategy",
                "executive_summary": "Q3 performance finished 1.1% ahead of target overall, but masked extreme vulnerability in Legacy Bridge ERP (9.5% return rate) and OmniChannel CRM (churn risk score 0.88). Immediate corrective discounting freezes recommended.",
                "strategic_recommendations": [
                    "Freeze discretionary discounting above 10% on North American SaaS tiers.",
                    "Assign dedicated technical account executives to top 3 accounts showing elevated return rates.",
                    "Migrate Legacy Bridge ERP customers to CloudNexus Enterprise with dedicated onboarding credits."
                ],
                "financial_impact": "$380,000 in at-risk ARR safeguarded through preemptive intervention.",
                "risk_matrix": [
                    {"category": "Product Churn", "severity": "HIGH", "mitigation": "Targeted Customer Success playbooks"},
                    {"category": "Discount Erosion", "severity": "MEDIUM", "mitigation": "Automated pricing approvals gate"}
                ]
            }
        },
        total_tokens=18420,
        total_latency_ms=1420,
        created_at=now - timedelta(hours=6)
    )

    # 2. Healthcare Emergency Department Triage Latency
    t2_id = "task-audit-health-9204"
    t2 = TaskModel(
        id=t2_id,
        title="Hospital Emergency Department Triage Latency & ICU Bed Turnover Audit",
        raw_prompt="Audit clinical emergency room triage wait times against target SLAs, detect operational bottlenecks, and formulate nurse-to-patient rebalancing protocol.",
        dataset_name="healthcare_patient_ops.csv",
        status="completed",
        plan_dag=[
            {"step": 1, "agent": "Planner Agent", "action": "Map clinical protocol DAG and HIPAA boundary constraints", "status": "completed"},
            {"step": 2, "agent": "Document Agent", "action": "Ingest healthcare_patient_ops.csv with PHI redaction", "status": "completed"},
            {"step": 3, "agent": "Research Agent", "action": "Benchmark against CMS hospital quality standards", "status": "completed"},
            {"step": 4, "agent": "Data Analyst Agent", "action": "Calculate SLA breach variance across ED, ICU, and Cardiology", "status": "completed"},
            {"step": 5, "agent": "Decision Agent", "action": "Synthesize clinical staffing surge recommendations", "status": "completed"},
            {"step": 6, "agent": "Quality Agent", "action": "Verify HIPAA safe harbor compliance and statistical grounding", "status": "completed"},
            {"step": 7, "agent": "Workflow Agent", "action": "Dispatch automated clinical alerts to medical directors", "status": "completed"}
        ],
        final_output={
            "summary": "Clinical operations compliance audit completed. Identified critical triage bottleneck in Emergency (28 min vs 15 min SLA) and ICU staffing deficit.",
            "total_tokens": 22650,
            "total_latency_ms": 1840,
            "management_report": {
                "title": "Clinical Operational Audit: ED Triage & Patient Flow Optimization",
                "executive_summary": "Emergency triage currently exceeds safety SLA by 86%. ICU nurse-to-patient ratio has dipped to 1.4:1 against the mandatory 2.0:1 threshold, requiring immediate activation of cross-department float pool.",
                "strategic_recommendations": [
                    "Activate secondary rapid-triage triage bay during peak hours (14:00 - 22:00).",
                    "Dispatch float-pool nursing personnel to ICU immediately to restore 2.0:1 statutory ratio.",
                    "Automate radiologist critical findings notifications to compress acknowledgment cycle from 18 to 10 minutes."
                ],
                "financial_impact": "Avoidance of estimated $1.2M in regulatory CMS penalties and 24% reduction in avoidable diversion hours.",
                "risk_matrix": [
                    {"category": "Patient Safety", "severity": "CRITICAL", "mitigation": "Emergency float pool activation"},
                    {"category": "Regulatory SLA", "severity": "HIGH", "mitigation": "Automated EHR escalation notifications"}
                ]
            }
        },
        total_tokens=22650,
        total_latency_ms=1840,
        created_at=now - timedelta(hours=4, minutes=30)
    )

    # 3. FinTech Fraud & AML Telemetry
    t3_id = "task-audit-fraud-7712"
    t3 = TaskModel(
        id=t3_id,
        title="High-Velocity FinTech AML Flag & Cross-Border Fraud Prevention Audit",
        raw_prompt="Scan transactional ledger for high-velocity payment bursts, cross-border jurisdiction hops, and AML risk thresholds.",
        dataset_name="financial_fraud_telemetry.csv",
        status="completed",
        plan_dag=[
            {"step": 1, "agent": "Planner Agent", "action": "Define FinCEN & BSA regulatory detection parameters", "status": "completed"},
            {"step": 2, "agent": "Document Agent", "action": "Ingest financial_fraud_telemetry.csv with zero PII exposure", "status": "completed"},
            {"step": 3, "agent": "Data Analyst Agent", "action": "Compute anomaly probability distribution and card velocity", "status": "completed"},
            {"step": 4, "agent": "Decision Agent", "action": "Establish automated quarantine and human escalation thresholds", "status": "completed"},
            {"step": 5, "agent": "Quality Agent", "action": "Cryptographic zero-false-positive validation", "status": "completed"},
            {"step": 6, "agent": "Workflow Agent", "action": "Generate SAR (Suspicious Activity Report) draft ledger", "status": "completed"}
        ],
        final_output={
            "summary": "Fraud intelligence scan analyzed 10 high-value flows: blocked 3 high-risk crypto/precious metals attempts totaling $205,300 with 100% precision.",
            "total_tokens": 19840,
            "total_latency_ms": 1620,
            "management_report": {
                "title": "FinTech Security Telemetry: AML Risk & Payment Anomaly Containment",
                "executive_summary": "Three transactions flagged with velocity > 4/hr and IP device trust scores < 0.40 were quarantined automatically at the HITL gateway, completely halting suspected account takeovers.",
                "strategic_recommendations": [
                    "Require mandatory step-up FIDO2 hardware MFA for accounts attempting wires over $40,000.",
                    "Submit automated Form SAR to FinCEN compliance queue for accounts ACC-44910 and ACC-99234."
                ],
                "financial_impact": "Direct recovery of $205,300 in fraudulent transfers and zero chargeback liability incurred."
            }
        },
        total_tokens=19840,
        total_latency_ms=1620,
        created_at=now - timedelta(hours=3, minutes=15)
    )

    # 4. Supply Chain Logistics Disruption
    t4_id = "task-audit-supply-6340"
    t4 = TaskModel(
        id=t4_id,
        title="Global Container Dwell & Port Congestion Risk Mitigation Plan",
        raw_prompt="Analyze maritime transit days and dwell hours across major shipping corridors; formulate rerouting paths around congested terminals.",
        dataset_name="supply_chain_logistics.csv",
        status="completed",
        plan_dag=[
            {"step": 1, "agent": "Planner Agent", "action": "Model multimodal freight network topology", "status": "completed"},
            {"step": 2, "agent": "Document Agent", "action": "Parse shipment telemetry across 10 global trade lanes", "status": "completed"},
            {"step": 3, "agent": "Data Analyst Agent", "action": "Compute container dwell variance and demurrage accumulation", "status": "completed"},
            {"step": 4, "agent": "Decision Agent", "action": "Optimize cost-latency trade-offs for rail vs air rerouting", "status": "completed"},
            {"step": 5, "agent": "Workflow Agent", "action": "Issue electronic EDI dispatch directives to freight forwarders", "status": "completed"}
        ],
        final_output={
            "summary": "Supply chain audit completed across 8,800 TEU cargo. Recommended split air-freight for critical pharmaceutical components and rail reroutes.",
            "total_tokens": 26100,
            "total_latency_ms": 2150,
            "management_report": {
                "title": "Global Logistics Intelligence: Maritime Congestion & Demurrage Shielding",
                "executive_summary": "Rotterdam and Hamburg port dwell times reached 94 and 118 hours respectively. Proactive diversion of 1,200 TEU around Cape of Good Hope avoids 14 days of terminal blockage.",
                "strategic_recommendations": [
                    "Divert shipment SH-5510 via Cape of Good Hope corridor immediately.",
                    "Split container SH-5512 to dispatch urgent medical cargo via air freight from Seoul.",
                    "Shift Ningbo-Piraeus volume to rail hub via Valencia."
                ],
                "financial_impact": "$1.45M in estimated demurrage penalties and inventory stockout losses averted."
            }
        },
        total_tokens=26100,
        total_latency_ms=2150,
        created_at=now - timedelta(hours=2)
    )

    # 5. Cybersecurity Zero-Day & MITRE Telemetry
    t5_id = "task-audit-cyber-5108"
    t5 = TaskModel(
        id=t5_id,
        title="Zero-Day MITRE ATT&CK Incident Telemetry & Isolation Protocol",
        raw_prompt="Correlate security incident telemetry, verify containment statuses, and confirm zero data exfiltration across sovereign clusters.",
        dataset_name="cybersecurity_incidents.csv",
        status="completed",
        plan_dag=[
            {"step": 1, "agent": "Planner Agent", "action": "Ingest SIEM telemetry and map against MITRE ATT&CK matrix", "status": "completed"},
            {"step": 2, "agent": "Document Agent", "action": "Audit intrusion logs across API gateways and payment vaults", "status": "completed"},
            {"step": 3, "agent": "Decision Agent", "action": "Issue cryptographically signed pod isolation and key rotation commands", "status": "completed"},
            {"step": 4, "agent": "Quality Agent", "action": "Zero-data-leakage verification via sovereign audit hash", "status": "completed"}
        ],
        final_output={
            "summary": "Cyber defense audit completed across 7 incident vectors: 100% neutralized with zero data exfiltration detected.",
            "total_tokens": 31450,
            "total_latency_ms": 2410,
            "management_report": {
                "title": "Sovereign SOC Incident Report: Threat Neutralization & Zero-Leakage Audit",
                "executive_summary": "All 7 incident vectors (including a CVSS 9.6 SQL injection attempt and prompt injection exfiltration probe) were contained autonomously with zero byte leakage.",
                "strategic_recommendations": [
                    "Rotate all database credentials and worker service tokens within 2 hours.",
                    "Mandate DPO dual-key authorization for Sovereign Health Node EMR queries."
                ],
                "financial_impact": "Zero compliance breaches, maintaining full SOC 2 Type II, HIPAA, and FedRAMP compliance standing."
            }
        },
        total_tokens=31450,
        total_latency_ms=2410,
        created_at=now - timedelta(hours=1, minutes=10)
    )

    # 6. SaaS Cohort NDR & Expansion (AWAITING APPROVAL)
    t6_id = "task-audit-saas-4019"
    t6 = TaskModel(
        id=t6_id,
        title="SaaS Enterprise Cohort Expansion & Net Dollar Retention (NDR) Forecast",
        raw_prompt="Forecast NDR across enterprise cohorts, analyze expansion velocity, and prepare human-in-the-loop executive outreach memo.",
        dataset_name="saas_mrr_churn_analytics.csv",
        status="awaiting_approval",
        plan_dag=[
            {"step": 1, "agent": "Planner Agent", "action": "Configure cohort retention and expansion modeling", "status": "completed"},
            {"step": 2, "agent": "Document Agent", "action": "Ingest saas_mrr_churn_analytics.csv", "status": "completed"},
            {"step": 3, "agent": "Data Analyst Agent", "action": "Calculate cohort NDR, ARR expansion, and churn propensity", "status": "completed"},
            {"step": 4, "agent": "Decision Agent", "action": "Formulate targeted account executive retention package", "status": "completed"},
            {"step": 5, "agent": "Workflow Agent", "action": "Halt at Human-in-the-Loop Gateway for executive signoff", "status": "awaiting_approval"}
        ],
        final_output={
            "summary": "Enterprise cohort analysis shows Enterprise Platinum NDR at 112.8% and Sovereign at 118.4%. Executive retention outreach generated and awaiting approval.",
            "total_tokens": 16250,
            "total_latency_ms": 1380
        },
        total_tokens=16250,
        total_latency_ms=1380,
        created_at=now - timedelta(minutes=24)
    )

    # Add pending human approval for task 6
    appr6 = ApprovalModel(
        id=t6_id,
        task_id=t6_id,
        action_type="EXECUTIVE_DISPATCH_AND_EXPANSION_CONTRACT",
        recipient="chief.revenue.officer@enterprise-corp.com",
        subject="[ACTION REQUIRED] NEXUS AI: Authorized Enterprise Platinum & Sovereign Expansion Package ($130,000 ARR)",
        preview_content="Executive Summary:\nOur multi-agent analytics pipeline audited Q1/Q2 cohorts and confirmed 118.4% NDR within Enterprise Sovereign tier. We recommend deploying automated expansion contracts and scheduling executive business reviews for top accounts.\n\nSign off required to execute external dispatch.",
        status="pending",
        created_at=now - timedelta(minutes=22)
    )

    # Add tasks to session
    db.add(t1)
    db.add(t2)
    db.add(t3)
    db.add(t4)
    db.add(t5)
    db.add(t6)
    db.add(appr6)

    # Add execution traces for agent telemetry
    tasks = [t1, t2, t3, t4, t5, t6]
    agent_names = ["Planner Agent", "Document Agent", "Research Agent", "Data Analyst Agent", "Decision Agent", "Quality Agent", "Workflow Agent"]

    for t in tasks:
        tokens_per_agent = t.total_tokens // len(agent_names)
        latency_per_agent = t.total_latency_ms // len(agent_names)
        for i, agent in enumerate(agent_names):
            rec = AgentExecutionModel(
                id=str(uuid.uuid4()),
                task_id=t.id,
                agent_name=agent,
                step_number=i + 1,
                phase="completed",
                message=f"{agent} verified step {i+1} for {t.title[:40]}...",
                payload={"status": "verified", "tokens": tokens_per_agent},
                confidence_score=0.98,
                tokens_consumed=tokens_per_agent,
                latency_ms=latency_per_agent,
                timestamp=t.created_at + timedelta(seconds=(i + 1) * 3)
            )
            db.add(rec)

    # Add audit log entries
    for t in tasks:
        audit = AuditLogModel(
            id=str(uuid.uuid4()),
            task_id=t.id,
            actor="NEXUS Autonomous Swarm",
            action=f"AUDIT_VERIFIED: {t.title[:50]}",
            details={"sha256": f"sha256-{uuid.uuid4().hex[:16]}", "status": t.status, "tokens": t.total_tokens},
            timestamp=t.created_at
        )
        db.add(audit)

    db.commit()
