import pandas as pd
import streamlit as st
from config.config import EXCEL_PATH


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
    
    # Supprimer les lignes où le nom est vide ou NaN
    df = df.dropna(subset=['name']).reset_index(drop=True)
    
    # Extraire le numéro et nettoyer le nom AVANT d'ajouter la colonne Ville
    df['numero'] = df['name'].str.extract(r'^(\d+)').fillna('')
    df['name'] = df['name'].str.replace(r'^\d+\s*-\s*', '', regex=True).str.strip()
    
    # Ne garder que les colonnes nécessaires
    columns_to_keep = ['numero', 'name'] + [col for col in df.columns if '_' in str(col)]
    df = df[columns_to_keep]
    
    return df

@st.cache_data
def load_data():
    """Charge et prépare les données depuis le fichier Excel"""
    try:
        if not EXCEL_PATH.exists():
            st.error(f"Le fichier Excel n'a pas été trouvé à l'emplacement : {EXCEL_PATH}")
            st.info("Veuillez placer votre fichier stats.xlsx dans le dossier 'data'")
            return None
            
        all_sheets = pd.read_excel(EXCEL_PATH, sheet_name=None)
        clean_data = []
        
        for ville, df in all_sheets.items():
            if ville != "Promedio partidos":
                clean_df = clean_dataframe(df)
                if not clean_df.empty:
                    clean_df['Ville'] = ville
                    clean_data.append(clean_df)
        
        # st.write(clean_data)

        if not clean_data:
            st.warning("Aucune donnée trouvée")
            return None
            
        return pd.concat(clean_data, ignore_index=True)
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {str(e)}")
        return None
    
    