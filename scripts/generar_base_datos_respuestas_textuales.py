#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Base de Datos Detallada ANXRISK - RESPUESTAS TEXTUALES
Genera 20 participantes con todas las respuestas textuales tal como aparecen en la aplicación
"""

import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)

def generar_datos_con_respuestas_textuales(n_participantes=20):
    """
    Genera una base de datos con las respuestas textuales exactas de cada cuestionario
    """
    
    # Nombres españoles realistas
    nombres = [
        "Miguel Flores", "Francisco Ortiz", "Pedro Díaz", "Guillermo Campos", "Irina Quintana",
        "Rafael Ruiz", "Concepción Ruiz", "Antonia Flores", "Pedro Jiménez", "Gloria Vargas",
        "Carmen López", "José García", "María González", "Antonio Martín", "Dolores Sánchez",
        "Manuel Pérez", "Pilar Rodríguez", "Francisco Fernández", "Rosa Jiménez", "Juan Moreno"
    ]
    
    # Datos demográficos
    edades = np.random.normal(40, 15, n_participantes).astype(int)
    edades = np.clip(edades, 18, 70)
    
    generos = np.random.choice(['M', 'F'], n_participantes, p=[0.47, 0.53])
    
    años_educacion = np.random.normal(12, 4, n_participantes)
    años_educacion = np.clip(años_educacion, 5, 20)
    
    # ===== DEFINIR OPCIONES DE RESPUESTA =====
    
    # HADS - Opciones por pregunta (algunas son diferentes)
    opciones_hads = {
        0: ["Nunca", "A veces", "Muchas veces", "Todos los días"],  # P1
        1: ["Nada", "Sólo un poco", "No mucho", "Como siempre"],    # P2 (invertida)
        2: ["Nada", "Un poco, pero no me preocupa", "Sí, pero no es muy fuerte", "Definitivamente y es muy fuerte"], # P3
        3: ["Nunca", "No muy seguido", "Generalmente", "Siempre"],  # P4 (invertida)
        4: ["Nunca", "En ciertas ocasiones", "Con bastante frecuencia", "Muy seguido"], # P5
        5: ["Nunca", "No mucho", "Mucho", "Bastante"],              # P6
        6: ["Nunca", "No muy seguido", "Muy frecuentemente", "Bastante seguido"] # P7
    }
    
    # ZSAS - Todas las preguntas tienen las mismas opciones
    opciones_zsas = ["Nunca o casi nunca", "A veces", "Con bastante frecuencia", "Siempre o casi siempre"]
    
    # SF-12 Opciones por tipo de pregunta
    opciones_sf12_salud = ["Mala", "Regular", "Buena", "Muy buena", "Excelente"]
    opciones_sf12_limitacion = ["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"]
    opciones_sf12_binario = ["Sí", "No"]
    opciones_sf12_frecuencia = ["Siempre", "Casi siempre", "Algunas veces", "Sólo alguna vez", "Nunca"]
    opciones_sf12_tiempo = ["Siempre", "Casi siempre", "Muchas veces", "Algunas veces", "Sólo alguna vez", "Nunca"]
    opciones_sf12_dolor = ["Nada", "Un poco", "Regular", "Bastante", "Mucho"]
    
    # LTE-12 - Todas binarias
    opciones_lte = ["No", "Sí"]
    
    # ===== GENERAR RESPUESTAS TEXTUALES =====
    
    # Estructura para almacenar datos
    data = {
        'nombre': nombres[:n_participantes],
        'edad': edades,
        'genero': generos,
        'años_educacion': años_educacion
    }
    
    # Variables para calcular totales
    hads_totales = []
    zsas_totales = []
    sf12_fisica_totales = []
    sf12_mental_totales = []
    lte_totales = []
    
    # ===== GENERAR HADS =====
    preguntas_hads = [
        "HADS1_Me siento tenso o nervioso",
        "HADS2_Todavía disfruto con lo que me ha gustado hacer", 
        "HADS3_Tengo sensación de miedo como si algo horrible fuera a suceder",
        "HADS4_Puedo estar sentado tranquilamente y sentirme relajado",
        "HADS5_Tengo sensación extraña como de aleteo o vacío en el estómago",
        "HADS6_Me siento inquieto como si no pudiera parar de moverme",
        "HADS7_Presento sensación de miedo muy intenso de un momento a otro"
    ]
    
    for pregunta in preguntas_hads:
        data[pregunta] = []
    
    for i in range(n_participantes):
        base_anxiety = np.random.beta(2, 3)
        respuestas_hads = []
        
        for j in range(7):
            if j in [1, 3]:  # Preguntas invertidas
                prob = 1 - base_anxiety + np.random.normal(0, 0.2)
            else:
                prob = base_anxiety + np.random.normal(0, 0.2)
            
            prob = np.clip(prob, 0, 1)
            indice_respuesta = np.random.choice([0, 1, 2, 3], p=_distribucion_likert(prob))
            respuesta_textual = opciones_hads[j][indice_respuesta]
            
            data[preguntas_hads[j]].append(respuesta_textual)
            respuestas_hads.append(indice_respuesta)
        
        hads_totales.append(sum(respuestas_hads))
    
    # ===== GENERAR ZSAS =====
    preguntas_zsas = [
        "ZSAS1_Me siento más nervioso y ansioso de lo habitual",
        "ZSAS2_Me siento con temor sin razón", 
        "ZSAS3_Me irrito con facilidad o siento pánico",
        "ZSAS4_Me siento como si fuera a reventar y partirme en pedazos",
        "ZSAS5_Siento que todo está bien y nada malo pasará",  # Invertida
        "ZSAS6_Mis brazos y piernas tiemblan",
        "ZSAS7_Me mortifican los dolores de la cabeza cuello o cintura",
        "ZSAS8_Me siento débil y me canso fácilmente",
        "ZSAS9_Me siento tranquilo y puedo permanecer en calma fácilmente",  # Invertida
        "ZSAS10_Puedo sentir que me late muy rápido el corazón",
        "ZSAS11_Sufro de mareos",
        "ZSAS12_Sufro de desmayos o siento que me voy a desmayar",
        "ZSAS13_Puedo inspirar y expirar fácilmente",  # Invertida
        "ZSAS14_Siento hormigueo falta de sensibilidad en dedos de manos y pies",
        "ZSAS15_Sufro de molestias estomacales o indigestión",
        "ZSAS16_Orino con mucha frecuencia",
        "ZSAS17_Generalmente mis manos están secas y calientes",  # Invertida
        "ZSAS18_Siento bochornos me he ruborizado con frecuencia",
        "ZSAS19_Me quedo dormido con facilidad y descanso durante la noche",  # Invertida
        "ZSAS20_Tengo pesadillas"
    ]
    
    # Preguntas invertidas en ZSAS (índices 0-based)
    preguntas_invertidas_zsas = [4, 8, 12, 16, 18]
    
    for pregunta in preguntas_zsas:
        data[pregunta] = []
    
    for i in range(n_participantes):
        base_anxiety = (hads_totales[i] / 21.0) + np.random.normal(0, 0.2)
        base_anxiety = np.clip(base_anxiety, 0, 1)
        respuestas_zsas = []
        
        for j in range(20):
            if j in preguntas_invertidas_zsas:
                prob = 1 - base_anxiety + np.random.normal(0, 0.15)
            else:
                prob = base_anxiety + np.random.normal(0, 0.15)
            
            prob = np.clip(prob, 0, 1)
            indice_respuesta = np.random.choice([0, 1, 2, 3], p=_distribucion_likert(prob))
            respuesta_textual = opciones_zsas[indice_respuesta]
            
            data[preguntas_zsas[j]].append(respuesta_textual)
            respuestas_zsas.append(indice_respuesta + 1)  # ZSAS va de 1-4
        
        zsas_totales.append(sum(respuestas_zsas))
    
    # ===== GENERAR SF-12 =====
    preguntas_sf12 = [
        "SF12F1_En general diría que su salud es",
        "SF12F2_Esfuerzos moderados limitación",
        "SF12F3_Subir varios pisos por escalera limitación",
        "SF12F4_Hizo menos de lo que quería por salud física",
        "SF12F5_Tuvo que dejar tareas por salud física",
        "SF12F6_Hasta qué punto el dolor le ha dificultado trabajo",
        "SF12M1_Hizo menos por problema emocional",
        "SF12M2_No hizo trabajo tan cuidadosamente por problema emocional",
        "SF12M3_Frecuencia salud física o problemas emocionales dificultaron actividades sociales",
        "SF12M4_Se sintió calmado y tranquilo cuánto tiempo",
        "SF12M5_Tuvo mucha energía cuánto tiempo",
        "SF12M6_Se ha sentido desanimado y triste cuánto tiempo"
    ]
    
    for pregunta in preguntas_sf12:
        data[pregunta] = []
    
    for i in range(n_participantes):
        ansiedad_nivel = hads_totales[i] / 21.0
        respuestas_sf12_f = []
        respuestas_sf12_m = []
        
        # SF-12 Física
        # P1: Salud general
        prob_buena_salud = 1 - ansiedad_nivel + np.random.normal(0, 0.2)
        indice = np.random.choice([0, 1, 2, 3, 4], p=_distribucion_salud(prob_buena_salud))
        data["SF12F1_En general diría que su salud es"].append(opciones_sf12_salud[indice])
        respuestas_sf12_f.append(indice + 1)
        
        # P2-P3: Limitaciones físicas
        for p in [1, 2]:
            prob_sin_limit = 1 - ansiedad_nivel * 0.5 + np.random.normal(0, 0.15)
            indice = np.random.choice([0, 1, 2], p=_distribucion_limitacion(prob_sin_limit))
            data[preguntas_sf12[p]].append(opciones_sf12_limitacion[indice])
            respuestas_sf12_f.append(indice + 1)
        
        # P4-P5: Problemas físicos
        for p in [3, 4]:
            prob_sin_problema = 1 - ansiedad_nivel * 0.3 + np.random.normal(0, 0.15)
            indice = np.random.choice([0, 1], p=[1-np.clip(prob_sin_problema, 0, 1), np.clip(prob_sin_problema, 0, 1)])
            data[preguntas_sf12[p]].append(opciones_sf12_binario[indice])
            respuestas_sf12_f.append(indice + 1)
        
        # P6: Dolor
        prob_sin_dolor = 1 - ansiedad_nivel * 0.4 + np.random.normal(0, 0.15)
        indice = np.random.choice([0, 1, 2, 3, 4], p=_distribucion_salud(prob_sin_dolor))
        data["SF12F6_Hasta qué punto el dolor le ha dificultado trabajo"].append(opciones_sf12_dolor[indice])
        respuestas_sf12_f.append(5 - indice)  # Invertida para el dolor
        
        # SF-12 Mental
        # P7-P8: Problemas emocionales
        for p in [6, 7]:
            prob_sin_problema = 1 - ansiedad_nivel + np.random.normal(0, 0.15)
            indice = np.random.choice([0, 1], p=[1-np.clip(prob_sin_problema, 0, 1), np.clip(prob_sin_problema, 0, 1)])
            data[preguntas_sf12[p]].append(opciones_sf12_binario[indice])
            respuestas_sf12_m.append(indice + 1)
        
        # P9: Actividades sociales
        prob_no_dificultad = 1 - ansiedad_nivel + np.random.normal(0, 0.15)
        indice = np.random.choice([0, 1, 2, 3, 4], p=_distribucion_frecuencia(prob_no_dificultad))
        data["SF12M3_Frecuencia salud física o problemas emocionales dificultaron actividades sociales"].append(opciones_sf12_frecuencia[indice])
        respuestas_sf12_m.append(indice)
        
        # P10-P11: Estados positivos
        for p in [9, 10]:
            prob_estado_positivo = 1 - ansiedad_nivel + np.random.normal(0, 0.15)
            indice = np.random.choice([0, 1, 2, 3, 4, 5], p=_distribucion_bienestar(prob_estado_positivo))
            data[preguntas_sf12[p]].append(opciones_sf12_tiempo[indice])
            respuestas_sf12_m.append(6 - indice)  # Invertir para que mayor sea mejor
        
        # P12: Desanimado/triste
        prob_no_triste = 1 - ansiedad_nivel + np.random.normal(0, 0.15)
        indice = np.random.choice([0, 1, 2, 3, 4, 5], p=_distribucion_bienestar(1-prob_no_triste))
        data["SF12M6_Se ha sentido desanimado y triste cuánto tiempo"].append(opciones_sf12_tiempo[indice])
        respuestas_sf12_m.append(indice)
        
        sf12_fisica_totales.append(sum(respuestas_sf12_f))
        sf12_mental_totales.append(sum(respuestas_sf12_m))
    
    # ===== GENERAR LTE-12 =====
    preguntas_lte12 = [
        "LTE1_Ha sufrido enfermedad lesión o agresión grave",
        "LTE2_Familiar cercano ha sufrido enfermedad lesión o agresión grave",
        "LTE3_Ha muerto padre hijo o pareja cónyuge",
        "LTE4_Ha muerto amigo cercano o familiar",
        "LTE5_Se ha separado por problemas matrimoniales",
        "LTE6_Ha roto relación estable",
        "LTE7_Problema grave con amigo cercano vecino o familiar",
        "LTE8_Se quedó sin empleo o buscó empleo más de un mes sin éxito",
        "LTE9_Le han despedido del trabajo",
        "LTE10_Ha tenido crisis económica grave",
        "LTE11_Problemas con policía o compareció ante tribunal",
        "LTE12_Le han robado o ha perdido objeto de valor"
    ]
    
    for pregunta in preguntas_lte12:
        data[pregunta] = []
    
    for i in range(n_participantes):
        ansiedad_nivel = hads_totales[i] / 21.0
        prob_evento = 0.2 + ansiedad_nivel * 0.4
        respuestas_lte = []
        
        for j in range(12):
            # Algunos eventos son más comunes
            if j in [0, 1, 3, 6, 10, 11]:  # Eventos más comunes
                prob_actual = prob_evento * 1.5
            elif j in [2, 4, 8]:  # Eventos menos comunes
                prob_actual = prob_evento * 0.5
            else:
                prob_actual = prob_evento
            
            prob_actual = np.clip(prob_actual, 0, 0.8)
            indice = np.random.choice([0, 1], p=[1-prob_actual, prob_actual])
            data[preguntas_lte12[j]].append(opciones_lte[indice])
            respuestas_lte.append(indice)
        
        lte_totales.append(sum(respuestas_lte))
    
    # ===== GENERAR MARCADORES GENÉTICOS =====
    # PRKCA: T/T = riesgo, C/C = protector
    prkca_genotipos = _generar_genotipos_hardy_weinberg(['C', 'T'], 0.3, n_participantes)
    
    # TCF4: A/A = riesgo, T/T = protector (CORREGIDO)
    tcf4_genotipos = _generar_genotipos_hardy_weinberg(['T', 'A'], 0.4, n_participantes)
    
    # CDH20: G/G = riesgo, A/A = protector (CORREGIDO)  
    cdh20_genotipos = _generar_genotipos_hardy_weinberg(['A', 'G'], 0.6, n_participantes)
    
    # ===== AGREGAR TOTALES Y GENÉTICA =====
    data.update({
        'hads_total': hads_totales,
        'zsas_total': zsas_totales,
        'sf12_fisica_total': sf12_fisica_totales,
        'sf12_mental_total': sf12_mental_totales,
        'lte12_total': lte_totales,
        'prkca': prkca_genotipos,
        'tcf4': tcf4_genotipos,
        'cdh20': cdh20_genotipos
    })
    
    df = pd.DataFrame(data)
    return df

def _distribucion_likert(prob):
    """Genera distribución de probabilidades para escalas Likert"""
    if prob <= 0.25:
        return [0.6, 0.3, 0.08, 0.02]
    elif prob <= 0.5:
        return [0.4, 0.35, 0.2, 0.05]
    elif prob <= 0.75:
        return [0.2, 0.3, 0.35, 0.15]
    else:
        return [0.1, 0.2, 0.35, 0.35]

def _distribucion_salud(prob):
    """Distribución para preguntas de salud (0-4)"""
    if prob <= 0.2:
        return [0.4, 0.3, 0.2, 0.08, 0.02]
    elif prob <= 0.4:
        return [0.2, 0.35, 0.3, 0.12, 0.03]
    elif prob <= 0.6:
        return [0.1, 0.2, 0.4, 0.25, 0.05]
    elif prob <= 0.8:
        return [0.05, 0.1, 0.25, 0.4, 0.2]
    else:
        return [0.02, 0.05, 0.15, 0.3, 0.48]

def _distribucion_limitacion(prob):
    """Distribución para limitaciones físicas (0-2)"""
    if prob <= 0.3:
        return [0.6, 0.3, 0.1]
    elif prob <= 0.7:
        return [0.3, 0.5, 0.2]
    else:
        return [0.1, 0.3, 0.6]

def _distribucion_frecuencia(prob):
    """Distribución para preguntas de frecuencia (0-4)"""
    if prob <= 0.2:
        return [0.1, 0.15, 0.25, 0.3, 0.2]
    elif prob <= 0.5:
        return [0.2, 0.25, 0.3, 0.2, 0.05]
    elif prob <= 0.8:
        return [0.4, 0.3, 0.2, 0.08, 0.02]
    else:
        return [0.6, 0.25, 0.1, 0.04, 0.01]

def _distribucion_bienestar(prob):
    """Distribución para preguntas de bienestar (0-5)"""
    if prob <= 0.2:
        return [0.3, 0.25, 0.2, 0.15, 0.08, 0.02]
    elif prob <= 0.4:
        return [0.2, 0.2, 0.25, 0.2, 0.1, 0.05]
    elif prob <= 0.6:
        return [0.1, 0.15, 0.2, 0.25, 0.2, 0.1]
    elif prob <= 0.8:
        return [0.05, 0.1, 0.15, 0.2, 0.25, 0.25]
    else:
        return [0.02, 0.05, 0.1, 0.15, 0.25, 0.43]

def _generar_genotipos_hardy_weinberg(alelos, freq_alelo2, n):
    """Genera genotipos según equilibrio Hardy-Weinberg"""
    p = 1 - freq_alelo2  # Frecuencia alelo 1
    q = freq_alelo2      # Frecuencia alelo 2
    
    # Probabilidades: p²(A1/A1), 2pq(A1/A2), q²(A2/A2)
    probs = [p**2, 2*p*q, q**2]
    genotipos_num = np.random.choice([0, 1, 2], n, p=probs)
    
    genotipos = []
    for geno in genotipos_num:
        if geno == 0:
            genotipos.append(f"{alelos[0]}/{alelos[0]}")
        elif geno == 1:
            genotipos.append(f"{alelos[0]}/{alelos[1]}")
        else:
            genotipos.append(f"{alelos[1]}/{alelos[1]}")
    
    return genotipos

def main():
    """Función principal"""
    print("\n" + "="*80)
    print("GENERACIÓN DE BASE DE DATOS CON RESPUESTAS TEXTUALES ANXRISK")
    print("="*80)
    
    # Generar datos
    print("\n📊 Generando 20 participantes con respuestas textuales exactas...")
    df = generar_datos_con_respuestas_textuales(20)
    
    # Mostrar estadísticas resumidas
    print(f"\n✅ BASE DE DATOS GENERADA:")
    print(f"  • Total participantes: {len(df)}")
    print(f"  • Total columnas: {len(df.columns)}")
    print(f"  • Edad promedio: {df['edad'].mean():.1f} años")
    print(f"  • HADS promedio: {df['hads_total'].mean():.1f}")
    print(f"  • ZSAS promedio: {df['zsas_total'].mean():.1f}")
    print(f"  • LTE-12 promedio: {df['lte12_total'].mean():.1f}")
    
    print(f"\n🧬 DISTRIBUCIÓN GENÉTICA:")
    for gen in ['prkca', 'tcf4', 'cdh20']:
        dist = df[gen].value_counts()
        print(f"  • {gen.upper()}:")
        for genotipo, count in dist.items():
            print(f"    - {genotipo}: {count} ({count/len(df)*100:.1f}%)")
    
    # Guardar archivos
    filename_csv = "base_datos_respuestas_textuales_20_participantes.csv"
    filename_excel = "base_datos_respuestas_textuales_20_participantes.xlsx"
    
    df.to_csv(filename_csv, index=False, encoding='utf-8')
    print(f"\n✅ Archivo CSV guardado: {filename_csv}")
    
    try:
        df.to_excel(filename_excel, index=False)
        print(f"✅ Archivo Excel guardado: {filename_excel}")
    except ImportError:
        print(f"⚠️ No se pudo generar Excel: requiere openpyxl")
    
    # Mostrar primeras filas (solo columnas principales)
    cols_principales = ['nombre', 'edad', 'genero', 'hads_total', 'zsas_total', 'lte12_total', 'prkca', 'tcf4', 'cdh20']
    print(f"\n📄 MUESTRA DE DATOS (primeras 5 filas):")
    print("="*80)
    print(df[cols_principales].head().to_string(index=False))
    
    # Mostrar ejemplos de respuestas textuales
    print(f"\n🔍 EJEMPLO RESPUESTAS TEXTUALES (Participante 1):")
    print("="*80)
    ejemplos = [
        ('HADS1_Me siento tenso o nervioso', df['HADS1_Me siento tenso o nervioso'].iloc[0]),
        ('ZSAS1_Me siento más nervioso y ansioso de lo habitual', df['ZSAS1_Me siento más nervioso y ansioso de lo habitual'].iloc[0]),
        ('SF12F1_En general diría que su salud es', df['SF12F1_En general diría que su salud es'].iloc[0]),
        ('LTE1_Ha sufrido enfermedad lesión o agresión grave', df['LTE1_Ha sufrido enfermedad lesión o agresión grave'].iloc[0])
    ]
    
    for pregunta, respuesta in ejemplos:
        print(f"  • {pregunta}: '{respuesta}'")
    
    print(f"\n🎯 ESTRUCTURA COMPLETA:")
    print(f"  • Datos demográficos: 4 columnas")
    print(f"  • Totales cuestionarios: 5 columnas") 
    print(f"  • Marcadores genéticos: 3 columnas")
    print(f"  • HADS respuestas textuales: 7 columnas")
    print(f"  • ZSAS respuestas textuales: 20 columnas")
    print(f"  • SF-12 respuestas textuales: 12 columnas")
    print(f"  • LTE-12 respuestas textuales: 12 columnas")
    print(f"  📋 TOTAL: {len(df.columns)} columnas")
    
    print("\n" + "="*80)
    print("BASE DE DATOS CON RESPUESTAS TEXTUALES GENERADA EXITOSAMENTE")
    print("="*80)

if __name__ == "__main__":
    main()
