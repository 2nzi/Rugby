import streamlit as st
import pandas as pd

def show_player_analysis(df):
    """Composant simple pour l'analyse des joueuses"""
    
    st.header("👤 Analyse des joueuses")
    
    # Liste des joueuses
    players = sorted(df['Nom'].unique())
    selected_player = st.selectbox("Choisir une joueuse", players)
    
    if selected_player:
        # Filtrer les données pour la joueuse sélectionnée
        player_data = df[df['Nom'] == selected_player]
        
        # Nom complet
        player_name = f"{player_data.iloc[0]['Prenom']} {player_data.iloc[0]['Nom']}"
        st.subheader(f"Statistiques de {player_name}")
        
        # Statistiques simples
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_actions = player_data['Nb_actions'].sum()
            st.metric("Total actions", f"{total_actions:.0f}")
        
        with col2:
            nb_matchs = player_data['Match'].nunique()
            st.metric("Matchs joués", nb_matchs)
        
        with col3:
            avg_per_match = total_actions / nb_matchs if nb_matchs > 0 else 0
            st.metric("Moyenne par match", f"{avg_per_match:.1f}")
        
        # Tableau des données
        st.subheader("📊 Détail des actions")
        
        # Résumé par action
        summary = player_data.groupby('Action')['Nb_actions'].sum().reset_index()
        summary = summary.sort_values('Nb_actions', ascending=False)
        
        st.dataframe(summary, use_container_width=True)
        
        # Données détaillées
        with st.expander("Voir toutes les statistiques détaillées"):
            st.dataframe(player_data, use_container_width=True)