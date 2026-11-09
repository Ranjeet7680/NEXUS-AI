import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

os.makedirs('assets/deck_images', exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Background image preparation
# -----------------------------------------------------------------------------
src_bg = 'assets/nexus-apple-bg.png'
if os.path.exists(src_bg):
    im = Image.open(src_bg).convert('RGBA')
    # Resize to 1920x1080 (16:9 widescreen)
    im_169 = im.resize((1920, 1080), Image.Resampling.LANCZOS)
    
    # Overlay dark gradient so text on slides is 100% readable
    dark_overlay = Image.new('RGBA', (1920, 1080), (3, 7, 18, 190))
    bg_composite = Image.alpha_composite(im_169, dark_overlay)
    bg_composite.convert('RGB').save('assets/deck_images/slide_bg_cover.jpg', quality=95)
    
    # Even darker overlay for content slides
    darker_overlay = Image.new('RGBA', (1920, 1080), (3, 7, 18, 225))
    bg_content = Image.alpha_composite(im_169, darker_overlay)
    bg_content.convert('RGB').save('assets/deck_images/slide_bg_content.jpg', quality=95)
    print("Prepared slide background images!")

# -----------------------------------------------------------------------------
# 2. Swarm Architecture Graphic (7 Agents)
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='#0B1224')
ax.set_facecolor('#0B1224')

agents = [
    ("Planner Agent", "Decompose Mission & DAG", "#397BFF", (1, 3)),
    ("Document Agent", "RAG & PHI Redaction", "#06B6D4", (3, 4)),
    ("Research Agent", "Industry Benchmarks", "#10B981", (3, 2)),
    ("Data Analyst Agent", "Statistical Python Math", "#865BFF", (5, 3)),
    ("Decision Agent", "Strategic Executive Synthesis", "#F59E0B", (7, 4)),
    ("Quality Agent", "100% Mathematical Grounding", "#EC4899", (7, 2)),
    ("Workflow Agent", "Audit Ledger & HITL Dispatch", "#6366F1", (9, 3))
]

# Draw connection lines
lines = [
    ((1, 3), (3, 4)), ((1, 3), (3, 2)),
    ((3, 4), (5, 3)), ((3, 2), (5, 3)),
    ((5, 3), (7, 4)), ((5, 3), (7, 2)),
    ((7, 4), (9, 3)), ((7, 2), (9, 3))
]
for p1, p2 in lines:
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="->", color="#38BDF8", lw=2.2, mutation_scale=15))

# Draw agent nodes
for name, desc, color, (x, y) in agents:
    # Outer glow box
    rect = plt.Rectangle((x-0.85, y-0.6), 1.7, 1.2, facecolor='#111A2E', edgecolor=color,
                         linewidth=2, linestyle='-', zorder=3, transform=ax.transData)
    ax.add_patch(rect)
    ax.text(x, y+0.15, name, color='#FFFFFF', fontsize=9.5, fontweight='bold',
            ha='center', va='center', zorder=4, family='sans-serif')
    ax.text(x, y-0.25, desc, color='#94A3B8', fontsize=7.5,
            ha='center', va='center', zorder=4, family='sans-serif')

ax.set_xlim(-0.2, 10.2)
ax.set_ylim(0.8, 5.2)
ax.axis('off')
plt.title("Deterministic Multi-Agent Collaboration DAG", color='#FFFFFF', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('assets/deck_images/diagram_swarm_dag.png', dpi=200, facecolor='#0B1224')
plt.close()
print("Saved diagram_swarm_dag.png")

# -----------------------------------------------------------------------------
# 3. Telemetry & SLA Waterfall Chart
# -----------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), facecolor='#0B1224')

# Latency chart
ax1.set_facecolor('#0B1224')
agents_list = ['Planner', 'Document', 'Research', 'Analyst', 'Decision', 'Quality', 'Workflow']
latencies = [185, 220, 310, 420, 380, 190, 240]
sla_limits = [500, 600, 700, 800, 750, 400, 500]
y_pos = np.arange(len(agents_list))

ax1.barh(y_pos, sla_limits, color='#EF4444', alpha=0.35, height=0.55, label='SLA Ceiling')
ax1.barh(y_pos, latencies, color='#10B981', height=0.35, label='NEXUS Observed Latency (ms)')
ax1.set_yticks(y_pos)
ax1.set_yticklabels(agents_list, color='#CBD5E1', fontsize=9, fontweight='bold')
ax1.set_xlabel('Execution Latency (Milliseconds)', color='#94A3B8', fontsize=8.5)
ax1.set_title('Agent SLA Response Times vs Thresholds', color='#FFFFFF', fontsize=10.5, fontweight='bold', pad=10)
ax1.tick_params(colors='#64748B')
ax1.grid(color='#1F2E4D', linestyle='--', alpha=0.5, axis='x')
ax1.legend(loc='lower right', facecolor='#111A2E', edgecolor='#1F2E4D', labelcolor='#CBD5E1', fontsize=8)
for spine in ax1.spines.values():
    spine.set_color('#1F2E4D')

# Throughput / Accuracy Chart
ax2.set_facecolor('#0B1224')
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
throughput = [120, 185, 240, 210, 310, 190, 380]
ax2.plot(days, throughput, color='#397BFF', marker='o', linewidth=2.5, markersize=6, label='Task Throughput')
ax2.fill_between(days, throughput, color='#397BFF', alpha=0.15)
ax2.set_title('Hourly Autonomous Swarm Throughput', color='#FFFFFF', fontsize=10.5, fontweight='bold', pad=10)
ax2.tick_params(colors='#64748B')
ax2.set_ylabel('Tasks Orchestrated / Day', color='#94A3B8', fontsize=8.5)
ax2.grid(color='#1F2E4D', linestyle='--', alpha=0.5)
for spine in ax2.spines.values():
    spine.set_color('#1F2E4D')

plt.tight_layout()
plt.savefig('assets/deck_images/chart_telemetry_combo.png', dpi=200, facecolor='#0B1224')
plt.close()
print("Saved chart_telemetry_combo.png")

# -----------------------------------------------------------------------------
# 4. Comparative Advantage Radar Chart
# -----------------------------------------------------------------------------
categories = ['Math Grounding', 'Audit Traceability', 'HITL Governance', 'Enterprise RAG', 'Multi-Agent State', 'Sovereign Enclave']
N = len(categories)

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

nexus_scores = [10.0, 9.8, 10.0, 9.5, 9.8, 9.6]
nexus_scores += nexus_scores[:1]

chatbot_scores = [3.0, 2.0, 1.5, 4.0, 2.0, 3.5]
chatbot_scores += chatbot_scores[:1]

fig, ax = plt.subplots(figsize=(6, 5), subplot_kw=dict(polar=True), facecolor='#0B1224')
ax.set_facecolor('#0B1224')

plt.xticks(angles[:-1], categories, color='#CBD5E1', size=8.5, fontweight='bold')
ax.tick_params(colors='#64748B', pad=12)
ax.set_rlabel_position(0)
plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="#64748B", size=7)
plt.ylim(0, 10.5)

# Plot NEXUS
ax.plot(angles, nexus_scores, linewidth=2.2, linestyle='solid', color='#00F5FF', label='NEXUS AI Swarm')
ax.fill(angles, nexus_scores, '#00F5FF', alpha=0.25)

# Plot Generic Chatbots
ax.plot(angles, chatbot_scores, linewidth=1.8, linestyle='dashed', color='#EF4444', label='Traditional LLM Chatbots')
ax.fill(angles, chatbot_scores, '#EF4444', alpha=0.15)

ax.grid(color='#1F2E4D')
ax.spines['polar'].set_color('#1F2E4D')
plt.title("NEXUS AI vs. Traditional LLM Solutions", color='#FFFFFF', size=11, fontweight='bold', y=1.1)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.15), facecolor='#111A2E', edgecolor='#1F2E4D', labelcolor='#CBD5E1', fontsize=8)

plt.tight_layout()
plt.savefig('assets/deck_images/chart_radar_comparison.png', dpi=200, facecolor='#0B1224')
plt.close()
print("Saved chart_radar_comparison.png")

# -----------------------------------------------------------------------------
# 5. ROI & Impact Graphic
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4), facecolor='#0B1224')
ax.set_facecolor('#0B1224')

metrics = ['Analysis Cycle Time', 'Math Hallucination', 'Regulatory Risk Cost', 'Decision Velocity']
before = [100, 100, 100, 100]
after = [18, 0, 12, 480]

x = np.arange(len(metrics))
width = 0.35

rects1 = ax.bar(x - width/2, before, width, label='Legacy Manual Operations', color='#64748B')
rects2 = ax.bar(x + width/2, after, width, label='NEXUS AI Orchestrated Swarm', color='#38BDF8')

ax.set_ylabel('Normalized Operational Metric (%)', color='#94A3B8', fontsize=8.5)
ax.set_title('Quantified Enterprise Efficiency & Risk Reduction Impact', color='#FFFFFF', fontsize=10.5, fontweight='bold', pad=12)
ax.set_xticks(x)
ax.set_xticklabels(metrics, color='#CBD5E1', fontsize=9, fontweight='bold')
ax.tick_params(colors='#64748B')
ax.grid(color='#1F2E4D', linestyle='--', alpha=0.5, axis='y')
ax.legend(facecolor='#111A2E', edgecolor='#1F2E4D', labelcolor='#CBD5E1', fontsize=8.5)
for spine in ax.spines.values():
    spine.set_color('#1F2E4D')

plt.tight_layout()
plt.savefig('assets/deck_images/chart_roi_impact.png', dpi=200, facecolor='#0B1224')
plt.close()
print("Saved chart_roi_impact.png")
print("All deck visual assets generated successfully!")
