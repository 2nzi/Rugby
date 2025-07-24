import pandas as pd
import sqlite3
import streamlit as st
from pathlib import Path

@st.cache_data
def load_data():
    """Charge les données depuis le fichier CSV"""
    try:
        data_path = Path(__file__).parent.parent.parent / "data/transformed/Rugby_Stats.csv"
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        st.error(f"Impossible de charger les données : {e}")
        return pd.DataFrame()

@st.cache_data
def load_from_database():
    """Charge les données depuis la base SQLite"""
    try:
        db_path = Path(__file__).parent.parent.parent / "data/transformed/Rugby_Stats.db"
        conn = sqlite3.connect(db_path)
        
        query = '''
        SELECT j.prenom, j.nom, m.nom_match, s.numero, a.nom_action, 
               n.id_niveau, s.nb_actions
        FROM Statistiques s
        JOIN Joueuse j ON s.id_joueuse = j.id_joueuse
        JOIN Match m ON s.id_match = m.id_match
        JOIN Action a ON s.id_action = a.id_action
        JOIN Niveau n ON s.id_niveau = n.id_niveau
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Impossible de charger depuis la base : {e}")
        return pd.DataFrame()

def get_database_stats():
    """Retourne les statistiques générales de la base"""
    try:
        db_path = Path(__file__).parent.parent.parent / "data/transformed/Rugby_Stats.db"
        conn = sqlite3.connect(db_path)
        
        # Nombre de joueuses
        nb_joueuses = pd.read_sql_query("SELECT COUNT(*) as count FROM Joueuse", conn).iloc[0]['count']
        
        # Nombre de matchs
        nb_matchs = pd.read_sql_query("SELECT COUNT(*) as count FROM Match", conn).iloc[0]['count']
        
        # Nombre total de statistiques
        nb_stats = pd.read_sql_query("SELECT COUNT(*) as count FROM Statistiques", conn).iloc[0]['count']
        
        conn.close()
        
        return {
            'nb_joueuses': nb_joueuses,
            'nb_matchs': nb_matchs,
            'nb_stats': nb_stats
        }
    except Exception as e:
        return {'nb_joueuses': 0, 'nb_matchs': 0, 'nb_stats': 0}

def get_player_stats(df, player_name=None):
    """Retourne les statistiques d'une joueuse spécifique"""
    if player_name:
        return df[df['Nom'].str.contains(player_name, case=False, na=False)]
    return df

def get_match_stats(df, match_name=None):
    """Retourne les statistiques d'un match spécifique"""
    if match_name:
        return df[df['Match'] == match_name]
    return df