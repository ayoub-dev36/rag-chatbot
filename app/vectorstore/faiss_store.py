"""
Module de gestion de la base vectorielle FAISS
"""
from typing import List, Optional
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import FAISS_INDEX_PATH


class FAISSVectorStore:
    """Gestionnaire de la base vectorielle FAISS"""
    
    def __init__(self, index_path: str = str(FAISS_INDEX_PATH)):
        """
        Initialise le gestionnaire FAISS
        
        Args:
            index_path: Chemin de sauvegarde de l'index
        """
        self.index_path = Path(index_path)
        self.vectorstore = None
    
    def create_index(
        self,
        chunks: List[Document],
        embeddings: HuggingFaceEmbeddings
    ) -> FAISS:
        """
        Crée un nouvel index FAISS
        
        Args:
            chunks: Liste de chunks à indexer
            embeddings: Modèle d'embeddings
            
        Returns:
            Instance FAISS
        """
        if not chunks:
            raise ValueError("Aucun chunk à indexer")
        
        print(f"🔨 Création de l'index FAISS avec {len(chunks)} chunks...")
        
        try:
            # Créer l'index FAISS
            self.vectorstore = FAISS.from_documents(
                documents=chunks,
                embedding=embeddings
            )
            
            print(f"✓ Index FAISS créé avec succès")
            return self.vectorstore
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la création de l'index: {str(e)}")
    
    def save_index(self) -> None:
        """Sauvegarde l'index FAISS sur le disque"""
        if self.vectorstore is None:
            raise ValueError("Aucun index à sauvegarder")
        
        try:
            # Créer le dossier parent si nécessaire
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Sauvegarder l'index
            self.vectorstore.save_local(str(self.index_path))
            
            print(f"✓ Index sauvegardé: {self.index_path}")
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la sauvegarde: {str(e)}")
    
    def load_index(self, embeddings: HuggingFaceEmbeddings) -> FAISS:
        """
        Charge un index FAISS existant
        
        Args:
            embeddings: Modèle d'embeddings
            
        Returns:
            Instance FAISS
        """
        if not self.index_path.exists():
            raise FileNotFoundError(f"Index introuvable: {self.index_path}")
        
        print(f"📂 Chargement de l'index FAISS...")
        
        try:
            self.vectorstore = FAISS.load_local(
                str(self.index_path),
                embeddings,
                allow_dangerous_deserialization=True  # Nécessaire pour charger l'index
            )
            
            print(f"✓ Index chargé avec succès")
            return self.vectorstore
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement: {str(e)}")
    
    def index_exists(self) -> bool:
        """
        Vérifie si un index existe déjà
        
        Returns:
            True si l'index existe
        """
        return self.index_path.exists() and (self.index_path / "index.faiss").exists()
    
    def add_documents(
        self,
        chunks: List[Document],
        embeddings: HuggingFaceEmbeddings
    ) -> None:
        """
        Ajoute des documents à un index existant
        
        Args:
            chunks: Nouveaux chunks à ajouter
            embeddings: Modèle d'embeddings
        """
        if self.vectorstore is None:
            raise ValueError("Aucun index chargé. Utilisez load_index() d'abord")
        
        print(f"➕ Ajout de {len(chunks)} nouveaux chunks...")
        
        try:
            self.vectorstore.add_documents(chunks)
            print(f"✓ Chunks ajoutés avec succès")
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors de l'ajout: {str(e)}")
    
    def get_vectorstore(self) -> Optional[FAISS]:
        """
        Récupère l'instance FAISS
        
        Returns:
            Instance FAISS ou None
        """
        return self.vectorstore


def create_or_load_faiss(
    chunks: List[Document],
    embeddings: HuggingFaceEmbeddings,
    index_path: str = str(FAISS_INDEX_PATH),
    force_recreate: bool = False
) -> FAISS:
    """
    Fonction utilitaire pour créer ou charger un index FAISS
    
    Args:
        chunks: Chunks à indexer
        embeddings: Modèle d'embeddings
        index_path: Chemin de l'index
        force_recreate: Forcer la recréation
        
    Returns:
        Instance FAISS
    """
    store = FAISSVectorStore(index_path=index_path)
    
    # Si l'index existe et qu'on ne force pas la recréation
    if store.index_exists() and not force_recreate:
        print("ℹ Index existant détecté")
        vectorstore = store.load_index(embeddings)
    else:
        # Créer un nouvel index
        vectorstore = store.create_index(chunks, embeddings)
        store.save_index()
    
    return vectorstore