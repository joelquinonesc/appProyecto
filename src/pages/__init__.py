"""
Inicializador del paquete pages
"""
from .eventos_vitales import mostrar_eventos_vitales
from .sf12 import mostrar_sf12
from .hads import mostrar_hads
from .zsas import mostrar_zsas

__all__ = ['mostrar_eventos_vitales', 'mostrar_sf12', 'mostrar_hads', 'mostrar_zsas']
