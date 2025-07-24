"""Configuration et constantes pour les graphiques"""

# Couleurs Stade Toulousain
COLORS = {
    'primary': '#CC0C13',      # Rouge principal
    'secondary': '#000000',    # Noir
    'white': '#FFFFFF',        # Blanc
    'light_red': 'rgba(204, 12, 19, 0.2)',
    'gray': '#666666'
}

# Palette pour dégradés STANDARD (noir -> rouge)
COLORSCALE = [[0, COLORS['secondary']], [1, COLORS['primary']]]

# Palette pour dégradés HEATMAP (blanc -> rouge)
COLORSCALE_HEATMAP = [[0, COLORS['white']], [1, COLORS['primary']]]

# Palette inversée (rouge -> blanc) pour certains cas
COLORSCALE_REVERSED = [[0, COLORS['primary']], [1, COLORS['white']]]

# Couleurs discrètes
DISCRETE_COLORS = [COLORS['primary'], COLORS['secondary'], COLORS['white'], COLORS['gray']]

# Style de base réutilisable
BASE_LAYOUT = {
    'plot_bgcolor': 'rgba(248, 249, 250, 0.5)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'font': dict(family='Arial', color=COLORS['secondary'], size=11)
}

def remove_colorscale_legend(fig):
    """Fonction utilitaire pour enlever la colorscale de n'importe quel graphique"""
    fig.update_traces(showscale=False)
    return fig

def apply_stade_style(fig, title=None, remove_colorbar=True):
    """Applique le style Stade Toulousain avec option pour enlever la colorbar"""
    
    if remove_colorbar:
        fig.update_traces(showscale=False)
    
    fig.update_layout(
        **BASE_LAYOUT,
        title={
            'text': title,
            'font': dict(color=COLORS['primary'], size=16, family='Arial Black'),
            'x': 0.5,
            'xanchor': 'center'
        } if title else None
    )
    
    return fig 