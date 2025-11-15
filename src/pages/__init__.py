"""
Inicializador del paquete pages
"""
from .eventos_vitales import mostrar_eventos_vitales
from .sf12_fisica import mostrar_sf12_fisica
from .sf12_mental import mostrar_sf12_mental
from .hads import mostrar_hads
from .zsas import mostrar_zsas
from . import resultados

__all__ = ['mostrar_eventos_vitales', 'mostrar_sf12_fisica', 'mostrar_sf12_mental', 'mostrar_hads', 'mostrar_zsas', 'resultados']
