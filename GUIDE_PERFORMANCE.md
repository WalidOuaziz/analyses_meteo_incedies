# ⚡ Guide d'Optimisation des Performances

## 🎯 Problème Identifié
- **1,202,311 lignes** de données météo
- **118,605 lignes** de données incendies
- Cartes et graphiques lents
- Consommation mémoire élevée

## ✅ Solutions Implémentées

### 1. 📦 Module `utils/performance.py` Créé

#### Fonctions Disponibles :

**a) Échantillonnage des Données**
```python
from utils.performance import sample_data_for_viz

# Au lieu d'afficher 1M de points, afficher 10k
df_sample = sample_data_for_viz(df, max_points=10000)
```

**b) Agrégation Temporelle**
```python
from utils.performance import aggregate_temporal_data

# Agréger par mois au lieu de jours
df_monthly = aggregate_temporal_data(df, freq='M')
```

**c) Optimisation Graphiques**
```python
from utils.performance import optimize_plotly_figure

fig = px.line(...)
fig = optimize_plotly_figure(fig, max_points=5000)
st.plotly_chart(fig)
```

**d) Pagination Tables**
```python
from utils.performance import paginate_dataframe

# Afficher page par page
page = st.sidebar.number_input("Page", 1, 100, 1)
df_page = paginate_dataframe(df, page_size=100, page_num=page)
st.dataframe(df_page)
```

**e) Limitation Marqueurs Carte**
```python
from utils.performance import limit_map_markers

# Limiter à 500 marqueurs sur la carte
gdf_limited = limit_map_markers(gdf, max_markers=500)
```

### 2. 🔧 Fonction `load_data()` Améliorée

**Nouvelles Options :**
```python
# Charger seulement certaines colonnes
df = load_data(columns=['date', 'TN', 'TX', 'NOM_USUEL'])

# Charger seulement certaines années
df = load_data(years=[2020, 2021, 2022])

# Échantillonner 10% des données
df = load_data(sample_frac=0.1)

# Combiner les options
df = load_data(
    columns=['date', 'TX', 'TN'],
    years=[2020, 2021],
    sample_frac=0.5
)
```

### 3. 📊 Optimisations Recommandées par Page

#### **Page Carte Interactive**
```python
# AVANT (lent)
df = load_data()
st.map(df)  # 1M de points

# APRÈS (rapide)
from utils.performance import limit_map_markers, sample_data_for_viz

df = load_data(years=[2020, 2021, 2022])  # 3 ans au lieu de 70
df_sample = sample_data_for_viz(df, max_points=1000)
st.map(df_sample)  # 1k points
```

#### **Page Températures**
```python
# AVANT (lent)
fig = px.line(df, x='date', y='TX')  # 1M de points

# APRÈS (rapide)
from utils.performance import aggregate_temporal_data

df_monthly = aggregate_temporal_data(df, freq='M')  # Par mois
fig = px.line(df_monthly, x='date', y='TX')  # ~800 points
```

#### **Page Analyse Incendies**
```python
# AVANT (lent)
st.dataframe(incendies_df)  # 118k lignes

# APRÈS (rapide)
from utils.performance import paginate_dataframe

page = st.sidebar.number_input("Page", 1, 1186, 1)
df_page = paginate_dataframe(incendies_df, page_size=100, page_num=page)
st.dataframe(df_page)
st.caption(f"Page {page}/1186 | Total: {len(incendies_df):,} lignes")
```

## 🚀 Application Immédiate

### Option 1: Filtres Utilisateur (Recommandé)
Ajoutez dans la sidebar de chaque page :

```python
st.sidebar.markdown("### ⚡ Performance")

# Choix de la période
year_range = st.sidebar.slider(
    "Période d'analyse",
    1956, 2023, (2015, 2023)
)

# Niveau de détail
detail_level = st.sidebar.select_slider(
    "Niveau de détail",
    options=['Faible (rapide)', 'Moyen', 'Élevé (lent)'],
    value='Moyen'
)

# Mapper vers échantillonnage
sample_map = {
    'Faible (rapide)': 0.1,   # 10%
    'Moyen': 0.3,              # 30%
    'Élevé (lent)': 1.0        # 100%
}

# Charger avec paramètres
df = load_data(
    years=list(range(year_range[0], year_range[1]+1)),
    sample_frac=sample_map[detail_level]
)
```

### Option 2: Mode Performance Automatique

```python
# En haut de chaque page
PERFORMANCE_MODE = True  # Activer/désactiver

if PERFORMANCE_MODE:
    MAX_CHART_POINTS = 10000
    MAX_MAP_MARKERS = 500
    MAX_TABLE_ROWS = 1000
    AGGREGATE_FREQ = 'M'  # Mensuel
else:
    MAX_CHART_POINTS = None
    MAX_MAP_MARKERS = None
    MAX_TABLE_ROWS = None
    AGGREGATE_FREQ = 'D'  # Quotidien
```

## 📈 Gains Attendus

| Fonctionnalité | Avant | Après | Gain |
|----------------|-------|-------|------|
| Chargement données | 5-10s | 1-2s | **5x** |
| Affichage graphique | 10-15s | 1-2s | **7x** |
| Carte interactive | 20-30s | 2-3s | **10x** |
| Tableau de données | Crash | Instantané | **∞** |
| Utilisation mémoire | 2-3 GB | 500 MB | **4-6x** |

## 🔍 Débogage Performance

Utilisez le moniteur de performance :

```python
from utils.performance import PerformanceMonitor

monitor = PerformanceMonitor()

monitor.start("Chargement données")
df = load_data()
monitor.end("Chargement données")

monitor.start("Création graphique")
fig = px.line(...)
monitor.end("Création graphique")

monitor.display_stats()  # Affiche dans sidebar
```

## ⚙️ Configuration Globale

Créez `config.py` :

```python
# config.py
PERFORMANCE_CONFIG = {
    'enable_optimization': True,
    'max_chart_points': 10000,
    'max_map_markers': 500,
    'max_table_rows': 1000,
    'default_years': 5,  # Charger 5 dernières années par défaut
    'cache_ttl': 3600,   # Cache 1 heure
    'sample_frac': 0.3,  # 30% des données
}
```

## 🎨 Interface Performance

Ajoutez un bouton performance dans la sidebar :

```python
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Mode Performance")

perf_mode = st.sidebar.toggle("Activer", value=True)

if perf_mode:
    st.sidebar.success("✅ Mode rapide activé")
    st.sidebar.info(
        "• Données agrégées par mois\n"
        "• Max 10k points par graphique\n"
        "• Max 500 marqueurs sur cartes"
    )
else:
    st.sidebar.warning("⚠️ Mode complet (peut être lent)")
```

## 📝 Checklist Application

- [ ] Ajouter filtres temporels dans sidebar
- [ ] Limiter points sur graphiques (10k max)
- [ ] Limiter marqueurs sur cartes (500 max)
- [ ] Paginer les tables (100 lignes/page)
- [ ] Agréger données temporelles (mensuel)
- [ ] Utiliser cache efficacement
- [ ] Charger seulement colonnes nécessaires
- [ ] Ajouter indicateur de progression
- [ ] Optimiser mémoire avec downcast
- [ ] Activer mode WebGL pour Plotly

## 🚀 Commande de Lancement

```powershell
python -m streamlit run Home.py --server.maxUploadSize 1000
```

---

💡 **Astuce** : Commencez par le mode performance activé par défaut, puis laissez l'utilisateur désactiver si besoin de données complètes.
