import pandas as pd
import streamlit as st

@st.cache_data
def calculate_player_scoring(df):
    """
    Calcule tous les niveaux de scoring des joueuses de rugby
    
    Args:
        df: DataFrame avec les données brutes
        
    Returns:
        dict: Contient tous les niveaux d'agrégation
            - 'by_action': Scores détaillés par (match, joueuse, action)
            - 'by_player_match': Scores par (match, joueuse) 
            - 'by_match': Scores moyens par match
            - 'global_average': Moyenne générale
    """
    
    # Configuration
    actions_interessees = [
        "DUEL",
        "PASSE",
        "PLAQUAGE", 
        "RUCK",
        "JAP",
        "RECEPTION JAP"
    ]
    
    facteur_pond = 100/3
    
    # 1. Calcul du score pondéré par (match, joueuse, action)
    df_grouped = df.groupby(
        ["Match", "Prenom", "Nom", "Action"]
    ).apply(
        lambda g: pd.Series({
            "score_pondere": (g["Niveau"] * g["Nb_actions"]).sum() / g["Nb_actions"].sum(),
            "nb_total_actions": g["Nb_actions"].sum()
        })
    ).reset_index()

    # Filtrage sur les actions intéressées 
    score_actions = df_grouped[df_grouped["Action"].str.upper().isin(actions_interessees)]

    # 2. Calcul de la note moyenne par (match, joueuse)
    score_actions["note_match_joueuse"] = score_actions.groupby(
        ["Match", "Prenom", "Nom"]
    )["score_pondere"].transform("mean") * facteur_pond

    score_match_joueuse = score_actions.drop_duplicates(
        subset=["Match", "Prenom", "Nom"]
    )[["Match", "Prenom", "Nom", "note_match_joueuse"]]

    # 3. Calcul de la note moyenne par match
    score_match = score_match_joueuse.groupby(["Match"]).apply(
        lambda g: pd.Series({
            "note_match_joueuse": g["note_match_joueuse"].mean()
        })
    ).reset_index()
    
    # 4. Métrique globale
    global_average = round(score_match["note_match_joueuse"].mean(), 2)

    return {
        'by_action': score_actions,
        'by_player_match': score_match_joueuse,
        'by_match': score_match, 
        'global_average': global_average
    }

@st.cache_data
def get_global_score(df):
    """
    Retourne uniquement la métrique globale (pour usage immédiat)
    """
    scoring_data = calculate_player_scoring(df)
    return scoring_data['global_average']

@st.cache_data  
def get_top_players(df, n_players=10):
    """
    Retourne le top N des joueuses par note moyenne
    """
    scoring_data = calculate_player_scoring(df)
    
    top_players = scoring_data['by_player_match'].groupby(['Prenom', 'Nom']).agg({
        'note_match_joueuse': 'mean'
    }).reset_index().sort_values('note_match_joueuse', ascending=False).head(n_players)
    
    return top_players

@st.cache_data
def get_match_scores(df):
    """
    Retourne les scores par match (pour charts futurs)
    """
    scoring_data = calculate_player_scoring(df)
    return scoring_data['by_match']

@st.cache_data  
def get_player_match_scores(df):
    """
    Retourne les scores par joueuse-match (pour charts futurs)
    """
    scoring_data = calculate_player_scoring(df)
    return scoring_data['by_player_match'] 