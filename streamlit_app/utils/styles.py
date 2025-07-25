import streamlit as st
from pathlib import Path

def load_css():
    """Charge le fichier CSS personnalisé"""
    css_file = Path(__file__).parent.parent / "assets" / "style.css"
    
    try:
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        st.markdown(f"""
        <style>
        {css_content}
        </style>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.warning("Fichier CSS non trouvé. Styles par défaut utilisés.")
    except Exception as e:
        st.error(f"Erreur lors du chargement du CSS : {e}")

def load_logo():
    """Charge le logo du Stade Toulousain"""
    logo_path = Path(__file__).parent.parent / "assets" / "Logo_Stade_Toulousain_Rugby.png"
    
    if logo_path.exists():
        return str(logo_path)
    return None

def create_rugby_title(left_text="u18 féminine", right_text="Stade Toulousain"):
    """Crée un header titre avec logo centré"""
    
    # Charger le logo
    logo_path = load_logo()
    
    if logo_path:
        # Convertir le logo en base64 pour l'affichage
        logo_base64 = get_base64_of_image(logo_path)
        
        st.markdown(f"""
        <div class="rugby-header-custom">
            <span class="title-left">{left_text}</span>
            <img src="data:image/png;base64,{logo_base64}" class="logo-center" alt="Logo Stade Toulousain"/>
            <span class="title-right">{right_text}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback si le logo n'est pas trouvé
        st.markdown(f'<h1 class="main-header">{left_text} - {right_text}</h1>', unsafe_allow_html=True)

def get_base64_of_image(path):
    """Convertit une image en base64 pour l'affichage"""
    import base64
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def create_metric_card(title, value, description=""):
    """Crée une carte métrique personnalisée"""
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin: 0; color: #1f4e79;">{title}</h3>
        <h2 style="margin: 0.5rem 0; color: #1f4e79; font-size: 2rem;">{value}</h2>
        <p style="margin: 0; color: #666; font-size: 0.9rem;">{description}</p>
    </div>
    """, unsafe_allow_html=True) 