import streamlit as st
import pandas as pd

def show_match_comparison(df):
    """Composant simple pour comparer les matchs"""
    


    st.header("In progress...")
    
    # st.header("⚔️ Comparaison des matchs")
    
    # # Statistiques générales par match
    # match_stats = df.groupby('Match').agg({
    #     'Nb_actions': 'sum',
    #     'Nom': 'nunique'  # Nombre de joueuses différentes
    # }).reset_index()
    
    # match_stats.columns = ['Match', 'Total_actions', 'Nb_joueuses']
    # match_stats['Moyenne_par_joueuse'] = match_stats['Total_actions'] / match_stats['Nb_joueuses']
    # match_stats = match_stats.sort_values('Total_actions', ascending=False)
    
    # st.subheader("📊 Classement des matchs par activité")
    # st.dataframe(match_stats, use_container_width=True)
    
    # # Sélection pour comparaison détaillée
    # st.subheader("🔍 Comparaison détaillée")
    
    # matches = sorted(df['Match'].unique())
    # col1, col2 = st.columns(2)
    
    # with col1:
    #     match1 = st.selectbox("Premier match", matches, key="match1")
    
    # with col2:
    #     match2 = st.selectbox("Second match", matches, key="match2", index=1 if len(matches) > 1 else 0)
    
    # if match1 and match2 and match1 != match2:
    #     col1, col2 = st.columns(2)
        
    #     with col1:
    #         st.markdown(f"**{match1}**")
    #         data1 = df[df['Match'] == match1]
            
    #         total1 = data1['Nb_actions'].sum()
    #         players1 = data1['Nom'].nunique()
            
    #         st.metric("Total actions", total1)
    #         st.metric("Nombre de joueuses", players1)
    #         st.metric("Moyenne par joueuse", f"{total1/players1:.1f}")
        
    #     with col2:
    #         st.markdown(f"**{match2}**")
    #         data2 = df[df['Match'] == match2]
            
    #         total2 = data2['Nb_actions'].sum()
    #         players2 = data2['Nom'].nunique()
            
    #         st.metric("Total actions", total2)
    #         st.metric("Nombre de joueuses", players2)
    #         st.metric("Moyenne par joueuse", f"{total2/players2:.1f}")