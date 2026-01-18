# 🌍 Application de Géovisualisation - Météo France

## 📋 Description

Application Streamlit pour l'analyse géospatiale des incendies et données météorologiques en France (Départements 13 et 05).

## ✨ Améliorations Récentes

### 🚀 Performance
- ✅ **Conversion CSV → Parquet** : Chargement 10x plus rapide
- ✅ **Suppression des fichiers non utilisés** : Optimisation de l'espace disque
- ✅ **Imports nettoyés** : Code plus propre et maintenable

### 🎨 Style et Interface
- ✅ **Design moderne** : Interface utilisateur repensée avec dégradés et animations
- ✅ **Sidebar stylisée** : Navigation améliorée avec style cohérent
- ✅ **Cartes et composants** : Composants visuels modernisés
- ✅ **Thème personnalisé** : Configuration couleurs dans `.streamlit/config.toml`

### 📦 Structure des Données

#### Fichiers de Données (Parquet - Format Optimisé)
```
data/raw/
├── meteo.parquet          # 1,202,311 lignes - Données météo complètes
├── incendies.parquet      # 118,605 lignes - Historique des incendies
├── dep_05/                # Shapefile département 05
└── dep_13/                # Shapefile département 13
```

## 🚀 Installation et Lancement

### 1. Activer l'environnement virtuel
```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Installer les dépendances (si nécessaire)
```powershell
pip install -r requirements.txt
```

### 3. Lancer l'application
```powershell
python -m streamlit run Home.py
```

L'application s'ouvrira automatiquement dans votre navigateur sur `http://localhost:8501`

## 📊 Pages Disponibles

### 🏠 Accueil
Tableau de bord principal avec description du projet et statistiques globales

### 🗺️ Analyse Incendies
- Statistiques des incendies par département
- Cartes interactives avec risques d'incendie
- Graphiques temporels et saisonniers

### 🗺️ Carte Interactive
Visualisation des stations météo sur carte interactive

### 🌡️ Températures
Analyse détaillée des températures avec tendances et anomalies

### 🌧️ Précipitations
Analyse des précipitations et sécheresses

### 💨 Analyse du Vent
Visualisation des vents avec roses des vents

### 🗺️ Comparaisons Géographiques
Comparaison multi-stations

### 🌪️ Événements Extrêmes
Détection et analyse des événements météorologiques extrêmes

## 🎨 Personnalisation du Style

Le style est centralisé dans `utils/styles.py` et peut être facilement modifié :

```python
from utils.styles import get_page_style

st.markdown(get_page_style(), unsafe_allow_html=True)
```

### Couleurs principales
- **Primaire** : `#3b82f6` (Bleu)
- **Succès** : `#10b981` (Vert)
- **Avertissement** : `#f59e0b` (Orange)
- **Danger** : `#ef4444` (Rouge)

## 📦 Technologies Utilisées

- **Streamlit** : Interface web interactive
- **Pandas** : Manipulation des données
- **GeoPandas** : Données géospatiales
- **Plotly** : Graphiques interactifs
- **Folium** : Cartes interactives
- **PyArrow** : Format Parquet optimisé

## 🔧 Dépannage

### L'application ne démarre pas
```powershell
# Vérifier que l'environnement virtuel est activé
.\venv\Scripts\Activate.ps1

# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

### Erreur de chargement des données
Vérifiez que les fichiers Parquet sont présents dans `data/raw/`:
- `meteo.parquet`
- `incendies.parquet`

### Port déjà utilisé
```powershell
# Lancer sur un autre port
python -m streamlit run Home.py --server.port 8502
```

## 📈 Optimisations

### Performance de Chargement
- **CSV** : ~10-15 secondes
- **Parquet** : ~1-2 secondes ⚡
- **Gain** : 5-10x plus rapide

### Taille des Fichiers
- **CSV** : ~200 MB
- **Parquet** : ~50 MB 📦
- **Gain** : 75% de réduction

## 👨‍💻 Développeur

**Walid Ouaziz**  
Projet de Géovisualisation - GMS

## 📄 Licence

Ce projet est développé dans un cadre académique.

---

💡 **Astuce** : Pour de meilleures performances, assurez-vous d'avoir au moins 4 GB de RAM disponibles.
