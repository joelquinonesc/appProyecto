"""
Página de Análisis Masivo - Procesa múltiples pacientes desde CSV
"""
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import joblib

from src.config import (
    MODEL_STANDARD_PATH,
    MODEL_EXTENDED_PATH,
    FEATURES_STANDARD,
    FEATURES_EXTENDED,
    GENOTIPOS_PRKCA,
    GENOTIPOS_TCF4,
    GENOTIPOS_CDH20,
    THRESHOLD_LOW,
    THRESHOLD_HIGH,
)
from src.utils.calculos import (
    transformar_edad_a_grupo,
    transformar_educacion_a_binaria,
    transformar_lte12_a_clasificacion,
    transformar_sf12_fisica_a_cuartil,
    transformar_sf12_mental_a_cuartil,
)

def mostrar_analisis_masivo():
    """Muestra la interfaz de análisis masivo de pacientes"""

    # Navigation back
    col_back, col_spacer = st.columns([1, 3])
    with col_back:
        if st.button("← Volver al Inicio", key="masivo_volver"):
            st.session_state.pagina_actual = "Home"
            st.rerun()

    st.markdown("""
    <div class="anxrisk-page-header">
        <h1>Análisis Masivo de Pacientes</h1>
        <p>Carga un archivo CSV para evaluar múltiples participantes de forma simultánea</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="anxrisk-card">
        <p><strong>Instrucciones:</strong> Carga un archivo CSV con los datos de tus participantes.
        El sistema calculará automáticamente el riesgo de ansiedad y generará un reporte detallado.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Template download ──
    st.markdown("### Descargar Plantilla CSV")

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
        'prkca': ['C/T', 'T/T', ''],
        'tcf4': ['A/T', 'A/A', ''],
        'cdh20': ['G/A', 'G/G', '']
    })

    csv_plantilla = plantilla_df.to_csv(index=False)
    st.download_button(
        label="Descargar Plantilla CSV",
        data=csv_plantilla,
        file_name="plantilla_pacientes.csv",
        mime="text/csv"
    )

    with st.expander("Descripción de columnas"):
        st.markdown("""
        | Columna | Descripción |
        |---------|-------------|
        | **nombre** | Nombre completo del paciente |
        | **edad** | Edad en años (1–120) |
        | **genero** | Masculino o Femenino |
        | **años_educacion** | Años de educación formal |
        | **hads_score** | Puntuación HADS (0–42, >8 indica riesgo) |
        | **zsas_score** | Puntuación ZSAS (20–80, >36 indica riesgo) |
        | **sf12_fisica** | Puntuación SF-12 Física (0–100) |
        | **sf12_mental** | Puntuación SF-12 Mental (0–100) |
        | **lte12_count** | Eventos vitales estresantes (0–12) |
        | **prkca** | *(opcional)* Genotipo: T/T, C/T, C/C |
        | **tcf4** | *(opcional)* Genotipo: A/A, A/T, T/T |
        | **cdh20** | *(opcional)* Genotipo: A/A, A/G, G/G |
        """)
        st.markdown("""
        <div class="anxrisk-note">
            <p>Si las columnas genéticas están vacías o contienen "N/A", se usa el <strong>modelo estándar (13 features)</strong>.
            Si contienen valores válidos, se usa el <strong>modelo extendido (22 features)</strong>.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── DATOS DEL PROFESIONAL EVALUADOR ──
    st.markdown("""
    <div class="anxrisk-card" style="border-left: 4px solid var(--primary);">
        <h3>👨‍⚕️ Datos del Profesional Evaluador</h3>
        <p style="font-size: 0.9375rem; color: var(--text-secondary); margin-bottom: 0.75rem;">
            Complete estos datos para que aparezcan en los reportes generados.
        </p>
    </div>
    """, unsafe_allow_html=True)
    prof_col1, prof_col2 = st.columns(2)
    with prof_col1:
        st.text_input("Nombre del profesional", key="masivo_prof_nombre", placeholder="Dr(a). Nombre Apellido")
        st.text_input("Cargo / Especialidad", key="masivo_prof_cargo", placeholder="Psiquiatra / Psicólogo clínico")
    with prof_col2:
        st.text_input("Institución", key="masivo_prof_institucion", placeholder="Hospital / Consultorio / IPS")
        st.text_input("Registro profesional", key="masivo_prof_registro", placeholder="TP-XXXXX")

    st.markdown("---")

    # ── Upload ──
    st.markdown("### Cargar Archivo CSV")

    uploaded_file = st.file_uploader(
        "Selecciona tu archivo CSV",
        type="csv",
        help="Asegúrate de que el CSV tenga todas las columnas requeridas"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            columnas_requeridas = [
                'nombre', 'edad', 'genero', 'años_educacion', 'hads_score',
                'zsas_score', 'sf12_fisica', 'sf12_mental', 'lte12_count'
            ]
            columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]

            if columnas_faltantes:
                st.error(f"Faltan las siguientes columnas: {', '.join(columnas_faltantes)}")
                return

            st.success(f"Archivo cargado correctamente: {len(df)} pacientes")

            st.markdown("### Vista Previa de Datos")
            st.dataframe(df.head(10), use_container_width=True)

            # Process button
            if st.button("Procesar y Generar Reportes", key="process_button", type="primary", use_container_width=True):
                st.markdown("---")
                st.markdown("### Procesando pacientes…")

                progress_bar = st.progress(0)
                status_text = st.empty()
                results = []

                for idx, (_, row) in enumerate(df.iterrows()):
                    status_text.text(f"Procesando: {row['nombre']} ({idx+1}/{len(df)})")
                    resultado = calcular_riesgo_paciente(row)
                    results.append(resultado)
                    progress_bar.progress((idx + 1) / len(df))

                valid_results = [r for r in results if r is not None and r.get('categoria_riesgo') != 'Error']
                df_resultados = pd.DataFrame(valid_results)

                if len(valid_results) < len(results):
                    st.warning(f"Se procesaron {len(valid_results)} de {len(results)} pacientes correctamente.")

                st.success("Procesamiento completado")
                st.markdown("---")

                # Consolidated results
                st.markdown("### Resultados Consolidados")
                st.dataframe(df_resultados, use_container_width=True)
                df_resultados_final = df_resultados

                # One-hot feature table
                st.markdown("---")
                st.markdown("### Codificación de Features para el Modelo MLP")

                features_detallados = []
                for _, row in df.iterrows():
                    tiene_gen = _paciente_tiene_genetica(row)

                    edad24 = transformar_edad_a_grupo(int(row['edad']))
                    aefgroups = transformar_educacion_a_binaria(int(row['años_educacion']))

                    lte12_clasif = transformar_lte12_a_clasificacion(int(row['lte12_count']))
                    lte12_0 = 1 if lte12_clasif == 0 else 0
                    lte12_1 = 1 if lte12_clasif == 1 else 0
                    lte12_2 = 1 if lte12_clasif == 2 else 0

                    sf12f_cuartil = transformar_sf12_fisica_a_cuartil(float(row['sf12_fisica']))
                    sf12f_q1 = 1 if sf12f_cuartil == 1 else 0
                    sf12f_q2 = 1 if sf12f_cuartil == 2 else 0
                    sf12f_q3 = 1 if sf12f_cuartil == 3 else 0
                    sf12f_q4 = 1 if sf12f_cuartil == 4 else 0

                    sf12m_cuartil = transformar_sf12_mental_a_cuartil(float(row['sf12_mental']))
                    sf12m_q1 = 1 if sf12m_cuartil == 1 else 0
                    sf12m_q2 = 1 if sf12m_cuartil == 2 else 0
                    sf12m_q3 = 1 if sf12m_cuartil == 3 else 0
                    sf12m_q4 = 1 if sf12m_cuartil == 4 else 0

                    feat = {
                        'Paciente': row['nombre'],
                        'Modelo': 'Extendido' if tiene_gen else 'Estándar',
                        '1-EDAD24': edad24,
                        '2-AEFGROUPS': aefgroups,
                        '3-LTE12_0': lte12_0,
                        '4-LTE12_1': lte12_1,
                        '5-LTE12_2': lte12_2,
                        '6-SF12F_Q1': sf12f_q1,
                        '7-SF12F_Q2': sf12f_q2,
                        '8-SF12F_Q3': sf12f_q3,
                        '9-SF12F_Q4': sf12f_q4,
                        '10-SF12M_Q1': sf12m_q1,
                        '11-SF12M_Q2': sf12m_q2,
                        '12-SF12M_Q3': sf12m_q3,
                        '13-SF12M_Q4': sf12m_q4,
                    }

                    if tiene_gen:
                        prkca_val = str(row.get('prkca', ''))
                        tcf4_val = str(row.get('tcf4', ''))
                        cdh20_val = str(row.get('cdh20', ''))
                        feat.update({
                            '14-PRKCA_C/C': 1 if prkca_val == 'C/C' else 0,
                            '15-PRKCA_C/T': 1 if prkca_val == 'C/T' else 0,
                            '16-PRKCA_T/T': 1 if prkca_val == 'T/T' else 0,
                            '17-TCF4_A/A': 1 if tcf4_val == 'A/A' else 0,
                            '18-TCF4_A/T': 1 if tcf4_val == 'A/T' else 0,
                            '19-TCF4_T/T': 1 if tcf4_val == 'T/T' else 0,
                            '20-CDH20_A/A': 1 if cdh20_val == 'A/A' else 0,
                            '21-CDH20_A/G': 1 if cdh20_val in ('A/G', 'G/A') else 0,
                            '22-CDH20_G/G': 1 if cdh20_val == 'G/G' else 0,
                        })

                    features_detallados.append(feat)

                df_features = pd.DataFrame(features_detallados)
                st.dataframe(df_features, use_container_width=True)

                with st.expander("Explicación de los Features"):
                    st.markdown("""
                    **Binarias Transformadas (2):**
                    - 1: **EDAD24** — 0 si edad ≤ 24 años, 1 si edad > 24
                    - 2: **AEFGROUPS** — 0 si años educación ≤ 14, 1 si ≥ 15

                    **LTE-12 (3 features one-hot):**
                    - 3: **LTE12_0** — 1 si 0 eventos estresantes
                    - 4: **LTE12_1** — 1 si 1 evento estresante
                    - 5: **LTE12_2** — 1 si 2 o más eventos estresantes

                    **SF-12 Física (4 features one-hot):**
                    - 6–9: **SF12F_Q1 a Q4** — Cuartiles según umbrales:
                      Q1: ≤15 | Q2: 15<x≤17 | Q3: 17<x≤19 | Q4: >19

                    **SF-12 Mental (4 features one-hot):**
                    - 10–13: **SF12M_Q1 a Q4** — Cuartiles según umbrales:
                      Q1: ≤15 | Q2: ≤18 | Q3: ≤21 | Q4: ≥22

                    **Panel Genético *(solo modelo extendido)*:**
                    - 14–16: **PRKCA** — C/C, C/T, T/T (one-hot)
                    - 17–19: **TCF4** — A/A, A/T, T/T (one-hot)
                    - 20–22: **CDH20** — A/A, A/G, G/G (one-hot)

                    **Modelo Estándar: 13 Features** | **Modelo Extendido: 22 Features**
                    """)

                # Statistics
                st.markdown("### Estadísticas Generales")

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

                # SHAP analysis
                st.markdown("### Calculando Análisis SHAP…")
                shap_progress = st.progress(0)

                try:
                    import sys
                    sys.path.insert(0, '/Users/breynerjoelquinonescastro/Documents/APP ANXRISK')
                    from scripts.shap_integration_masivo import main_shap_integration

                    shap_result = main_shap_integration(
                        df[['nombre', 'edad', 'años_educacion', 'lte12_count',
                            'sf12_fisica', 'sf12_mental', 'prkca', 'tcf4', 'cdh20']]
                    )
                    shap_progress.progress(100)

                    if shap_result:
                        df_shap_cols = shap_result['df_with_shap'].copy()
                        shap_cols = [col for col in df_shap_cols.columns if col.startswith('SHAP_')]

                        df_resultados_final = df_resultados.copy()
                        for shap_col in shap_cols:
                            df_resultados_final[shap_col] = df_shap_cols[shap_col].values

                        cols_to_display = ['nombre', 'riesgo_predicho', 'categoria_riesgo'] + shap_cols
                        df_resultados_display = df_resultados_final[cols_to_display].copy()

                        rename_dict = {}
                        for col in shap_cols:
                            feature_name = col.replace('SHAP_', '')
                            rename_dict[col] = f'SHAP: {feature_name}'
                        df_resultados_display = df_resultados_display.rename(columns=rename_dict)

                        st.markdown("### Resultados Consolidados + Top 10 Características SHAP")
                        st.dataframe(df_resultados_display, use_container_width=True)

                        # Top 10 importance
                        st.markdown("### Top 10 Características Más Importantes")
                        col1, col2, col3, col4, col5 = st.columns(5)
                        col6, col7, col8, col9, col10 = st.columns(5)

                        cols_metrics = [col1, col2, col3, col4, col5, col6, col7, col8, col9, col10]

                        top_names = shap_result.get('top10_names', [])
                        top_importance = shap_result.get('top10_importance', [])

                        for i, (feat_name, importance) in enumerate(zip(top_names, top_importance)):
                            if i < len(cols_metrics):
                                with cols_metrics[i]:
                                    st.metric(f"#{i+1}", feat_name, f"SHAP: {importance:.4f}")
                    else:
                        st.warning("No se pudo calcular SHAP. Mostrando resultados sin análisis SHAP.")

                except Exception as shap_error:
                    st.warning(f"Error calculando SHAP: {str(shap_error)}")

                st.markdown("---")
                st.markdown("### Descargar Resultados")

                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    csv_resultados = df_resultados_final.to_csv(index=False)
                    st.download_button(
                        label="Descargar Resultados (CSV)",
                        data=csv_resultados,
                        file_name="resultados_analisis_masivo.csv",
                        mime="text/csv",
                        key="download_csv",
                        use_container_width=True
                    )

                with col_dl2:
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        df_resultados_final.to_excel(writer, sheet_name='Resultados', index=False)
                    buffer.seek(0)

                    st.download_button(
                        label="Descargar Resultados (Excel)",
                        data=buffer,
                        file_name="resultados_analisis_masivo.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_excel",
                        use_container_width=True
                    )

        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")
            import traceback
            st.error(f"Detalles del error: {traceback.format_exc()}")


def _paciente_tiene_genetica(row):
    """Detecta si un registro CSV tiene datos genéticos válidos."""
    for col in ('prkca', 'tcf4', 'cdh20'):
        val = str(row.get(col, '')).strip()
        if val == '' or val.lower() in ('n/a', 'na', 'nan', 'none', '-'):
            return False
    return True


def calcular_riesgo_paciente(row):
    """
    Calcula el riesgo de ansiedad para un paciente individual.
    Usa modelo estándar (13 features) o extendido (22 features) según
    disponibilidad de datos genéticos.
    """

    try:
        tiene_gen = _paciente_tiene_genetica(row)

        edad24 = transformar_edad_a_grupo(int(row['edad']))
        aefgroups = transformar_educacion_a_binaria(int(row['años_educacion']))

        lte12_clasif = transformar_lte12_a_clasificacion(int(row['lte12_count']))
        lte12_0 = 1 if lte12_clasif == 0 else 0
        lte12_1 = 1 if lte12_clasif == 1 else 0
        lte12_2 = 1 if lte12_clasif == 2 else 0

        sf12f_cuartil = transformar_sf12_fisica_a_cuartil(float(row['sf12_fisica']))
        sf12f_q1 = 1 if sf12f_cuartil == 1 else 0
        sf12f_q2 = 1 if sf12f_cuartil == 2 else 0
        sf12f_q3 = 1 if sf12f_cuartil == 3 else 0
        sf12f_q4 = 1 if sf12f_cuartil == 4 else 0

        sf12m_cuartil = transformar_sf12_mental_a_cuartil(float(row['sf12_mental']))
        sf12m_q1 = 1 if sf12m_cuartil == 1 else 0
        sf12m_q2 = 1 if sf12m_cuartil == 2 else 0
        sf12m_q3 = 1 if sf12m_cuartil == 3 else 0
        sf12m_q4 = 1 if sf12m_cuartil == 4 else 0

        base_features = [
            edad24, aefgroups,
            lte12_0, lte12_1, lte12_2,
            sf12f_q1, sf12f_q2, sf12f_q3, sf12f_q4,
            sf12m_q1, sf12m_q2, sf12m_q3, sf12m_q4,
        ]

        if tiene_gen:
            prkca_val = str(row['prkca']).strip()
            tcf4_val = str(row['tcf4']).strip()
            cdh20_val = str(row['cdh20']).strip()

            gen_features = [
                1 if prkca_val == 'C/C' else 0,
                1 if prkca_val == 'C/T' else 0,
                1 if prkca_val == 'T/T' else 0,
                1 if tcf4_val == 'A/A' else 0,
                1 if tcf4_val == 'A/T' else 0,
                1 if tcf4_val == 'T/T' else 0,
                1 if cdh20_val == 'A/A' else 0,
                1 if cdh20_val in ('A/G', 'G/A') else 0,
                1 if cdh20_val == 'G/G' else 0,
            ]
            features = np.array([base_features + gen_features])
            modelo_path = MODEL_EXTENDED_PATH
            modelo_label = 'Extendido'
        else:
            features = np.array([base_features])
            modelo_path = MODEL_STANDARD_PATH
            modelo_label = 'Estándar'

        try:
            modelo = joblib.load(modelo_path)
            riesgo_predicho = modelo.predict_proba(features)[0][1]
        except Exception:
            riesgo_predicho = calcular_riesgo_simple(row)

        if riesgo_predicho < THRESHOLD_LOW:
            categoria = "Bajo"
        elif riesgo_predicho < THRESHOLD_HIGH:
            categoria = "Moderado"
        else:
            categoria = "Alto"

        resultado = {
            'nombre': row['nombre'],
            'edad': int(row['edad']),
            'genero': row['genero'],
            'años_educacion': int(row['años_educacion']),
            'hads_score': float(row['hads_score']),
            'zsas_score': float(row['zsas_score']),
            'sf12_fisica': float(row['sf12_fisica']),
            'sf12_mental': float(row['sf12_mental']),
            'lte12_count': int(row['lte12_count']),
            'riesgo_predicho': round(riesgo_predicho, 4),
            'categoria_riesgo': categoria,
            'modelo': modelo_label,
        }

        if tiene_gen:
            resultado['prkca'] = str(row['prkca'])
            resultado['tcf4'] = str(row['tcf4'])
            resultado['cdh20'] = str(row['cdh20'])
        else:
            resultado['prkca'] = 'N/A'
            resultado['tcf4'] = 'N/A'
            resultado['cdh20'] = 'N/A'

        return resultado

    except Exception as e:
        print(f"Error procesando {row.get('nombre', 'paciente desconocido')}: {str(e)}")
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
            'prkca': row.get('prkca', 'N/A'),
            'tcf4': row.get('tcf4', 'N/A'),
            'cdh20': row.get('cdh20', 'N/A'),
            'riesgo_predicho': 0.0,
            'categoria_riesgo': 'Error',
            'modelo': 'N/A',
        }


def calcular_riesgo_simple(row):
    """
    Calcula un riesgo simple basado en las métricas si el modelo no está disponible
    """
    hads_norm = min(float(row['hads_score']) / 42, 1.0)
    zsas_norm = min((float(row['zsas_score']) - 20) / 60, 1.0)
    sf12_mental_norm = 1 - (float(row['sf12_mental']) / 100)

    riesgo = (hads_norm * 0.3) + (zsas_norm * 0.3) + (sf12_mental_norm * 0.4)

    return round(riesgo, 4)
