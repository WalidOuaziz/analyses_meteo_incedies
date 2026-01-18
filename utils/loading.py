"""
Utilitaires pour afficher des indicateurs de chargement
"""

import streamlit as st
from functools import wraps
import time


def with_loading(message="⏳ Chargement en cours..."):
    """
    Décorateur pour afficher un spinner pendant l'exécution d'une fonction
    
    Usage:
        @with_loading("Création du graphique...")
        def create_chart():
            return px.line(...)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with st.spinner(message):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def show_with_spinner(content_func, spinner_text="⏳ Génération en cours..."):
    """
    Affiche un spinner pendant la génération de contenu
    
    Args:
        content_func: Fonction qui génère le contenu
        spinner_text: Message du spinner
        
    Returns:
        Résultat de content_func
        
    Usage:
        fig = show_with_spinner(
            lambda: px.line(df, x='date', y='value'),
            "⏳ Création du graphique..."
        )
        st.plotly_chart(fig)
    """
    with st.spinner(spinner_text):
        return content_func()


def display_chart(fig, spinner_text="⏳ Affichage du graphique...", **kwargs):
    """
    Affiche un graphique Plotly avec spinner
    
    Args:
        fig: Figure Plotly
        spinner_text: Message du spinner
        **kwargs: Arguments pour st.plotly_chart
    """
    with st.spinner(spinner_text):
        st.plotly_chart(fig, **kwargs)


def display_map(map_obj, spinner_text="⏳ Affichage de la carte...", **kwargs):
    """
    Affiche une carte Folium avec spinner
    
    Args:
        map_obj: Objet carte Folium
        spinner_text: Message du spinner
        **kwargs: Arguments pour st_folium
    """
    from streamlit_folium import st_folium
    with st.spinner(spinner_text):
        st_folium(map_obj, **kwargs)


def display_dataframe(df, spinner_text="⏳ Affichage du tableau...", **kwargs):
    """
    Affiche un DataFrame avec spinner
    
    Args:
        df: DataFrame pandas
        spinner_text: Message du spinner
        **kwargs: Arguments pour st.dataframe
    """
    with st.spinner(spinner_text):
        st.dataframe(df, **kwargs)


def display_table(df, spinner_text="⏳ Affichage de la table...", **kwargs):
    """
    Affiche une table avec spinner
    
    Args:
        df: DataFrame pandas
        spinner_text: Message du spinner
        **kwargs: Arguments pour st.table
    """
    with st.spinner(spinner_text):
        st.table(df, **kwargs)


class LoadingContext:
    """
    Context manager pour afficher un spinner
    
    Usage:
        with LoadingContext("Chargement des données..."):
            df = load_data()
            process_data(df)
    """
    
    def __init__(self, message="⏳ Chargement...", show_success=False, success_msg="✅ Terminé"):
        self.message = message
        self.show_success = show_success
        self.success_msg = success_msg
        self.placeholder = None
    
    def __enter__(self):
        self.placeholder = st.empty()
        with self.placeholder:
            st.spinner(self.message)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.show_success and exc_type is None:
            with self.placeholder:
                st.success(self.success_msg)
                time.sleep(0.5)
            self.placeholder.empty()
        else:
            self.placeholder.empty()


def create_and_display_chart(create_func, spinner_text="⏳ Création du graphique...", **display_kwargs):
    """
    Crée et affiche un graphique avec un seul spinner
    
    Args:
        create_func: Fonction qui crée le graphique
        spinner_text: Message du spinner
        **display_kwargs: Arguments pour st.plotly_chart
        
    Usage:
        create_and_display_chart(
            lambda: px.line(df, x='date', y='value'),
            "⏳ Analyse en cours...",
            use_container_width=True
        )
    """
    with st.spinner(spinner_text):
        fig = create_func()
        st.plotly_chart(fig, **display_kwargs)


def create_and_display_map(create_func, spinner_text="⏳ Création de la carte...", **display_kwargs):
    """
    Crée et affiche une carte avec un seul spinner
    
    Args:
        create_func: Fonction qui crée la carte
        spinner_text: Message du spinner
        **display_kwargs: Arguments pour st_folium
        
    Usage:
        create_and_display_map(
            lambda: create_folium_map(data),
            "⏳ Génération de la carte...",
            width=700, height=500
        )
    """
    from streamlit_folium import st_folium
    with st.spinner(spinner_text):
        map_obj = create_func()
        st_folium(map_obj, **display_kwargs)


# Alias pour compatibilité
show_chart = display_chart
show_map = display_map
show_dataframe = display_dataframe
show_table = display_table
