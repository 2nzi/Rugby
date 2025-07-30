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
    

    from streamlit_option_menu import option_menu

    with st.sidebar:
        selected = option_menu( None, 
                ["Tableau de bord", 'Analyse par joueuse', 'Comparaison des matchs', 'Statistiques techniques'], 
                icons=None, default_index=1,
                menu_icon="cast",
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"display": "None"}, 
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin":"3px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "#000000"},
                }
            )
    # Affichage des pages
    if selected == "Tableau de bord":
        show_dashboard(df)
    elif selected == "Analyse par joueuse":
        show_player_analysis(df)
    elif selected == "Comparaison des matchs":
        show_match_comparison(df)
    elif selected == "Statistiques techniques":
        show_technical_stats(df)

if __name__ == "__main__":
    main()