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
    # Puntuación básica
    puntaje = sum(respuestas)
    # En una implementación real, aquí iría el algoritmo completo de puntuación SF-12
    return puntaje
