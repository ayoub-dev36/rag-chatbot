@echo off
chcp 65001 >nul
cls

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║          🛑 ARRÊT DES PROCESSUS RAG CHATBOT                     ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Recherche des processus actifs...
echo.

REM Tuer les processus Python (uvicorn, streamlit)
echo 🗑️  Arrêt de Python/Uvicorn/Streamlit...
taskkill /F /IM python.exe 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ Processus Python arrêtés
) else (
    echo ℹ Aucun processus Python actif
)

REM Libérer le port 8000 (FastAPI)
echo.
echo 🔍 Libération du port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
    taskkill /F /PID %%a 2>nul
    echo ✓ Port 8000 libéré
    goto :port8501
)
echo ℹ Port 8000 déjà libre

:port8501
REM Libérer le port 8501 (Streamlit)
echo.
echo 🔍 Libération du port 8501...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8501"') do (
    taskkill /F /PID %%a 2>nul
    echo ✓ Port 8501 libéré
    goto :done
)
echo ℹ Port 8501 déjà libre

:done
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    ✅ PROCESSUS ARRÊTÉS                          ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 💡 Vous pouvez maintenant relancer: run.bat
echo.
pause