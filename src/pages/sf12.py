"""
Compatibilidad: stub para la antigua `mostrar_sf12`.

Este archivo proporciona una función `mostrar_sf12()` que redirige
la navegación a la nueva implementación dividida en `sf12_fisica`
y `sf12_mental`. Mantiene la API previa para evitar import errors
en otros módulos que todavía esperen `mostrar_sf12`.
"""
import streamlit as st
from .sf12_fisica import mostrar_sf12_fisica


def mostrar_sf12():
    """Mostrar la primera parte (física) y avisar al usuario.

    Mantiene la firma antigua para compatibilidad con imports existentes.
    """
    st.warning(
        "La versión combinada del SF-12 fue archivada. Se iniciará la versión dividida (Física → Mental).",
        icon="⚠️",
    )
    # Lanzar la página física. La página mental se accede desde el botón "Siguiente →".
    mostrar_sf12_fisica()
