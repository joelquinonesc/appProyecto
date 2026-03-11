"""
Funciones de transformación y cálculo para ANXRISK.

Contiene toda la lógica pura (sin dependencias de Streamlit) para convertir
los datos crudos del paciente en las variables que consumen los modelos
XGBoost (estándar 13 features) y XGBoost (extendido 22 features).

Bloques:
  1. Transformaciones demográficas (edad, género, educación)
  2. Eventos vitales LTE-12
  3. Salud SF-12 (componentes física y mental, cuartiles)
  4. Niveles de ansiedad HADS y ZSAS
  5. Clasificación de riesgo (umbrales fijos)
"""


def transformar_edad_a_grupo(edad):
    """
    Transforma la edad en una variable categórica binaria.
    
    Args:
        edad (int): Edad en años
        
    Returns:
        int: 0 si edad <= 24, 1 si edad > 24
    """
    return 0 if edad <= 24 else 1

def transformar_genero_a_binario(genero):
    """
    Transforma el género en una variable binaria.
    
    Args:
        genero (str): Género ('Masculino' o 'Femenino')
        
    Returns:
        int: 0 si Masculino, 1 si Femenino
    """
    if isinstance(genero, str):
        return 0 if genero.lower() in ['masculino', 'hombre', 'male', 'm'] else 1
    return genero  # Si ya es numérico, retornar tal cual

def calcular_nivel_hads(puntaje):
    if puntaje >= 8:
        return "⚠️ Riesgo de Ansiedad"
    else:
        return "✅ Riesgo Bajo"

def calcular_nivel_zsas(puntaje_normalizado):
    if puntaje_normalizado >= 36:
        return "⚠️ Riesgo de Ansiedad"
    else:
        return "✅ Riesgo Bajo"

def calcular_sf12(respuestas):
    """
    Calcula puntuaciones simplificadas para SF-12 separando componentes física (PCS)
    y mental (MCS).

    Estrategia (simplificada): se suman los ítems correspondientes a cada componente.
    Asignación (índices 0-based):
      - PCS (física): ítems [0,1,2,3,4,7]  (Q1, Q2, Q3, Q4, Q5, Q8)
      - MCS (mental): ítems [5,6,8,9,10,11] (Q6, Q7, Q9, Q10, Q11, Q12)

    Args:
        respuestas (list): lista de hasta 12 valores numéricos (pueden ser ints/floats)

    Returns:
        dict: {'fisica': float|None, 'mental': float|None, 'total': float|None}
    """
    if not respuestas:
        return {'fisica': None, 'mental': None, 'total': None}

    # Normalizar longitud y convertir a float cuando sea posible
    vals = []
    for i in range(12):
        try:
            x = respuestas[i]
        except IndexError:
            vals.append(None)
            continue
        if x is None:
            vals.append(None)
        else:
            try:
                vals.append(float(x))
            except Exception:
                vals.append(None)

    pcs_indices = [0, 1, 2, 3, 4, 7]
    mcs_indices = [5, 6, 8, 9, 10, 11]

    pcs_items = [vals[i] for i in pcs_indices]
    mcs_items = [vals[i] for i in mcs_indices]

    # Calcular cada componente de forma independiente si sus ítems están completos
    pcs = None
    mcs = None

    if not any(v is None for v in pcs_items):
        pcs = sum(pcs_items)

    if not any(v is None for v in mcs_items):
        mcs = sum(mcs_items)

    total = pcs + mcs if (pcs is not None and mcs is not None) else None

    return {'fisica': pcs, 'mental': mcs, 'total': total}


def transformar_educacion_a_binaria(años_educacion):
    """
    Transforma los años de educación formal en una variable binaria:
    - 0 si años_educacion <= 14
    - 1 si años_educacion >= 15

    Args:
        años_educacion (int): Años de educación formal

    Returns:
        int: 0 o 1
    """
    try:
        años = int(años_educacion)
    except Exception:
        return None

    return 0 if años <= 14 else 1


def transformar_lte12_a_clasificacion(total_puntaje):
    """
    Transforma el puntaje total de la LTE-12 en una clasificación ordinal:
    - 0 si total == 0
    - 1 si total == 1
    - 2 si total >= 2

    Args:
        total_puntaje (int): Suma de respuestas afirmativas (0-12)

    Returns:
        int: 0, 1 o 2 según la regla
    """
    try:
        t = int(total_puntaje)
    except Exception:
        return None

    if t <= 0:
        return 0
    if t == 1:
        return 1
    return 2


def transformar_sf12_fisica_a_cuartil(puntaje):
    """
    Clasifica el puntaje físico del SF-12 en cuartiles con umbrales:
    - Q1 si puntaje <= 15
    - Q2 si puntaje <= 17
    - Q3 si puntaje <= 19
    - Q4 si puntaje >= 20

    Args:
        puntaje (int|float): Puntaje físico calculado

    Returns:
        int: 1..4 representando el cuartil, o None si entrada inválida
    """
    try:
        p = float(puntaje)
    except Exception:
        return None

    if p <= 15:
        return 1
    if p <= 17:
        return 2
    if p <= 19:
        return 3
    return 4


def transformar_sf12_fisica_a_label(puntaje):
    """
    Devuelve una etiqueta textual del cuartil para la componente física del SF-12.
    Etiquetas: 'Q1', 'Q2', 'Q3', 'Q4'

    Args:
        puntaje (int|float): Puntaje físico calculado

    Returns:
        str: Etiqueta del cuartil ('Q1'..'Q4') o None si entrada inválida
    """
    cuartil = transformar_sf12_fisica_a_cuartil(puntaje)
    if cuartil is None:
        return None
    return f"Q{cuartil}"


def transformar_sf12_mental_a_cuartil(puntaje):
    """
    Clasifica el puntaje mental del SF-12 en cuartiles según el rango 6-30:
    - Cuartil 1 (1) si puntaje <= 15
    - Cuartil 2 (2) si puntaje <= 18
    - Cuartil 3 (3) si puntaje <= 21
    - Cuartil 4 (4) si puntaje >= 22

    Args:
        puntaje (int|float): Puntaje mental calculado

    Returns:
        int: 1..4 representando el cuartil, o None si entrada inválida
    """
    try:
        p = float(puntaje)
    except Exception:
        return None

    if p <= 15:
        return 1
    if p <= 18:
        return 2
    if p <= 21:
        return 3
    return 4


def transformar_sf12_mental_a_label(puntaje):
    """
    Devuelve una etiqueta textual del cuartil para la componente mental del SF-12.
    Etiquetas: 'Q1', 'Q2', 'Q3', 'Q4'
    """
    cuartil = transformar_sf12_mental_a_cuartil(puntaje)
    if cuartil is None:
        return None
    return f"Q{cuartil}"


def clasificar_por_youden(proba, umbral, ancho=0.10):
    """Clasifica probabilidad en tres categorías con umbrales fijos.

    - Bajo: prob < 0.30
    - Moderado: 0.30 <= prob < 0.70
    - Alto: prob >= 0.70

    Args:
        proba (float): probabilidad estimada para la clase positiva
        umbral (float|None): no se usa (mantenido por compatibilidad)
        ancho (float): no se usa (mantenido por compatibilidad)

    Returns:
        str: 'Bajo', 'Moderado' o 'Alto'
    """
    try:
        p = float(proba)
    except Exception:
        return 'No disponible'

    if p < 0.30:
        return 'Bajo'
    elif p < 0.70:
        return 'Moderado'
    else:
        return 'Alto'
