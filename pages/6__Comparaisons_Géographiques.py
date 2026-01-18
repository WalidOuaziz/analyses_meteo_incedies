"""
Page de comparaison géographique - Données météorologiques
Comparaison multi-stations et multi-variables
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
from utils.styles import get_page_style
from utils.loading import display_chart

# ==================== CONFIGURATION PAGE ====================

st.set_page_config(
    page_title="Comparaison Géographique - Météo France",
    page_icon="🗺️",
    layout="wide"
)

# Appliquer le style
st.markdown(get_page_style(), unsafe_allow_html=True)

# ==================== CACHE SESSION ====================

@st.cache_data(ttl=3600)
def load_data_optimized(years=None, stations=None):
    """Charge les données optimisées pour cette page"""
    # Charger seulement les colonnes nécessaires
    essential_cols = ['NUM_POSTE', 'NOM_USUEL', 'LAT', 'LON', 'ALTI', 'AAAAMMJJ',
                     'TN', 'TX', 'TM', 'RR', 'FFM', 'FXY', 'DXY']
    
    with st.spinner('⏳ Chargement optimisé...'):
        df = load_data("data/raw/meteo.parquet", columns=essential_cols, years=years)
        
        # Filtrer par stations si spécifié
        if stations:
            df = df[df['NOM_USUEL'].isin(stations)]
        
        return df

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

def create_comparison_stations_line(df, stations, variable, periode_affichage):
    """Comparaison des stations par ligne (OPTIMISÉ)"""
    if variable not in df.columns or 'annee' not in df.columns:
        return None
    
    df_filtered = df[df['NOM_USUEL'].isin(stations)].copy()
    
    # Agrégation par année pour réduire les points
    df_yearly = df_filtered.groupby(['annee', 'NOM_USUEL'])[variable].mean().reset_index()
    
    # Limiter le nombre de stations si trop nombreuses
    if len(stations) > 10:
        top_stations = df_yearly.groupby('NOM_USUEL')[variable].mean().nlargest(10).index
        df_yearly = df_yearly[df_yearly['NOM_USUEL'].isin(top_stations)]
        st.info(f"ℹ️ Affichage des 10 stations avec les valeurs les plus élevées")
    
    fig = px.line(
        df_yearly,
        x='annee',
        y=variable,
        color='NOM_USUEL',
        title=f'Comparaison des Stations - {COLUMN_DESCRIPTIONS.get(variable, variable)} ({periode_affichage})',
        labels={
            'annee': 'Année',
            variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})',
            'NOM_USUEL': 'Station'
        },
        markers=True,
        render_mode='webgl'  # Accélération GPU
    )
    
    fig.update_layout(
        height=500, 
        hovermode='x unified', 
        template='plotly_white',
        showlegend=True,
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
    )
    fig.layout.transition = {'duration': 0}  # Désactiver animations
    
    return fig


def create_comparison_stations_bar(df, stations, variable):
    """Comparaison des stations par barres (moyenne globale)"""
    if variable not in df.columns:
        return None
    
    df_filtered = df[df['NOM_USUEL'].isin(stations)].copy()
    df_stats = df_filtered.groupby('NOM_USUEL')[variable].mean().reset_index().sort_values(variable, ascending=False)
    
    fig = px.bar(
        df_stats,
        x='NOM_USUEL',
        y=variable,
        title=f'Moyenne par Station - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        labels={
            'NOM_USUEL': 'Station',
            variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})'
        },
        color=variable,
        color_continuous_scale='Viridis'
    )
    
    fig.update_xaxes(tickangle=45)
    fig.update_layout(height=500, template='plotly_white', showlegend=False)
    
    return fig


def create_comparison_boxplot(df, stations, variable):
    """Comparaison des distributions par station (boxplot)"""
    if variable not in df.columns:
        return None
    
    df_filtered = df[df['NOM_USUEL'].isin(stations)].copy()
    
    fig = px.box(
        df_filtered,
        x='NOM_USUEL',
        y=variable,
        title=f'Distribution par Station - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        labels={
            'NOM_USUEL': 'Station',
            variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})'
        },
        color='NOM_USUEL',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_xaxes(tickangle=45)
    fig.update_layout(height=500, template='plotly_white', showlegend=False)
    
    return fig


def create_scatter_altitude_vs_variable(df, stations, variable):
    """Graphique:  altitude vs variable"""
    if variable not in df.columns or 'ALTI' not in df.columns:
        return None
    
    df_filtered = df[df['NOM_USUEL'].isin(stations)].copy()
    df_stats = df_filtered.groupby(['NOM_USUEL', 'ALTI'])[variable].mean().reset_index()
    
    fig = px.scatter(
        df_stats,
        x='ALTI',
        y=variable,
        hover_data=['NOM_USUEL'],
        title=f'Influence de l\'Altitude - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        labels={
            'ALTI':  'Altitude (m)',
            variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})'
        },
        size_max=15,
        color_discrete_sequence=['#3498db']
    )
    
    # Ajouter ligne de tendance
    z = np.polyfit(df_stats['ALTI'], df_stats[variable], 1)
    p = np.poly1d(z)
    fig.add_scatter(
        x=df_stats['ALTI'].sort_values(),
        y=p(df_stats['ALTI'].sort_values()),
        mode='lines',
        name='Tendance',
        line=dict(color='red', dash='dash')
    )
    
    fig.update_layout(height=500, template='plotly_white')
    
    return fig


def create_heatmap_stations_months(df, stations, variable):
    """Heatmap:  stations x mois"""
    if variable not in df.columns or 'mois' not in df.columns:
        return None
    
    df_filtered = df[df['NOM_USUEL'].isin(stations)].copy()
    df_pivot = df_filtered.groupby(['NOM_USUEL', 'mois'])[variable].mean().reset_index()
    df_pivot = df_pivot.pivot(index='NOM_USUEL', columns='mois', values=variable)
    
    fig = go.Figure(data=go.Heatmap(
        z=df_pivot.values,
        x=['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
        y=df_pivot.index,
        colorscale='RdYlBu_r' if variable in ['TN', 'TX', 'TM'] else 'Viridis',
        colorbar=dict(title=UNITS.get(variable, '')),
        hoverongaps=False,
        hovertemplate='Station: %{y}<br>Mois: %{x}<br>Valeur: %{z:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f'Cycle Annuel par Station - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        xaxis_title='Mois',
        yaxis_title='Station',
        height=400 + len(stations) * 20,
        template='plotly_white'
    )
    
    return fig


def create_multi_variables_comparison(df, stations, variables, periode_affichage):
    """Comparaison de plusieurs variables pour une station"""
    if not stations or not variables:
        return None
    
    # Prendre la première station si plusieurs sont sélectionnées
    station = stations[0]
    
    df_filtered = df[df['NOM_USUEL'] == station].copy()
    variables_dispo = [v for v in variables if v in df_filtered.columns]
    
    if len(variables_dispo) < 2:
        return None
    
    df_yearly = df_filtered.groupby('annee')[variables_dispo].mean().reset_index()
    
    fig = make_subplots(
        rows=len(variables_dispo),
        cols=1,
        subplot_titles=[f'{COLUMN_DESCRIPTIONS.get(v, v)} ({UNITS.get(v, "")})' for v in variables_dispo],
        specs=[[{"secondary_y": False}] for _ in variables_dispo]
    )
    
    colors = px.colors.qualitative.Plotly
    
    for idx, var in enumerate(variables_dispo, 1):
        fig.add_trace(
            go.Scatter(
                x=df_yearly['annee'],
                y=df_yearly[var],
                name=COLUMN_DESCRIPTIONS.get(var, var),
                mode='lines+markers',
                line=dict(color=colors[idx-1], width=2),
                marker=dict(size=4)
            ),
            row=idx, col=1
        )
        
        fig.update_yaxes(
            title_text=f'{COLUMN_DESCRIPTIONS.get(var, var)} ({UNITS.get(var, "")})',
            row=idx, col=1
        )
    
    fig.update_xaxes(title_text='Année', row=len(variables_dispo), col=1)
    
    fig.update_layout(
        title=f'Comparaison Multi-Variables - {station} ({periode_affichage})',
        height=300 * len(variables_dispo),
        template='plotly_white',
        hovermode='x unified',
        showlegend=True
    )
    
    return fig


def create_radar_stations(df, stations, variable):
    """Graphique radar:  comparaison par mois"""
    if variable not in df.columns or 'mois' not in df.columns:
        return None
    
    df_filtered = df[df['NOM_USUEL'].isin(stations)].copy()
    
    # Prendre max 6 stations pour clarté
    if len(stations) > 6:
        st.warning(f"⚠️ Affichage limité à 6 stations sur {len(stations)} pour clarté")
        stations = stations[: 6]
    
    fig = go.Figure()
    
    for station in stations:
        df_station = df_filtered[df_filtered['NOM_USUEL'] == station]
        monthly_data = df_station.groupby('mois')[variable].mean()
        
        fig.add_trace(go.Scatterpolar(
            r=monthly_data.values,
            theta=['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'],
            fill='toself',
            name=station,
            opacity=0.7
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, df_filtered[variable].max()])),
        title=f'Comparaison Radar par Mois - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        height=600,
        template='plotly_white',
        hovermode='closest'
    )
    
    return fig


def create_latitude_longitude_map(df, stations, variable):
    """Carte géographique avec couleurs selon la variable"""
    if variable not in df.columns or 'LAT' not in df.columns or 'LON' not in df.columns:
        return None
    
    df_filtered = df[df['NOM_USUEL'].isin(stations)].copy()
    df_map = df_filtered.groupby(['NOM_USUEL', 'LAT', 'LON'])[variable].mean().reset_index()
    
    fig = px.scatter_geo(
        df_map,
        lat='LAT',
        lon='LON',
        color=variable,
        hover_name='NOM_USUEL',
        hover_data={variable: ':.2f', 'LAT': ':.4f', 'LON': ':.4f'},
        title=f'Localisation des Stations - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        color_continuous_scale='Viridis',
        size_max=20,
        scope='europe',
        labels={variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})'}
    )
    
    fig.update_layout(height=600, template='plotly_white')
    
    return fig


def create_latitude_vs_variable(df, stations, variable):
    """Graphique: latitude vs variable"""
    if variable not in df.columns or 'LAT' not in df.columns:
        return None
    
    df_filtered = df[df['NOM_USUEL'].isin(stations)].copy()
    df_stats = df_filtered.groupby(['NOM_USUEL', 'LAT'])[variable].mean().reset_index()
    
    fig = px.scatter(
        df_stats,
        x='LAT',
        y=variable,
        hover_data=['NOM_USUEL'],
        title=f'Influence de la Latitude - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        labels={
            'LAT': 'Latitude (°N)',
            variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})'
        },
        size_max=15,
        color_discrete_sequence=['#e74c3c']
    )
    
    # Ajouter ligne de tendance
    z = np.polyfit(df_stats['LAT'], df_stats[variable], 1)
    p = np.poly1d(z)
    fig.add_scatter(
        x=df_stats['LAT'].sort_values(),
        y=p(df_stats['LAT'].sort_values()),
        mode='lines',
        name='Tendance',
        line=dict(color='blue', dash='dash')
    )
    
    fig.update_layout(height=500, template='plotly_white')
    
    return fig


def create_longitude_vs_variable(df, stations, variable):
    """Graphique: longitude vs variable"""
    if variable not in df.columns or 'LON' not in df.columns:
        return None
    
    df_filtered = df[df['NOM_USUEL'].isin(stations)].copy()
    df_stats = df_filtered.groupby(['NOM_USUEL', 'LON'])[variable].mean().reset_index()
    
    fig = px.scatter(
        df_stats,
        x='LON',
        y=variable,
        hover_data=['NOM_USUEL'],
        title=f'Influence de la Longitude - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        labels={
            'LON': 'Longitude (°E)',
            variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})'
        },
        size_max=15,
        color_discrete_sequence=['#2ecc71']
    )
    
    # Ajouter ligne de tendance
    z = np.polyfit(df_stats['LON'], df_stats[variable], 1)
    p = np.poly1d(z)
    fig.add_scatter(
        x=df_stats['LON'].sort_values(),
        y=p(df_stats['LON'].sort_values()),
        mode='lines',
        name='Tendance',
        line=dict(color='red', dash='dash')
    )
    
    fig.update_layout(height=500, template='plotly_white')
    
    return fig


def calculate_comparison_statistics(df, stations, variable):
    """Calcule les statistiques par station"""
    if variable not in df.columns:
        return None
    
    df_filtered = df[df['NOM_USUEL'].isin(stations)].copy()
    
    stats_by_station = df_filtered.groupby('NOM_USUEL')[variable].agg([
        ('Moyenne', 'mean'),
        ('Médiane', 'median'),
        ('Écart-type', 'std'),
        ('Min', 'min'),
        ('Max', 'max'),
        ('Étendue', lambda x: x.max() - x.min())
    ]).reset_index()
    
    return stats_by_station.sort_values('Moyenne', ascending=False)


# ==================== INTERFACE PRINCIPALE ====================

def main():
    st.title("🗺️ Comparaison Géographique")
    st.markdown("**Analyse comparative multi-stations et multi-variables**")
    
    # ==================== MODE PERFORMANCE ====================
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Performance")
    
    perf_mode = st.sidebar.toggle("Mode Rapide", value=True, help="Charge 5 dernières années au lieu de toutes")
    
    if perf_mode:
        default_years = list(range(2018, 2024))  # 2018-2023
        st.sidebar.success("✅ Mode rapide: 2018-2023")
    else:
        default_years = None
        st.sidebar.warning("⚠️ Toutes les années (lent)")
    
    # ==================== CHARGEMENT DONNÉES ====================
    
    df_full = load_data_optimized(years=default_years)
    
    if df_full.empty:
        st.error("❌ Impossible de charger les données")
        st.stop()
    
    # Extraction des années disponibles
    annee_min = int(df_full['annee'].min())
    annee_max = int(df_full['annee'].max())
    
    # Info performance
    st.caption(f"📊 {len(df_full):,} lignes chargées | Période: {annee_min}-{annee_max}")
    
    # ==================== FILTRES ====================
    
    st.markdown("---")
    st.subheader("🎛️ Configuration de la Comparaison")
    
    filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 2])
    
    with filter_col1:
        st.markdown("##### 📅 Période")
        
        mode_periode = st.radio(
            "Mode",
            options=['Toute la période', 'Plage personnalisée'],
            horizontal=False,
            key="periode_comp"
        )
        
        if mode_periode == 'Plage personnalisée':
            col_a, col_b = st.columns(2)
            with col_a:
                annee_debut = st.slider(
                    "Année de début",
                    min_value=annee_min,
                    max_value=annee_max,
                    value=annee_min,
                    step=1,
                    key="debut_comp"
                )
            with col_b:
                annee_fin = st.slider(
                    "Année de fin",
                    min_value=annee_debut,
                    max_value=annee_max,
                    value=annee_max,
                    step=1,
                    key="fin_comp"
                )
            
            periode_affichage = f"{annee_debut}-{annee_fin}"
            df = df_full[(df_full['annee'] >= annee_debut) & (df_full['annee'] <= annee_fin)].copy()
        else:
            periode_affichage = f"{annee_min}-{annee_max}"
            df = df_full.copy()
    
    with filter_col2:
        st.markdown("##### 📍 Sélection des Stations")
        
        selection_mode = st.radio(
            "Choisir les stations",
            options=['Région PACA', 'Stations spécifiques', 'Toute la France'],
            horizontal=False,
            key="selection_mode"
        )
        
        if selection_mode == 'Région PACA':
            stations_dispo = sorted([
                s for s in STATIONS_PACA 
                if s.upper() in df['NOM_USUEL'].str.upper().values
            ])
            stations_select = st.multiselect(
                "Stations PACA",
                options=stations_dispo,
                default=stations_dispo[: 5] if len(stations_dispo) >= 5 else stations_dispo,
                key="stations_paca"
            )
        elif selection_mode == 'Stations spécifiques':
            toutes_stations = sorted(df['NOM_USUEL'].unique().tolist())
            stations_select = st.multiselect(
                "Sélectionnez les stations",
                options=toutes_stations,
                default=toutes_stations[: 5],
                key="stations_spec"
            )
        else:
            stations_dispo = sorted(df['NOM_USUEL'].unique().tolist())
            # Limiter à 10 pour performance
            if len(stations_dispo) > 10:
                st.info(f"ℹ️ {len(stations_dispo)} stations disponibles. Affichage limité à 10 premières.")
                stations_select = stations_dispo[:10]
            else: 
                stations_select = stations_dispo
        
        if not stations_select:
            st.warning("⚠️ Sélectionnez au least une station")
            st.stop()
    
    with filter_col3:
        st.markdown("##### 📊 Variables")
        
        variables_dispo = {
            'TN': '🌡️ T. Min',
            'TX': '🌡️ T.Max',
            'TM': '🌡️ T.Moy',
            'RR': '🌧️ Précipitations',
            'FFM': '💨 Vitesse Vent Moy',
            'FXY': '💨 Rafales Max'
        }
        
        variables_dict = {k: v for k, v in variables_dispo.items() if k in df.columns}
        
        variable_select = st.selectbox(
            "Variable principale",
            options=list(variables_dict.keys()),
            format_func=lambda x: variables_dict[x],
            key="var_comp"
        )
    
    st.markdown("---")
    
    if df.empty or not stations_select:
        st.warning("⚠️ Aucune donnée disponible")
        st.stop()
    
    # Filtrer les données
    df = df[df['NOM_USUEL'].isin(stations_select)].copy()
    
    # ==================== STATISTIQUES COMPARATIVES ====================
    
    st.subheader(f"📊 Statistiques Comparatives - {periode_affichage}")
    
    stats_df = calculate_comparison_statistics(df, stations_select, variable_select)
    
    if stats_df is not None:
        st.dataframe(
            stats_df.style.format({
                'Moyenne': '{:.2f}',
                'Médiane': '{:.2f}',
                'Écart-type': '{:.2f}',
                'Min':  '{:.2f}',
                'Max': '{:.2f}',
                'Étendue': '{:.2f}'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown("---")
    
    # ==================== VISUALISATIONS ====================
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Comparaison Temporelle",
        "📊 Distributions",
        "🗺️ Géographie",
        "📐 Gradients",
        "🎯 Multi-Variables"
    ])
    
    with tab1:
        st.subheader("Comparaison Temporelle des Stations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Évolution Annuelle")
            fig_line = create_comparison_stations_line(df, stations_select, variable_select, periode_affichage)
            if fig_line:
                st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            st.markdown("#### Moyennes par Station")
            fig_bar = create_comparison_stations_bar(df, stations_select, variable_select)
            if fig_bar: 
                st.plotly_chart(fig_bar, use_container_width=True)
    
    with tab2:
        st.subheader("Distributions par Station")
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown("#### Boîte à Moustaches")
            fig_box = create_comparison_boxplot(df, stations_select, variable_select)
            if fig_box:
                st.plotly_chart(fig_box, use_container_width=True)
        
        with col2:
            st.markdown("#### Cycle Annuel")
            fig_heatmap = create_heatmap_stations_months(df, stations_select, variable_select)
            if fig_heatmap:
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("#### Graphique Radar")
        fig_radar = create_radar_stations(df, stations_select, variable_select)
        if fig_radar:
            st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab3:
        st.subheader("🗺️ Analyse Géographique")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Carte des Stations")
            fig_map = create_latitude_longitude_map(df, stations_select, variable_select)
            if fig_map:
                st.plotly_chart(fig_map, use_container_width=True)
        
        with col2:
            st.markdown("#### Infos Géographiques")
            
            df_geo = df.groupby('NOM_USUEL').agg({
                'LAT':  'first',
                'LON': 'first',
                'ALTI': 'first'
            }).reset_index()
            
            st.dataframe(
                df_geo.style.format({
                    'LAT': '{:.4f}',
                    'LON':  '{:.4f}',
                    'ALTI': '{:.0f}'
                }),
                use_container_width=True,
                hide_index=True
            )
    
    with tab4:
        st.subheader("📐 Analyse des Gradients Géographiques")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Influence Altitude")
            fig_alt = create_scatter_altitude_vs_variable(df, stations_select, variable_select)
            if fig_alt:
                st.plotly_chart(fig_alt, use_container_width=True)
        
        with col2:
            st.markdown("#### Influence Latitude")
            fig_lat = create_latitude_vs_variable(df, stations_select, variable_select)
            if fig_lat:
                st.plotly_chart(fig_lat, use_container_width=True)
        
        with col3:
            st.markdown("#### Influence Longitude")
            fig_lon = create_longitude_vs_variable(df, stations_select, variable_select)
            if fig_lon:
                st.plotly_chart(fig_lon, use_container_width=True)
        
        st.markdown("---")
        
        # Calculer les corrélations
        st.markdown("#### 📊 Corrélations")
        
        df_corr = df.groupby('NOM_USUEL').agg({
            'LAT': 'first',
            'LON': 'first',
            'ALTI': 'first',
            variable_select: 'mean'
        }).reset_index()
        
        if len(df_corr) > 2:
            corr_lat = df_corr[['LAT', variable_select]].corr().iloc[0, 1]
            corr_lon = df_corr[['LON', variable_select]].corr().iloc[0, 1]
            corr_alt = df_corr[['ALTI', variable_select]].corr().iloc[0, 1]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Corrélation Latitude",
                    f"{corr_lat:.3f}",
                    delta="forte" if abs(corr_lat) > 0.7 else "modérée" if abs(corr_lat) > 0.3 else "faible"
                )
            
            with col2:
                st.metric(
                    "Corrélation Longitude",
                    f"{corr_lon:.3f}",
                    delta="forte" if abs(corr_lon) > 0.7 else "modérée" if abs(corr_lon) > 0.3 else "faible"
                )
            
            with col3:
                st.metric(
                    "Corrélation Altitude",
                    f"{corr_alt:.3f}",
                    delta="forte" if abs(corr_alt) > 0.7 else "modérée" if abs(corr_alt) > 0.3 else "faible"
                )
    
    with tab5:
        st.subheader("🎯 Comparaison Multi-Variables")
        
        st.markdown("##### Sélectionnez les variables à comparer")
        
        variables_options = list(variables_dict.keys())
        variables_multi = st.multiselect(
            "Variables",
            options=variables_options,
            default=[variables_options[0], variables_options[1]] if len(variables_options) > 1 else variables_options,
            key="multi_var"
        )
        
        if variables_multi and len(variables_multi) > 1:
            st.markdown("##### Sélectionnez une station")
            
            station_multi = st.selectbox(
                "Station",
                options=stations_select,
                key="station_multi"
            )
            
            fig_multi = create_multi_variables_comparison(df, [station_multi], variables_multi, periode_affichage)
            if fig_multi:
                st.plotly_chart(fig_multi, use_container_width=True)
            else:
                st.warning("⚠️ Impossible de créer la comparaison multi-variables")
        else:
            st.info("ℹ️ Sélectionnez au moins 2 variables")
    
    # ==================== EXPORT ====================
    
    st.markdown("---")
    with st.expander("📥 Exporter les Données"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Export données filtrées
            csv_data = df.to_csv(index=False, sep=';').encode('utf-8')
            st.download_button(
                label="📥 Données brutes (CSV)",
                data=csv_data,
                file_name=f"comparaison_geo_{periode_affichage}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Export statistiques
            if stats_df is not None:
                csv_stats = stats_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📊 Statistiques (CSV)",
                    data=csv_stats,
                    file_name=f"stats_comparaison_{periode_affichage}.csv",
                    mime="text/csv"
                )
    
    # ==================== FOOTER ====================
    
    st.markdown("---")
    st.caption(f"""
    🗺️ Comparaison Géographique | {periode_affichage} | 
    {len(stations_select)} stations | {len(df):,} mesures
    """)

if __name__ == "__main__":
    main()