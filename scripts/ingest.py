"""
Script d'ingestion et d'indexation des documents

Usage:
    python scripts/ingest.py
"""
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from app.loaders.document_loader import load_documents
from app.preprocess.text_cleaner import clean_documents
from app.chunking.text_splitter import split_documents
from app.embeddings.embedding_model import load_embedding_model
from app.vectorstore.faiss_store import create_or_load_faiss
from config.settings import RAW_DIR


def ingest_documents(source_path: str = None, force_recreate: bool = False):
    """
    Pipeline complet d'ingestion des documents
    
    Args:
        source_path: Chemin vers les fichiers (défaut: data/raw/)
        force_recreate: Forcer la recréation de l'index
    """
    print("\n" + "="*70)
    print("🚀 DÉMARRAGE DU PIPELINE D'INGESTION")
    print("="*70 + "\n")
    
    # Étape 1: Chargement des documents
    print("📂 ÉTAPE 1/5 : Chargement des documents")
    print("-"*70)
    
    if source_path is None:
        source_path = str(RAW_DIR)
    
    try:
        documents = load_documents(source_path)
        
        if not documents:
            print("❌ Aucun document trouvé. Vérifiez le dossier data/raw/")
            return
        
        print(f"✓ {len(documents)} document(s) chargé(s)\n")
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement: {str(e)}")
        return
    
    # Étape 2: Nettoyage et normalisation
    print("🧹 ÉTAPE 2/5 : Nettoyage et normalisation")
    print("-"*70)
    
    try:
        cleaned_documents = clean_documents(documents)
        print()
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {str(e)}")
        return
    
    # Étape 3: Découpage en chunks
    print("✂️  ÉTAPE 3/5 : Découpage en chunks")
    print("-"*70)
    
    try:
        chunks = split_documents(cleaned_documents)
        print()
        
    except Exception as e:
        print(f"❌ Erreur lors du découpage: {str(e)}")
        return
    
    # Étape 4: Chargement du modèle d'embeddings
    print("🧠 ÉTAPE 4/5 : Chargement du modèle d'embeddings")
    print("-"*70)
    
    try:
        embeddings = load_embedding_model()
        print()
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle: {str(e)}")
        return
    
    # Étape 5: Création de l'index FAISS
    print("💾 ÉTAPE 5/5 : Création de l'index FAISS")
    print("-"*70)
    
    try:
        vectorstore = create_or_load_faiss(
            chunks=chunks,
            embeddings=embeddings,
            force_recreate=force_recreate
        )
        print()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'indexation: {str(e)}")
        return
    
    # Résumé final
    print("="*70)
    print("✅ INGESTION TERMINÉE AVEC SUCCÈS")
    print("="*70)
    print(f"📊 Résumé :")
    print(f"   • Documents chargés : {len(documents)}")
    print(f"   • Documents nettoyés : {len(cleaned_documents)}")
    print(f"   • Chunks créés : {len(chunks)}")
    print(f"   • Index FAISS : Prêt")
    print("\n💡 Vous pouvez maintenant lancer le chat : python scripts/chat.py")
    print("="*70 + "\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingestion et indexation des documents")
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Chemin vers les documents (défaut: data/raw/)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Forcer la recréation de l'index"
    )
    
    args = parser.parse_args()
    
    ingest_documents(source_path=args.path, force_recreate=args.force)