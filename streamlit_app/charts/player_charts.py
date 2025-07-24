import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .config import COLORS, COLORSCALE, BASE_LAYOUT

def create_top_players_chart(df, n_players=10):
    """Graphique complet du top des joueuses avec style intégré"""
    
    # Préparer les données
    top_players = df.groupby(['Prenom', 'Nom'])['Nb_actions'].sum().reset_index()
    top_players['Nom_complet'] = top_players['Prenom'] + ' ' + top_players['Nom']
    top_players = top_players.nlargest(n_players, 'Nb_actions')
    
    # Créer le graphique AVEC son style
    fig = px.bar(
        top_players,
        x='Nb_actions',
        y='Nom_complet',
        orientation='h',
        title=f"Top {n_players} des joueuses",
        color='Nb_actions',
        color_continuous_scale=COLORSCALE
    )
    
    # Style intégré directement
    fig.update_layout(
        **BASE_LAYOUT,
        height=400,
        coloraxis_showscale=False,
        yaxis={
            'categoryorder': 'total ascending',
            'title': '',
            'tickfont': dict(color=COLORS['secondary'], size=12)
        },
        xaxis={
            'title': 'Nombre d\'actions',
            'tickfont': dict(color=COLORS['secondary'], size=11)
        },
        title={
            'font': dict(color=COLORS['primary'], size=16, family='Arial Black'),
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    
    # Axes
    fig.update_xaxes(
        showgrid=True,
        gridcolor=COLORS['light_red'],
        zeroline=True,
        zerolinecolor=COLORS['primary']
    )
    
    fig.update_yaxes(showgrid=False)
    fig.update_xaxes(showgrid=False)
    
    return fig

def create_player_actions_pie(df, player_name):
    """Graphique en camembert des actions d'une joueuse"""
    
    player_data = df[df['Nom'].str.contains(player_name, case=False)]
    if player_data.empty:
        return None
    
    action_breakdown = player_data.groupby('Action')['Nb_actions'].sum().reset_index()
    
    fig = px.pie(
        action_breakdown,
        values='Nb_actions',
        names='Action',
        title=f"Actions de {player_name}",
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['gray']]
    )
    
    # Style spécifique au pie chart
    fig.update_layout(
        **BASE_LAYOUT,
        title={
            'font': dict(color=COLORS['primary'], size=16, family='Arial Black'),
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    
    fig.update_traces(
        textfont_size=12,
        textfont_color='white',
        marker=dict(line=dict(color='white', width=2))
    )
    
    return fig

def create_player_level_distribution(df, player_name):
    """Distribution des niveaux pour une joueuse"""
    
    player_data = df[df['Nom'].str.contains(player_name, case=False)]
    if player_data.empty:
        return None
    
    level_data = player_data.groupby('Niveau')['Nb_actions'].sum().reset_index()
    level_data['Niveau_label'] = level_data['Niveau'].map({
        0: 'Basique', 1: 'Correct', 2: 'Bon', 3: 'Excellent'
    })
    
    fig = px.bar(
        level_data,
        x='Niveau_label',
        y='Nb_actions',
        title=f"Niveau de performance - {player_name}",
        color='Niveau',
        color_continuous_scale=COLORSCALE
    )
    
    fig.update_layout(
        **BASE_LAYOUT,
        xaxis={'title': 'Niveau de performance'},
        yaxis={'title': 'Nombre d\'actions'},
        title={
            'font': dict(color=COLORS['primary'], size=16, family='Arial Black'),
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    
    return fig

def create_player_profile_chart(df, player_name):
    """Graphique de profil d'une joueuse - alias pour create_player_actions_pie"""
    return create_player_actions_pie(df, player_name)

def create_player_evolution_chart(df, player_name):
    """Évolution d'une joueuse par match"""
    
    player_data = df[df['Nom'].str.contains(player_name, case=False)]
    if player_data.empty:
        return None
    
    evolution = player_data.groupby('Match')['Nb_actions'].sum().reset_index()
    
    fig = px.line(
        evolution,
        x='Match',
        y='Nb_actions',
        title=f"Évolution de {player_name}",
        markers=True
    )
    
    fig.update_traces(
        line_color=COLORS['primary'],
        marker_color=COLORS['primary'],
        marker_size=8
    )
    
    fig.update_layout(
        **BASE_LAYOUT,
        title={
            'font': dict(color=COLORS['primary'], size=16, family='Arial Black'),
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    
    return fig

def create_player_comparison_radar(df, players_list):
    """Graphique radar simple pour comparer des joueuses"""
    
    # Version simplifiée pour éviter les erreurs
    if not players_list or len(players_list) == 0:
        return None
    
    # Pour l'instant, retournons un graphique simple
    player = players_list[0]
    player_data = df[df['Nom'].str.contains(player, case=False)]
    
    if player_data.empty:
        return None
    
    action_breakdown = player_data.groupby('Action')['Nb_actions'].sum().reset_index()
    
    fig = px.bar(
        action_breakdown,
        x='Action',
        y='Nb_actions',
        title=f"Profil de {player}",
        color='Nb_actions',
        color_continuous_scale=COLORSCALE
    )
    
    fig.update_layout(**BASE_LAYOUT)
    
    return fig