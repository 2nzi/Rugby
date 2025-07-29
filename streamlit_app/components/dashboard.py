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
    create_team_activity_heatmap,       # ← NOUVEAU
    create_performance_comparison_chart  # ← NOUVEAU
)
from analytics.scoring import *

def show_dashboard(df):
    """Affiche le tableau de bord principal"""



    st.divider()
    
    # Métriques générales

    metrics_config = [
        {
            "title": "Moy. note match",
            "value": get_global_score(df),
            "format": "{:,.2f}"
        },
        {
            "title": "Total actions",
            "value": df['Nb_actions'].sum(),
            "format": "{:,.0f}"
        },
        {
            "title": "Joueuses actives", 
            "value": df['Nom'].nunique(),
            "format": "{}"
        },
        {
            "title": "Matchs analysés",
            "value": df['Match'].nunique(), 
            "format": "{}"
        },
        {
            "title": "Moy. actions/joueuse",
            "value": df.groupby(['Prenom', 'Nom'])['Nb_actions'].sum().mean(),
            "format": "{:.0f}"
        }
    ]
    
    # Création des colonnes dynamiquement
    cols = st.columns(len(metrics_config))
    
    # Affichage des métriques avec une boucle
    for i, metric in enumerate(metrics_config):
        with cols[i]:
            formatted_value = metric["format"].format(metric["value"])
            st.metric(metric["title"], formatted_value)

    
    st.divider()
    


    fig = create_performance_comparison_chart(df)
    st.plotly_chart(fig, use_container_width=True)

    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        fig = create_top_players_chart(df, n_players=15)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = create_actions_distribution_chart(df)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Graphiques pleine largeur
    # col1, col2 = st.columns(2)
    
    # with col1:
    #     fig = create_matches_activity_chart(df)
    #     st.plotly_chart(fig, use_container_width=True)
    
    # with col2:
    #     fig = create_team_activity_heatmap(df)
    #     st.plotly_chart(fig, use_container_width=True)
    
    # st.divider()

    # fig = create_performance_heatmap(df, n_players=15)
    # st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
