"""
Página de Análisis Masivo - Procesa múltiples pacientes desde CSV
"""
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import joblib

def mostrar_analisis_masivo():
    """Muestra la interfaz de análisis masivo de pacientes"""
    
    # CSS general
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>📊 Análisis Masivo de Pacientes</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(165, 214, 167, 0.1) 100%); 
                border-left: 5px solid #4CAF50; border-radius: 8px; padding: 20px; margin-bottom: 20px;'>
        <p style='color: #1B5E20; font-weight: 500;'>
        📋 <strong>Instrucciones:</strong> Carga un archivo CSV con los datos de tus participantes. 
        El sistema calculará automáticamente el riesgo de ansiedad y generará un reporte detallado.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sección de descarga de plantilla
    st.markdown("### 📥 Descargar Plantilla CSV")
    
    # Crear CSV de plantilla
    plantilla_df = pd.DataFrame({
        'nombre': ['Juan Pérez', 'María García', 'Carlos López'],
        'edad': [45, 38, 52],
        'genero': ['Masculino', 'Femenino', 'Masculino'],
        'años_educacion': [12, 16, 14],
        'hads_score': [8, 5, 12],
        'zsas_score': [42, 28, 55],
        'sf12_fisica': [35.5, 48.2, 32.1],
        'sf12_mental': [42.1, 50.3, 38.5],
        'lte12_count': [3, 1, 4],
        'prkca': ['C/T', 'T/T', 'C/C'],
        'tcf4': ['A/T', 'A/A', 'T/T'],
        'cdh20': ['G/A', 'G/G', 'A/A']
    })
    
    csv_plantilla = plantilla_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Descargar Plantilla CSV",
        data=csv_plantilla,
        file_name="plantilla_pacientes.csv",
        mime="text/csv"
    )
    
    st.markdown("**Descripción de columnas:**")
    st.markdown("""
    - **nombre**: Nombre completo del paciente
    - **edad**: Edad en años (1-120)
    - **genero**: Masculino o Femenino
    - **años_educacion**: Años de educación formal
    - **hads_score**: Puntuación HADS (0-42, >8 indica alto riesgo)
    - **zsas_score**: Puntuación ZSAS (20-80, >36 indica alto riesgo)
    - **sf12_fisica**: Puntuación SF-12 Física (0-100)
    - **sf12_mental**: Puntuación SF-12 Mental (0-100)
    - **lte12_count**: Número de eventos vitales estresantes (0-12)
    - **prkca**: Genotipo (T/T, C/T, C/C)
    - **tcf4**: Genotipo (A/A, A/T, T/T)
    - **cdh20**: Genotipo (G/G, G/A, A/A)
    """)
    
    st.markdown("---")
    st.markdown("### 📤 Cargar Archivo CSV")
    
    # Upload CSV
    uploaded_file = st.file_uploader(
        "Selecciona tu archivo CSV",
        type="csv",
        help="Asegúrate de que el CSV tenga todas las columnas requeridas"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Validar columnas requeridas
            columnas_requeridas = ['nombre', 'edad', 'genero', 'años_educacion', 'hads_score', 
                                  'zsas_score', 'sf12_fisica', 'sf12_mental', 'lte12_count', 
                                  'prkca', 'tcf4', 'cdh20']
            
            columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
            
            if columnas_faltantes:
                st.error(f"❌ Faltan las siguientes columnas: {', '.join(columnas_faltantes)}")
                return
            
            st.success(f"✅ Archivo cargado correctamente: {len(df)} pacientes")
            
            st.markdown("### 📋 Vista Previa de Datos")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Botón para procesar
            if st.button("🔄 Procesar y Generar Reportes", key="process_button", use_container_width=True):
                st.markdown("---")
                st.markdown("### ⏳ Procesando pacientes...")
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                results = []
                
                for idx, (_, row) in enumerate(df.iterrows()):
                    # Actualizar estado
                    status_text.text(f"Procesando: {row['nombre']} ({idx+1}/{len(df)})")
                    
                    # Calcular riesgo (aquí iría tu modelo)
                    resultado = calcular_riesgo_paciente(row)
                    results.append(resultado)
                    
                    progress_bar.progress((idx + 1) / len(df))
                
                # Crear DataFrame de resultados, filtrando errores
                valid_results = [r for r in results if r is not None and r.get('categoria_riesgo') != 'Error']
                df_resultados = pd.DataFrame(valid_results)
                
                if len(valid_results) < len(results):
                    st.warning(f"⚠️ Se procesaron {len(valid_results)} de {len(results)} pacientes correctamente.")
                
                st.success("✅ ¡Procesamiento completado!")
                st.markdown("---")
                
                # Mostrar resultados preliminares
                st.markdown("### 📊 Resultados Consolidados")
                st.dataframe(df_resultados, use_container_width=True)
                df_resultados_final = df_resultados
                
                # Tabla de transformaciones one-hot DETALLADA (22 features)
                st.markdown("---")
                st.markdown("### 🔄 Codificación de los 22 Features para el Modelo XGBoost Extendido")
                
                # Importar funciones de transformación (EXACTAS a resultados.py)
                from src.utils.calculos import transformar_educacion_a_binaria, transformar_sf12_fisica_a_cuartil, transformar_sf12_mental_a_cuartil, transformar_lte12_a_clasificacion
                
                # Crear tabla expandida con todos los 22 features
                features_detallados = []
                for _, row in df.iterrows():
                    # 1-2. TRANSFORMAR EDAD Y EDUCACIÓN (consistente con calculos.py)
                    edad24 = 0 if int(row['edad']) <= 24 else 1
                    aefgroups = transformar_educacion_a_binaria(int(row['años_educacion']))
                    
                    # 3-6. SF-12 FÍSICA ONE-HOT de cuartiles (SOLO UNO es 1, resto 0)
                    sf12f_cuartil = transformar_sf12_fisica_a_cuartil(float(row['sf12_fisica']))
                    sf12f_q1 = 1 if sf12f_cuartil == 1 else 0
                    sf12f_q2 = 1 if sf12f_cuartil == 2 else 0
                    sf12f_q3 = 1 if sf12f_cuartil == 3 else 0
                    sf12f_q4 = 1 if sf12f_cuartil == 4 else 0
                    
                    # 7-10. SF-12 MENTAL ONE-HOT de cuartiles (SOLO UNO es 1, resto 0)
                    sf12m_cuartil = transformar_sf12_mental_a_cuartil(float(row['sf12_mental']))
                    sf12m_q1 = 1 if sf12m_cuartil == 1 else 0
                    sf12m_q2 = 1 if sf12m_cuartil == 2 else 0
                    sf12m_q3 = 1 if sf12m_cuartil == 3 else 0
                    sf12m_q4 = 1 if sf12m_cuartil == 4 else 0
                    
                    # 11-13. PRKCA ONE-HOT (binarios)
                    prkca_cc = 1 if row['prkca'] == 'C/C' else 0
                    prkca_ct = 1 if row['prkca'] == 'C/T' else 0
                    prkca_tt = 1 if row['prkca'] == 'T/T' else 0
                    
                    # 14-16. TCF4 ONE-HOT (binarios)
                    tcf4_aa = 1 if row['tcf4'] == 'A/A' else 0
                    tcf4_at = 1 if row['tcf4'] == 'A/T' else 0
                    tcf4_tt = 1 if row['tcf4'] == 'T/T' else 0
                    
                    # 17-19. CDH20 ONE-HOT (binarios)
                    cdh20_aa = 1 if row['cdh20'] == 'A/A' else 0
                    cdh20_ag = 1 if row['cdh20'] == 'G/A' else 0
                    cdh20_gg = 1 if row['cdh20'] == 'G/G' else 0
                    
                    # 20-22. LTE12 ONE-HOT (consistente con calculos.py: 0=0, 1=1, 2+=2)
                    lte12_clasif = transformar_lte12_a_clasificacion(int(row['lte12_count']))
                    lte12_0 = 1 if lte12_clasif == 0 else 0
                    lte12_1 = 1 if lte12_clasif == 1 else 0
                    lte12_2 = 1 if lte12_clasif == 2 else 0
                    
                    feat = {
                        'Paciente': row['nombre'],
                        # 2 BINARIAS (transformadas)
                        '1-EDAD24': edad24,
                        '2-AEFGROUPS': aefgroups,
                        # LTE12 ONE-HOT (3 features) - DESPUÉS de edad y educación
                        '3-LTE12_0': lte12_0,
                        '4-LTE12_1': lte12_1,
                        '5-LTE12_2': lte12_2,
                        # SF-12 Física ONE-HOT (Q1-Q4, solo uno es 1)
                        '6-SF12F_Q1': sf12f_q1,
                        '7-SF12F_Q2': sf12f_q2,
                        '8-SF12F_Q3': sf12f_q3,
                        '9-SF12F_Q4': sf12f_q4,
                        # SF-12 Mental ONE-HOT (Q1-Q4, solo uno es 1)
                        '10-SF12M_Q1': sf12m_q1,
                        '11-SF12M_Q2': sf12m_q2,
                        '12-SF12M_Q3': sf12m_q3,
                        '13-SF12M_Q4': sf12m_q4,
                        # PRKCA ONE-HOT (3 features)
                        '14-PRKCA_C/C': prkca_cc,
                        '15-PRKCA_C/T': prkca_ct,
                        '16-PRKCA_T/T': prkca_tt,
                        # TCF4 ONE-HOT (3 features)
                        '17-TCF4_A/A': tcf4_aa,
                        '18-TCF4_A/T': tcf4_at,
                        '19-TCF4_T/T': tcf4_tt,
                        # CDH20 ONE-HOT (3 features)
                        '20-CDH20_A/A': cdh20_aa,
                        '21-CDH20_A/G': cdh20_ag,
                        '22-CDH20_G/G': cdh20_gg,
                    }
                    features_detallados.append(feat)
                
                df_features = pd.DataFrame(features_detallados)
                st.dataframe(df_features, use_container_width=True)
                
                # Explicación detallada
                st.markdown("""
                **Explicación de los 22 Features:**
                
                **Binarias Transformadas (2):**
                - 1: **EDAD24** - 0 si edad ≤ 24 años, 1 si edad > 24
                - 2: **AEFGROUPS** - 0 si años educación ≤ 14, 1 si ≥ 15
                
                **SF-12 Física (4 features)** - Rango variable, asignado a 4 cuartiles:
                - 6-9: **SF12F_Q1 a Q4** - Cuartiles según SHAP
                  - Q1: ≤15 | Q2: 15<x≤17 | Q3: 17<x≤19 | Q4: >19
                
                **SF-12 Mental (4 features)** - Rango variable, asignado a 4 cuartiles:
                - 10-13: **SF12M_Q1 a Q4** - Cuartiles según definición original
                  - Q1: ≤15 | Q2: ≤18 | Q3: ≤21 | Q4: ≥22
                
                **PRKCA - One-Hot (3 features binarios):**
                - 14: **PRKCA_C/C** - 1 si genotipo=C/C, 0 si no
                - 15: **PRKCA_C/T** - 1 si genotipo=C/T, 0 si no
                - 16: **PRKCA_T/T** - 1 si genotipo=T/T, 0 si no
                
                **TCF4 - One-Hot (3 features binarios):**
                - 17: **TCF4_A/A** - 1 si genotipo=A/A, 0 si no
                - 18: **TCF4_A/T** - 1 si genotipo=A/T, 0 si no
                - 19: **TCF4_T/T** - 1 si genotipo=T/T, 0 si no
                
                **CDH20 - One-Hot (3 features binarios):**
                - 20: **CDH20_A/A** - 1 si genotipo=A/A, 0 si no
                - 21: **CDH20_A/G** - 1 si genotipo=G/A, 0 si no
                - 22: **CDH20_G/G** - 1 si genotipo=G/G, 0 si no
                
                **TOTAL: 22 Features** → Modelo XGBoost Extendido → Predicción de Riesgo
                """)
                
                # Estadísticas
                st.markdown("### 📈 Estadísticas Generales")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    bajo = len(df_resultados[df_resultados['categoria_riesgo'] == 'Bajo'])
                    st.metric("Riesgo Bajo", bajo, delta=f"{(bajo/len(df_resultados)*100):.1f}%")
                
                with col2:
                    moderado = len(df_resultados[df_resultados['categoria_riesgo'] == 'Moderado'])
                    st.metric("Riesgo Moderado", moderado, delta=f"{(moderado/len(df_resultados)*100):.1f}%")
                
                with col3:
                    alto = len(df_resultados[df_resultados['categoria_riesgo'] == 'Alto'])
                    st.metric("Riesgo Alto", alto, delta=f"{(alto/len(df_resultados)*100):.1f}%")
                
                with col4:
                    promedio_riesgo = df_resultados['riesgo_predicho'].mean()
                    st.metric("Riesgo Promedio", f"{promedio_riesgo:.3f}", delta=None)
                st.markdown("---")
                
                # Calcular valores SHAP para las top 10 características
                st.markdown("### 🔬 Calculando Análisis SHAP...")
                shap_progress = st.progress(0)
                
                try:
                    # Importar función de integración SHAP
                    import sys
                    import os
                    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                    from scripts.shap_integration_masivo import main_shap_integration
                    
                    # Calcular SHAP (pasando df con nombre para poder hacer merge)
                    shap_result = main_shap_integration(df[['nombre', 'edad', 'años_educacion', 'lte12_count', 'sf12_fisica', 'sf12_mental', 'prkca', 'tcf4', 'cdh20']])
                    shap_progress.progress(100)
                    
                    if shap_result:
                        # Combinar resultados (riesgo) con valores SHAP
                        # df_resultados tiene: nombre, riesgo_predicho, categoria_riesgo
                        # shap_result['df_with_shap'] tiene: nombre, SHAP_* columns
                        
                        df_shap_cols = shap_result['df_with_shap'].copy()
                        shap_cols = [col for col in df_shap_cols.columns if col.startswith('SHAP_')]
                        
                        # Crear un merge basado en el índice (ambos df tienen mismo orden)
                        df_resultados_final = df_resultados.copy()
                        for shap_col in shap_cols:
                            # Las filas están alineadas en el mismo orden, así que usar iloc
                            df_resultados_final[shap_col] = df_shap_cols[shap_col].values
                        
                        # Seleccionar columnas para display: nombre, riesgo, categoría, y top 5 SHAP
                        cols_to_display = ['nombre', 'riesgo_predicho', 'categoria_riesgo'] + shap_cols
                        df_resultados_display = df_resultados_final[cols_to_display].copy()
                        
                        # Renombrar columnas SHAP para mejor legibilidad
                        rename_dict = {}
                        for col in shap_cols:
                            feature_name = col.replace('SHAP_', '')
                            rename_dict[col] = f'SHAP: {feature_name}'
                        df_resultados_display = df_resultados_display.rename(columns=rename_dict)
                        
                        st.markdown("### 📊 Resultados Consolidados + Top 10 Características SHAP")
                        st.dataframe(df_resultados_display, use_container_width=True)
                        
                        # Mostrar resumen de importancia (TOP 10)
                        st.markdown("### 🏆 Top 10 Características Más Importantes")
                        col1, col2, col3, col4, col5 = st.columns(5)
                        col6, col7, col8, col9, col10 = st.columns(5)
                        
                        cols_metrics = [col1, col2, col3, col4, col5, col6, col7, col8, col9, col10]
                        
                        # Asegurarse de que tenemos las claves correctas
                        top_names = shap_result.get('top10_names', [])
                        top_importance = shap_result.get('top10_importance', [])
                        
                        for i, (feat_name, importance) in enumerate(zip(top_names, top_importance)):
                            if i < len(cols_metrics):
                                with cols_metrics[i]:
                                    st.metric(f"#{i+1}", feat_name, f"SHAP: {importance:.4f}")
                    else:
                        st.warning("⚠️ No se pudo calcular SHAP. Mostrando resultados sin análisis SHAP...")
                        
                except Exception as shap_error:
                    st.warning(f"⚠️ Error calculando SHAP: {str(shap_error)}")
                
                st.markdown("---")
                st.markdown("### 💾 Descargar Resultados")
                
                # CSV
                csv_resultados = df_resultados_final.to_csv(index=False)
                st.download_button(
                    label="⬇️ Descargar Resultados (CSV)",
                    data=csv_resultados,
                    file_name="resultados_analisis_masivo.csv",
                    mime="text/csv",
                    key="download_csv"
                )
                
                # Excel
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df_resultados_final.to_excel(writer, sheet_name='Resultados', index=False)
                buffer.seek(0)
                
                st.download_button(
                    label="⬇️ Descargar Resultados (Excel)",
                    data=buffer,
                    file_name="resultados_analisis_masivo.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_excel"
                )
        
        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {str(e)}")
            import traceback
            st.error(f"Detalles del error: {traceback.format_exc()}")


def calcular_riesgo_paciente(row):
    """
    Calcula el riesgo de ansiedad para un paciente individual
    usando XGBoost Extendido con 22 FEATURES (EXACTO a resultados.py)
    """
    
    try:
        # Importar funciones de transformación
        from src.utils.calculos import (
            transformar_educacion_a_binaria,
            transformar_sf12_fisica_a_cuartil,
            transformar_sf12_mental_a_cuartil,
            transformar_lte12_a_clasificacion
        )
        
        # 1-2. TRANSFORMACIONES BINARIAS (consistente con calculos.py)
        edad24 = 0 if int(row['edad']) <= 24 else 1
        aefgroups = transformar_educacion_a_binaria(int(row['años_educacion']))
        
        # 3-6. SF-12 FÍSICA ONE-HOT (solo uno es 1)
        sf12f_cuartil = transformar_sf12_fisica_a_cuartil(float(row['sf12_fisica']))
        sf12f_q1 = 1 if sf12f_cuartil == 1 else 0
        sf12f_q2 = 1 if sf12f_cuartil == 2 else 0
        sf12f_q3 = 1 if sf12f_cuartil == 3 else 0
        sf12f_q4 = 1 if sf12f_cuartil == 4 else 0
        
        # 7-10. SF-12 MENTAL ONE-HOT (solo uno es 1)
        sf12m_cuartil = transformar_sf12_mental_a_cuartil(float(row['sf12_mental']))
        sf12m_q1 = 1 if sf12m_cuartil == 1 else 0
        sf12m_q2 = 1 if sf12m_cuartil == 2 else 0
        sf12m_q3 = 1 if sf12m_cuartil == 3 else 0
        sf12m_q4 = 1 if sf12m_cuartil == 4 else 0
        
        # 11-13. PRKCA ONE-HOT
        prkca_cc = 1 if row['prkca'] == 'C/C' else 0
        prkca_ct = 1 if row['prkca'] == 'C/T' else 0
        prkca_tt = 1 if row['prkca'] == 'T/T' else 0
        
        # 14-16. TCF4 ONE-HOT
        tcf4_aa = 1 if row['tcf4'] == 'A/A' else 0
        tcf4_at = 1 if row['tcf4'] == 'A/T' else 0
        tcf4_tt = 1 if row['tcf4'] == 'T/T' else 0
        
        # 17-19. CDH20 ONE-HOT
        cdh20_aa = 1 if row['cdh20'] == 'A/A' else 0
        cdh20_ag = 1 if row['cdh20'] == 'G/A' else 0
        cdh20_gg = 1 if row['cdh20'] == 'G/G' else 0
        
        # 20-22. LTE12 ONE-HOT (consistente con calculos.py: 0=0, 1=1, 2+=2)
        lte12_clasif = transformar_lte12_a_clasificacion(int(row['lte12_count']))
        lte12_0 = 1 if lte12_clasif == 0 else 0
        lte12_1 = 1 if lte12_clasif == 1 else 0
        lte12_2 = 1 if lte12_clasif == 2 else 0
        
        # VECTOR DE 22 FEATURES (ORDEN EXACTO DEL MODELO)
        features = np.array([[
            edad24, aefgroups,
            lte12_0, lte12_1, lte12_2,
            sf12f_q1, sf12f_q2, sf12f_q3, sf12f_q4,
            sf12m_q1, sf12m_q2, sf12m_q3, sf12m_q4,
            prkca_cc, prkca_ct, prkca_tt,
            tcf4_aa, tcf4_at, tcf4_tt,
            cdh20_aa, cdh20_ag, cdh20_gg
        ]])
        
        # Usar el modelo XGBoost Extendido
        try:
            modelo_path = "src/models/anxrisk_best_extended.joblib"
            modelo = joblib.load(modelo_path)
            riesgo_predicho = modelo.predict_proba(features)[0][1]
        except:
            # Si el modelo no se encuentra, hacer una predicción simple
            riesgo_predicho = calcular_riesgo_simple(row)
        
        # Determinar categoría de riesgo
        if riesgo_predicho < 0.3:
            categoria = "Bajo"
        elif riesgo_predicho < 0.7:
            categoria = "Moderado"
        else:
            categoria = "Alto"
        
        return {
            'nombre': row['nombre'],
            'edad': int(row['edad']),
            'genero': row['genero'],
            'años_educacion': int(row['años_educacion']),
            'hads_score': float(row['hads_score']),
            'zsas_score': float(row['zsas_score']),
            'sf12_fisica': int(row['sf12_fisica']),
            'sf12_mental': int(row['sf12_mental']),
            'lte12_count': int(row['lte12_count']),
            'prkca': row['prkca'],
            'tcf4': row['tcf4'],
            'cdh20': row['cdh20'],
            'riesgo_predicho': round(riesgo_predicho, 4),
            'categoria_riesgo': categoria
        }
    
    except Exception as e:
        # En lugar de usar st.warning (que puede no estar disponible), usar print
        print(f"⚠️ Error procesando {row.get('nombre', 'paciente desconocido')}: {str(e)}")
        # Retornar un resultado por defecto en caso de error
        return {
            'nombre': row.get('nombre', 'Error'),
            'edad': row.get('edad', 0),
            'genero': row.get('genero', 'Desconocido'),
            'años_educacion': row.get('años_educacion', 0),
            'hads_score': row.get('hads_score', 0),
            'zsas_score': row.get('zsas_score', 0),
            'sf12_fisica': row.get('sf12_fisica', 0),
            'sf12_mental': row.get('sf12_mental', 0),
            'lte12_count': row.get('lte12_count', 0),
            'prkca': row.get('prkca', 'T/T'),
            'tcf4': row.get('tcf4', 'A/A'),
            'cdh20': row.get('cdh20', 'G/G'),
            'riesgo_predicho': 0.0,
            'categoria_riesgo': 'Error'
        }


def calcular_riesgo_simple(row):
    """
    Calcula un riesgo simple basado en las métricas si el modelo no está disponible.
    Normaliza HADS y ZSAS para estimar un riesgo ponderado de apoyo.
    """
    hads_norm = min(float(row['hads_score']) / 42, 1.0)
    zsas_norm = min((float(row['zsas_score']) - 20) / 60, 1.0)
    sf12_mental_norm = 1 - (float(row['sf12_mental']) / 100)

    riesgo = (hads_norm * 0.3) + (zsas_norm * 0.3) + (sf12_mental_norm * 0.4)
    return round(riesgo, 4)
