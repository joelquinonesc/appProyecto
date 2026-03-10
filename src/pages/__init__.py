"""
Inicializador del paquete pages
"""
from . import home
from . import demograficos
from . import datos_geneticos
from . import resultados
from . import analisis_masivo
from .eventos_vitales import mostrar_eventos_vitales
from .sf12_fisica import mostrar_sf12_fisica
from .sf12_mental import mostrar_sf12_mental
from .hads import mostrar_hads
from .zsas import mostrar_zsas

__all__ = [
    'home',
    'demograficos',
    'datos_geneticos',
    'resultados',
    'analisis_masivo',
    'mostrar_eventos_vitales',
    'mostrar_sf12_fisica',
    'mostrar_sf12_mental',
    'mostrar_hads',
    'mostrar_zsas',
]
