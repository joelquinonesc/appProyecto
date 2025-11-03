"""
Ejemplo de transformación de edad a grupo_edad
Este script demuestra cómo transformar la variable edad en una variable categórica binaria.
Incluye ejemplos para procesamiento en batch y datos dinámicos.
"""

import pandas as pd
from src.utils.calculos import transformar_edad_a_grupo


def ejemplo_basico():
    """
    Ejemplo básico con DataFrame estático
    """
    print("=" * 60)
    print("EJEMPLO 1: TRANSFORMACIÓN BÁSICA CON DATAFRAME")
    print("=" * 60)
    
    # Crear DataFrame de ejemplo
    df = pd.DataFrame({
        'edad': [18, 22, 25, 30]
    })
    
    # Aplicar la transformación
    df['grupo_edad'] = df['edad'].apply(transformar_edad_a_grupo)
    
    print("\nDataFrame con transformación aplicada:")
    print(df)
    print("\nRegla aplicada:")
    print("  - edad <= 24 → grupo_edad = 0")
    print("  - edad > 24  → grupo_edad = 1")
    print()


def ejemplo_datos_multiples():
    """
    Ejemplo con múltiples registros y datos adicionales
    """
    print("=" * 60)
    print("EJEMPLO 2: DATOS DEMOGRÁFICOS COMPLETOS")
    print("=" * 60)
    
    # DataFrame con más información
    df = pd.DataFrame({
        'nombre': ['Ana García', 'Carlos López', 'María Rodríguez', 'Juan Pérez', 'Laura Martínez'],
        'edad': [20, 24, 25, 28, 32],
        'genero': ['Femenino', 'Masculino', 'Femenino', 'Masculino', 'Femenino']
    })
    
    # Aplicar transformación
    df['grupo_edad'] = df['edad'].apply(transformar_edad_a_grupo)
    
    print("\nDataFrame completo:")
    print(df)
    print("\nEstadísticas por grupo:")
    print(df.groupby('grupo_edad')['edad'].describe())
    print()


def procesar_registro_individual(edad, nombre="Paciente"):
    """
    Función para procesar un registro individual
    Útil para procesamiento dinámico en Streamlit
    
    Args:
        edad (int): Edad del paciente
        nombre (str): Nombre del paciente
        
    Returns:
        dict: Diccionario con datos procesados
    """
    grupo_edad = transformar_edad_a_grupo(edad)
    
    return {
        'nombre': nombre,
        'edad': edad,
        'grupo_edad': grupo_edad,
        'etiqueta_grupo': 'Joven (≤24 años)' if grupo_edad == 0 else 'Adulto (>24 años)'
    }


def ejemplo_streaming_simulado():
    """
    Ejemplo de procesamiento dinámico de datos
    Simula el procesamiento de múltiples registros
    """
    print("=" * 60)
    print("EJEMPLO 3: PROCESAMIENTO DINÁMICO DE MÚLTIPLES REGISTROS")
    print("=" * 60)
    
    # Simular datos entrantes
    datos_entrantes = [
        {'nombre': 'Paciente 1', 'edad': 19},
        {'nombre': 'Paciente 2', 'edad': 24},
        {'nombre': 'Paciente 3', 'edad': 25},
        {'nombre': 'Paciente 4', 'edad': 35},
        {'nombre': 'Paciente 5', 'edad': 22},
    ]
    
    print("\nProcesando datos...\n")
    
    resultados = []
    for dato in datos_entrantes:
        # Procesar cada registro individualmente
        resultado = procesar_registro_individual(dato['edad'], dato['nombre'])
        resultados.append(resultado)
        
        print(f"✓ {resultado['nombre']}: edad={resultado['edad']} → "
              f"grupo_edad={resultado['grupo_edad']} ({resultado['etiqueta_grupo']})")
    
    # Convertir a DataFrame para análisis
    df_resultados = pd.DataFrame(resultados)
    print("\nDataFrame consolidado:")
    print(df_resultados)
    print()


def ejemplo_vectorizado():
    """
    Ejemplo de procesamiento vectorizado (más eficiente para grandes volúmenes)
    """
    print("=" * 60)
    print("EJEMPLO 4: PROCESAMIENTO VECTORIZADO (ESCALABLE)")
    print("=" * 60)
    
    # Crear un DataFrame grande
    import numpy as np
    np.random.seed(42)
    
    df = pd.DataFrame({
        'id': range(1, 1001),
        'edad': np.random.randint(18, 65, 1000)
    })
    
    # Transformación vectorizada (más rápida para grandes datasets)
    df['grupo_edad'] = (df['edad'] > 24).astype(int)
    
    print(f"\nDataFrame procesado: {len(df)} registros")
    print("\nPrimeras 10 filas:")
    print(df.head(10))
    
    print("\nDistribución por grupos:")
    distribucion = df['grupo_edad'].value_counts().sort_index()
    print(distribucion)
    print(f"\nGrupo 0 (≤24 años): {distribucion[0]} personas ({distribucion[0]/len(df)*100:.1f}%)")
    print(f"Grupo 1 (>24 años): {distribucion[1]} personas ({distribucion[1]/len(df)*100:.1f}%)")
    print()


def ejemplo_integracion_streamlit():
    """
    Ejemplo de código para integración con Streamlit
    """
    print("=" * 60)
    print("EJEMPLO 5: INTEGRACIÓN CON STREAMLIT")
    print("=" * 60)
    
    print("""
Código de ejemplo para usar en Streamlit:

```python
import streamlit as st
from src.utils.calculos import transformar_edad_a_grupo

# Capturar edad del usuario
edad = st.number_input("Edad", min_value=0, max_value=120, step=1)

# Calcular grupo automáticamente
if edad > 0:
    grupo_edad = transformar_edad_a_grupo(edad)
    
    # Mostrar resultado
    if grupo_edad == 0:
        st.info(f"Grupo de edad: Joven (≤24 años)")
    else:
        st.info(f"Grupo de edad: Adulto (>24 años)")
    
    # Guardar en session_state
    st.session_state['edad'] = edad
    st.session_state['grupo_edad'] = grupo_edad
```
""")


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "EJEMPLOS DE TRANSFORMACIÓN EDAD → GRUPO_EDAD" + " " * 3 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    # Ejecutar todos los ejemplos
    ejemplo_basico()
    ejemplo_datos_multiples()
    ejemplo_streaming_simulado()
    ejemplo_vectorizado()
    ejemplo_integracion_streamlit()
    
    print("=" * 60)
    print("✓ TODOS LOS EJEMPLOS EJECUTADOS CORRECTAMENTE")
    print("=" * 60)
    print()
