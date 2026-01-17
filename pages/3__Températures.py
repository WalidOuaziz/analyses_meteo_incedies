"""
Page d'analyse des températures - Données météorologiques
Visualisation de l'évolution des températures (1956-2023)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime

# Imports des modules utils
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_data
from utils.preprocessing import filter_by_altitude
from utils.constants import COLUMN_DESCRIPTIONS, UNITS, MONTHS_FR

# ==================== CONFIGURATION PAGE ====================

st.set_page_config(
    page_title="Analyse des Températures - Météo France",
    page_icon="🌡️",
    layout="wide"
)

# ==================== CACHE SESSION ====================

@st.cache_resource
def load_data_cached():
    """Charge les données une seule fois et les met en cache"""
    return load_data("data/raw/meteo_2000_2020.csv")

# ==================== STATIONS PACA ====================

STATIONS_PACA = [
    "AIX EN PROVENCE", "AIX-LA-MOLLE", "AIX-LES MILLES", "AIX-PUYRICARD",
    "ARLES", "ARLES-MAS-REY", "ARLES-ROUSTY", "ARLES-SALIN", "ARLES-SAMBUC",
    "ARLES-VILLE", "AUBAGNE", "AUBAGNE-DDE", "AURIOL COL DE LA COUTRONNE",
    "BARBENTANE", "BEC DE L AIGLE", "BERRE", "BOUC-BEL-AIR BOURG", "CABRIES",
    "CAP COURONNE", "CARRY-LE-ROUET", "CASSIS", "CASSIS-POMPIERS",
    "CHARLEVAL BOURG", "CHATEAURENARD", "CHATEUNEUF-LES", "CUGES-LES-PINS",
    "EYGUIERES", "EYRAGUES", "EYRAGUES DOMAINE DE BEAUCHAMP", "FOS-SUR-MER SOLMER",
    "GARDANNE", "GARDANNE LA MINE", "GEMENOS", "GRAVESON EDF", "GREASQUE LA MINE",
    "ISTRES", "JOUQUES", "LA CIOTAT LA GUILLAUMIERE", "LA CIOTAT PAVILLON DU PORT",
    "LA DESTROUSSE BOURG", "LA DESTROUSSE_SAPC", "LA FARE LES OLIVIERS",
    "LA PENNE-SUR-HUVEAUNE ECOLE", "LAMBESC", "LE-PUY-STE-REPA",
    "LES PENNES-MIRABEAU", "MALLEMORT", "MALLEMORT QUARTIER DES CLOS",
    "MALLEMORT-VILLE", "MARIGNANE", "MARSEILLE", "MARSEILLE ARENC",
    "MARSEILLE MONT ROSE", "MARSEILLE-BOREL", "MARSEILLE-MOUREPIANE",
    "MARSEILLE-OBS", "MARSEILLE-OLIVES", "MARSEILLE-PLANIER",
    "MARSEILLE-ST BARNABE", "MARSEILLE-STE MARTHE", "MARTIGUES",
    "MARTIGUES PONTEAU - EDF", "MARTIGUES-COURONNE", "MEYRARGUES",
    "MEYREUIL", "MIMET", "MIRAMAS PONTS ET CHAUSSEES", "MRS-LA-BOUDINIE",
    "MRS-PHARO", "PEYROLLES EN PROVENCE", "PEYROLLES_FORET",
    "PEYROLLES-EN-PROVENCE EDF", "PLAN-D'ORGON SAINT-ESTEVE", "POMEGUES",
    "PORT-DE-BOUC BOTTAI", "PORT-DE-BOUC-SJ", "PORT-DE-BOUC-TP",
    "PORT-SAINT-LOUIS-DU-RHONE-P-C", "PORT-ST-LOUIS-DU-RHONE-GARAGE",
    "PORT-ST-LOUIS-DU-RHONE-MAS", "ROGNES", "ROGNES TOURNEFORT",
    "ROQUEFORT-LA-BEDOULE", "ROQUEFORT-LA-BEDOULE ECOLE", "ROQUEVAIRE",
    "ROUSSET", "SAINT-MARTIN-DE-CRAU VERGIERE", "SAINT-MARTIN-DE-CRAU VILLAGE",
    "ST CANNAT", "ST CHAMAS", "ST-ANDIOL", "STE BAUME", "STES MARIES-DDE",
    "STES-MARIES-DE-LA-MER", "ST-MARTIN-CRAU", "ST-MARTIN-LE LUQUIER"
]

# ==================== FONCTIONS DE VISUALISATION ====================

def create_evolution_annuelle(df, variable):
    """Graphique d'évolution annuelle avec min/max"""
    if 'annee' not in df.columns or variable not in df.columns:
        return None
    
    df_yearly = df.groupby('annee')[variable].agg(['mean', 'min', 'max', 'std']).reset_index()
    
    fig = go.Figure()
    
    # Zone min-max
    fig.add_trace(go.Scatter(
        x=df_yearly['annee'],
        y=df_yearly['max'],
        mode='lines',
        name='Maximum',
        line=dict(color='rgba(231, 76, 60, 0.3)', width=1),
        showlegend=True
    ))
    
    fig.add_trace(go.Scatter(
        x=df_yearly['annee'],
        y=df_yearly['min'],
        mode='lines',
        name='Minimum',
        line=dict(color='rgba(52, 152, 219, 0.3)', width=1),
        fill='tonexty',
        fillcolor='rgba(52, 152, 219, 0.1)',
        showlegend=True
    ))
    
    # Ligne moyenne
    fig.add_trace(go.Scatter(
        x=df_yearly['annee'],
        y=df_yearly['mean'],
        mode='lines+markers',
        name='Moyenne',
        line=dict(color='#3498db', width=3),
        marker=dict(size=6, color='#3498db')
    ))
    
    # Tendance linéaire
    z = np.polyfit(df_yearly['annee'], df_yearly['mean'], 1)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(
        x=df_yearly['annee'],
        y=p(df_yearly['annee']),
        mode='lines',
        name='Tendance',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=f'Évolution Annuelle - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        xaxis_title='Année',
        yaxis_title=f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})',
        height=500,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Annotation de tendance
    tendance = z[0]
    signe = "+" if tendance > 0 else ""
    fig.add_annotation(
        text=f"Tendance: {signe}{tendance:.3f} {UNITS.get(variable, '')}/an",
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        showarrow=False,
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="red",
        borderwidth=2
    )
    
    return fig


def create_evolution_mensuelle(df, variable, annee_selectionnee=None):
    """Graphique d'évolution mensuelle"""
    if 'mois' not in df.columns or variable not in df.columns:
        return None
    
    if annee_selectionnee and 'annee' in df.columns:
        df = df[df['annee'] == annee_selectionnee]
    
    if 'annee' in df.columns:
        df_monthly = df.groupby(['annee', 'mois'])[variable].mean().reset_index()
        
        fig = px.line(
            df_monthly,
            x='mois',
            y=variable,
            color='annee',
            title=f'Évolution Mensuelle - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
            labels={
                'mois': 'Mois',
                variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})',
                'annee': 'Année'
            },
            markers=True
        )
    else:
        df_monthly = df.groupby('mois')[variable].mean().reset_index()
        
        fig = px.line(
            df_monthly,
            x='mois',
            y=variable,
            title=f'Cycle Annuel Moyen - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
            labels={
                'mois': 'Mois',
                variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})'
            },
            markers=True
        )
        fig.update_traces(line_color='#3498db', line_width=3, marker_size=8)
    
    fig.update_xaxes(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
                  'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    )
    
    fig.update_layout(height=500, hovermode='x unified', template='plotly_white')
    
    return fig


def create_heatmap_annuel(df, variable):
    """Heatmap mois x année"""
    if 'annee' not in df.columns or 'mois' not in df.columns or variable not in df.columns:
        return None
    
    df_pivot = df.groupby(['annee', 'mois'])[variable].mean().reset_index()
    df_pivot = df_pivot.pivot(index='mois', columns='annee', values=variable)
    
    fig = go.Figure(data=go.Heatmap(
        z=df_pivot.values,
        x=df_pivot.columns,
        y=['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
           'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
        colorscale='RdYlBu_r',
        colorbar=dict(title=UNITS.get(variable, '')),
        hoverongaps=False,
        hovertemplate='Année: %{x}<br>Mois: %{y}<br>Valeur: %{z:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'Calendrier Thermique - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        xaxis_title='Année',
        yaxis_title='Mois',
        height=500,
        template='plotly_white'
    )
    
    return fig


def create_comparison_decades(df, variable):
    """Comparaison par décennie"""
    if 'annee' not in df.columns or variable not in df.columns:
        return None
    
    # Créer les décennies
    df['decennie'] = (df['annee'] // 10) * 10
    df['decennie_label'] = df['decennie'].astype(str) + 's'
    
    df_decades = df.groupby(['decennie', 'decennie_label', 'mois'])[variable].mean().reset_index()
    
    fig = px.line(
        df_decades,
        x='mois',
        y=variable,
        color='decennie_label',
        title=f'Comparaison par Décennie - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        labels={
            'mois': 'Mois',
            variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})',
            'decennie_label': 'Décennie'
        },
        markers=True
    )
    
    fig.update_xaxes(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
                  'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    )
    
    fig.update_layout(height=500, hovermode='x unified', template='plotly_white')
    
    return fig


def create_boxplot_mensuel(df, variable):
    """Boxplot par mois"""
    if 'mois' not in df.columns or variable not in df.columns:
        return None
    
    df['mois_nom'] = df['mois'].map({
        1: 'Jan', 2: 'Fév', 3: 'Mar', 4: 'Avr', 5: 'Mai', 6: 'Juin',
        7: 'Juil', 8: 'Août', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Déc'
    })
    
    fig = px.box(
        df,
        x='mois',
        y=variable,
        title=f'Distribution Mensuelle - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        labels={
            'mois': 'Mois',
            variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})'
        },
        color='mois',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_xaxes(
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 
                  'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    )
    
    fig.update_layout(height=500, showlegend=False, template='plotly_white')
    
    return fig


def create_moyennes_mobiles(df, variable, window=30):
    """Graphique avec moyennes mobiles"""
    if 'date' not in df.columns or variable not in df.columns:
        return None
    
    # Agréger par date
    df_daily = df.groupby('date')[variable].mean().reset_index().sort_values('date')
    
    # Calculer moyennes mobiles
    df_daily['MA_7'] = df_daily[variable].rolling(window=7, center=True).mean()
    df_daily['MA_30'] = df_daily[variable].rolling(window=30, center=True).mean()
    df_daily['MA_365'] = df_daily[variable].rolling(window=365, center=True).mean()
    
    fig = go.Figure()
    
    # Données brutes (semi-transparentes)
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily[variable],
        mode='lines',
        name='Données quotidiennes',
        line=dict(color='lightgray', width=1),
        opacity=0.5
    ))
    
    # Moyenne mobile 7 jours
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['MA_7'],
        mode='lines',
        name='Moyenne mobile 7 jours',
        line=dict(color='#3498db', width=2)
    ))
    
    # Moyenne mobile 30 jours
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['MA_30'],
        mode='lines',
        name='Moyenne mobile 30 jours',
        line=dict(color='#e74c3c', width=2)
    ))
    
    # Moyenne mobile 365 jours
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['MA_365'],
        mode='lines',
        name='Moyenne mobile 365 jours',
        line=dict(color='#2ecc71', width=3)
    ))
    
    fig.update_layout(
        title=f'Moyennes Mobiles - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        xaxis_title='Date',
        yaxis_title=f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})',
        height=500,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def create_anomalies_chart(df, variable):
    """Graphique des anomalies"""
    if 'annee' not in df.columns or 'mois' not in df.columns or variable not in df.columns:
        return None
    
    # Calculer moyenne historique par mois
    moyenne_historique = df.groupby('mois')[variable].mean()
    
    # Calculer anomalies
    df_anom = df.copy()
    df_anom['moyenne_hist'] = df_anom['mois'].map(moyenne_historique)
    df_anom['anomalie'] = df_anom[variable] - df_anom['moyenne_hist']
    
    # Agréger par année
    df_yearly_anom = df_anom.groupby('annee')['anomalie'].mean().reset_index()
    
    # Couleurs selon signe
    colors = ['#e74c3c' if x > 0 else '#3498db' for x in df_yearly_anom['anomalie']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=df_yearly_anom['annee'],
            y=df_yearly_anom['anomalie'],
            marker_color=colors,
            hovertemplate='Année: %{x}<br>Anomalie: %{y:.2f}<extra></extra>'
        )
    ])
    
    fig.add_hline(y=0, line_dash="dash", line_color="black", line_width=2)
    
    fig.update_layout(
        title=f'Anomalies par rapport à la Moyenne Historique - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        xaxis_title='Année',
        yaxis_title=f'Anomalie ({UNITS.get(variable, "")})',
        height=500,
        template='plotly_white',
        showlegend=False
    )
    
    return fig


def create_jours_extremes_chart(df, variable, seuil=None):
    """Graphique du nombre de jours extrêmes"""
    if 'annee' not in df.columns or variable not in df.columns:
        return None
    
    if seuil is None:
        seuil = df[variable].quantile(0.90) if variable in ['TX', 'TM'] else df[variable].quantile(0.10)
    
    if variable in ['TX', 'TM']:
        label = f"Jours > {seuil:.1f}°C"
        df_extremes = df[df[variable] > seuil].groupby('annee').size().reset_index(name='jours_extremes')
    else:
        label = f"Jours < {seuil:.1f}°C"
        df_extremes = df[df[variable] < seuil].groupby('annee').size().reset_index(name='jours_extremes')
    
    fig = px.bar(
        df_extremes,
        x='annee',
        y='jours_extremes',
        title=f'Nombre de Jours Extrêmes - {label}',
        labels={
            'annee': 'Année',
            'jours_extremes':  'Nombre de jours'
        },
        color='jours_extremes',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(height=500, template='plotly_white', showlegend=False)
    
    return fig


def create_comparison_variables(df):
    """Comparaison des trois variables TN, TX, TM"""
    variables = ['TN', 'TX', 'TM']
    variables_dispo = [v for v in variables if v in df.columns]
    
    if len(variables_dispo) < 2:
        return None
    
    df_yearly = df.groupby('annee')[variables_dispo].mean().reset_index()
    
    fig = go.Figure()
    
    for var in variables_dispo:
        label_map = {'TN': 'Température Min', 'TX': 'Température Max', 'TM':  'Température Moy'}
        fig.add_trace(go.Scatter(
            x=df_yearly['annee'],
            y=df_yearly[var],
            mode='lines+markers',
            name=label_map.get(var, var),
            line=dict(width=2)
        ))
    
    fig.update_layout(
        title='Comparaison des Températures (Min, Max, Moy)',
        xaxis_title='Année',
        yaxis_title='Température (°C)',
        height=500,
        hovermode='x unified',
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def calculate_statistics(df, variable):
    """Calcule les statistiques descriptives"""
    if variable not in df.columns:
        return None
    
    stats = {
        'Moyenne': df[variable].mean(),
        'Médiane': df[variable].median(),
        'Écart-type': df[variable].std(),
        'Minimum': df[variable].min(),
        'Maximum': df[variable].max(),
        'Q1 (25%)': df[variable].quantile(0.25),
        'Q3 (75%)': df[variable].quantile(0.75),
        'Étendue': df[variable].max() - df[variable].min(),
        'Coefficient de variation': (df[variable].std() / df[variable].mean() * 100) if df[variable].mean() != 0 else 0
    }
    
    return stats


# ==================== INTERFACE PRINCIPALE ====================

def main():
    st.title("🌡️ Analyse des Températures")
    st.markdown("**Exploration de l'évolution thermique de 1956 à 2023**")
    
    # ==================== FILTRES DE PÉRIODE (AVANT CHARGEMENT) ====================
    
    st.markdown("---")
    st.subheader("🎛️ Sélection de la Période")
    
    # Charger uniquement les métadonnées pour afficher les années disponibles
    with st.spinner("📊 Chargement des métadonnées..."):
        df_full = load_data_cached()
    
    if df_full.empty:
        st.error("❌ Fichier CSV introuvable:  data/raw/meteo_2000_2020.csv")
        st.stop()
    
    # Extraction des années disponibles
    annee_min = int(df_full['annee'].min())
    annee_max = int(df_full['annee'].max())
    
    # Interface de sélection de période
    filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 2])
    
    with filter_col1:
        st.markdown("##### 📅 Mode de Sélection")
        mode_periode = st.radio(
            "Choisir la période",
            options=['Toute la période', 'Plage personnalisée', 'Années spécifiques'],
            horizontal=False
        )
    
    with filter_col2:
        st.markdown("##### 📏 Plage")
        
        if mode_periode == 'Plage personnalisée':
            col_a, col_b = st.columns(2)
            with col_a:
                annee_debut = st.slider(
                    "Année de début",
                    min_value=annee_min,
                    max_value=annee_max,
                    value=annee_min,
                    step=1
                )
            with col_b:
                annee_fin = st.slider(
                    "Année de fin",
                    min_value=annee_debut,
                    max_value=annee_max,
                    value=annee_max,
                    step=1
                )
            
            periode_affichage = f"{annee_debut}-{annee_fin}"
            df = df_full[(df_full['annee'] >= annee_debut) & (df_full['annee'] <= annee_fin)].copy()
            
        elif mode_periode == 'Années spécifiques':
            annees_dispo = sorted(df_full['annee'].unique().tolist(), reverse=True)
            annees_select = st.multiselect(
                "Sélectionnez les années",
                options=annees_dispo,
                default=annees_dispo[: 5]
            )
            
            if annees_select:
                periode_affichage = f"{len(annees_select)} années sélectionnées"
                df = df_full[df_full['annee'].isin(annees_select)].copy()
            else:
                st.warning("⚠️ Sélectionnez au moins une année")
                st.stop()
        else:
            periode_affichage = f"{annee_min}-{annee_max}"
            df = df_full.copy()
    
    with filter_col3:
        st.markdown("##### 📊 Statistiques")
        st.info(f"""
        **Données chargées:**
        - Période: {periode_affichage}
        - Lignes: {len(df):,}
        - Stations: {df['NUM_POSTE'].nunique()}
        """)
    
    st.markdown("---")
    
    # ==================== FILTRES GÉOGRAPHIQUES ====================
    
    st.subheader("🎛️ Filtres Géographiques")
    
    filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 2])
    
    with filter_col1:
        st.markdown("##### 📍 Zone")
        
        filtre_zone = st.radio(
            "Localisation",
            options=['France', 'PACA', 'Stations PACA'],
            horizontal=True
        )
        
        if filtre_zone == 'PACA':
            df = df[
                df['NOM_USUEL'].str.upper().isin([s.upper() for s in STATIONS_PACA])
            ].copy()
            zone_affichage = "Région PACA"
            
        elif filtre_zone == 'Stations PACA':
            stations_dispo = sorted([
                s for s in STATIONS_PACA 
                if s.upper() in df['NOM_USUEL'].str.upper().values
            ])
            
            stations_select = st.multiselect(
                "Sélectionnez les stations",
                options=stations_dispo,
                default=stations_dispo[:3] if len(stations_dispo) >= 3 else stations_dispo
            )
            
            if stations_select:
                df = df[
                    df['NOM_USUEL'].str.upper().isin([s.upper() for s in stations_select])
                ].copy()
                zone_affichage = f"{len(stations_select)} station(s) PACA"
            else: 
                st.warning("⚠️ Sélectionnez au moins une station")
                st.stop()
        else:
            zone_affichage = "France entière"
    
    with filter_col2:
        st.markdown("##### 🌡️ Variable")
        
        variables_dispo = {
            'TN': '🌡️ Température Min',
            'TX': '🌡️ Température Max',
            'TM': '🌡️ Température Moy'
        }
        
        variables_dict = {k: v for k, v in variables_dispo.items() if k in df.columns}
        
        variable_select = st.selectbox(
            "Choisir la variable",
            options=list(variables_dict.keys()),
            format_func=lambda x: variables_dict[x]
        )
    
    with filter_col3:
        st.markdown("##### 📏 Altitude")
        if 'ALTI' in df.columns:
            alti_min, alti_max = st.slider(
                "Plage d'altitude (m)",
                min_value=int(df['ALTI'].min()),
                max_value=int(df['ALTI'].max()),
                value=(int(df['ALTI'].min()), int(df['ALTI'].max()))
            )
            df = df[(df['ALTI'] >= alti_min) & (df['ALTI'] <= alti_max)].copy()
    
    st.markdown("---")
    
    if df.empty:
        st.warning("⚠️ Aucune donnée disponible avec ces filtres")
        st.stop()
    
    # ==================== STATISTIQUES ====================
    
    st.subheader(f"📊 Statistiques - {periode_affichage} | {zone_affichage}")
    
    stats = calculate_statistics(df, variable_select)
    
    if stats: 
        stat_cols = st.columns(5)
        unit = UNITS.get(variable_select, '°C')
        
        with stat_cols[0]:
            st.metric("Moyenne", f"{stats['Moyenne']:.2f} {unit}")
        with stat_cols[1]:
            st.metric("Médiane", f"{stats['Médiane']:.2f} {unit}")
        with stat_cols[2]:
            st.metric("Écart-type", f"{stats['Écart-type']:.2f} {unit}")
        with stat_cols[3]: 
            st.metric("Minimum", f"{stats['Minimum']:.2f} {unit}")
        with stat_cols[4]:
            st.metric("Maximum", f"{stats['Maximum']:.2f} {unit}")
    
    st.markdown("---")
    
    # ==================== VISUALISATIONS ====================
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Évolution Annuelle",
        "📅 Cycle Mensuel",
        "🗓️ Calendrier",
        "📊 Distributions",
        "🔍 Jours Extrêmes",
        "🔍 Analyses Avancées"
    ])
    
    with tab1:
        st.subheader("Évolution sur la Période")
        
        fig_annual = create_evolution_annuelle(df, variable_select)
        if fig_annual:
            st.plotly_chart(fig_annual, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Anomalies Climatiques")
            fig_anom = create_anomalies_chart(df, variable_select)
            if fig_anom: 
                st.plotly_chart(fig_anom, use_container_width=True)
        
        with col2:
            st.markdown("#### Comparaison par Décennie")
            fig_decades = create_comparison_decades(df, variable_select)
            if fig_decades:
                st.plotly_chart(fig_decades, use_container_width=True)
    
    with tab2:
        st.subheader("Cycles Mensuels")
        
        annee_selectionnee = None
        if mode_periode == 'Années spécifiques' and annees_select and len(annees_select) == 1:
            annee_selectionnee = annees_select[0]
        
        fig_monthly = create_evolution_mensuelle(df, variable_select, annee_selectionnee)
        if fig_monthly: 
            st.plotly_chart(fig_monthly, use_container_width=True)
        
        st.markdown("#### Distribution par Mois")
        fig_box = create_boxplot_mensuel(df, variable_select)
        if fig_box: 
            st.plotly_chart(fig_box, use_container_width=True)
    
    with tab3:
        st.subheader("Calendrier Thermique")
        
        fig_heatmap = create_heatmap_annuel(df, variable_select)
        if fig_heatmap:
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            st.info("""
            💡 **Interprétation**:  Cette visualisation permet d'identifier rapidement: 
            - Les mois et années les plus chauds/froids
            - Les tendances saisonnières
            - Les anomalies climatiques
            """)
    
    with tab4:
        st.subheader("Distributions Statistiques")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogramme
            fig_hist = px.histogram(
                df.dropna(subset=[variable_select]),
                x=variable_select,
                nbins=50,
                title=f'Distribution - {COLUMN_DESCRIPTIONS.get(variable_select, variable_select)}',
                labels={variable_select: f'{COLUMN_DESCRIPTIONS.get(variable_select, variable_select)} ({UNITS.get(variable_select, "")})'},
                color_discrete_sequence=['#3498db']
            )
            fig_hist.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Statistiques détaillées
            if stats:
                st.markdown("#### Statistiques Détaillées")
                stats_df = pd.DataFrame(list(stats.items()), columns=['Statistique', 'Valeur'])
                stats_df['Valeur'] = stats_df['Valeur'].apply(lambda x: f"{x:.2f}" if isinstance(x, float) else str(x))
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    with tab5:
        st.subheader("Analyse des Jours Extrêmes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Jours Chauds/Froids")
            fig_extremes = create_jours_extremes_chart(df, variable_select)
            if fig_extremes: 
                st.plotly_chart(fig_extremes, use_container_width=True)
        
        with col2:
            st.markdown("#### Statistiques Extrêmes")
            
            if variable_select in ['TX', 'TM']: 
                p90 = df[variable_select].quantile(0.90)
                st.metric(f"90e percentile", f"{p90:.2f}°C")
                st.metric("Jours au-dessus du 90e percentile", f"{(df[variable_select] > p90).sum()}")
            else:
                p10 = df[variable_select].quantile(0.10)
                st.metric(f"10e percentile", f"{p10:.2f}°C")
                st.metric("Jours au-dessous du 10e percentile", f"{(df[variable_select] < p10).sum()}")
    
    with tab6:
        st.subheader("Analyses Avancées")
        
        # Sous-onglets pour les analyses avancées
        subtab1, subtab2, subtab3, subtab4 = st.tabs(["Moyennes Mobiles", "Comparaison Variables", "Tendances", "Export"])
        
        with subtab1:
            st.markdown("#### Lissage par Moyennes Mobiles")
            
            # Limiter les données pour performance
            if len(df) > 50000:
                st.warning(f"⚠️ Trop de données ({len(df):,}).Échantillonnage aléatoire de 50,000 points.")
                df_sample = df.sample(50000, random_state=42)
            else:
                df_sample = df

            fig_ma = create_moyennes_mobiles(df_sample, variable_select)
            if fig_ma:
                st.plotly_chart(fig_ma, use_container_width=True)
                
                st.info("""
                💡 **Légende**:
                - **7 jours**: Tendance hebdomadaire
                - **30 jours**: Tendance mensuelle
                - **365 jours**: Tendance annuelle
                """)
        
        with subtab2:
            st.markdown("#### Comparaison des Variables Thermiques")
            
            fig_comp = create_comparison_variables(df)
            if fig_comp: 
                st.plotly_chart(fig_comp, use_container_width=True)
            else:
                st.info("Pas assez de variables disponibles pour la comparaison")
        
        with subtab3:
            st.markdown("#### Analyse de Tendance")
            
            if 'annee' in df.columns:
                df_yearly = df.groupby('annee')[variable_select].mean().reset_index()
                
                # Régression linéaire
                z = np.polyfit(df_yearly['annee'], df_yearly[variable_select], 1)
                tendance_an = z[0]
                tendance_totale = tendance_an * (df_yearly['annee'].max() - df_yearly['annee'].min())
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Tendance annuelle",
                        f"{tendance_an:+.3f} {UNITS.get(variable_select, '')}/an",
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        "Tendance totale",
                        f"{tendance_totale:+.2f} {UNITS.get(variable_select, '')}",
                        delta=f"sur {df_yearly['annee'].max() - df_yearly['annee'].min()} ans"
                    )
                
                with col3:
                    variation_pct = (tendance_totale / df_yearly[variable_select].mean() * 100) if df_yearly[variable_select].mean() != 0 else 0
                    st.metric(
                        "Variation",
                        f"{variation_pct:+.1f}%",
                        delta="par rapport à la moyenne"
                    )
                
                # Interprétation
                st.markdown("---")
                st.markdown("#### 🔍 Interprétation")
                
                if abs(tendance_an) < 0.01:
                    st.success("✅ **Tendance stable**:  Pas de changement significatif sur la période")
                elif tendance_an > 0:
                    st.warning(f"📈 **Tendance à la hausse**: Augmentation de {abs(tendance_an):.3f} {UNITS.get(variable_select, '')}/an")
                else:
                    st.info(f"📉 **Tendance à la baisse**: Diminution de {abs(tendance_an):.3f} {UNITS.get(variable_select, '')}/an")
        
        with subtab4:
            st.markdown("#### Exporter les Données")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Export données filtrées
                csv_data = df.to_csv(index=False, sep=';').encode('utf-8')
                st.download_button(
                    label="📥 Télécharger données brutes (CSV)",
                    data=csv_data,
                    file_name=f"temperature_analyse_{periode_affichage}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Export statistiques
                if stats:
                    stats_df = pd.DataFrame(list(stats.items()), columns=['Statistique', 'Valeur'])
                    csv_stats = stats_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📊 Télécharger statistiques (CSV)",
                        data=csv_stats,
                        file_name=f"statistiques_temperature_{periode_affichage}.csv",
                        mime="text/csv"
                    )
    
    # ==================== FOOTER ====================
    
    st.markdown("---")
    st.caption(f"""
    🌡️ Analyse des Températures | {periode_affichage} | {zone_affichage} |
    {df['NUM_POSTE'].nunique()} stations | {len(df):,} mesures
    """)

if __name__ == "__main__": 
    main()