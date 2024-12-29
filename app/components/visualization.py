import matplotlib.pyplot as plt
from mplsoccer import PyPizza
import pandas as pd
from config.config import CATEGORIES, CHART_CONFIG

import matplotlib.pyplot as plt
from mplsoccer import PyPizza
import pandas as pd
import streamlit as st
from config.config import CATEGORIES, CHART_CONFIG


def create_pizza_chart(final_df, selected_ville, selected_player, max_values):
    try:
        from urllib.request import urlopen
        from PIL import Image
        import matplotlib.image as image
        
        player_data = final_df[(final_df['Ville'] == selected_ville) & 
                             (final_df['name'] == selected_player)]
        
        if player_data.empty:
            st.warning(f"Aucune donnée trouvée pour {selected_player} dans {selected_ville}")
            return None
            
        player_data = player_data.iloc[0]
        
        params, values, slice_colors = [], [], []
        min_ranges, max_ranges = [], []
        
        # Préparation des données pour le graphique
        for cat_name, cat_info in CATEGORIES.items():
            for subcat, display_text in cat_info['subcats'].items():
                params.append(display_text)
                if subcat in final_df.columns and pd.notna(player_data[subcat]):
                    value = float(player_data[subcat])
                    values.append(value)
                    min_ranges.append(0)
                    max_ranges.append(max_values[cat_name][subcat])
                else:
                    values.append(0)
                    min_ranges.append(0)
                    max_ranges.append(100)
                slice_colors.append(cat_info['color'])

        # Création du graphique
        text_colors = ["#000000"] * len(params)
        fig, ax = plt.subplots(figsize=CHART_CONFIG["figsize"])
        
        pizza_config = {k: v for k, v in CHART_CONFIG.items() if k != "figsize"}
        pizza_config['inner_circle_size'] = 30  # Augmenter la taille du cercle intérieur

        baker = PyPizza(
            params=params,
            min_range=min_ranges,
            max_range=max_ranges,
            **pizza_config
        )

        fig, ax = baker.make_pizza(
            values,
            figsize=(10, 10),
            color_blank_space="same",
            slice_colors=slice_colors,
            value_colors=text_colors,
            value_bck_colors=slice_colors,
            blank_alpha=0.4,
            kwargs_slices=dict(
                edgecolor="#F2F2F2",
                zorder=2,
                linewidth=1
            ),
            kwargs_params=dict(
                color="#000000",
                fontsize=8,
                va="center"
            ),
            kwargs_values=dict(
                color="#000000",
                fontsize=8,
                zorder=3,
                bbox=dict(
                    edgecolor="#000000",
                    facecolor="white",
                    boxstyle="round,pad=0.2",
                    lw=1
                )
            )
        )

        # Ajouter l'image au centre
        try:
            # Charger et ajouter le logo au centre
            logo_url = "https://upload.wikimedia.org/wikipedia/fr/thumb/0/01/Logo_Stade_Toulousain_Rugby.svg/775px-Logo_Stade_Toulousain_Rugby.svg.png?20180529221555"
            logo = Image.open(urlopen(logo_url))
            
            # Créer un nouvel axe pour l'image
            ax_image = fig.add_axes([0.4478, 0.4315, 0.13, 0.127], zorder=2)
            ax_image.imshow(logo)
            ax_image.axis('off')
        except Exception as e:
            st.warning(f"Impossible de charger l'image: {str(e)}")

        return fig
        
    except Exception as e:
        st.error(f"Erreur lors de la création du graphique: {str(e)}")
        return None

def get_max_values_for_ville(final_df, selected_ville):
    """Calcule les valeurs maximales pour une ville donnée"""
    # Filtrer les données pour la ville sélectionnée et exclure "GENERAL"
    ville_data = final_df[(final_df['Ville'] == selected_ville) & 
                         (final_df['name'] != "GENERAL")]
    max_values = {}
    
    for cat_name, cat_info in CATEGORIES.items():
        cat_values = {}  # Utiliser un dictionnaire pour stocker les max par sous-catégorie
        for subcat in cat_info['subcats'].keys():
            if subcat in final_df.columns:
                values = ville_data[subcat].dropna()
                if not values.empty:
                    cat_values[subcat] = max(values.astype(float))
        if cat_values:
            max_values[cat_name] = cat_values
    
    return max_values

def display_metrics(max_values):
    """Affiche les valeurs maximales par catégorie de manière esthétique en deux colonnes"""
    
    st.markdown("""
        <style>
        div[data-testid="stVerticalBlock"] div[style*="flex-direction: column"] div[data-testid="stVerticalBlock"] {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Diviser les catégories en deux groupes
    categories = list(max_values.items())
    mid = (len(categories) + 1) // 2
    
    # Créer deux colonnes principales
    col_left, col_right = st.columns(2)
    
    # Remplir la colonne gauche
    with col_left:
        for cat_name, subcats in categories[:mid]:
            cat_color = CATEGORIES[cat_name]['color']
            with st.container():
                st.markdown(f"""
                    <h3 style='
                        color: {cat_color};
                        font-size: 20px;
                        padding-bottom: 10px;
                        border-bottom: 2px solid {cat_color};
                        margin-bottom: 15px;
                    '>
                        {cat_name}
                    </h3>
                """, unsafe_allow_html=True)
                
                for subcat, value in subcats.items():
                    st.markdown(f"""
                        <div style='display: flex; justify-content: space-between; padding: 5px 0;'>
                            <span style='color: #666; font-size: 16px;'>
                                {CATEGORIES[cat_name]['subcats'][subcat].replace(chr(10), ' ')}
                            </span>
                            <span style='color: #333; font-weight: bold; font-size: 16px;'>
                                {value}
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
    
    # Remplir la colonne droite
    with col_right:
        for cat_name, subcats in categories[mid:]:
            cat_color = CATEGORIES[cat_name]['color']
            with st.container():
                st.markdown(f"""
                    <h3 style='
                        color: {cat_color};
                        font-size: 20px;
                        padding-bottom: 10px;
                        border-bottom: 2px solid {cat_color};
                        margin-bottom: 15px;
                    '>
                        {cat_name}
                    </h3>
                """, unsafe_allow_html=True)
                
                for subcat, value in subcats.items():
                    st.markdown(f"""
                        <div style='display: flex; justify-content: space-between; padding: 5px 0;'>
                            <span style='color: #666; font-size: 16px;'>
                                {CATEGORIES[cat_name]['subcats'][subcat].replace(chr(10), ' ')}
                            </span>
                            <span style='color: #333; font-weight: bold; font-size: 16px;'>
                                {value}
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)