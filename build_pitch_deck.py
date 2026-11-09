import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Dark Theme Palette
    C_BG_DARK = RGBColor(3, 7, 18)        # #030712
    C_CARD_BG = RGBColor(15, 23, 42)      # #0F172A
    C_CARD_BORDER = RGBColor(31, 46, 77)  # #1F2E4D
    C_BLUE = RGBColor(57, 123, 255)       # #397BFF
    C_CYAN = RGBColor(0, 245, 255)        # #00F5FF
    C_PURPLE = RGBColor(134, 91, 255)     # #865BFF
    C_EMERALD = RGBColor(16, 185, 129)    # #10B981
    C_AMBER = RGBColor(245, 158, 11)      # #F59E0B
    C_ROSE = RGBColor(244, 63, 94)        # #F43F5E
    C_WHITE = RGBColor(255, 255, 255)
    C_MUTED = RGBColor(148, 163, 184)     # #94A3B8
    C_DIM = RGBColor(100, 116, 139)       # #64748B

    bg_cover_path = 'assets/deck_images/slide_bg_cover.jpg'
    bg_content_path = 'assets/deck_images/slide_bg_content.jpg'

    def apply_background(slide, is_cover=False):
        bg = bg_cover_path if is_cover else bg_content_path
        if os.path.exists(bg):
            slide.shapes.add_picture(bg, 0, 0, width=prs.slide_width, height=prs.slide_height)
        else:
            bg_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
            bg_rect.fill.solid()
            bg_rect.fill.fore_color.rgb = C_BG_DARK
            bg_rect.line.fill.background()

    def add_header(slide, title, category_tag, slide_num):
        # Category tag
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(8), Inches(0.35))
        tf = tx_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = category_tag.upper()
        p.font.name = 'Consolas'
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_CYAN

        # Main slide title
        tx_box2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(10), Inches(0.75))
        tf2 = tx_box2.text_frame
        tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
        p2 = tf2.paragraphs[0]
        p2.text = title
        p2.font.name = 'Arial'
        p2.font.size = Pt(21)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE

        # Brand & Slide counter in top-right
        right_box = slide.shapes.add_textbox(Inches(9.5), Inches(0.48), Inches(3.0), Inches(0.6))
        rf = right_box.text_frame
        rf.margin_left = rf.margin_top = rf.margin_right = rf.margin_bottom = 0
        rp = rf.paragraphs[0]
        rp.alignment = PP_ALIGN.RIGHT
        rp.text = f"NEXUS AI Enterprise | Slide {slide_num} of 12"
        rp.font.name = 'Consolas'
        rp.font.size = Pt(9)
        rp.font.color.rgb = C_DIM

        # Subtle divider rule
        rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.48), Inches(11.733), Inches(0.015))
        rule.fill.solid()
        rule.fill.fore_color.rgb = C_CARD_BORDER
        rule.line.fill.background()

    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=C_BLUE, tag=""):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = C_CARD_BORDER
        card.line.width = Pt(1.2)

        # Top accent bar on card
        bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.15), top, width - Inches(0.3), Inches(0.04))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent_color
        bar.line.fill.background()

        tx_box = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), width - Inches(0.5), height - Inches(0.36))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        if tag:
            p_tag = tf.paragraphs[0]
            p_tag.text = tag.upper()
            p_tag.font.name = 'Consolas'
            p_tag.font.size = Pt(8.5)
            p_tag.font.bold = True
            p_tag.font.color.rgb = accent_color
            p_tag.space_after = Pt(4)
            p_title = tf.add_paragraph()
        else:
            p_title = tf.paragraphs[0]

        p_title.text = title
        p_title.font.name = 'Arial'
        p_title.font.size = Pt(13)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE
        p_title.space_after = Pt(10)

        for b in body_bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"•  {b}"
            p_b.font.name = 'Arial'
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = C_MUTED
            p_b.space_after = Pt(6)

        return card

    def add_stat_box(slide, left, top, width, height, big_num, label, subtext, color=C_CYAN):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG
        box.line.color.rgb = C_CARD_BORDER
        box.line.width = Pt(1)

        tx = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
        tf = tx.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p1 = tf.paragraphs[0]
        p1.text = big_num
        p1.font.name = 'Arial'
        p1.font.size = Pt(28)
        p1.font.bold = True
        p1.font.color.rgb = color
        p1.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.name = 'Arial'
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = subtext
        p3.font.name = 'Arial'
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = C_MUTED

    # =========================================================================
    # SLIDE 1: Title & Executive Vision Cover
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1, is_cover=True)

    # Top Brand Pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.0), Inches(4.2), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(17, 26, 46)
    pill.line.color.rgb = C_BLUE
    pill_tf = pill.text_frame
    pill_p = pill_tf.paragraphs[0]
    pill_p.text = "NEXUS AI 2.0  //  ENTERPRISE MULTI-AGENT SWARM"
    pill_p.alignment = PP_ALIGN.CENTER
    pill_p.font.name = 'Consolas'
    pill_p.font.size = Pt(9.5)
    pill_p.font.bold = True
    pill_p.font.color.rgb = C_CYAN

    # Giant Headline
    tx1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.65), Inches(11.5), Inches(2.2))
    tf1 = tx1.text_frame
    tf1.word_wrap = True
    p_h1 = tf1.paragraphs[0]
    p_h1.text = "Deterministic Multi-Agent Governance"
    p_h1.font.name = 'Arial'
    p_h1.font.size = Pt(36)
    p_h1.font.bold = True
    p_h1.font.color.rgb = C_WHITE
    p_h1.space_after = Pt(6)

    p_h2 = tf1.add_paragraph()
    p_h2.text = "& Enterprise Intelligence Platform"
    p_h2.font.name = 'Arial'
    p_h2.font.size = Pt(34)
    p_h2.font.bold = True
    p_h2.font.color.rgb = C_BLUE
    p_h2.space_after = Pt(16)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Transitioning mission-critical operations from fragile conversational prompts to verifiable, stateful LangGraph agent swarms with 0.00% math hallucinations and cryptographic Human-in-the-Loop oversight."
    p_sub.font.name = 'Arial'
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = C_MUTED

    # 3 Stat Cards on Cover
    add_stat_box(s1, Inches(0.8), Inches(4.7), Inches(3.7), Inches(1.8), "7-Agent Swarm", "Role-Specialized DAG", "Planner, Analyst, Decision, Quality & Audit nodes", C_BLUE)
    add_stat_box(s1, Inches(4.8), Inches(4.7), Inches(3.7), Inches(1.8), "0.00%", "Math Hallucinations", "Sandboxed NumPy/Pandas execution micro-kernels", C_EMERALD)
    add_stat_box(s1, Inches(8.8), Inches(4.7), Inches(3.7), Inches(1.8), "Dual-Key HITL", "Cryptographic Gate", "Immutable SHA-256 audit ledger before external dispatch", C_PURPLE)

    # Footer Watermark
    tx_foot = s1.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.7), Inches(0.4))
    tf_f = tx_foot.text_frame
    pf = tf_f.paragraphs[0]
    pf.text = "RFC-2026-NEXUS Architecture Specification  |  Live at nexus-ai-ten-gamma.vercel.app  |  Air-Gapped Sovereign Ready"
    pf.font.name = 'Consolas'
    pf.font.size = Pt(8.5)
    pf.font.color.rgb = C_DIM

    # =========================================================================
    # SLIDE 2: The Enterprise AI Problem Statement
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2)
    add_header(s2, "Why Single LLMs & Ad-Hoc Scripts Fail in Mission-Critical Enterprise Production", "// 02 . INDUSTRY CHALLENGE", 2)

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8),
             "1. Mathematical & Data Hallucinations",
             [
                 "Probabilistic token sampling inherently lacks computational certainty.",
                 "Financial ARR, clinical dosage, and inventory numbers are frequently fabricated.",
                 "Context window dilution causes loss of critical facts across lengthy documents.",
                 "Zero guarantee of mathematical grounding in board reports and audit filings."
             ], C_ROSE, "CRISIS: ACCURACY")

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8),
             "2. The Black-Box Liability Crisis",
             [
                 "Conversational chatbots leave zero verifiable trace of internal reasoning.",
                 "Audit and regulatory compliance teams cannot reconstruct decision pathways.",
                 "No immutable state machine checkpoints between steps.",
                 "Vulnerability to catastrophic regulatory fines (SEC, HIPAA, GDPR, FedRAMP)."
             ], C_AMBER, "CRISIS: AUDITABILITY")

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8),
             "3. Rogue Agent Exfiltration & Tool Risk",
             [
                 "Ad-hoc AI agents execute tool dispatches without human oversight.",
                 "Prompt injection attacks can hijack agent memory and leak corporate secrets.",
                 "Absence of deterministic Human-in-the-Loop approval gates.",
                 "External communications (emails, wire transfers, database drops) fire blindly."
             ], C_PURPLE, "CRISIS: GOVERNANCE")

    # =========================================================================
    # SLIDE 3: The NEXUS Solution — Multi-Agent Collaborative Swarm
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3)
    add_header(s3, "The NEXUS Solution: Deterministic LangGraph Multi-Agent Architecture", "// 03 . SOLUTION ARCHITECTURE", 3)

    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.2), Inches(4.8),
             "Core Paradigm Shift",
             [
                 "Separation of Concerns: Decomposes unstructured missions into 7 micro-agent nodes, each bound by least-privilege security policies.",
                 "LangGraph Stateful Execution: Shared episodic and working memory preserves deterministic state checkpoints across execution branches.",
                 "Sandboxed Execution Micro-Kernels: Quantitative math runs exclusively in isolated Python/NumPy environments, eliminating text-generation hallucination.",
                 "Cryptographic State Ledger: Every agent input, tool payload, and output is signed with SHA-256 hashes into an immutable audit chain."
             ], C_CYAN, "DETERMINISTIC SWARM")

    if os.path.exists('assets/deck_images/diagram_swarm_dag.png'):
        s3.shapes.add_picture('assets/deck_images/diagram_swarm_dag.png', Inches(6.3), Inches(1.8), width=Inches(6.2), height=Inches(4.8))

    # =========================================================================
    # SLIDE 4: Deep Dive — The 7 Autonomous Swarm Agents
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4)
    add_header(s4, "Specialized AI Roles with Strict Least-Privilege Guardrails", "// 04 . SWARM AGENT ROLES", 4)

    card_w = Inches(2.75)
    card_h = Inches(2.3)

    # Row 1 (4 agents)
    add_card(s4, Inches(0.8), Inches(1.8), card_w, card_h,
             "1. Planner Agent",
             ["Decomposes mission into DAG states.", "Establishes domain constraints & schema.", "Allocates tokens & SLA thresholds."], C_BLUE, "NODE 1")

    add_card(s4, Inches(3.75), Inches(1.8), card_w, card_h,
             "2. Document Agent",
             ["Parses enterprise CSV/JSON/PDF.", "Automated PII/PHI redaction pipeline.", "Vectorizes chunks into pgvector RAG."], C_CYAN, "NODE 2")

    add_card(s4, Inches(6.7), Inches(1.8), card_w, card_h,
             "3. Research Agent",
             ["Retrieves domain benchmarks & SLAs.", "CMS, FinCEN, MITRE, SaaS NDR knowledge.", "Enriches prompt with empirical data."], C_EMERALD, "NODE 3")

    add_card(s4, Inches(9.65), Inches(1.8), card_w, card_h,
             "4. Analyst Agent",
             ["Executes sandboxed Python math.", "Variance, anomaly & regression modeling.", "0.00% calculation hallucination."], C_PURPLE, "NODE 4")

    # Row 2 (3 agents)
    add_card(s4, Inches(0.8), Inches(4.35), Inches(3.7), card_h,
             "5. Decision Agent",
             ["Synthesizes statistical findings into executive briefing.", "Formulates actionable mitigation strategy and revenue protection.", "Prepares external deliverables with risk score classification."], C_AMBER, "NODE 5: STRATEGY")

    add_card(s4, Inches(4.8), Inches(4.35), Inches(3.7), card_h,
             "6. Quality & Evaluator Agent",
             ["Adversarial auditor validating math against raw source data.", "Enforces zero-tolerance citation grounding standards.", "Certifies deliverable before advancing to delivery."], C_ROSE, "NODE 6: VERIFICATION")

    add_card(s4, Inches(8.8), Inches(4.35), Inches(3.7), card_h,
             "7. Workflow Agent",
             ["Packages management deliverables into cryptographic ledger.", "Evaluates policy: pauses state machine at HITL Gateway if risk >= 0.70.", "Dispatches authorized actions post human approval."], C_BLUE, "NODE 7: GOVERNANCE")

    # =========================================================================
    # SLIDE 5: Execution DAG Lifecycle & State Machine Transitions
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5)
    add_header(s5, "Mathematical Grounding & Checkpointing at Every State Transition", "// 05 . EXECUTION LIFECYCLE", 5)

    add_card(s5, Inches(0.8), Inches(1.8), Inches(2.75), Inches(3.2),
             "Phase 1: Ingestion",
             [
                 "Tabular data validation.",
                 "Automated HIPAA/GDPR sanitization.",
                 "Cosine similarity vector indexing.",
                 "Schema-grounded prompt injection."
             ], C_CYAN, "RAG VECTORIZATION")

    add_card(s5, Inches(3.75), Inches(1.8), Inches(2.75), Inches(3.2),
             "Phase 2: Execution",
             [
                 "Parallel DAG execution.",
                 "NumPy statistical modeling.",
                 "Episodic memory search.",
                 "Risk score classification."
             ], C_BLUE, "SANDBOXED MATH")

    add_card(s5, Inches(6.7), Inches(1.8), Inches(2.75), Inches(3.2),
             "Phase 3: Quality Gate",
             [
                 "Zero-hallucination verification.",
                 "Math recalculation parity check.",
                 "Citation grounding check.",
                 "Policy threshold evaluation."
             ], C_PURPLE, "ADVERSARIAL CHECK")

    add_card(s5, Inches(9.65), Inches(1.8), Inches(2.75), Inches(3.2),
             "Phase 4: Delivery",
             [
                 "Dual-key human signoff if needed.",
                 "Cryptographic SHA-256 signing.",
                 "Immutable ledger logging.",
                 "External tool dispatch."
             ], C_EMERALD, "FINAL SETTLEMENT")

    # Stat strip below
    add_stat_box(s5, Inches(0.8), Inches(5.25), Inches(3.7), Inches(1.4), "< 342ms", "Average Execution Latency", "Microsecond agent coordination", C_CYAN)
    add_stat_box(s5, Inches(4.8), Inches(5.25), Inches(3.7), Inches(1.4), "100% ACID", "State Machine Checkpoints", "Resumable LangGraph pipeline", C_BLUE)
    add_stat_box(s5, Inches(8.8), Inches(5.25), Inches(3.7), Inches(1.4), "Zero Leakage", "Sovereign Air-Gap Isolation", "No prompt or payload egress", C_EMERALD)

    # =========================================================================
    # SLIDE 6: Cryptographic Human-in-the-Loop (HITL) Governance
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6)
    add_header(s6, "Zero Autonomous External Egress Without Explicit Human Authorization", "// 06 . HITL GOVERNANCE", 6)

    add_card(s6, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8),
             "1. Automated Trigger Criteria",
             [
                 "Risk Score >= 0.70: Actions with high financial, legal, or operational impact are frozen automatically.",
                 "External Boundary Dispatches: Customer emails, vendor orders, and wire transfers mandate sign-off.",
                 "Regulatory SLAs: Healthcare clinical surges and cybersecurity remediations require human authority."
             ], C_AMBER, "GATEWAY POLICY")

    add_card(s6, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8),
             "2. Dual-Key Operator Queue",
             [
                 "Interactive Preview: Operators inspect exact email/action body and synthesized rationale.",
                 "One-Click Authorization: Single-click 'Approve & Execute' or 'Reject & Terminate'.",
                 "Reviewer Justification: Operator notes are permanently attached to the cryptographic transaction record."
             ], C_BLUE, "HUMAN OPERATOR")

    add_card(s6, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8),
             "3. Immutable Audit Ledger",
             [
                 "Cryptographic Hashing: Every decision is signed with SHA-256 fingerprints.",
                 "Tamper-Evident Ledger: Historical tasks cannot be modified or deleted.",
                 "Enterprise Compliance Ready: Exportable for SOC 2 Type II, HIPAA, and ISO 27001 auditor reviews."
             ], C_EMERALD, "COMPLIANCE LEDGER")

    # =========================================================================
    # SLIDE 7: Enterprise Multi-Domain Data Hub (7 Core Verticals)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7)
    add_header(s7, "Pre-Trained Industry Schemas Across 7 Mission-Critical Verticals", "// 07 . ENTERPRISE DATASETS", 7)

    col_w = Inches(3.7)
    # Left column (3 verticals)
    add_card(s7, Inches(0.8), Inches(1.8), col_w, Inches(1.5),
             "1. Banking & FinTech",
             ["Dataset: financial_fraud_telemetry.csv", "High-velocity AML flags, anomaly detection, card velocity."], C_PURPLE, "FINTECH")

    add_card(s7, Inches(0.8), Inches(3.45), col_w, Inches(1.5),
             "2. Clinical Healthcare Systems",
             ["Dataset: healthcare_patient_ops.csv", "Emergency triage latency, ICU ratios, physician lead SLAs."], C_EMERALD, "HEALTHCARE")

    add_card(s7, Inches(0.8), Inches(5.1), col_w, Inches(1.5),
             "3. Global Supply Chain Logistics",
             ["Dataset: supply_chain_logistics.csv", "Port dwell hours, demurrage shielding, multimodal rerouting."], C_AMBER, "LOGISTICS")

    # Middle column (3 verticals)
    add_card(s7, Inches(4.8), Inches(1.8), col_w, Inches(1.5),
             "4. Cyber Threat & SOC Defense",
             ["Dataset: cybersecurity_incidents.csv", "MITRE ATT&CK vectors, CVSS 9.6 isolation, zero exfiltration."], C_ROSE, "CYBER DEFENSE")

    add_card(s7, Inches(4.8), Inches(3.45), col_w, Inches(1.5),
             "5. SaaS Revenue & Churn Analytics",
             ["Dataset: saas_mrr_churn_analytics.csv", "Net Dollar Retention (118.4%), cohort churn, expansion playbooks."], C_CYAN, "SAAS ANALYTICS")

    add_card(s7, Inches(4.8), Inches(5.1), col_w, Inches(1.5),
             "6. Biopharma Clinical Trials",
             ["Dataset: clinical_trial_metrics.csv", "FDA Phase III endpoints, p-value statistics, retention rates."], C_BLUE, "LIFE SCIENCES")

    # Right column (Summary & Custom Upload)
    add_card(s7, Inches(8.8), Inches(1.8), col_w, Inches(4.8),
             "7. Custom Enterprise Ingestion",
             [
                 "Universal Schema Parser: Ingest any CSV, JSON, or text dataset instantly.",
                 "Automated RAG Vectorization: Generates semantic chunks with metadata tagging in pgvector.",
                 "One-Click Swarm Orchestration: Launch specialized 7-agent mission templates across any tabular file in < 2 seconds.",
                 "Zero Training Egress: Proprietary business datasets remain strictly isolated in memory."
             ], C_CYAN, "ANY TABULAR DATASET")

    # =========================================================================
    # SLIDE 8: Real-Time Telemetry & Operations Command Center
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_background(s8)
    add_header(s8, "Live Cluster Monitoring, SLA Waterfalls & Guardrail Auditing", "// 08 . REAL-TIME TELEMETRY", 8)

    if os.path.exists('assets/deck_images/chart_telemetry_combo.png'):
        s8.shapes.add_picture('assets/deck_images/chart_telemetry_combo.png', Inches(0.8), Inches(1.8), width=Inches(7.2), height=Inches(4.8))

    add_card(s8, Inches(8.3), Inches(1.8), Inches(4.2), Inches(4.8),
             "Live Operational Metrics",
             [
                 "100% SLA Adherence: All agents finish well below red latency ceilings.",
                 "99.4% Autonomous Success: Certified by Quality Agent grounding check.",
                 "Real-Time Hardware Telemetry: Active load monitoring across sovereign GPU clusters.",
                 "Instant Timeframe Filtering: Inspect telemetry across 1H, 24H, 7D, or 30D operational windows.",
                 "Zero Performance Degradation: Horizontal scalability across multi-tenant clusters."
             ], C_EMERALD, "SLA DASHBOARD")

    # =========================================================================
    # SLIDE 9: Security, Compliance & Sovereign Deployment Models
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_background(s9)
    add_header(s9, "Air-Gapped Sovereign AI with Zero Model Training Egress", "// 09 . SECURITY & COMPLIANCE", 9)

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3),
             "1. Zero Model Training Guarantee",
             [
                 "Customer prompts, proprietary datasets, and agent outputs are NEVER used to train, fine-tune, or calibrate models.",
                 "Explicit contractual data ownership backed by Master Services Agreement."
             ], C_CYAN, "DATA SOVEREIGNTY")

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.3),
             "2. Cryptographic Enclave Isolation",
             [
                 "AES-256 encryption at rest; TLS 1.3 in transit.",
                 "Row-Level Security (RLS) tenant isolation prevents cross-organization data leakage.",
                 "Automated real-time PII & PHI redaction prior to LLM context ingestion."
             ], C_BLUE, "ENCRYPTION")

    add_card(s9, Inches(0.8), Inches(4.35), Inches(5.6), Inches(2.3),
             "3. Multi-Regulation Compliance",
             [
                 "Pre-configured for SOC 2 Type II, HIPAA, ISO 27001, GDPR, and FedRAMP.",
                 "Cryptographic audit logs exportable for external regulatory inspection."
             ], C_PURPLE, "CERTIFICATION")

    add_card(s9, Inches(6.8), Inches(4.35), Inches(5.6), Inches(2.3),
             "4. Flexible Deployment Topologies",
             [
                 "Dedicated Sovereign VPC (AWS, GCP, Azure) with customer-managed keys (BYOK).",
                 "Air-Gapped On-Premises bare-metal deployment with zero internet connectivity."
             ], C_EMERALD, "AIR-GAPPED READY")

    # =========================================================================
    # SLIDE 10: Comparative Competitive Advantage
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_background(s10)
    add_header(s10, "NEXUS AI vs. Traditional LLM Solutions & Fragile Script Frameworks", "// 10 . COMPETITIVE ADVANTAGE", 10)

    if os.path.exists('assets/deck_images/chart_radar_comparison.png'):
        s10.shapes.add_picture('assets/deck_images/chart_radar_comparison.png', Inches(0.8), Inches(1.8), width=Inches(5.0), height=Inches(4.8))

    add_card(s10, Inches(6.1), Inches(1.8), Inches(6.4), Inches(4.8),
             "Enterprise Architectural Comparison",
             [
                 "Deterministic State Machine vs. Uncontrolled Chat: NEXUS coordinates stateful LangGraph agents with deterministic rollback capabilities.",
                 "Sandboxed Python Math Execution: Calculations run in isolated NumPy runtimes with 0.00% math hallucination guarantee.",
                 "Dual-Key Human-in-the-Loop Gateway: High-risk actions freeze automatically until signed off by human operators.",
                 "Immutable Cryptographic SHA-256 Ledger: Every prompt, execution trace, and output is permanently audited.",
                 "Enterprise Production SLA: Sub-450ms P99 latency and 99.9% uptime availability."
             ], C_CYAN, "WHY NEXUS WINS")

    # =========================================================================
    # SLIDE 11: Enterprise ROI & Quantifiable Impact Metrics
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_background(s11)
    add_header(s11, "Quantifiable Business Acceleration Across Enterprise Deployments", "// 11 . BUSINESS IMPACT & ROI", 11)

    if os.path.exists('assets/deck_images/chart_roi_impact.png'):
        s11.shapes.add_picture('assets/deck_images/chart_roi_impact.png', Inches(0.8), Inches(1.8), width=Inches(5.8), height=Inches(4.8))

    add_stat_box(s11, Inches(6.9), Inches(1.8), Inches(5.6), Inches(1.1), "82% Faster", "Analytical Cycle Times", "Complex audits compressed from 48 hours to 14 minutes", C_CYAN)
    add_stat_box(s11, Inches(6.9), Inches(3.05), Inches(5.6), Inches(1.1), "$2.4M Saved", "Average Annual Breach Avoidance", "Preempting regulatory penalties, demurrage & chargebacks", C_EMERALD)
    add_stat_box(s11, Inches(6.9), Inches(4.3), Inches(5.6), Inches(1.1), "0.00%", "Math & Fact Hallucinations", "100% verified mathematical grounding on all structured data", C_BLUE)
    add_stat_box(s11, Inches(6.9), Inches(5.55), Inches(5.6), Inches(1.1), "4.8x Velocity", "Executive Decision Acceleration", "Ready-to-sign executive management reports & briefs", C_PURPLE)

    # =========================================================================
    # SLIDE 12: Roadmap, Enterprise Licensing & Call to Action
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_background(s12)
    add_header(s12, "Deploy NEXUS AI into Your Sovereign Infrastructure Today", "// 12 . ENTERPRISE LICENSING & NEXT STEPS", 12)

    add_card(s12, Inches(0.8), Inches(1.8), Inches(3.7), Inches(3.4),
             "1. Enterprise Cloud SaaS",
             [
                 "Dedicated tenant isolation.",
                 "Instant access to 7 pre-built datasets.",
                 "API Gateway & Swagger Docs.",
                 "99.9% Uptime Enterprise SLA."
             ], C_BLUE, "TIER 1")

    add_card(s12, Inches(4.8), Inches(1.8), Inches(3.7), Inches(3.4),
             "2. Sovereign Private VPC",
             [
                 "AWS, Azure, or GCP Dedicated VPC.",
                 "Customer-Managed Encryption (BYOK).",
                 "Custom LLM fine-tuning weights.",
                 "Dedicated Customer Success Engineer."
             ], C_PURPLE, "TIER 2")

    add_card(s12, Inches(8.8), Inches(1.8), Inches(3.7), Inches(3.4),
             "3. Air-Gapped Sovereign Node",
             [
                 "100% On-Premise bare-metal install.",
                 "Zero internet egress required.",
                 "Defense, Intelligence & Healthcare.",
                 "Custom tool & database adapters."
             ], C_EMERALD, "TIER 3")

    # Bottom Call to Action Banner
    cta = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.4), Inches(11.733), Inches(1.5))
    cta.fill.solid()
    cta.fill.fore_color.rgb = RGBColor(17, 26, 46)
    cta.line.color.rgb = C_CYAN
    cta.line.width = Pt(1.5)

    tx_cta = s12.shapes.add_textbox(Inches(1.0), Inches(5.55), Inches(11.3), Inches(1.2))
    tf_cta = tx_cta.text_frame
    tf_cta.word_wrap = True
    p_c1 = tf_cta.paragraphs[0]
    p_c1.text = "READY TO EVALUATE NEXUS AI FOR YOUR ORGANIZATION?"
    p_c1.font.name = 'Arial'
    p_c1.font.size = Pt(14)
    p_c1.font.bold = True
    p_c1.font.color.rgb = C_CYAN
    p_c1.space_after = Pt(4)

    p_c2 = tf_cta.add_paragraph()
    p_c2.text = "• Live Platform Sandbox: https://nexus-ai-ten-gamma.vercel.app\n• Architecture Whitepaper: https://nexus-ai-ten-gamma.vercel.app/whitepaper\n• GitHub Source: https://github.com/Ranjeet7680/NEXUS-AI  |  Contact: partnerships@nexus-ai.platform"
    p_c2.font.name = 'Consolas'
    p_c2.font.size = Pt(9.5)
    p_c2.font.color.rgb = C_WHITE

    # Save presentation
    output_path = 'assets/NEXUS_AI_Platform_Presentation.pptx'
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path} ({os.path.getsize(output_path)} bytes)")

    # Also save to static directory so it is downloadable directly from the website!
    static_output = 'backend/static/NEXUS_AI_Platform_Presentation.pptx'
    prs.save(static_output)
    print(f"Presentation copied to web static folder: {static_output} ({os.path.getsize(static_output)} bytes)")

if __name__ == '__main__':
    create_presentation()
