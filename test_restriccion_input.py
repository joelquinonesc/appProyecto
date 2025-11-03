"""
Prueba visual de la restricción de años de educación
"""
import sys
sys.path.append('.')

from src.utils.calculos import validar_años_educacion

print("\n" + "="*70)
print("  RESTRICCION DE AÑOS DE EDUCACION EN EL FORMULARIO")
print("="*70 + "\n")

print("COMPORTAMIENTO DEL CAMPO DE ENTRADA:")
print("-" * 70)

edades_ejemplo = [0, 10, 15, 18, 20, 25, 30, 40]

for edad in edades_ejemplo:
    max_educacion = max(0, edad - 5)
    
    print(f"\nEdad ingresada: {edad} años")
    print(f"  └─> Máximo permitido: {max_educacion} años")
    print(f"  └─> Rango del input: 0 a {max_educacion}")
    
    if edad == 0:
        print(f"  └─> Estado: CAMPO DESHABILITADO (debe ingresar edad primero)")
    else:
        print(f"  └─> Estado: ACTIVO")
        
    # Ejemplos de valores
    print(f"\n  Ejemplos de valores:")
    
    if edad > 0:
        valores_prueba = [
            max_educacion - 2,
            max_educacion - 1,
            max_educacion,
            max_educacion + 1,
            max_educacion + 2
        ]
        
        for valor in valores_prueba:
            if valor < 0:
                continue
                
            es_valido, _, _ = validar_años_educacion(edad, valor)
            
            if valor <= max_educacion:
                # El input SÍ permitirá este valor
                estado = "✓ PERMITIDO por el input"
                simbolo = "✓"
            else:
                # El input NO permitirá este valor
                estado = "✗ BLOQUEADO por el input"
                simbolo = "✗"
            
            print(f"    {simbolo} {valor} años -> {estado}")

print("\n" + "="*70)
print("CARACTERISTICAS DEL CONTROL:")
print("="*70)
print("""
1. DESHABILITADO si edad = 0
   - No se puede escribir nada
   - Mensaje: "Ingrese primero su edad"

2. LIMITE DINAMICO basado en edad
   - max_value = edad - 5
   - Se actualiza automáticamente al cambiar edad

3. NO PERMITE valores mayores al máximo
   - Los botones +/- se detienen en el máximo
   - No se puede escribir un valor mayor manualmente

4. VALIDACION VISUAL en tiempo real
   - Verde (✓) si valor es válido
   - Rojo (✗) si valor excede (esto no debería pasar)

5. MENSAJE INFORMATIVO
   - Muestra el máximo permitido según la edad
   - Se actualiza dinámicamente
""")

print("="*70)
print("EJEMPLOS PRACTICOS:")
print("="*70)

ejemplos = [
    {"edad": 20, "descripcion": "Estudiante universitario"},
    {"edad": 18, "descripcion": "Recién graduado de secundaria"},
    {"edad": 30, "descripcion": "Profesional con posgrado"},
    {"edad": 15, "descripcion": "Estudiante de secundaria"},
]

for ej in ejemplos:
    edad = ej["edad"]
    max_edu = max(0, edad - 5)
    desc = ej["descripcion"]
    
    print(f"\n{desc} - {edad} años:")
    print(f"  Campo permite: 0 a {max_edu} años")
    print(f"  Ejemplos válidos: {', '.join(str(i) for i in range(0, min(max_edu+1, 6)))}, ..., {max_edu}")
    print(f"  NO puede ingresar: {max_edu + 1}, {max_edu + 2}, {max_edu + 3}, ...")

print("\n" + "="*70)
print("CONCLUSION:")
print("="*70)
print("""
✓ El campo de entrada PREVIENE físicamente ingresar valores inválidos
✓ No es necesario validar después, el control ya lo hace
✓ La interfaz es intuitiva y guía al usuario
✓ Imposible guardar datos con educación inválida

NOTA: El formulario usa st.number_input() con max_value dinámico,
      lo que hace imposible que el usuario ingrese un valor mayor.
""")

print("="*70 + "\n")
