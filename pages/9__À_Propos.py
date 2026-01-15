"""
Page À Propos - Présentation du dashboard météorologiqu e
Explication des fonctionnalités et de l'utilité du site
"""

import streamlit as st
from datetime import datetime

# ==================== CONFIGURATION PAGE ====================

st.set_page_config(
    page_title="À Propos - Météo France Dashboard",
    page_icon="ℹ️",
    layout="wide"
)

# ==================== INTERFACE ====================

def main():
    
    # ==================== HEADER ====================
    
    st.title("ℹ️ À Propos de ce Dashboard")
    st.markdown("**Une plateforme interactive pour explorer les données météorologiques de la France (1956-2023)**")
    
    # ==================== INTRODUCTION ====================
    
    st.markdown("---")
    st.header("🎯 Qu'est-ce que c'est? ")
    
    intro_col1, intro_col2 = st.columns([1.5, 1])
    
    with intro_col1:
        st.markdown("""
        ### Dashboard Météorologique Interactif
        
        Ce site est une **plateforme d'analyse et de visualisation** des données météorologiques 
        françaises couvrant plus de **67 ans de données** (1956-2023).
        
        Il a été créé pour permettre aux utilisateurs (chercheurs, étudiants, climatologues, 
        météorologues) d'explorer et d'analyser les tendances climatiques, les événements 
        extrêmes et les variations régionales de la météo en France.
        
        ### 📊 Données Utilisées
        - **Source**: Météo-France
        - **Période**: 1956-2023 (67 ans)
        - **Stations**: 100+ stations météorologiques en France
        - **Mise à jour**: Quotidienne
        """)
    
    with intro_col2:
        st.metric("📅 Années de données", "67 ans")
        st.metric("🌍 Stations", "100+")
        st.metric("📈 Mesures", "1M+")
        st.metric("🗺️ Régions", "13+")
    
    # ==================== PAGES DISPONIBLES ====================
    
    st.markdown("---")
    st.header("📚 Pages Disponibles")
    
    pages_info = {
        "📈 Analyse Temporelle": {
            "icon": "📈",
            "description": "Visualisez l'évolution des variables météorologiques dans le temps",
            "features": [
                "✅ Graphiques d'évolution annuelle avec tendances",
                "✅ Cycle mensuel et saisonnier",
                "✅ Anomalies climatiques",
                "✅ Comparaison par décennie",
                "✅ Moyennes mobiles (7j, 30j, 365j)",
                "✅ Analyse de régression linéaire"
            ],
            "variables": "Température (Min, Max, Moy), Précipitations, Vent"
        },
        
        "🌡️ Analyse des Températures": {
            "icon":  "🌡️",
            "description": "Explorez les variations thermiques et les tendances",
            "features":  [
                "✅ Évolution des 3 paramètres (TN, TX, TM)",
                "✅ Jours extrêmes (chauds/froids)",
                "✅ Amplitude thermique",
                "✅ Filtre par altitude",
                "✅ Anomalies par rapport à la normale",
                "✅ Calendrier thermique interactif"
            ],
            "variables": "Température Min, Max, Moyenne"
        },
        
        "🌧️ Analyse des Précipitations": {
            "icon":  "🌧️",
            "description": "Analysez les régimes de précipitations et les extrêmes",
            "features": [
                "✅ Total annuel vs intensité",
                "✅ Jours pluvieux vs jours secs",
                "✅ Anomalies de précipitations",
                "✅ Classification par classes de vent",
                "✅ Évolution du nombre de jours pluvieux",
                "✅ Statistiques par mois et année"
            ],
            "variables": "Précipitations (mm)"
        },
        
        "💨 Analyse du Vent": {
            "icon": "💨",
            "description": "Étudiez la dynamique éolienne et les tempêtes",
            "features":  [
                "✅ Rose des vents (16 directions)",
                "✅ Vitesse moyenne et rafales maximales",
                "✅ Classification Beaufort",
                "✅ Anomalies et tendances",
                "✅ Jours extrêmes (tempêtes)",
                "✅ Intensité moyenne des événements"
            ],
            "variables": "Vitesse Vent, Rafales Maximales"
        },
        
        "🗺️ Comparaison Géographique": {
            "icon": "🗺️",
            "description": "Comparez plusieurs stations sur une même variable",
            "features": [
                "✅ Comparaison multi-stations (ligne, barres)",
                "✅ Analyse des gradients (altitude, latitude, longitude)",
                "✅ Rose des vents radar par station",
                "✅ Carte interactive avec localisation",
                "✅ Corrélations géographiques",
                "✅ Comparaison multi-variables"
            ],
            "variables": "Toutes les variables"
        },
        
        "🗺️ Carte Interactive": {
            "icon": "🗺️",
            "description": "Visualisez les données sur une carte interactive",
            "features": [
                "✅ Carte avec Markers ou Heatmap",
                "✅ Filtrage par année et date",
                "✅ Sélection de variable à afficher",
                "✅ Analyse topographique (altitude)",
                "✅ Top stations par valeur",
                "✅ Comparaison temporelle (7 jours)"
            ],
            "variables":  "Toutes les variables"
        },
        
        "🌪️ Événements Extrêmes": {
            "icon": "🌪️",
            "description":  "Détectez et analysez les phénomènes extrêmes",
            "features": [
                "✅ Détection vagues de chaleur (TX > 30°C / 3j)",
                "✅ Détection vagues de froid (TN < 0°C / 3j)",
                "✅ Analyse des tempêtes et rafales",
                "✅ Précipitations extrêmes (déluge)",
                "✅ Fréquence des événements par année",
                "✅ Localisation des hotspots"
            ],
            "variables": "TX, TN, RR, FFM, FXY"
        }
    }
    
    for page_name, page_data in pages_info.items():
        with st.expander(f"{page_data['icon']} {page_name}"):
            st.markdown(f"**{page_data['description']}**")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("**Fonctionnalités:**")
                for feature in page_data['features']:
                    st.markdown(f"- {feature}")
            
            with col2:
                st.markdown("**Variables disponibles:**")
                st.info(page_data['variables'])
    
    # ==================== VARIABLES EXPLIQUÉES ====================
    
    st.markdown("---")
    st.header("📊 Variables Météorologiques Expliquées")
    
    variables = {
        "🌡️ TN - Température Minimale": {
            "description": "La température la plus basse enregistrée au cours d'une journée",
            "unité": "°C",
            "seuils": {
                "Normal": "> 0°C",
                "Froid": "0°C à -5°C",
                "Très froid": "-5°C à -15°C",
                "Extrême":  "< -15°C"
            }
        },
        
        "🌡️ TX - Température Maximale": {
            "description":  "La température la plus élevée enregistrée au cours d'une journée",
            "unité": "°C",
            "seuils": {
                "Normal": "< 20°C",
                "Chaud": "20-30°C",
                "Très chaud": "30-38°C",
                "Extrême": "> 38°C"
            }
        },
        
        "🌡️ TM - Température Moyenne": {
            "description": "Moyenne des températures min et max d'une journée",
            "unité": "°C",
            "seuils": {
                "Normal": "Entre TN et TX",
                "Utilisée pour":  "Tendances climatiques générales"
            }
        },
        
        "📏 TAMPLI - Amplitude Thermique": {
            "description": "Différence entre la température maximale et minimale (TX - TN)",
            "unité": "°C",
            "seuils": {
                "Faible": "< 10°C (jours nuageux)",
                "Modérée": "10-20°C (conditions normales)",
                "Forte": "> 20°C (jours ensoleillés)"
            }
        },
        
        "🌧️ RR - Précipitations":  {
            "description": "Quantité d'eau tombée du ciel (pluie, neige convertie en eau)",
            "unité": "mm",
            "seuils": {
                "Pas de pluie": "0 mm",
                "Averse": "1-10 mm",
                "Pluie": "10-50 mm",
                "Forte pluie": "50-100 mm",
                "Déluge": "> 100 mm"
            }
        },
        
        "💨 FFM - Vitesse Moyenne du Vent": {
            "description": "Vitesse moyenne du vent sur la journée",
            "unité":  "m/s (× 3.6 = km/h)",
            "seuils": {
                "Calme": "0-2 m/s (0-7 km/h)",
                "Léger":  "2-5 m/s (7-18 km/h)",
                "Modéré": "5-11 m/s (18-40 km/h)",
                "Tempête": "> 17.5 m/s (> 63 km/h)"
            }
        },
        
        "🌪️ FXY - Rafales Maximales": {
            "description": "Vitesse maximale du vent enregistrée",
            "unité": "m/s (× 3.6 = km/h)",
            "seuils": {
                "Fort": "10.8 m/s (39 km/h)",
                "Coup de vent": "10.8-17.5 m/s (39-63 km/h)",
                "Tempête": "17.5-25 m/s (63-90 km/h)",
                "Tempête violente": "> 25 m/s (> 90 km/h)"
            }
        }
    }
    
    for var_name, var_info in variables.items():
        with st.expander(var_name):
            col1, col2 = st.columns([1.5, 1])
            
            with col1:
                st.markdown(f"**Description:** {var_info['description']}")
                st.markdown(f"**Unité:** {var_info['unité']}")
            
            with col2:
                st.markdown("**Seuils et Classifications:**")
                for seuil, valeur in var_info['seuils'].items():
                    st.markdown(f"- **{seuil}**:  {valeur}")
    
    # ==================== COMMENT UTILISER ====================
    
    st.markdown("---")
    st.header("🚀 Comment Utiliser le Dashboard")
    
    usage_steps = [
        ("1️⃣ Sélectionner une Page", "Chaque onglet correspond à un type d'analyse. Commencez par celle qui vous intéresse."),
        ("2️⃣ Configurer les Filtres", "Sélectionnez la période, la région, les stations, et la variable à analyser."),
        ("3️⃣ Explorer les Données", "Utilisez les graphiques interactifs pour découvrir les tendances et motifs."),
        ("4️⃣ Comparer et Analyser", "Utilisez les comparaisons géographiques ou temporelles pour des insights plus profonds."),
        ("5️⃣ Télécharger les Résultats", "Exportez les données en CSV pour analyse ultérieure."),
        ("6️⃣ Partager les Découvertes", "Utilisez les graphiques pour créer des rapports ou des présentations."),
    ]
    
    for step, description in usage_steps: 
        st.markdown(f"### {step}")
        st.markdown(f"{description}")
        st.markdown("")
    
    # ==================== CAS D'USAGE ====================
    
    st.markdown("---")
    st.header("💡 Cas d'Usage Possibles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎓 Recherche Académique")
        st.markdown("""
        - **Études climatiques** sur les tendances à long terme
        - **Analyse des extrêmes** pour thèses et publications
        - **Comparaisons régionales** des variations climatiques
        - **Données de validation** pour modèles climatiques
        """)
    
    with col2:
        st.markdown("### 🌍 Agriculture & Environnement")
        st.markdown("""
        - **Planification agricole** selon les régimes pluviométriques
        - **Analyse des risques** de sécheresse ou d'inondation
        - **Études phénologiques** en fonction de la température
        - **Adaptation au changement climatique** par région
        """)
    
    with col3:
        st.markdown("### 🏭 Énergie & Infrastructure")
        st.markdown("""
        - **Estimation de production** éolienne/hydraulique
        - **Prévention de dommages** par tempêtes
        - **Gestion de charge** selon les conditions météo
        - **Planification énergétique** long terme
        """)
    
    # ==================== CARACTÉRISTIQUES ====================
    
    st.markdown("---")
    st.header("⭐ Points Forts du Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Données
        - ✅ 67 ans de données (1956-2023)
        - ✅ 100+ stations météorologiques
        - ✅ 7 variables principales
        - ✅ Mise à jour quotidienne
        
        ### 📈 Analyses
        - ✅ Tendances longues périodes
        - ✅ Détection d'anomalies
        - ✅ Comparaisons multi-stations
        - ✅ Événements extrêmes
        """)
    
    with col2:
        st.markdown("""
        ### 🎨 Visualisations
        - ✅ Graphiques interactifs (Plotly)
        - ✅ Cartes géographiques (Folium)
        - ✅ Calendriers thermiques
        - ✅ Rose des vents
        
        ### 💾 Export
        - ✅ Téléchargement CSV
        - ✅ Graphiques haute résolution
        - ✅ Partage facile
        - ✅ API-friendly (future)
        """)
    
    # ==================== SEUILS EXTRÊMES ====================
    
    st.markdown("---")
    st.header("🚨 Seuils de Définition des Extrêmes")
    
    extremes_data = {
        "🔥 Vagues de Chaleur": "TX > 30°C pendant 3+ jours consécutifs",
        "❄️ Vagues de Froid": "TN < 0°C pendant 3+ jours consécutifs",
        "💧 Déluge": "RR > 100 mm en 24h",
        "🌪️ Tempête": "FFM > 17.5 m/s (63 km/h) ou FXY > 25 m/s (90 km/h)",
        "❄️ Neige": "Présence de TN < 0°C avec précipitations",
        "🌞 Canicule": "TX > 35°C pendant 3+ jours + nuit chaude"
    }
    
    for event, definition in extremes_data.items():
        st.markdown(f"**{event}**:  {definition}")
    
    # ==================== MÉTHODOLOGIE ====================
    
    st.markdown("---")
    st.header("🔬 Méthodologie")
    
    st.markdown("""
    ### Sources de Données
    - **Agence**:  Météo-France
    - **Couverture**: France métropolitaine et territoires
    - **Fréquence**: Données quotidiennes
    - **Validation**: Données QC (Quality Control) intégrées
    
    ### Calculs Effectués
    - **Moyennes annuelles**: Moyennes arithmétiques simples
    - **Tendances**: Régression linéaire par moindres carrés
    - **Anomalies**: Écart à la moyenne historique (1956-2023)
    - **Percentiles**:  Quantiles pour analyse de distributions
    
    ### Limitations
    - Les données manquantes sont exclues des calculs
    - Certaines stations n'ont pas l'historique complet (1956+)
    - QC ne garantit pas 100% d'exactitude
    - Conditions météo locales peuvent affecter les mesures
    """)
    
    # ==================== CONTACT & SUPPORT ====================
    
    st.markdown("---")
    st.header("📞 Support & Feedback")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🐛 Signaler un Bug
        Si vous découvrez un problème ou une erreur:
        1.Notez la date et l'heure
        2.Décrivez les étapes pour reproduire
        3.Envoyez à: support@meteo-dashboard.fr
        """)
    
    with col2:
        st.markdown("""
        ### 💬 Suggestions de Nouvelles Fonctionnalités
        Nous accueillons les suggestions! 
        - Nouveaux types d'analyses
        - Améliorations de performance
        - Nouvelles visualisations
        - Intégrations API
        """)
    
    # ==================== INFORMATIONS LÉGALES ====================
    
    st.markdown("---")
    st.header("⚖️ Informations Légales")
    
    st.markdown("""
    ### Licence des Données
    - Données Météo-France: License [ODbL](https://opendatacommons.org/licenses/odbl/1.0/)
    - Dashboard:  MIT License
    
    ### Confidentialité
    - Aucune donnée personnelle collectée
    - Aucun cookie de suivi
    - Logs serveur anonymisés
    
    ### Utilisation
    - À usage **libre et gratuit**
    - Attribution recommandée:  "Données Météo-France"
    - Pas de revente des données
    - Pour usage commercial: Contacter Météo-France
    """)
    
    # ==================== À PROPOS DE NOUS ====================
    
    st.markdown("---")
    st.header("👥 À Propos de Nous")
    
    st.markdown("""
    ### Qui Sommes-Nous?
    Ce dashboard a été créé dans le cadre d'un projet de **géovisualisation** 
    pour rendre les données météorologiques françaises accessible à tous.
    
    ### Notre Mission
    **Démocratiser l'accès aux données climatiques** et permettre à chacun
    (chercheurs, étudiants, professionnels, citoyens) de: 
    - Comprendre les tendances climatiques
    - Analyser les impacts locaux
    - Participer à la recherche climatique
    - Prendre des décisions informées
    
    ### Remerciements
    - Météo-France pour les données
    - Streamlit pour la plateforme
    - La communauté open-source
    """)
    
    # ==================== FOOTER ====================
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📚 Ressources
        - [Météo-France](https://www.meteo.fr)
        - [Données ouvertes](https://www.data.gouv.fr)
        - [OpenWeatherMap](https://openweathermap.org)
        """)
    
    with col2:
        st.markdown("""
        ### 🔗 Liens Utiles
        - [Glossaire Météo](https://www.meteo.fr)
        - [Rapports IPCC](https://www.ipcc.ch)
        - [GHG Data](https://ghgdata.es)
        """)
    
    with col3:
        st.markdown("""
        ### 📱 Suivez-Nous
        - Twitter: @MeteoFr
        - GitHub: dashboard-meteo
        - Email: info@meteo-dashboard.fr
        """)
    
    st.divider()
    
    st.caption(f"""
    © 2024 Dashboard Météorologique - Tous droits réservés | 
    Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M')} |
    Version: 1.0.0
    """)


if __name__ == "__main__": 
    main()