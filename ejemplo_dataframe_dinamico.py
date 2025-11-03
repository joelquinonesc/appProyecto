"""
Ejemplo de uso del DataFrame dinámico
Demuestra cómo se van agregando datos conforme el usuario llena los formularios
"""

import pandas as pd
import sys
sys.path.append('.')

from src.utils.calculos import transformar_edad_a_grupo, transformar_genero_a_binario


def simular_llenado_formulario():
    """
    Simula el llenado progresivo de formularios y muestra cómo se actualiza el DataFrame
    """
    print("=" * 80)
    print("SIMULACIÓN DE LLENADO DE FORMULARIOS - ACTUALIZACIÓN DINÁMICA DEL DATAFRAME")
    print("=" * 80)
    print()
    
    # Inicializar DataFrame vacío
    df = pd.DataFrame(columns=[
        'timestamp',
        'nombre',
        'edad',
        'grupo_edad',
        'genero',
        'genero_binario',
        'años_educacion',
        'lte12_puntaje',
        'sf12_fisica',
        'sf12_mental',
        'hads_ansiedad',
        'hads_depresion',
        'zsas_puntaje'
    ])
    
    print("📋 PASO 1: DataFrame inicializado (vacío)")
    print(f"Columnas: {list(df.columns)}")
    print(f"Registros: {len(df)}")
    print()
    
    # ===== FORMULARIO 1: DATOS DEMOGRÁFICOS =====
    print("-" * 80)
    print("👤 FORMULARIO 1: DATOS DEMOGRÁFICOS")
    print("-" * 80)
    
    # Simulamos que el usuario ingresa sus datos
    datos_demograficos = {
        'timestamp': '20251102_143000',
        'nombre': 'Ana García',
        'edad': 22,
        'genero': 'Femenino',
        'años_educacion': 16
    }
    
    # Aplicar transformaciones automáticamente
    datos_demograficos['grupo_edad'] = transformar_edad_a_grupo(datos_demograficos['edad'])
    datos_demograficos['genero_binario'] = transformar_genero_a_binario(datos_demograficos['genero'])
    
    print(f"\nUsuario ingresó:")
    print(f"  Nombre: {datos_demograficos['nombre']}")
    print(f"  Edad: {datos_demograficos['edad']}")
    print(f"  → Grupo edad: {datos_demograficos['grupo_edad']} {'(Joven ≤24 años)' if datos_demograficos['grupo_edad'] == 0 else '(Adulto >24 años)'}")
    print(f"  Género: {datos_demograficos['genero']}")
    print(f"  → Género binario: {datos_demograficos['genero_binario']} {'(Masculino=0)' if datos_demograficos['genero_binario'] == 0 else '(Femenino=1)'}")
    print(f"  Años educación: {datos_demograficos['años_educacion']}")
    
    # Agregar registro al DataFrame
    df = pd.concat([df, pd.DataFrame([datos_demograficos])], ignore_index=True)
    
    print(f"\n✅ DataFrame actualizado - Ahora tiene {len(df)} registro(s)")
    print("\nDataFrame actual:")
    print(df[['nombre', 'edad', 'grupo_edad', 'genero', 'genero_binario', 'años_educacion']])
    print()
    
    # ===== FORMULARIO 2: EVENTOS VITALES (LTE-12) =====
    print("-" * 80)
    print("📝 FORMULARIO 2: EVENTOS VITALES (LTE-12)")
    print("-" * 80)
    
    # Simulamos respuestas a las 12 preguntas (Sí = 1, No = 0)
    respuestas_lte = [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
    puntaje_lte = sum(respuestas_lte)
    
    print(f"\nUsuario respondió 12 preguntas sobre eventos estresantes")
    print(f"Eventos experimentados: {puntaje_lte} de 12")
    
    # Actualizar el DataFrame
    df.at[0, 'lte12_puntaje'] = puntaje_lte
    
    print(f"\n✅ DataFrame actualizado")
    print("\nDataFrame actual:")
    print(df[['nombre', 'edad', 'grupo_edad', 'lte12_puntaje']])
    print()
    
    # ===== FORMULARIO 3: SF-12 =====
    print("-" * 80)
    print("🏥 FORMULARIO 3: SF-12 (SALUD)")
    print("-" * 80)
    
    sf12_fisica = 45.2
    sf12_mental = 52.8
    
    print(f"\nPuntajes calculados del SF-12:")
    print(f"  Salud Física: {sf12_fisica}")
    print(f"  Salud Mental: {sf12_mental}")
    
    # Actualizar el DataFrame
    df.at[0, 'sf12_fisica'] = sf12_fisica
    df.at[0, 'sf12_mental'] = sf12_mental
    
    print(f"\n✅ DataFrame actualizado")
    print("\nDataFrame actual:")
    print(df[['nombre', 'grupo_edad', 'lte12_puntaje', 'sf12_fisica', 'sf12_mental']])
    print()
    
    # ===== FORMULARIO 4: HADS =====
    print("-" * 80)
    print("😰 FORMULARIO 4: HADS (ANSIEDAD Y DEPRESIÓN)")
    print("-" * 80)
    
    hads_ansiedad = 8
    hads_depresion = 6
    
    print(f"\nPuntajes HADS:")
    print(f"  Ansiedad: {hads_ansiedad}")
    print(f"  Depresión: {hads_depresion}")
    
    # Actualizar el DataFrame
    df.at[0, 'hads_ansiedad'] = hads_ansiedad
    df.at[0, 'hads_depresion'] = hads_depresion
    
    print(f"\n✅ DataFrame actualizado")
    print("\nDataFrame actual:")
    print(df[['nombre', 'grupo_edad', 'lte12_puntaje', 'hads_ansiedad', 'hads_depresion']])
    print()
    
    # ===== FORMULARIO 5: ZSAS =====
    print("-" * 80)
    print("😟 FORMULARIO 5: ZSAS (ESCALA DE ANSIEDAD)")
    print("-" * 80)
    
    zsas_puntaje = 48
    
    print(f"\nPuntaje ZSAS normalizado: {zsas_puntaje}")
    
    # Actualizar el DataFrame
    df.at[0, 'zsas_puntaje'] = zsas_puntaje
    
    print(f"\n✅ DataFrame actualizado")
    print("\nDataFrame COMPLETO:")
    print(df)
    print()
    
    # ===== RESUMEN FINAL =====
    print("=" * 80)
    print("📊 RESUMEN FINAL - DATAFRAME COMPLETO")
    print("=" * 80)
    print()
    
    print(f"Total de registros: {len(df)}")
    print(f"Total de columnas: {len(df.columns)}")
    print()
    
    print("Datos recolectados:")
    print(f"  ✓ Datos demográficos: {datos_demograficos['nombre']}, {datos_demograficos['edad']} años, Grupo {datos_demograficos['grupo_edad']}")
    print(f"  ✓ LTE-12: {puntaje_lte} eventos estresantes")
    print(f"  ✓ SF-12: Física={sf12_fisica}, Mental={sf12_mental}")
    print(f"  ✓ HADS: Ansiedad={hads_ansiedad}, Depresión={hads_depresion}")
    print(f"  ✓ ZSAS: {zsas_puntaje}")
    print()
    
    # Mostrar estadísticas del grupo_edad
    print("-" * 80)
    print("📈 ANÁLISIS DEL GRUPO DE EDAD")
    print("-" * 80)
    print(f"\nPaciente: {datos_demograficos['nombre']}")
    print(f"Edad: {datos_demograficos['edad']} años")
    print(f"Clasificación: Grupo {datos_demograficos['grupo_edad']} - {'Joven (≤24 años)' if datos_demograficos['grupo_edad'] == 0 else 'Adulto (>24 años)'}")
    print()
    
    # Mostrar el DataFrame transpuesto para mejor visualización
    print("-" * 80)
    print("📋 VISTA TRANSPUESTA DEL DATAFRAME (para mejor visualización)")
    print("-" * 80)
    print()
    df_transpuesto = df.T
    df_transpuesto.columns = ['Paciente 1']
    print(df_transpuesto)
    print()
    
    print("=" * 80)
    print("✅ SIMULACIÓN COMPLETADA")
    print("=" * 80)
    print()
    print("💡 En la aplicación real de Streamlit:")
    print("   - Cada formulario actualiza automáticamente el DataFrame")
    print("   - La transformación edad → grupo_edad se aplica en tiempo real")
    print("   - Todos los datos quedan disponibles para análisis posterior")
    print("   - El DataFrame se puede exportar a CSV en cualquier momento")
    print()


def ejemplo_multiples_pacientes():
    """
    Ejemplo con múltiples pacientes para mostrar el DataFrame con varios registros
    """
    print("\n\n")
    print("=" * 80)
    print("EJEMPLO 2: MÚLTIPLES PACIENTES EN EL DATAFRAME")
    print("=" * 80)
    print()
    
    # Crear datos de ejemplo para varios pacientes
    pacientes = [
        {'nombre': 'Ana García', 'edad': 22, 'genero': 'Femenino', 'años_educacion': 16, 'lte12': 3},
        {'nombre': 'Carlos López', 'edad': 28, 'genero': 'Masculino', 'años_educacion': 18, 'lte12': 1},
        {'nombre': 'María Rodríguez', 'edad': 24, 'genero': 'Femenino', 'años_educacion': 14, 'lte12': 5},
        {'nombre': 'Juan Pérez', 'edad': 35, 'genero': 'Masculino', 'años_educacion': 12, 'lte12': 2},
    ]
    
    # Crear DataFrame
    df_list = []
    for i, p in enumerate(pacientes):
        df_list.append({
            'timestamp': f'2025110{i+1}_14{30+i*5:02d}00',
            'nombre': p['nombre'],
            'edad': p['edad'],
            'grupo_edad': transformar_edad_a_grupo(p['edad']),
            'genero': p['genero'],
            'genero_binario': transformar_genero_a_binario(p['genero']),
            'años_educacion': p['años_educacion'],
            'lte12_puntaje': p['lte12']
        })
    
    df = pd.DataFrame(df_list)
    
    print("DataFrame con 4 pacientes:")
    print(df)
    print()
    
    print("-" * 80)
    print("ANÁLISIS POR GRUPO DE EDAD")
    print("-" * 80)
    print()
    
    grupos = df.groupby('grupo_edad')
    for grupo, data in grupos:
        etiqueta = 'Joven (≤24 años)' if grupo == 0 else 'Adulto (>24 años)'
        print(f"\nGrupo {grupo} - {etiqueta}:")
        print(f"  Pacientes: {len(data)}")
        print(f"  Edad promedio: {data['edad'].mean():.1f} años")
        print(f"  Eventos estresantes promedio: {data['lte12_puntaje'].mean():.1f}")
        print(f"  Nombres: {', '.join(data['nombre'].tolist())}")
    
    print()
    print("=" * 80)


if __name__ == "__main__":
    print("\n")
    print("=" * 80)
    print("         DEMOSTRACION DE DATAFRAME DINAMICO")
    print("=" * 80)
    print()
    
    simular_llenado_formulario()
    ejemplo_multiples_pacientes()
    
    print("\n💾 Los datos se van actualizando conforme el usuario llena cada formulario")
    print("📊 El grupo_edad se calcula automáticamente al ingresar la edad")
    print("✨ Todo queda listo para análisis y exportación\n")
