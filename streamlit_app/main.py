import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

# Configuration de la page
st.set_page_config(
    page_title="Analyse Rugby - Équipe Féminine",
    page_icon="🏉",
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
from utils.data_loader import load_data, get_database_stats

def main():
    # Titre principal
    create_rugby_title("🏉 U18 Stade Toulousain Féminine")
    
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