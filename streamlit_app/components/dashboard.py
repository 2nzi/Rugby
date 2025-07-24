import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show_dashboard(df):
    """Affiche le tableau de bord principal"""
    
    st.header("🏠 Tableau de bord général")
    
    # Métriques générales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_actions = df['Nb_actions'].sum()
        st.metric("Total actions", f"{total_actions:,.0f}")
    
    with col2:
        nb_joueuses = df['Nom'].nunique()
        st.metric("Joueuses actives", nb_joueuses)
    
    with col3:
        nb_matchs = df['Match'].nunique()
        st.metric("Matchs analysés", nb_matchs)
    
    with col4:
        avg_actions = df.groupby(['Prenom', 'Nom'])['Nb_actions'].sum().mean()
        st.metric("Moy. actions/joueuse", f"{avg_actions:.0f}")
    
    st.divider()
    
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 10 des joueuses")
        top_players = df.groupby(['Prenom', 'Nom'])['Nb_actions'].sum().reset_index()
        top_players['Nom_complet'] = top_players['Prenom'] + ' ' + top_players['Nom']
        top_players = top_players.nlargest(10, 'Nb_actions')
        
        fig = px.bar(
            top_players, 
            x='Nb_actions', 
            y='Nom_complet',
            orientation='h',
            title="Nombre total d'actions par joueuse",
            color='Nb_actions',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚽ Répartition des actions")
        action_stats = df.groupby('Action')['Nb_actions'].sum().reset_index()
        
        fig = px.pie(
            action_stats, 
            values='Nb_actions', 
            names='Action',
            title="Distribution des types d'actions"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Analyse par niveau de performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Performance par niveau")
        niveau_stats = df.groupby('Niveau')['Nb_actions'].sum().reset_index()
        niveau_stats['Niveau_label'] = niveau_stats['Niveau'].map({
            0: 'Niveau 0 (Basique)',
            1: 'Niveau 1 (Correct)', 
            2: 'Niveau 2 (Bon)',
            3: 'Niveau 3 (Excellent)'
        })
        
        fig = px.bar(
            niveau_stats,
            x='Niveau_label',
            y='Nb_actions',
            title="Nombre d'actions par niveau de qualité",
            color='Niveau',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏉 Performance par match")
        match_stats = df.groupby('Match')['Nb_actions'].sum().reset_index()
        match_stats = match_stats.sort_values('Nb_actions', ascending=True)
        
        fig = px.bar(
            match_stats,
            x='Nb_actions',
            y='Match',
            orientation='h',
            title="Total d'actions par match",
            color='Nb_actions',
            color_continuous_scale='Oranges'
        )
        fig.update_layout(height=500, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap des performances
    st.subheader("🔥 Carte de chaleur : Actions par joueuse et match")
    
    # Préparer les données pour la heatmap
    heatmap_data = df.groupby(['Nom', 'Match'])['Nb_actions'].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Nom', columns='Match', values='Nb_actions').fillna(0)
    
    # Limiter aux 15 meilleures joueuses pour la lisibilité
    top_15_players = df.groupby('Nom')['Nb_actions'].sum().nlargest(15).index
    heatmap_pivot = heatmap_pivot.loc[top_15_players]
    
    fig = px.imshow(
        heatmap_pivot,
        aspect='auto',
        title="Intensité d'activité par joueuse et match",
        color_continuous_scale='Blues'
    )
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)