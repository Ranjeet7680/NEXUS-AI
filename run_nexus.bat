@echo off
echo ========================================================
echo   NEXUS AI - Autonomous Multi-Agent Platform
echo   One Intelligent Platform. Multiple AI Agents.
echo ========================================================
echo.
echo Starting FastAPI Multi-Agent Orchestrator Gateway...
echo Web Command Center will be available at: http://localhost:8000
echo Swagger API Documentation available at: http://localhost:8000/docs
echo.
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
pause
