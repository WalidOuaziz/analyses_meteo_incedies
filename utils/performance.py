"""
Module d'optimisation de performance pour données massives
"""

import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data
def sample_data_for_viz(df: pd.DataFrame, max_points: int = 10000, method: str = 'random') -> pd.DataFrame:
    """
    Échantillonne les données pour visualisation rapide
    
    Args:
        df: DataFrame complet
        max_points: Nombre maximum de points à afficher
        method: 'random', 'first', 'last', 'stratified'
        
    Returns:
        DataFrame échantillonné
    """
    if len(df) <= max_points:
        return df
    
    if method == 'random':
        return df.sample(n=max_points, random_state=42)
    elif method == 'first':
        return df.head(max_points)
    elif method == 'last':
        return df.tail(max_points)
    elif method == 'stratified' and 'annee' in df.columns:
        # Échantillonnage stratifié par année
        return df.groupby('annee', group_keys=False).apply(
            lambda x: x.sample(min(len(x), max_points // df['annee'].nunique()))
        )
    
    return df.sample(n=max_points, random_state=42)


@st.cache_data
def aggregate_temporal_data(df: pd.DataFrame, freq: str = 'M') -> pd.DataFrame:
    """
    Agrège les données temporelles pour réduire le nombre de points
    
    Args:
        df: DataFrame avec colonne 'date'
        freq: Fréquence d'agrégation ('D', 'W', 'M', 'Y')
        
    Returns:
        DataFrame agrégé
    """
    if 'date' not in df.columns:
        return df
    
    df_agg = df.set_index('date').resample(freq).agg({
        col: 'mean' for col in df.select_dtypes(include=[np.number]).columns
    })
    
    return df_agg.reset_index()


@st.cache_data
def reduce_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Réduit l'utilisation mémoire du DataFrame
    
    Args:
        df: DataFrame à optimiser
        
    Returns:
        DataFrame optimisé
    """
    df = df.copy()
    
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    for col in df.select_dtypes(include=['integer']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:
            df[col] = df[col].astype('category')
    
    return df


@st.cache_data
def filter_data_by_date_range(df: pd.DataFrame, start_date=None, end_date=None) -> pd.DataFrame:
    """
    Filtre efficace par plage de dates
    
    Args:
        df: DataFrame avec colonne 'date'
        start_date: Date de début
        end_date: Date de fin
        
    Returns:
        DataFrame filtré
    """
    if 'date' not in df.columns:
        return df
    
    mask = pd.Series(True, index=df.index)
    
    if start_date:
        mask &= df['date'] >= start_date
    
    if end_date:
        mask &= df['date'] <= end_date
    
    return df[mask]


@st.cache_data
def get_top_n_categories(df: pd.DataFrame, column: str, n: int = 10) -> list:
    """
    Récupère les N catégories les plus fréquentes
    
    Args:
        df: DataFrame
        column: Nom de la colonne
        n: Nombre de catégories à retourner
        
    Returns:
        Liste des top N catégories
    """
    return df[column].value_counts().head(n).index.tolist()


def optimize_plotly_figure(fig, max_points: int = 5000):
    """
    Optimise une figure Plotly pour performance
    
    Args:
        fig: Figure Plotly
        max_points: Nombre max de points
        
    Returns:
        Figure optimisée
    """
    # Réduire la qualité des rendus pour vitesse
    fig.update_layout(
        hovermode='closest',  # Au lieu de 'x' ou 'y'
        dragmode='pan',  # Désactiver zoom par défaut
    )
    
    # Désactiver les animations
    fig.layout.transition = {'duration': 0}
    
    return fig


@st.cache_data
def paginate_dataframe(df: pd.DataFrame, page_size: int = 100, page_num: int = 1) -> pd.DataFrame:
    """
    Pagination pour grands DataFrames
    
    Args:
        df: DataFrame complet
        page_size: Taille de la page
        page_num: Numéro de page (1-indexé)
        
    Returns:
        DataFrame paginé
    """
    start_idx = (page_num - 1) * page_size
    end_idx = start_idx + page_size
    
    return df.iloc[start_idx:end_idx]


@st.cache_data
def limit_map_markers(gdf, max_markers: int = 500):
    """
    Limite le nombre de marqueurs sur une carte
    
    Args:
        gdf: GeoDataFrame
        max_markers: Nombre maximum de marqueurs
        
    Returns:
        GeoDataFrame échantillonné
    """
    if len(gdf) <= max_markers:
        return gdf
    
    # Échantillonnage spatial intelligent
    return gdf.sample(n=max_markers, random_state=42)


def get_performance_config():
    """
    Retourne la configuration de performance recommandée
    
    Returns:
        dict: Configuration
    """
    return {
        'max_chart_points': 10000,
        'max_map_markers': 500,
        'max_table_rows': 1000,
        'aggregation_freq': 'M',  # Mensuel par défaut
        'enable_downsampling': True,
        'enable_caching': True,
        'chart_renderer': 'webgl'  # Pour Plotly
    }


@st.cache_data
def create_summary_stats(df: pd.DataFrame, group_by: str = None) -> pd.DataFrame:
    """
    Crée des statistiques résumées au lieu d'afficher toutes les données
    
    Args:
        df: DataFrame
        group_by: Colonne de groupement
        
    Returns:
        DataFrame de statistiques
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if group_by and group_by in df.columns:
        stats = df.groupby(group_by)[numeric_cols].agg(['count', 'mean', 'std', 'min', 'max'])
    else:
        stats = df[numeric_cols].describe()
    
    return stats


class PerformanceMonitor:
    """Moniteur de performance pour débogage"""
    
    def __init__(self):
        self.timings = {}
    
    def start(self, label: str):
        """Démarre un timer"""
        import time
        self.timings[label] = {'start': time.time()}
    
    def end(self, label: str):
        """Arrête un timer et affiche le temps"""
        import time
        if label in self.timings:
            elapsed = time.time() - self.timings[label]['start']
            self.timings[label]['elapsed'] = elapsed
            return elapsed
        return 0
    
    def display_stats(self):
        """Affiche les statistiques de performance"""
        if self.timings:
            st.sidebar.markdown("### ⚡ Performance")
            for label, data in self.timings.items():
                if 'elapsed' in data:
                    st.sidebar.text(f"{label}: {data['elapsed']:.2f}s")
