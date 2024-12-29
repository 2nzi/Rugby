

def create_pizza_chart(final_df, selected_ville):
    """Crée le graphique pizza pour une ville donnée"""
    ville_data = final_df[final_df['Ville'] == selected_ville].iloc[0]
    
    params, values, slice_colors = [], [], []
    max_values = {}
    
    # Calcul des valeurs maximales
    for cat_name, cat_info in CATEGORIES.items():
        cat_values = []
        for subcat in cat_info['subcats'].keys():
            if subcat in final_df.columns and pd.notna(ville_data[subcat]):
                cat_values.append(float(ville_data[subcat]))
        if cat_values:
            max_values[cat_name] = max(cat_values)

    # Préparation des données pour le graphique
    for cat_name, cat_info in CATEGORIES.items():
        for subcat, display_text in cat_info['subcats'].items():
            params.append(display_text)
            if subcat in final_df.columns and pd.notna(ville_data[subcat]):
                value = float(ville_data[subcat])
                max_val = max_values[cat_name]
                normalized_value = (value / max_val * 100) if max_val > 0 else 0
                values.append(round(normalized_value, 2))
            else:
                values.append(0)
            slice_colors.append(cat_info['color'])

    # Création du graphique
    text_colors = ["#000000"] * len(params)
    fig, ax = plt.subplots(figsize=CHART_CONFIG["figsize"])
    
    # Créer un dictionnaire de configuration sans figsize pour PyPizza
    pizza_config = {k: v for k, v in CHART_CONFIG.items() if k != "figsize"}
    
    baker = PyPizza(
        params=params,
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

    return fig, max_values