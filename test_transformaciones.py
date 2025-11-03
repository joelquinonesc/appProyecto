"""
Script de prueba rápida para transformaciones
"""
import pandas as pd
import sys
sys.path.append('.')

from src.utils.calculos import transformar_edad_a_grupo, transformar_genero_a_binario

print("\n" + "="*60)
print("  PRUEBA DE TRANSFORMACIONES")
print("="*60 + "\n")

# Datos de ejemplo
datos = {
    'nombre': ['Ana Garcia', 'Carlos Lopez', 'Maria Rodriguez', 'Juan Perez'],
    'edad': [22, 28, 24, 35],
    'genero': ['Femenino', 'Masculino', 'Femenino', 'Masculino']
}

df = pd.DataFrame(datos)

# Aplicar transformaciones
df['grupo_edad'] = df['edad'].apply(transformar_edad_a_grupo)
df['genero_binario'] = df['genero'].apply(transformar_genero_a_binario)

print("DataFrame con transformaciones:\n")
print(df)

print("\n" + "="*60)
print("REGLAS APLICADAS:")
print("  - Edad: 0 (Joven <=24 años) | 1 (Adulto >24 años)")
print("  - Genero: 0 (Masculino) | 1 (Femenino)")
print("="*60 + "\n")

# Mostrar resumen
print("RESUMEN POR GRUPO DE EDAD:")
for grupo in [0, 1]:
    etiqueta = "Joven (<=24)" if grupo == 0 else "Adulto (>24)"
    datos_grupo = df[df['grupo_edad'] == grupo]
    print(f"\nGrupo {grupo} - {etiqueta}:")
    print(f"  Cantidad: {len(datos_grupo)}")
    print(f"  Nombres: {', '.join(datos_grupo['nombre'].tolist())}")

print("\nRESUMEN POR GENERO:")
for gen in [0, 1]:
    etiqueta = "Masculino" if gen == 0 else "Femenino"
    datos_gen = df[df['genero_binario'] == gen]
    print(f"\nGenero {gen} - {etiqueta}:")
    print(f"  Cantidad: {len(datos_gen)}")
    print(f"  Nombres: {', '.join(datos_gen['nombre'].tolist())}")

print("\n" + "="*60)
print("[OK] Transformaciones aplicadas correctamente")
print("="*60 + "\n")
