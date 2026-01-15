import streamlit as st
from utils.data_loader import load_data, get_data_summary

# ==================== CONFIG PAGE ====================
st.set_page_config(
    page_title="🌦️ Géovisualisation Météo France",
    page_icon="🌍",
    layout="wide"
)

# ==================== TITRE ====================
st.title("🌍 Application de géovisualisation des données météo")
st.markdown(
    """
    Analyse et visualisation des données météorologiques françaises  
    **(Températures • Précipitations • Vent • Événements extrêmes)**
    """
)

# ==================== CHARGEMENT DES DONNÉES ====================
@st.cache_data
def load_global_data():
    return load_data()

df = load_global_data()

if df.empty:
    st.stop()

# ==================== RÉSUMÉ GLOBAL ====================
summary = get_data_summary(df)

st.subheader("📊 Aperçu des données")

col1, col2, col3, col4 = st.columns(4)

col1.metric("📍 Stations", summary["nb_stations"])
col2.metric("🗓️ Jours", summary["nb_jours"])
col3.metric("🗺️ Régions", summary["nb_regions"])
col4.metric("📄 Lignes", f"{summary['nb_lignes']:,}")

st.markdown("---")

# ==================== COMPLÉTUDE ====================
st.subheader("✅ Complétude des variables principales")

for var, rate in summary["completude"].items():
    st.progress(rate / 100, text=f"{var} : {rate:.1f}%")

st.info("➡️ Utilisez le menu de gauche pour naviguer entre les analyses.")
