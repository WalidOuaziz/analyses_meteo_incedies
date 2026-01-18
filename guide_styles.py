"""
🎨 Guide des Styles de l'Application
====================================

Ce fichier montre comment utiliser les styles personnalisés dans vos pages Streamlit.
"""

import streamlit as st
from utils.styles import get_page_style

# ========================================
# 1. APPLIQUER LE STYLE GLOBAL
# ========================================

st.set_page_config(page_title="Guide des Styles", page_icon="🎨", layout="wide")
st.markdown(get_page_style(), unsafe_allow_html=True)

# ========================================
# 2. UTILISER LES CARTES
# ========================================

st.title("🎨 Guide des Styles")

st.markdown("""
<div class="card">
    <h3>Carte Standard</h3>
    <p>Utilisez la classe <code>card</code> pour une carte de base.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card card-success">
    <h3>✅ Carte de Succès</h3>
    <p>Utilisez <code>card card-success</code> pour les réussites.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card card-warning">
    <h3>⚠️ Carte d'Avertissement</h3>
    <p>Utilisez <code>card card-warning</code> pour les avertissements.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card card-danger">
    <h3>❌ Carte de Danger</h3>
    <p>Utilisez <code>card card-danger</code> pour les erreurs.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card card-info">
    <h3>ℹ️ Carte d'Information</h3>
    <p>Utilisez <code>card card-info</code> pour les informations.</p>
</div>
""", unsafe_allow_html=True)

# ========================================
# 3. UTILISER LES BADGES
# ========================================

st.markdown("---")
st.subheader("Badges")

st.markdown("""
<span class="badge badge-primary">Badge Primaire</span>
<span class="badge badge-success">Badge Succès</span>
<span class="badge badge-warning">Badge Avertissement</span>
<span class="badge badge-danger">Badge Danger</span>
""", unsafe_allow_html=True)

# ========================================
# 4. UTILISER LES STAT BOXES
# ========================================

st.markdown("---")
st.subheader("Boîtes de Statistiques")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-label">Total d'Incendies</div>
        <div class="stat-number">118,605</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-label">Stations Météo</div>
        <div class="stat-number">1,202</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-label">Années de Données</div>
        <div class="stat-number">67</div>
    </div>
    """, unsafe_allow_html=True)

# ========================================
# 5. UTILISER LA FEATURE BOX
# ========================================

st.markdown("---")
st.subheader("Boîte de Fonctionnalité")

st.markdown("""
<div class="feature-box">
    <h3>✨ Fonctionnalité Premium</h3>
    <p>Cette boîte met en évidence les fonctionnalités importantes avec un dégradé attrayant.</p>
</div>
""", unsafe_allow_html=True)

# ========================================
# 6. EXEMPLES D'UTILISATION
# ========================================

st.markdown("---")
st.subheader("📝 Exemples de Code")

st.code("""
# Exemple 1: Carte simple
st.markdown('''
<div class="card">
    <h3>Titre de la Carte</h3>
    <p>Contenu de la carte...</p>
</div>
''', unsafe_allow_html=True)

# Exemple 2: Badges
st.markdown('''
<span class="badge badge-primary">Nouveau</span>
<span class="badge badge-success">Actif</span>
''', unsafe_allow_html=True)

# Exemple 3: Stat Box
st.markdown('''
<div class="stat-box">
    <div class="stat-label">Label</div>
    <div class="stat-number">1,234</div>
</div>
''', unsafe_allow_html=True)
""", language="python")

# ========================================
# 7. PALETTE DE COULEURS
# ========================================

st.markdown("---")
st.subheader("🎨 Palette de Couleurs")

colors = {
    "Primaire": "#3b82f6",
    "Succès": "#10b981",
    "Avertissement": "#f59e0b",
    "Danger": "#ef4444",
    "Info": "#06b6d4",
    "Fond": "#f5f7fa",
    "Texte": "#1e293b"
}

col1, col2 = st.columns(2)

with col1:
    for name, color in list(colors.items())[:4]:
        st.markdown(f"""
        <div style="background: {color}; padding: 1rem; border-radius: 8px; color: white; margin: 0.5rem 0;">
            <strong>{name}</strong><br>{color}
        </div>
        """, unsafe_allow_html=True)

with col2:
    for name, color in list(colors.items())[4:]:
        bg_color = color if name != "Fond" else color
        text_color = "white" if name != "Fond" else "#1e293b"
        st.markdown(f"""
        <div style="background: {bg_color}; padding: 1rem; border-radius: 8px; color: {text_color}; margin: 0.5rem 0;">
            <strong>{name}</strong><br>{color}
        </div>
        """, unsafe_allow_html=True)

# ========================================
# 8. COMPOSANTS STREAMLIT NATIFS
# ========================================

st.markdown("---")
st.subheader("📊 Composants Streamlit Stylisés")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Température", "24°C", "+2°C")

with col2:
    st.metric("Précipitations", "45 mm", "-5 mm")

with col3:
    st.metric("Vent", "15 km/h", "+3 km/h")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 Graphiques", "📋 Données", "⚙️ Paramètres"])

with tab1:
    st.write("Contenu du tab Graphiques")

with tab2:
    st.write("Contenu du tab Données")

with tab3:
    st.write("Contenu du tab Paramètres")

st.markdown("---")
st.info("💡 **Astuce**: Tous ces styles sont automatiquement appliqués lorsque vous importez `get_page_style()` de `utils.styles`")
st.success("✅ Le style est cohérent sur toutes les pages de l'application!")
