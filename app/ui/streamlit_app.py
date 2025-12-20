"""
Interface Streamlit pour le système RAG
"""
import streamlit as st
import requests
import time
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="RAG Local Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL de l'API
API_URL = "http://localhost:8000"

# ==================== STYLES CSS ====================

def load_custom_css():
    """Charge le CSS personnalisé"""
    st.markdown("""
        <style>
        /* Fond noir général */
        .stApp {
            background-color: #000000;
        }
        
        /* Texte blanc par défaut */
        .stApp, p, span, label, h1, h2, h3 {
            color: #FFFFFF !important;
        }
        
        /* Sidebar noir */
        section[data-testid="stSidebar"] {
            background-color: #0a0a0a;
            border-right: 2px solid #8B5CF6;
        }
        
        /* Inputs et text areas */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: #1a1a1a;
            color: #FFFFFF;
            border: 1px solid #8B5CF6;
        }
        
        /* Boutons */
        .stButton > button {
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(139, 92, 246, 0.4);
        }
        
        /* File uploader */
        .stFileUploader {
            background-color: #1a1a1a;
            border: 2px dashed #8B5CF6;
            border-radius: 10px;
            padding: 20px;
        }
        
        /* Messages de chat */
        .chat-message {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            animation: fadeIn 0.3s;
        }
        
        .user-message {
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            margin-left: 20%;
        }
        
        .bot-message {
            background-color: #1a1a1a;
            border: 1px solid #8B5CF6;
            margin-right: 20%;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #1a1a1a;
            color: #FFFFFF;
            border: 1px solid #8B5CF6;
        }
        
        /* Success/Error boxes */
        .stSuccess, .stError, .stWarning, .stInfo {
            background-color: #1a1a1a;
            border-left: 4px solid #8B5CF6;
            color: #FFFFFF;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            color: #8B5CF6 !important;
            font-size: 2rem !important;
        }
        
        /* Headers avec gradient */
        .gradient-text {
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        </style>
    """, unsafe_allow_html=True)


# ==================== FONCTIONS API ====================

def check_api_status():
    """Vérifie le statut de l'API"""
    try:
        response = requests.get(f"{API_URL}/status", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def upload_files_to_api(files):
    """Upload les fichiers vers l'API"""
    try:
        files_data = [
            ("files", (file.name, file, file.type))
            for file in files
        ]
        response = requests.post(f"{API_URL}/upload", files=files_data)
        return response.json()
    except Exception as e:
        st.error(f"Erreur: {str(e)}")
        return None


def ingest_documents():
    """Lance l'ingestion des documents"""
    try:
        response = requests.post(f"{API_URL}/ingest")
        return response.json()
    except Exception as e:
        st.error(f"Erreur: {str(e)}")
        return None


def query_documents(question):
    """Pose une question aux documents"""
    try:
        response = requests.post(
            f"{API_URL}/query",
            json={"question": question}
        )
        return response.json()
    except Exception as e:
        st.error(f"Erreur: {str(e)}")
        return None


def reset_system():
    """Réinitialise le système"""
    try:
        response = requests.delete(f"{API_URL}/reset")
        return response.json()
    except Exception as e:
        st.error(f"Erreur: {str(e)}")
        return None


# ==================== INTERFACE PRINCIPALE ====================

def main():
    # Charger le CSS
    load_custom_css()
    
    # Header avec gradient
    st.markdown("""
        <h1 class="gradient-text" style="text-align: center; font-size: 3rem; margin-bottom: 0;">
            🤖 RAG Local Chatbot
        </h1>
        <p style="text-align: center; color: #9CA3AF; font-size: 1.2rem; margin-top: 0;">
            Question-Réponse Intelligent basé sur vos Documents • 100% Local
        </p>
        <hr style="border: 1px solid #8B5CF6; margin: 20px 0;">
    """, unsafe_allow_html=True)
    
    # Vérifier le statut de l'API
    status = check_api_status()
    
    if status is None:
        st.error("⚠️ API non accessible. Assurez-vous que FastAPI est lancé (python -m uvicorn app.api.main:app --reload)")
        st.stop()
    
    # ==================== SIDEBAR ====================
    
    with st.sidebar:
        st.markdown("### 📊 Tableau de bord")
        
        # Statut du système
        if status:
            details = status.get('details', {})
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📁 Fichiers", details.get('files_uploaded', 0))
            with col2:
                index_status = "✅" if details.get('index_exists') else "❌"
                st.metric("🗄️ Index", index_status)
            
            rag_status = "🟢 Prêt" if details.get('rag_initialized') else "🔴 Non initialisé"
            st.info(f"**Statut RAG:** {rag_status}")
        
        st.markdown("---")
        
        # Section Upload
        st.markdown("### 📤 Importer des documents")
        
        uploaded_files = st.file_uploader(
            "Choisissez vos fichiers",
            type=['pdf', 'docx', 'html', 'pptx'],
            accept_multiple_files=True,
            help="Formats supportés: PDF, DOCX, HTML, PPTX"
        )
        
        if uploaded_files:
            if st.button("⬆️ Upload", use_container_width=True):
                with st.spinner("Upload en cours..."):
                    result = upload_files_to_api(uploaded_files)
                    if result:
                        st.success(f"✅ {result['message']}")
                        st.rerun()
        
        st.markdown("---")
        
        # Section Indexation
        st.markdown("### 🔄 Indexation")
        
        if st.button("🚀 Indexer les documents", use_container_width=True):
            with st.spinner("Indexation en cours... (cela peut prendre quelques minutes)"):
                progress_bar = st.progress(0)
                
                for i in range(100):
                    time.sleep(0.05)
                    progress_bar.progress(i + 1)
                
                result = ingest_documents()
                
                if result and result.get('status') == 'success':
                    st.success("✅ Indexation réussie!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de l'indexation")
        
        st.markdown("---")
        
        # Section Réinitialisation
        st.markdown("### 🗑️ Réinitialiser")
        
        if st.button("🔄 Tout supprimer", use_container_width=True, type="secondary"):
            if st.checkbox("Confirmer la suppression"):
                result = reset_system()
                if result:
                    st.success("✅ Système réinitialisé")
                    st.rerun()
    
    # ==================== ZONE PRINCIPALE ====================
    
    # Vérifier si le système est prêt
    if not status.get('details', {}).get('rag_initialized'):
        st.warning("⚠️ **Système non initialisé**")
        st.info("""
        **Pour commencer :**
        1. 📤 Uploadez vos documents dans la barre latérale
        2. 🚀 Cliquez sur "Indexer les documents"
        3. 💬 Posez vos questions !
        """)
        st.stop()
    
    # Zone de chat
    st.markdown("### 💬 Posez vos questions")
    
    # Initialiser l'historique de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Afficher l'historique
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>🧑 Vous:</strong><br>{message["content"]}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="chat-message bot-message">
                        <strong>🤖 Assistant:</strong><br>{message["content"]}
                    </div>
                """, unsafe_allow_html=True)
                
                # Afficher les sources si disponibles
                if "sources" in message and message["sources"]:
                    with st.expander("📚 Voir les sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.markdown(f"""
                                **Source {i}:** {source.get('source', 'Inconnu')} (Page {source.get('page', 'N/A')})
                                
                                *Extrait:* {source.get('content', '')}
                            """)
    
    # Input utilisateur
    with st.container():
        col1, col2 = st.columns([5, 1])
        
        with col1:
            user_input = st.text_input(
                "Votre question",
                placeholder="Posez votre question sur les documents...",
                label_visibility="collapsed"
            )
        
        with col2:
            send_button = st.button("📤 Envoyer", use_container_width=True)
    
    # Traiter la question
    if send_button and user_input:
        # Ajouter la question à l'historique
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Obtenir la réponse
        with st.spinner("🔍 Recherche dans les documents..."):
            response = query_documents(user_input)
            
            if response and response.get('success'):
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.get('answer', ''),
                    "sources": response.get('sources', [])
                })
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "❌ Erreur lors de la recherche."
                })
        
        st.rerun()
    
    # Bouton pour effacer l'historique
    if st.session_state.messages:
        if st.button("🗑️ Effacer l'historique"):
            st.session_state.messages = []
            st.rerun()


# ==================== MAIN ====================

if __name__ == "__main__":
    main()