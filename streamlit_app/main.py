import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

# Configuration de la page
st.set_page_config(
    page_title="U18 Féminine - Stade Toulousain",
    page_icon="./assets/Logo_Stade_Toulousain_Rugby.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Charger les styles personnalisés
from utils.styles import load_css, create_rugby_title

# CHARGER LES STYLES CSS
load_css()

# Imports des composants
from components.dashboard import show_dashboard
from components.player_analysis import show_player_analysis
from components.match_comparison import show_match_comparison
from components.technical_stats import show_technical_stats
from utils.data_loader import load_data
from analytics.scoring import get_global_score

def create_nav_button(text, page_key, current_page):
    """Crée un bouton de navigation avec style actif si nécessaire"""
    if current_page == page_key:
        st.sidebar.markdown(f"""
        <div style="background: linear-gradient(135deg, #000000 50%, #252525 100%); 
                    color: white; padding: 0.5rem 1rem; border-radius: 10px; 
                    font-weight: bold; margin-bottom: 0.5rem;">
            {text}
        </div>
        """, unsafe_allow_html=True)
    else:
        if st.sidebar.button(text, key=f"nav_{page_key}"):
            st.session_state.page = page_key
            st.rerun()

def main():
    # Titre principal
    create_rugby_title("u18 féminine", "Stade Toulousain")
    
    # Charger les données
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        st.stop()
    
    # Initialiser la page par défaut
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"
    
    # Navigation optimisée
    current_page = st.session_state.page
    
    create_nav_button("Tableau de bord", "dashboard", current_page)
    create_nav_button("Analyse par joueuse", "player", current_page)
    create_nav_button("Comparaison des matchs", "match", current_page)
    create_nav_button("Statistiques techniques", "stats", current_page)

    # Affichage des pages
    if st.session_state.page == "dashboard":
        show_dashboard(df)
    elif st.session_state.page == "player":
        show_player_analysis(df)
    elif st.session_state.page == "match":
        show_match_comparison(df)
    elif st.session_state.page == "stats":
        show_technical_stats(df)

if __name__ == "__main__":
    main()