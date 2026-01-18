"""
Page de carte interactive des stations météo en France
Visualisation géographique avancée des données météorologiques
"""

import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Imports des modules utils
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_data
from utils.constants import COLUMN_DESCRIPTIONS, UNITS
from utils.styles import get_page_style
from utils.loading import display_map, display_chart

# ==================== CONFIGURATION PAGE ====================

st.set_page_config(
    page_title="Carte Interactive - Météo France",
    page_icon="🗺️",
    layout="wide"
)

# Appliquer le style
st.markdown(get_page_style(), unsafe_allow_html=True)

# ==================== CACHE SESSION ====================

@st.cache_resource
def load_data_cached():
    """Charge les données une seule fois et les met en cache"""
    with st.spinner('⏳ Chargement des données...'):
        return load_data("data/raw/meteo.parquet")

# ==================== FONCTIONS AUXILIAIRES ====================

def get_color_scale(value, min_val, max_val, color_type='temperature'):
    """Retourne une couleur selon la valeur et l'échelle"""
    if pd.isna(value):
        return '#808080'
    
    if max_val == min_val:
        norm_value = 0.5
    else:
        norm_value = (value - min_val) / (max_val - min_val)
        norm_value = max(0, min(1, norm_value))
    
    if color_type == 'temperature':
        if norm_value < 0.5:
            r = int(norm_value * 2 * 255)
            g = int(norm_value * 2 * 255)
            b = 255
        else:
            r = 255
            g = int(255 - (norm_value - 0.5) * 2 * 255)
            b = 0
    elif color_type == 'precipitation':
        intensity = int((1 - norm_value) * 255)
        r = intensity
        g = intensity
        b = 255
    else:
        if norm_value < 0.5:
            r = int(norm_value * 2 * 255)
            g = 255
            b = 0
        else:
            r = 255
            g = int(255 - (norm_value - 0.5) * 2 * 255)
            b = 0
    
    return f'#{r:02x}{g:02x}{b: 02x}'


def create_popup_html(row, variable, date_str):
    """Crée le contenu HTML pour le popup de la station"""
    unit = UNITS.get(variable, '')
    value = row.get(variable, 'N/A')
    
    if pd.notna(value) and isinstance(value, (int, float)):
        value_str = f"{value:.1f} {unit}"
    else: 
        value_str = "Donnée manquante"
    
    html = f"""
    <div style='font-family: Arial; width: 280px;'>
        <h4 style='margin: 0 0 10px 0; color: #2c3e50;'>📍 {row['NOM_USUEL']}</h4>
        <hr style='margin: 5px 0;'>
        <table style='width: 100%; font-size: 12px;'>
            <tr>
                <td><b>Code:</b></td>
                <td>{row['NUM_POSTE']}</td>
            </tr>
            <tr>
                <td><b>Altitude:</b></td>
                <td>{int(row['ALTI'])} m</td>
            </tr>
            <tr>
                <td><b>Lat/Lon:</b></td>
                <td>{row['LAT']:.3f} / {row['LON']:.3f}</td>
            </tr>
            <tr style='background-color: #f0f0f0;'>
                <td><b>Date:</b></td>
                <td>{date_str}</td>
            </tr>
        </table>
        <hr style='margin: 5px 0;'>
        <div style='background-color: #e8f4f8; padding:  10px; border-radius:  5px; margin-top:  10px;'>
            <p style='margin: 0; font-size: 12px; color:  #555;'>
                <b>{COLUMN_DESCRIPTIONS.get(variable, variable)}:</b>
            </p>
            <p style='margin: 5px 0 0 0; font-size:  18px; font-weight: bold; color: #2c3e50;'>
                {value_str}
            </p>
        </div>
        <hr style='margin: 10px 0 5px 0;'>
        <div style='font-size: 11px; color: #666;'>
    """
    
    if 'TN' in row and pd.notna(row['TN']):
        html += f"<div>🌡️ T. Min: {row['TN']:.1f}°C</div>"
    if 'TX' in row and pd.notna(row['TX']):
        html += f"<div>🌡️ T.Max: {row['TX']:.1f}°C</div>"
    if 'RR' in row and pd.notna(row['RR']):
        html += f"<div>🌧️ Pluie: {row['RR']:.1f} mm</div>"
    
    html += "</div></div>"
    
    return html


def create_interactive_map(df_jour, variable, center_lat=46.603354, center_lon=1.888334):
    """Crée une carte Folium interactive"""
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6,
        tiles='OpenStreetMap',
        control_scale=True,
        prefer_canvas=True
    )
    
    # Ajouter les fonds de carte
    folium.TileLayer(
        tiles='CartoDB positron',
        name='Clair',
        attr='© CartoDB',
        overlay=False
    ).add_to(m)
    
    folium.TileLayer(
        tiles='CartoDB dark_matter',
        name='Sombre',
        attr='© CartoDB',
        overlay=False
    ).add_to(m)
    
    folium.TileLayer(
        tiles='OpenTopoMap',
        name='Relief',
        attr='© OpenTopoMap',
        overlay=False
    ).add_to(m)
    
    if df_jour.empty or variable not in df_jour.columns:
        folium.LayerControl(position='topright').add_to(m)
        return m
    
    df_valid = df_jour.dropna(subset=['LAT', 'LON', variable]).copy()
    
    if df_valid.empty:
        folium.LayerControl(position='topright').add_to(m)
        return m
    
    min_val = df_valid[variable].min()
    max_val = df_valid[variable].max()
    
    if variable in ['TN', 'TX', 'TM', 'TAMPLI']:
        color_type = 'temperature'
    elif variable in ['RR', 'DRR']: 
        color_type = 'precipitation'
    else:
        color_type = 'wind'
    
    # Feature group pour les markers
    fg_markers = folium.FeatureGroup(name='Stations', show=True)
    
    date_str = df_jour['date'].iloc[0].strftime('%d/%m/%Y') if 'date' in df_jour.columns else 'N/A'
    
    for idx, row in df_valid.iterrows():
        color = get_color_scale(row[variable], min_val, max_val, color_type)
        
        popup_html = create_popup_html(row, variable, date_str)
        
        folium.CircleMarker(
            location=[row['LAT'], row['LON']],
            radius=7,
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"{row['NOM_USUEL']}:  {row[variable]:.1f}",
            color='#333',
            fillColor=color,
            fillOpacity=0.75,
            weight=1
        ).add_to(fg_markers)
    
    fg_markers.add_to(m)
    
    # Légende
    legend_html = create_legend_html(min_val, max_val, variable, color_type)
    m.get_root().html.add_child(folium.Element(legend_html))
    
    folium.LayerControl(position='topright').add_to(m)
    
    return m


def create_legend_html(min_val, max_val, variable, color_type):
    """Crée la légende HTML"""
    unit = UNITS.get(variable, '')
    var_name = COLUMN_DESCRIPTIONS.get(variable, variable)
    
    colors = []
    for i in range(10):
        val = min_val + (max_val - min_val) * i / 9
        color = get_color_scale(val, min_val, max_val, color_type)
        colors.append(color)
    
    gradient = ', '.join(colors)
    
    legend_html = f"""
    <div style="
        position: fixed; 
        bottom: 50px; 
        right: 50px; 
        width: 220px; 
        background-color: white; 
        border: 2px solid #333; 
        border-radius: 5px;
        z-index: 9999; 
        padding: 12px;
        font-family: Arial;
        box-shadow: 0 0 15px rgba(0,0,0,0.2);
    ">
        <h4 style="margin: 0 0 10px 0; font-size: 13px; color: #333;">{var_name}</h4>
        <div style="
            height: 25px; 
            background:  linear-gradient(to right, {gradient});
            border: 1px solid #999;
            border-radius: 3px;
        "></div>
        <div style="
            display: flex; 
            justify-content: space-between; 
            font-size: 11px; 
            margin-top: 8px;
            color: #555;
        ">
            <span><b>{min_val:.1f} {unit}</b></span>
            <span><b>{max_val:.1f} {unit}</b></span>
        </div>
    </div>
    """
    
    return legend_html


def create_heatmap_density(df_jour, variable):
    """Crée une carte de chaleur"""
    m = folium.Map(
        location=[46.603354, 1.888334],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    if df_jour.empty or variable not in df_jour.columns:
        return m
    
    df_valid = df_jour.dropna(subset=['LAT', 'LON', variable]).copy()
    
    if df_valid.empty:
        return m
    
    min_val = df_valid[variable].min()
    max_val = df_valid[variable].max()
    
    if max_val > min_val:
        df_valid['intensity'] = (df_valid[variable] - min_val) / (max_val - min_val)
    else:
        df_valid['intensity'] = 0.5
    
    heat_data = df_valid[['LAT', 'LON', 'intensity']].values.tolist()
    
    plugins.HeatMap(
        heat_data,
        min_opacity=0.3,
        max_zoom=13,
        radius=25,
        blur=15,
        gradient={
            0.0: 'blue',
            0.5: 'yellow',
            1.0: 'red'
        }
    ).add_to(m)
    
    return m


def create_top_stations_chart(df, variable, top_n=15):
    """Graphique des meilleures stations"""
    if df.empty or variable not in df.columns:
        return None
    
    df_sorted = df.nlargest(top_n, variable)
    
    # ✅ Utiliser px.bar avec orientation='h' au lieu de px.barh
    fig = px.bar(
        df_sorted.sort_values(variable),
        y='NOM_USUEL',
        x=variable,
        orientation='h',
        title=f'Top {top_n} Stations - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        labels={
            variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})',
            'NOM_USUEL': 'Station'
        },
        color=variable,
        color_continuous_scale='RdYlBu_r' if variable in ['TN', 'TX', 'TM'] else 'Blues'
    )
    
    fig.update_layout(height=450, showlegend=False, template='plotly_white')
    
    return fig

def create_distribution_chart(df, variable):
    """Graphique de distribution"""
    if df.empty or variable not in df.columns:
        return None
    
    df_valid = df.dropna(subset=[variable])
    
    if df_valid.empty:
        return None
    
    fig = px.histogram(
        df_valid,
        x=variable,
        nbins=40,
        title=f'Distribution - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        labels={variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})'},
        color_discrete_sequence=['#3498db'],
        marginal='box'
    )
    
    mean_val = df_valid[variable].mean()
    median_val = df_valid[variable].median()
    
    fig.add_vline(x=mean_val, line_dash="dash", line_color="red",
                  annotation_text=f"Moy: {mean_val:.1f}",
                  annotation_position="top left")
    fig.add_vline(x=median_val, line_dash="dot", line_color="green",
                  annotation_text=f"Méd: {median_val:.1f}",
                  annotation_position="top right")
    
    fig.update_layout(height=400, showlegend=False, template='plotly_white')
    
    return fig


def create_altitude_analysis(df, variable):
    """Analyse influence altitude"""
    if df.empty or variable not in df.columns or 'ALTI' not in df.columns:
        return None
    
    df_valid = df.dropna(subset=['LAT', 'LON', 'ALTI', variable])
    
    if df_valid.empty:
        return None
    
    fig = px.scatter(
        df_valid,
        x='ALTI',
        y=variable,
        hover_name='NOM_USUEL',
        title=f'Relation Altitude - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        labels={
            'ALTI': 'Altitude (m)',
            variable: f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})'
        },
        color=variable,
        size_max=10,
        color_continuous_scale='Viridis'
    )
    
    # Ajouter ligne de tendance
    z = np.polyfit(df_valid['ALTI'], df_valid[variable], 1)
    p = np.poly1d(z)
    x_trend = np.array([df_valid['ALTI'].min(), df_valid['ALTI'].max()])
    
    fig.add_scatter(
        x=x_trend,
        y=p(x_trend),
        mode='lines',
        name='Tendance',
        line=dict(color='red', width=3, dash='dash')
    )
    
    fig.update_layout(height=400, template='plotly_white')
    
    return fig


def create_temporal_comparison(df, variable, date_ref):
    """Graphique comparaison temporelle"""
    if df.empty or variable not in df.columns or 'date' not in df.columns:
        return None
    
    # ✅ Convertir date_ref en datetime64
    date_ref = pd.to_datetime(date_ref)
    
    # Données pour 7 jours autour de la date
    start_date = date_ref - timedelta(days=3)
    end_date = date_ref + timedelta(days=3)
    
    df_range = df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()
    
    if df_range.empty:
        return None
    
    df_daily = df_range.groupby('date')[variable].agg(['mean', 'min', 'max']).reset_index()
    
    fig = go.Figure()
    
    # Zone min-max
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['max'],
        fill=None,
        mode='lines',
        name='Max',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['min'],
        fill='tonexty',
        mode='lines',
        name='Plage',
        line=dict(color='rgba(0,0,0,0)'),
        fillcolor='rgba(52, 152, 219, 0.2)'
    ))
    
    # Ligne moyenne
    fig.add_trace(go.Scatter(
        x=df_daily['date'],
        y=df_daily['mean'],
        mode='lines+markers',
        name='Moyenne',
        line=dict(color='#3498db', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=f'Évolution 7j - {COLUMN_DESCRIPTIONS.get(variable, variable)}',
        xaxis_title='Date',
        yaxis_title=f'{COLUMN_DESCRIPTIONS.get(variable, variable)} ({UNITS.get(variable, "")})',
        height=350,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig

# ==================== INTERFACE PRINCIPALE ====================

def main():
    st.title("🗺️ Carte Interactive des Stations Météo")
    st.markdown("Visualisez les données météorologiques en temps réel sur la carte interactive")
    
    # ==================== CHARGEMENT DONNÉES ====================
    
    with st.spinner("📊 Chargement des données..."):
        df_full = load_data_cached()
    
    if df_full.empty:
        st.error("❌ Fichier CSV introuvable:  data/raw/meteo. csv")
        st.stop()
    
    # ==================== FILTRES PRINCIPAUX (Top) ====================
    
    st.markdown("---")
    st.subheader("🎛️ Sélection des Données")
    
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1.5, 1.5, 1])
    
    with filter_col1:
        st.markdown("##### 📅 Année et Date")
        
        annee_min = df_full['annee'].min()
        annee_max = df_full['annee'].max()
        
        annee_selectionnee = st.slider(
            "Année",
            min_value=int(annee_min),
            max_value=int(annee_max),
            value=int(annee_max),
            step=1
        )
        
        # Filtrer par année
        df_annee = df_full[df_full['annee'] == annee_selectionnee].copy()
        
        date_min = df_annee['date'].min().date()
        date_max = df_annee['date'].max().date()
        
        date_selectionnee = st.date_input(
            "Date",
            value=date_max,
            min_value=date_min,
            max_value=date_max
        )
    
    with filter_col2:
        st.markdown("##### 📊 Variable")
        
        variables_dispo = {
            'TN': '🌡️ T. Min',
            'TX': '🌡️ T.Max',
            'TM': '🌡️ T.Moy',
            'TAMPLI': '📏 Amplitude',
            'RR': '🌧️ Pluie',
            'FFM': '💨 Vent Moy',
            'FXY': '💨 Rafales Max'
        }
        
        variables_dict = {k: v for k, v in variables_dispo.items() if k in df_annee.columns}
        
        variable_selectionnee = st.selectbox(
            "Choisir la variable",
            options=list(variables_dict.keys()),
            format_func=lambda x: variables_dict[x]
        )
    
    with filter_col3:
        st.markdown("##### 🎨 Mode Affichage")
        
        type_viz = st.radio(
            "Type de carte",
            options=['Heatmap','Markers','Hybride'],
            horizontal=True
        )
    
    with filter_col4:
        st.markdown("##### ⛰️ Altitude")
        
        alt_min = int(df_annee['ALTI'].min())
        alt_max = int(df_annee['ALTI'].max())
        
        altitude_min = st.number_input(
            "Min (m)",
            min_value=alt_min,
            max_value=alt_max,
            value=alt_min,
            step=100
        )
        
        altitude_max = st.number_input(
            "Max (m)",
            min_value=altitude_min,
            max_value=alt_max,
            value=alt_max,
            step=100
        )
    
    st.markdown("---")
    
    # ==================== FILTRAGE DONNÉES ====================
    
    df_jour = df_annee[df_annee['date'] == pd.to_datetime(date_selectionnee)].copy()
    df_jour = df_jour[(df_jour['ALTI'] >= altitude_min) & (df_jour['ALTI'] <= altitude_max)].copy()
    
    if df_jour.empty:
        st.warning("⚠️ Aucune donnée pour cette sélection")
        st.stop()
    
    # ==================== STATISTIQUES ====================
    
    st.subheader("📊 Vue d'Ensemble")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📍 Stations", f"{df_jour['NUM_POSTE'].nunique():,}")
    
    with col2:
        if variable_selectionnee in df_jour.columns:
            val_moy = df_jour[variable_selectionnee].mean()
            st.metric("📊 Moyenne", f"{val_moy:.1f} {UNITS.get(variable_selectionnee, '')}")
    
    with col3:
        if variable_selectionnee in df_jour.columns:
            val_min = df_jour[variable_selectionnee].min()
            st.metric("📉 Min", f"{val_min:.1f} {UNITS.get(variable_selectionnee, '')}")
    
    with col4:
        if variable_selectionnee in df_jour.columns:
            val_max = df_jour[variable_selectionnee].max()
            st.metric("📈 Max", f"{val_max:.1f} {UNITS.get(variable_selectionnee, '')}")
    
    with col5:
        if variable_selectionnee in df_jour.columns:
            val_std = df_jour[variable_selectionnee].std()
            st.metric("📊 Écart-type", f"{val_std:.1f}")
    
    st.markdown("---")
    
    # ==================== CARTE INTERACTIVE ====================
    
    st.subheader(f"🗺️ Carte - {date_selectionnee.strftime('%d/%m/%Y')}")
    
    with st.spinner("🗺️ Génération de la carte..."):
        if type_viz == 'Heatmap':
            carte = create_heatmap_density(df_jour, variable_selectionnee)
        elif type_viz == 'Hybride':
            # Créer une carte combinée
            carte = create_interactive_map(df_jour, variable_selectionnee)
            df_valid = df_jour.dropna(subset=['LAT', 'LON', variable_selectionnee])
            if not df_valid.empty:
                heat_data = [(row['LAT'], row['LON'], 0.5) for _, row in df_valid.iterrows()]
                plugins.HeatMap(heat_data, radius=20, blur=15, max_zoom=10).add_to(carte)
        else:
            carte = create_interactive_map(df_jour, variable_selectionnee)
        
        st_folium(carte, width=1400, height=600)
    
    st.markdown("---")
    
    # ==================== ANALYSES ====================
    
    st.subheader("📈 Analyses Complémentaires")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏆 Top Stations",
        "📊 Distribution",
        "⛰️ Altitude",
        "📅 Temporel",
        "📋 Données"
    ])
    
    with tab1:
        fig = create_top_stations_chart(df_jour, variable_selectionnee, top_n=18)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = create_distribution_chart(df_jour, variable_selectionnee)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        fig = create_altitude_analysis(df_jour, variable_selectionnee)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Données d'altitude non disponibles")
    
    with tab4:
        fig = create_temporal_comparison(df_annee, variable_selectionnee, date_selectionnee)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Données temporelles insuffisantes")
    
    with tab5:
        cols_display = ['NUM_POSTE', 'NOM_USUEL', 'ALTI', variable_selectionnee]
        cols_display = [col for col in cols_display if col in df_jour.columns]
        
        df_display = df_jour[cols_display].sort_values(
            by=variable_selectionnee,
            ascending=False,
            na_position='last'
        ).reset_index(drop=True)
        
        st.dataframe(df_display, use_container_width=True, height=400)
        
        csv = df_display.to_csv(index=False, sep=';').encode('utf-8')
        st.download_button(
            "📥 Télécharger (CSV)",
            csv,
            f"meteo_{date_selectionnee.strftime('%Y%m%d')}_{variable_selectionnee}.csv",
            "text/csv"
        )
    
    # ==================== FOOTER ====================
    
    st.markdown("---")
    st.caption(f"""
    🗺️ Carte Interactive Météo | {date_selectionnee.strftime('%d/%m/%Y')} | 
    {df_jour['NUM_POSTE'].nunique()} stations | Année {annee_selectionnee}
    """)


if __name__ == "__main__": 
    main()