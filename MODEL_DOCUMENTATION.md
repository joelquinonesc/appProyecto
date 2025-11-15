# Documentación del Modelo de Predicción de Riesgo de Ansiedad - ANXRISK

## 📋 Descripción General

ANXRISK es una aplicación web desarrollada con Streamlit que evalúa el riesgo de ansiedad en pacientes mediante la integración de datos clínicos, demográficos, genéticos y de eventos vitales. Utiliza modelos de machine learning (LightGBM para hombres, MLP para mujeres) entrenados con técnicas de SHAP para explicabilidad.

## 📊 Fuentes de Datos

La aplicación recopila información de los siguientes cuestionarios y fuentes:

### 1. Datos Demográficos

- **Edad**: En años
- **Género**: Masculino (0) o Femenino (1)
- **Años de Educación**: Educación formal completada

### 2. Cuestionario HADS (Hospital Anxiety and Depression Scale)

- 14 preguntas sobre síntomas de ansiedad y depresión
- Puntaje total: 0-21
- Niveles: Normal (≤7), Leve (8-10), Moderada (11-14), Severa (≥15)

### 3. Cuestionario ZSAS (Zung Self-Rating Anxiety Scale)

- 20 preguntas sobre síntomas de ansiedad
- Puntaje bruto: 20-80
- Puntaje normalizado: (bruto × 100) / 80
- Niveles: Normal (<45), Leve-Moderada (45-59), Marcada-Severa (60-74), Extrema (≥75)

### 4. Cuestionario SF-12 (Short Form Health Survey)

- 12 preguntas sobre calidad de vida relacionada con la salud
- Componentes: Física (PCS) y Mental (MCS)
- Cálculo simplificado:
  - **PCS**: Suma de ítems Q1,Q2,Q3,Q4,Q5,Q8
  - **MCS**: Suma de ítems Q6,Q7,Q9,Q10,Q11,Q12

### 5. Cuestionario LTE-12 (Life Time Events)

- 12 eventos vitales estresantes
- Puntaje: Número de eventos experimentados (0-12)

### 6. Datos Genéticos

- **PRKCA**: Gen relacionado con regulación del estrés (T/T, C/T, C/C)
- **TCF4**: Gen relacionado con desarrollo neuronal (A/A, A/T, T/T)
- **CDH20**: Gen relacionado con conectividad neuronal (G/G, G/A, A/A)

## 🔢 Cálculos Detallados por Respuesta

### HADS (Escala de Ansiedad y Depresión Hospitalaria)

**7 preguntas**, cada una con 4 opciones (0-3 puntos):

1. Me siento tenso(a) o nervioso(a): Nunca(0), A veces(1), Muchas veces(2), Todos los días(3)
2. Todavía disfruto con lo que me ha gustado hacer: Nada(0), Sólo un poco(1), No mucho(2), Como siempre(3)
3. Tengo una sensación de miedo, como si algo horrible fuera a suceder: Nada(0), Un poco(1), Si pero no fuerte(2), Definitivamente(3)
4. Puedo estar sentado(a) tranquilamente y sentirme relajado(a): Nunca(0), No muy seguido(1), Generalmente(2), Siempre(3)
5. Tengo una sensación extraña, como de aleteo o vacío en el estómago: Nunca(0), En ciertas ocasiones(1), Con bastante frecuencia(2), Muy seguido(3)
6. Me siento inquieto(a), como si no pudiera parar de moverme: Nunca(0), No mucho(1), Mucho(2), Bastante(3)
7. Presento una sensación de miedo muy intenso de un momento a otro: Nunca(0), No muy seguido(1), Muy frecuentemente(2), Bastante seguido(3)

**Cálculo total**: Suma de todas las respuestas (0-21)

### ZSAS (Escala de Ansiedad de Zung)

**20 preguntas**, cada una con 4 opciones (1-4 puntos):

**Preguntas directas** (puntuación normal):

- Nunca o casi nunca (1), A veces (2), Con bastante frecuencia (3), Siempre o casi siempre (4)

**Preguntas invertidas** (puntuación invertida):

- Nunca o casi nunca (4), A veces (3), Con bastante frecuencia (2), Siempre o casi siempre (1)

Preguntas invertidas: 5,9,13,17,19

**Cálculo**:

- Puntaje bruto = Suma de todas las respuestas (20-80)
- Puntaje normalizado = Puntaje bruto × 1.25 (25-100)

### SF-12 (Short Form Health Survey)

**12 preguntas**, puntuación estándar SF-12 (mayor puntuación = mejor salud):

#### Componente Física (PCS)

**Preguntas**: 1,2,3,4,5,8

1. **En general, ¿diría que su salud es?**

   - Excelente (5), Muy buena (4), Buena (3), Regular (2), Mala (1)

2. **Esfuerzos moderados (mover una mesa, caminar más de 1 hora)**

   - Sí, limitado mucho (1), Sí, limitado un poco (2), No, no limitado (3)

3. **Subir varios pisos por la escalera**

   - Sí, limitado mucho (1), Sí, limitado un poco (2), No, no limitado (3)

4. **¿Hizo menos de lo que hubiera querido hacer?** (por salud física)

   - Sí (1), No (2)

5. **¿Tuvo que dejar de hacer algunas tareas?** (por salud física)

   - Sí (1), No (2)

6. **¿Hasta qué punto el dolor le ha dificultado su trabajo habitual?**
   - Nada (5), Un poco (4), Regular (3), Bastante (2), Mucho (1)

**PCS = Q1 + Q2 + Q3 + Q4 + Q5 + Q8** (rango: 6-30)

#### Componente Mental (MCS)

**Preguntas**: 6,7,9,10,11,12

6. **¿Hizo menos de lo que hubiera querido hacer, por algún problema emocional?**

   - Sí (1), No (2)

7. **¿No hizo su trabajo o sus actividades cotidianas tan cuidadosamente como de costumbre, por algún problema emocional?**

   - Sí (1), No (2)

8. **¿Con qué frecuencia la salud física o los problemas emocionales le han dificultado sus actividades sociales (como visitar a los amigos o familiares)?**

   - Siempre (1), Casi siempre (2), Algunas veces (3), Sólo alguna vez (4), Nunca (5)10. **¿Se sintió calmado y tranquilo? ¿Cuánto tiempo?**
   - Siempre (6), Casi siempre (5), Muchas veces (4), Algunas veces (3), Sólo una vez (2), Nunca (1)

9. **¿Tuvo mucha energía? ¿Cuánto tiempo?**

   - Siempre (6), Casi siempre (5), Muchas veces (4), Algunas veces (3), Sólo una vez (2), Nunca (1)

10. **¿Se ha sentido desanimado(a) y triste? ¿Cuánto tiempo?**
    - Siempre (1), Casi siempre (2), Muchas veces (3), Algunas veces (4), Sólo una vez (5), Nunca (6)

**MCS = Q6 + Q7 + Q9 + Q10 + Q11 + Q12** (rango: 6-27)### LTE-12 (Lista de Experiencias Amenazantes)

**12 preguntas** de Sí/No:

Cada "Sí" cuenta como 1 punto, "No" como 0.

**Total = Número de "Sí" (0-12)**

## 🔄 Transformaciones de Datos

### Variables Binarias

#### EDAD24 (Grupo de Edad)

```python
if 24 <= edad <= 34:
    EDAD24 = 1  # Grupo joven
else:
    EDAD24 = 0  # Otros grupos
```

#### AEFGROUPS (Grupo de Educación)

```python
if años_educación >= 15:
    AEFGROUPS = 1  # Educación superior
else:
    AEFGROUPS = 0  # Educación básica/secundaria
```

### Cuartiles SF-12

Los puntajes de SF-12 se clasifican en cuartiles para capturar niveles relativos de salud:

#### Componente Física (SF12F)

- **Q1**: puntaje ≤ 15 (peor salud física)
- **Q2**: 16-20
- **Q3**: 21-25
- **Q4**: ≥ 26 (mejor salud física)

#### Componente Mental (SF12M)

- **Q1**: puntaje ≤ 15 (peor salud mental)
- **Q2**: 16-20
- **Q3**: 21-25
- **Q4**: ≥ 26 (mejor salud mental)

### Clasificación LTE-12

```python
if total_eventos == 0:
    LTE12 = 0
elif total_eventos == 1:
    LTE12 = 1
else:  # >= 2
    LTE12 = 2
```

### Codificación One-Hot

Todas las variables categóricas se convierten a variables dummy binarias:

#### SF-12 Física

- SF12F_Q1: 1 si cuartil 1, 0 otherwise
- SF12F_Q2: 1 si cuartil 2, 0 otherwise
- SF12F_Q3: 1 si cuartil 3, 0 otherwise
- SF12F_Q4: 1 si cuartil 4, 0 otherwise

#### SF-12 Mental

- SF12M_Q1: 1 si cuartil 1, 0 otherwise
- SF12M_Q2: 1 si cuartil 2, 0 otherwise
- SF12M_Q3: 1 si cuartil 3, 0 otherwise
- SF12M_Q4: 1 si cuartil 4, 0 otherwise

#### Genotipo PRKCA

- PRKCA_C/C: 1 si C/C, 0 otherwise
- PRKCA_C/T: 1 si C/T, 0 otherwise
- PRKCA_T/T: 1 si T/T, 0 otherwise

#### Genotipo TCF4

- TCF4_A/A: 1 si A/A, 0 otherwise
- TCF4_A/T: 1 si A/T, 0 otherwise
- TCF4_T/T: 1 si T/T, 0 otherwise

#### Genotipo CDH20

- CDH20_A/A: 1 si A/A, 0 otherwise
- CDH20_A/G: 1 si G/A, 0 otherwise
- CDH20_G/G: 1 si G/G, 0 otherwise

#### LTE-12

- LTE12_0: 1 si clasificación 0, 0 otherwise
- LTE12_1: 1 si clasificación 1, 0 otherwise
- LTE12_2: 1 si clasificación 2, 0 otherwise

## 🎯 Features del Modelo

El modelo recibe exactamente **22 features** en el siguiente orden:

1. **EDAD24**: Grupo de edad binario
2. **AEFGROUPS**: Grupo de educación binario
3. **SF12F_Q1**: Salud física cuartil 1
4. **SF12F_Q2**: Salud física cuartil 2
5. **SF12F_Q3**: Salud física cuartil 3
6. **SF12F_Q4**: Salud física cuartil 4
7. **SF12M_Q1**: Salud mental cuartil 1
8. **SF12M_Q2**: Salud mental cuartil 2
9. **SF12M_Q3**: Salud mental cuartil 3
10. **SF12M_Q4**: Salud mental cuartil 4
11. **PRKCA_C/C**: Genotipo PRKCA C/C
12. **PRKCA_C/T**: Genotipo PRKCA C/T
13. **PRKCA_T/T**: Genotipo PRKCA T/T
14. **TCF4_A/A**: Genotipo TCF4 A/A
15. **TCF4_A/T**: Genotipo TCF4 A/T
16. **TCF4_T/T**: Genotipo TCF4 T/T
17. **CDH20_A/A**: Genotipo CDH20 A/A
18. **CDH20_A/G**: Genotipo CDH20 G/A
19. **CDH20_G/G**: Genotipo CDH20 G/G
20. **LTE12_0**: Eventos vitales clasificación 0
21. **LTE12_1**: Eventos vitales clasificación 1
22. **LTE12_2**: Eventos vitales clasificación 2

## 🤖 Modelos de Machine Learning

### Selección por Género

- **Masculino (GENERO=0)**: LightGBM Classifier
- **Femenino (GENERO=1)**: MLP Classifier

### Arquitectura

- **LightGBM**: Modelo basado en árboles de decisión, eficiente para datos tabulares
- **MLP**: Red neuronal con capas ocultas, captura relaciones no lineales complejas

### Entrenamiento

- Datos balanceados por género
- Validación cruzada
- Optimización de hiperparámetros
- Métricas: AUC, precisión, recall, F1-score

## 📈 Salida del Modelo

### Predicción Binaria

- **0**: Bajo riesgo de ansiedad
- **1**: Alto riesgo de ansiedad

### Probabilidades

- Probabilidad de bajo riesgo (clase 0)
- Probabilidad de alto riesgo (clase 1)

### Explicabilidad SHAP

- **Importancia global**: Mean Absolute SHAP values por feature
- **Contribuciones locales**: SHAP values por instancia
- **Gráfico de resumen**: Visualización dot plot de contribuciones

## 🔍 Interpretación de Resultados

### Alto Riesgo (1)

- HADS ≥ 8 Y ZSAS ≥ 36
- O puntaje alto en cuestionarios clínicos
- Factores genéticos de riesgo presentes
- Baja salud física/mental (cuartiles bajos)
- Alto número de eventos vitales estresantes

### Bajo Riesgo (0)

- HADS < 8 O ZSAS < 36
- Buena salud autopercibida
- Factores protectores genéticos
- Bajo estrés vital

### SHAP Values

- **Positivo**: Aumenta probabilidad de alto riesgo
- **Negativo**: Disminuye probabilidad de alto riesgo
- **Magnitud**: Importancia relativa de la feature

## 📝 Notas Técnicas

- Todos los datos son anonimizados y confidenciales
- Los modelos están validados clínicamente
- Los resultados son preliminares y requieren evaluación profesional
- La aplicación cumple con estándares éticos de IA en salud

## 🛠️ Desarrollo

Para modificaciones o actualizaciones, consultar:

- `src/utils/calculos.py`: Funciones de transformación
- `src/pages/datos_geneticos.py`: Lógica de predicción
- `src/models/`: Archivos de modelos entrenados</content>
  <parameter name="filePath">c:/xampp/htdocs/ANXRISK/appProyecto/MODEL_DOCUMENTATION.md
