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
