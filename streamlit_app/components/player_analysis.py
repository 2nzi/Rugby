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

    # Exemple d'images de joueurs (plus d'images pour tester le carrousel)
    joueurs_images = [
        {
            "name": "Dupont",
            "url": image_to_base64(r"C:\Users\antoi\Documents\Work_Learn\Rugby\data\player_images\AD.jpg")
        },
        {
            "name": "Cristiano Ronaldo",
            "url": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg"
        },
        {
            "name": "Kylian Mbappé",
            "url": "https://upload.wikimedia.org/wikipedia/commons/5/57/Kylian_Mbapp%C3%A9_2019.jpg"
        },
        {
            "name": "Erling Haaland",
            "url": "https://upload.wikimedia.org/wikipedia/commons/0/07/Erling_Haaland_2023.jpg"
        },
        {
            "name": "Neymar Jr",
            "url": "https://upload.wikimedia.org/wikipedia/commons/6/6b/Neymar_Jr_2019.jpg"
        },
        {
            "name": "Kevin De Bruyne",
            "url": "https://upload.wikimedia.org/wikipedia/commons/7/7d/Kevin_De_Bruyne_2019.jpg"
        },
        {
            "name": "Mohamed Salah",
            "url": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Mohamed_Salah_2018.jpg"
        },
        {
            "name": "Robert Lewandowski",
            "url": "https://upload.wikimedia.org/wikipedia/commons/8/82/Robert_Lewandowski_2018.jpg"
        },
        {
            "name": "Karim Benzema",
            "url": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Karim_Benzema_2018.jpg"
        },
        {
            "name": "Harry Kane",
            "url": "https://upload.wikimedia.org/wikipedia/commons/3/3c/2018-07-07_Sweden_v_England_FIFA_World_Cup_2018_%28cropped%29.jpg"
        },
        {
            "name": "Vinícius Jr",
            "url": "https://upload.wikimedia.org/wikipedia/commons/7/76/Vin%C3%ADcius_J%C3%BAnior_2023.jpg"
        },
        {
            "name": "Jude Bellingham",
            "url": "https://upload.wikimedia.org/wikipedia/commons/7/7a/Jude_Bellingham_2023.jpg"
        }
    ]

    # Créer un dictionnaire avec les noms uniques des joueurs au bon format
    joueurs_images = [
        {
            "name": f"{row['Prenom']} {row['Nom']}",
            # "url": image_to_base64(r"C:\Users\antoi\Documents\Work_Learn\Rugby\data\player_images\MT.jpg")  # Image par défaut
            "url": "" # Image par défaut
        }
        for _, row in sorted(df[['Nom', 'Prenom']].drop_duplicates().iterrows(), key=lambda x: (x[1]['Nom'], x[1]['Prenom']))
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
    selected_player = result['selected_image'].split(" ")[1]
    
    if selected_player:
        # Filtrer les données pour la joueuse sélectionnée
        player_data = df[df['Nom'] == selected_player]
        
        # Nom complet
        player_name = f"{player_data.iloc[0]['Prenom']} {player_data.iloc[0]['Nom']}"
        st.subheader(f"Statistiques de {player_name}")
        
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
        
        # Tableau des données
        st.subheader("📊 Détail des actions")
        
        # Résumé par action
        summary = player_data.groupby('Action')['Nb_actions'].sum().reset_index()
        summary = summary.sort_values('Nb_actions', ascending=False)
        
        st.dataframe(summary, use_container_width=True)
        
        # Données détaillées
        with st.expander("Voir toutes les statistiques détaillées"):
            st.dataframe(player_data, use_container_width=True)