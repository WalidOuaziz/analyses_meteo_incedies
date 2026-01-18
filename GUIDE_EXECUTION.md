# 🚀 Guide d'Exécution du Projet - Application de Géovisualisation

## 📋 Table des Matières
1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Lancement de l'Application](#lancement-de-lapplication)
4. [Structure du Projet](#structure-du-projet)
5. [Utilisation](#utilisation)
6. [Déploiement Streamlit Cloud](#déploiement-streamlit-cloud)
7. [Résolution des Problèmes](#résolution-des-problèmes)

---

## 🔧 Prérequis

### Logiciels Requis
- **Python 3.8+** (recommandé : Python 3.10 ou 3.11)
- **Git** (pour cloner le projet)
- **Éditeur de code** : VS Code, PyCharm, etc.

### Vérifier l'installation Python
```powershell
python --version
# Doit afficher : Python 3.x.x
```

---

## 💾 Installation

### 1. Cloner le Projet
```powershell
# Cloner le dépôt Git
git clone <URL_DU_DEPOT>

# Naviguer dans le dossier
cd app_geovisualisation
```

### 2. Créer un Environnement Virtuel
```powershell
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activer l'environnement (Windows CMD)
venv\Scripts\activate.bat

# Activer l'environnement (Linux/Mac)
source venv/bin/activate
```

**✅ Confirmation** : Vous devriez voir `(venv)` au début de votre ligne de commande.

### 3. Installer les Dépendances
```powershell
# Mettre à jour pip
python -m pip install --upgrade pip

# Installer les packages requis
pip install -r requirements.txt
```

**📦 Packages Principaux** :
- `streamlit` : Framework web
- `pandas` : Manipulation de données
- `plotly` : Graphiques interactifs
- `folium` : Cartes interactives
- `geopandas` : Données géospatiales
- `pyarrow` : Support format Parquet

### 4. Vérifier les Données
```powershell
# Lister les fichiers de données
Get-ChildItem data\raw -Recurse | Select-Object Name, Length | Format-Table
```

**📊 Fichiers Requis** :
- ✅ `meteo_sample.parquet` (~1 MB)
- ✅ `incendies_sample.parquet` (~2 MB)
- ✅ `dep_05/*.shp` (shapefiles département 05)
- ✅ `dep_13/*.shp` (shapefiles département 13)

**⚠️ Si les fichiers *_sample.parquet n'existent pas** :
```powershell
# Générer les échantillons (nécessite les fichiers complets)
python create_sample_data.py
```

---

## 🎯 Lancement de l'Application

### Méthode 1 : Commande Simple
```powershell
# S'assurer que l'environnement virtuel est activé
streamlit run Home.py
```

### Méthode 2 : Commande Python Module (Recommandée)
```powershell
# Plus fiable, fonctionne même si streamlit n'est pas dans le PATH
python -m streamlit run Home.py
```

### 🌐 Accès à l'Application
Après le lancement, l'application s'ouvre automatiquement dans votre navigateur :
- **URL locale** : http://localhost:8501
- **URL réseau** : http://[VOTRE_IP]:8501

**🛑 Pour arrêter l'application** :
- Appuyez sur `Ctrl + C` dans le terminal

---

## 📁 Structure du Projet

```
app_geovisualisation/
│
├── Home.py                          # Page d'accueil (point d'entrée)
├── requirements.txt                 # Dépendances Python
├── create_sample_data.py           # Script génération échantillons
├── .gitignore                      # Fichiers exclus de Git
│
├── pages/                          # Pages de l'application
│   ├── 1__Carte_Interactive.py     # Carte météo interactive
│   ├── 3__Températures.py          # Analyses températures
│   ├── 4__Précipitations.py        # Analyses précipitations
│   ├── 5__Analyse_du_Vent.py       # Analyses vent
│   ├── 6__Comparaisons_Géographiques.py  # Comparaisons stations
│   ├── 7__Événements_Extrêmes.py   # Événements climatiques
│   └── Analyse_Incendies.py        # Analyses incendies
│
├── utils/                          # Modules utilitaires
│   ├── __init__.py
│   ├── data_loader.py              # Chargement données optimisé
│   ├── constants.py                # Constantes globales
│   ├── styles.py                   # Styles CSS personnalisés
│   ├── loading.py                  # Spinners de chargement
│   ├── performance.py              # Optimisations performance
│   └── preprocessing.py            # Prétraitement données
│
├── components/                     # Composants réutilisables
│   ├── __init__.py
│   ├── charts.py                   # Graphiques
│   ├── filters.py                  # Filtres interactifs
│   └── maps.py                     # Cartes
│
└── data/                           # Données
    └── raw/
        ├── meteo_sample.parquet         # Données météo (2018-2023)
        ├── incendies_sample.parquet     # Données incendies (2010-2022)
        ├── dep_05/                      # Shapefiles Hautes-Alpes
        │   └── *.shp
        └── dep_13/                      # Shapefiles Bouches-du-Rhône
            └── *.shp
```

---

## 📊 Utilisation

### Navigation
L'application utilise une **barre latérale** pour naviguer entre les pages :

1. **🏠 Accueil** : Vue d'ensemble et statistiques
2. **🗺️ Carte Interactive** : Visualisation géographique
3. **🌡️ Températures** : Analyses thermiques
4. **💧 Précipitations** : Analyses pluviométriques
5. **💨 Analyse du Vent** : Rose des vents, rafales
6. **📍 Comparaisons Géographiques** : Multi-stations
7. **⚡ Événements Extrêmes** : Canicules, sécheresses
8. **🔥 Analyse Incendies** : Statistiques feux de forêt

### Filtres Disponibles
- **Période** : Sélection dates/années
- **Stations** : Choix stations météo
- **Départements** : Filtrage géographique
- **Variables** : Température, pluie, vent, etc.
- **Saisons** : Été, hiver, etc.

### Exports
- **📥 CSV** : Téléchargement données filtrées
- **📸 PNG** : Export graphiques (via Plotly)

---

## ☁️ Déploiement Streamlit Cloud

### Préparation

1. **Vérifier .gitignore**
```gitignore
# Fichiers exclus (trop volumineux)
data/raw/meteo.parquet
data/raw/incendies.parquet
data/raw/*.xlsx
data/raw/*.csv
```

2. **Vérifier requirements.txt**
```txt
streamlit>=1.28.0
pandas>=2.0.0
pyarrow>=12.0.0
...
```

3. **Vérifier les fichiers sample**
```powershell
# Doivent être < 5 MB chacun
Get-ChildItem data\raw\*_sample.parquet
```

### Étapes de Déploiement

#### 1. Pousser vers GitHub
```powershell
# Ajouter tous les fichiers
git add .

# Commit
git commit -m "Optimisation pour déploiement Streamlit Cloud"

# Push vers GitHub
git push origin main
```

#### 2. Configurer Streamlit Cloud

1. Aller sur **[share.streamlit.io](https://share.streamlit.io)**
2. Cliquer sur **"New app"**
3. Configurer :
   - **Repository** : Votre dépôt GitHub
   - **Branch** : main (ou master)
   - **Main file path** : `Home.py`
4. Cliquer sur **"Deploy"**

#### 3. Attendre le Déploiement
- ⏱️ Temps : 5-10 minutes
- 🔄 Statut visible dans l'interface
- ✅ URL publique générée automatiquement

### URL de l'Application
```
https://[NOM_APP]-[HASH].streamlit.app
```

---

## 🔧 Résolution des Problèmes

### Problème 1 : Module Not Found
**Erreur** : `ModuleNotFoundError: No module named 'streamlit'`

**Solution** :
```powershell
# Vérifier que l'environnement virtuel est activé
# Doit afficher (venv) au début de la ligne

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Problème 2 : Fichier de Données Introuvable
**Erreur** : `FileNotFoundError: data/raw/meteo_sample.parquet`

**Solution** :
```powershell
# Vérifier que les fichiers existent
ls data\raw\*.parquet

# Si absents, générer les échantillons
python create_sample_data.py
```

### Problème 3 : Port Déjà Utilisé
**Erreur** : `OSError: [Errno 48] Address already in use`

**Solution** :
```powershell
# Lancer sur un autre port
streamlit run Home.py --server.port 8502
```

### Problème 4 : Erreur Déploiement Streamlit Cloud
**Erreur** : `Oh no. Error running app`

**Causes Possibles** :
1. **Fichiers trop volumineux**
   ```powershell
   # Vérifier tailles
   Get-ChildItem -Recurse | Where {$_.Length -gt 5MB}
   ```

2. **Dépendances manquantes**
   ```txt
   # Ajouter à requirements.txt
   pyarrow>=12.0.0
   ```

3. **Chemin fichier incorrect**
   ```python
   # Utiliser chemins relatifs
   "data/raw/meteo_sample.parquet"  # ✅
   "D:/GMS/.../meteo_sample.parquet"  # ❌
   ```

### Problème 5 : Performances Lentes
**Solution 1 : Activer le Mode Performance**
```python
# Sur la page Comparaisons Géographiques
# Activer "Mode Performance (échantillonnage)"
```

**Solution 2 : Réduire la Période**
```python
# Filtrer sur 2-3 ans au lieu de 6 ans
years = [2021, 2022, 2023]
```

**Solution 3 : Vider le Cache**
```
# Menu Streamlit (haut droite) → Clear cache
```

---

## 📞 Commandes Utiles

### Gestion Environnement
```powershell
# Activer environnement
.\venv\Scripts\Activate.ps1

# Désactiver environnement
deactivate

# Lister packages installés
pip list

# Créer requirements.txt
pip freeze > requirements.txt
```

### Streamlit
```powershell
# Lancer application
streamlit run Home.py

# Lancer sur port spécifique
streamlit run Home.py --server.port 8502

# Désactiver auto-reload
streamlit run Home.py --server.runOnSave false

# Afficher version
streamlit --version
```

### Git
```powershell
# Statut modifications
git status

# Voir différences
git diff

# Ajouter fichiers
git add .

# Commit
git commit -m "Message"

# Push
git push
```

### Données
```powershell
# Générer échantillons
python create_sample_data.py

# Taille fichiers
Get-ChildItem data\raw -Recurse | Select Name, Length

# Compter lignes Parquet (en Python)
python -c "import pandas as pd; print(len(pd.read_parquet('data/raw/meteo_sample.parquet')))"
```

---

## 📚 Documentation Complémentaire

- **[ECHANTILLONNAGE_DONNEES.txt](ECHANTILLONNAGE_DONNEES.txt)** : Détails échantillonnage
- **[GUIDE_PERFORMANCE.md](GUIDE_PERFORMANCE.md)** : Optimisations performance
- **[GUIDE_LOADING.md](GUIDE_LOADING.md)** : Système de chargement
- **[README.md](README.md)** : Vue d'ensemble projet

---

## ✅ Checklist de Démarrage

- [ ] Python 3.8+ installé
- [ ] Projet cloné
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Fichiers de données présents (`meteo_sample.parquet`, `incendies_sample.parquet`)
- [ ] Application lancée (`streamlit run Home.py`)
- [ ] Navigateur ouvert sur http://localhost:8501
- [ ] Toutes les pages fonctionnelles

---

## 🎓 Prochaines Étapes

1. **Explorer l'application** : Tester toutes les pages
2. **Personnaliser** : Modifier couleurs, titres dans `utils/styles.py`
3. **Ajouter données** : Intégrer d'autres départements/régions
4. **Déployer** : Publier sur Streamlit Cloud
5. **Partager** : Diffuser l'URL publique

---

**📧 Support** : Consultez la documentation ou les fichiers GUIDE_*.md pour plus de détails.

**🌟 Bonne utilisation !**
