"""
Module de génération des embeddings (local)
Version compatible avec sentence-transformers>=2.6.0
"""
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL_NAME, EMBEDDING_DEVICE


class EmbeddingModel:
    """Gestionnaire du modèle d'embeddings local"""
    
    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL_NAME,
        device: str = EMBEDDING_DEVICE
    ):
        """
        Initialise le modèle d'embeddings
        
        Args:
            model_name: Nom du modèle HuggingFace
            device: Device (cpu/cuda)
        """
        self.model_name = model_name
        self.device = device
        self.embeddings = None
    
    def load_model(self) -> HuggingFaceEmbeddings:
        """
        Charge le modèle d'embeddings
        
        Returns:
            Instance HuggingFaceEmbeddings
        """
        if self.embeddings is None:
            print(f"📥 Chargement du modèle d'embeddings: {self.model_name}")
            
            try:
                # Version corrigée pour langchain-huggingface 0.0.1
                self.embeddings = HuggingFaceEmbeddings(
                    model_name=self.model_name,
                    model_kwargs={'device': self.device},
                    encode_kwargs={
                        'normalize_embeddings': True,
                        'batch_size': 32
                    }
                )
                
                print(f"✓ Modèle d'embeddings chargé avec succès")
                
                # Test pour vérifier la dimension
                test_embed = self.embeddings.embed_query("test")
                print(f"  - Device: {self.device}")
                print(f"  - Dimension: {len(test_embed)}")
                
            except Exception as e:
                raise RuntimeError(f"Erreur lors du chargement du modèle: {str(e)}")
        
        return self.embeddings
    
    def get_embeddings(self) -> HuggingFaceEmbeddings:
        """
        Récupère l'instance d'embeddings (charge si nécessaire)
        
        Returns:
            Instance HuggingFaceEmbeddings
        """
        if self.embeddings is None:
            return self.load_model()
        return self.embeddings
    
    def embed_text(self, text: str) -> list:
        """
        Génère l'embedding d'un texte
        
        Args:
            text: Texte à encoder
            
        Returns:
            Vecteur d'embedding
        """
        embeddings = self.get_embeddings()
        return embeddings.embed_query(text)
    
    def embed_texts(self, texts: list) -> list:
        """
        Génère les embeddings de plusieurs textes
        
        Args:
            texts: Liste de textes
            
        Returns:
            Liste de vecteurs d'embeddings
        """
        embeddings = self.get_embeddings()
        return embeddings.embed_documents(texts)


def load_embedding_model(
    model_name: str = EMBEDDING_MODEL_NAME,
    device: str = EMBEDDING_DEVICE
) -> HuggingFaceEmbeddings:
    """
    Fonction utilitaire pour charger le modèle d'embeddings
    
    Args:
        model_name: Nom du modèle
        device: Device
        
    Returns:
        Instance HuggingFaceEmbeddings
    """
    model = EmbeddingModel(model_name=model_name, device=device)
    return model.load_model()