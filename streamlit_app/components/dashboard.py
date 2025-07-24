import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from charts import create_top_players_chart, create_actions_distribution_chart, create_matches_activity_chart

def show_dashboard(df):
    """Affiche le tableau de bord principal"""
    
    st.header("🏠 Tableau de bord général")
    
    # Métriques générales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_actions = df['Nb_actions'].sum()
        st.metric("Total actions", f"{total_actions:,.0f}")
    
    with col2:
        nb_joueuses = df['Nom'].nunique()
        st.metric("Joueuses actives", nb_joueuses)
    
    with col3:
        nb_matchs = df['Match'].nunique()
        st.metric("Matchs analysés", nb_matchs)
    
    with col4:
        avg_actions = df.groupby(['Prenom', 'Nom'])['Nb_actions'].sum().mean()
        st.metric("Moy. actions/joueuse", f"{avg_actions:.0f}")
    
    st.divider()
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        # USAGE ULTRA-SIMPLE
        fig = create_top_players_chart(df, n_players=10)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # AUTRE GRAPHIQUE
        fig = create_actions_distribution_chart(df)
        st.plotly_chart(fig, use_container_width=True)
    
    col3, col4 = st.columns(2)

    with col3:
        # Graphique pleine largeur
        fig = create_matches_activity_chart(df)
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        # Heatmap des performances
        # Préparer les données pour la heatmap
        heatmap_data = df.groupby(['Nom', 'Match'])['Nb_actions'].sum().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='Nom', columns='Match', values='Nb_actions').fillna(0)
        
        # Limiter aux 15 meilleures joueuses pour la lisibilité
        top_15_players = df.groupby('Nom')['Nb_actions'].sum().nlargest(15).index
        heatmap_pivot = heatmap_pivot.loc[top_15_players]
        
        fig = px.imshow(
            heatmap_pivot,
            aspect='auto',
            title="Intensité d'activité par joueuse et match",
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)