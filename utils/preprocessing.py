"""
Fonctions de prétraitement et filtrage des données
"""

import pandas as pd
import streamlit as st
from datetime import datetime
from typing import List


@st.cache_data
def filter_by_date_range(
    df: pd.DataFrame,
    date_debut: datetime,
    date_fin: datetime
) -> pd.DataFrame:
    """Filtre les données par période"""
    if 'date' not in df.columns or df.empty:
        return df

    mask = (
        (df['date'] >= pd.to_datetime(date_debut)) &
        (df['date'] <= pd.to_datetime(date_fin))
    )
    return df.loc[mask].copy()


@st.cache_data
def filter_by_stations(
    df: pd.DataFrame,
    station_ids: List[str]
) -> pd.DataFrame:
    """Filtre les données par station(s)"""
    if not station_ids or 'NUM_POSTE' not in df.columns or df.empty:
        return df

    return df[df['NUM_POSTE'].isin(station_ids)].copy()


@st.cache_data
def filter_by_altitude(
    df: pd.DataFrame,
    alt_min: int,
    alt_max: int
) -> pd.DataFrame:
    """Filtre les données par altitude"""
    if 'ALTI' not in df.columns or df.empty:
        return df

    mask = (df['ALTI'] >= alt_min) & (df['ALTI'] <= alt_max)
    return df.loc[mask].copy()


@st.cache_data
def filter_by_region(
    df: pd.DataFrame,
    regions: List[str]
) -> pd.DataFrame:
    """Filtre les données par région(s)"""
    if not regions or 'region' not in df.columns or df.empty:
        return df

    return df[df['region'].isin(regions)].copy()


@st.cache_data
def aggregate_by_period(
    df: pd.DataFrame,
    period: str = 'D',
    agg_functions: dict | None = None
) -> pd.DataFrame:
    """Agrège les données par période"""
    if 'date' not in df.columns or df.empty:
        return df

    if agg_functions is None:
        agg_functions = {
            'TN': 'mean',
            'TX': 'mean',
            'TM': 'mean',
            'TAMPLI': 'mean',
            'RR': 'sum',
            'FFM': 'mean',
            'FXY': 'max'
        }

    agg_dict = {c: f for c, f in agg_functions.items() if c in df.columns}
    if not agg_dict:
        return df

    df_agg = (
        df.set_index('date')
          .resample(period)
          .agg(agg_dict)
          .reset_index()
    )

    return df_agg


@st.cache_data
def aggregate_by_station(
    df: pd.DataFrame,
    agg_functions: dict | None = None
) -> pd.DataFrame:
    """Agrège les données par station"""
    if 'NUM_POSTE' not in df.columns or df.empty:
        return df

    if agg_functions is None:
        agg_functions = {
            'NOM_USUEL': 'first',
            'LAT': 'first',
            'LON': 'first',
            'ALTI': 'first',
            'region': 'first',
            'TN': 'mean',
            'TX': 'mean',
            'TM': 'mean',
            'RR': 'sum',
            'FFM': 'mean'
        }

    agg_dict = {c: f for c, f in agg_functions.items() if c in df.columns}
    if not agg_dict:
        return df

    df_agg = (
        df.groupby('NUM_POSTE')
          .agg(agg_dict)
          .reset_index()
    )

    return df_agg


@st.cache_data
def detect_extreme_events(
    df: pd.DataFrame,
    event_type: str,
    threshold: float,
    duration: int = 1
) -> pd.DataFrame:
    """Détecte les événements météorologiques extrêmes"""
    if df.empty or 'date' not in df.columns:
        return pd.DataFrame()

    events = []

    for station in df['NUM_POSTE'].unique():
        df_station = df[df['NUM_POSTE'] == station].sort_values('date')

        if event_type == 'canicule' and 'TX' in df.columns:
            mask = df_station['TX'] > threshold

        elif event_type == 'gel' and 'TN' in df.columns:
            mask = df_station['TN'] < threshold

        else:
            continue

        groups = (mask != mask.shift()).cumsum()
        sequences = df_station[mask].groupby(groups)

        for _, seq in sequences:
            if len(seq) >= duration:
                events.append({
                    'NUM_POSTE': station,
                    'NOM_USUEL': seq['NOM_USUEL'].iloc[0],
                    'type': event_type,
                    'date_debut': seq['date'].min(),
                    'date_fin': seq['date'].max(),
                    'duree': len(seq),
                    'valeur_moy': seq.iloc[:, -1].mean()
                })

    if event_type == 'forte_pluie' and 'RR' in df.columns:
        for _, row in df[df['RR'] > threshold].iterrows():
            events.append({
                'NUM_POSTE': row['NUM_POSTE'],
                'NOM_USUEL': row['NOM_USUEL'],
                'type': 'forte_pluie',
                'date_debut': row['date'],
                'date_fin': row['date'],
                'duree': 1,
                'valeur_max': row['RR']
            })

    if event_type == 'tempete' and 'FXY' in df.columns:
        for _, row in df[df['FXY'] > threshold].iterrows():
            events.append({
                'NUM_POSTE': row['NUM_POSTE'],
                'NOM_USUEL': row['NOM_USUEL'],
                'type': 'tempete',
                'date_debut': row['date'],
                'date_fin': row['date'],
                'duree': 1,
                'valeur_max': row['FXY']
            })

    return pd.DataFrame(events)


@st.cache_data
def calculate_monthly_stats(
    df: pd.DataFrame,
    variable: str
) -> pd.DataFrame:
    """Calcule les statistiques mensuelles"""
    if variable not in df.columns or 'annee_mois' not in df.columns or df.empty:
        return pd.DataFrame()

    stats = (
        df.groupby('annee_mois')[variable]
          .agg(
              moyenne='mean',
              minimum='min',
              maximum='max',
              ecart_type='std',
              mediane='median',
              nb_valeurs='count'
          )
          .reset_index()
    )

    return stats
