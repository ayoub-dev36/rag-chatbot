"""
Pipeline RAG - VERSION OPTIMISÉE
Prompt identique au test qui fonctionne
"""
from pathlib import Path
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from config.settings import BASE_DIR


class RAGPipeline:
    """Pipeline RAG complet"""
    
    def __init__(self, llm: Ollama, retriever):
        self.llm = llm
        self.retriever = retriever
        self.chain = None
    
    def get_prompt_template(self) -> PromptTemplate:
        """
        Template de prompt OPTIMISÉ
        ✅ IDENTIQUE au test qui fonctionne
        """
        template = """Réponds à la question en utilisant UNIQUEMENT le contexte fourni.

CONTEXTE:
{context}

QUESTION: {question}

Si la réponse est dans le contexte, réponds clairement.
Si la réponse n'est PAS dans le contexte, dis: "Information non trouvée."

RÉPONSE:"""
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def build_chain(self) -> RetrievalQA:
        """Construit la chaîne RAG"""
        print(f"🔗 Construction de la chaîne RAG")
        
        try:
            prompt = self.get_prompt_template()
            
            self.chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.retriever,
                return_source_documents=True,
                chain_type_kwargs={
                    "prompt": prompt,
                    "verbose": False
                }
            )
            
            print("✓ Chaîne RAG construite")
            return self.chain
            
        except Exception as e:
            raise RuntimeError(f"Erreur construction chaîne: {str(e)}")
    
    def query(self, question: str) -> dict:
        """Pose une question au système RAG"""
        if self.chain is None:
            self.build_chain()
        
        print(f"\n❓ Question: {question}")
        
        try:
            # LangChain 0.1.20+ utilise invoke
            response = self.chain.invoke({"query": question})
            
            print(f"✓ Réponse générée")
            print(f"  - Sources: {len(response.get('source_documents', []))}")
            
            return response
            
        except Exception as e:
            print(f"❌ Erreur requête: {str(e)}")
            raise


def build_rag_chain(llm: Ollama, retriever) -> RetrievalQA:
    """Fonction utilitaire"""
    pipeline = RAGPipeline(llm, retriever)
    return pipeline.build_chain()