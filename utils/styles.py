"""
Styles CSS personnalisés pour l'application Streamlit
Appliqué de manière cohérente sur toutes les pages
"""

def get_page_style():
    """Retourne le CSS principal pour les pages"""
    return """
    <style>
        /* === GÉNÉRAL === */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        .main {
            padding: 1.5rem 2rem;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }
        
        /* === TITRES === */
        h1 {
            color: #1e3a8a;
            font-weight: 700;
            padding-bottom: 1rem;
            border-bottom: 3px solid #3b82f6;
            margin-bottom: 2rem;
        }
        
        h2 {
            color: #1e40af;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        
        h3 {
            color: #2563eb;
            font-weight: 600;
            margin-top: 1.5rem;
        }
        
        /* === CARTES === */
        .card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            margin: 1rem 0;
            border-left: 4px solid #3b82f6;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.12);
        }
        
        .card-success {
            border-left-color: #10b981;
            background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        }
        
        .card-warning {
            border-left-color: #f59e0b;
            background: linear-gradient(135deg, #ffffff 0%, #fffbeb 100%);
        }
        
        .card-danger {
            border-left-color: #ef4444;
            background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
        }
        
        .card-info {
            border-left-color: #06b6d4;
            background: linear-gradient(135deg, #ffffff 0%, #ecfeff 100%);
        }
        
        /* === MÉTRIQUES === */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #1e3a8a;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.95rem;
            color: #64748b;
            font-weight: 500;
        }
        
        [data-testid="stMetricDelta"] {
            font-size: 0.9rem;
        }
        
        /* === SIDEBAR === */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e40af 50%, #3b82f6 100%) !important;
            padding: 2rem 1rem;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            background: transparent !important;
        }
        
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: white !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stMarkdown {
            color: rgba(255, 255, 255, 0.95) !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stMultiSelect label,
        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stDateInput label,
        [data-testid="stSidebar"] .stRadio label,
        [data-testid="stSidebar"] .stCheckbox label {
            color: white !important;
            font-weight: 600;
            font-size: 1rem;
        }
        
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
        [data-testid="stSidebar"] input,
        [data-testid="stSidebar"] select {
            background-color: rgba(255, 255, 255, 0.95) !important;
            color: #1e293b !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
        }
        
        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.3) !important;
            margin: 1.5rem 0;
        }
        
        [data-testid="stSidebar"] .stButton > button {
            background: rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            border: 2px solid rgba(255, 255, 255, 0.4) !important;
        }
        
        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255, 255, 255, 0.3) !important;
            border-color: rgba(255, 255, 255, 0.6) !important;
        }
        
        /* === BOUTONS === */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
            transform: translateY(-1px);
        }
        
        /* === INPUTS === */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {
            border-radius: 8px;
            border: 2px solid #e2e8f0;
            transition: border-color 0.2s;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* === TABS === */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: white;
            border-radius: 10px;
            padding: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            background-color: #f1f5f9;
            color: #64748b;
            border: none;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
        }
        
        /* === DATAFRAME === */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* === EXPANDER === */
        .streamlit-expanderHeader {
            background-color: #f8fafc;
            border-radius: 8px;
            font-weight: 600;
            color: #1e3a8a;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #f1f5f9;
        }
        
        /* === BADGES === */
        .badge {
            display: inline-block;
            padding: 0.35rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 0.2rem;
        }
        
        .badge-primary {
            background-color: #dbeafe;
            color: #1e40af;
        }
        
        .badge-success {
            background-color: #d1fae5;
            color: #065f46;
        }
        
        .badge-warning {
            background-color: #fef3c7;
            color: #92400e;
        }
        
        .badge-danger {
            background-color: #fee2e2;
            color: #991b1b;
        }
        
        /* === ALERTES === */
        .stAlert {
            border-radius: 10px;
            border-left-width: 4px;
        }
        
        /* === FEATURE BOX === */
        .feature-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }
        
        .feature-box h3 {
            color: white;
            margin-top: 0;
        }
        
        /* === STAT BOX === */
        .stat-box {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            transition: transform 0.2s;
        }
        
        .stat-box:hover {
            transform: scale(1.03);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1e3a8a;
            margin: 0.5rem 0;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #64748b;
            font-weight: 500;
        }
        
        /* === ANIMATIONS === */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .card, .stat-box {
            animation: fadeIn 0.5s ease-out;
        }
        
        /* === SCROLLBAR === */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
    </style>
    """


def get_sidebar_style():
    """Retourne le CSS pour personnaliser davantage la sidebar"""
    return """
    <style>
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e3a8a 50%, #3b82f6 100%);
        }
        
        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.2);
            margin: 1.5rem 0;
        }
        
        [data-testid="stSidebar"] .stMarkdown {
            color: white;
        }
    </style>
    """
