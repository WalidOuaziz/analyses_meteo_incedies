# 📋 Guide d'Utilisation des Spinners de Chargement

## ✅ Module Créé : `utils/loading.py`

Ce module fournit des fonctions pour afficher automatiquement des spinners pendant le chargement de tous les composants visuels.

---

## 🎯 Utilisation par Type de Composant

### 1. **Graphiques Plotly**

#### AVANT (sans loading) :
```python
fig = px.line(df, x='date', y='temperature')
st.plotly_chart(fig, use_container_width=True)
```

#### APRÈS (avec loading) :
```python
from utils.loading import display_chart

fig = px.line(df, x='date', y='temperature')
display_chart(fig, "⏳ Génération du graphique...", use_container_width=True)
```

### 2. **Cartes Folium**

#### AVANT :
```python
from streamlit_folium import st_folium

m = folium.Map(location=[43.5, 5.5], zoom_start=8)
st_folium(m, width=700, height=500)
```

#### APRÈS :
```python
from utils.loading import display_map

m = folium.Map(location=[43.5, 5.5], zoom_start=8)
display_map(m, "⏳ Chargement de la carte...", width=700, height=500)
```

### 3. **DataFrames / Tables**

#### AVANT :
```python
st.dataframe(df, use_container_width=True)
```

#### APRÈS :
```python
from utils.loading import display_dataframe

display_dataframe(df, "⏳ Chargement du tableau...", use_container_width=True)
```

### 4. **Création + Affichage en 1 étape**

Pour les opérations lourdes, combinez création et affichage :

```python
from utils.loading import create_and_display_chart

# Au lieu de :
# fig = create_complex_chart(df)  # Lent
# st.plotly_chart(fig)

# Utilisez :
create_and_display_chart(
    lambda: create_complex_chart(df),
    "⏳ Analyse complexe en cours...",
    use_container_width=True
)
```

### 5. **Context Manager (pour blocs de code)**

```python
from utils.loading import LoadingContext

with LoadingContext("⏳ Traitement des données...", show_success=True):
    df_filtered = df[df['year'] > 2020]
    df_aggregated = df_filtered.groupby('station').mean()
    fig = px.bar(df_aggregated)
# Affiche "✅ Terminé" automatiquement
```

---

## 🔧 Remplacement Global sur Toutes les Pages

### Page 3__Températures.py
```python
# Ligne 19 - Ajouter import
from utils.loading import display_chart

# Remplacer tous les st.plotly_chart par :
display_chart(fig, "⏳ Génération...", use_container_width=True)
```

### Page 4__Précipitations.py
```python
# Même chose
from utils.loading import display_chart
display_chart(fig, "⏳ Analyse des précipitations...", use_container_width=True)
```

### Page 5__Analyse_du_Vent.py
```python
from utils.loading import display_chart
display_chart(fig, "⏳ Calcul des vents...", use_container_width=True)
```

### Page 6__Comparaisons_Géographiques.py
```python
from utils.loading import display_chart
display_chart(fig, "⏳ Comparaison en cours...", use_container_width=True)
```

### Page 7__Événements_Extrêmes.py
```python
from utils.loading import display_chart
display_chart(fig, "⏳ Détection des événements...", use_container_width=True)
```

### Page 1__Carte_Interactive.py
```python
from utils.loading import display_map, display_chart

# Pour les cartes
display_map(m, "⏳ Chargement de la carte...", width=700, height=500)

# Pour les graphiques
display_chart(fig, "⏳ Création du graphique...", use_container_width=True)
```

### Page Analyse_Incendies.py
```python
from utils.loading import display_map, display_chart

# Cartes
display_map(m, "⏳ Carte des incendies...", width=700, height=500)

# Graphiques
display_chart(fig, "⏳ Statistiques incendies...", use_container_width=True)
```

---

## 📝 Rechercher et Remplacer (Regex)

Utilisez VS Code pour remplacer automatiquement :

### Pour les graphiques :
**Rechercher :** `st\.plotly_chart\((.*?),\s*use_container_width=True\)`  
**Remplacer par :** `display_chart($1, "⏳ Génération...", use_container_width=True)`

### Pour les cartes :
**Rechercher :** `st_folium\((.*?),\s*width=(.*?),\s*height=(.*?)\)`  
**Remplacer par :** `display_map($1, "⏳ Chargement...", width=$2, height=$3)`

### Pour les dataframes :
**Rechercher :** `st\.dataframe\((.*?),\s*use_container_width=True\)`  
**Remplacer par :** `display_dataframe($1, "⏳ Chargement...", use_container_width=True)`

---

## ⚡ Exemples Réels par Page

### Températures - Ligne 715
```python
# AVANT
st.plotly_chart(fig_annual, use_container_width=True)

# APRÈS
display_chart(fig_annual, "⏳ Évolution annuelle...", use_container_width=True)
```

### Températures - Ligne 723
```python
# AVANT
st.plotly_chart(fig_anom, use_container_width=True)

# APRÈS
display_chart(fig_anom, "⏳ Calcul des anomalies...", use_container_width=True)
```

### Températures - Ligne 752
```python
# AVANT
st.plotly_chart(fig_heatmap, use_container_width=True)

# APRÈS
display_chart(fig_heatmap, "⏳ Calendrier thermique...", use_container_width=True)
```

### Analyse Incendies - Cartes
```python
# AVANT
st_folium(m, width=700, height=500)

# APRÈS
display_map(m, "⏳ Carte des zones à risque...", width=700, height=500)
```

---

## 🎨 Messages de Spinner Personnalisés

### Suggestions par type de visualisation :

| Type | Message Suggéré |
|------|----------------|
| Graphique temporel | "⏳ Analyse de l'évolution..." |
| Heatmap | "⏳ Génération du calendrier..." |
| Boxplot | "⏳ Calcul des statistiques..." |
| Carte géographique | "⏳ Chargement de la carte..." |
| Carte choroplèthe | "⏳ Calcul des zones..." |
| Rose des vents | "⏳ Analyse des directions..." |
| Tableau de données | "⏳ Chargement des données..." |
| Statistiques | "⏳ Calcul en cours..." |

---

## ✅ Checklist d'Application

- [x] Module `utils/loading.py` créé
- [x] Import ajouté dans toutes les pages
- [ ] Remplacer `st.plotly_chart` par `display_chart` (Page 3)
- [ ] Remplacer `st.plotly_chart` par `display_chart` (Page 4)
- [ ] Remplacer `st.plotly_chart` par `display_chart` (Page 5)
- [ ] Remplacer `st.plotly_chart` par `display_chart` (Page 6)
- [ ] Remplacer `st.plotly_chart` par `display_chart` (Page 7)
- [ ] Remplacer `st_folium` par `display_map` (Page 1)
- [ ] Remplacer `st_folium` par `display_map` (Analyse Incendies)
- [ ] Remplacer `st.dataframe` par `display_dataframe` (toutes pages)

---

## 🚀 Résultat Attendu

Avant le chargement de chaque graphique/carte/tableau, l'utilisateur verra :
```
⏳ [Message personnalisé]...
```

Puis le composant s'affiche immédiatement après.

**Avantages :**
- ✅ Retour visuel immédiat
- ✅ Utilisateur sait que l'app travaille
- ✅ Meilleure expérience utilisateur
- ✅ Pas de page blanche pendant le chargement

---

**Prochaine étape :** Appliquer les remplacements sur toutes les pages !
