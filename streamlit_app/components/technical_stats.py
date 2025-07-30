import streamlit as st
import pandas as pd

def show_technical_stats(df):
    """Composant simple pour les statistiques techniques"""
    
    st.header("In progress...")


    # st.header("📈 Statistiques techniques")
    
    # # Analyse par type d'action
    # st.subheader("⚽ Analyse par type d'action")
    
    # action_stats = df.groupby('Action').agg({
    #     'Nb_actions': ['sum', 'mean', 'count'],
    #     'Niveau': 'mean'
    # }).round(2)
    
    # # Aplatir les colonnes multi-niveau
    # action_stats.columns = ['Total', 'Moyenne', 'Occurrences', 'Niveau_moyen']
    # action_stats = action_stats.sort_values('Total', ascending=False)
    
    # st.dataframe(action_stats, use_container_width=True)
    
    # # Analyse par niveau de performance
    # st.subheader("⭐ Analyse par niveau de performance")
    
    # niveau_stats = df.groupby('Niveau').agg({
    #     'Nb_actions': ['sum', 'count'],
    #     'Action': lambda x: x.nunique()
    # }).round(2)
    
    # niveau_stats.columns = ['Total_actions', 'Occurrences', 'Types_action']
    
    # # Ajouter des labels
    # niveau_labels = {0: 'Basique', 1: 'Correct', 2: 'Bon', 3: 'Excellent'}
    # niveau_stats['Label'] = niveau_stats.index.map(niveau_labels)
    
    # st.dataframe(niveau_stats, use_container_width=True)
    
    # # Top performers par action
    # st.subheader("🏆 Top performers par action")
    
    # action_choice = st.selectbox("Choisir une action", sorted(df['Action'].unique()))
    
    # if action_choice:
    #     top_performers = df[df['Action'] == action_choice].groupby(['Prenom', 'Nom'])['Nb_actions'].sum().reset_index()
    #     top_performers['Nom_complet'] = top_performers['Prenom'] + ' ' + top_performers['Nom']
    #     top_performers = top_performers.sort_values('Nb_actions', ascending=False).head(10)
        
    #     st.dataframe(
    #         top_performers[['Nom_complet', 'Nb_actions']], 
    #         use_container_width=True,
    #         hide_index=True
    #     )