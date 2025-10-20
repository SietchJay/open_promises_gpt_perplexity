@echo off
title Unified Promise Registry - Starter
color 0a
echo =============================================
echo     🚀 Starte Unified Promise Registry
echo =============================================
echo.

:: Projektpfad anpassen, falls nötig
cd /d "%~dp0"

:: --- Starte Promise Server ---
echo [1/3] Starte Promise Server...
start "Promise Server" cmd /k "uvicorn promise_server:app --reload"

:: --- Kurze Pause ---
timeout /t 5 /nobreak >nul

:: --- Starte Cache Watcher ---
echo [2/3] Starte Cache Watcher...
start "Cache Watcher" cmd /k "python cache_watcher.py"

:: --- Kurze Pause ---
timeout /t 3 /nobreak >nul

:: --- Starte Selbstverpflichtungs-Agent ---
if exist self_commit_agent.py (
    echo [3/3] Starte Selbstverpflichtungs-Agent...
    start "Self-Commit Agent" cmd /k "python self_commit_agent.py"
) else (
    echo ⚠️ Kein self_commit_agent.py gefunden – übersprungen.
)

echo.
echo ✅ Alle Module gestartet!
echo.
pause
