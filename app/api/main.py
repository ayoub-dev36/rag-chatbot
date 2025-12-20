"""
API FastAPI pour le système RAG
VERSION AVEC LOGS DE DEBUG
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import shutil
from pathlib import Path
import sys

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.loaders.document_loader import load_documents
from app.preprocess.text_cleaner import clean_documents
from app.chunking.text_splitter import split_documents
from app.embeddings.embedding_model import load_embedding_model
from app.vectorstore.faiss_store import FAISSVectorStore, create_or_load_faiss
from app.retriever.similarity_search import get_retriever
from app.llm.llama_model import load_llm
from app.rag.rag_pipeline import RAGPipeline
from config.settings import RAW_DIR, FAISS_INDEX_PATH, SUPPORTED_EXTENSIONS, SEARCH_TOP_K

# Initialisation de l'app FastAPI
app = FastAPI(
    title="RAG Local Chatbot API",
    description="API pour le système de Question-Réponse basé sur documents",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODÈLES PYDANTIC ====================

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = SEARCH_TOP_K

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    success: bool

class StatusResponse(BaseModel):
    status: str
    message: str
    details: Optional[dict] = None

# ==================== VARIABLES GLOBALES ====================

rag_pipeline: Optional[RAGPipeline] = None
embeddings_model = None
vectorstore = None

# ==================== INITIALISATION ====================

@app.on_event("startup")
async def startup_event():
    """Initialisation au démarrage"""
    global embeddings_model
    
    print("="*70)
    print("🚀 DÉMARRAGE DE L'API RAG")
    print("="*70)
    
    try:
        # Charger le modèle d'embeddings
        print("\n📥 Chargement du modèle d'embeddings...")
        embeddings_model = load_embedding_model()
        print("✓ Modèle d'embeddings chargé\n")
        
        # Vérifier si un index existe
        store = FAISSVectorStore(index_path=str(FAISS_INDEX_PATH))
        if store.index_exists():
            print("📂 Index FAISS existant détecté")
            await load_rag_system()
        else:
            print("⚠️  Aucun index FAISS trouvé")
            print("💡 Uploadez des documents et lancez /ingest\n")
    
    except Exception as e:
        print(f"❌ Erreur au démarrage: {str(e)}\n")

async def load_rag_system():
    """Charge le système RAG complet"""
    global rag_pipeline, vectorstore, embeddings_model
    
    print("\n🔗 Chargement du système RAG...")
    
    try:
        # Charger l'index FAISS
        store = FAISSVectorStore(index_path=str(FAISS_INDEX_PATH))
        vectorstore = store.load_index(embeddings_model)
        print("✓ Index FAISS chargé")
        
        # Créer le retriever
        retriever = get_retriever(vectorstore, top_k=SEARCH_TOP_K)
        print(f"✓ Retriever créé (top_k={SEARCH_TOP_K})")
        
        # Charger le LLM
        llm = load_llm()
        print("✓ LLM chargé")
        
        # Créer le pipeline RAG
        rag_pipeline = RAGPipeline(llm, retriever)
        rag_pipeline.build_chain()
        print("✓ Pipeline RAG prêt\n")
        
    except Exception as e:
        print(f"❌ Erreur chargement RAG: {str(e)}\n")
        raise

# ==================== ENDPOINTS ====================

@app.get("/", response_model=StatusResponse)
async def root():
    """Page d'accueil de l'API"""
    return StatusResponse(
        status="online",
        message="API RAG Local Chatbot opérationnelle",
        details={
            "version": "1.0.0",
            "endpoints": ["/upload", "/ingest", "/query", "/status"]
        }
    )

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Vérifie le statut du système"""
    
    # Vérifier l'index FAISS
    store = FAISSVectorStore(index_path=str(FAISS_INDEX_PATH))
    index_exists = store.index_exists()
    
    # Vérifier le RAG
    rag_ready = rag_pipeline is not None
    
    # Compter les fichiers
    raw_files = list(RAW_DIR.glob("*"))
    supported_files = [f for f in raw_files if f.suffix in SUPPORTED_EXTENSIONS]
    
    status = "ready" if (index_exists and rag_ready) else "not_ready"
    
    return StatusResponse(
        status=status,
        message="Système prêt" if status == "ready" else "Système non initialisé",
        details={
            "index_exists": index_exists,
            "rag_initialized": rag_ready,
            "files_uploaded": len(supported_files),
            "supported_extensions": SUPPORTED_EXTENSIONS,
            "search_top_k": SEARCH_TOP_K
        }
    )

@app.post("/upload", response_model=StatusResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload de fichiers"""
    if not files:
        raise HTTPException(status_code=400, detail="Aucun fichier fourni")
    
    uploaded = []
    errors = []
    
    for file in files:
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in SUPPORTED_EXTENSIONS:
            errors.append({
                "file": file.filename,
                "error": f"Extension non supportée: {file_ext}"
            })
            continue
        
        try:
            file_path = RAW_DIR / file.filename
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded.append(file.filename)
            print(f"✓ Fichier uploadé: {file.filename}")
            
        except Exception as e:
            errors.append({
                "file": file.filename,
                "error": str(e)
            })
    
    if not uploaded and errors:
        raise HTTPException(
            status_code=400,
            detail=f"Aucun fichier n'a pu être uploadé: {errors}"
        )
    
    return StatusResponse(
        status="success",
        message=f"{len(uploaded)} fichier(s) uploadé(s)",
        details={
            "uploaded": uploaded,
            "errors": errors if errors else None
        }
    )

@app.post("/ingest", response_model=StatusResponse)
async def ingest_documents(background_tasks: BackgroundTasks):
    """Lance l'ingestion des documents"""
    global embeddings_model, vectorstore, rag_pipeline
    
    # Vérifier s'il y a des fichiers
    raw_files = list(RAW_DIR.glob("*"))
    supported_files = [f for f in raw_files if f.suffix in SUPPORTED_EXTENSIONS]
    
    if not supported_files:
        raise HTTPException(
            status_code=400,
            detail="Aucun fichier à indexer. Uploadez d'abord des documents."
        )
    
    try:
        print("\n" + "="*70)
        print("🚀 DÉBUT DE L'INGESTION")
        print("="*70 + "\n")
        
        # 1. Charger les documents
        print("📂 Chargement des documents...")
        documents = load_documents(str(RAW_DIR))
        print(f"✓ {len(documents)} documents chargés\n")
        
        # 2. Nettoyer
        print("🧹 Nettoyage...")
        cleaned_documents = clean_documents(documents)
        print(f"✓ {len(cleaned_documents)} documents nettoyés\n")
        
        # 3. Découper
        print("✂️  Chunking...")
        chunks = split_documents(cleaned_documents)
        print(f"✓ {len(chunks)} chunks créés\n")
        
        # 4. Créer l'index FAISS
        print("💾 Création index FAISS...")
        vectorstore = create_or_load_faiss(
            chunks=chunks,
            embeddings=embeddings_model,
            force_recreate=True
        )
        print(f"✓ Index créé avec {len(chunks)} chunks\n")
        
        # 5. Charger le système RAG
        await load_rag_system()
        
        print("="*70)
        print("✅ INGESTION TERMINÉE")
        print("="*70 + "\n")
        
        return StatusResponse(
            status="success",
            message="Documents indexés avec succès",
            details={
                "documents_loaded": len(documents),
                "chunks_created": len(chunks),
                "files_processed": len(supported_files)
            }
        )
        
    except Exception as e:
        print(f"\n❌ ERREUR INGESTION: {str(e)}\n")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'ingestion: {str(e)}"
        )

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Pose une question aux documents"""
    global rag_pipeline
    
    if rag_pipeline is None:
        raise HTTPException(
            status_code=400,
            detail="Système RAG non initialisé. Lancez d'abord /ingest"
        )
    
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="La question ne peut pas être vide"
        )
    
    try:
        print("\n" + "-"*70)
        print(f"❓ Question reçue: {request.question}")
        print("-"*70)
        
        # Interroger le système RAG
        response = rag_pipeline.query(request.question)
        
        # Extraire la réponse et les sources
        answer = response.get('result', '')
        source_docs = response.get('source_documents', [])
        
        print(f"\n✅ Réponse: {answer[:100]}...")
        print(f"📚 Sources: {len(source_docs)} document(s)\n")
        
        # Formater les sources
        sources = []
        for doc in source_docs:
            sources.append({
                "source": doc.metadata.get('source', 'Inconnu'),
                "page": doc.metadata.get('page', 'N/A'),
                "content": doc.page_content[:200] + "..."
            })
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            success=True
        )
        
    except Exception as e:
        print(f"\n❌ ERREUR QUERY: {str(e)}\n")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la requête: {str(e)}"
        )

@app.delete("/reset", response_model=StatusResponse)
async def reset_system():
    """Réinitialise le système"""
    global rag_pipeline, vectorstore
    
    try:
        # Supprimer l'index FAISS
        if FAISS_INDEX_PATH.exists():
            shutil.rmtree(FAISS_INDEX_PATH)
        
        # Supprimer les fichiers raw
        for file in RAW_DIR.glob("*"):
            if file.is_file():
                file.unlink()
        
        # Réinitialiser les variables
        rag_pipeline = None
        vectorstore = None
        
        print("\n✓ Système réinitialisé\n")
        
        return StatusResponse(
            status="success",
            message="Système réinitialisé"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la réinitialisation: {str(e)}"
        )

# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )