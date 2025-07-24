import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from charts import (
    create_top_players_chart, 
    create_actions_distribution_chart, 
    create_matches_activity_chart,
    create_performance_heatmap,        # ← NOUVEAU
    create_team_activity_heatmap       # ← NOUVEAU
)

def show_dashboard(df):
    """Affiche le tableau de bord principal"""
        
    st.divider()
    
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
        fig = create_top_players_chart(df, n_players=10)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_actions_distribution_chart(df)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Graphiques pleine largeur
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_matches_activity_chart(df)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_team_activity_heatmap(df)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()

    fig = create_performance_heatmap(df, n_players=15)
    st.plotly_chart(fig, use_container_width=True)