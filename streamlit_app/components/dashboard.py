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
from analytics.scoring import *

def show_dashboard(df):
    """Affiche le tableau de bord principal"""


    # st.write(calculate_player_scoring(df))
    # st.write(calculate_player_scoring(df)['by_action'])

    # Calculer la moyenne des notes par match et action
    scoring_data = calculate_player_scoring(df)['by_action']
    avg_scores = scoring_data.groupby(['Match', 'Action'])['note_match_joueuse'].mean().reset_index()
    
    # Calculer la plage dynamique : min note moyenne -10 à max note moyenne +10
    min_note = avg_scores['note_match_joueuse'].min()
    max_note = avg_scores['note_match_joueuse'].max()
    y_range = [min_note - 10, max_note + 10]
    
    # Créer un graphique avec deux axes Y
    fig = go.Figure()
    
    # Ajouter le graphique en barres sur l'axe Y gauche
    for action in avg_scores['Action'].unique():
        action_data = avg_scores[avg_scores['Action'] == action]
        fig.add_trace(
            go.Bar(
                x=action_data['Match'],
                y=action_data['note_match_joueuse'],
                name=action,
                yaxis='y'
            )
        )
    
    # Ajouter un graphique en ligne sur l'axe Y droit (exemple avec la moyenne générale par match)
    match_sum = scoring_data.groupby(['Match'])['nb_total_actions'].sum().reset_index()
    fig.add_trace(
        go.Scatter(
            x=match_sum['Match'],
            y=match_sum['nb_total_actions'],
            name='Moyenne générale',
            yaxis='y2',
            line=dict(color='black', width=3),
            mode='lines+markers'
        )
    )
    
    # Configuration des axes
    fig.update_layout(
        title="Moyenne des notes par match et action",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        yaxis=dict(
            title="Note moyenne par action",
            range=y_range,
            side='left'
        ),
        yaxis2=dict(
            title="Nombre d'actions dans le match",
            side='right',
            overlaying='y'
        ),
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)
    # perf_by_action_chart(df)


    st.divider()
    
    # Métriques générales
    # Configuration des métriques
    # st.dataframe(df)

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