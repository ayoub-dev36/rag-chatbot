"""
Module de découpage du texte en chunks
"""
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


class DocumentSplitter:
    """Découpe les documents en chunks optimaux"""
    
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        """
        Initialise le splitter
        
        Args:
            chunk_size: Taille maximale d'un chunk
            chunk_overlap: Chevauchement entre chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Séparateurs hiérarchiques pour un meilleur découpage
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=[
                "\n\n\n",  # Triple saut de ligne (séparation forte)
                "\n\n",    # Double saut de ligne (paragraphes)
                "\n",      # Saut de ligne simple
                ". ",      # Fin de phrase
                "! ",      # Point d'exclamation
                "? ",      # Point d'interrogation
                "; ",      # Point-virgule
                ", ",      # Virgule
                " ",       # Espace
                ""         # Caractère par caractère (dernier recours)
            ],
            add_start_index=True  # Ajoute l'index de début dans les métadonnées
        )
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Découpe les documents en chunks
        
        Args:
            documents: Liste de documents à découper
            
        Returns:
            Liste de documents découpés (chunks)
        """
        if not documents:
            print("⚠ Aucun document à découper")
            return []
        
        try:
            chunks = self.splitter.split_documents(documents)
            
            # Enrichir les métadonnées
            for i, chunk in enumerate(chunks):
                chunk.metadata['chunk_id'] = i
                chunk.metadata['chunk_size'] = len(chunk.page_content)
            
            print(f"✓ {len(chunks)} chunk(s) créé(s) à partir de {len(documents)} document(s)")
            print(f"  - Taille moyenne: {sum(len(c.page_content) for c in chunks) // len(chunks)} caractères")
            
            return chunks
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors du découpage: {str(e)}")
    
    def get_chunk_statistics(self, chunks: List[Document]) -> dict:
        """
        Calcule des statistiques sur les chunks
        
        Args:
            chunks: Liste de chunks
            
        Returns:
            Dictionnaire de statistiques
        """
        if not chunks:
            return {}
        
        sizes = [len(chunk.page_content) for chunk in chunks]
        
        return {
            'total_chunks': len(chunks),
            'avg_size': sum(sizes) / len(sizes),
            'min_size': min(sizes),
            'max_size': max(sizes),
            'total_characters': sum(sizes)
        }


def split_documents(
    documents: List[Document],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> List[Document]:
    """
    Fonction utilitaire pour découper des documents
    
    Args:
        documents: Liste de documents
        chunk_size: Taille des chunks
        chunk_overlap: Chevauchement
        
    Returns:
        Liste de chunks
    """
    splitter = DocumentSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)