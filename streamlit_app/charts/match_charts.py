import pandas as pd
import plotly.express as px
from utils.chart_styles import create_custom_bar_chart, apply_stade_style

def create_matches_ranking_chart(df):
    """Classement des matchs par activité"""
    
    match_stats = df.groupby('Match').agg({
        'Nb_actions': 'sum',
        'Nom': 'nunique'
    }).reset_index()
    
    match_stats.columns = ['Match', 'Total_actions', 'Nb_joueuses']
    match_stats['Moyenne_par_joueuse'] = match_stats['Total_actions'] / match_stats['Nb_joueuses']
    
    return create_custom_bar_chart(
        data=match_stats.sort_values('Total_actions', ascending=True),
        x='Total_actions',
        y='Match',
        title="Activité totale par match",
        orientation='h'
    )

def create_match_comparison_chart(df, match1, match2):
    """Comparaison entre deux matchs"""
    
    comparison_data = []
    
    for match in [match1, match2]:
        match_data = df[df['Match'] == match]
        stats = {
            'Match': match,
            'Total_actions': match_data['Nb_actions'].sum(),
            'Nb_joueuses': match_data['Nom'].nunique(),
            'Actions_DUEL': match_data[match_data['Action'] == 'DUEL']['Nb_actions'].sum(),
            'Actions_PLAQUAGE': match_data[match_data['Action'] == 'PLAQUAGE']['Nb_actions'].sum(),
            'Actions_RUCK': match_data[match_data['Action'] == 'RUCK']['Nb_actions'].sum()
        }
        comparison_data.append(stats)
    
    df_comparison = pd.DataFrame(comparison_data)
    
    # Graphique en barres groupées
    fig = px.bar(
        df_comparison.melt(id_vars=['Match'], var_name='Métrique', value_name='Valeur'),
        x='Métrique',
        y='Valeur',
        color='Match',
        barmode='group',
        title=f"Comparaison {match1} vs {match2}",
        color_discrete_sequence=['#CC0C13', '#000000']
    )
    
    return apply_stade_style(fig)