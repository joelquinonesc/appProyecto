"""
Generador de base de datos simulada con 100 participantes
para testing de la aplicación ANXRISK
"""
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)

def generar_datos_simulados(n_participantes=100):
    """
    Genera datos simulados con correlaciones realistas para ansiedad
    """
    
    # 1. DATOS DEMOGRÁFICOS
    # ========================
    edades = np.random.normal(42, 15, n_participantes)
    edades = np.clip(edades, 18, 80).astype(int)
    
    generos = np.random.choice(['M', 'F'], n_participantes, p=[0.45, 0.55])
    
    # Las mujeres tienden a reportar más ansiedad (40% más de probabilidad)
    factor_genero = np.where(generos == 'F', 1.4, 1.0)
    
    # Educación correlacionada con edad
    años_educacion = np.zeros(n_participantes)
    for i in range(n_participantes):
        max_edu = max(edades[i] - 5, 6)  # Mínimo 6 años de educación
        años_educacion[i] = np.random.normal(12, 3, 1)[0]
        años_educacion[i] = np.clip(años_educacion[i], 6, max_edu).astype(int)
    
    # 2. EVENTOS VITALES (LTE-12: 0-12 eventos)
    # ==========================================
    # Distribución: mayoría sin eventos, algunos con varios
    lte12_counts = np.random.negative_binomial(n=2, p=0.3, size=n_participantes)
    lte12_counts = np.clip(lte12_counts, 0, 12).astype(int)
    
    # Los eventos vitales aumentan la ansiedad (más eventos = más riesgo)
    factor_lte12 = 1 + (lte12_counts / 12) * 0.8
    
    # 3. CUESTIONARIOS CLÍNICOS
    # =========================
    
    # HADS (0-21, puntuación normal <8)
    # Correlacionado con: género, eventos vitales
    # AUMENTAR VARIABILIDAD: incluir más casos de ALTO riesgo
    hads_base = np.random.normal(9, 4, n_participantes)  # Media ~9 con desviación ~4
    hads_base = hads_base + (lte12_counts * 0.4)  # Peso moderado del evento vital
    hads_base = hads_base + factor_genero * 1
    hads_score = np.clip(hads_base, 0, 21).astype(int)
    
    # ZSAS (20-80, puntuación normal <36)
    # Fuerte correlación con HADS, pero con más variabilidad
    # HADS ahora está en rango 0-21, por lo que escalamos la relación
    zsas_base = 30 + (hads_score / 21) * 30  # Escalado al nuevo rango HADS
    zsas_base = zsas_base + np.random.normal(0, 5, n_participantes)  # Ruido
    zsas_score = np.clip(zsas_base, 20, 80).astype(int)
    
    # SF-12 FÍSICA (rango 6-30 o transformado a 0-24 cuartiles)
    # Correlación inversa con edad y eventos vitales
    # Cuartiles: Q1≤15, Q2≤17, Q3≤19, Q4≥20
    # MEJORADO: Aumentar base para distribuir mejor entre cuartiles
    # Base elevada (media ~18-20) + ruido permite alcanzar Q2-Q4 con mayor frecuencia
    sf12_fisica_base = 20 - (edades / 80) * 3 - (lte12_counts * 0.3) + np.random.normal(0, 5.5, n_participantes)
    sf12_fisica = np.clip(sf12_fisica_base, 6, 30).astype(int)
    
    # SF-12 MENTAL (rango 6-30 o transformado a 0-30 cuartiles)
    # Correlación FUERTE inversa con HADS/ZSAS - esto es crítico
    # Cuartiles: Q1≤15, Q2≤18, Q3≤21, Q4≥22
    # MEJORADO: Mayor variabilidad para distribuir entre todos los cuartiles
    # Base elevada (media ~20) + ruido fuerte permite alcanzar Q4 con mayor frecuencia
    sf12_mental_base = 22 - (hads_score * 0.25) - (zsas_score * 0.02) + np.random.normal(0, 5.5, n_participantes)
    sf12_mental = np.clip(sf12_mental_base, 6, 30).astype(int)
    
    # 4. MARCADORES GENÉTICOS
    # =======================
    # Genotipos con notación real
    # Con sesgos de prevalencia realistas
    
    # PRKCA (proteína quinasa C alfa): C/C, C/T, T/T
    # CORRIGIDO: Alelo T de riesgo (~20% en población) - T/T es genotipo de riesgo según literatura
    prkca_numeric = np.random.binomial(n=2, p=0.2, size=n_participantes)
    prkca = np.array([['C/C', 'C/T', 'T/T'][val] for val in prkca_numeric])
    factor_prkca = 1 + (prkca_numeric * 0.25)
    
    # TCF4 (factor de transcripción 4): A/A, A/T, T/T
    # CORREGIDO: Alelo A de riesgo (~35%) - A/A es genotipo de riesgo según modelo entrenado
    tcf4_numeric = np.random.binomial(n=2, p=0.35, size=n_participantes)
    tcf4 = np.array([['A/A', 'A/T', 'T/T'][val] for val in tcf4_numeric])
    # Factor invertido: A/A (val=0) tiene mayor impacto que T/T (val=2)
    factor_tcf4 = 1 + ((2 - tcf4_numeric) * 0.30)  # Invierte la lógica: 0→2, 1→1, 2→0
    
    # CDH20 (cadherina 20): G/G, A/G, A/A  
    # CORREGIDO: Alelo G de riesgo (~25%) - G/G es genotipo de riesgo según modelo entrenado
    cdh20_numeric = np.random.binomial(n=2, p=0.25, size=n_participantes)
    cdh20 = np.array([['G/G', 'A/G', 'A/A'][val] for val in cdh20_numeric])
    # G/G (val=0) tiene mayor impacto que A/A (val=2)
    factor_cdh20 = 1 + ((2 - cdh20_numeric) * 0.25)  # Invierte la lógica
    
    # Los genes influyen levemente en los síntomas
    hads_score = np.clip(hads_score * factor_prkca * 0.97, 0, 21).astype(int)
    zsas_score = np.clip(zsas_score * factor_tcf4 * 0.98, 20, 80).astype(int)
    sf12_mental = np.clip(sf12_mental / (factor_cdh20 * 1.05), 6, 30).astype(int)
    
    # 5. CREAR NOMBRES REALISTAS
    # ==========================
    nombres_m = ['Juan', 'Carlos', 'Miguel', 'José', 'Roberto', 'David', 'Francisco', 
                 'Rafael', 'Andrés', 'Marcos', 'Luis', 'Pedro', 'Diego', 'Javier',
                 'Guillermo', 'Enrique', 'Arturo', 'Sergio', 'Ramón', 'Fernando']
    
    nombres_f = ['María', 'Ana', 'Carmen', 'Rosa', 'Isabel', 'Francisca', 'Antonia',
                 'Concepción', 'Dolores', 'Esperanza', 'Gloria', 'Helena', 'Irina',
                 'Juana', 'Lucia', 'Marta', 'Nancy', 'Olivia', 'Patricia', 'Rosario']
    
    apellidos = ['García', 'Rodríguez', 'Martínez', 'Hernández', 'López', 'Pérez',
                 'González', 'Sánchez', 'Díaz', 'Moreno', 'Jiménez', 'Navarro',
                 'Gutierrez', 'Ruiz', 'Alonso', 'Medina', 'Ortiz', 'Campos',
                 'Romero', 'Acosta', 'Quintana', 'Vargas', 'Flores', 'Silva']
    
    nombres = []
    for i in range(n_participantes):
        if generos[i] == 'M':
            nombres.append(f"{np.random.choice(nombres_m)} {np.random.choice(apellidos)}")
        else:
            nombres.append(f"{np.random.choice(nombres_f)} {np.random.choice(apellidos)}")
    
    # 6. CREAR DATAFRAME FINAL
    # ========================
    df = pd.DataFrame({
        'nombre': nombres,
        'edad': edades,
        'genero': generos,
        'años_educacion': años_educacion,
        'hads_score': hads_score,
        'zsas_score': zsas_score,
        'sf12_fisica': sf12_fisica,
        'sf12_mental': sf12_mental,
        'lte12_count': lte12_counts,
        'prkca': prkca,
        'tcf4': tcf4,
        'cdh20': cdh20
    })
    
    # 7. ESTADÍSTICAS DE VALIDACIÓN
    # =============================
    print("\n" + "="*70)
    print("ESTADÍSTICAS DE LA BASE DE DATOS SIMULADA")
    print("="*70)
    
    print("\n📊 RESUMEN DEMOGRÁFICO:")
    print(f"  • Total de participantes: {n_participantes}")
    print(f"  • Edad: media={edades.mean():.1f}, rango=[{edades.min()}-{edades.max()}]")
    print(f"  • Género: M={sum(generos=='M')}, F={sum(generos=='F')}")
    print(f"  • Educación: media={años_educacion.mean():.1f} años")
    
    print("\n🎯 CUESTIONARIOS CLÍNICOS:")
    print(f"  • HADS: media={hads_score.mean():.1f}, rango=[{hads_score.min()}-{hads_score.max()}]")
    print(f"    - Bajo riesgo (<8): {sum(hads_score < 8)} personas ({sum(hads_score < 8)/n_participantes*100:.1f}%)")
    print(f"    - Alto riesgo (≥8): {sum(hads_score >= 8)} personas ({sum(hads_score >= 8)/n_participantes*100:.1f}%)")
    
    print(f"\n  • ZSAS: media={zsas_score.mean():.1f}, rango=[{zsas_score.min()}-{zsas_score.max()}]")
    print(f"    - Bajo riesgo (<36): {sum(zsas_score < 36)} personas ({sum(zsas_score < 36)/n_participantes*100:.1f}%)")
    print(f"    - Alto riesgo (≥36): {sum(zsas_score >= 36)} personas ({sum(zsas_score >= 36)/n_participantes*100:.1f}%)")
    
    print(f"\n  • SF-12 Física: media={sf12_fisica.mean():.1f}, rango=[{sf12_fisica.min()}-{sf12_fisica.max()}] (escala 6-30)")
    print(f"  • SF-12 Mental: media={sf12_mental.mean():.1f}, rango=[{sf12_mental.min()}-{sf12_mental.max()}] (escala 6-30)")
    
    print("\n🧬 MARCADORES GENÉTICOS:")
    print(f"  • PRKCA:")
    print(f"    - C/C (protector): {sum(prkca == 'C/C')} personas ({sum(prkca == 'C/C')/n_participantes*100:.1f}%)")
    print(f"    - C/T (heterocigoto): {sum(prkca == 'C/T')} personas ({sum(prkca == 'C/T')/n_participantes*100:.1f}%)")
    print(f"    - T/T (riesgo): {sum(prkca == 'T/T')} personas ({sum(prkca == 'T/T')/n_participantes*100:.1f}%)")
    
    print(f"\n  • TCF4:")
    print(f"    - A/A (riesgo): {sum(tcf4 == 'A/A')} personas ({sum(tcf4 == 'A/A')/n_participantes*100:.1f}%)")
    print(f"    - A/T (heterocigoto): {sum(tcf4 == 'A/T')} personas ({sum(tcf4 == 'A/T')/n_participantes*100:.1f}%)")
    print(f"    - T/T (protector): {sum(tcf4 == 'T/T')} personas ({sum(tcf4 == 'T/T')/n_participantes*100:.1f}%)")
    
    print(f"\n  • CDH20:")
    print(f"    - G/G (riesgo): {sum(cdh20 == 'G/G')} personas ({sum(cdh20 == 'G/G')/n_participantes*100:.1f}%)")
    print(f"    - A/G (heterocigoto): {sum(cdh20 == 'A/G')} personas ({sum(cdh20 == 'A/G')/n_participantes*100:.1f}%)")
    print(f"    - A/A (protector): {sum(cdh20 == 'A/A')} personas ({sum(cdh20 == 'A/A')/n_participantes*100:.1f}%)")
    
    print("\n📋 EVENTOS VITALES:")
    print(f"  • LTE-12: media={lte12_counts.mean():.1f}, rango=[{lte12_counts.min()}-{lte12_counts.max()}]")
    print(f"  • Sin eventos: {sum(lte12_counts == 0)} personas ({sum(lte12_counts == 0)/n_participantes*100:.1f}%)")
    print(f"  • Con eventos: {sum(lte12_counts > 0)} personas ({sum(lte12_counts > 0)/n_participantes*100:.1f}%)")
    
    print("\n📈 CORRELACIONES CLAVE:")
    # Correlaciones
    corr_hads_zsas = np.corrcoef(hads_score, zsas_score)[0, 1]
    corr_hads_lte = np.corrcoef(hads_score, lte12_counts)[0, 1]
    corr_hads_sf12m = np.corrcoef(hads_score, sf12_mental)[0, 1]
    corr_edad_hads = np.corrcoef(edades, hads_score)[0, 1]
    
    print(f"  • HADS ↔ ZSAS: {corr_hads_zsas:.3f} (muy fuerte)")
    print(f"  • HADS ↔ LTE-12: {corr_hads_lte:.3f} (moderada)")
    print(f"  • HADS ↔ SF-12 Mental: {corr_hads_sf12m:.3f} (fuerte negativa)")
    print(f"  • Edad ↔ HADS: {corr_edad_hads:.3f} (débil)")
    
    print("\n✅ Distribución de Riesgos Esperados:")
    # Crear puntuación de riesgo simple para visualización
    riesgo_simple = (
        (hads_score / 21 * 0.4) +
        ((zsas_score - 20) / 60 * 0.3) +
        ((27 - sf12_mental) / 21 * 0.3)
    )
    
    bajo_riesgo = sum(riesgo_simple < 0.3)
    moderado_riesgo = sum((riesgo_simple >= 0.3) & (riesgo_simple < 0.7))
    alto_riesgo = sum(riesgo_simple >= 0.7)
    
    print(f"  • Riesgo BAJO (<0.3): {bajo_riesgo} personas ({bajo_riesgo/n_participantes*100:.1f}%)")
    print(f"  • Riesgo MODERADO (0.3-0.7): {moderado_riesgo} personas ({moderado_riesgo/n_participantes*100:.1f}%)")
    print(f"  • Riesgo ALTO (>0.7): {alto_riesgo} personas ({alto_riesgo/n_participantes*100:.1f}%)")
    
    print("\n" + "="*70 + "\n")
    
    return df

# Generar y guardar datos
if __name__ == "__main__":
    df = generar_datos_simulados(n_participantes=100)
    
    # Guardar como CSV
    df.to_csv('datos_simulados_100_participantes.csv', index=False, encoding='utf-8-sig')
    print("✅ Base de datos guardada como: datos_simulados_100_participantes.csv")
    
    # Guardar como Excel para mejor visualización
    try:
        df.to_excel('datos_simulados_100_participantes.xlsx', index=False, sheet_name='Participantes')
        print("✅ Base de datos guardada como: datos_simulados_100_participantes.xlsx")
    except Exception as e:
        print(f"⚠️ No se pudo generar Excel: {e}")
    
    # Mostrar primeras filas
    print("\n📄 PRIMERAS 10 FILAS DE LA BASE DE DATOS:")
    print("="*70)
    print(df.head(10).to_string(index=False))
