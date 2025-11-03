# Validación de Años de Educación Formal

## ✅ Nueva Funcionalidad Implementada

Se ha implementado una **validación automática** para los años de educación formal con mensajes informativos para el usuario.

---

## 📐 Regla de Validación

```
max_años_educacion = edad - 5
```

### Ejemplos:
- **Edad 20 años** → Máximo 15 años de educación
- **Edad 18 años** → Máximo 13 años de educación
- **Edad 25 años** → Máximo 20 años de educación
- **Edad 30 años** → Máximo 25 años de educación

---

## 📁 Archivos Modificados

### 1. **`src/utils/calculos.py`**
✅ Nueva función `validar_años_educacion(edad, años_educacion)`
- Valida que los años de educación cumplan con la regla
- Retorna: `(es_valido, max_permitido, mensaje)`

```python
def validar_años_educacion(edad, años_educacion):
    """
    Valida que los años de educación no excedan el máximo permitido.
    Regla: años_educacion <= (edad - 5)
    """
    max_permitido = max(0, edad - 5)
    es_valido = años_educacion <= max_permitido
    return es_valido, max_permitido, mensaje
```

### 2. **`src/pages/demograficos.py`**
✅ Cálculo dinámico del máximo permitido
✅ Mensaje informativo mostrando el límite según la edad
✅ Validación al momento de guardar
✅ Mensajes de error descriptivos

**Características implementadas:**
- ℹ️ Mensaje informativo: "Según tu edad (X años), puedes tener un máximo de Y años de educación formal"
- 🔒 Campo de entrada limitado automáticamente al máximo permitido
- ❌ Validación al guardar con mensaje de error claro
- ✅ Mensaje de éxito al guardar correctamente

---

## 🎨 Interfaz de Usuario

### Mensaje Informativo
Cuando el usuario ingresa su edad, ve automáticamente:

```
ℹ️ Según tu edad (20 años), puedes tener un máximo de 15 años 
   de educación formal (edad - 5).
```

### Campo de Entrada
- **Min:** 0
- **Max:** Calculado dinámicamente (edad - 5)
- **Ayuda:** "Máximo permitido: X años (edad - 5)"

### Mensajes de Error
Si intenta ingresar un valor inválido:
```
❌ Los años de educación formal (16) no pueden ser más de 15 años 
   (edad - 5). Por favor, corrija el valor.
```

### Mensaje de Éxito
Al guardar correctamente:
```
✅ Datos guardados correctamente para [Nombre]
```

---

## 🧪 Tests Disponibles

### Test 1: `test_validacion_educacion.py`
Prueba exhaustiva de la función de validación con 8 casos de prueba.

```bash
python test_validacion_educacion.py
```

**Casos probados:**
- ✓ Edad 20, Educación 15 → VÁLIDO
- ✓ Edad 20, Educación 16 → INVÁLIDO
- ✓ Edad 25, Educación 18 → VÁLIDO
- ✓ Edad 18, Educación 13 → VÁLIDO
- ✓ Edad 18, Educación 14 → INVÁLIDO
- Y más...

### Test 2: `test_transformaciones.py`
Prueba integrada con todas las transformaciones.

```bash
python test_transformaciones.py
```

---

## 📊 Ejemplo Práctico

### Caso Válido
```
Paciente: Ana García
Edad: 20 años
Educación declarada: 15 años
Máximo permitido: 15 años
Estado: ✓ ACEPTADO
```

### Caso Inválido
```
Paciente: Juan Pérez
Edad: 22 años
Educación declarada: 20 años
Máximo permitido: 17 años
Estado: ✗ RECHAZADO
NOTA: Debe reducir los años de educación a 17 o menos
```

---

## 🔄 Flujo de Validación

```
Usuario ingresa edad
    ↓
Se calcula max_educacion = edad - 5
    ↓
Se muestra mensaje informativo
    ↓
Campo de entrada se limita automáticamente
    ↓
Usuario ingresa años de educación
    ↓
Al hacer clic en "Guardar":
    ↓
Se valida: años_educacion <= max_educacion
    ↓
Si válido → ✅ Guardar datos
Si inválido → ❌ Mostrar error
```

---

## 💡 Justificación

Esta validación asegura que los datos sean **realistas y coherentes**:

- Una persona de 20 años no podría tener 18 años de educación formal
- Se asume que la educación formal comienza aproximadamente a los 5 años
- Previene errores de captura de datos
- Mejora la calidad de los datos recolectados

---

## 📈 Integración con DataFrame

La validación se integra completamente con el DataFrame dinámico:

```python
# Columnas del DataFrame
- edad               # Edad en años
- años_educacion     # Años de educación (validados)
- max_educacion      # Máximo permitido (calculado)
- educacion_valida   # True/False (validación)
```

---

## ✅ Estado de Implementación

✅ **Función de validación** creada en `calculos.py`  
✅ **Interfaz actualizada** con mensajes informativos  
✅ **Validación en tiempo real** al cambiar edad  
✅ **Validación al guardar** con mensajes de error  
✅ **Tests completos** y funcionando  
✅ **Documentación** completa  

---

## 🚀 Cómo Usar

### En la Aplicación
1. Abrir el formulario de Datos Demográficos
2. Ingresar la edad
3. Ver el mensaje informativo con el máximo permitido
4. Ingresar años de educación (dentro del límite)
5. Guardar datos

### En Código
```python
from src.utils.calculos import validar_años_educacion

edad = 20
años_educacion = 15

es_valido, max_permitido, mensaje = validar_años_educacion(edad, años_educacion)

if es_valido:
    print(f"✓ Datos válidos. Máximo: {max_permitido}")
else:
    print(f"✗ Error: {mensaje}")
```

---

## 🎯 Resultados

- ✅ Validación automática implementada
- ✅ Mensajes claros y descriptivos
- ✅ Prevención de datos incorrectos
- ✅ Mejor experiencia de usuario
- ✅ Datos más confiables para análisis

---

## 📝 Notas Adicionales

- La validación es **no intrusiva**: permite valores válidos sin restricción
- Los mensajes son **descriptivos**: explican claramente el problema
- La interfaz es **adaptativa**: se ajusta automáticamente según la edad
- Los tests son **exhaustivos**: cubren casos límite y normales

---

**Para ejecutar la aplicación:**
```bash
python run.py
```

**Para ejecutar los tests:**
```bash
python test_validacion_educacion.py
python test_transformaciones.py
```
