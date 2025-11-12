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

def validar_años_educacion(edad, años_educacion):
    """
    Valida que los años de educación no excedan el máximo permitido.
    Regla: años_educacion <= (edad - 5)
    
    Args:
        edad (int): Edad del paciente
        años_educacion (int): Años de educación formal
        
    Returns:
        tuple: (es_valido, max_permitido, mensaje)
    """
    max_permitido = max(0, edad - 5)
    es_valido = años_educacion <= max_permitido
    
    if es_valido:
        mensaje = f"✓ Años de educación válidos ({años_educacion} <= {max_permitido})"
    else:
        mensaje = f"✗ Los años de educación ({años_educacion}) exceden el máximo permitido ({max_permitido})"
    
    return es_valido, max_permitido, mensaje

def calcular_nivel_hads(puntaje):
    if puntaje <= 7:
        return "Normal"
    elif puntaje <= 10:
        return "Ansiedad leve"
    elif puntaje <= 14:
        return "Ansiedad moderada"
    else:
        return "Ansiedad severa"

def calcular_nivel_zsas(puntaje_normalizado):
    if puntaje_normalizado < 45:
        return "Normal"
    elif puntaje_normalizado < 60:
        return "Ansiedad leve a moderada"
    elif puntaje_normalizado < 75:
        return "Ansiedad marcada a severa"
    else:
        return "Ansiedad extrema"

def calcular_sf12(respuestas):
    """
    Calcula puntuaciones simplificadas para SF-12 separando componentes física (PCS)
    y mental (MCS).

    Estrategia (simplificada): se suman los ítems correspondientes a cada componente.
    Asignación (índices 0-based):
      - PCS (física): ítems [0,1,2,3,4,7]  (Q1, Q2, Q3, Q4, Q5, Q8)
      - MCS (mental): ítems [5,6,8,9,10,11] (Q6, Q7, Q9, Q10, Q11, Q12)

    Args:
        respuestas (list): lista de 12 valores numéricos (pueden ser ints/floats)

    Returns:
        dict: {'fisica': float, 'mental': float, 'total': float}
    """
    if not respuestas or len(respuestas) < 12:
        # Si faltan respuestas, devolver None para cada componente
        return {'fisica': None, 'mental': None, 'total': None}

    try:
        vals = [float(x) if x is not None else 0.0 for x in respuestas]
    except Exception:
        vals = [0.0 for _ in range(12)]

    pcs_indices = [0, 1, 2, 3, 4, 7]
    mcs_indices = [5, 6, 8, 9, 10, 11]

    pcs = sum(vals[i] for i in pcs_indices)
    mcs = sum(vals[i] for i in mcs_indices)
    total = pcs + mcs

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
    Clasifica el puntaje físico del SF-12 en cuartiles según umbrales provistos:
    - Cuartil 1 (1) si puntaje <= 15
    - Cuartil 2 (2) si puntaje <= 17
    - Cuartil 3 (3) si puntaje <= 19
    - Cuartil 4 (4) si puntaje >= 20

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
    Clasifica el puntaje mental del SF-12 en cuartiles según umbrales sugeridos:
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
