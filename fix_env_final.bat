@echo off
chcp 65001 >nul
cls

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║     🔧 SOLUTION DÉFINITIVE - Résolution conflits LangChain      ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

set ENV_NAME=rag-chatbot-env

echo 📋 Ce script va:
echo    1. Supprimer complètement l'environnement existant
echo    2. Nettoyer tous les caches
echo    3. Créer un nouvel environnement propre
echo    4. Installer les packages dans le BON ORDRE
echo    5. Utiliser les VERSIONS COMPATIBLES testées
echo.
pause

REM ============================================
REM 1. NETTOYAGE COMPLET
REM ============================================

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║ ÉTAPE 1/5 : Nettoyage complet                                   ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo 🗑️  Désactivation de tous les environnements...
call conda deactivate 2>nul
call conda deactivate 2>nul
call conda deactivate 2>nul

echo 🗑️  Suppression de l'environnement %ENV_NAME%...
call conda env remove -n %ENV_NAME% -y 2>nul

echo 🧹 Nettoyage du cache pip...
pip cache purge 2>nul

echo 🧹 Nettoyage du cache conda...
call conda clean --all -y

echo ✓ Nettoyage terminé
echo.

REM ============================================
REM 2. CRÉATION ENVIRONNEMENT
REM ============================================

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║ ÉTAPE 2/5 : Création de l'environnement                         ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo 🔨 Création de l'environnement avec Python 3.10...
call conda create -n %ENV_NAME% python=3.10 -y

if %ERRORLEVEL% NEQ 0 (
    echo ❌ ERREUR: Impossible de créer l'environnement
    pause
    exit /b 1
)

echo ✓ Environnement créé
echo.

REM ============================================
REM 3. ACTIVATION
REM ============================================

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║ ÉTAPE 3/5 : Activation de l'environnement                       ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

call conda activate %ENV_NAME%

if %ERRORLEVEL% NEQ 0 (
    echo ❌ ERREUR: Impossible d'activer l'environnement
    pause
    exit /b 1
)

echo ✓ Environnement activé: %ENV_NAME%
echo.

REM ============================================
REM 4. MISE À JOUR PIP
REM ============================================

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║ ÉTAPE 4/5 : Mise à jour de pip                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

python -m pip install --upgrade pip setuptools wheel

echo ✓ pip mis à jour
echo.

REM ============================================
REM 5. INSTALLATION PACKAGES (ORDRE CRITIQUE)
REM ============================================

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║ ÉTAPE 5/5 : Installation des packages                           ║
echo ║             (Cela peut prendre 10-15 minutes)                   ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo ⚠️  IMPORTANT: Installation dans un ordre PRÉCIS pour éviter les conflits
echo.

REM Groupe 1: Dépendances de base
echo [Groupe 1/6] Dépendances de base...
echo    • numpy
pip install numpy==1.24.3

echo    • tiktoken
pip install tiktoken==0.5.2

echo.

REM Groupe 2: LangChain CORE (ordre important!)
echo [Groupe 2/6] LangChain Core (ORDRE CRITIQUE)...
echo    • langsmith (en premier!)
pip install langsmith==0.1.55

echo    • langchain-core
pip install langchain-core==0.1.52

echo    • langchain
pip install langchain==0.1.16

echo    • langchain-community
pip install langchain-community==0.0.38

echo.

REM Groupe 3: Embeddings
echo [Groupe 3/6] Modèles d'embeddings...
echo    • sentence-transformers
pip install "sentence-transformers>=2.6.0"

echo    • langchain-huggingface
pip install langchain-huggingface==0.0.1

echo.

REM Groupe 4: Vector Store et LLM
echo [Groupe 4/6] FAISS et Ollama...
echo    • faiss-cpu
pip install faiss-cpu==1.7.4

echo    • ollama
pip install ollama==0.1.6

echo.

REM Groupe 5: Document Loaders
echo [Groupe 5/6] Document loaders...
pip install pypdf==3.17.4
pip install python-docx==1.1.0
pip install beautifulsoup4==4.12.2
pip install lxml==5.1.0
pip install python-pptx==0.6.23
pip install unstructured==0.11.8

echo.

REM Groupe 6: API et Interface
echo [Groupe 6/6] FastAPI et Streamlit...
pip install fastapi==0.109.0
pip install "uvicorn[standard]==0.27.0"
pip install python-multipart==0.0.6
pip install pydantic==2.5.3
pip install streamlit==1.29.0
pip install requests==2.31.0
pip install python-dotenv==1.0.0

echo.
echo ✓ Toutes les installations terminées
echo.

REM ============================================
REM VÉRIFICATION
REM ============================================

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║ VÉRIFICATION DE L'INSTALLATION                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Test des imports critiques...
echo.

python -c "import langchain; print('✓ langchain:', langchain.__version__)" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ langchain - ERREUR
    goto :error
)

python -c "import langchain_community; print('✓ langchain-community')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ langchain-community - ERREUR
    goto :error
)

python -c "import langchain_core; print('✓ langchain-core')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ langchain-core - ERREUR
    goto :error
)

python -c "import langsmith; print('✓ langsmith')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ langsmith - ERREUR
    goto :error
)

python -c "import sentence_transformers; print('✓ sentence-transformers:', sentence_transformers.__version__)" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ sentence-transformers - ERREUR
    goto :error
)

python -c "import faiss; print('✓ faiss-cpu')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ faiss-cpu - ERREUR
    goto :error
)

python -c "import fastapi; print('✓ fastapi:', fastapi.__version__)" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ fastapi - ERREUR
    goto :error
)

python -c "import streamlit; print('✓ streamlit:', streamlit.__version__)" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ streamlit - ERREUR
    goto :error
)

echo.
echo ✅ Tous les packages critiques sont installés et fonctionnels
goto :success

:error
echo.
echo ❌ ERREUR: Certains packages ne sont pas correctement installés
echo.
echo 💡 Solutions:
echo    1. Relancez ce script: fix_env_final.bat
echo    2. Vérifiez votre connexion internet
echo    3. Consultez les logs d'erreur ci-dessus
echo.
pause
exit /b 1

:success
REM ============================================
REM CRÉATION DOSSIERS
REM ============================================

echo.
echo 📁 Création des dossiers du projet...
if not exist "data\raw" mkdir data\raw
if not exist "data\processed" mkdir data\processed
if not exist "data\vectordb" mkdir data\vectordb
if not exist "logs" mkdir logs

echo ✓ Dossiers créés
echo.

REM ============================================
REM SUCCÈS
REM ============================================

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    ✅ INSTALLATION RÉUSSIE                       ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 🎉 L'environnement est prêt à l'emploi!
echo.
echo 📊 Versions installées:
python -c "import langchain, streamlit, fastapi; print(f'   • LangChain: {langchain.__version__}'); print(f'   • Streamlit: {streamlit.__version__}'); print(f'   • FastAPI: {fastapi.__version__}')"
echo.
echo 🚀 PROCHAINES ÉTAPES:
echo.
echo    1. L'environnement est déjà activé (%ENV_NAME%)
echo.
echo    2. Téléchargez le modèle LLM:
echo       ollama pull llama3
echo.
echo    3. Lancez le projet:
echo       run.bat
echo.
echo 💡 Pour réactiver l'environnement plus tard:
echo     conda activate %ENV_NAME%
echo.
echo 📝 Sauvegarde de la configuration...

REM Sauvegarder les versions
(
echo ENV_NAME=%ENV_NAME%
echo PYTHON_VERSION=3.10
echo CREATED_DATE=%date% %time%
echo LANGCHAIN_VERSION=0.1.16
echo STREAMLIT_VERSION=1.29.0
echo FASTAPI_VERSION=0.109.0
) > .env_info

echo ✓ Configuration sauvegardée dans .env_info
echo.

pause