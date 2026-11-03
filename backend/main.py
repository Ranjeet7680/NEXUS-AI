import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.database import init_db
from backend.api import chat, agents, approvals, analytics, documents, settings, memory, voice

app = FastAPI(
    title="NEXUS AI - Autonomous Multi-Agent Intelligence Platform",
    description="One Intelligent Platform. Multiple AI Agents. Real-World Impact.",
    version="2.0.0"
)

# CORS middleware for development flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Register API Routers
app.include_router(chat.router)
app.include_router(agents.router)
app.include_router(approvals.router)
app.include_router(analytics.router)
app.include_router(documents.router)
app.include_router(settings.router)
app.include_router(memory.router)
app.include_router(voice.router)

# Static file serving
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    return {
        "status": "healthy",
        "platform": "NEXUS AI Enterprise Orchestration",
        "version": "2.0.0",
        "multi_agent_engine": "active",
        "gateway": "ready"
    }

@app.api_route("/", methods=["GET", "HEAD"])
def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "message": "NEXUS AI API Gateway is active. Visit /docs for Swagger API documentation or load the Command Center UI."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
