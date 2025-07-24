import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

# Configuration de la page
st.set_page_config(
    page_title="U18 Stade Toulousain Féminine",
    page_icon="./assets/Logo_Stade_Toulousain_Rugby.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS pour interface propre
st.markdown("""
<style>
    /* Supprimer complètement la barre supérieure */
    header[data-testid="stHeader"] {
        height: 0px;
        display: none;
    }
    
    /* Supprimer le bouton Deploy */
    .stAppDeployButton {
        display: none;
    }
    
    /* Supprimer le menu hamburger */
    #MainMenu {
        display: none;
    }
    
    /* Supprimer le footer "Made with Streamlit" */
    footer {
        display: none;
    }
    
    /* Supprimer l'espace en haut */
    .stApp > header {
        background-color: transparent;
    }
    
    /* Réduire l'espacement en haut */
    .stAppViewContainer .main .block-container {
        padding-top: 1rem;
    }
    
    /* Style personnalisé pour votre app */
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #1f4e79;
        padding-bottom: 1rem;
    }
    
    /* Style pour les métriques */
    .metric-card {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f4e79;
        margin: 0.5rem 0;
    }
    
    /* Style pour la sidebar */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Imports des composants
from components.dashboard import show_dashboard
from components.player_analysis import show_player_analysis
from components.match_comparison import show_match_comparison
from components.technical_stats import show_technical_stats
from utils.data_loader import load_data, get_database_stats

def main():
    # Titre principal (maintenant sans la barre Streamlit)
    st.markdown('<h1 class="main-header">Analyse des Performances Rugby</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar pour la navigation
    st.sidebar.title("Navigation")
    
    # Charger les données
    try:
        df = load_data()
        db_stats = get_database_stats()
        
        # Afficher quelques statistiques de base dans la sidebar
        st.sidebar.markdown("### 📊 Aperçu des données")
        st.sidebar.metric("Nombre de joueuses", db_stats['nb_joueuses'])
        st.sidebar.metric("Nombre de matchs", db_stats['nb_matchs'])
        st.sidebar.metric("Total statistiques", db_stats['nb_stats'])
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        st.stop()
    
    # Menu de navigation
    page = st.sidebar.selectbox(
        "Choisir une analyse",
        [
            "🏠 Tableau de bord",
            "👤 Analyse par joueuse", 
            "⚔️ Comparaison des matchs",
            "📈 Statistiques techniques"
        ]
    )
    
    # Affichage des pages
    if page == "🏠 Tableau de bord":
        show_dashboard(df)
    elif page == "👤 Analyse par joueuse":
        show_player_analysis(df)
    elif page == "⚔️ Comparaison des matchs":
        show_match_comparison(df)
    elif page == "📈 Statistiques techniques":
        show_technical_stats(df)

if __name__ == "__main__":
    main()