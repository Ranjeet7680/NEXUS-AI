import time
import uuid
from typing import Dict, Any, List, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/voice", tags=["Voice AI"])

class VoiceIntentRequest(BaseModel):
    transcript: str = Field(..., description="Transcribed voice text from user")
    language: Optional[str] = Field("en-US", description="Spoken language tag")
    hands_free: Optional[bool] = Field(False, description="Whether hands-free continuous mode is active")

class VoiceTurn(BaseModel):
    id: str
    user_transcript: str
    ai_response: str
    intent: str
    target_action: Optional[Dict[str, Any]] = None
    language: str
    timestamp: float

VOICE_HISTORY: List[Dict[str, Any]] = []

INTENT_MAP = [
    {
        "keywords": ["sales", "revenue", "product performance", "sales report", "বিক্রয়", "बिक्री", "விற்பனை"],
        "intent": "RUN_SALES_MISSION",
        "action": {
            "type": "NAVIGATE_AND_RUN",
            "target": "app-workspace",
            "scenario": "sales",
            "prompt": "Analyze this company's sales data, find the top-performing products, identify revenue risks, generate a management report, and prepare an email for the management team.",
            "dataset": "sample_sales_q3.csv"
        },
        "response_en": "Analyzing Q3 enterprise sales report. Activating Planner, Document, and Data Analyst agents.",
        "response_hi": "Q3 बिक्री रिपोर्ट का विश्लेषण शुरू कर रहे हैं। एजेंट सक्रिय कर दिए गए हैं।",
        "response_bn": "Q3 বিক্রয় রিপোর্ট বিশ্লেষণ শুরু করছি। এজেন্ট সক্রিয় করা হয়েছে।",
        "response_ta": "விற்பனை அறிக்கை பகுப்பாய்வு தொடங்குகிறது. முகவர்கள் இயக்கப்படுகிறார்கள்."
    },
    {
        "keywords": ["hospital", "clinical", "patient", "sla", "emergency", "स्वास्थ्य", "হাসপাতাল", "மருத்துவமனை"],
        "intent": "RUN_HEALTHCARE_MISSION",
        "action": {
            "type": "NAVIGATE_AND_RUN",
            "target": "app-workspace",
            "scenario": "healthcare",
            "prompt": "Analyze hospital clinical departmental operations, identify breached SLA wait times, evaluate patient flow bottlenecks, and draft an operational intervention brief.",
            "dataset": "healthcare_patient_ops.csv"
        },
        "response_en": "Initiating hospital clinical SLA audit. Inspecting Emergency triage latencies and ICU capacity bottlenecks.",
        "response_hi": "अस्पताल एसएलए और आपातकालीन विभाग का ऑडिट शुरू किया जा रहा है।",
        "response_bn": "হাসপাতাল এসএলএ ও জরুরি বিভাগের অডিট শুরু করা হচ্ছে।",
        "response_ta": "மருத்துவமனை அவசர பிரிவு கண்காணிப்பு தொடங்குகிறது."
    },
    {
        "keywords": ["active agents", "show agents", "agent status", "agents", "एजेंट", "এজেন্ট"],
        "intent": "NAVIGATE_AGENTS",
        "action": {
            "type": "NAVIGATE",
            "target": "app-agents"
        },
        "response_en": "Opening AI Agent Control Center. 8 specialized autonomous agents are currently active and healthy.",
        "response_hi": "एजेंट कंट्रोल सेंटर खोल रहे हैं। सभी 8 एजेंट सक्रिय हैं।",
        "response_bn": "এজেন্ট কন্ট্রোল সেন্টার খোলা হচ্ছে। ৮টি এজেন্ট সক্রিয় আছে।",
        "response_ta": "ஏஜென்ட் கண்ட்ரோல் சென்டர் திறக்கப்படுகிறது."
    },
    {
        "keywords": ["workflow", "node editor", "create workflow", "build workflow", "वर्कफ़्लो", "ওয়ার্কফ্লো"],
        "intent": "NAVIGATE_WORKFLOW",
        "action": {
            "type": "NAVIGATE",
            "target": "app-workflow-builder"
        },
        "response_en": "Switching to Visual Workflow Builder. Ready to drag and connect stateful agent nodes.",
        "response_hi": "विजुअल वर्कफ़्लो बिल्डर खोला जा रहा है।",
        "response_bn": "ভিজ্যুয়াল ওয়ার্কফ্লো বিল্ডার চালু করা হচ্ছে।",
        "response_ta": "விஷுவல் ஒர்க்ஃப்ளோ பில்டர் திறக்கப்படுகிறது."
    },
    {
        "keywords": ["approvals", "pending", "human in the loop", "sign off", "स्वीकृति", "অনুমোদন"],
        "intent": "NAVIGATE_APPROVALS",
        "action": {
            "type": "NAVIGATE",
            "target": "app-approvals"
        },
        "response_en": "Opening Approvals Center. Inspecting pending Tier-1 Human-in-the-Loop governance requests.",
        "response_hi": "अनुमोदन केंद्र खोल रहे हैं। मानवीय समीक्षा अनुरोध उपलब्ध हैं।",
        "response_bn": "অনুমোদন কেন্দ্র খোলা হচ্ছে।",
        "response_ta": "அங்கீகார மையம் திறக்கப்படுகிறது."
    },
    {
        "keywords": ["documents", "upload", "files", "csv", "दस्तावेज़", "নথি"],
        "intent": "NAVIGATE_DOCUMENTS",
        "action": {
            "type": "NAVIGATE",
            "target": "app-documents"
        },
        "response_en": "Opening Document Intelligence. Ready for CSV and PDF schema extraction.",
        "response_hi": "दस्तावेज़ इंटेलिजेंस हब खोला जा रहा है।",
        "response_bn": "ডকুমেন্ট ইন্টেলিজেন্স হাব খোলা হচ্ছে।",
        "response_ta": "ஆவண மேலாண்மை திறக்கப்படுகிறது."
    },
    {
        "keywords": ["overview", "analytics", "dashboard", "metrics", "डैशबोर्ड", "ড্যাশবোর্ড"],
        "intent": "NAVIGATE_OVERVIEW",
        "action": {
            "type": "NAVIGATE",
            "target": "app-overview"
        },
        "response_en": "Switching to Platform Operations Overview and throughput telemetry.",
        "response_hi": "डैशबोर्ड और सिस्टम टेलीमेट्री खोला जा रहा है।",
        "response_bn": "ড্যাশবোর্ড ও সিস্টেম টেলিমেট্রি খোলা হচ্ছে।",
        "response_ta": "முதன்மை டாஷ்போர்டு திறக்கப்படுகிறது."
    },
    {
        "keywords": ["approve", "authorize", "confirm action", "accept", "स्वीकृत", "मंज़ूर", "অনুমোদন করুন", "அங்கீகரிக்கவும்"],
        "intent": "APPROVE_ACTION",
        "action": {
            "type": "SUBMIT_APPROVAL",
            "decision": "approve"
        },
        "response_en": "Cryptographic authorization acknowledged. Resuming state machine and dispatching external action.",
        "response_hi": "स्वीकृति दर्ज की गई। वर्कफ़्लो फिर से शुरू हो रहा है।",
        "response_bn": "অনুমোদন সম্পন্ন হয়েছে। ওয়ার্কফ্লো পুনরায় চালু হচ্ছে।",
        "response_ta": "அங்கீகாரம் உறுதி செய்யப்பட்டது. பணி தொடர்கிறது."
    },
    {
        "keywords": ["reject", "halt action", "cancel dispatch", "disapprove", "रद्द", "खारिज", "நிராகரிக்கவும்"],
        "intent": "REJECT_ACTION",
        "action": {
            "type": "SUBMIT_APPROVAL",
            "decision": "reject"
        },
        "response_en": "Sensitive external action rejected by operator. Execution terminated safely.",
        "response_hi": "कार्यवाही अस्वीकार कर दी गई है।",
        "response_bn": "পদক্ষেপটি বাতিল করা হয়েছে।",
        "response_ta": "செயல் நிராகரிக்கப்பட்டது."
    },
    {
        "keywords": ["marketplace", "store", "install agent", "मार्केटप्लेस"],
        "intent": "NAVIGATE_MARKETPLACE",
        "action": {
            "type": "NAVIGATE",
            "target": "app-marketplace"
        },
        "response_en": "Opening Enterprise Agent Marketplace. Browse pre-configured specialized agents.",
        "response_hi": "एजेंट मार्केटप्लेस खोला जा रहा है।",
        "response_bn": "এজেন্ট মার্কেটপ্লেস খোলা হচ্ছে।",
        "response_ta": "ஏஜென்ட் அங்காடி திறக்கப்படுகிறது."
    },
    {
        "keywords": ["memory", "knowledge base", "vector", "rag", "मेमोरी", "ज्ञान भंडार"],
        "intent": "NAVIGATE_MEMORY",
        "action": {
            "type": "NAVIGATE",
            "target": "app-memory"
        },
        "response_en": "Opening Enterprise Semantic Memory and Vector Knowledge Base.",
        "response_hi": "सिमेंटिक मेमोरी और नॉलेज बेस खोला जा रहा है।",
        "response_bn": "মেমরি এবং নলেজ বেস খোলা হচ্ছে।",
        "response_ta": "நினைவக களஞ்சியம் திறக்கப்படுகிறது."
    },
    {
        "keywords": ["history", "audit log", "ledger", "tasks history", "इतिहास", "ऑडिट"],
        "intent": "NAVIGATE_HISTORY",
        "action": {
            "type": "NAVIGATE",
            "target": "app-history"
        },
        "response_en": "Opening Execution History and cryptographic audit ledger.",
        "response_hi": "टास्क इतिहास और ऑडिट लेजर खोला जा रहा है।",
        "response_bn": "কাজের ইতিহাস ও অডিট লেজার খোলা হচ্ছে।",
        "response_ta": "பணி வரலாறு திறக்கப்படுகிறது."
    },
    {
        "keywords": ["settings", "configuration", "api keys", "providers", "सेटिंग्स"],
        "intent": "NAVIGATE_SETTINGS",
        "action": {
            "type": "NAVIGATE",
            "target": "app-settings"
        },
        "response_en": "Opening Settings and LLM Provider configuration.",
        "response_hi": "सेटिंग्स और मॉडल कॉन्फ़िगरेशन खोला जा रहा है।",
        "response_bn": "সেটিংস খোলা হচ্ছে।",
        "response_ta": "அமைப்புகள் திறக்கப்படுகிறது."
    }
]

@router.post("/intent")
def parse_voice_intent(payload: VoiceIntentRequest):
    text_lower = payload.transcript.lower().strip()
    lang = payload.language or "en-US"

    matched_intent = None
    for entry in INTENT_MAP:
        for kw in entry["keywords"]:
            if kw.lower() in text_lower:
                matched_intent = entry
                break
        if matched_intent:
            break

    if matched_intent:
        resp_text = matched_intent.get("response_en", "Command acknowledged.")
        if lang.startswith("hi"):
            resp_text = matched_intent.get("response_hi", resp_text)
        elif lang.startswith("bn"):
            resp_text = matched_intent.get("response_bn", resp_text)
        elif lang.startswith("ta"):
            resp_text = matched_intent.get("response_ta", resp_text)

        turn = {
            "id": f"turn_{uuid.uuid4().hex[:8]}",
            "user_transcript": payload.transcript,
            "ai_response": resp_text,
            "intent": matched_intent["intent"],
            "target_action": matched_intent["action"],
            "language": lang,
            "timestamp": time.time()
        }
    else:
        # Generic Query / AI Conversational Response
        resp_text = f"I heard: '{payload.transcript}'. Routing to NEXUS AI Planner and Knowledge Engine."
        turn = {
            "id": f"turn_{uuid.uuid4().hex[:8]}",
            "user_transcript": payload.transcript,
            "ai_response": resp_text,
            "intent": "GENERAL_QUERY",
            "target_action": {
                "type": "GENERAL_QUERY",
                "prompt": payload.transcript
            },
            "language": lang,
            "timestamp": time.time()
        }

    VOICE_HISTORY.insert(0, turn)
    if len(VOICE_HISTORY) > 50:
        VOICE_HISTORY.pop()

    return turn

@router.get("/history")
def get_voice_history():
    return {
        "count": len(VOICE_HISTORY),
        "history": VOICE_HISTORY
    }

@router.delete("/history")
def clear_voice_history():
    VOICE_HISTORY.clear()
    return {"status": "cleared", "message": "Voice conversation history reset."}
