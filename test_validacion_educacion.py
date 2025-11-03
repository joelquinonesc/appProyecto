"""
Script de prueba para validación de años de educación
"""
import pandas as pd
import sys
sys.path.append('.')

from src.utils.calculos import validar_años_educacion

print("\n" + "="*70)
print("  PRUEBA DE VALIDACION: AÑOS DE EDUCACION FORMAL")
print("="*70 + "\n")

# Casos de prueba
casos = [
    {"edad": 20, "años_educacion": 15, "esperado": True},   # Válido: 20-5=15
    {"edad": 20, "años_educacion": 16, "esperado": False},  # Inválido: excede
    {"edad": 25, "años_educacion": 18, "esperado": True},   # Válido: 25-5=20
    {"edad": 30, "años_educacion": 20, "esperado": True},   # Válido: 30-5=25
    {"edad": 18, "años_educacion": 13, "esperado": True},   # Válido: 18-5=13
    {"edad": 18, "años_educacion": 14, "esperado": False},  # Inválido: excede
    {"edad": 10, "años_educacion": 3, "esperado": True},    # Válido: 10-5=5
    {"edad": 40, "años_educacion": 30, "esperado": True},   # Válido: 40-5=35
]

print("REGLA: años_educacion <= (edad - 5)")
print("="*70 + "\n")

resultados = []
for i, caso in enumerate(casos, 1):
    edad = caso["edad"]
    años_edu = caso["años_educacion"]
    esperado = caso["esperado"]
    
    es_valido, max_permitido, mensaje = validar_años_educacion(edad, años_edu)
    
    # Verificar si el resultado coincide con lo esperado
    exito = "✓ PASS" if (es_valido == esperado) else "✗ FAIL"
    
    print(f"Caso {i}: Edad={edad}, Educacion={años_edu}")
    print(f"  Max permitido: {max_permitido} años")
    print(f"  Resultado: {'VALIDO' if es_valido else 'INVALIDO'}")
    print(f"  {mensaje}")
    print(f"  Test: {exito}")
    print()
    
    resultados.append({
        "Caso": i,
        "Edad": edad,
        "Educacion": años_edu,
        "Max_Permitido": max_permitido,
        "Valido": es_valido,
        "Test": "PASS" if (es_valido == esperado) else "FAIL"
    })

# Resumen en DataFrame
df = pd.DataFrame(resultados)

print("="*70)
print("RESUMEN DE PRUEBAS")
print("="*70)
print(df.to_string(index=False))

# Contar resultados
total = len(resultados)
passed = sum(1 for r in resultados if r["Test"] == "PASS")
failed = total - passed

print("\n" + "="*70)
print(f"RESULTADO FINAL: {passed}/{total} pruebas exitosas")
if failed == 0:
    print("✓ TODAS LAS PRUEBAS PASARON")
else:
    print(f"✗ {failed} PRUEBAS FALLARON")
print("="*70 + "\n")

# Ejemplos prácticos
print("="*70)
print("EJEMPLOS PRACTICOS")
print("="*70 + "\n")

ejemplos = [
    {"nombre": "Ana Garcia", "edad": 20, "educacion": 15},
    {"nombre": "Carlos Lopez", "edad": 28, "educacion": 18},
    {"nombre": "Maria Rodriguez", "edad": 35, "educacion": 25},
    {"nombre": "Juan Perez", "edad": 22, "educacion": 20},  # Este es inválido
]

for ej in ejemplos:
    nombre = ej["nombre"]
    edad = ej["edad"]
    edu = ej["educacion"]
    
    es_valido, max_p, msg = validar_años_educacion(edad, edu)
    
    print(f"Paciente: {nombre}")
    print(f"  Edad: {edad} años")
    print(f"  Educacion declarada: {edu} años")
    print(f"  Maximo permitido: {max_p} años")
    print(f"  Estado: {'✓ ACEPTADO' if es_valido else '✗ RECHAZADO'}")
    if not es_valido:
        print(f"  NOTA: Debe reducir los años de educacion a {max_p} o menos")
    print()

print("="*70)
print("INFORMACION")
print("="*70)
print("\nEsta validacion asegura que los datos sean realistas:")
print("- Una persona de 20 años puede tener maximo 15 años de educacion")
print("- Una persona de 18 años puede tener maximo 13 años de educacion")
print("- Formula: max_educacion = edad - 5")
print("\n" + "="*70 + "\n")
