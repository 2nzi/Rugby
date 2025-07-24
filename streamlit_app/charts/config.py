"""Configuration et constantes pour les graphiques"""

# Couleurs Stade Toulousain
COLORS = {
    'primary': '#CC0C13',      # Rouge principal
    'secondary': '#000000',    # Noir
    'white': '#FFFFFF',        # Blanc
    'light_red': 'rgba(204, 12, 19, 0.2)',
    'gray': '#666666'
}

# Palette pour dégradés
COLORSCALE = [[0, COLORS['secondary']], [1, COLORS['primary']]]

# Couleurs discrètes
DISCRETE_COLORS = [COLORS['primary'], COLORS['secondary'], COLORS['gray']]

# Style de base réutilisable
BASE_LAYOUT = {
    'plot_bgcolor': 'rgba(248, 249, 250, 0.5)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'font': dict(family='Arial', color=COLORS['secondary'], size=11)
} 