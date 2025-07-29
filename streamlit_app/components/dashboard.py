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
    st.write(calculate_player_scoring(df)['by_player_match'])

    # Calculer la moyenne des notes par match et action
    scoring_data = calculate_player_scoring(df)['by_action']
    avg_scores = scoring_data.groupby(['Match', 'Action'])['note_match_joueuse'].mean().reset_index()
        
    # Trouver la meilleure note par match avec le nom et prénom de la joueuse
    best_scores_with_names = scoring_data.loc[scoring_data.groupby(['Match'])['note_match_joueuse'].idxmax()][['Match', 'Prenom', 'Nom', 'note_match_joueuse']].reset_index(drop=True)
    st.write("Meilleures notes par match :")
    st.write(best_scores_with_names)

    # Trouver la moins bonne note par match avec le nom et prénom de la joueuse
    worst_scores_with_names = scoring_data.loc[scoring_data.groupby(['Match'])['note_match_joueuse'].idxmin()][['Match', 'Prenom', 'Nom', 'note_match_joueuse']].reset_index(drop=True)
    st.write("Moins bonnes notes par match :")
    st.write(worst_scores_with_names)

    # Calculer la plage dynamique : min note globale -10 à max note globale +10
    min_note = scoring_data['note_match_joueuse'].min()
    max_note = scoring_data['note_match_joueuse'].max()
    y_range = [min_note - 10, max_note + 10]
    
    # Créer un graphique avec deux axes Y
    fig = go.Figure()
    
    # Ajouter le graphique en barres sur l'axe Y gauche avec dégradé de couleurs
    from charts.config import COLORS
    
    actions = avg_scores['Action'].unique()
    n_actions = len(actions)
    
    for i, action in enumerate(actions):
        action_data = avg_scores[avg_scores['Action'] == action]
        # Calculer la couleur avec un dégradé de secondary (noir) à primary (rouge)
        ratio = i / (n_actions - 1) if n_actions > 1 else 0
        color = f"rgba({204 * ratio + 0 * (1-ratio):.0f}, {12 * ratio + 0 * (1-ratio):.0f}, {19 * ratio + 0 * (1-ratio):.0f}, 1)"
        
        fig.add_trace(
            go.Bar(
                x=action_data['Match'],
                y=action_data['note_match_joueuse'],
                name=action,
                yaxis='y',
                marker_color=color
            )
        )
    
    # Ajouter un graphique en ligne sur l'axe Y droit (nombre d'actions)
    match_sum = scoring_data.groupby(['Match'])['nb_total_actions'].sum().reset_index()
    fig.add_trace(
        go.Scatter(
            x=match_sum['Match'],
            y=match_sum['nb_total_actions'],
            name='Nombre total d\'actions',
            yaxis='y2',
            line=dict(color='#226D68', width=3),
            marker=dict(color='#76CDCD', size=8),
            mode='lines+markers'
        )
    )

    # Ajouter les meilleures notes par match (même échelle que les barres)
    best_scores = scoring_data.groupby(['Match'])['note_match_joueuse'].max().reset_index()
    # Récupérer les noms des joueuses avec les meilleures notes
    best_scores_with_names = scoring_data.loc[scoring_data.groupby(['Match'])['note_match_joueuse'].idxmax()][['Match', 'Prenom', 'Nom', 'note_match_joueuse']].reset_index(drop=True)

    fig.add_trace(
        go.Scatter(
            x=best_scores_with_names['Match'],
            y=best_scores_with_names['note_match_joueuse'],
            name='Meilleure note par match',
            yaxis='y',  # Même axe que les barres
            line=dict(width=0),  # Pas de ligne
            marker=dict(color='#2E8B57', size=10),  # Vert foncé, marqueur plus gros
            mode='markers+text',
            text=best_scores_with_names['Prenom'] + ' ' + best_scores_with_names['Nom'],
            textposition='top center',
            textfont=dict(size=10, color='#2E8B57')
        )
    )

    # Ajouter les moins bonnes notes par match (même échelle que les barres)
    worst_scores = scoring_data.groupby(['Match'])['note_match_joueuse'].min().reset_index()
    # Récupérer les noms des joueuses avec les moins bonnes notes
    worst_scores_with_names = scoring_data.loc[scoring_data.groupby(['Match'])['note_match_joueuse'].idxmin()][['Match', 'Prenom', 'Nom', 'note_match_joueuse']].reset_index(drop=True)

    fig.add_trace(
        go.Scatter(
            x=worst_scores_with_names['Match'],
            y=worst_scores_with_names['note_match_joueuse'],
            name='Moins bonne note par match',
            yaxis='y',  # Même axe que les barres
            line=dict(width=0),  # Pas de ligne
            marker=dict(color='#FF8C00', size=10),  # Orange foncé pour une meilleure visibilité
            mode='markers+text',
            text=worst_scores_with_names['Prenom'] + ' ' + worst_scores_with_names['Nom'],
            textposition='bottom center',
            textfont=dict(size=10, color='#FF8C00')
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