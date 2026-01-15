"""
Constantes et configurations pour l'application météo
"""

# ==================== DESCRIPTIONS DES COLONNES ====================

COLUMN_DESCRIPTIONS = {
    # Identification
    'NUM_POSTE': 'Numéro de poste météorologique',
    'NOM_USUEL': 'Nom de la station',
    'LAT': 'Latitude (degrés décimaux)',
    'LON': 'Longitude (degrés décimaux)',
    'ALTI': 'Altitude (mètres)',
    'AAAAMMJJ': 'Date (format AAAAMMJJ)',
    
    # Précipitations
    'RR': 'Précipitations quotidiennes (mm)',
    'QRR': 'Qualité précipitations',
    'DRR': 'Durée des précipitations (minutes)',
    'QDRR': 'Qualité durée précipitations',
    
    # Températures
    'TN': 'Température minimale (°C)',
    'QTN': 'Qualité température minimale',
    'HTN': 'Heure température minimale',
    'QHTN': 'Qualité heure température minimale',
    'TX': 'Température maximale (°C)',
    'QTX': 'Qualité température maximale',
    'HTX': 'Heure température maximale',
    'QHTX': 'Qualité heure température maximale',
    'TM': 'Température moyenne (°C)',
    'QTM': 'Qualité température moyenne',
    'TNTXM': 'Moyenne des températures min et max (°C)',
    'QTNTXM': 'Qualité moyenne TN/TX',
    'TAMPLI': 'Amplitude thermique (°C)',
    'QTAMPLI': 'Qualité amplitude',
    'TNSOL': 'Température minimale du sol (°C)',
    'QTNSOL': 'Qualité température sol',
    'TN50': 'Température minimale à 50cm (°C)',
    'QTN50': 'Qualité température 50cm',
    
    # Vent
    'FFM': 'Vitesse moyenne du vent (m/s)',
    'QFFM': 'Qualité vent moyen',
    'FF2M': 'Vitesse vent à 2m (m/s)',
    'QFF2M': 'Qualité vent 2m',
    'FXY': 'Rafale maximale quotidienne (m/s)',
    'QFXY': 'Qualité rafale max',
    'DXY': 'Direction rafale max (degrés)',
    'QDXY': 'Qualité direction rafale',
    'HXY': 'Heure rafale max',
    'QHXY': 'Qualité heure rafale',
    'FXI': 'Rafale instantanée maximale (m/s)',
    'QFXI': 'Qualité rafale instantanée',
    'DXI': 'Direction rafale instantanée (degrés)',
    'QDXI': 'Qualité direction rafale inst',
    'HXI': 'Heure rafale instantanée',
    'QHXI': 'Qualité heure rafale inst',
    'FXI2': 'Rafale instantanée 2 (m/s)',
    'QFXI2': 'Qualité rafale inst 2',
    'DXI2': 'Direction rafale inst 2 (degrés)',
    'QDXI2': 'Qualité direction rafale inst 2',
    'HXI2': 'Heure rafale inst 2',
    'QHXI2': 'Qualité heure rafale inst 2',
    'FXI3S': 'Rafale sur 3 secondes (m/s)',
    'QFXI3S': 'Qualité rafale 3s',
    'DXI3S': 'Direction rafale 3s (degrés)',
    'QDXI3S': 'Qualité direction rafale 3s',
    'HXI3S': 'Heure rafale 3s',
    'QHXI3S': 'Qualité heure rafale 3s',
    
    # Autres
    'DG': 'Degrés jours de chauffage',
    'QDG': 'Qualité degrés jours'
}

# ==================== NOMS COURTS POUR AFFICHAGE ====================

SHORT_NAMES = {
    'TN': 'Temp. Min',
    'TX': 'Temp. Max',
    'TM': 'Temp. Moy',
    'TAMPLI': 'Amplitude',
    'RR': 'Précipitations',
    'FFM': 'Vent Moyen',
    'FXY': 'Rafales Max'
}

# ==================== UNITÉS ====================

UNITS = {
    'TN': '°C',
    'TX': '°C',
    'TM': '°C',
    'TAMPLI': '°C',
    'TNSOL': '°C',
    'TN50': '°C',
    'RR': 'mm',
    'DRR': 'min',
    'FFM': 'm/s',
    'FF2M': 'm/s',
    'FXY': 'm/s',
    'FXI': 'm/s',
    'DXY': '°',
    'DXI': '°',
    'ALTI': 'm'
}

# ==================== SEUILS MÉTÉOROLOGIQUES ====================

THRESHOLDS = {
    # Températures
    'canicule_tx': 35,           # TX > 35°C
    'forte_chaleur_tx': 30,      # TX > 30°C
    'gel_tn': 0,                 # TN < 0°C
    'grand_froid_tn': -5,        # TN < -5°C
    'nuit_tropicale_tn': 20,     # TN > 20°C
    
    # Précipitations
    'pluie_faible': 1,           # RR > 1mm
    'pluie_moderee': 10,         # RR > 10mm
    'pluie_forte': 50,           # RR > 50mm
    'pluie_extreme': 100,        # RR > 100mm
    
    # Vent
    'vent_faible': 5,            # < 5 m/s (18 km/h)
    'vent_modere': 10,           # < 10 m/s (36 km/h)
    'vent_fort': 20,             # < 20 m/s (72 km/h)
    'tempete': 28,               # > 28 m/s (100 km/h)
    
    # Durée événements
    'duree_canicule': 3,         # 3 jours consécutifs
    'duree_vague_froid': 3,      # 3 jours consécutifs
    'duree_secheresse': 30       # 30 jours sans pluie
}

# ==================== CODES QUALITÉ ====================

QUALITY_CODES = {
    '0': 'Donnée absente',
    '1': 'Donnée correcte',
    '2': 'Donnée douteuse',
    '3': 'Donnée modifiée',
    '4': 'Donnée reconstituée',
    '5': 'Donnée non validée',
    '9': 'Donnée manquante'
}

QUALITY_GOOD = ['1']  # Codes considérés comme bonne qualité

# ==================== SAISONS ====================

SEASONS = {
    'Hiver': [12, 1, 2],
    'Printemps': [3, 4, 5],
    'Été': [6, 7, 8],
    'Automne': [9, 10, 11]
}

MONTHS_FR = {
    1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril',
    5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Août',
    9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
}

# ==================== PALETTES DE COULEURS ====================

COLOR_PALETTES = {
    'temperature': ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8',
                   '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026'],
    'precipitation': ['#ffffff', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6',
                     '#2171b5', '#08519c', '#08306b'],
    'wind': ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6',
            '#4292c6', '#2171b5', '#08519c', '#08306b']
}

# ==================== RÉGIONS FRANÇAISES (mapping départements) ====================

REGIONS_FRANCE = {
    '01': 'Auvergne-Rhône-Alpes',
    '02': 'Hauts-de-France',
    '03': 'Auvergne-Rhône-Alpes',
    '04': 'Provence-Alpes-Côte d\'Azur',
    '05': 'Provence-Alpes-Côte d\'Azur',
    '06': 'Provence-Alpes-Côte d\'Azur',
    '07': 'Auvergne-Rhône-Alpes',
    '08': 'Grand Est',
    '09': 'Occitanie',
    '10': 'Grand Est',
    '11': 'Occitanie',
    '12': 'Occitanie',
    '13': 'Provence-Alpes-Côte d\'Azur',
    '14': 'Normandie',
    '15': 'Auvergne-Rhône-Alpes',
    '16': 'Nouvelle-Aquitaine',
    '17': 'Nouvelle-Aquitaine',
    '18': 'Centre-Val de Loire',
    '19': 'Nouvelle-Aquitaine',
    '21': 'Bourgogne-Franche-Comté',
    '22': 'Bretagne',
    '23': 'Nouvelle-Aquitaine',
    '24': 'Nouvelle-Aquitaine',
    '25': 'Bourgogne-Franche-Comté',
    '26': 'Auvergne-Rhône-Alpes',
    '27': 'Normandie',
    '28': 'Centre-Val de Loire',
    '29': 'Bretagne',
    '2A': 'Corse',
    '2B': 'Corse',
    '30': 'Occitanie',
    '31': 'Occitanie',
    '32': 'Occitanie',
    '33': 'Nouvelle-Aquitaine',
    '34': 'Occitanie',
    '35': 'Bretagne',
    '36': 'Centre-Val de Loire',
    '37': 'Centre-Val de Loire',
    '38': 'Auvergne-Rhône-Alpes',
    '39': 'Bourgogne-Franche-Comté',
    '40': 'Nouvelle-Aquitaine',
    '41': 'Centre-Val de Loire',
    '42': 'Auvergne-Rhône-Alpes',
    '43': 'Auvergne-Rhône-Alpes',
    '44': 'Pays de la Loire',
    '45': 'Centre-Val de Loire',
    '46': 'Occitanie',
    '47': 'Nouvelle-Aquitaine',
    '48': 'Occitanie',
    '49': 'Pays de la Loire',
    '50': 'Normandie',
    '51': 'Grand Est',
    '52': 'Grand Est',
    '53': 'Pays de la Loire',
    '54': 'Grand Est',
    '55': 'Grand Est',
    '56': 'Bretagne',
    '57': 'Grand Est',
    '58': 'Bourgogne-Franche-Comté',
    '59': 'Hauts-de-France',
    '60': 'Hauts-de-France',
    '61': 'Normandie',
    '62': 'Hauts-de-France',
    '63': 'Auvergne-Rhône-Alpes',
    '64': 'Nouvelle-Aquitaine',
    '65': 'Occitanie',
    '66': 'Occitanie',
    '67': 'Grand Est',
    '68': 'Grand Est',
    '69': 'Auvergne-Rhône-Alpes',
    '70': 'Bourgogne-Franche-Comté',
    '71': 'Bourgogne-Franche-Comté',
    '72': 'Pays de la Loire',
    '73': 'Auvergne-Rhône-Alpes',
    '74': 'Auvergne-Rhône-Alpes',
    '75': 'Île-de-France',
    '76': 'Normandie',
    '77': 'Île-de-France',
    '78': 'Île-de-France',
    '79': 'Nouvelle-Aquitaine',
    '80': 'Hauts-de-France',
    '81': 'Occitanie',
    '82': 'Occitanie',
    '83': 'Provence-Alpes-Côte d\'Azur',
    '84': 'Provence-Alpes-Côte d\'Azur',
    '85': 'Pays de la Loire',
    '86': 'Nouvelle-Aquitaine',
    '87': 'Nouvelle-Aquitaine',
    '88': 'Grand Est',
    '89': 'Bourgogne-Franche-Comté',
    '90': 'Bourgogne-Franche-Comté',
    '91': 'Île-de-France',
    '92': 'Île-de-France',
    '93': 'Île-de-France',
    '94': 'Île-de-France',
    '95': 'Île-de-France'
}

# ==================== CONFIGURATION GRAPHIQUES ====================

CHART_CONFIG = {
    'height': 500,
    'template': 'plotly_white',
    'font_size': 12,
    'title_font_size': 16,
    'show_legend': True,
    'margin': {'l': 50, 'r': 50, 't': 80, 'b': 50}
}

# ==================== COLONNES PRINCIPALES ====================

MAIN_COLUMNS = {
    'identification': ['NUM_POSTE', 'NOM_USUEL', 'LAT', 'LON', 'ALTI'],
    'date': ['AAAAMMJJ'],
    'temperature': ['TN', 'TX', 'TM', 'TAMPLI'],
    'precipitation': ['RR', 'DRR'],
    'wind': ['FFM', 'FXY', 'DXY']
}

# Colonnes numériques à convertir
NUMERIC_COLUMNS = ['LAT', 'LON', 'ALTI', 'RR', 'TN', 'TX', 'TM', 'TAMPLI', 
                   'TNSOL', 'TN50', 'FFM', 'FF2M', 'FXY', 'FXI', 'DXY', 
                   'DXI', 'DRR', 'DG']