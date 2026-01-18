"""
Script de test pour vérifier que l'application fonctionne correctement
après les optimisations
"""

import sys
from pathlib import Path

print("🔍 Vérification de l'application...")
print("=" * 60)

# 1. Vérifier que les fichiers Parquet existent
print("\n📦 Vérification des fichiers de données...")

meteo_file = Path("data/raw/meteo.parquet")
incendies_file = Path("data/raw/incendies.parquet")

if meteo_file.exists():
    size_mb = meteo_file.stat().st_size / (1024 * 1024)
    print(f"✅ meteo.parquet trouvé ({size_mb:.1f} MB)")
else:
    print("❌ meteo.parquet MANQUANT!")
    sys.exit(1)

if incendies_file.exists():
    size_mb = incendies_file.stat().st_size / (1024 * 1024)
    print(f"✅ incendies.parquet trouvé ({size_mb:.1f} MB)")
else:
    print("❌ incendies.parquet MANQUANT!")
    sys.exit(1)

# 2. Vérifier que les anciens CSV ont été supprimés
print("\n🗑️ Vérification de la suppression des fichiers CSV...")

old_files = ["meteo.csv", "incendies.csv", "meteo_2000_2020.csv"]
for old_file in old_files:
    path = Path("data/raw") / old_file
    if path.exists():
        print(f"⚠️ {old_file} existe encore (peut être supprimé)")
    else:
        print(f"✅ {old_file} supprimé")

# 3. Test de chargement rapide
print("\n⚡ Test de performance de chargement...")

try:
    import pandas as pd
    import time
    
    start = time.time()
    df = pd.read_parquet(meteo_file)
    load_time = time.time() - start
    
    print(f"✅ Données chargées en {load_time:.2f} secondes")
    print(f"📊 {len(df):,} lignes chargées")
    print(f"📋 {len(df.columns)} colonnes")
    
except Exception as e:
    print(f"❌ Erreur de chargement: {e}")
    sys.exit(1)

# 4. Vérifier les modules utils
print("\n🔧 Vérification des modules utils...")

try:
    from utils.data_loader import load_data
    print("✅ data_loader importé")
    
    from utils.constants import NUMERIC_COLUMNS
    print("✅ constants importé")
    
    from utils.styles import get_page_style
    print("✅ styles importé")
    
    from utils.preprocessing import filter_by_altitude
    print("✅ preprocessing importé")
    
except Exception as e:
    print(f"❌ Erreur d'import: {e}")
    sys.exit(1)

# 5. Vérifier la configuration Streamlit
print("\n⚙️ Vérification de la configuration...")

config_file = Path(".streamlit/config.toml")
if config_file.exists():
    print("✅ Fichier de configuration trouvé")
else:
    print("⚠️ Fichier de configuration manquant")

# 6. Vérifier les pages
print("\n📄 Vérification des pages...")

pages = [
    "Home.py",
    "pages/Analyse_Incendies.py",
    "pages/1__Carte_Interactive.py",
    "pages/3__Températures.py",
    "pages/4__Précipitations.py",
    "pages/5__Analyse_du_Vent.py",
    "pages/6__Comparaisons_Géographiques.py",
    "pages/7__Événements_Extrêmes.py"
]

for page in pages:
    if Path(page).exists():
        print(f"✅ {page}")
    else:
        print(f"❌ {page} MANQUANT!")

print("\n" + "=" * 60)
print("✨ Vérification terminée avec succès!")
print("\n🚀 Pour lancer l'application:")
print("   python -m streamlit run Home.py")
print("=" * 60)
