import streamlit as st
from difflib import get_close_matches

def create_sidebar(data):
    """Crée la barre latérale avec les contrôles"""
    with st.sidebar:
        st.header("Configuration")
        
        # Sélection de la ville
        selected_ville = st.selectbox(
            "Sélectionner une ville",
            options=data['Ville'].unique()
        )
        
        # Filtrer les joueurs pour la ville sélectionnée
        ville_players = data[data['Ville'] == selected_ville]['name'].unique()
        
        # Sélection du joueur
        selected_player = st.selectbox(
            "Sélectionner un joueur",
            options=ville_players
        )
        
    return selected_ville, selected_player

def create_main_layout(data, selected_ville):
    """Crée la disposition principale de l'application"""
    # Affichage des données brutes dans un expander
    with st.expander("Voir les données brutes"):
        st.dataframe(data[data['Ville'] == selected_ville])
    
    # Création des colonnes pour l'affichage
    col1, col2 = st.columns([3, 4])
    
    return col1, col2