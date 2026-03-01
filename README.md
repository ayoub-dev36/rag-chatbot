<div align="center">

# RAG Local Chatbot

**Système de Question-Réponse Intelligent basé sur vos Documents**

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.16-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://python.langchain.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/Ollama-LLaMA_3-black?style=for-the-badge)](https://ollama.ai/)
[![FAISS](https://img.shields.io/badge/FAISS-1.7.4-0467DF?style=for-the-badge&logo=meta&logoColor=white)](https://github.com/facebookresearch/faiss)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

*Chatbot RAG 100% local — aucune donnée envoyée dans le cloud*

[Architecture](#-architecture) • [Installation](#-installation) • [Utilisation](#-utilisation) • [API](#-api-endpoints) • [Pipeline](#-pipeline-rag)

</div>

---

## Table des matières

- [À propos](#-à-propos)
- [Architecture](#-architecture)
- [Stack technique](#-stack-technique)
- [Pipeline RAG](#-pipeline-rag)
- [Structure du projet](#-structure-du-projet)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [API Endpoints](#-api-endpoints)
- [Dépannage](#-dépannage)
- [Licence](#-licence)

---

## À propos

**RAG Local Chatbot** est un système de Question-Réponse (QA) basé sur l'architecture **Retrieval-Augmented Generation**. Il permet d'interroger vos propres documents en langage naturel, avec des réponses précises et sourcées, sans jamais envoyer vos données vers un serveur externe.

**Formats supportés :** PDF · DOCX · HTML · PPTX · TXT

**Points forts :**
- 100% local — LLM, embeddings et index vectoriel tournent sur votre machine
- Anti-hallucination — le modèle répond uniquement à partir du contenu de vos documents
- Sources citées — chaque réponse indique le document et la page d'origine
- Interface double — UI Streamlit pour les utilisateurs, REST API pour les intégrations

---

## Architecture

### Vue d'ensemble du système

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          COUCHE PRÉSENTATION                            │
│                                                                         │
│   ┌──────────────────────────┐        ┌──────────────────────────┐     │
│   │     Streamlit UI         │        │      FastAPI REST         │     │
│   │     Port 8501            │◄──────►│      Port 8000            │     │
│   │  (Interface utilisateur) │  HTTP  │  (Backend / API)          │     │
│   └──────────────────────────┘        └────────────┬─────────────┘     │
└────────────────────────────────────────────────────│────────────────────┘
                                                     │
┌────────────────────────────────────────────────────▼────────────────────┐
│                           COUCHE RAG                                    │
│                                                                         │
│   ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌───────────┐  │
│   │  Document  │───►│   Text     │───►│   Text     │───►│ Embedding │  │
│   │  Loader    │    │  Cleaner   │    │  Splitter  │    │  Model    │  │
│   │            │    │            │    │ chunk=300  │    │ MiniLM-L6 │  │
│   └────────────┘    └────────────┘    └────────────┘    └─────┬─────┘  │
│                                                               │         │
│   ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌─────▼─────┐  │
│   │  Response  │◄───│  LLaMA 3   │◄───│  Prompt    │◄───│   FAISS   │  │
│   │ + Sources  │    │  (Ollama)  │    │  Template  │    │  Search   │  │
│   └────────────┘    └────────────┘    └────────────┘    └───────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                                     │
┌────────────────────────────────────────────────────▼────────────────────┐
│                         COUCHE STOCKAGE                                 │
│                                                                         │
│   ┌──────────────────┐    ┌──────────────────┐    ┌────────────────┐   │
│   │   data/raw/      │    │  FAISS Index     │    │  Ollama Model  │   │
│   │   (documents     │    │  data/vectordb/  │    │  llama3 (4GB)  │   │
│   │    originaux)    │    │  (vecteurs 384d) │    │                │   │
│   └──────────────────┘    └──────────────────┘    └────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### Flux de données détaillé

```
╔══════════════════════════════════════════════════════════════════════════╗
║                     PHASE 1 — INDEXATION DES DOCUMENTS                  ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   Documents (PDF/DOCX/HTML/PPTX/TXT)                                    ║
║        │                                                                 ║
║        ▼                                                                 ║
║   [Document Loader]  ──  PyPDF · python-docx · BeautifulSoup · pptx    ║
║        │                                                                 ║
║        ▼                                                                 ║
║   [Text Cleaner]     ──  Normalisation Unicode, suppression bruit       ║
║        │                                                                 ║
║        ▼                                                                 ║
║   [Text Splitter]    ──  RecursiveCharacterTextSplitter                 ║
║        │                   chunk_size=300 / overlap=50                   ║
║        ▼                                                                 ║
║   [Embedding Model]  ──  sentence-transformers/all-MiniLM-L6-v2        ║
║        │                   Vecteurs 384 dimensions (CPU/GPU)             ║
║        ▼                                                                 ║
║   [FAISS Index]      ──  Stockage local  →  data/vectordb/              ║
║                                                                          ║
╠══════════════════════════════════════════════════════════════════════════╣
║                     PHASE 2 — GÉNÉRATION DE RÉPONSE                     ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   Question utilisateur                                                   ║
║        │                                                                 ║
║        ▼                                                                 ║
║   [Embedding Model]  ──  Vectorisation de la question                   ║
║        │                                                                 ║
║        ▼                                                                 ║
║   [FAISS Search]     ──  Recherche par similarité cosinus               ║
║        │                   top_k=3 chunks les plus pertinents            ║
║        ▼                                                                 ║
║   [Prompt Template]  ──  Construction : Context + Question              ║
║        │                   Anti-hallucination par design                 ║
║        ▼                                                                 ║
║   [LLaMA 3 / Ollama] ──  Inférence locale  temperature=0.0             ║
║        │                   max_tokens=2000                               ║
║        ▼                                                                 ║
║   Réponse + Sources citées                                               ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## Stack technique

### Couche IA & Machine Learning

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **LLM** | LLaMA 3 via Ollama | — | Génération de réponses en local |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` | ≥ 2.6.0 | Vectorisation texte (384 dim) |
| **Vector Store** | FAISS (Facebook AI Similarity Search) | 1.7.4 | Index vectoriel haute performance |
| **RAG Framework** | LangChain (`RetrievalQA`) | 0.1.16 | Orchestration de la chaîne RAG |
| **HuggingFace** | `langchain-huggingface` | 0.0.1 | Interface modèles embeddings |

### Couche Backend & API

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **API REST** | FastAPI | 0.109.0 | Backend HTTP — endpoints CRUD |
| **Serveur ASGI** | Uvicorn | 0.27.0 | Serveur async hautes performances |
| **Validation** | Pydantic | 2.5.3 | Schémas de données & validation |
| **CORS** | FastAPI Middleware | — | Sécurisation des origines |

### Couche Frontend

| Composant | Technologie | Version | Rôle |
|-----------|-------------|---------|------|
| **Interface Web** | Streamlit | 1.29.0 | UI interactive (chat, upload, dashboard) |
| **HTTP Client** | Requests | 2.31.0 | Communication Streamlit → FastAPI |

### Couche Document Processing

| Composant | Technologie | Version | Format supporté |
|-----------|-------------|---------|-----------------|
| **PDF** | PyPDF | 3.17.4 | `.pdf` |
| **Word** | python-docx | 1.1.0 | `.docx` |
| **Web** | BeautifulSoup4 + lxml | 4.12.2 | `.html` |
| **PowerPoint** | python-pptx | 0.6.23 | `.pptx` |
| **Texte** | Built-in / unstructured | 0.11.8 | `.txt` |

### Environnement & Infrastructure

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| **Runtime** | Python 3.10 | Langage principal |
| **Env. manager** | Conda / Miniconda | Isolation des dépendances |
| **LLM Runtime** | Ollama | Exécution locale de LLaMA 3 |
| **OS** | Windows / Linux / macOS | Multi-plateforme |

---

## Pipeline RAG

### Paramètres du pipeline

| Paramètre | Valeur | Justification |
|-----------|--------|---------------|
| `CHUNK_SIZE` | `300` | Chunks focalisés, précision accrue |
| `CHUNK_OVERLAP` | `50` | Continuité sémantique entre chunks |
| `SEARCH_TOP_K` | `3` | Équilibre pertinence / bruit |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Léger, rapide, 384 dimensions |
| `LLM_TEMPERATURE` | `0.0` | Réponses déterministes, fiables |
| `LLM_MAX_TOKENS` | `2000` | Réponses complètes autorisées |
| `EMBEDDING_DEVICE` | `cpu` | Compatible sans GPU (CUDA optionnel) |
| `RAG_CHAIN_TYPE` | `stuff` | Contexte injecté en une seule fois |

### Prompt anti-hallucination

Le système utilise un prompt strict qui contraint le modèle à ne répondre qu'à partir du contexte fourni :

```
Réponds à la question en utilisant UNIQUEMENT le contexte fourni.

CONTEXTE: {context}
QUESTION: {question}

Si la réponse est dans le contexte, réponds clairement.
Si la réponse n'est PAS dans le contexte, dis: "Information non trouvée."

RÉPONSE:
```

---

## Structure du projet

```
rag-chatbot/
│
├── app/                          # Code source principal
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py               # FastAPI — endpoints REST (upload, ingest, query, reset)
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   └── streamlit_app.py      # Interface Streamlit — chat + dashboard
│   │
│   ├── loaders/
│   │   └── document_loader.py    # Chargement multi-format (PDF, DOCX, HTML, PPTX, TXT)
│   │
│   ├── preprocess/
│   │   └── text_cleaner.py       # Nettoyage et normalisation Unicode
│   │
│   ├── chunking/
│   │   └── text_splitter.py      # RecursiveCharacterTextSplitter (chunk=300, overlap=50)
│   │
│   ├── embeddings/
│   │   └── embedding_model.py    # HuggingFace Embeddings — all-MiniLM-L6-v2
│   │
│   ├── vectorstore/
│   │   └── faiss_store.py        # Création, sauvegarde et chargement de l'index FAISS
│   │
│   ├── retriever/
│   │   └── similarity_search.py  # Recherche par similarité cosinus (top_k=3)
│   │
│   ├── llm/
│   │   └── llama_model.py        # Connexion Ollama — LLaMA 3
│   │
│   ├── rag/
│   │   └── rag_pipeline.py       # RetrievalQA chain — orchestration complète
│   │
│   └── prompts/
│       └── rag_prompt.txt        # Template de prompt optimisé
│
├── config/
│   └── settings.py               # Paramètres globaux (chemins, hyperparamètres)
│
├── data/
│   ├── raw/                      # Documents originaux à indexer
│   ├── processed/                # Documents pré-traités
│   └── vectordb/                 # Index FAISS persisté
│
├── scripts/
│   └── ingest.py                 # Script d'indexation en ligne de commande
│
├── run.bat                       # Lancement rapide (Windows)
├── fix_env_final.bat             # Résolution de problèmes d'environnement
├── kill_processes.bat            # Arrêt propre des services
├── requirements.txt              # Dépendances Python (versions compatibles testées)
├── environment.yml               # Configuration environnement Conda
├── .gitignore
└── LICENSE
```

---

## Prérequis

### Matériel recommandé

| Ressource | Minimum | Recommandé |
|-----------|---------|------------|
| **RAM** | 8 GB | 16 GB |
| **Stockage** | 10 GB libres | 20 GB |
| **CPU** | 4 cœurs | 8 cœurs+ |
| **GPU** | — (optionnel) | NVIDIA CUDA (embeddings 10x plus rapide) |

### Logiciels requis

1. **Anaconda ou Miniconda** — [télécharger ici](https://www.anaconda.com/download)
2. **Ollama** — [télécharger ici](https://ollama.ai)
3. **Git** — pour cloner le dépôt

---

## Installation

### Étape 1 — Cloner le projet

```bash
git clone https://github.com/ayoub-dev36/rag-chatbot.git
cd rag-chatbot
```

### Étape 2 — Créer l'environnement Conda

```bash
# Depuis le fichier environment.yml (recommandé)
conda env create -f environment.yml
conda activate rag-chatbot-env
```

Ou manuellement :

```bash
conda create -n rag-chatbot-env python=3.10 -y
conda activate rag-chatbot-env
pip install -r requirements.txt
```

### Étape 3 — Télécharger le modèle LLM

```bash
# Lancer Ollama
ollama serve

# Dans un autre terminal, télécharger LLaMA 3
ollama pull llama3
```

### Étape 4 — Vérifier l'installation

```bash
python -c "import langchain, streamlit, fastapi, faiss; print('Installation OK')"
ollama list
```

---

## Configuration

Tous les paramètres sont centralisés dans [config/settings.py](config/settings.py) :

```python
# Chunking
CHUNK_SIZE = 300           # Taille des chunks en caractères
CHUNK_OVERLAP = 50         # Chevauchement entre chunks

# Embeddings
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DEVICE = "cpu"   # "cuda" si GPU disponible

# FAISS
SEARCH_TOP_K = 3           # Nombre de chunks récupérés par requête

# LLM
LLM_MODEL = "llama3"
LLM_TEMPERATURE = 0.0      # 0.0 = déterministe
LLM_MAX_TOKENS = 2000

# Formats supportés
SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".html", ".pptx", ".txt"]
```

---

## Utilisation

### Démarrage complet

**Terminal 1 — Ollama :**
```bash
ollama serve
```

**Terminal 2 — Lancement des services (Windows) :**
```bash
run.bat
```

Ou manuellement :

```bash
# Terminal 2 — FastAPI
conda activate rag-chatbot-env
uvicorn app.api.main:app --host 0.0.0.0 --port 8000

# Terminal 3 — Streamlit
conda activate rag-chatbot-env
streamlit run app/ui/streamlit_app.py --server.port 8501
```

**Accès :**
- Interface utilisateur : http://localhost:8501
- API REST + documentation : http://localhost:8000/docs

### Workflow standard

1. **Ouvrir** l'interface sur http://localhost:8501
2. **Uploader** vos documents (glisser-déposer)
3. **Indexer** en cliquant sur "Indexer les documents"
4. **Interroger** vos documents en langage naturel

### Indexation en ligne de commande

```bash
# Placer les documents dans data/raw/
python scripts/ingest.py
```

---

## API Endpoints

**Base URL :** `http://localhost:8000`
**Documentation interactive :** http://localhost:8000/docs

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/` | Statut de l'API |
| `GET` | `/status` | État du système RAG |
| `POST` | `/upload` | Upload de documents |
| `POST` | `/ingest` | Indexation des documents |
| `POST` | `/query` | Question aux documents |
| `DELETE` | `/reset` | Réinitialisation complète |

### Exemple — Requête `POST /query`

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "Qu'\''est-ce que Python ?", "top_k": 3}'
```

**Réponse :**
```json
{
  "answer": "Python est un langage de programmation...",
  "sources": [
    {
      "source": "cours_python.pdf",
      "page": "2",
      "content": "Python est un langage interprété..."
    }
  ],
  "success": true
}
```

---

## Dépannage

### "API non accessible"

```bash
# Vérifier que FastAPI tourne
curl http://localhost:8000/status

# Relancer manuellement
uvicorn app.api.main:app --host 0.0.0.0 --port 8000
```

### "Ollama non trouvé"

```bash
ollama list          # Vérifier les modèles disponibles
ollama serve         # Démarrer le service
ollama pull llama3   # Télécharger le modèle si absent
```

### "Index FAISS introuvable"

```bash
# Indexer les documents
python scripts/ingest.py
```

### "Port déjà utilisé"

```bash
# Windows — arrêt propre des processus
kill_processes.bat
```

### "Problème d'environnement Conda"

```bash
# Windows — script de correction automatique
fix_env_final.bat
```

---

## Performances

| Opération | Temps indicatif |
|-----------|----------------|
| Chargement de 100 pages PDF | ~10 s |
| Génération embeddings (100 chunks) | ~5 s (CPU) |
| Recherche FAISS | < 100 ms |
| Génération réponse (LLaMA 3) | ~3–5 s |
| **Query end-to-end** | **~5 s** |

> Avec GPU CUDA : les embeddings sont ~10x plus rapides. Modifier `EMBEDDING_DEVICE = "cuda"` dans `config/settings.py`.

---

## Contribution

1. Forker le projet
2. Créer une branche : `git checkout -b feature/ma-fonctionnalite`
3. Commiter : `git commit -m "feat: description"`
4. Pousser : `git push origin feature/ma-fonctionnalite`
5. Ouvrir une Pull Request

---

## Licence

Ce projet est distribué sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour les détails.

---

<div align="center">

Développé par **[Ayoub Bakkouri](https://github.com/ayoub-dev36)**

[![GitHub](https://img.shields.io/badge/GitHub-ayoub--dev36-181717?style=flat-square&logo=github)](https://github.com/ayoub-dev36)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ayoub_Bakkouri-0077B5?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/ayoub-bakkouri-196759250/)

*Si ce projet vous est utile, n'hésitez pas à lui laisser une étoile.*

</div>
