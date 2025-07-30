import streamlit as st
import pandas as pd

def show_player_analysis(df):
    """Composant simple pour l'analyse des joueuses"""




    import streamlit as st
    from streamlit_image_carousel import image_carousel

    import base64

    def image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            return f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode()}"


    # Créer un dictionnaire avec les noms uniques des joueurs au bon format
    joueurs_images = [
        {
            "name": f"{row['Prenom']} {row['Nom']}",
            "url": "" # Pas d'image pour le moment
        }
        for _, row in sorted(df[['Nom', 'Prenom']].drop_duplicates().iterrows(), key=lambda x: (x[1]['Nom'], x[1]['Prenom']))
    ]
    
    # Créer un dictionnaire avec les noms uniques des matchs pour le deuxième carousel
    matchs_images = [
        {
            "name": match_name,
            "url": "" # Pas d'image pour le moment
        }
        for match_name in sorted(df['Match'].unique())
    ]



    result = image_carousel(
        images=joueurs_images,
        selected_image=None,
        background_color="#ffffff",
        active_border_color="#000000",
        active_glow_color=f"rgba({0}, {0}, {0}, 0.7)",
        # active_glow_color="#000000",
        fallback_background="#ffffff",
        fallback_gradient_end="#ffffff",
        text_color="#000000",
        arrow_color="#31333f",
    )

    # st.write(result)

    
    # Liste des joueuses
    if result and result.get('selected_image'):
        selected_player = result['selected_image'].split(" ")[1]
    else:
        selected_player = None
    
    colA, colB = st.columns([4, 1])

    with colA:
        # Tableau des données
        if selected_player:
            # Filtrer les données pour la joueuse sélectionnée
            player_data = df[df['Nom'] == selected_player]
                    
            # Statistiques simples
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_actions = player_data['Nb_actions'].sum()
                st.metric("Total actions", f"{total_actions:.0f}")
            
            with col2:
                nb_matchs = player_data['Match'].nunique()
                st.metric("Matchs joués", nb_matchs)
            
            with col3:
                avg_per_match = total_actions / nb_matchs if nb_matchs > 0 else 0
                st.metric("Moyenne par match", f"{avg_per_match:.1f}")
        else:
            st.info("👆 Veuillez sélectionner une joueuse dans le carousel ci-dessus pour voir ses statistiques.")
            return
    with colB:
        result2 = image_carousel(
            images=matchs_images,
            selected_image=None,
            background_color="#ffffff",
            active_border_color="#000000",
            active_glow_color=f"rgba({0}, {0}, {0}, 0.7)",
            # active_glow_color="#000000",
            fallback_background="#ffffff",
            fallback_gradient_end="#ffffff",
            text_color="#000000",
            arrow_color="#31333f",
            orientation="vertical"
        )

        
        # Données détaillées
    with st.expander("Voir toutes les statistiques détaillées"):
        st.dataframe(player_data, use_container_width=True)