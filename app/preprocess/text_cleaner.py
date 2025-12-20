"""
Module de nettoyage et normalisation du texte
"""
import re
import unicodedata
from typing import List
from langchain.schema import Document


class TextCleaner:
    """Nettoie et normalise le texte des documents"""
    
    def __init__(self):
        # Patterns à supprimer
        self.patterns_to_remove = [
            r'\n{3,}',  # Plusieurs sauts de ligne
            r'\s{3,}',  # Plusieurs espaces
            r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]',  # Caractères de contrôle
        ]
    
    def normalize_unicode(self, text: str) -> str:
        """
        Normalise les caractères Unicode
        
        Args:
            text: Texte à normaliser
            
        Returns:
            Texte normalisé
        """
        # Normalisation NFKD (décomposition de compatibilité)
        text = unicodedata.normalize('NFKD', text)
        # Encoder en ASCII, ignorer les erreurs, puis décoder
        text = text.encode('ascii', 'ignore').decode('ascii')
        return text
    
    def remove_special_characters(self, text: str) -> str:
        """
        Supprime les caractères spéciaux inutiles
        
        Args:
            text: Texte à nettoyer
            
        Returns:
            Texte nettoyé
        """
        for pattern in self.patterns_to_remove:
            text = re.sub(pattern, ' ', text)
        
        return text
    
    def remove_extra_whitespace(self, text: str) -> str:
        """
        Supprime les espaces multiples et normalise les espaces
        
        Args:
            text: Texte à nettoyer
            
        Returns:
            Texte nettoyé
        """
        # Remplacer plusieurs espaces par un seul
        text = re.sub(r'\s+', ' ', text)
        # Supprimer espaces en début/fin
        text = text.strip()
        return text
    
    def remove_headers_footers(self, text: str) -> str:
        """
        Supprime les headers/footers typiques
        (numéros de page, dates, etc.)
        
        Args:
            text: Texte à nettoyer
            
        Returns:
            Texte nettoyé
        """
        # Pattern pour numéros de page (ex: "Page 1", "1/10", etc.)
        text = re.sub(r'\bPage\s+\d+\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b\d+\s*/\s*\d+\b', '', text)
        
        # Pattern pour dates communes
        text = re.sub(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', '', text)
        
        return text
    
    def clean_text(self, text: str) -> str:
        """
        Pipeline complet de nettoyage
        
        Args:
            text: Texte à nettoyer
            
        Returns:
            Texte nettoyé
        """
        if not text:
            return ""
        
        # Étape 1: Normalisation Unicode
        text = self.normalize_unicode(text)
        
        # Étape 2: Suppression caractères spéciaux
        text = self.remove_special_characters(text)
        
        # Étape 3: Suppression headers/footers
        text = self.remove_headers_footers(text)
        
        # Étape 4: Normalisation des espaces
        text = self.remove_extra_whitespace(text)
        
        return text
    
    def clean_document(self, document: Document) -> Document:
        """
        Nettoie un document LangChain
        
        Args:
            document: Document à nettoyer
            
        Returns:
            Document nettoyé
        """
        cleaned_content = self.clean_text(document.page_content)
        
        return Document(
            page_content=cleaned_content,
            metadata=document.metadata
        )
    
    def clean_documents(self, documents: List[Document]) -> List[Document]:
        """
        Nettoie une liste de documents
        
        Args:
            documents: Liste de documents
            
        Returns:
            Liste de documents nettoyés
        """
        cleaned_docs = []
        
        for doc in documents:
            try:
                cleaned_doc = self.clean_document(doc)
                # Ne garder que les documents avec du contenu
                if cleaned_doc.page_content.strip():
                    cleaned_docs.append(cleaned_doc)
            except Exception as e:
                print(f"⚠ Erreur lors du nettoyage: {str(e)}")
                continue
        
        print(f"✓ {len(cleaned_docs)} document(s) nettoyé(s)")
        return cleaned_docs


def clean_documents(documents: List[Document]) -> List[Document]:
    """
    Fonction utilitaire pour nettoyer des documents
    
    Args:
        documents: Liste de documents
        
    Returns:
        Liste de documents nettoyés
    """
    cleaner = TextCleaner()
    return cleaner.clean_documents(documents)