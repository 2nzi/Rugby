import pandas as pd
import plotly.express as px
from .config import COLORS, COLORSCALE, BASE_LAYOUT

def create_matches_activity_chart(df):
    """Graphique d'activité par match"""
    
    match_stats = df.groupby('Match').agg({
        'Nb_actions': 'sum',
        'Nom': 'nunique'
    }).reset_index()
    
    match_stats.columns = ['Match', 'Total_actions', 'Nb_joueuses']
    match_stats = match_stats.sort_values('Total_actions', ascending=True)
    
    fig = px.bar(
        match_stats,
        x='Total_actions',
        y='Match',
        orientation='h',
        title="Activité totale par match",
        color='Total_actions',
        color_continuous_scale=COLORSCALE
    )
    
    fig.update_layout(
        **BASE_LAYOUT,
        height=500,
        coloraxis_showscale=False,
        yaxis={
            'categoryorder': 'total ascending',
            'title': '',
            'tickfont': dict(color=COLORS['secondary'], size=11)
        },
        xaxis={
            'title': 'Nombre total d\'actions',
            'tickfont': dict(color=COLORS['secondary'], size=11)
        },
        title={
            'font': dict(color=COLORS['secondary'], size=16, family='Arial Black'),
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    
    return fig

def create_actions_distribution_chart(df):
    """Distribution des types d'actions avec dégradé basé sur l'importance"""
    
    action_stats = df.groupby('Action')['Nb_actions'].sum().reset_index()
    
    # Calculer le pourcentage pour chaque action
    total_actions = action_stats['Nb_actions'].sum()
    action_stats['Pourcentage'] = (action_stats['Nb_actions'] / total_actions) * 100
    
    # Trier par importance (pourcentage décroissant)
    action_stats = action_stats.sort_values('Pourcentage', ascending=False)
    
    # Créer un dégradé de couleurs basé sur l'importance
    n_actions = len(action_stats)
    colors = []
    for i in range(n_actions):
        # Dégradé de noir (moins important) à rouge (plus important)
        ratio = i / (n_actions - 1) if n_actions > 1 else 0
        color = f"rgba({204 * ratio + 0 * (1-ratio):.0f}, {12 * ratio + 0 * (1-ratio):.0f}, {19 * ratio + 0 * (1-ratio):.0f}, 1)"
        colors.append(color)
    
    fig = px.pie(
        action_stats,
        values='Nb_actions',
        names='Action',
        title="Répartition des types d'actions",
        color_discrete_sequence=colors
    )
    
    fig.update_layout(
        **BASE_LAYOUT,
        title={
            'font': dict(color=COLORS['secondary'], size=16, family='Arial Black'),
            'x': 0.4,
            'xanchor': 'center'
        }
    )
    
    # Ajouter des bordures blanches entre chaque part
    fig.update_traces(
        marker=dict(line=dict(color='white', width=2))
    )
    
    return fig

def create_matches_ranking_chart(df):
    """Même fonction que create_matches_activity_chart pour compatibilité"""
    return create_matches_activity_chart(df)

def create_match_comparison_chart(df, match1, match2):
    """Comparaison entre deux matchs - simple"""
    
    comparison_data = []
    
    for match in [match1, match2]:
        match_data = df[df['Match'] == match]
        stats = {
            'Match': match,
            'Total_actions': match_data['Nb_actions'].sum(),
            'Nb_joueuses': match_data['Nom'].nunique()
        }
        comparison_data.append(stats)
    
    df_comparison = pd.DataFrame(comparison_data)
    
    fig = px.bar(
        df_comparison,
        x='Match',
        y='Total_actions',
        title=f"Comparaison {match1} vs {match2}",
        color='Match',
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary']]
    )
    
    fig.update_layout(**BASE_LAYOUT)
    
    return fig