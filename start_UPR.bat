@echo off
cd /d "%~dp0"
echo 🚀 Starte Unified Promise Registry Server...
start cmd /k "uvicorn promise_server:app --host 0.0.0.0 --port 8000"
timeout /t 5 >nul
echo 🔁 Starte Überwachung...
start cmd /k "python upr_polling.py"
echo 🌐 Öffne Browser...
start http://127.0.0.1:8000/promises
echo ✅ UPR läuft! Fenster können geöffnet bleiben.
pause
