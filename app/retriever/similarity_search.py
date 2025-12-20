"""
Module de recherche sémantique (retriever)
"""
from typing import List
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from config.settings import SEARCH_TOP_K


class SimilaritySearchRetriever:
    """Gestionnaire de recherche sémantique"""
    
    def __init__(self, vectorstore: FAISS, top_k: int = SEARCH_TOP_K):
        """
        Initialise le retriever
        
        Args:
            vectorstore: Instance FAISS
            top_k: Nombre de documents à récupérer
        """
        self.vectorstore = vectorstore
        self.top_k = top_k
        self.retriever = None
    
    def get_retriever(self):
        """
        Crée et retourne le retriever de base
        
        Returns:
            Retriever LangChain
        """
        if self.retriever is None:
            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": self.top_k,
                    "score_threshold": 0.5  # Seuil de similarité minimale
                }
            )
        
        return self.retriever
    
    def search(self, query: str) -> List[Document]:
        """
        Recherche les documents les plus similaires
        
        Args:
            query: Question de l'utilisateur
            
        Returns:
            Liste de documents pertinents
        """
        print(f"🔍 Recherche: '{query}'")
        
        try:
            retriever = self.get_retriever()
            documents = retriever.get_relevant_documents(query)
            
            print(f"✓ {len(documents)} document(s) trouvé(s)")
            
            return documents
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la recherche: {str(e)}")
    
    def search_with_scores(self, query: str) -> List[tuple]:
        """
        Recherche avec scores de similarité
        
        Args:
            query: Question de l'utilisateur
            
        Returns:
            Liste de tuples (Document, score)
        """
        try:
            results = self.vectorstore.similarity_search_with_score(
                query,
                k=self.top_k
            )
            
            print(f"✓ {len(results)} document(s) trouvé(s) avec scores")
            for i, (doc, score) in enumerate(results, 1):
                print(f"  {i}. Score: {score:.4f} | {doc.page_content[:100]}...")
            
            return results
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la recherche: {str(e)}")
    
    def mmr_search(self, query: str, fetch_k: int = 20, lambda_mult: float = 0.5) -> List[Document]:
        """
        Recherche MMR (Maximum Marginal Relevance) pour diversifier les résultats
        
        Args:
            query: Question de l'utilisateur
            fetch_k: Nombre de documents à récupérer initialement
            lambda_mult: Balance entre similarité (1.0) et diversité (0.0)
            
        Returns:
            Liste de documents diversifiés
        """
        try:
            documents = self.vectorstore.max_marginal_relevance_search(
                query,
                k=self.top_k,
                fetch_k=fetch_k,
                lambda_mult=lambda_mult
            )
            
            print(f"✓ {len(documents)} document(s) diversifié(s) trouvé(s)")
            
            return documents
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la recherche MMR: {str(e)}")


def get_retriever(
    vectorstore: FAISS,
    top_k: int = SEARCH_TOP_K,
    search_type: str = "similarity"
) -> any:
    """
    Fonction utilitaire pour créer un retriever
    
    Args:
        vectorstore: Instance FAISS
        top_k: Nombre de résultats
        search_type: Type de recherche ("similarity" ou "mmr")
        
    Returns:
        Retriever configuré
    """
    search_manager = SimilaritySearchRetriever(vectorstore, top_k)
    
    if search_type == "mmr":
        return lambda query: search_manager.mmr_search(query)
    else:
        return search_manager.get_retriever()