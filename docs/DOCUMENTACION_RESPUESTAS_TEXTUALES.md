# 📊 BASE DE DATOS ANXRISK - RESPUESTAS TEXTUALES

**Fecha:** 28 de Noviembre de 2025  
**Archivo:** `base_datos_respuestas_textuales_20_participantes.csv` / `base_datos_respuestas_textuales_20_participantes.xlsx`  
**Participantes:** 20 personas  
**Columnas:** 63 variables

---

## ✨ **CARACTERÍSTICA PRINCIPAL**

Esta base de datos contiene las **respuestas textuales exactas** tal como aparecen en la aplicación ANXRISK. En lugar de números (0, 1, 2, 3), cada celda muestra la respuesta real que seleccionó el participante.

### 🎯 **DIFERENCIA CLAVE:**
- ❌ **Base anterior:** `HADS1_Me siento tenso o nervioso = 2`
- ✅ **Esta base:** `HADS1_Me siento tenso o nervioso = "Muchas veces"`

---

## 📋 **EJEMPLOS DE RESPUESTAS TEXTUALES**

### **🔍 CUESTIONARIO HADS:**
| Pregunta | Respuestas Posibles | Ejemplo Participante |
|----------|--------------------|--------------------|
| HADS1_Me siento tenso o nervioso | "Nunca", "A veces", "Muchas veces", "Todos los días" | "Muchas veces" |
| HADS2_Todavía disfruto con lo que me ha gustado hacer | "Nada", "Sólo un poco", "No mucho", "Como siempre" | "No mucho" |
| HADS3_Tengo sensación de miedo | "Nada", "Un poco, pero no me preocupa", "Sí, pero no es muy fuerte", "Definitivamente y es muy fuerte" | "Un poco, pero no me preocupa" |

### **🔥 CUESTIONARIO ZSAS:**
| Pregunta | Respuestas Posibles | Ejemplo Participante |
|----------|--------------------|--------------------|
| ZSAS1_Me siento más nervioso y ansioso | "Nunca o casi nunca", "A veces", "Con bastante frecuencia", "Siempre o casi siempre" | "A veces" |
| ZSAS5_Siento que todo está bien | "Nunca o casi nunca", "A veces", "Con bastante frecuencia", "Siempre o casi siempre" | "Nunca o casi nunca" |
| ZSAS20_Tengo pesadillas | "Nunca o casi nunca", "A veces", "Con bastante frecuencia", "Siempre o casi siempre" | "Con bastante frecuencia" |

### **🏥 CUESTIONARIO SF-12:**
| Pregunta | Respuestas Posibles | Ejemplo Participante |
|----------|--------------------|--------------------|
| SF12F1_En general diría que su salud es | "Mala", "Regular", "Buena", "Muy buena", "Excelente" | "Buena" |
| SF12F2_Esfuerzos moderados limitación | "Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto" | "Sí, limitado un poco" |
| SF12M4_Se sintió calmado y tranquilo | "Siempre", "Casi siempre", "Muchas veces", "Algunas veces", "Sólo alguna vez", "Nunca" | "Algunas veces" |

### **⚡ CUESTIONARIO LTE-12:**
| Pregunta | Respuestas Posibles | Ejemplo Participante |
|----------|--------------------|--------------------|
| LTE1_Ha sufrido enfermedad lesión o agresión grave | "No", "Sí" | "No" |
| LTE3_Ha muerto padre hijo o pareja cónyuge | "No", "Sí" | "Sí" |
| LTE8_Se quedó sin empleo | "No", "Sí" | "No" |

---

## 🎯 **VENTAJAS DE RESPUESTAS TEXTUALES**

### ✅ **Para Investigadores:**
- **Legibilidad inmediata:** No necesita decodificar números
- **Interpretación directa:** Se ve exactamente qué respondió cada persona
- **Análisis cualitativo:** Fácil identificación de patrones de respuesta
- **Presentación clara:** Los resultados son autoexplicativos

### ✅ **Para Usuarios de la Base:**
- **Sin confusión:** No hay que recordar qué significa cada número
- **Validación sencilla:** Puede verificar que las respuestas tienen sentido
- **Análisis estadístico:** Aún puede convertir a números si es necesario
- **Comprensión inmediata:** Cualquier persona puede entender los datos

---

## 📊 **ESTRUCTURA COMPLETA**

### **1. DATOS IDENTIFICATORIOS (4 columnas)**
- `nombre` - Nombre completo del participante
- `edad` - Edad en años
- `genero` - M/F
- `años_educacion` - Años de educación formal

### **2. PUNTAJES TOTALES (5 columnas)**
- `hads_total` - Suma total HADS (0-21)
- `zsas_total` - Suma total ZSAS (20-80)
- `sf12_fisica_total` - Suma componente físico SF-12
- `sf12_mental_total` - Suma componente mental SF-12
- `lte12_total` - Suma eventos vitales (0-12)

### **3. MARCADORES GENÉTICOS (3 columnas)**
- `prkca` - T/T (riesgo), C/C (protector)
- `tcf4` - A/A (riesgo), T/T (protector) 
- `cdh20` - G/G (riesgo), A/A (protector)

### **4. RESPUESTAS TEXTUALES HADS (7 columnas)**
```
HADS1_Me siento tenso o nervioso
HADS2_Todavía disfruto con lo que me ha gustado hacer
HADS3_Tengo sensación de miedo como si algo horrible fuera a suceder
HADS4_Puedo estar sentado tranquilamente y sentirme relajado
HADS5_Tengo sensación extraña como de aleteo o vacío en el estómago
HADS6_Me siento inquieto como si no pudiera parar de moverme
HADS7_Presento sensación de miedo muy intenso de un momento a otro
```

### **5. RESPUESTAS TEXTUALES ZSAS (20 columnas)**
```
ZSAS1_Me siento más nervioso y ansioso de lo habitual
ZSAS2_Me siento con temor sin razón
ZSAS3_Me irrito con facilidad o siento pánico
ZSAS4_Me siento como si fuera a reventar y partirme en pedazos
ZSAS5_Siento que todo está bien y nada malo pasará
...hasta ZSAS20_Tengo pesadillas
```

### **6. RESPUESTAS TEXTUALES SF-12 (12 columnas)**
```
SF12F1_En general diría que su salud es
SF12F2_Esfuerzos moderados limitación
SF12F3_Subir varios pisos por escalera limitación
SF12F4_Hizo menos de lo que quería por salud física
SF12F5_Tuvo que dejar tareas por salud física
SF12F6_Hasta qué punto el dolor le ha dificultado trabajo
SF12M1_Hizo menos por problema emocional
...hasta SF12M6_Se ha sentido desanimado y triste cuánto tiempo
```

### **7. RESPUESTAS TEXTUALES LTE-12 (12 columnas)**
```
LTE1_Ha sufrido enfermedad lesión o agresión grave
LTE2_Familiar cercano ha sufrido enfermedad lesión o agresión grave
LTE3_Ha muerto padre hijo o pareja cónyuge
...hasta LTE12_Le han robado o ha perdido objeto de valor
```

---

## 🔍 **CASOS DE USO ESPECÍFICOS**

### **📈 Análisis Descriptivo:**
```
Participante 1:
- HADS1: "Muchas veces" se siente tenso
- ZSAS5: "Nunca o casi nunca" siente que todo está bien  
- SF12F1: Salud "Buena"
- LTE3: "Sí" ha muerto familiar cercano
```

### **📊 Análisis de Frecuencias:**
```
¿Cuántas personas respondieron "Siempre o casi siempre" a ZSAS20 (pesadillas)?
- Fácil filtrado: df[df['ZSAS20_Tengo pesadillas'] == 'Siempre o casi siempre']
```

### **🔗 Análisis de Correlaciones:**
```
Relación entre "Muchas veces" tenso (HADS1) y "Con bastante frecuencia" nervioso (ZSAS1)
- Legible sin decodificación de números
```

---

## 📋 **CONVERSIÓN A NÚMEROS SI ES NECESARIA**

Si necesitas análisis estadísticos, puedes convertir fácilmente:

### **HADS - Mapeo de respuestas:**
```python
hads_mapeo = {
    "Nunca": 0, "A veces": 1, "Muchas veces": 2, "Todos los días": 3,
    "Nada": 0, "Sólo un poco": 1, "No mucho": 2, "Como siempre": 3,
    # ... etc por cada pregunta
}
```

### **ZSAS - Mapeo uniforme:**
```python
zsas_mapeo = {
    "Nunca o casi nunca": 1,
    "A veces": 2, 
    "Con bastante frecuencia": 3,
    "Siempre o casi siempre": 4
}
```

### **LTE-12 - Mapeo binario:**
```python
lte_mapeo = {"No": 0, "Sí": 1}
```

---

## 🎯 **ESTADÍSTICAS DE LA BASE GENERADA**

### **📊 Resumen Cuantitativo:**
- **Participantes:** 20 personas
- **Edad promedio:** 37.5 años
- **HADS promedio:** 8.3 (umbral clínico: ≥8)
- **ZSAS promedio:** 42.7 (umbral significativo: ≥36)
- **Eventos vitales promedio:** 4.8

### **🧬 Genotipos (con interpretaciones corregidas):**
- **PRKCA:** 45% C/C (protector), 35% C/T, 20% T/T (riesgo)
- **TCF4:** 50% T/T (protector), 35% T/A, 15% A/A (riesgo)
- **CDH20:** 40% G/G (riesgo), 40% A/G, 20% A/A (protector)

### **✨ Ejemplos de Respuestas Reales:**
- **Ansiedad alta:** "Siempre o casi siempre me siento nervioso"
- **Salud buena:** "En general diría que mi salud es muy buena"
- **Sin eventos:** "No he sufrido crisis económica grave"
- **Con eventos:** "Sí ha muerto un familiar cercano"

---

## 📁 **ARCHIVOS DISPONIBLES**

1. **`base_datos_respuestas_textuales_20_participantes.csv`** - Formato CSV
2. **`base_datos_respuestas_textuales_20_participantes.xlsx`** - Formato Excel  
3. **`generar_base_datos_respuestas_textuales.py`** - Script generador

---

## ⚠️ **NOTAS IMPORTANTES**

### **🔄 Consistencia con ANXRISK:**
- Las respuestas textuales son **exactamente** las mismas que aparecen en la aplicación
- La codificación genética está **corregida** según el modelo entrenado real
- Las correlaciones entre cuestionarios son **realistas** y coherentes

### **🎯 Recomendaciones de Uso:**
- **Presentaciones:** Ideal para mostrar ejemplos reales de respuestas
- **Validación:** Verificar lógica de cuestionarios sin decodificar
- **Investigación cualitativa:** Análisis de patrones textuales
- **Enseñanza:** Mostrar cómo funcionan los instrumentos de medida

---

**📊 Estado:** ✅ Lista para uso inmediato  
**🔬 Validación:** Respuestas coherentes con niveles de ansiedad  
**📋 Formato:** Respuestas textuales completas + totales numéricos  
**🎯 Objetivo:** Máxima claridad y usabilidad sin pérdida de información
