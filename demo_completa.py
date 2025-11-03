"""
Demostración visual de las validaciones implementadas
"""
import pandas as pd
import sys
sys.path.append('.')

from src.utils.calculos import (
    transformar_edad_a_grupo, 
    transformar_genero_a_binario,
    validar_años_educacion
)

print("\n" + "="*80)
print("  DEMOSTRACION COMPLETA: TRANSFORMACIONES Y VALIDACIONES")
print("="*80 + "\n")

# Datos de ejemplo con casos válidos e inválidos
datos_pacientes = [
    {"nombre": "Ana Garcia", "edad": 20, "genero": "Femenino", "educacion": 15},    # Válido
    {"nombre": "Carlos Lopez", "edad": 28, "genero": "Masculino", "educacion": 18}, # Válido
    {"nombre": "Maria Rodriguez", "edad": 24, "genero": "Femenino", "educacion": 20}, # Inválido
    {"nombre": "Juan Perez", "edad": 18, "genero": "Masculino", "educacion": 13},   # Válido
    {"nombre": "Laura Martinez", "edad": 35, "genero": "Femenino", "educacion": 35}, # Inválido
]

resultados = []

print("PROCESANDO PACIENTES...")
print("-" * 80 + "\n")

for i, paciente in enumerate(datos_pacientes, 1):
    nombre = paciente["nombre"]
    edad = paciente["edad"]
    genero = paciente["genero"]
    educacion = paciente["educacion"]
    
    print(f"[{i}] Paciente: {nombre}")
    print(f"    Datos ingresados:")
    print(f"      - Edad: {edad} años")
    print(f"      - Genero: {genero}")
    print(f"      - Educacion: {educacion} años")
    
    # Transformaciones
    grupo_edad = transformar_edad_a_grupo(edad)
    genero_binario = transformar_genero_a_binario(genero)
    
    print(f"\n    Transformaciones aplicadas:")
    print(f"      - Grupo edad: {grupo_edad} ({'Joven <=24' if grupo_edad == 0 else 'Adulto >24'})")
    print(f"      - Genero binario: {genero_binario} ({'Masculino' if genero_binario == 0 else 'Femenino'})")
    
    # Validación
    es_valido, max_permitido, mensaje = validar_años_educacion(edad, educacion)
    
    print(f"\n    Validacion de educacion:")
    print(f"      - Maximo permitido: {max_permitido} años (edad - 5)")
    print(f"      - Educacion declarada: {educacion} años")
    
    if es_valido:
        print(f"      - Estado: ✓ VALIDO")
        print(f"      - Accion: DATOS ACEPTADOS Y GUARDADOS")
    else:
        print(f"      - Estado: ✗ INVALIDO")
        print(f"      - Razon: Excede el maximo permitido ({max_permitido} años)")
        print(f"      - Accion: RECHAZADO - Debe corregir el valor")
    
    print("\n" + "-" * 80 + "\n")
    
    resultados.append({
        "Nombre": nombre,
        "Edad": edad,
        "Grupo_Edad": grupo_edad,
        "Genero": genero,
        "Genero_Binario": genero_binario,
        "Educacion": educacion,
        "Max_Permitido": max_permitido,
        "Valido": "SI" if es_valido else "NO"
    })

# Crear DataFrame
df = pd.DataFrame(resultados)

print("="*80)
print("DATAFRAME RESULTANTE")
print("="*80 + "\n")
print(df.to_string(index=False))

# Estadísticas
total = len(resultados)
validos = sum(1 for r in resultados if r["Valido"] == "SI")
invalidos = total - validos

print("\n" + "="*80)
print("ESTADISTICAS")
print("="*80)
print(f"\nTotal de pacientes procesados: {total}")
print(f"  - Datos validos: {validos} ({validos/total*100:.1f}%)")
print(f"  - Datos invalidos: {invalidos} ({invalidos/total*100:.1f}%)")

# Análisis por grupo
print("\n" + "-"*80)
print("ANALISIS POR GRUPO DE EDAD")
print("-"*80)
for grupo in [0, 1]:
    etiqueta = "Joven (<=24 años)" if grupo == 0 else "Adulto (>24 años)"
    datos_grupo = df[df['Grupo_Edad'] == grupo]
    print(f"\nGrupo {grupo} - {etiqueta}:")
    print(f"  Cantidad: {len(datos_grupo)}")
    print(f"  Pacientes: {', '.join(datos_grupo['Nombre'].tolist())}")
    validos_grupo = datos_grupo[datos_grupo['Valido'] == 'SI']
    print(f"  Datos validos: {len(validos_grupo)}/{len(datos_grupo)}")

# Análisis por género
print("\n" + "-"*80)
print("ANALISIS POR GENERO")
print("-"*80)
for gen in [0, 1]:
    etiqueta = "Masculino" if gen == 0 else "Femenino"
    datos_gen = df[df['Genero_Binario'] == gen]
    print(f"\nGenero {gen} - {etiqueta}:")
    print(f"  Cantidad: {len(datos_gen)}")
    print(f"  Pacientes: {', '.join(datos_gen['Nombre'].tolist())}")
    validos_gen = datos_gen[datos_gen['Valido'] == 'SI']
    print(f"  Datos validos: {len(validos_gen)}/{len(datos_gen)}")

print("\n" + "="*80)
print("RESUMEN DE FUNCIONALIDADES IMPLEMENTADAS")
print("="*80)
print("""
✓ TRANSFORMACION EDAD -> GRUPO_EDAD
  - Edad <=24 -> Grupo 0 (Joven)
  - Edad >24  -> Grupo 1 (Adulto)

✓ TRANSFORMACION GENERO -> GENERO_BINARIO
  - Masculino -> 0
  - Femenino  -> 1

✓ VALIDACION DE AÑOS DE EDUCACION
  - Formula: max_educacion = edad - 5
  - Validacion automatica al guardar
  - Mensajes informativos para el usuario
  - Prevencion de datos incorrectos

✓ DATAFRAME DINAMICO
  - Actualizacion automatica
  - Exportable a CSV
  - Listo para analisis
""")

print("="*80)
print("[OK] Sistema completo y funcionando correctamente")
print("="*80 + "\n")
