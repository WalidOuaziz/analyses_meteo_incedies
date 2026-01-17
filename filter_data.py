"""
Script pour extraire les données météo de 2000 à 2020
Lit meteo.csv et crée meteo_2000_2020.csv
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

def filter_meteo_data(input_file, output_file, year_start=2000, year_end=2020):
    """
    Filtre les données météo par période
    
    Args:
        input_file: Chemin du fichier source
        output_file: Chemin du fichier de sortie
        year_start: Année de début (incluse)
        year_end: Année de fin (incluse)
    """
    
    print(f"🔄 Lecture du fichier {input_file}...")
    
    try:
        # Lire le fichier CSV
        df = pd.read_csv(
            input_file,
            sep=';',
            encoding='utf-8',
            low_memory=False
        )
        
        print(f"✅ {len(df):,} lignes chargées")
        print(f"📊 Colonnes : {list(df.columns)}")
        
        # Convertir la colonne date
        if 'AAAAMMJJ' in df.columns:
            df['date'] = pd.to_datetime(df['AAAAMMJJ'], format='%Y%m%d', errors='coerce')
            df['annee'] = df['date'].dt.year
            
            # Filtrer par année
            df_filtered = df[(df['annee'] >= year_start) & (df['annee'] <= year_end)].copy()
            
            # Supprimer les colonnes temporaires
            df_filtered = df_filtered.drop(columns=['date', 'annee'], errors='ignore')
            
            print(f"\n🔍 Filtrage de {year_start} à {year_end}...")
            print(f"✅ {len(df_filtered):,} lignes retenues ({len(df_filtered)/len(df)*100:.1f}% des données)")
            
            # Statistiques
            print(f"\n📈 Statistiques :")
            print(f"   - Nombre de stations : {df_filtered['NUM_POSTE'].nunique() if 'NUM_POSTE' in df_filtered.columns else 'N/A'}")
            print(f"   - Période : {df_filtered['AAAAMMJJ'].min()} à {df_filtered['AAAAMMJJ'].max()}")
            
            # Sauvegarder
            print(f"\n💾 Sauvegarde dans {output_file}...")
            df_filtered.to_csv(
                output_file,
                sep=';',
                index=False,
                encoding='utf-8'
            )
            
            # Taille du fichier
            file_size_mb = Path(output_file).stat().st_size / (1024 * 1024)
            print(f"✅ Fichier créé : {file_size_mb:.2f} MB")
            print(f"✅ TERMINÉ ! Fichier disponible : {output_file}")
            
            return df_filtered
            
        else:
            print("❌ Erreur : Colonne 'AAAAMMJJ' introuvable")
            return None
            
    except FileNotFoundError:
        print(f"❌ Erreur : Fichier {input_file} introuvable")
        return None
    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
        return None


if __name__ == "__main__":
    # Configuration
    INPUT_FILE = "data/raw/meteo.csv"
    OUTPUT_FILE = "data/raw/meteo_2000_2020.csv"
    
    # Créer le dossier de sortie si nécessaire
    Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)
    
    # Exécuter le filtrage
    print("=" * 60)
    print("🌤️  FILTRAGE DES DONNÉES MÉTÉO")
    print("=" * 60)
    
    df_result = filter_meteo_data(INPUT_FILE, OUTPUT_FILE, 2000, 2020)
    
    if df_result is not None:
        print("\n" + "=" * 60)
        print("✅ SUCCÈS !")
        print("=" * 60)
        print(f"\nVous pouvez maintenant utiliser : {OUTPUT_FILE}")
        print(f"Pour charger ce fichier dans votre app, modifiez :")
        print(f'  load_data("{OUTPUT_FILE}")')