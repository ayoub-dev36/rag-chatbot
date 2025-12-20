"""
Module de gestion du LLM local (LLaMA via Ollama)
"""
from langchain_community.llms import Ollama
from config.settings import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS


class LlamaModel:
    """Gestionnaire du modèle LLaMA local"""
    
    def __init__(
        self,
        model: str = LLM_MODEL,
        temperature: float = LLM_TEMPERATURE,
        max_tokens: int = LLM_MAX_TOKENS
    ):
        """
        Initialise le modèle LLaMA
        
        Args:
            model: Nom du modèle Ollama
            temperature: Créativité (0.0 = déterministe, 1.0 = créatif)
            max_tokens: Longueur maximale de la réponse
        """
        self.model_name = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.llm = None
    
    def load_model(self) -> Ollama:
        """
        Charge le modèle LLaMA via Ollama
        
        Returns:
            Instance Ollama
        """
        if self.llm is None:
            print(f"🤖 Chargement du modèle LLM: {self.model_name}")
            
            try:
                self.llm = Ollama(
                    model=self.model_name,
                    temperature=self.temperature,
                    num_predict=self.max_tokens,
                    # Paramètres supplémentaires pour améliorer les réponses
                    top_k=40,
                    top_p=0.9,
                    repeat_penalty=1.1,
                )
                
                print(f"✓ Modèle LLM chargé avec succès")
                print(f"  - Modèle: {self.model_name}")
                print(f"  - Temperature: {self.temperature}")
                print(f"  - Max tokens: {self.max_tokens}")
                
            except Exception as e:
                raise RuntimeError(
                    f"Erreur lors du chargement du modèle: {str(e)}\n"
                    f"Assurez-vous qu'Ollama est installé et que le modèle '{self.model_name}' est disponible.\n"
                    f"Installation: ollama pull {self.model_name}"
                )
        
        return self.llm
    
    def get_llm(self) -> Ollama:
        """
        Récupère l'instance du LLM (charge si nécessaire)
        
        Returns:
            Instance Ollama
        """
        if self.llm is None:
            return self.load_model()
        return self.llm
    
    def generate(self, prompt: str) -> str:
        """
        Génère une réponse à partir d'un prompt
        
        Args:
            prompt: Prompt d'entrée
            
        Returns:
            Réponse générée
        """
        llm = self.get_llm()
        
        try:
            response = llm.invoke(prompt)
            return response
            
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la génération: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Teste la connexion au modèle
        
        Returns:
            True si le modèle répond
        """
        try:
            llm = self.get_llm()
            response = llm.invoke("Bonjour")
            return len(response) > 0
            
        except Exception as e:
            print(f"❌ Erreur de connexion: {str(e)}")
            return False


def load_llm(
    model: str = LLM_MODEL,
    temperature: float = LLM_TEMPERATURE,
    max_tokens: int = LLM_MAX_TOKENS
) -> Ollama:
    """
    Fonction utilitaire pour charger le LLM
    
    Args:
        model: Nom du modèle
        temperature: Temperature
        max_tokens: Max tokens
        
    Returns:
        Instance Ollama
    """
    llm_manager = LlamaModel(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return llm_manager.load_model()