import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .config import COLORS, COLORSCALE, COLORSCALE_HEATMAP, BASE_LAYOUT, apply_stade_style

def create_top_players_chart(df, n_players=10):
    """Graphique complet du top des joueuses basé sur les notes moyennes"""
    
    from analytics.scoring import calculate_player_scoring
    
    # Calculer les notes moyennes par joueuse
    scoring_data = calculate_player_scoring(df)['by_player_match']
    top_players = scoring_data.groupby(['Prenom', 'Nom'])['note_match_joueuse'].mean().reset_index()
    top_players['Nom_complet'] = top_players['Prenom'] + ' ' + top_players['Nom']
    top_players = top_players.nlargest(n_players, 'note_match_joueuse')
    
    # Créer le graphique AVEC son style
    fig = px.bar(
        top_players,
        x='note_match_joueuse',
        y='Nom_complet',
        orientation='h',
        title=f"Top {n_players} des joueuses par note moyenne",
        color='note_match_joueuse',
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
            'title': 'Note moyenne',
            'tickfont': dict(color=COLORS['secondary'], size=11)
        },
        title={
            'font': dict(color=COLORS['secondary'], size=16, family='Arial Black'),
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
            'font': dict(color=COLORS['secondary'], size=16, family='Arial Black'),
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
        0: '0', 1: '1', 2: '2', 3: '3'
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
            'font': dict(color=COLORS['secondary'], size=16, family='Arial Black'),
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

def create_performance_heatmap(df, n_players=15):
    """Heatmap des performances - BLANC -> ROUGE uniquement"""
    
    # Préparer les données pour la heatmap
    heatmap_data = df.groupby(['Nom', 'Match'])['Nb_actions'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Nom', columns='Match', values='Nb_actions').fillna(0)
    
    # Limiter aux meilleures joueuses pour la lisibilité
    top_players = df.groupby('Nom')['Nb_actions'].sum().nlargest(n_players).index
    heatmap_pivot = heatmap_pivot.loc[top_players]
    
    # Créer la heatmap avec BLANC -> ROUGE ← CHANGEMENT ICI
    fig = px.imshow(
        heatmap_pivot,
        aspect='auto',
        title=f"Intensité d'activité - Top {n_players}",
        color_continuous_scale=COLORSCALE_HEATMAP,  # ← BLANC -> ROUGE
        labels={'color': 'Nb actions'}
    )
    
    # ENLEVER LA COLORSCALE LEGEND
    fig.update_traces(showscale=False)
    
    # Appliquer le style Stade Toulousain
    fig.update_layout(
        **BASE_LAYOUT,
        height=600,
        coloraxis_showscale=False,
        title={
            'font': dict(color=COLORS['secondary'], size=16, family='Arial Black'),
            'x': 0.5,
            'xanchor': 'center'
        },
        # Style des axes
        xaxis={
            'title': 'Matchs',
            'tickfont': dict(color=COLORS['secondary'], size=10),
            'tickangle': 45  # Incliner les noms de matchs pour la lisibilité
        },
        yaxis={
            'title': 'Joueuses',
            'tickfont': dict(color=COLORS['secondary'], size=10)
        }
    )
    
    # Personnaliser le hover
    fig.update_traces(
        hoverlabel=dict(
            bgcolor=COLORS['primary'],
            font_color='white',
            font_size=12
        )
    )
    
    return fig

def create_team_activity_heatmap(df):
    """Heatmap par action/niveau - BLANC -> ROUGE uniquement"""
    
    # Préparer les données : Actions vs Niveaux
    heatmap_data = df.groupby(['Action', 'Niveau'])['Nb_actions'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Action', columns='Niveau', values='Nb_actions').fillna(0)
    
    # Renommer les colonnes pour plus de clarté
    level_labels = {0: '0', 1: '1', 2: '2', 3: '3'}
    heatmap_pivot.columns = [level_labels.get(col, f'Niveau {col}') for col in heatmap_pivot.columns]
    
    fig = px.imshow(
        heatmap_pivot,
        aspect='auto',
        title="Intensité par action et niveau",
        color_continuous_scale=COLORSCALE_HEATMAP
    )
    
    # Style Stade Toulousain
    fig.update_traces(showscale=False)
    
    fig.update_layout(
        **BASE_LAYOUT,
        height=400,
        coloraxis_showscale=False,
        title={
            'font': dict(color=COLORS['secondary'], size=16, family='Arial Black'),
            'x': 0.6,
            'xanchor': 'center'
        },
        xaxis={
            'title': '',
            'tickfont': dict(color=COLORS['secondary'], size=11)
        },
        yaxis={
            'title': '',
            'tickfont': dict(color=COLORS['secondary'], size=11)
        }
    )
    
    fig.update_traces(
        hoverlabel=dict(
            bgcolor=COLORS['primary'],
            font_color='white',
            font_size=12
        )
    )
    
    return fig

def create_performance_heatmap_advanced(df, n_players=15, match_filter=None, colorscale_type='stade'):
    """Heatmap avancée avec options"""
    
    # Filtrer par matchs si spécifié
    if match_filter:
        df_filtered = df[df['Match'].isin(match_filter)]
    else:
        df_filtered = df
    
    # Préparer les données
    heatmap_data = df_filtered.groupby(['Nom', 'Match'])['Nb_actions'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Nom', columns='Match', values='Nb_actions').fillna(0)
    
    # Top joueuses
    top_players = df_filtered.groupby('Nom')['Nb_actions'].sum().nlargest(n_players).index
    heatmap_pivot = heatmap_pivot.loc[top_players]
    
    # Choisir la colorscale
    if colorscale_type == 'stade':
        colorscale = COLORSCALE
    elif colorscale_type == 'reversed':
        colorscale = [[0, COLORS['primary']], [1, COLORS['secondary']]]
    else:
        colorscale = COLORSCALE
    
    fig = px.imshow(
        heatmap_pivot,
        aspect='auto',
        title=f"Heatmap personnalisée - {len(heatmap_pivot.index)} joueuses",
        color_continuous_scale=colorscale
    )
    
    # Style
    fig.update_traces(showscale=False)
    
    fig.update_layout(
        **BASE_LAYOUT,
        coloraxis_showscale=False,
        height=500,
        title={
            'font': dict(color=COLORS['secondary'], size=16, family='Arial Black'),
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    
    return fig

def create_performance_comparison_chart(df):
    """Graphique combiné : barres (notes moyennes par action) + ligne (nombre d'actions) + points (meilleures/moins bonnes notes)"""
    
    from analytics.scoring import calculate_player_scoring
    
    # Calculer les données de scoring
    scoring_data = calculate_player_scoring(df)['by_action']
    avg_scores = scoring_data.groupby(['Match', 'Action'])['note_match_joueuse'].mean().reset_index()
    
    # Calculer la plage dynamique : min note globale -10 à max note globale +10
    min_note = scoring_data['note_match_joueuse'].min()
    max_note = scoring_data['note_match_joueuse'].max()
    y_range = [min_note - 10, max_note + 10]
    
    # Créer un graphique avec deux axes Y
    fig = go.Figure()
    
    # Ajouter le graphique en barres sur l'axe Y gauche avec dégradé de couleurs
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
    
    # Ajouter les meilleures notes par match
    best_scores_with_names = scoring_data.loc[scoring_data.groupby(['Match'])['note_match_joueuse'].idxmax()][['Match', 'Prenom', 'Nom', 'note_match_joueuse']].reset_index(drop=True)
    fig.add_trace(
        go.Scatter(
            x=best_scores_with_names['Match'],
            y=best_scores_with_names['note_match_joueuse'],
            name='Meilleure note par match',
            yaxis='y',
            line=dict(width=0),
            marker=dict(color='#2E8B57', size=12),
            mode='markers+text',
            text=best_scores_with_names['Prenom'] + ' ' + best_scores_with_names['Nom'],
            textposition='top center',
            textfont=dict(size=11, color='#2E8B57'),
            hoverinfo='skip'
        )
    )
    
    # Ajouter les moins bonnes notes par match
    worst_scores_with_names = scoring_data.loc[scoring_data.groupby(['Match'])['note_match_joueuse'].idxmin()][['Match', 'Prenom', 'Nom', 'note_match_joueuse']].reset_index(drop=True)
    fig.add_trace(
        go.Scatter(
            x=worst_scores_with_names['Match'],
            y=worst_scores_with_names['note_match_joueuse'],
            name='Moins bonne note par match',
            yaxis='y',
            line=dict(width=0),
            marker=dict(color='#FF8C00', size=12),
            mode='markers+text',
            text=worst_scores_with_names['Prenom'] + ' ' + worst_scores_with_names['Nom'],
            textposition='bottom center',
            textfont=dict(size=11, color='#FF8C00'),
            hoverinfo='skip'
        )
    )
    
    # Configuration des axes
    fig.update_layout(
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
        barmode='group',
        **BASE_LAYOUT
    )
    
    return fig