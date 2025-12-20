@echo off
chcp 65001 >nul
cls

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          🤖 RAG LOCAL CHATBOT - Lancement du système 🤖         ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Vérifier l'environnement Conda
echo 🔍 Vérification de l'environnement Conda...

if "%CONDA_DEFAULT_ENV%"=="" (
    echo ⚠️  Aucun environnement Conda activé
    echo.
    echo 💡 Activez l'environnement avec:
    echo    activate.bat
    echo    ou
    echo    conda activate rag-chatbot-env
    echo.
    set /p choice="Voulez-vous continuer quand même? (o/n): "
    if /i not "%choice%"=="o" exit /b
) else (
    if not "%CONDA_DEFAULT_ENV%"=="rag-chatbot-env" (
        echo ⚠️  Environnement actuel: %CONDA_DEFAULT_ENV%
        echo 💡 Environnement recommandé: rag-chatbot-env
        echo.
        set /p choice="Voulez-vous continuer? (o/n): "
        if /i not "%choice%"=="o" exit /b
    ) else (
        echo ✓ Environnement Conda correct: %CONDA_DEFAULT_ENV%
    )
)

echo.

REM Créer le dossier logs s'il n'existe pas
if not exist "logs" mkdir logs

echo 🔍 Vérification d'Ollama...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo ⚠️  Ollama n'est pas lancé
    echo 💡 Lancez-le avec: ollama serve
    echo.
    set /p choice="Voulez-vous continuer quand même? (o/n): "
    if /i not "%choice%"=="o" exit /b
) else (
    echo ✓ Ollama est actif
)

echo.

REM Vérifier si le port 8000 est libre
netstat -ano | findstr ":8000" >nul
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  Port 8000 déjà utilisé
    set /p choice="Arrêter le processus? (o/n): "
    if /i "%choice%"=="o" (
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do taskkill /F /PID %%a >nul 2>&1
        echo ✓ Port 8000 libéré
    )
)

REM Vérifier si le port 8501 est libre
netstat -ano | findstr ":8501" >nul
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  Port 8501 déjà utilisé
    set /p choice="Arrêter le processus? (o/n): "
    if /i "%choice%"=="o" (
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8501"') do taskkill /F /PID %%a >nul 2>&1
        echo ✓ Port 8501 libéré
    )
)

echo.

REM Lancer FastAPI
echo 🚀 Démarrage de FastAPI (Backend)...
start /B python -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload > logs\fastapi.log 2>&1

REM Attendre 3 secondes
timeout /t 3 /nobreak >nul

REM Vérifier si FastAPI a démarré
netstat -ano | findstr ":8000" >nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ FastAPI lancé sur http://localhost:8000
) else (
    echo ❌ Erreur: FastAPI n'a pas démarré
    echo 📄 Logs:
    type logs\fastapi.log
    exit /b 1
)

echo.

REM Lancer Streamlit
echo 🌐 Démarrage de Streamlit (Frontend)...
start /B streamlit run app\ui\streamlit_app.py --server.port 8501 --server.headless true > logs\streamlit.log 2>&1

REM Attendre 3 secondes
timeout /t 3 /nobreak >nul

REM Vérifier si Streamlit a démarré
netstat -ano | findstr ":8501" >nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ Streamlit lancé sur http://localhost:8501
) else (
    echo ❌ Erreur: Streamlit n'a pas démarré
    echo 📄 Logs:
    type logs\streamlit.log
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    ✅ SYSTÈME OPÉRATIONNEL                       ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 🐍 Environnement: %CONDA_DEFAULT_ENV%
echo 📍 Interface : http://localhost:8501
echo 📍 API       : http://localhost:8000
echo 📍 Docs API  : http://localhost:8000/docs
echo.
echo 💡 Fermez cette fenêtre pour arrêter les services
echo 📄 Logs: logs\fastapi.log, logs\streamlit.log
echo.

REM Ouvrir le navigateur
start http://localhost:8501

REM Attendre
pause