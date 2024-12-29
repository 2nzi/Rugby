import streamlit as st
from utils.data_processing import load_data
from components.layout import create_sidebar, create_main_layout
from components.visualization import create_pizza_chart, display_metrics, get_max_values_for_ville
import pandas as pd

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Statistiques Rugby",
    page_icon="🏉",
    layout="wide"
)

def main():
    """Fonction principale de l'application"""
    st.title("🏉 Analyse des Statistiques Rugby")
    
    # Chargement des données
    data = load_data()
    # Conversion des colonnes numériques
    numeric_columns = data.select_dtypes(include=['object']).columns
    for col in numeric_columns:
        if col != 'name' and col != 'Ville':
            data[col] = pd.to_numeric(data[col], errors='coerce')
    
    # Création de l'interface
    selected_ville, selected_player = create_sidebar(data)
    col1, col2 = create_main_layout(data, selected_ville)
    
    with col1:
        st.subheader(f"Statistiques pour {selected_player} ({selected_ville})")
        # Récupérer uniquement les valeurs maximales
        max_values = get_max_values_for_ville(data, selected_ville)
        fig = create_pizza_chart(data, selected_ville, selected_player, max_values)
        if fig is not None:
            st.pyplot(fig)
    
    with col2:
        st.subheader("Valeurs maximales pour ce match")
        if max_values:
            display_metrics(max_values)
        else:
            st.warning("Aucune donnée maximale disponible")

if __name__ == "__main__":
    main()