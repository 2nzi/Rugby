import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.chart_styles import create_custom_bar_chart, apply_stade_style, get_stade_toulousain_colors

def create_top_players_chart(df, n_players=10):
    """Graphique du top des joueuses"""
    
    top_players = df.groupby(['Prenom', 'Nom'])['Nb_actions'].sum().reset_index()
    top_players['Nom_complet'] = top_players['Prenom'] + ' ' + top_players['Nom']
    top_players = top_players.nlargest(n_players, 'Nb_actions')
    
    return create_custom_bar_chart(
        data=top_players,
        x='Nb_actions',
        y='Nom_complet',
        title=f"Top {n_players} des joueuses",
        orientation='h'
    )

def create_player_profile_chart(df, player_name):
    """Graphique de profil d'une joueuse"""
    
    player_data = df[df['Nom'].str.contains(player_name, case=False)]
    if player_data.empty:
        return None
    
    # Actions par type
    action_breakdown = player_data.groupby('Action')['Nb_actions'].sum().reset_index()
    
    fig = px.pie(
        action_breakdown,
        values='Nb_actions',
        names='Action',
        title=f"Répartition des actions - {player_name}",
        color_discrete_sequence=get_stade_toulousain_colors()
    )
    
    return apply_stade_style(fig)

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
        markers=True,
        line_shape='spline'
    )
    
    fig.update_traces(
        line_color='#CC0C13',
        marker_color='#CC0C13',
        marker_size=8
    )
    
    return apply_stade_style(fig)

def create_player_comparison_radar(df, players_list):
    """Graphique radar pour comparer des joueuses"""
    
    if len(players_list) > 4:
        players_list = players_list[:4]  # Limiter à 4 joueuses
    
    # Préparer les données
    comparison_data = []
    actions = df['Action'].unique()
    
    for player in players_list:
        player_data = df[df['Nom'].str.contains(player, case=False)]
        player_stats = []
        
        for action in actions:
            total = player_data[player_data['Action'] == action]['Nb_actions'].sum()
            player_stats.append(total)
        
        comparison_data.append({
            'player': player,
            'actions': actions,
            'values': player_stats
        })
    
    # Créer le radar
    fig = go.Figure()
    
    colors = get_stade_toulousain_colors()
    
    for i, data in enumerate(comparison_data):
        fig.add_trace(go.Scatterpolar(
            r=data['values'],
            theta=data['actions'],
            fill='toself',
            name=data['player'],
            line_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max([max(d['values']) for d in comparison_data])]),
            bgcolor='rgba(248, 249, 250, 0.5)'
        ),
        title="Comparaison des joueuses",
        showlegend=True
    )
    
    return apply_stade_style(fig)