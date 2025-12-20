# 🤖 RAG Local Chatbot

<div align="center">

**Système de Question-Réponse Intelligent basé sur vos Documents**

![Python](https://img.shields.io/badge/Python-3.10-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.1.20-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-teal)
![Streamlit](https://img.shields.io/badge/Streamlit-1.34.0-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

*Chatbot RAG 100% local utilisant LangChain, LLaMA et FAISS*

[Fonctionnalités](#-fonctionnalités) • [Architecture](#-architecture) • [Installation](#-installation) • [Utilisation](#-utilisation) • [Documentation](#-documentation)

</div>

---

## 📋 Table des matières

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Technologies utilisées](#-technologies-utilisées)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Structure du projet](#-structure-du-projet)
- [Pipeline RAG](#-pipeline-rag)
- [API Endpoints](#-api-endpoints)
- [Dépannage](#-dépannage)
- [Contribution](#-contribution)
- [Licence](#-licence)

---

## 🎯 À propos

**RAG Local Chatbot** est un système de Question-Réponse intelligent qui permet d'interroger vos documents (PDF, DOCX, HTML, PPTX, TXT) en langage naturel. Contrairement aux solutions cloud, ce chatbot fonctionne **100% en local**, garantissant la confidentialité de vos données.

### Cas d'usage

- 📚 **Documentation d'entreprise** : Interrogez votre base de connaissances
- 🎓 **Éducation** : Posez des questions sur vos cours et supports de formation
- 📊 **Analyse de documents** : Extrayez rapidement des informations de rapports
- 🔍 **Recherche** : Explorez des corpus documentaires volumineux

---

## ✨ Fonctionnalités

### 🚀 Fonctionnalités principales

- ✅ **100% Local** : Aucune donnée envoyée vers le cloud
- ✅ **Multi-formats** : Support PDF, DOCX, HTML, PPTX, TXT
- ✅ **Interface moderne** : UI Streamlit élégante avec thème sombre
- ✅ **API REST** : FastAPI pour intégration facile
- ✅ **RAG optimisé** : Chunking intelligent, embeddings locaux, FAISS
- ✅ **Anti-hallucination** : Réponses strictement basées sur vos documents
- ✅ **Sources citées** : Traçabilité complète des réponses
- ✅ **Scalable** : Architecture modulaire et extensible

### 🎨 Interface utilisateur

- 🌑 Thème sombre professionnel
- 📤 Upload par drag & drop
- 💬 Chat interactif avec historique
- 📚 Affichage des sources
- 📊 Tableau de bord en temps réel
- 🔄 Indexation en un clic

---

## 🏗️ Architecture

### Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFACE STREAMLIT                      │
│              (Port 8501 - Frontend Web)                     │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      API FASTAPI                            │
│              (Port 8000 - Backend REST)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    PIPELINE RAG                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Loader    │→ │   Cleaner    │→ │   Chunker    │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Embeddings  │→ │    FAISS     │→ │  Retriever   │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    LLM      │→ │  RAG Chain   │→ │   Response   │      │
│  │  (LLaMA)    │  │              │  │   + Sources  │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Flux de données

```
Upload → Loader → Cleaner → Chunker → Embeddings → FAISS Index
                                                        ↓
Question → Embedding → FAISS Search → Retriever → Prompt + Context → LLM → Réponse
```

---

## 🛠️ Technologies utilisées

### Core Framework

| Technologie | Version | Utilisation |
|------------|---------|-------------|
| **Python** | 3.10 | Langage principal |
| **LangChain** | 0.1.20 | Framework RAG |
| **FastAPI** | 0.111.0 | Backend REST API |
| **Streamlit** | 1.34.0 | Interface utilisateur |
| **Uvicorn** | 0.29.0 | Serveur ASGI |

### IA & Machine Learning

| Technologie | Version | Utilisation |
|------------|---------|-------------|
| **Ollama** | 0.1.9 | Runtime LLM local |
| **LLaMA 3** | - | Modèle de langage |
| **Sentence Transformers** | 2.7.0 | Embeddings |
| **FAISS** | 1.8.0 | Base vectorielle |
| **HuggingFace** | - | Modèles d'embeddings |

### Document Processing

| Technologie | Version | Utilisation |
|------------|---------|-------------|
| **PyPDF** | 4.2.0 | Lecture PDF |
| **python-docx** | 1.1.0 | Lecture DOCX |
| **beautifulsoup4** | 4.12.3 | Parsing HTML |
| **python-pptx** | 0.6.23 | Lecture PPTX |
| **unstructured** | 0.13.0 | Parsing avancé |

---

## 📋 Prérequis

### Système

- **OS** : Windows 10/11, Linux, macOS
- **RAM** : Minimum 8 GB (16 GB recommandé)
- **Stockage** : 10 GB d'espace libre
- **CPU** : Processeur multi-cœurs recommandé
- **GPU** : Optionnel (accélération CUDA)

### Logiciels

1. **Anaconda ou Miniconda**
   - Télécharger : [https://www.anaconda.com/download](https://www.anaconda.com/download)

2. **Ollama**
   - Télécharger : [https://ollama.ai](https://ollama.ai)
   - Installer le modèle LLaMA 3 : `ollama pull llama3`

3. **Git** (optionnel)
   - Pour cloner le repository

---

## 🚀 Installation

### Méthode 1 : Installation automatique (Recommandé)

#### Windows

```batch
# 1. Cloner le projet
git clone <votre-repo-url>
cd LearningLocal

# 2. Lancer l'installation automatique
install_FINAL.bat

# 3. Télécharger le modèle LLM
ollama pull llama3
```

#### Linux/macOS

```bash
# 1. Cloner le projet
git clone <votre-repo-url>
cd LearningLocal

# 2. Rendre les scripts exécutables
chmod +x *.sh

# 3. Lancer l'installation
./install_FINAL.sh

# 4. Télécharger le modèle LLM
ollama pull llama3
```

### Méthode 2 : Installation manuelle

```bash
# 1. Créer l'environnement Conda
conda create -n rag-chatbot-env python=3.10 -y
conda activate rag-chatbot-env

# 2. Installer les dépendances
pip install -r requirements_FINAL.txt

# 3. Créer la structure des dossiers
mkdir -p data/raw data/processed data/vectordb logs

# 4. Télécharger le modèle LLM
ollama pull llama3
```

### Vérification de l'installation

```bash
# Activer l'environnement
conda activate rag-chatbot-env

# Tester les imports
python -c "import langchain, streamlit, fastapi; print('✅ Installation OK')"

# Vérifier Ollama
ollama list
```

---

## ⚙️ Configuration

### Fichier `config/settings.py`

Personnalisez les paramètres du système :

```python
# Chunking
CHUNK_SIZE = 300          # Taille des chunks (caractères)
CHUNK_OVERLAP = 50        # Chevauchement entre chunks

# Embeddings
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DEVICE = "cpu"  # ou "cuda" si GPU

# FAISS
SEARCH_TOP_K = 3          # Nombre de documents à récupérer

# LLM
LLM_MODEL = "llama3"      # Modèle Ollama
LLM_TEMPERATURE = 0.0     # Créativité (0.0 = déterministe)
LLM_MAX_TOKENS = 2000     # Longueur max de réponse
```

### Variables d'environnement (optionnel)

Créez un fichier `.env` :

```bash
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_PORT=8501
```

---

## 🎮 Utilisation

### Démarrage rapide

#### 1. Activer l'environnement

```batch
conda activate rag-chatbot-env
```

#### 2. Lancer Ollama (terminal séparé)

```batch
ollama serve
```

#### 3. Ajouter des documents

Placez vos fichiers dans le dossier `data/raw/` :

```
data/raw/
├── cours_python.pdf
├── rapport_2024.docx
└── documentation.html
```

#### 4. Indexer les documents

```batch
python scripts/ingest_simple.py
```

**Sortie attendue :**
```
✅ INGESTION TERMINÉE
   • Documents chargés : 3
   • Chunks créés : 45
   • Index FAISS : Prêt
```

#### 5. Lancer l'interface

```batch
# Windows
run.bat

# Linux/macOS
./run.sh
```

#### 6. Accéder à l'interface

Ouvrez votre navigateur : **http://localhost:8501**

---

## 📁 Structure du projet

```
LearningLocal/
│
├── 📂 app/                          # Code source principal
│   ├── 📂 api/                      # Backend FastAPI
│   │   ├── __init__.py
│   │   └── main.py                  # Endpoints REST
│   │
│   ├── 📂 ui/                       # Interface Streamlit
│   │   ├── __init__.py
│   │   └── streamlit_app.py         # Frontend web
│   │
│   ├── 📂 loaders/                  # Chargement documents
│   │   ├── __init__.py
│   │   └── document_loader.py       # PyPDF, Docx, HTML, PPTX
│   │
│   ├── 📂 preprocess/               # Nettoyage texte
│   │   ├── __init__.py
│   │   └── text_cleaner.py          # Normalisation Unicode
│   │
│   ├── 📂 chunking/                 # Découpage texte
│   │   ├── __init__.py
│   │   └── text_splitter.py         # RecursiveCharacterTextSplitter
│   │
│   ├── 📂 embeddings/               # Génération embeddings
│   │   ├── __init__.py
│   │   └── embedding_model.py       # HuggingFace Embeddings
│   │
│   ├── 📂 vectorstore/              # Base vectorielle
│   │   ├── __init__.py
│   │   └── faiss_store.py           # FAISS Index
│   │
│   ├── 📂 retriever/                # Recherche sémantique
│   │   ├── __init__.py
│   │   └── similarity_search.py     # Similarité cosinus
│   │
│   ├── 📂 llm/                      # Modèle de langage
│   │   ├── __init__.py
│   │   └── llama_model.py           # Ollama LLaMA
│   │
│   ├── 📂 rag/                      # Pipeline RAG
│   │   ├── __init__.py
│   │   └── rag_pipeline.py          # RetrievalQA Chain
│   │
│   └── 📂 prompts/                  # Templates de prompts
│       └── rag_prompt.txt           # Prompt optimisé
│
├── 📂 config/                       # Configuration
│   └── settings.py                  # Paramètres globaux
│
├── 📂 data/                         # Données
│   ├── raw/                         # Documents originaux
│   ├── processed/                   # Documents nettoyés
│   └── vectordb/                    # Index FAISS
│
├── 📂 logs/                         # Fichiers de logs
│   ├── fastapi.log                  # Logs API
│   └── streamlit.log                # Logs UI
│
├── 📂 scripts/                      # Scripts utilitaires
│   ├── ingest.py                    # Indexation complète
│   ├── ingest_simple.py             # Indexation simplifiée
│   └── chat.py                      # Chat en ligne de commande
│
├── 📄 install_FINAL.bat             # Installation Windows
├── 📄 fix_env_final.bat             # Résolution problèmes
├── 📄 run.bat                       # Lancement Windows
├── 📄 kill_processes.bat            # Arrêt processus
├── 📄 check_ports.bat               # Diagnostic ports
│
├── 📄 requirements_FINAL.txt        # Dépendances Python (versions testées)
├── 📄 environment.yml               # Config environnement Conda
│
├── 📄 .gitignore                    # Fichiers à ignorer
├── 📄 README.md                     # Ce fichier
└── 📄 LICENSE                       # Licence MIT
```

---

## 🔄 Pipeline RAG Détaillé

### 1️⃣ Ingestion des documents

```
Documents bruts (PDF, DOCX, etc.)
         ↓
    Loader (PyPDF, python-docx, etc.)
         ↓
    Document LangChain
         ↓
    Text Cleaner (normalisation Unicode, suppression caractères)
         ↓
    Text Splitter (chunks de 300 caractères, overlap 50)
         ↓
    Embeddings (sentence-transformers/all-MiniLM-L6-v2)
         ↓
    FAISS Index (sauvegardé localement)
```

### 2️⃣ Génération de réponse

```
Question utilisateur
         ↓
    Embedding de la question
         ↓
    FAISS Similarity Search (top_k=3)
         ↓
    Documents pertinents récupérés
         ↓
    Construction du prompt (Context + Question)
         ↓
    LLM (LLaMA 3 via Ollama)
         ↓
    Réponse + Sources citées
```

### Paramètres optimisés

| Paramètre | Valeur | Justification |
|-----------|--------|---------------|
| Chunk Size | 300 | Chunks focalisés, moins de bruit |
| Chunk Overlap | 50 | Continuité sémantique |
| Top K | 3 | Équilibre pertinence/contexte |
| Temperature | 0.0 | Réponses déterministes |
| Max Tokens | 2000 | Réponses détaillées possibles |

---

## 🌐 API Endpoints

### Base URL : `http://localhost:8000`

#### `GET /`
Page d'accueil de l'API

**Réponse :**
```json
{
  "status": "online",
  "message": "API RAG Local Chatbot opérationnelle",
  "details": {
    "version": "1.0.0",
    "endpoints": ["/upload", "/ingest", "/query", "/status"]
  }
}
```

#### `GET /status`
Statut du système

**Réponse :**
```json
{
  "status": "ready",
  "message": "Système prêt",
  "details": {
    "index_exists": true,
    "rag_initialized": true,
    "files_uploaded": 5,
    "supported_extensions": [".pdf", ".docx", ".html", ".pptx", ".txt"],
    "search_top_k": 3
  }
}
```

#### `POST /upload`
Upload de fichiers

**Body :** `multipart/form-data`

**Réponse :**
```json
{
  "status": "success",
  "message": "3 fichier(s) uploadé(s)",
  "details": {
    "uploaded": ["cours.pdf", "rapport.docx"],
    "errors": null
  }
}
```

#### `POST /ingest`
Indexation des documents

**Réponse :**
```json
{
  "status": "success",
  "message": "Documents indexés avec succès",
  "details": {
    "documents_loaded": 10,
    "chunks_created": 145,
    "files_processed": 3
  }
}
```

#### `POST /query`
Question aux documents

**Body :**
```json
{
  "question": "Qu'est-ce que Python ?",
  "top_k": 3
}
```

**Réponse :**
```json
{
  "answer": "Python est un langage de programmation...",
  "sources": [
    {
      "source": "cours.pdf",
      "page": "2",
      "content": "Python est un langage..."
    }
  ],
  "success": true
}
```

#### `DELETE /reset`
Réinitialisation du système

**Réponse :**
```json
{
  "status": "success",
  "message": "Système réinitialisé"
}
```

---

## 🐛 Dépannage

### Problème : "API non accessible"

**Cause :** FastAPI n'est pas lancé

**Solution :**
```batch
# Vérifier les processus
check_ports.bat

# Lancer FastAPI manuellement
python -m uvicorn app.api.main:app --reload
```

### Problème : "Ollama non trouvé"

**Cause :** Ollama n'est pas installé ou pas lancé

**Solution :**
```batch
# Vérifier Ollama
ollama list

# Lancer le service
ollama serve

# Télécharger le modèle
ollama pull llama3
```

### Problème : "Index FAISS introuvable"

**Cause :** Documents pas indexés

**Solution :**
```batch
# Ajouter des documents dans data/raw/
# Puis indexer
python scripts/ingest_simple.py
```

### Problème : "Port déjà utilisé"

**Cause :** Un processus utilise déjà le port 8000 ou 8501

**Solution :**
```batch
# Arrêter les processus
kill_processes.bat

# Relancer
run.bat
```

### Problème : "Je ne trouve pas cette information"

**Cause :** Documents pas correctement indexés ou question hors contexte

**Solution :**
```batch
# 1. Supprimer l'ancien index
rmdir /S /Q data\vectordb

# 2. Réindexer
python scripts/ingest_simple.py

# 3. Vérifier avec le test
python test_complet_integre.py
```

### Logs de debug

```batch
# Voir les logs FastAPI
type logs\fastapi.log

# Voir les logs Streamlit
type logs\streamlit.log
```

---

## 🧪 Tests

### Test complet du système

```batch
python test_complet_integre.py
```

**Vérifie :**
- ✅ Chargement documents
- ✅ Chunking
- ✅ Embeddings
- ✅ Index FAISS
- ✅ LLM Ollama
- ✅ Pipeline RAG
- ✅ Questions réelles

### Chat en ligne de commande

```batch
python scripts/chat.py
```

---

## 🔒 Sécurité et confidentialité

- ✅ **100% Local** : Aucune donnée envoyée vers des serveurs externes
- ✅ **Pas d'API externe** : Pas besoin de clés OpenAI, Anthropic, etc.
- ✅ **Données privées** : Vos documents restent sur votre machine
- ✅ **Open Source** : Code entièrement auditable

---

## 📈 Performances

### Benchmarks (machine standard)

| Opération | Temps moyen |
|-----------|-------------|
| Chargement 100 pages PDF | ~10s |
| Génération embeddings (100 chunks) | ~5s |
| Recherche FAISS | <100ms |
| Génération réponse LLM | ~3-5s |
| **Total query end-to-end** | **~5s** |

### Optimisations possibles

- 🚀 **GPU** : Utilisez CUDA pour les embeddings (10x plus rapide)
- 🚀 **FAISS GPU** : Recherche vectorielle accélérée
- 🚀 **Batch processing** : Indexation par lots
- 🚀 **Modèles quantifiés** : LLM plus légers (GGUF, GGML)

---

## 🤝 Contribution

Les contributions sont les bienvenues !

### Comment contribuer

1. **Fork** le projet
2. **Créer** une branche (`git checkout -b feature/amelioration`)
3. **Commit** vos changements (`git commit -m 'Ajout fonctionnalité'`)
4. **Push** vers la branche (`git push origin feature/amelioration`)
5. **Ouvrir** une Pull Request

### Guidelines

- Suivre le style de code existant
- Ajouter des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation
- Tester localement avant de soumettre

---

## 📚 Ressources

### Documentation officielle

- [LangChain](https://python.langchain.com/docs/get_started)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://docs.streamlit.io/)
- [Ollama](https://github.com/ollama/ollama)
- [FAISS](https://github.com/facebookresearch/faiss)

### Tutoriels et articles

- [Introduction au RAG](https://www.langchain.com/retrieval-augmented-generation)
- [Sentence Transformers](https://www.sbert.net/)
- [LLaMA](https://ai.meta.com/llama/)

---

## 🙏 Remerciements

- **LangChain** pour le framework RAG
- **Meta AI** pour LLaMA
- **Ollama** pour le runtime LLM local
- **Facebook Research** pour FAISS
- **HuggingFace** pour les modèles d'embeddings
- **FastAPI** et **Streamlit** pour les interfaces

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 📧 Contact

Pour toute question ou suggestion :

- 📧 Email : votre.email@example.com
- 🐙 GitHub : [@votre-username](https://github.com/ayoub-dev36)
- 💼 LinkedIn : [Votre Profil](https://www.linkedin.com/in/ayoub-bakkouri-196759250/)

---

<div align="center">

**Développé avec ❤️ pour la communauté Open Source**

⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile sur GitHub !

[⬆ Retour en haut](#-rag-local-chatbot)

</div>