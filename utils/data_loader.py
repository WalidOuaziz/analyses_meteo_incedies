"""
Fonctions de chargement et préparation des données météorologiques
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from .constants import NUMERIC_COLUMNS, REGIONS_FRANCE, MONTHS_FR, SEASONS

@st.cache_data(show_spinner=False, ttl=3600)  # Cache 1 heure
def load_data(filepath: str = "data/raw/meteo.parquet", 
              columns: list = None, 
              years: list = None,
              sample_frac: float = None) -> pd.DataFrame:
    """
    Charge et prépare les données météorologiques depuis le fichier Parquet
    OPTIMISÉ pour données massives
    
    Args:
        filepath: Chemin vers le fichier Parquet
        columns: Liste de colonnes à charger (None = toutes)
        years: Liste d'années à filtrer (None = toutes)
        sample_frac: Fraction de données à échantillonner (0.1 = 10%)
        
    Returns:
        DataFrame pandas avec les données nettoyées et enrichies
    """
    try:
        # Vérifier que le fichier existe
        if not Path(filepath).exists():
            st.error(f"❌ Fichier non trouvé : {filepath}")
            st.info("📁 Placez votre fichier Parquet dans le dossier data/raw/")
            return pd.DataFrame()
        
        # Charger seulement les colonnes nécessaires pour économiser mémoire
        df = pd.read_parquet(filepath, columns=columns)
        
        # Filtrer par années si spécifié
        if years and 'AAAAMMJJ' in df.columns:
            df['temp_year'] = df['AAAAMMJJ'].astype(str).str[:4].astype(int)
            df = df[df['temp_year'].isin(years)]
            df = df.drop('temp_year', axis=1)
        
        # Échantillonnage si demandé
        if sample_frac and 0 < sample_frac < 1:
            df = df.sample(frac=sample_frac, random_state=42)
        
        # Convertir les types de données
        df = convert_data_types(df)
        
        # Ajouter les colonnes calculées
        df = add_computed_columns(df)
        
        # Gérer les données manquantes
        df = handle_missing_values(df)
        
        # Optimiser la mémoire
        df = reduce_memory_usage(df)
        
        return df
        
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données : {str(e)}")
        return pd.DataFrame()


def reduce_memory_usage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Réduit l'utilisation mémoire du DataFrame
    """
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    for col in df.select_dtypes(include=['int']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    return df


def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convertit les colonnes aux types appropriés
    
    Args:
        df: DataFrame brut
        
    Returns:
        DataFrame avec types convertis
    """
    # Copier pour éviter les warnings
    df = df.copy()
    
    # Convertir la date
    if 'AAAAMMJJ' in df.columns:
        df['date'] = pd.to_datetime(df['AAAAMMJJ'], format='%Y%m%d', errors='coerce')
    
    # Convertir les colonnes numériques
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Convertir altitude en entier
    if 'ALTI' in df.columns:
        df['ALTI'] = df['ALTI'].fillna(0).astype(int)
    
    return df


def add_computed_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute des colonnes calculées utiles pour l'analyse
    
    Args:
        df: DataFrame avec données de base
        
    Returns:
        DataFrame enrichi avec colonnes calculées
    """
    df = df.copy()
    
    if 'date' in df.columns:
        # Extraire les composantes de date
        df['annee'] = df['date'].dt.year
        df['mois'] = df['date'].dt.month
        df['jour'] = df['date'].dt.day
        df['jour_annee'] = df['date'].dt.dayofyear
        df['jour_semaine'] = df['date'].dt.dayofweek
        
        # Nom du mois en français
        df['nom_mois'] = df['mois'].map(MONTHS_FR)
        
        # Saison
        df['saison'] = df['mois'].apply(get_season)
        
        # Année-mois pour groupby
        df['annee_mois'] = df['date'].dt.to_period('M').astype(str)
    
    # Extraire le code département (2 premiers chiffres du NUM_POSTE)
    if 'NUM_POSTE' in df.columns:
        df['dept'] = df['NUM_POSTE'].astype(str).str[:2]
        df['region'] = df['dept'].map(REGIONS_FRANCE)
    
    # Convertir vent m/s en km/h pour plus de lisibilité
    if 'FFM' in df.columns:
        df['FFM_kmh'] = df['FFM'] * 3.6
    if 'FXY' in df.columns:
        df['FXY_kmh'] = df['FXY'] * 3.6
    
    # Indicateurs booléens pour événements
    if 'TN' in df.columns:
        df['jour_gel'] = df['TN'] < 0
    if 'TX' in df.columns:
        df['jour_canicule'] = df['TX'] > 35
        df['jour_chaleur'] = df['TX'] > 30
    if 'RR' in df.columns:
        df['jour_pluie'] = df['RR'] > 1
        df['jour_pluie_forte'] = df['RR'] > 50
    
    return df


def get_season(month: int) -> str:
    """
    Retourne la saison correspondant au mois
    
    Args:
        month: Numéro du mois (1-12)
        
    Returns:
        Nom de la saison
    """
    for season, months in SEASONS.items():
        if month in months:
            return season
    return 'Inconnu'


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gère les valeurs manquantes
    
    Args:
        df: DataFrame avec possibles valeurs manquantes
        
    Returns:
        DataFrame avec gestion des valeurs manquantes
    """
    df = df.copy()
    
    # Remplacer les valeurs sentinelles par NaN si nécessaire
    # (certains fichiers météo utilisent 9999 ou -999 pour valeurs manquantes)
    
    # Pour l'instant, pandas gère déjà les valeurs vides avec pd.to_numeric
    
    return df


@st.cache_data
def get_stations_list(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retourne la liste unique des stations avec leurs métadonnées
    
    Args:
        df: DataFrame complet
        
    Returns:
        DataFrame avec une ligne par station
    """
    if df.empty:
        return pd.DataFrame()
    
    stations = df.groupby('NUM_POSTE').agg({
        'NOM_USUEL': 'first',
        'LAT': 'first',
        'LON': 'first',
        'ALTI': 'first',
        'dept': 'first',
        'region': 'first',
        'date': ['min', 'max', 'count']
    }).reset_index()
    
    # Aplatir les colonnes multi-index
    stations.columns = ['NUM_POSTE', 'NOM_USUEL', 'LAT', 'LON', 'ALTI', 
                       'dept', 'region', 'date_debut', 'date_fin', 'nb_mesures']
    
    return stations


@st.cache_data
def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Retourne un résumé statistique des données
    
    Args:
        df: DataFrame complet
        
    Returns:
        Dictionnaire avec statistiques clés
    """
    if df.empty:
        return {}
    
    summary = {
        'nb_lignes': len(df),
        'nb_stations': df['NUM_POSTE'].nunique() if 'NUM_POSTE' in df.columns else 0,
        'date_min': df['date'].min() if 'date' in df.columns else None,
        'date_max': df['date'].max() if 'date' in df.columns else None,
        'nb_jours': df['date'].nunique() if 'date' in df.columns else 0,
        'nb_regions': df['region'].nunique() if 'region' in df.columns else 0,
        'completude': {}
    }
    
    # Calculer le taux de complétude pour les colonnes principales
    for col in ['TN', 'TX', 'TM', 'RR', 'FFM']:
        if col in df.columns:
            summary['completude'][col] = (df[col].notna().sum() / len(df) * 100)
    
    return summary


def filter_by_quality(df: pd.DataFrame, quality_threshold: str = '1') -> pd.DataFrame:
    """
    Filtre les données selon leur qualité
    
    Args:
        df: DataFrame à filtrer
        quality_threshold: Code qualité minimum acceptable
        
    Returns:
        DataFrame filtré
    """
    df_filtered = df.copy()
    
    # Liste des colonnes de qualité
    quality_cols = [col for col in df.columns if col.startswith('Q') and col != 'QTNTXM']
    
    # Filtrer sur la qualité (garder seulement code '1' = donnée correcte)
    for qcol in quality_cols:
        if qcol in df.columns:
            data_col = qcol[1:]  # Enlever le Q du début
            if data_col in df.columns:
                df_filtered.loc[df_filtered[qcol] != quality_threshold, data_col] = np.nan
    
    return df_filtered


@st.cache_data
def export_to_csv(df: pd.DataFrame) -> bytes:
    """
    Exporte le DataFrame en CSV pour téléchargement
    
    Args:
        df: DataFrame à exporter
        
    Returns:
        Données CSV en bytes
    """
    return df.to_csv(index=False, sep=';', encoding='utf-8').encode('utf-8')