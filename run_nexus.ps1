Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  NEXUS AI - Autonomous Multi-Agent Platform" -ForegroundColor White
Write-Host "  One Intelligent Platform. Multiple AI Agents." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting FastAPI Multi-Agent Orchestrator Gateway..." -ForegroundColor Green
Write-Host "Web Command Center: http://localhost:8000" -ForegroundColor Yellow
Write-Host "Swagger API Docs:   http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""

Start-Process "http://localhost:8000"
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
