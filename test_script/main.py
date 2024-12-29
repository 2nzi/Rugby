import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import PyPizza, add_image

# Définir les catégories et leurs sous-catégories avec descriptions
categories = {
    'Duel': {
        'color': "#1A78CF",
        'subcats': {
            'Duel_0': 'Duel\nPerdu',
            'Duel_1': 'Duel\nGagné',
            'Duel_2': 'Duel\nNeutre',
            'Duel_3': 'Duel\nDécisif',
            'Duel_M': 'Duel\nMoyenne'
        }
    },
    'Passe': {
        'color': "#FF9300",
        'subcats': {
            'Passe_0': 'Passe\nRatée',
            'Passe_1': 'Passe\nSimple',
            'Passe_2': 'Passe\nBonne',
            'Passe_3': 'Passe\nDécisive',
            'Passe_M': 'Passe\nMoyenne'
        }
    },
    'Plaquage': {
        'color': "#D70232",
        'subcats': {
            'Plaquage_0': 'Plaquage\nRaté',
            'Plaquage_1': 'Plaquage\nSimple',
            'Plaquage_2': 'Plaquage\nOffensif',
            'Plaquage_3': 'Plaquage\nDécisif',
            'Plaquage_M': 'Plaquage\nMoyenne'
        }
    },
    'Ruck': {
        'color': "#2ECC71",
        'subcats': {
            'Ruck_0': 'Ruck\nPerdu',
            'Ruck_1': 'Ruck\nGagné',
            'Ruck_2': 'Ruck\nDominant',
            'Ruck_3': 'Ruck\nDécisif',
            'Ruck_M': 'Ruck\nMoyenne'
        }
    },
    'JAP': {
        'color': "#9B59B6",
        'subcats': {
            'JAP_0': 'JAP\nRaté',
            'JAP_1': 'JAP\nSimple',
            'JAP_2': 'JAP\nBon',
            'JAP_3': 'JAP\nDécisif',
            'JAP_M': 'JAP\nMoyenne'
        }
    },
    'Reception JAP': {
        'color': "#F1C40F",
        'subcats': {
            'Reception_JAP_0': 'Récep\nRatée',
            'Reception_JAP_1': 'Récep\nSimple',
            'Reception_JAP_2': 'Récep\nBonne',
            'Reception_JAP_3': 'Récep\nDécisive',
            'Reception_JAP_M': 'Récep\nMoyenne'
        }
    }
}

# 1. Lire toutes les feuilles dans un dictionnaire
all_sheets = pd.read_excel("stats.xlsx", sheet_name=None)

def clean_dataframe(df):
    # Récupérer les catégories principales (ligne 0)
    categories = df.iloc[0]
    # Récupérer les sous-catégories (ligne 2)
    sub_categories = df.iloc[2]
    
    # Créer un dictionnaire pour stocker les nouvelles colonnes
    new_columns = {}
    current_category = None
    
    # Parcourir toutes les colonnes pour créer les nouveaux noms
    for i, (cat, subcat) in enumerate(zip(categories, sub_categories)):
        if pd.notna(cat):
            current_category = cat
        if pd.notna(subcat) and current_category is not None:
            new_name = f"{current_category}_{subcat}"
            new_columns[df.columns[i]] = new_name
    
    # Garder la colonne 'name' telle quelle
    new_columns[df.columns[0]] = 'name'
    
    # Renommer les colonnes
    df = df.rename(columns=new_columns)
    
    # Supprimer les trois premières lignes et réinitialiser l'index
    df = df.iloc[3:].reset_index(drop=True)
    
    # Ne garder que les colonnes renommées
    columns_to_keep = ['name'] + [col for col in df.columns if '_' in str(col)]
    df = df[columns_to_keep]
    
    return df

# Liste pour stocker les données nettoyées
clean_data = []

for ville, df in all_sheets.items():
    if ville != "Promedio partidos":
        # Nettoyer le DataFrame
        clean_df = clean_dataframe(df)
        
        # Filtrer pour Onillon
        onillon_data = clean_df[clean_df['name'].str.contains('onillon', case=False, na=False)]
        
        if not onillon_data.empty:
            # Ajouter la ville
            onillon_data['Ville'] = ville
            clean_data.append(onillon_data)

# Combiner tous les DataFrames
if clean_data:
    final_df = pd.concat(clean_data, ignore_index=True)

    # Initialiser les listes
    params = []
    values = []
    slice_colors = []

    # Extraire les données pour une ville spécifique
    ville_data = final_df.iloc[0]

    # Trouver la valeur maximale pour chaque catégorie
    max_values = {}
    for cat_name, cat_info in categories.items():
        cat_values = []
        for subcat in cat_info['subcats'].keys():
            if subcat in final_df.columns and pd.notna(ville_data[subcat]):
                cat_values.append(float(ville_data[subcat]))
        if cat_values:
            max_values[cat_name] = max(cat_values)

    # Remplir les listes avec TOUTES les sous-catégories
    for cat_name, cat_info in categories.items():
        for subcat, display_text in cat_info['subcats'].items():
            params.append(display_text)
            if subcat in final_df.columns and pd.notna(ville_data[subcat]):
                # Normaliser par rapport au maximum de la catégorie
                value = float(ville_data[subcat])
                max_val = max_values[cat_name]
                normalized_value = (value / max_val * 100) if max_val > 0 else 0
                values.append(round(normalized_value, 2))
            else:
                values.append(0)
            slice_colors.append(cat_info['color'])

    # Créer le graphique
    if len(params) > 0:
        text_colors = ["#000000"] * len(params)

        baker = PyPizza(
            params=params,                  
            background_color="#EBEBE9",     
            straight_line_color="#EBEBE9",  
            straight_line_lw=1,             
            last_circle_lw=0,              
            other_circle_lw=0,              
            inner_circle_size=20,
            straight_line_limit=100
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
                edgecolor="#F2F2F2", zorder=2, linewidth=1
            ),                               
            kwargs_params=dict(
                color="#000000", fontsize=8,  
                va="center"
            ),                               
            kwargs_values=dict(
                color="#000000", fontsize=8,  
                zorder=3,
                bbox=dict(
                    edgecolor="#000000", facecolor="white",
                    boxstyle="round,pad=0.2", lw=1
                )
            )                                
        )

        ville = final_df['Ville'].iloc[0]
        fig.text(
            0.515, 0.975, f"Statistiques détaillées de M. Onillon - {ville}", size=16,
            ha="center", color="#000000"
        )

        # Ajouter une note sur l'échelle
        max_values_text = "\n".join([f"{cat}: max={val:.2f}" for cat, val in max_values.items()])
        fig.text(
            0.95, 0.02, 
            f"Valeurs maximales par catégorie:\n{max_values_text}", 
            size=8, ha="right", color="#000000"
        )

        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                    label=cat_name,
                                    markerfacecolor=cat_info['color'], markersize=10)
                          for cat_name, cat_info in categories.items()]
        ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))

        plt.show()
    else:
        print("Aucune donnée disponible pour le graphique")
else:
    print("Aucune donnée trouvée pour Onillon")