# Actualización: Transformación de Género a Variable Binaria

## ✅ Cambios Implementados

Se ha agregado la transformación de la variable **género** a una variable binaria en el DataFrame:

### 📊 Nueva Regla de Transformación

```python
genero_binario = 0  # Si Masculino
genero_binario = 1  # Si Femenino
```

---

## 📁 Archivos Modificados

### 1. **`src/utils/calculos.py`**
✅ Agregada función `transformar_genero_a_binario(genero)`
- Convierte "Masculino" → 0
- Convierte "Femenino" → 1
- Maneja variaciones: 'masculino', 'hombre', 'male', 'm'

### 2. **`src/pages/demograficos.py`**
✅ Importa `transformar_genero_a_binario`
✅ Calcula `genero_binario` automáticamente al guardar datos
✅ Agrega campo `genero_binario` al diccionario de datos

### 3. **`src/utils/dataframe_manager.py`**
✅ Agregada columna `genero_binario` al DataFrame
✅ Actualización automática del campo en registro demográfico

### 4. **Archivos de Ejemplo**
✅ `ejemplo_transformacion_edad.py` - Actualizado con transformación de género
✅ `ejemplo_dataframe_dinamico.py` - Incluye genero_binario
✅ `test_transformaciones.py` - Nuevo script de prueba rápida

---

## 📊 Estructura Actualizada del DataFrame

```python
Columnas del DataFrame:
- timestamp          # ID de sesión
- nombre             # Nombre del paciente
- edad               # Edad en años
- grupo_edad         # 0 (<=24) o 1 (>24)
- genero             # "Masculino" o "Femenino"
- genero_binario     # 0 (Masculino) o 1 (Femenino) ← NUEVO
- años_educacion     # Años de educación formal
- lte12_puntaje      # Puntaje eventos vitales
- sf12_fisica        # Salud física
- sf12_mental        # Salud mental
- hads_ansiedad      # Nivel de ansiedad
- hads_depresion     # Nivel de depresión
- zsas_puntaje       # Escala de ansiedad
- gen_prkca          # Gen PRKCA
- gen_tcf4           # Gen TCF4
- gen_cdh20          # Gen CDH20
```

---

## 🎯 Ejemplo de Uso

```python
from src.utils.calculos import transformar_genero_a_binario

# Transformación automática
genero = "Masculino"
genero_binario = transformar_genero_a_binario(genero)  # → 0

genero = "Femenino"
genero_binario = transformar_genero_a_binario(genero)  # → 1
```

---

## 📈 Ejemplo de DataFrame Resultante

```
            nombre  edad     genero  grupo_edad  genero_binario
0       Ana Garcia    22   Femenino           0               1
1     Carlos Lopez    28  Masculino           1               0
2  Maria Rodriguez    24   Femenino           0               1
3       Juan Perez    35  Masculino           1               0
```

---

## 🧪 Verificación

Para probar las transformaciones:

```bash
python test_transformaciones.py
```

Este script muestra:
- ✅ DataFrame con ambas transformaciones aplicadas
- ✅ Reglas de transformación
- ✅ Resumen por grupo de edad
- ✅ Resumen por género

---

## 🔄 Integración en Streamlit

Cuando un usuario llena el formulario demográfico:

1. **Ingresa género**: Selecciona "Masculino" o "Femenino"
2. **Transformación automática**: Se calcula `genero_binario`
3. **Almacenamiento**: Ambos valores se guardan en el DataFrame:
   - `genero`: Valor original ("Masculino" o "Femenino")
   - `genero_binario`: Valor numérico (0 o 1)

---

## 📝 Resumen de Transformaciones Aplicadas

| Variable Original | Variable Transformada | Regla |
|-------------------|----------------------|-------|
| edad              | grupo_edad           | ≤24 → 0, >24 → 1 |
| genero            | genero_binario       | Masculino → 0, Femenino → 1 |

---

## ✅ Estado Actual

✅ **Transformación edad → grupo_edad** (implementada anteriormente)  
✅ **Transformación genero → genero_binario** (recién implementada)  
✅ **DataFrame dinámico** actualizado con ambas transformaciones  
✅ **Ejemplos** actualizados y funcionando  
✅ **Tests** disponibles para verificación  

---

## 🎉 Listo para Usar

La aplicación ahora transforma automáticamente:
- ✅ Edad a grupo de edad binario
- ✅ Género a variable binaria
- ✅ Almacena ambas transformaciones en el DataFrame
- ✅ Disponible para análisis estadístico inmediato

**Ejecutar aplicación:**
```bash
python run.py
```

**Ejecutar tests:**
```bash
python test_transformaciones.py
```
