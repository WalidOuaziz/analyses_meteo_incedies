"""
Page d'accueil - Tableau de bord principal
Description complète du projet et navigation
"""

import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Import du style personnalisé
sys.path.append(str(Path(__file__).parent))
from utils.styles import get_page_style

# ==================== CONFIGURATION PAGE ====================

st.set_page_config(
    page_title="Accueil - Analyse Géospatiale",
    page_icon="🏠",
    layout="wide"
)

# ==================== CSS PERSONNALISÉ ====================

st.markdown(get_page_style(), unsafe_allow_html=True)

# ==================== HEADER ====================

st.title("🌍 Analyse Géospatiale - Météo France")
st.markdown("""
# Bienvenue sur le Tableau de Bord d'Analyse Géospatiale

**Une plateforme complète pour l'analyse des incendies, données climatiques et géographiques**

""")

# ==================== DESCRIPTION GÉNÉRALE ====================

st.markdown("---")
st.header("📋 Description Générale du Projet")

st.markdown("""
### Objectif Principal
Ce projet offre une analyse géospatiale complète et interactive des **incendies de forêt** 
en France, en particulier dans les **départements 13 (Bouches-du-Rhône) et 05 (Hautes-Alpes)**. 
Il combine des données géographiques, climatiques et d'incendies pour fournir des insights 
détaillés sur les risques d'incendie et les facteurs environnementaux. 

### Portée du Projet
- **Couverture Géographique**:  Départements 13 et 05 (Sud-Est France)
- **Période Couverte**: 1973 - 2022 (118,605 enregistrements d'incendies)
- **Source des Données**: 
  - Fichiers shapefile des communes (géométries)
  - Base de données d'incendies (CSV)
  - Données de topographie et forêt

### Public Cible
- Autorités environnementales
- Agences de gestion des risques
- Chercheurs en incendies de forêt
- Collectivités territoriales
- Professionnels de la prévention

""")

# ==================== DONNÉES DISPONIBLES ====================

st.markdown("---")
st.header("📊 Données Disponibles")

col1, col2, col3 = st.columns(3)

with col1:
    st. markdown("""
    ### 🗺️ Données Géospatiales
    - **Communes**:  Géométries complètes
    - **Topographie**: Pentes (min, moy, max)
    - **Forêts**: Surface forestière par commune
    - **Localisation**: Coordonnées précises
    - **Risque Incendie**: Indice calculé
    """)

with col2:
    st.markdown("""
    ### 🔥 Données Incendies
    - **118,605** incendies enregistrés
    - **Période**: 1973 - 2022
    - **Surface Affectée**: En hectares
    - **Localisation**: Par commune
    - **Temporalité**: Année, mois, heure
    - **Origine**: Type et source d'alerte
    """)

with col3:
    st.markdown("""
    ### 🌡️ Données Météorologiques
    - **Températures**: Max, Min, Moyenne
    - **Précipitations**: En mm
    - **Vent**:  Vitesse et direction
    - **Humidité**:  Données disponibles
    - **Évolution Annuelle**: Tendances
    """)

# ==================== PAGES DISPONIBLES ====================

st.markdown("---")
st.header("📑 Pages Disponibles")

st.markdown("""
### 1. 🏠 **Home** (Vous êtes ici)
- Présentation générale du projet
- Description des données
- Guide de navigation
- Points clés et statistiques

### 2. 🗺️ **Analyse Géospatiale** 
#### Contenu Principal: 
**📊 Statistiques & Filtres**
- Statistiques globales (communes, surface forêt, risque moyen)
- Filtres par département et risque minimum

**🔥 Graphiques Incendies (5 visualisations)**
- Nombre d'incendies par année (line chart)
- Nombre d'incendies par mois (histogram)
- Répartition mensuelle (pie chart)
- Surface affectée par année (bar chart)
- Analyse combinée nombre + surface (dual axis)

**📊 Analyses Géospatiales (2 visualisations)**
- Top 20 communes à risque élevé
- Couverture forestière par département

**🗺️ Cartes Interactives (3 cartes)**
1. **Carte du Risque Incendie** - Communes colorées par risque avec marqueurs incendies
2. **Carte des Pentes** - Choroplèthe montrant la topographie
3. **Heatmap des Incendies** - Densité spatiale des événements

**📋 Données Détaillées**
- Tableau complet filtrable
- Export en CSV

### 3. 📈 **Analyse Incendies** (Nouvelle)
#### Contenu Détaillé:
**🔥 Visualisations des Incendies**
- Évolution temporelle complète
- Distribution par saison
- Analyse par type d'incendie
- Localisation géographique
- Tendances et prévisions

**🌍 Cartes Spécialisées**
- Carte de densité des incendies
- Points chauds (hotspots)
- Evolution spatiale dans le temps

**📊 Statistiques Avancées**
- Corrélation avec météo
- Analyse saisonnière
- Comparaison interannuelle
- Tendances long terme

""")

# ==================== CARACTÉRISTIQUES TECHNIQUES ====================

st.markdown("---")
st.header("⚙️ Caractéristiques Techniques")

tab1, tab2, tab3 = st.tabs(["🔧 Architecture", "📊 Visualisations", "⚡ Performance"])

with tab1:
    st.markdown("""
    ### Stack Technologique
    - **Framework**: Streamlit (Python)
    - **Données Spatiales**: GeoPandas, Shapely
    - **Visualisation**: Plotly, Folium
    - **Traitement**: Pandas, NumPy
    - **Système Cache**:  Streamlit @st.cache_resource
    
    ### Structure des Données
    ```
    └── data/
        ├── raw/
        │   ├── dep_13/
        │   │   └── communes_13_with_data_for_carte_danger_incendie.shp
        │   ├── dep_05/
        │   │   └── communes_05_with_data_for_carte_danger_incendie.shp
        │   └── incendies. csv (118,605 lignes)
        └── processed/ (pour futures optimisations)
    ```
    """)

with tab2:
    st.markdown("""
    ### Types de Visualisations
    
    **Graphiques Statistiques** (8+)
    - Line Charts (tendances temporelles)
    - Bar Charts (comparaisons)
    - Histogrammes (distributions)
    - Pie Charts (parts de marché)
    - Box Plots (variations)
    - Scatter Plots (corrélations)
    
    **Cartes Géospatiales** (3+)
    - Choroplèthes (densités)
    - Heatmaps (concentrations)
    - Marqueurs (localisations)
    - Clusters (groupements)
    
    **Tableaux de Données**
    - Filtrables et triables
    - Export CSV
    - Pagination
    """)

with tab3:
    st.markdown("""
    ### Optimisations Appliquées
    
    **Chargement des Données**
    - Cache @st.cache_resource pour shapefiles
    - Session state pour éviter rechargements
    - Barre de progression pendant chargement
    - Messages informatifs clairs
    
    **Réduction Mémoire**
    - Chargement sélectif des colonnes (usecols)
    - Types numériques optimisés (int32, float32)
    - Filtrage précoce des données (deps 13, 05)
    - Limitation des points affichés sur cartes
    
    **Rendu Interactif**
    - Onglets pour éviter rechargement simultané
    - Spinner pendant génération cartes
    - Mode sombre supporté
    - Responsive sur mobile
    """)

# ==================== STATISTIQUES CLÉS ====================

st.markdown("---")
st.header("📈 Statistiques Clés")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📊 Total Incendies",
        "118,605",
        "1973-2022"
    )

with col2:
    st.metric(
        "🗺️ Communes",
        "~300",
        "Deps 13 & 05"
    )

with col3:
    st.metric(
        "📏 Surface Forêt",
        "~1. 2M ha",
        "Analysée"
    )

with col4:
    st.metric(
        "📅 Années",
        "50",
        "de données"
    )

# ==================== GUIDE D'UTILISATION ====================

st.markdown("---")
st.header("🎯 Guide d'Utilisation")

with st.expander("📘 Comment utiliser l'application? "):
    st.markdown("""
    ### Étape 1: Accédez aux Pages
    - Utilisez le menu de gauche (☰) pour naviguer
    - Cliquez sur "Analyse Géospatiale" pour les cartes et graphiques
    - Cliquez sur "Analyse Incendies" pour les incendies détaillés
    
    ### Étape 2: Filtrez les Données
    - Sélectionnez les départements (13, 05 ou les deux)
    - Ajustez le risque minimum d'incendie
    - Les graphiques se mettent à jour automatiquement
    
    ### Étape 3: Explorez les Visualisations
    - Passez la souris sur les graphiques pour plus de détails
    - Cliquez sur les légendes pour afficher/masquer des séries
    - Utilisez les onglets pour différentes vues
    
    ### Étape 4: Téléchargez les Données
    - Expandez "Données Détaillées"
    - Cliquez sur le bouton "Télécharger (CSV)"
    - Les données respectent vos filtres actuels
    
    ### Conseil Utile
    - Les cartes peuvent être agrandies en haut à droite
    - Les cartes supportent le zoom avec la molette de souris
    - Chaque marqueur a une popup avec infos détaillées
    """)

# ==================== FAQ ====================

st.markdown("---")
st.header("❓ Questions Fréquentes")

with st.expander("Quels départements sont couverts?"):
    st.markdown("""
    Le projet couvre actuellement les départements: 
    - **13 (Bouches-du-Rhône)** - Provence-Alpes-Côte d'Azur
    - **05 (Hautes-Alpes)** - Provence-Alpes-Côte d'Azur
    
    Ces régions présentent des taux d'incendies particulièrement élevés. 
    """)

with st.expander("Quelle est la précision des coordonnées?"):
    st.markdown("""
    - **Communes**: Centroïdes ou polices administatifs officiels
    - **Incendies**: Localisés au niveau commune (approximation ±5km)
    - **Cartes**: Précision au mètre pour shapefiles
    """)

with st.expander("Comment sont calculés les risques?"):
    st.markdown("""
    L'indice de risque est calculé comme suit:
    
    ```
    Risque = (Surface_Forêt/Max_Forêt × 0.5) + (Pente_Moy/Max_Pente × 0.5) × 100
    ```
    
    Facteurs considérés:
    - **50%**: Densité forestière
    - **50%**: Topographie (pente moyenne)
    
    **Interprétation**:
    - 🟢 0-25%: Risque faible
    - 🟡 25-50%:  Risque modéré
    - 🟠 50-75%: Risque élevé
    - 🔴 75-100%: Risque très élevé
    """)

with st.expander("Puis-je exporter les données?"):
    st.markdown("""
    Oui!  Dans chaque page: 
    1. Expandez "Données Détaillées" ou "Données Géospatiales"
    2. Cliquez le bouton "📥 Télécharger (CSV)"
    3. Les données téléchargées respectent vos filtres actuels
    
    Format:  CSV avec séparateur `;` (français)
    """)

with st.expander("Comment interpréter les graphiques?"):
    st.markdown("""
    ### Types de Graphiques
    
    **Line Chart (Nombre par Année)**
    - Axe X: Année
    - Axe Y: Nombre d'incendies
    - Tendance: Hausse/baisse au fil du temps
    
    **Bar Chart (Surface par Année)**
    - Axe X: Année
    - Axe Y: Surface parcourue (ha)
    - Comparative: Plus la barre est haute, plus de surface brûlée
    
    **Pie Chart (Répartition Mensuelle)**
    - Pourcentage du total par mois
    - Couleur: Plus intense = plus d'incendies
    
    **Heatmap**
    - 🔵 Bleu: Peu d'activité
    - 🟡 Jaune: Activité modérée
    - 🔴 Rouge: Forte concentration
    """)

# ==================== INFORMATION TECHNIQUE ====================

st.markdown("---")
st.header("ℹ️ Informations Supplémentaires")

col1, col2 = st.columns(2)

with col1:
    st. info("""
    ### 🔄 Mise à Jour des Données
    - Données incendies: Jusqu'au 20 septembre 2022
    - Données géographiques: Référentiel 2022
    - Mise à jour planifiée: Annuelle
    """)

with col2:
    st.warning("""
    ### ⚠️ Limitations Connues
    - Coordonnées incendies approximées au niveau commune
    - Données météo non intégrées (version future)
    - Couverture limitée à 2 départements
    """)

# ==================== CONTACT & SUPPORT ====================



# ==================== FOOTER ====================

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.caption("🏢 Développé par Météo France")

with col2:
    st. caption(f"📅 Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y')}")

with col3:
    st.caption("🔐 Données publiques - Libre d'accès")

st.markdown("""
---
**Disclaimer**: Cette application fournit une analyse à titre informatif.  
Les données et analyses ne remplacent pas les avis officiels des autorités.
""")