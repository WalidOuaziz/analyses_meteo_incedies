"""
Page d'analyse géospatiale des départements 13 et 05
Statistiques et graphiques en premier, puis cartes
"""

import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ==================== CONFIGURATION PAGE ====================

st.set_page_config(
    page_title="Analyse Géospatiale - Météo France",
    page_icon="🗺️",
    layout="wide"
)

# ==================== CACHE SESSION ====================

@st.cache_resource
def load_shapefiles():
    """Charge les fichiers shapefiles"""
    try:
        gdf_13 = gpd.read_file("data/raw/dep_13/communes_13_with_data_for_carte_danger_incendie.shp")
        gdf_05 = gpd.read_file("data/raw/dep_05/communes_05_with_data_for_carte_danger_incendie.shp")
        return gdf_13, gdf_05
    except Exception as e:  
        st.error(f"Erreur lors du chargement des shapefiles: {e}")
        return None, None


@st.cache_resource
def load_incendies_csv():
    """Charge le fichier CSV d'incendies"""
    try:  
        df = pd.read_csv(
            "data/raw/incendies.csv", 
            sep=';', 
            encoding='latin-1'
        )
        return df
        
    except Exception as e:  
        st.error(f"❌ Erreur lors du chargement du CSV:  {e}")
        return None

# ==================== FONCTIONS DE TRAITEMENT ====================

def prepare_geodata(gdf_13, gdf_05):
    """Prépare les données géospatiales"""
    
    gdfs = []
    
    for gdf, dept_name in [(gdf_13, '13'), (gdf_05, '05')]:
        gdf = gdf.copy()
        
        gdf.columns = gdf.columns.str.strip().str.lower()
        
        for col in gdf.columns:
            if any(x in col for x in ['area', 'surf', 'pente']):
                gdf[col] = pd.to_numeric(gdf[col], errors='coerce')
        
        gdf['departement'] = dept_name
        gdf['dept_label'] = f"Département {dept_name}"
        
        if 'surf_foret' in gdf.columns and 'pente_mean' in gdf.columns:
            max_foret = gdf['surf_foret'].max()
            max_pente = gdf['pente_mean'].max()
            
            if max_foret > 0 and max_pente > 0:
                gdf['risque_feu'] = (
                    (gdf['surf_foret'].fillna(0) / max_foret) * 0.5 +
                    (gdf['pente_mean'].fillna(0) / max_pente) * 0.5
                ) * 100
            else:  
                gdf['risque_feu'] = 50
        else:  
            gdf['risque_feu'] = 50
        
        gdfs.append(gdf)
    
    gdf_combined = pd.concat(gdfs, ignore_index=True)
    gdf_combined = gpd.GeoDataFrame(gdf_combined, crs=gdf_13.crs)
    
    return gdf_combined


def prepare_incendies(df):
    """Prépare les données d'incendies"""
    if df is None or df.empty:
        st.warning("⚠️ Données d'incendies vides")
        return None
    
    df = df.copy()
    
    try:
        df.columns = df.columns.str.strip()
        
        # Convertir Année et mois
        if 'Année' in df.columns:
            df['Année'] = pd.to_numeric(df['Année'], errors='coerce')
        
        if 'mois' in df.columns:
            df['mois'] = pd.to_numeric(df['mois'], errors='coerce')
        
        if 'heure' in df.columns:
            df['heure'] = pd.to_numeric(df['heure'], errors='coerce')
        
        # Convertir surface
        if 'Surface parcourue (m2)' in df.columns:
            df['Surface parcourue (m2)'] = pd.to_numeric(df['Surface parcourue (m2)'], errors='coerce')
            df['surf_ha'] = df['Surface parcourue (m2)'] / 10000
        
        if 'surf_ha' in df.columns:
            df['surf_ha'] = pd.to_numeric(df['surf_ha'], errors='coerce')
        
        # Filtrer pour deps 13 et 05
        if 'Département' in df.columns:
            df['Département'] = df['Département'].astype(str).str.strip()
            df = df[df['Département'].isin(['13', '05', '6', '5'])]
        
        return df
        
    except Exception as e:  
        st.error(f"❌ Erreur préparation incendies: {e}")
        return None


# ==================== GRAPHIQUES INCENDIES ====================

def create_fires_by_year(incendies_df):
    """Nombre de feux par année"""
    
    if incendies_df is None or 'Année' not in incendies_df.columns:
        return None
    
    try:
        yearly = incendies_df.dropna(subset=['Année']).groupby('Année').size().reset_index(name='Nombre')
        yearly['Année'] = yearly['Année'].astype(int)
        yearly = yearly.sort_values('Année')
        
        if yearly.empty:
            return None
        
        fig = px.line(
            yearly,
            x='Année',
            y='Nombre',
            title='Nombre d\'Incendies par Année',
            labels={'Année': 'Année', 'Nombre': 'Nombre d\'Incendies'},
            markers=True,
            line_shape='spline'
        )
        
        fig.update_traces(line=dict(color='#DC143C', width=3), marker=dict(size=8))
        fig.update_layout(height=400, template='plotly_white', hovermode='x unified')
        
        return fig
    except Exception as e:
        return None


def create_fires_by_month(incendies_df):
    """Nombre de feux par mois"""
    
    if incendies_df is None or 'mois' not in incendies_df.columns:
        return None
    
    try:  
        monthly = incendies_df.dropna(subset=['mois']).groupby('mois').size().reset_index(name='Nombre')
        monthly['mois'] = monthly['mois'].astype(int)
        
        if monthly.empty:
            return None
        
        mois_names = {1: 'Jan', 2: 'Fév', 3: 'Mar', 4: 'Avr', 5: 'Mai', 6: 'Juin',
                      7: 'Juil', 8: 'Août', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Déc'}
        monthly['mois_nom'] = monthly['mois'].map(mois_names)
        
        fig = px.bar(
            monthly,
            x='mois_nom',
            y='Nombre',
            title='Nombre d\'Incendies par Mois',
            labels={'mois_nom': 'Mois', 'Nombre': 'Nombre d\'Incendies'},
            color='Nombre',
            color_continuous_scale='Reds',
            text='Nombre'
        )
        
        fig.update_traces(textposition='auto')
        fig.update_layout(height=400, template='plotly_white')
        
        return fig
    except Exception as e:
        return None


def create_fires_by_month_pie(incendies_df):
    """Répartition mensuelle"""
    
    if incendies_df is None or 'mois' not in incendies_df.columns:
        return None
    
    try:  
        monthly = incendies_df.dropna(subset=['mois']).groupby('mois').size().reset_index(name='Nombre')
        monthly['mois'] = monthly['mois'].astype(int)
        
        if monthly.empty:
            return None
        
        mois_names = {1: 'Jan', 2: 'Fév', 3: 'Mar', 4: 'Avr', 5: 'Mai', 6: 'Juin',
                      7: 'Juil', 8: 'Août', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Déc'}
        monthly['mois_nom'] = monthly['mois'].map(mois_names)
        
        fig = px.pie(
            monthly,
            names='mois_nom',
            values='Nombre',
            title='Répartition Mensuelle des Incendies',
            color_discrete_sequence=px.colors.sequential.Reds
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        return fig
    except Exception as e:
        return None


def create_affected_area_by_year(incendies_df):
    """Surface affectée par année"""
    
    if incendies_df is None or 'Année' not in incendies_df.columns or 'surf_ha' not in incendies_df.columns:
        return None
    
    try: 
        yearly = incendies_df.dropna(subset=['Année', 'surf_ha']).groupby('Année')['surf_ha'].sum().reset_index(name='Surface')
        yearly['Année'] = yearly['Année'].astype(int)
        yearly = yearly.sort_values('Année')
        
        if yearly.empty:
            return None
        
        fig = px.bar(
            yearly,
            x='Année',
            y='Surface',
            title='Surface Affectée par Année',
            labels={'Année': 'Année', 'Surface': 'Surface (ha)'},
            color='Surface',
            color_continuous_scale='Oranges',
            text='Surface'
        )
        
        fig.update_traces(texttemplate='%{text:.0f}', textposition='auto')
        fig.update_layout(height=400, template='plotly_white')
        
        return fig
    except Exception as e: 
        return None


def create_combined_fires_analysis(incendies_df):
    """Analyse combinée"""
    
    if incendies_df is None or 'Année' not in incendies_df.columns:
        return None
    
    try:  
        # Nombre par année
        nb_fires = incendies_df.dropna(subset=['Année']).groupby('Année').size().reset_index(name='Nombre')
        nb_fires['Année'] = nb_fires['Année'].astype(int)
        
        # Surface par année
        surface = incendies_df.dropna(subset=['Année', 'surf_ha']).groupby('Année')['surf_ha'].sum().reset_index(name='Surface')
        surface['Année'] = surface['Année'].astype(int)
        
        # Merger
        yearly = nb_fires.merge(surface, on='Année', how='outer')
        yearly = yearly.sort_values('Année')
        
        if yearly.empty:
            return None
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(
                x=yearly['Année'],
                y=yearly['Surface'],
                mode='lines+markers',
                name='Surface (ha)',
                line=dict(color='orange', width=3),
                marker=dict(size=8)
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Bar(
                x=yearly['Année'],
                y=yearly['Nombre'],
                name='Nombre d\'incendies',
                marker_color='#DC143C',
                opacity=0.6
            ),
            secondary_y=True
        )
        
        fig.update_xaxes(title_text="Année")
        fig.update_yaxes(title_text="Surface (ha)", secondary_y=False)
        fig.update_yaxes(title_text="Nombre", secondary_y=True)
        
        fig.update_layout(
            title='Nombre et Surface par Année',
            height=400,
            template='plotly_white',
            hovermode='x unified'
        )
        
        return fig
    except Exception as e:
        return None


def create_risque_feu_chart(gdf):
    """Top communes par risque"""
    gdf_sorted = gdf.nlargest(20, 'risque_feu')
    
    fig = px.bar(
        gdf_sorted.sort_values('risque_feu'),
        x='risque_feu',
        y='nom',
        title='Top 20 Communes - Risque Incendie',
        labels={'risque_feu': 'Risque (%)', 'nom': 'Commune'},
        color='risque_feu',
        color_continuous_scale='Reds',
        orientation='h'
    )
    fig.update_layout(height=500, template='plotly_white', showlegend=False)
    return fig


def create_foret_analysis(gdf):
    """Couverture forestière"""
    by_dept = gdf.groupby('dept_label').agg({
        'surf_foret': 'sum',
        'area_ha': 'sum'
    }).reset_index()
    
    fig = go.Figure(data=[
        go.Bar(name='Forêt (ha)', x=by_dept['dept_label'], y=by_dept['surf_foret'], marker_color='darkgreen'),
        go.Bar(name='Total (ha)', x=by_dept['dept_label'], y=by_dept['area_ha'], marker_color='lightgreen')
    ])
    
    fig.update_layout(title='Couverture Forestière', barmode='group', height=400, template='plotly_white')
    return fig, by_dept


def calculate_statistics(gdf, incendies_df):
    """Calcule les statistiques"""
    
    stats = {
        'Communes': len(gdf),
        'Surface Forêt (ha)': gdf['surf_foret'].sum() if 'surf_foret' in gdf.columns else 0,
        'Risque Moyen (%)': gdf['risque_feu'].mean() if 'risque_feu' in gdf.columns else 0,
    }
    
    if incendies_df is not None and not incendies_df.empty:
        stats['Total Incendies'] = len(incendies_df)
        if 'Année' in incendies_df.columns:
            annees = incendies_df['Année'].dropna()
            if len(annees) > 0:
                stats['Années'] = f"{int(annees.min())}-{int(annees.max())}"
                stats['Nb Années'] = int(annees.max()) - int(annees.min()) + 1
        if 'surf_ha' in incendies_df.columns:
            stats['Surface Totale (ha)'] = incendies_df['surf_ha'].sum()
    
    return stats


# ==================== CARTES GÉOSPATIALES ====================

def create_interactive_map(gdf, incendies_df=None):
    """Crée une carte interactive des communes et risques"""
    
    m = folium.Map(
        location=[44.5, 4.0],
        zoom_start=7,
        tiles='CartoDB positron'
    )
    
    for idx, row in gdf.iterrows():
        try:
            geom = row['geometry']
            risque = row.get('risque_feu', 50)
            
            if risque > 75:
                color = '#8B0000'
            elif risque > 50:
                color = '#DC143C'
            elif risque > 25:
                color = '#FF8C00'
            else:  
                color = '#FFD700'
            
            nom = row.get('nom', 'N/A')
            
            popup_html = f"""
            <b>{nom}</b><br>
            Risque: {risque:.1f}%<br>
            Forêt: {row.get('surf_foret', 0):.1f} ha<br>
            Pente: {row.get('pente_mean', 0):.1f}°
            """
            
            folium.GeoJson(
                data=geom.__geo_interface__,
                style_function=lambda x, c=color: {
                    'fillColor': c,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.6
                },
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"{nom}"
            ).add_to(m)
        except:   
            continue
    
    folium.LayerControl().add_to(m)
    return m


def create_pente_map(gdf):
    """Crée une carte choroplèthe des pentes"""
    
    m = folium.Map(
        location=[44.5, 4.0],
        zoom_start=7,
        tiles='CartoDB positron'
    )
    
    pente_max = gdf['pente_mean'].max()
    
    for idx, row in gdf.iterrows():
        try:
            geom = row['geometry']
            pente = row.get('pente_mean', 0)
            
            intensity = pente / pente_max if pente_max > 0 else 0
            if intensity > 0.75:
                color = '#8B0000'
            elif intensity > 0.5:
                color = '#FF4500'
            elif intensity > 0.25:
                color = '#FFD700'
            else:  
                color = '#90EE90'
            
            nom = row.get('nom', 'N/A')
            
            popup_html = f"""
            <b>{nom}</b><br>
            Pente moy: {pente:.1f}°<br>
            Pente min: {row.get('pente_min', 0):.1f}°<br>
            Pente max: {row.get('pente_max', 0):.1f}°
            """
            
            folium.GeoJson(
                data=geom.__geo_interface__,
                style_function=lambda x, c=color: {
                    'fillColor': c,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.6
                },
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"{nom}"
            ).add_to(m)
        except:  
            continue
    
    folium.LayerControl().add_to(m)
    return m


def create_incendies_heatmap(incendies_df):
    """Crée une heatmap des incendies"""
    
    m = folium.Map(
        location=[44.5, 4.0],
        zoom_start=7,
        tiles='CartoDB positron'
    )
    
    if incendies_df is not None and not incendies_df.empty:
        try:
            coords_list = []
            
            for idx, row in incendies_df.iterrows():
                try:
                    dept = str(row.get('Département', '13')).strip()
                    
                    if dept in ['13', '6']: 
                        lat = 43.7 + np.random.uniform(-0.5, 0.5)
                        lon = 5.2 + np.random.uniform(-0.5, 0.5)
                    else:
                        lat = 44.3 + np.random.uniform(-0.5, 0.5)
                        lon = 5.8 + np.random.uniform(-0.5, 0.5)
                    
                    if pd.notna(lat) and pd.notna(lon):
                        coords_list.append([lat, lon])
                except: 
                    continue
            
            if coords_list:  
                plugins.HeatMap(
                    coords_list,
                    min_opacity=0.3,
                    max_zoom=13,
                    radius=30,
                    blur=20,
                    gradient={0.0: 'blue', 0.5: 'yellow', 1.0: 'red'}
                ).add_to(m)
        except Exception as e:  
            pass
    
    folium.LayerControl().add_to(m)
    return m


# ==================== INTERFACE PRINCIPALE ====================

def main():
    st.title("🗺️ Analyse Géospatiale - Départements 13 & 05")
    st.markdown("**Analyse complète avec incendies et géographie**")
    
    # Charger données
    with st.spinner("📂 Chargement..."):
        gdf_13, gdf_05 = load_shapefiles()
    
    if gdf_13 is None or gdf_05 is None:
        st.error("❌ Impossible de charger les shapefiles")
        st.stop()
    
    with st.spinner("📊 Chargement incendies..."):
        incendies_df = load_incendies_csv()
    
    gdf = prepare_geodata(gdf_13, gdf_05)
    if incendies_df is not None:  
        incendies_df = prepare_incendies(incendies_df)
    
    # ==================== STATISTIQUES ====================
    
    st.markdown("---")
    st.subheader("📊 Statistiques Globales")
    
    stats = calculate_statistics(gdf, incendies_df)
    
    cols = st.columns(len(stats))
    for i, (key, value) in enumerate(stats.items()):
        with cols[i]:
            if isinstance(value, (int, float)):
                if value > 10000:
                    st.metric(key, f"{value:,.0f}")
                else:  
                    st.metric(key, f"{value:.1f}" if isinstance(value, float) else value)
            else:
                st.metric(key, value)
    
    st.markdown("---")
    
    # ==================== FILTRES ====================
    
    st.subheader("🎛️ Filtres")
    col1, col2 = st.columns(2)
    
    with col1:
        dept_select = st.multiselect(
            "Département(s)",
            options=['13', '05'],
            default=['13', '05']
        )
        gdf_filtered = gdf[gdf['departement'].isin(dept_select)]
    
    with col2:
        risque_min = st.slider("Risque minimum (%)", 0, 100, 0, 5)
        gdf_filtered = gdf_filtered[gdf_filtered['risque_feu'] >= risque_min]
    
    st.markdown("---")
    
    if gdf_filtered.empty:
        st.warning("⚠️ Aucune donnée")
        st.stop()
    
    # ==================== GRAPHIQUES INCENDIES ====================
    
    st.subheader("🔥 Analyse des Incendies")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Feux par Année (Line)")
        fig = create_fires_by_year(incendies_df)
        if fig:  
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Feux par Mois (Histogram)")
        fig = create_fires_by_month(incendies_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown("#### Répartition Mensuelle (Pie)")
        fig = create_fires_by_month_pie(incendies_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Surface Affectée par Année (Bar)")
        fig = create_affected_area_by_year(incendies_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Analyse Combinée (Line + Bar)")
        fig = create_combined_fires_analysis(incendies_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ==================== ANALYSES GÉOSPATIALES ====================
    
    st.subheader("📊 Analyses Géospatiales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Risque Incendie")
        fig = create_risque_feu_chart(gdf_filtered)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Couverture Forestière")
        fig, by_dept = create_foret_analysis(gdf_filtered)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ==================== CARTES ====================
    
    st.subheader("🗺️ Cartes Géospatiales")
    
    tab1, tab2, tab3 = st.tabs(["Risque Incendie", "Pentes", "Heatmap Incendies"])
    
    with tab1:
        st.markdown("#### Carte du Risque Incendie")
        with st.spinner("🗺️ Génération de la carte..."):
            carte = create_interactive_map(gdf_filtered, incendies_df)
            st_folium(carte, width=1400, height=700)
    
    with tab2:
        st.markdown("#### Carte des Pentes")
        with st.spinner("🗺️ Génération de la carte..."):
            carte_pente = create_pente_map(gdf_filtered)
            st_folium(carte_pente, width=1400, height=700)
    
    with tab3:
        st.markdown("#### Heatmap des Incendies")
        with st.spinner("🗺️ Génération de la heatmap..."):
            carte_incendies = create_incendies_heatmap(incendies_df)
            st_folium(carte_incendies, width=1400, height=700)
    
    st.markdown("---")
    
    # ==================== DONNÉES DÉTAILLÉES ====================
    
    with st.expander("📋 Données Détaillées"):
        st.write(f"Communes filtrées: {len(gdf_filtered)}")
        if incendies_df is not None:   
            st.write(f"Total Incendies: {len(incendies_df)}")
            st.dataframe(incendies_df.head(100), use_container_width=True)
    
    st.caption(f"🗺️ Analyse Géospatiale | {len(gdf_filtered)} communes")


if __name__ == "__main__":
    main()