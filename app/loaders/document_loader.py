"""
Module de chargement des documents
Supporte: PDF, DOCX, HTML, PPTX
"""
from pathlib import Path
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    BSHTMLLoader,
    UnstructuredPowerPointLoader
)
from langchain.schema import Document


class DocumentLoader:
    """Charge différents types de documents"""
    
    def __init__(self):
        self.loaders = {
            '.pdf': PyPDFLoader,
            '.docx': UnstructuredWordDocumentLoader,
            '.html': BSHTMLLoader,
            '.pptx': UnstructuredPowerPointLoader
        }
    
    def load_document(self, file_path: str) -> List[Document]:
        """
        Charge un document selon son extension
        
        Args:
            file_path: Chemin vers le fichier
            
        Returns:
            Liste de documents LangChain
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable: {file_path}")
        
        extension = path.suffix.lower()
        
        if extension not in self.loaders:
            raise ValueError(
                f"Extension non supportée: {extension}. "
                f"Extensions supportées: {list(self.loaders.keys())}"
            )
        
        loader_class = self.loaders[extension]
        loader = loader_class(str(path))
        
        try:
            documents = loader.load()
            print(f"✓ {len(documents)} page(s) chargée(s) depuis {path.name}")
            return documents
        except Exception as e:
            raise RuntimeError(f"Erreur lors du chargement de {path.name}: {str(e)}")
    
    def load_documents_from_directory(self, directory: str) -> List[Document]:
        """
        Charge tous les documents d'un répertoire
        
        Args:
            directory: Chemin vers le répertoire
            
        Returns:
            Liste de tous les documents chargés
        """
        dir_path = Path(directory)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Répertoire introuvable: {directory}")
        
        all_documents = []
        
        for file_path in dir_path.iterdir():
            if file_path.suffix.lower() in self.loaders:
                try:
                    docs = self.load_document(str(file_path))
                    all_documents.extend(docs)
                except Exception as e:
                    print(f"⚠ Erreur avec {file_path.name}: {str(e)}")
                    continue
        
        print(f"\n✓ Total: {len(all_documents)} page(s) chargée(s)")
        return all_documents


def load_documents(path: str) -> List[Document]:
    """
    Fonction utilitaire pour charger des documents
    
    Args:
        path: Chemin vers un fichier ou un répertoire
        
    Returns:
        Liste de documents
    """
    loader = DocumentLoader()
    path_obj = Path(path)
    
    if path_obj.is_file():
        return loader.load_document(path)
    elif path_obj.is_dir():
        return loader.load_documents_from_directory(path)
    else:
        raise ValueError(f"Chemin invalide: {path}")