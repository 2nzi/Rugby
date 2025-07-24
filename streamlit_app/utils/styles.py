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

def create_rugby_title(title):
    """Crée un header titre"""
    
    st.markdown(f'<h1 class="main-header">{title}</h1>', unsafe_allow_html=True)

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