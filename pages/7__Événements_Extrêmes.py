"""
Page d'analyse des événements météorologiques extrêmes
Détection et visualisation des phénomènes extrêmes (1956-2023)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

# Imports des modules utils
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_data
from utils.constants import COLUMN_DESCRIPTIONS, UNITS

# ==================== CONFIGURATION PAGE ====================

st.set_page_config(
    page_title="Événements Extrêmes - Météo France",
    page_icon="🌪️",
    layout="wide"
)

# ==================== CACHE SESSION ====================

@st.cache_resource
def load_data_cached():
    """Charge les données une seule fois et les met en cache"""
    return load_data("data/raw/meteo.csv")

# ==================== DÉFINITION DES SEUILS ====================

THRESHOLDS = {
    'TX':  {
        'extrême_chaud': 38.0,
        'très_chaud': 32.0,
        'normal_haut': 20.0
    },
    'TN': {
        'extrême_froid': -15.0,
        'très_froid': -5.0,
        'gel': 0.0
    },
    'RR': {
        'déluge': 100.0,
        'forte_pluie': 50.0,
        'pluie':  10.0,
        'averse': 1.0
    },
    'FFM': {
        'tempête': 17.5,  # 63 km/h
        'coup_de_vent': 10.8,  # 39 km/h
        'vent_frais': 5.4  # 19 km/h
    },
    'FXY': {
        'tempête_violente': 25.0,  # 90 km/h
        'tempête':  17.5,  # 63 km/h
        'coup_de_vent': 10.8  # 39 km/h
    }
}

COLORS_EXTREMES = {
    'extrême':  '#8B0000',
    'très_grave': '#DC143C',
    'grave':  '#FF4500',
    'modéré': '#FFD700',
    'normal': '#90EE90'
}

# ==================== FONCTIONS DE DÉTECTION ====================

def classify_value(value, variable):
    """Classifie une valeur selon les seuils extrêmes"""
    if pd.isna(value) or variable not in THRESHOLDS: 
        return 'normal', 'gray'
    
    thresholds = THRESHOLDS[variable]
    
    if variable in ['TX', 'FFM', 'FXY']: 
        # Croissant (plus haute = plus extrême)
        if value >= thresholds.get('extrême_chaud', thresholds.get('tempête_violente', float('inf'))):
            return 'extrême', COLORS_EXTREMES['extrême']
        elif value >= thresholds.get('très_chaud', thresholds.get('tempête', float('inf'))):
            return 'très_grave', COLORS_EXTREMES['très_grave']
        elif value >= thresholds.get('coup_de_vent', float('inf')):
            return 'grave', COLORS_EXTREMES['grave']
        else:
            return 'normal', COLORS_EXTREMES['normal']
    
    elif variable == 'TN':
        # Décroissant (plus basse = plus extrême)
        if value <= thresholds.get('extrême_froid', float('-inf')):
            return 'extrême', COLORS_EXTREMES['extrême']
        elif value <= thresholds.get('très_froid', float('-inf')):
            return 'très_grave', COLORS_EXTREMES['très_grave']
        elif value <= thresholds.get('gel', float('-inf')):
            return 'grave', COLORS_EXTREMES['grave']
        else:
            return 'normal', COLORS_EXTREMES['normal']
    
    elif variable == 'RR':
        # Croissant (plus pluie = plus extrême)
        if value >= thresholds.get('déluge', float('inf')):
            return 'extrême', COLORS_EXTREMES['extrême']
        elif value >= thresholds.get('forte_pluie', float('inf')):
            return 'très_grave', COLORS_EXTREMES['très_grave']
        elif value >= thresholds.get('pluie', float('inf')):
            return 'grave', COLORS_EXTREMES['grave']
        elif value >= thresholds.get('averse', 0):
            return 'modéré', COLORS_EXTREMES['modéré']
        else:
            return 'normal', COLORS_EXTREMES['normal']
    
    return 'normal', COLORS_EXTREMES['normal']


def detect_extreme_events(df, variable, threshold_level='extrême'):
    """Détecte les événements extrêmes"""
    if variable not in THRESHOLDS or variable not in df.columns:
        return pd.DataFrame()
    
    thresholds = THRESHOLDS[variable]
    
    # Définir le seuil selon le niveau
    if threshold_level == 'extrême':
        if variable in ['TX', 'FFM', 'FXY']: 
            seuil = thresholds.get('extrême_chaud', thresholds.get('tempête_violente', float('inf')))
            df_events = df[df[variable] >= seuil].copy()
        elif variable == 'TN':
            seuil = thresholds.get('extrême_froid', float('-inf'))
            df_events = df[df[variable] <= seuil].copy()
        else:
            seuil = thresholds.get('déluge', float('inf'))
            df_events = df[df[variable] >= seuil].copy()
    
    elif threshold_level == 'très_grave':
        if variable in ['TX', 'FFM', 'FXY']: 
            seuil = thresholds.get('très_chaud', thresholds.get('tempête', float('inf')))
            df_events = df[df[variable] >= seuil].copy()
        elif variable == 'TN': 
            seuil = thresholds.get('très_froid', float('-inf'))
            df_events = df[df[variable] <= seuil].copy()
        else:
            seuil = thresholds.get('forte_pluie', float('inf'))
            df_events = df[df[variable] >= seuil].copy()
    
    else: 
        return pd.DataFrame()
    
    if df_events.empty:
        return pd.DataFrame()
    
    # Ajouter la classification
    df_events['classification'] = df_events[variable].apply(
        lambda x: classify_value(x, variable)[0]
    )
    
    return df_events.sort_values(variable, ascending=False)


def create_heatwave_analysis(df):
    """Analyse les vagues de chaleur (TX > 30°C pendant 3+ jours)"""
    if 'TX' not in df.columns or 'date' not in df.columns:
        return None, None
    
    # Identifier les jours chauds (TX > 30°C)
    df_sorted = df.sort_values('date').copy()
    df_sorted['day_hot'] = df_sorted['TX'] > 30.0
    
    # Identifier les périodes de vague de chaleur
    df_sorted['group'] = (df_sorted['day_hot'] != df_sorted['day_hot'].shift()).cumsum()
    
    heatwaves = []
    for group_id, group_data in df_sorted[df_sorted['day_hot']].groupby('group'):
        if len(group_data) >= 3:  # Au moins 3 jours
            heatwaves.append({
                'date_debut': group_data['date'].min(),
                'date_fin': group_data['date'].max(),
                'durée_jours': len(group_data),
                'tx_max': group_data['TX'].max(),
                'tx_moy': group_data['TX'].mean(),
                'station': group_data['NOM_USUEL'].iloc[0] if len(group_data) > 0 else 'N/A'
            })
    
    if not heatwaves:
        return None, None
    
    df_heatwaves = pd.DataFrame(heatwaves).sort_values('tx_max', ascending=False)
    
    # Graphique
    fig = px.bar(
        df_heatwaves.head(20),
        x='date_debut',
        y='durée_jours',
        color='tx_max',
        hover_data=['station', 'tx_max', 'tx_moy'],
        title='Vagues de Chaleur (TX > 30°C pendant 3+ jours)',
        labels={
            'date_debut': 'Date de début',
            'durée_jours': 'Durée (jours)',
            'tx_max': 'TX Max (°C)'
        },
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(height=400, template='plotly_white')
    
    return df_heatwaves, fig


def create_cold_snap_analysis(df):
    """Analyse les vagues de froid (TN < 0°C pendant 3+ jours)"""
    if 'TN' not in df.columns or 'date' not in df.columns:
        return None, None
    
    df_sorted = df.sort_values('date').copy()
    df_sorted['day_cold'] = df_sorted['TN'] < 0.0
    
    df_sorted['group'] = (df_sorted['day_cold'] != df_sorted['day_cold'].shift()).cumsum()
    
    coldsnaps = []
    for group_id, group_data in df_sorted[df_sorted['day_cold']].groupby('group'):
        if len(group_data) >= 3:
            coldsnaps.append({
                'date_debut': group_data['date'].min(),
                'date_fin': group_data['date'].max(),
                'durée_jours': len(group_data),
                'tn_min': group_data['TN'].min(),
                'tn_moy': group_data['TN'].mean(),
                'station':  group_data['NOM_USUEL'].iloc[0] if len(group_data) > 0 else 'N/A'
            })
    
    if not coldsnaps:
        return None, None
    
    df_coldsnaps = pd.DataFrame(coldsnaps).sort_values('tn_min')
    
    fig = px.bar(
        df_coldsnaps.head(20),
        x='date_debut',
        y='durée_jours',
        color='tn_min',
        hover_data=['station', 'tn_min', 'tn_moy'],
        title='Vagues de Froid (TN < 0°C pendant 3+ jours)',
        labels={
            'date_debut':  'Date de début',
            'durée_jours': 'Durée (jours)',
            'tn_min':  'TN Min (°C)'
        },
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(height=400, template='plotly_white')
    
    return df_coldsnaps, fig


def create_extreme_timeline(df, variable):
    """Chronologie des événements extrêmes"""
    if variable not in df.columns or 'date' not in df.columns:
        return None
    
    df_extreme = detect_extreme_events(df, variable, 'très_grave')
    
    if df_extreme.empty:
        return None
    
    df_extreme = df_extreme.sort_values('date')
    
    fig = px.scatter(
        df_extreme,
        x='date',
        y=variable,
        color='classification',
        hover_name='NOM_USUEL',
        hover_data={'date': '|%Y-%m-%d', variable: ':.1f'},
        title=f'Chronologie des Événements Extrêmes - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        labels={
            'date':  'Date',
            variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})',
            'classification': 'Classification'
        },
        color_discrete_map={
            'extrême':  COLORS_EXTREMES['extrême'],
            'très_grave': COLORS_EXTREMES['très_grave'],
            'grave': COLORS_EXTREMES['grave'],
            'normal': COLORS_EXTREMES['normal']
        },
        size_max=12
    )
    
    fig.update_layout(height=400, template='plotly_white', hovermode='x unified')
    
    return fig


def create_frequency_analysis(df, variable, year_range=None):
    """Analyse la fréquence des événements extrêmes par année"""
    if variable not in df.columns or 'date' not in df.columns:
        return None
    
    df_sorted = df.sort_values('date').copy()
    df_sorted['annee'] = df_sorted['date'].dt.year
    
    # Compter les événements extrêmes par année
    events_by_year = []
    
    for year in sorted(df_sorted['annee'].unique()):
        df_year = df_sorted[df_sorted['annee'] == year]
        
        df_extrême = detect_extreme_events(df_year, variable, 'extrême')
        df_très_grave = detect_extreme_events(df_year, variable, 'très_grave')
        
        events_by_year.append({
            'année': year,
            'Extrêmes': len(df_extrême),
            'Très graves': len(df_très_grave),
            'Total': len(df_extrême) + len(df_très_grave)
        })
    
    df_freq = pd.DataFrame(events_by_year)
    
    if df_freq.empty:
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_freq['année'],
        y=df_freq['Extrêmes'],
        mode='lines+markers',
        name='Extrêmes',
        line=dict(color=COLORS_EXTREMES['extrême'], width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_freq['année'],
        y=df_freq['Très graves'],
        mode='lines+markers',
        name='Très graves',
        line=dict(color=COLORS_EXTREMES['très_grave'], width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title=f'Fréquence des Événements Extrêmes - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        xaxis_title='Année',
        yaxis_title='Nombre d\'événements',
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig


def create_extremes_map(df, variable):
    """Localisation des événements extrêmes"""
    if variable not in df.columns:
        return None
    
    df_extreme = detect_extreme_events(df, variable, 'très_grave')
    
    if df_extreme.empty:
        return None
    
    # Agrégér par station
    df_stations = df_extreme.groupby(['NOM_USUEL', 'LAT', 'LON']).agg({
        variable: ['count', 'max', 'mean']
    }).reset_index()
    
    df_stations.columns = ['NOM_USUEL', 'LAT', 'LON', 'nb_events', 'max_value', 'mean_value']
    
    fig = px.scatter_geo(
        df_stations,
        lat='LAT',
        lon='LON',
        size='nb_events',
        color='max_value',
        hover_name='NOM_USUEL',
        hover_data={
            'nb_events': True,
            'max_value':  ':.1f',
            'mean_value': ':.1f',
            'LAT': ':.3f',
            'LON':  ':.3f'
        },
        title=f'Localisation des Événements Extrêmes - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        color_continuous_scale='Reds',
        scope='europe'
    )
    
    fig.update_layout(height=500, template='plotly_white')
    
    return fig


def create_percentile_analysis(df, variable):
    """Analyse par percentiles"""
    if variable not in df.columns:
        return None
    
    df_valid = df.dropna(subset=[variable])
    
    if df_valid.empty:
        return None
    
    percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
    values = [df_valid[variable].quantile(p/100) for p in percentiles]
    
    fig = go.Figure(data=[
        go.Bar(
            x=[f'{p}e' for p in percentiles],
            y=values,
            marker=dict(
                color=values,
                colorscale='RdYlBu_r' if variable in ['TN', 'TX', 'TM'] else 'Blues',
                showscale=True
            ),
            text=[f'{v:.1f}' for v in values],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title=f'Analyse par Percentiles - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        xaxis_title='Percentile',
        yaxis_title=f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})',
        height=400,
        template='plotly_white'
    )
    
    return fig


# ==================== INTERFACE PRINCIPALE ====================

def main():
    st.title("🌪️ Analyse des Événements Météorologiques Extrêmes")
    st.markdown("**Détection et analyse des phénomènes extrêmes (1956-2023)**")
    
    # Chargement des données
    with st.spinner("📊 Chargement des données..."):
        df = load_data_cached()
    
    if df.empty:
        st.error("❌ Fichier CSV introuvable:   data/raw/meteo.csv")
        st.stop()
    
    # ==================== FILTRES ====================
    
    st.markdown("---")
    st.subheader("🎛️ Configuration")
    
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        st.markdown("##### 📅 Période")
        
        annee_min = int(df['annee'].min())
        annee_max = int(df['annee'].max())
        
        annees_select = st.slider(
            "Années",
            min_value=annee_min,
            max_value=annee_max,
            value=(annee_min, annee_max),
            step=1
        )
        
        df_filtered = df[(df['annee'] >= annees_select[0]) & (df['annee'] <= annees_select[1])].copy()
    
    with col2:
        st.markdown("##### 📊 Type d'Événement")
        
        event_type = st.radio(
            "Choisir",
            options=['Vagues de Chaleur', 'Vagues de Froid', 'Tempêtes', 'Précipitations Extrêmes', 'Tous les Extrêmes'],
            horizontal=False
        )
    
    with col3:
        st.markdown("##### 🌍 Localisation")
        
        show_all = st.checkbox("Afficher toutes les stations", value=True)
        
        if not show_all:
            stations = sorted(df_filtered['NOM_USUEL'].unique())
            stations_select = st.multiselect(
                "Sélectionner les stations",
                options=stations,
                default=stations[: 5]
            )
            df_filtered = df_filtered[df_filtered['NOM_USUEL'].isin(stations_select)].copy()
    
    st.markdown("---")
    
    # ==================== ANALYSE PAR TYPE ====================
    
    if event_type == 'Vagues de Chaleur':
        st.subheader("🔥 Analyse des Vagues de Chaleur")
        st.info("Une vague de chaleur est définie comme une période d'au moins 3 jours consécutifs avec TX > 30°C")
        
        df_heatwaves, fig_timeline = create_heatwave_analysis(df_filtered)
        
        if df_heatwaves is not None and fig_timeline is not None: 
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(fig_timeline, use_container_width=True)
            
            with col2:
                st.markdown("#### Statistiques")
                st.metric("Nombre de vagues", len(df_heatwaves))
                st.metric("Durée moyenne", f"{df_heatwaves['durée_jours'].mean():.1f} jours")
                st.metric("TX max observée", f"{df_heatwaves['tx_max'].max():.1f}°C")
                
                st.markdown("#### Top 10 Vagues")
                st.dataframe(
                    df_heatwaves.head(10).style.format({
                        'date_debut': lambda x: x.strftime('%Y-%m-%d'),
                        'date_fin': lambda x:  x.strftime('%Y-%m-%d'),
                        'tx_max': '{:.1f}',
                        'tx_moy': '{:.1f}'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.warning("⚠️ Aucune vague de chaleur détectée")
    
    elif event_type == 'Vagues de Froid':
        st.subheader("❄️ Analyse des Vagues de Froid")
        st.info("Une vague de froid est définie comme une période d'au moins 3 jours consécutifs avec TN < 0°C")
        
        df_coldsnaps, fig_timeline = create_cold_snap_analysis(df_filtered)
        
        if df_coldsnaps is not None and fig_timeline is not None: 
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(fig_timeline, use_container_width=True)
            
            with col2:
                st.markdown("#### Statistiques")
                st.metric("Nombre de vagues", len(df_coldsnaps))
                st.metric("Durée moyenne", f"{df_coldsnaps['durée_jours'].mean():.1f} jours")
                st.metric("TN min observée", f"{df_coldsnaps['tn_min'].min():.1f}°C")
                
                st.markdown("#### Top 10 Vagues")
                st.dataframe(
                    df_coldsnaps.head(10).style.format({
                        'date_debut':  lambda x: x.strftime('%Y-%m-%d'),
                        'date_fin': lambda x: x.strftime('%Y-%m-%d'),
                        'tn_min': '{:.1f}',
                        'tn_moy': '{:.1f}'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.warning("⚠️ Aucune vague de froid détectée")
    
    elif event_type == 'Tempêtes': 
        st.subheader("🌪️ Analyse des Tempêtes")
        st.info("Seuil:  FFM > 17.5 m/s (63 km/h) ou FXY > 25 m/s (90 km/h)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Vitesse Moyenne")
            fig1 = create_extreme_timeline(df_filtered, 'FFM')
            if fig1:
                st.plotly_chart(fig1, use_container_width=True)
            
            fig2 = create_frequency_analysis(df_filtered, 'FFM')
            if fig2:
                st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            st.markdown("#### Rafales Maximales")
            fig3 = create_extreme_timeline(df_filtered, 'FXY')
            if fig3:
                st.plotly_chart(fig3, use_container_width=True)
            
            fig4 = create_frequency_analysis(df_filtered, 'FXY')
            if fig4:
                st.plotly_chart(fig4, use_container_width=True)
    
    elif event_type == 'Précipitations Extrêmes': 
        st.subheader("🌧️ Analyse des Précipitations Extrêmes")
        st.info("Seuil extrême: RR > 100 mm | Seuil grave: RR > 50 mm")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = create_extreme_timeline(df_filtered, 'RR')
            if fig1:
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = create_frequency_analysis(df_filtered, 'RR')
            if fig2:
                st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        
        fig3 = create_extremes_map(df_filtered, 'RR')
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)
    
    else:  # Tous les extrêmes
        st.subheader("📊 Vue d'Ensemble - Tous les Extrêmes")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔥 Chaleur",
            "❄️ Froid",
            "💨 Vent",
            "💧 Pluie"
        ])
        
        with tab1:
            fig_heat_freq = create_frequency_analysis(df_filtered, 'TX')
            fig_heat_perc = create_percentile_analysis(df_filtered, 'TX')
            
            if fig_heat_freq: 
                st.plotly_chart(fig_heat_freq, use_container_width=True)
            if fig_heat_perc: 
                st.plotly_chart(fig_heat_perc, use_container_width=True)
        
        with tab2:
            fig_cold_freq = create_frequency_analysis(df_filtered, 'TN')
            fig_cold_perc = create_percentile_analysis(df_filtered, 'TN')
            
            if fig_cold_freq:
                st.plotly_chart(fig_cold_freq, use_container_width=True)
            if fig_cold_perc:
                st.plotly_chart(fig_cold_perc, use_container_width=True)
        
        with tab3:
            fig_wind_freq = create_frequency_analysis(df_filtered, 'FFM')
            fig_wind_perc = create_percentile_analysis(df_filtered, 'FFM')
            
            if fig_wind_freq:
                st.plotly_chart(fig_wind_freq, use_container_width=True)
            if fig_wind_perc: 
                st.plotly_chart(fig_wind_perc, use_container_width=True)
        
        with tab4:
            fig_rain_freq = create_frequency_analysis(df_filtered, 'RR')
            fig_rain_perc = create_percentile_analysis(df_filtered, 'RR')
            
            if fig_rain_freq:
                st.plotly_chart(fig_rain_freq, use_container_width=True)
            if fig_rain_perc: 
                st.plotly_chart(fig_rain_perc, use_container_width=True)
    
    # ==================== DONNÉES ====================
    
    st.markdown("---")
    with st.expander("📋 Voir les données détaillées"):
        
        var_select = st.selectbox(
            "Variable à afficher",
            options=['TN', 'TX', 'RR', 'FFM', 'FXY']
        )
        
        df_display = detect_extreme_events(df_filtered, var_select, 'très_grave')
        
        if not df_display.empty:
            cols = ['date', 'NOM_USUEL', var_select, 'classification']
            cols = [c for c in cols if c in df_display.columns]
            
            st.dataframe(
                df_display[cols].sort_values('date', ascending=False),
                use_container_width=True,
                height=400
            )
            
            csv = df_display[cols].to_csv(index=False, sep=';').encode('utf-8')
            st.download_button(
                "📥 Télécharger",
                csv,
                f"extremes_{var_select}.csv",
                "text/csv"
            )
        else:
            st.info("Aucun événement extrême trouvé")
    
    # ==================== FOOTER ====================
    
    st.markdown("---")
    st.caption(f"""
    🌪️ Analyse des Extrêmes | {annees_select[0]}-{annees_select[1]} |
    {df_filtered['NUM_POSTE'].nunique()} stations | {len(df_filtered):,} mesures
    """)


if __name__ == "__main__":
    main()