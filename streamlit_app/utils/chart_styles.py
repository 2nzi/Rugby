import plotly.express as px
import plotly.graph_objects as go

# Couleurs du Stade Toulousain
STADE_COLORS = {
    'primary': '#CC0C13',      # Rouge principal
    'secondary': '#000000',    # Noir
    'accent': '#FFFFFF',       # Blanc
    'light_red': 'rgba(204, 12, 19, 0.2)',
    'dark_gray': '#333333'
}

def get_stade_toulousain_colorscale():
    """Palette de couleurs Stade Toulousain"""
    return [[0, STADE_COLORS['secondary']], [1, STADE_COLORS['primary']]]

def get_stade_toulousain_colors():
    """Couleurs discrètes pour graphiques multiples"""
    return [STADE_COLORS['primary'], STADE_COLORS['secondary'], 
            STADE_COLORS['dark_gray'], STADE_COLORS['light_red']]

def apply_stade_style(fig, title=None):
    """Applique le style Stade Toulousain à n'importe quel graphique"""
    
    fig.update_layout(
        # Fond et papier
        plot_bgcolor='rgba(248, 249, 250, 0.5)',
        paper_bgcolor='rgba(0,0,0,0)',
        
        # Police et couleurs
        font=dict(family='Arial', color=STADE_COLORS['secondary'], size=11),
        
        # Titre
        title=dict(
            text=title,
            font=dict(color=STADE_COLORS['primary'], size=16, family='Arial Black'),
            x=0.5,
            xanchor='center'
        ) if title else None,
        
        # Barre de couleur
        coloraxis_colorbar=dict(
            title=dict(text="Intensité", font=dict(color=STADE_COLORS['primary'], size=12)),
            tickfont=dict(color=STADE_COLORS['secondary'], size=10),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor=STADE_COLORS['primary'],
            borderwidth=1
        )
    )
    
    # Axes
    fig.update_xaxes(
        showgrid=True,
        gridcolor=STADE_COLORS['light_red'],
        gridwidth=1,
        zeroline=True,
        zerolinecolor=STADE_COLORS['primary'],
        zerolinewidth=2,
        tickfont=dict(color=STADE_COLORS['secondary'], size=11)
    )
    
    fig.update_yaxes(
        showgrid=False,
        tickfont=dict(color=STADE_COLORS['secondary'], size=11)
    )
    
    # Hover personnalisé
    fig.update_traces(
        hoverlabel=dict(
            bgcolor=STADE_COLORS['primary'],
            font_color='white',
            font_size=12
        )
    )
    
    return fig

def create_custom_bar_chart(data, x, y, title="", orientation='h', remove_y_title=True):
    """Crée un graphique en barres avec le style Stade Toulousain"""
    
    fig = px.bar(
        data,
        x=x,
        y=y,
        orientation=orientation,
        color=x if orientation=='h' else y,
        color_continuous_scale=get_stade_toulousain_colorscale()
    )
    
    # Appliquer le style
    fig = apply_stade_style(fig, title)
    
    # Configuration spécifique pour les barres horizontales
    if orientation == 'h':
        fig.update_layout(
            yaxis={
                'categoryorder': 'total ascending',
                'title': '' if remove_y_title else y
            },
            xaxis={'title': x.replace('_', ' ').title()}
        )
    
    return fig