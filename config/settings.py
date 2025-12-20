"""
Configuration globale du projet RAG
VERSION OPTIMISÉE POUR MEILLEURES RÉPONSES
"""
import os
from pathlib import Path

# Chemins de base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
VECTORDB_DIR = DATA_DIR / "vectordb"

# Créer les dossiers s'ils n'existent pas
for directory in [RAW_DIR, PROCESSED_DIR, VECTORDB_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================
# Configuration du Text Splitter
# ============================================
# OPTIMISÉ : Chunks plus petits = meilleure précision
CHUNK_SIZE = 300  # ✅ MODIFIÉ de 700 à 300
CHUNK_OVERLAP = 50  # ✅ MODIFIÉ de 120 à 50

# ============================================
# Configuration des Embeddings
# ============================================
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DEVICE = "cpu"

# ============================================
# Configuration FAISS
# ============================================
FAISS_INDEX_PATH = VECTORDB_DIR / "faiss_index"
SEARCH_TOP_K = 3  # ✅ MODIFIÉ de 4 à 3 (moins de bruit)

# ============================================
# Configuration LLM
# ============================================
LLM_MODEL = "llama3"
LLM_TEMPERATURE = 0.0  # ✅ MODIFIÉ de 0.1 à 0.0 (plus déterministe)
LLM_MAX_TOKENS = 2000  # ✅ MODIFIÉ de 500 à 2000 (réponses plus longues)

# ============================================
# Configuration RAG
# ============================================
RAG_CHAIN_TYPE = "stuff"

# ============================================
# Types de fichiers supportés
# ============================================
SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".html", ".pptx", ".txt"]  # ✅ AJOUTÉ .txt

# Configuration des logs
LOGGING_LEVEL = "INFO"