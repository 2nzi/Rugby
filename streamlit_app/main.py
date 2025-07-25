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

def main():
    # Titre principal
    create_rugby_title("u18 féminine", "Stade Toulousain")
    
    
    # Charger les données
    try:
        df = load_data()
        
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

    actions_interessees = [
        "DUEL",
        "PASSE",
        "PLAQUAGE",
        "RUCK",
        "JAP",
        "RECEPTION JAP"
    ]

    facteur_pond = 100/3
    # Calcul du score pondéré par (match, joueuse, action)
    df_grouped = df.groupby(
        ["Match", "Prenom", "Nom", "Action"]
    ).apply(
        lambda g: pd.Series({
            "score_pondere": (g["Niveau"] * g["Nb_actions"]).sum() / g["Nb_actions"].sum(),
            "nb_total_actions": g["Nb_actions"].sum()
        })
    ).reset_index()

    # On filtre uniquement sur les actions intéressées (attention à la casse)
    score_actions = df_grouped[df_grouped["Action"].str.upper().isin(actions_interessees)]

    # Calcul de la note moyenne par (match, joueuse)
    score_actions["note_match_joueuse"] = score_actions.groupby(
        ["Match", "Prenom", "Nom"]
    )["score_pondere"].transform("mean")*facteur_pond

    # Affichage détaillé (par action)
    st.write("df1")
    st.dataframe(score_actions)

    score_match_joueuse = score_actions.drop_duplicates(subset=["Match", "Prenom", "Nom"])[["Match", "Prenom", "Nom", "note_match_joueuse"]]
    
    st.write("df2")
    st.dataframe(score_match_joueuse)

    score_match = score_match_joueuse.groupby(["Match"]).apply(
        lambda g: pd.Series({
            "note_match_joueuse": g["note_match_joueuse"].mean()
        })
    ).reset_index()
    st.write("df3")
    st.dataframe(score_match)

    st.write("note_moyenne_match_joueuse")
    st.write(round(score_match["note_match_joueuse"].mean(), 2))


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