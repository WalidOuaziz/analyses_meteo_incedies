"""
Script pour créer des échantillons de données optimisés pour le déploiement Streamlit Cloud.
Ce script réduit la taille des fichiers de données en filtrant sur les années récentes.
"""

import pandas as pd
import os
from pathlib import Path

def create_sample_data():
    """Crée des fichiers échantillons à partir des données complètes."""
    
    print("🔄 Création des fichiers échantillons pour le déploiement...")
    
    # Chemins des fichiers
    data_dir = Path("data/raw")
    
    # 1. Traiter les données météo (plus volumineux: 10.4MB)
    meteo_file = data_dir / "meteo.parquet"
    if meteo_file.exists():
        print(f"\n📊 Traitement de {meteo_file.name}...")
        df_meteo = pd.read_parquet(meteo_file)
        print(f"   Taille originale: {len(df_meteo):,} lignes, {meteo_file.stat().st_size / 1024 / 1024:.2f} MB")
        
        # Extraire l'année et filtrer (2018-2023 pour réduire de ~90%)
        if 'AAAAMMJJ' in df_meteo.columns:
            df_meteo['year'] = pd.to_datetime(df_meteo['AAAAMMJJ'], format='%Y%m%d').dt.year
            df_meteo_sample = df_meteo[df_meteo['year'] >= 2018].copy()
            df_meteo_sample = df_meteo_sample.drop(columns=['year'])
        else:
            # Si pas de colonne AAAAMMJJ, prendre les derniers 20%
            df_meteo_sample = df_meteo.tail(int(len(df_meteo) * 0.2)).copy()
        
        # Sauvegarder l'échantillon
        sample_file = data_dir / "meteo_sample.parquet"
        df_meteo_sample.to_parquet(sample_file, compression='snappy', index=False)
        print(f"   ✅ Échantillon créé: {len(df_meteo_sample):,} lignes, {sample_file.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"   📉 Réduction: {(1 - len(df_meteo_sample)/len(df_meteo))*100:.1f}%")
    else:
        print(f"⚠️  Fichier non trouvé: {meteo_file}")
    
    # 2. Traiter les données incendies (moins critique: 3.4MB)
    incendies_file = data_dir / "incendies.parquet"
    if incendies_file.exists():
        print(f"\n🔥 Traitement de {incendies_file.name}...")
        df_incendies = pd.read_parquet(incendies_file)
        print(f"   Taille originale: {len(df_incendies):,} lignes, {incendies_file.stat().st_size / 1024 / 1024:.2f} MB")
        
        # Filtrer sur les années récentes (2010-2023)
        if 'An' in df_incendies.columns:
            df_incendies_sample = df_incendies[df_incendies['An'] >= 2010].copy()
        else:
            # Prendre les derniers 50%
            df_incendies_sample = df_incendies.tail(int(len(df_incendies) * 0.5)).copy()
        
        # Sauvegarder l'échantillon
        sample_file = data_dir / "incendies_sample.parquet"
        df_incendies_sample.to_parquet(sample_file, compression='snappy', index=False)
        print(f"   ✅ Échantillon créé: {len(df_incendies_sample):,} lignes, {sample_file.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"   📉 Réduction: {(1 - len(df_incendies_sample)/len(df_incendies))*100:.1f}%")
    else:
        print(f"⚠️  Fichier non trouvé: {incendies_file}")
    
    print("\n" + "="*60)
    print("✅ CRÉATION DES ÉCHANTILLONS TERMINÉE")
    print("="*60)
    print("\n📝 PROCHAINES ÉTAPES:")
    print("1. Vérifier les tailles des fichiers créés")
    print("2. Mettre à jour .gitignore pour exclure les fichiers complets")
    print("3. Modifier data_loader.py pour utiliser les *_sample.parquet")
    print("4. Pousser vers GitHub et déployer sur Streamlit Cloud")

if __name__ == "__main__":
    create_sample_data()
