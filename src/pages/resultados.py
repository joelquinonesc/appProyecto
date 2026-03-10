"""
Página de Resultados de la Evaluación
"""
import streamlit as st
from src.utils.dataframe_manager import mostrar_dataframe_actual, obtener_registro_actual
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import datetime
import os

from src.config import (
    MODEL_STANDARD_PATH,
    MODEL_EXTENDED_PATH,
    FEATURES_STANDARD,
    FEATURES_EXTENDED,
    GENOTIPOS_PRKCA,
    GENOTIPOS_TCF4,
    GENOTIPOS_CDH20,
)

# Helper: obtener mensaje según cuartil físico
def _obtener_mensaje_cuartil_fisica(cuartil):
    """Retorna mensaje interpretativo según el cuartil de salud física"""
    if cuartil == 1:
        return "📉 Salud Física Muy Baja (Q1): Experimentas limitaciones significativas en actividades físicas. Se recomienda evaluar con un profesional de salud."
    elif cuartil == 2:
        return "📊 Salud Física Baja (Q2): Tu salud física está por debajo del promedio. Considera mejorar tu nivel de actividad físico."
    elif cuartil == 3:
        return "📈 Salud Física Moderada (Q3): Tu salud física está en un nivel intermedio. Hay oportunidades para mejorar con ejercicio regular."
    elif cuartil == 4:
        return "✅ Salud Física Excelente (Q4): Gozas de muy buena salud física. Mantén tus hábitos saludables de actividad y ejercicio."
    else:
        return "ℹ️ Salud Física: Información no disponible"


# Helper: obtener mensaje según cuartil mental
def _obtener_mensaje_cuartil_mental(cuartil):
    """Retorna mensaje interpretativo según el cuartil de salud mental"""
    if cuartil == 1:
        return "📉 Salud Mental Muy Baja (Q1): Experimentas limitaciones significativas en tu bienestar emocional. Consulta con un profesional de salud mental."
    elif cuartil == 2:
        return "📊 Salud Mental Baja (Q2): Tu salud mental está por debajo del promedio. Considera buscar apoyo psicológico o emocional."
    elif cuartil == 3:
        return "📈 Salud Mental Moderada (Q3): Tu salud mental está en un nivel intermedio. Practica técnicas de bienestar emocional."
    elif cuartil == 4:
        return "✅ Salud Mental Excelente (Q4): Gozas de muy buen bienestar emocional y mental. Sigue manteniendo hábitos saludables."
    else:
        return "ℹ️ Salud Mental: Información no disponible"


# Helper: obtener cuartil físico a partir del registro de forma robusta
# (moved to module level so multiple functions in this module can use it)
def _obtener_sf12f_cuartil_desde_registro(reg):
    from src.utils.calculos import transformar_sf12_fisica_a_cuartil
    if not reg:
        return transformar_sf12_fisica_a_cuartil(0)
    # Priorizar columna numérica explícita si existe
    if reg.get('sf12_fisica_cuartil') is not None:
        try:
            return int(reg.get('sf12_fisica_cuartil'))
        except Exception:
            pass
    # Si existe etiqueta textual en el registro (p.ej. 'Q4')
    label = reg.get('sf12_fisica_cuartil_label') or reg.get('sf12_fisica')
    if isinstance(label, str) and label.upper().startswith('Q'):
        try:
            return int(label.upper().lstrip('Q'))
        except Exception:
            pass
    # Si el campo 'sf12_fisica' contiene un puntaje numérico, calcular cuartil desde el puntaje
    raw = reg.get('sf12_fisica')
    try:
        if raw is None:
            return transformar_sf12_fisica_a_cuartil(0)
        # Si raw ya es entero 1..4, usarlo
        if isinstance(raw, (int, float)) and int(raw) in (1,2,3,4):
            return int(raw)
        val = float(raw)
        # Si es un puntaje, convertir a cuartil
        return transformar_sf12_fisica_a_cuartil(val)
    except Exception:
        return transformar_sf12_fisica_a_cuartil(0)

def mostrar_resultados():
    # --- Cargar estilos CSS globales ---
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Título centrado y en negro
    st.markdown(
        "<h1 style='text-align: center; color: #2E2E2E; font-size: 2rem; font-weight: 700;'>📊 Resultados de la Evaluación</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align: center; color: #2E2E2E; font-size: 1.25rem; font-weight: 600; margin-bottom: 2rem;'>Análisis completo del riesgo de ansiedad</h3>",
        unsafe_allow_html=True
    )
    
    # Verificar que hay datos para mostrar
    if 'resultados' not in st.session_state or 'zsas' not in st.session_state.get('resultados', {}):
        st.warning("⚠️ No hay datos disponibles. Por favor, complete todos los cuestionarios primero.")
        if st.button("← Volver a Ansiedad (ZSAS)"):
            st.session_state.pagina_actual = 'Ansiedad (ZSAS)'
            st.rerun()
        return
    
    # Obtener registro actual
    registro = obtener_registro_actual()

    # Contenedor para exportar a HTML
    resultado_html = generar_html_resultados(st.session_state.resultados, registro)
    
    # Botón para exportar a HTML
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="📄 Descargar Reporte en HTML",
            data=resultado_html,
            file_name="reporte_evaluacion_ansiedad.html",
            mime="text/html",
            type="primary",
            use_container_width=True
        )
        st.info("💡 El archivo HTML descargado puede convertirse a PDF usando el navegador (Archivo → Imprimir → Guardar como PDF)")
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Mostrar resultados en tarjeta
    st.markdown("""
    <div style="background: #FFFFFF; padding: 2rem; border-radius: 12px; box-shadow: 0 3px 12px rgba(0,0,0,0.08); border: 1px solid #D1D1D1; margin: 1.5rem 0;">
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #2E2E2E; text-align: center; margin-bottom: 1.5rem;'>📋 Resumen de la Evaluación Completa</h3>", unsafe_allow_html=True)
    
    # Datos Demográficos
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>👤 Datos Demográficos</h4>", unsafe_allow_html=True)
    try:
        # Intentar obtener de resultados primero, luego de session_state directo
        demo_data = st.session_state.resultados.get('datos_demograficos') or st.session_state.get('datos_demograficos')
        if demo_data:
            demo_col1, demo_col2, demo_col3 = st.columns(3)
            with demo_col1:
                st.metric(label="Edad", value=f"{demo_data['edad']} años")
            with demo_col2:
                # Verificar si genero es número o texto
                if isinstance(demo_data.get('genero'), int):
                    genero_texto = "Masculino" if demo_data['genero'] == 0 else "Femenino" if demo_data['genero'] == 1 else "No especificado"
                else:
                    genero_texto = demo_data.get('genero', 'No especificado')
                st.metric(label="Género", value=genero_texto)
            with demo_col3:
                st.metric(label="Educación", value=f"{demo_data['años_educacion']} años")
        else:
            st.info("Datos demográficos no disponibles")
    except (KeyError, TypeError):
        st.info("Datos demográficos no disponibles")
    
    # Eventos Vitales
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>📅 Eventos Vitales (LTE-12)</h4>", unsafe_allow_html=True)
    try:
        eventos_data = st.session_state.resultados['eventos_vitales']
        st.metric(label="Eventos estresantes", value=f"{eventos_data['total']}")
    except KeyError:
        st.info("Datos de eventos vitales no disponibles")
    
    # SF-12
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>🏥 Salud Física y Mental (SF-12)</h4>", unsafe_allow_html=True)
    try:
        # The SF-12 pages store both scores under a single key 'sf12'
        sf12 = st.session_state.resultados.get('sf12', {})

        # Debug: mostrar qué hay en sf12
        # st.write(f"DEBUG sf12: {sf12}")

        fisica_val = sf12.get('puntaje_fisico') if isinstance(sf12, dict) else None
        mental_val = sf12.get('puntaje_mental') if isinstance(sf12, dict) else None
        cuartil_fisica = sf12.get('cuartil_fisica') if isinstance(sf12, dict) else None
        cuartil_mental = sf12.get('cuartil_mental') if isinstance(sf12, dict) else None

        if fisica_val is not None or mental_val is not None:
            sf12_col1, sf12_col2 = st.columns(2)
            with sf12_col1:
                if fisica_val is not None:
                    st.metric(label="Componente Físico", value=f"{float(fisica_val):.1f}")
                    # Mensaje según cuartil físico
                    mensaje_fisica = _obtener_mensaje_cuartil_fisica(cuartil_fisica)
                    st.info(mensaje_fisica)
                else:
                    st.info("Componente físico no disponible")
            with sf12_col2:
                if mental_val is not None:
                    st.metric(label="Componente Mental", value=f"{float(mental_val):.1f}")
                    # Mensaje según cuartil mental
                    mensaje_mental = _obtener_mensaje_cuartil_mental(cuartil_mental)
                    st.info(mensaje_mental)
                else:
                    st.info("Componente mental no disponible")
        else:
            st.info("Datos SF-12 no disponibles")
    except (KeyError, TypeError, ValueError) as e:
        st.info(f"Datos SF-12 no disponibles ({str(e)})")
    
    # HADS
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>😰 Ansiedad HADS</h4>", unsafe_allow_html=True)
    try:
        hads_data = st.session_state.resultados['hads']
        hads_col1, hads_col2 = st.columns(2)
        with hads_col1:
            st.metric(label="Puntaje", value=hads_data['puntaje'])
        with hads_col2:
            st.metric(label="Nivel", value=hads_data['nivel'])
    except KeyError:
        st.info("Datos HADS no disponibles")
    
    # ZSAS
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>😟 Ansiedad de Zung (ZSAS)</h4>", unsafe_allow_html=True)
    try:
        zsas_data = st.session_state.resultados['zsas']
        zsas_col1, zsas_col2 = st.columns(2)
        with zsas_col1:
            st.metric(label="Puntaje bruto", value=zsas_data['total'])
        with zsas_col2:
            st.metric(label="Nivel", value=zsas_data['nivel'])
    except KeyError:
        st.info("Datos ZSAS no disponibles")
    
    # Datos Genéticos (Opcionales)
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>🧬 Perfil Genético</h4>", unsafe_allow_html=True)
    genetico_data = st.session_state.resultados.get('datos_geneticos')
    if genetico_data:
        gen_col1, gen_col2, gen_col3 = st.columns(3)
        with gen_col1:
            st.markdown(f"""
            <div style='background: #F5F5F5; padding: 1rem; border-radius: 8px; border-left: 3px solid #4CAF50;'>
                <p style='color: #666; margin: 0; font-size: 0.9rem;'>Gen PRKCA</p>
                <p style='color: #2E2E2E; margin: 0; font-size: 1.3rem; font-weight: 700;'>{genetico_data['prkca']}</p>
            </div>
            """, unsafe_allow_html=True)
        with gen_col2:
            st.markdown(f"""
            <div style='background: #F5F5F5; padding: 1rem; border-radius: 8px; border-left: 3px solid #4CAF50;'>
                <p style='color: #666; margin: 0; font-size: 0.9rem;'>Gen TCF4</p>
                <p style='color: #2E2E2E; margin: 0; font-size: 1.3rem; font-weight: 700;'>{genetico_data['tcf4']}</p>
            </div>
            """, unsafe_allow_html=True)
        with gen_col3:
            st.markdown(f"""
            <div style='background: #F5F5F5; padding: 1rem; border-radius: 8px; border-left: 3px solid #4CAF50;'>
                <p style='color: #666; margin: 0; font-size: 0.9rem;'>Gen CDH20</p>
                <p style='color: #2E2E2E; margin: 0; font-size: 1.3rem; font-weight: 700;'>{genetico_data['cdh20']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Módulo genético no utilizado en esta evaluación")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Mostrar DataFrame completo
    st.markdown("---")
    st.markdown("<h3 style='color: #4CAF50; font-size: 1.5rem; margin-top: 2rem;'>📊 DataFrame Completo de la Evaluación</h3>", unsafe_allow_html=True)
    mostrar_dataframe_actual()
    
    # Predicción de riesgo con modelo
    st.markdown("---")
    st.markdown("<h3 style='color: #4CAF50; font-size: 1.5rem; margin-top: 2rem;'>🤖 Predicción de Riesgo de Ansiedad</h3>", unsafe_allow_html=True)

    # ── Sección de genética OPCIONAL ──────────────────────────────
    st.markdown("#### 🧬 ¿Dispone de datos genéticos del paciente?")
    tiene_genetica = st.toggle("Incluir panel genético (modelo extendido, 22 features)", value=False, key="toggle_genetica")

    if tiene_genetica:
        gen_col1, gen_col2, gen_col3 = st.columns(3)
        with gen_col1:
            prkca_sel = st.selectbox("Genotipo PRKCA", GENOTIPOS_PRKCA, key="gen_prkca_sel")
        with gen_col2:
            tcf4_sel = st.selectbox("Genotipo TCF4", GENOTIPOS_TCF4, key="gen_tcf4_sel")
        with gen_col3:
            cdh20_sel = st.selectbox("Genotipo CDH20", GENOTIPOS_CDH20, key="gen_cdh20_sel")
        st.session_state.resultados['datos_geneticos'] = {
            'prkca': prkca_sel, 'tcf4': tcf4_sel, 'cdh20': cdh20_sel
        }
    else:
        st.session_state.resultados['datos_geneticos'] = None
        st.info("ℹ️ Estimación basada en perfil clínico. La incorporación del panel genético podría refinar esta estimación.")

    if registro:
        genero = registro.get('genero')

        # Selección dinámica del modelo
        if tiene_genetica:
            model_path = MODEL_EXTENDED_PATH
            model_name = "CatBoost Extendido (22 features)"
            canonical_order = list(FEATURES_EXTENDED)
        else:
            model_path = MODEL_STANDARD_PATH
            model_name = "CatBoost Estándar (13 features)"
            canonical_order = list(FEATURES_STANDARD)

        try:
            import joblib
            model = joblib.load(model_path)

            # Preparar features
            from src.utils.calculos import transformar_lte12_a_clasificacion, transformar_sf12_fisica_a_cuartil, transformar_sf12_mental_a_cuartil, transformar_educacion_a_binaria
            
            edad24 = registro.get('grupo_edad', 0)
            aefgroups = transformar_educacion_a_binaria(registro.get('años_educacion', 0))
            
            lte12_clasif = transformar_lte12_a_clasificacion(registro.get('lte12_puntaje', 0))
            lte12_0 = 1 if lte12_clasif == 0 else 0
            lte12_1 = 1 if lte12_clasif == 1 else 0
            lte12_2 = 1 if lte12_clasif == 2 else 0
            
            # Antes: sf12f_cuartil = transformar_sf12_fisica_a_cuartil(registro.get('sf12_fisica', 0))
            sf12f_cuartil = _obtener_sf12f_cuartil_desde_registro(registro)
            sf12f_q1 = 1 if sf12f_cuartil == 1 else 0
            sf12f_q2 = 1 if sf12f_cuartil == 2 else 0
            sf12f_q3 = 1 if sf12f_cuartil == 3 else 0
            sf12f_q4 = 1 if sf12f_cuartil == 4 else 0
            
            sf12m_cuartil = transformar_sf12_mental_a_cuartil(registro.get('sf12_mental', 0))
            sf12m_q1 = 1 if sf12m_cuartil == 1 else 0
            sf12m_q2 = 1 if sf12m_cuartil == 2 else 0
            sf12m_q3 = 1 if sf12m_cuartil == 3 else 0
            sf12m_q4 = 1 if sf12m_cuartil == 4 else 0
            
            # Features base (13) — siempre presentes
            features_dict = {
                'EDAD24': edad24,
                'AEFGROUPS': aefgroups,
                'LTE12_0': lte12_0,
                'LTE12_1': lte12_1,
                'LTE12_2': lte12_2,
                'SF12F_Q1': sf12f_q1,
                'SF12F_Q2': sf12f_q2,
                'SF12F_Q3': sf12f_q3,
                'SF12F_Q4': sf12f_q4,
                'SF12M_Q1': sf12m_q1,
                'SF12M_Q2': sf12m_q2,
                'SF12M_Q3': sf12m_q3,
                'SF12M_Q4': sf12m_q4,
            }

            # Si hay genética, añadir 9 features one-hot (total 22)
            if tiene_genetica:
                gen_data = st.session_state.resultados['datos_geneticos']
                prkca = gen_data['prkca']
                tcf4 = gen_data['tcf4']
                cdh20 = gen_data['cdh20']

                features_dict['PRKCA_C/C'] = 1 if prkca == 'C/C' else 0
                features_dict['PRKCA_C/T'] = 1 if prkca == 'C/T' else 0
                features_dict['PRKCA_T/T'] = 1 if prkca == 'T/T' else 0
                features_dict['TCF4_A/A'] = 1 if tcf4 == 'A/A' else 0
                features_dict['TCF4_A/T'] = 1 if tcf4 == 'A/T' else 0
                features_dict['TCF4_T/T'] = 1 if tcf4 == 'T/T' else 0
                features_dict['CDH20_A/A'] = 1 if cdh20 == 'A/A' else 0
                features_dict['CDH20_A/G'] = 1 if cdh20 == 'A/G' else 0
                features_dict['CDH20_G/G'] = 1 if cdh20 == 'G/G' else 0
            
            # Construir DataFrame de features en el orden canónico definido por features_dict
            X = pd.DataFrame([features_dict])

            # Forzar el orden EXACTO del modelo para predicción
            canonical_order = list(features_dict.keys())
            try:
                X = X[canonical_order]
            except KeyError as e:
                st.error(f"Error construyendo features en el orden esperado: {e}")
                return

            # Preparar X que será enviada al modelo (todo interno, sin mensajes al usuario)
            model_features = None
            if hasattr(model, 'feature_names_in_'):
                model_features = list(model.feature_names_in_)
            elif hasattr(model, 'feature_name_'):
                model_features = list(model.feature_name_)

            # Default: usar X tal cual (orden canónico)
            X_for_model = X.copy()

            if model_features is not None:
                # Si el modelo espera exactamente las mismas columnas (mismos nombres), pero distinto orden,
                # reindexar internamente al orden del modelo para evitar incompatibilidades.
                if set(model_features) == set(canonical_order):
                    if model_features != canonical_order:
                        X_for_model = X[model_features]
                else:
                    # Si hay diferencia en el conjunto de nombres, reindexar a model_features rellenando con 0
                    # para columnas faltantes y descartando columnas extras.
                    X_for_model = X.reindex(columns=model_features, fill_value=0)

            # Mostrar features transformadas (mantener la visualización en orden canónico)
            modo_label = "Extendido (22 features)" if tiene_genetica else "Estándar (13 features)"
            features_display = {'GENERO': genero, **features_dict}
            X_display = pd.DataFrame([features_display])
            st.markdown(f"### 📊 Features Transformadas — Modo {modo_label}")
            st.dataframe(X_display, use_container_width=True, hide_index=True)

            # Predicción usando X_for_model (interno)
            prediction = model.predict(X_for_model)[0]

            # Obtener probabilidad de clase positiva si está disponible
            prob_alto = None
            if hasattr(model, 'predict_proba'):
                try:
                    prob_alto = float(model.predict_proba(X_for_model)[0][1])
                except Exception:
                    prob_alto = None

            # Clasificación final en tres niveles usando umbrales fijos
            from src.utils.calculos import clasificar_por_youden
            if prob_alto is not None:
                nivel_triple = clasificar_por_youden(prob_alto, None, ancho=0.10)
            else:
                # Si no hay probabilidad, usar la predicción binaria para mapear a Bajo/Alto
                nivel_triple = 'Alto' if prediction == 1 else 'Bajo'

            # Guardar datos en session_state para usar en PDF
            st.session_state.resultados['prob_alto'] = prob_alto
            st.session_state.resultados['nivel_triple'] = nivel_triple
            st.session_state.resultados['model'] = model
            st.session_state.resultados['X_for_model'] = X_for_model
            st.session_state.resultados['modelo_usado'] = model_name
            st.session_state.resultados['tiene_genetica'] = tiene_genetica

            riesgo = nivel_triple
            color = "#F44336" if nivel_triple == 'Alto' else "#FFB74D" if nivel_triple == 'Moderado' else "#4CAF50"

            st.markdown(f"""
            <div style='background: #FFFFFF; padding: 2.5rem; border-radius: 12px; box-shadow: 0 3px 12px rgba(0,0,0,0.08); border: 1px solid #D1D1D1; margin: 1.5rem 0; text-align: center;'>
                <h2 style='color: {color}; margin-bottom: 0.5rem; font-size: 2.5rem;'>{riesgo}</h2>
                <p style='color: #666; margin: 0.5rem 0; font-size: 1rem;'>Nivel de Riesgo de Ansiedad</p>
                <p style='color: #2E2E2E; margin: 0; font-size: 0.95rem;'>Probabilidad: <strong>{prob_alto:.1%}</strong></p>
            </div>
            """, unsafe_allow_html=True)

            # Explicación SHAP integrada
            mostrar_shap_analysis(model, X_for_model, genero)
            
        except FileNotFoundError:
            st.warning(f"Modelo no encontrado: {model_path}")
        except Exception as e:
            st.error(f"Error en la predicción: {str(e)}")
    else:
        st.info("No hay datos disponibles para predicción")
    
    # Nota final
    st.markdown("""
    <div style='margin-top: 1.5rem; padding: 1rem; background: #FFF9E6; border-radius: 8px; border-left: 4px solid #FFC107;'>
        <p style='color: #2E2E2E; margin: 0.5rem 0;'><strong>⚠️ Nota importante:</strong></p>
        <p style='color: #2E2E2E; margin: 0.5rem 0;'>
        Esta herramienta proporciona un análisis preliminar basado en modelos de aprendizaje automático supervisado. Los resultados deben ser interpretados en el contexto clínico completo del paciente y utilizados como apoyo en la toma de decisiones.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botones de navegación
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Volver a Ansiedad (ZSAS)", use_container_width=True):
            st.session_state.pagina_actual = 'Ansiedad (ZSAS)'
            st.rerun()
    with col3:
        if st.button("🔄 Nueva Evaluación", type="primary", use_container_width=True):
            # Limpiar toda la sesión
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            # Establecer página inicial
            st.session_state.pagina_actual = 'Home'
            st.rerun()


def mostrar_shap_analysis(model, X, genero):
    """Muestra el análisis SHAP"""
    st.markdown("### 📈 Análisis de Interpretabilidad del Modelo (SHAP)")
    st.markdown("""
    <div style='background: #E3F2FD; padding: 1rem; border-radius: 8px; border-left: 4px solid #2196F3; margin-bottom: 1.5rem;'>
        <p style='color: #1565C0; margin: 0; font-size: 0.95rem;'>
            <strong>ℹ️ ¿Qué es SHAP?</strong> SHAP (SHapley Additive exPlanations) es una técnica que explica cada predicción 
            mostrando el impacto de cada característica. Las gráficas y explicaciones a continuación detallen cómo el modelo llegó a esta conclusión.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        import shap
        import matplotlib
        matplotlib.use('Agg')  # Configurar backend no-interactivo para Streamlit
        import matplotlib.pyplot as plt
        try:
            from catboost import CatBoostClassifier
            has_catboost = True
        except ImportError:
            has_catboost = False
        try:
            import lightgbm as lgb
            has_lgb = True
        except ImportError:
            has_lgb = False
        
        feature_names = list(X.columns)
        X_array = X.values
        
        # Seleccionar el explicador SHAP según el tipo de modelo
        if has_catboost and isinstance(model, CatBoostClassifier):
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_array)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
        elif has_lgb and isinstance(model, lgb.LGBMClassifier):
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_array)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
        else:
            background_data = X_array
            explainer = shap.KernelExplainer(model.predict_proba, background_data, feature_names=feature_names)
            shap_values = explainer.shap_values(X_array)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
        
        if hasattr(shap_values, 'values'):
            shap_array = shap_values.values
        elif isinstance(shap_values, np.ndarray):
            shap_array = shap_values
        else:
            shap_array = np.array(shap_values)
        
        if shap_array.ndim == 1:
            shap_array = shap_array.reshape(1, -1)
        elif shap_array.ndim == 3:
            shap_array = shap_array[:, :, -1]
        
        # Gráfico SHAP
        n_features = X.shape[1]
        top_n = min(15, n_features) if n_features > 13 else 13
        st.markdown(f"#### 📊 Top {top_n} Características más Influyentes")
        top_indices = np.argsort(np.abs(shap_array[0]))[-top_n:][::-1]
        top_shap_values = shap_array[0][top_indices]
        top_feature_names = [feature_names[i] for i in top_indices]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = ['#DC3545' if val > 0 else '#28A745' for val in top_shap_values]
        ax.barh(range(len(top_shap_values)), top_shap_values, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
        ax.set_yticks(range(len(top_shap_values)))
        ax.set_yticklabels(top_feature_names, fontsize=10)
        ax.set_xlabel('SHAP Value (Contribución al Riesgo)', fontsize=12, fontweight='bold')
        ax.set_title('Impacto de Características en la Predicción', fontsize=14, fontweight='bold')
        ax.axvline(x=0, color='black', linestyle='-', linewidth=1.5)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#DC3545', alpha=0.8, edgecolor='black', label='Aumenta Riesgo'),
            Patch(facecolor='#28A745', alpha=0.8, edgecolor='black', label='Disminuye Riesgo')
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Explicación de colores SHAP
        st.markdown("""
        <div style='background: #F8F9FA; padding: 1rem; border-radius: 8px; border-left: 4px solid #6C757D; margin: 1rem 0;'>
            <p style='color: #2E2E2E; margin: 0; font-size: 0.95rem; font-weight: 600;'>
                📊 <strong>Interpretación de Colores:</strong>
            </p>
            <ul style='margin: 0.5rem 0 0 1rem; padding: 0;'>
                <li style='color: #DC3545; font-size: 0.9rem; margin: 0.3rem 0;'>
                    <strong>🔴 Barras rojas (hacia la derecha):</strong> Factores que <strong>AUMENTARON</strong> tu riesgo de ansiedad
                </li>
                <li style='color: #28A745; font-size: 0.9rem; margin: 0.3rem 0;'>
                    <strong>🟢 Barras verdes (hacia la izquierda):</strong> Factores que <strong>DISMINUYERON</strong> tu riesgo de ansiedad
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Explicación detallada de las características
        st.markdown("#### 📋 Explicación Detallada de los Factores")
        generar_interpretacion_shap(shap_array, feature_names, X, top_indices)
        
    except Exception as e:
        st.error(f"Error generando análisis SHAP: {str(e)}")


def generar_interpretacion_shap(shap_array, feature_names, X, top_indices):
    """Genera interpretación personalizada de SHAP para los top_indices proporcionados"""
    
    st.markdown("""
        <div style='background: #FFFFFF; padding: 1.5rem; border-radius: 8px; border: 1px solid #E0E0E0; margin-top: 1rem;'>
            <h4 style='color: #2E2E2E; margin-top: 0; border-bottom: 2px solid #4CAF50; padding-bottom: 0.5rem;'>
                🔍 Cómo se Llegó a Esta Predicción
            </h4>
            <p style='color: #666; margin: 1rem 0 0 0; font-size: 0.95rem;'>
                A continuación se detalla el impacto de cada factor en la predicción del riesgo de ansiedad:
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    for idx in top_indices:
        feature = feature_names[idx]
        shap_val = shap_array[0][idx]
        feature_val = X.iloc[0, idx]
        
        color = "#DC3545" if shap_val > 0 else "#28A745"
        efecto = "aumenta" if shap_val > 0 else "disminuye"
        icono = "⬆️" if shap_val > 0 else "⬇️"
        
        interpretacion = obtener_interpretacion_feature(feature, feature_val)
        
        st.markdown(f"""
        <div style='background: #F8F9FA; padding: 0.75rem; margin: 0.5rem 0; border-radius: 6px; border-left: 4px solid {color};'>
            <strong style='color: {color}; font-size: 0.95rem;'>{icono} {feature}</strong>
            <p style='color: #2E2E2E; margin: 0.3rem 0; font-size: 0.9rem;'>{interpretacion}</p>
            <p style='color: #666; margin: 0; font-size: 0.85rem;'>{efecto} riesgo (~{abs(shap_val):.3f} SHAP)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #FFF3CD; padding: 1rem; margin-top: 1.5rem; border-radius: 6px; border-left: 4px solid #FFC107;'>
        <p style='color: #856404; margin: 0; font-size: 0.95rem;'>
            <strong>💡 Resumen Clínico:</strong> El modelo considera principalmente la salud mental/física del paciente, 
            factores genéticos y eventos vitales estresantes para determinar el riesgo de ansiedad.
        </p>
    </div>
    """, unsafe_allow_html=True)


def obtener_interpretacion_feature(feature, feature_val):
    """Retorna interpretación clínica de una feature"""
    if feature == "EDAD24":
        return f"Grupo de edad {'24-34 años' if feature_val == 1 else 'fuera de 24-34 años'}"
    elif feature == "AEFGROUPS":
        return f"Nivel educativo {'superior (≥15 años)' if feature_val == 1 else 'básico/secundario (<15 años)'}"
    elif "SF12F" in feature:
        cuartil = feature.split("_")[1]
        if feature_val == 1:
            descripciones = {
                "Q1": "salud física muy baja (cuartil 1)",
                "Q2": "salud física baja (cuartil 2)",
                "Q3": "salud física moderada (cuartil 3)",
                "Q4": "salud física buena (cuartil 4)"
            }
            return f"Paciente presenta {descripciones.get(cuartil, cuartil)}"
        return f"No pertenece a este nivel de salud física ({cuartil})"
    elif "SF12M" in feature:
        cuartil = feature.split("_")[1]
        if feature_val == 1:
            descripciones = {
                "Q1": "salud mental muy baja (cuartil 1)",
                "Q2": "salud mental baja (cuartil 2)",
                "Q3": "salud mental moderada (cuartil 3)",
                "Q4": "salud mental buena (cuartil 4)"
            }
            return f"Paciente presenta {descripciones.get(cuartil, cuartil)}"
        return f"No pertenece a este nivel de salud mental ({cuartil})"
    elif "PRKCA" in feature:
        genotipo = feature.split("_")[1]
        return f"Genotipo PRKCA {genotipo} {'presente' if feature_val == 1 else 'ausente'} (regulación del estrés)"
    elif "TCF4" in feature:
        genotipo = feature.split("_")[1]
        return f"Genotipo TCF4 {genotipo} {'presente' if feature_val == 1 else 'ausente'} (transcripción neuronal)"
    elif "CDH20" in feature:
        genotipo = feature.split("_")[1]
        return f"Genotipo CDH20 {genotipo} {'presente' if feature_val == 1 else 'ausente'} (conectividad neuronal)"
    elif "LTE12" in feature:
        nivel = feature.split("_")[1]
        if feature_val == 1:
            descripciones = {
                "0": "sin eventos vitales estresantes",
                "1": "1 evento vital estresante",
                "2": "2 o más eventos vitales estresantes"
            }
            return f"Paciente experimentó {descripciones.get(nivel, nivel)}"
        return f"No se encuentra en esta categoría de eventos vitales ({nivel})"
    return f"Valor de la característica: {feature_val}"


def generar_html_resultados(resultados, registro):
    """Genera HTML completo para exportar a PDF"""
    html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Evaluación de Ansiedad</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #2E2E2E;
        }
        h1 { color: #4CAF50; text-align: center; }
        h2 { color: #4CAF50; border-bottom: 2px solid #E0E0E0; padding-bottom: 10px; }
        h3 { color: #2E2E2E; }
        .section {
            background: #F8F9FA;
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        .metric {
            display: inline-block;
            margin: 10px 20px 10px 0;
        }
        .metric-label {
            color: #666;
            font-size: 0.9rem;
        }
        .metric-value {
            color: #2E2E2E;
            font-size: 1.3rem;
            font-weight: bold;
        }
        .warning {
            background: #FFF9E6;
            padding: 15px;
            border-left: 4px solid #FFC107;
            border-radius: 8px;
            margin: 20px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th, td {
            border: 1px solid #E0E0E0;
            padding: 10px;
            text-align: left;
        }
        th {
            background: #4CAF50;
            color: white;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <h1>📊 Reporte de Evaluación de Ansiedad</h1>
    <p style="text-align: center; color: #666;">Análisis completo del riesgo de ansiedad</p>
"""
    
    # Datos demográficos
    demo_data = resultados.get('datos_demograficos') or st.session_state.get('datos_demograficos')
    if demo_data:
        # Verificar si genero es número o texto
        if isinstance(demo_data.get('genero'), int):
            genero_txt = "Masculino" if demo_data['genero'] == 0 else "Femenino"
        else:
            genero_txt = demo_data.get('genero', 'No especificado')
            
        html += f"""
    <h2>👤 Datos Demográficos</h2>
    <div class="section">
        <div class="metric">
            <div class="metric-label">Edad</div>
            <div class="metric-value">{demo_data['edad']} años</div>
        </div>
        <div class="metric">
            <div class="metric-label">Género</div>
            <div class="metric-value">{genero_txt}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Educación</div>
            <div class="metric-value">{demo_data['años_educacion']} años</div>
        </div>
    </div>
"""
    
    # Eventos vitales
    if 'eventos_vitales' in resultados:
        eventos = resultados['eventos_vitales']
        html += f"""
    <h2>📅 Eventos Vitales (LTE-12)</h2>
    <div class="section">
        <div class="metric">
            <div class="metric-label">Eventos estresantes</div>
            <div class="metric-value">{eventos['total']} eventos significativos</div>
        </div>
    </div>
"""
    
    # HADS
    if 'hads' in resultados:
        hads = resultados['hads']
        html += f"""
    <h2>😰 Ansiedad HADS</h2>
    <div class="section">
        <div class="metric">
            <div class="metric-label">Puntaje</div>
            <div class="metric-value">{hads['puntaje']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Nivel</div>
            <div class="metric-value">{hads['nivel']}</div>
        </div>
    </div>
"""
    
    # SF-12
    if 'sf12' in resultados:
        sf12 = resultados['sf12']
        fisica_val = sf12.get('puntaje_fisico')
        mental_val = sf12.get('puntaje_mental')
        cuartil_fisica = sf12.get('cuartil_fisica')
        cuartil_mental = sf12.get('cuartil_mental')
        
        if isinstance(sf12, dict):
            html += """
    <h2>� Salud SF-12</h2>
    <div class="section">
"""
            if fisica_val is not None:
                mensaje_fisica = _obtener_mensaje_cuartil_fisica(cuartil_fisica)
                html += f"""
        <h3>Componente Físico</h3>
        <div class="metric">
            <div class="metric-label">Puntaje</div>
            <div class="metric-value">{fisica_val:.1f}</div>
        </div>
        <p><em>{mensaje_fisica}</em></p>
"""
            if mental_val is not None:
                mensaje_mental = _obtener_mensaje_cuartil_mental(cuartil_mental)
                html += f"""
        <h3>Componente Mental</h3>
        <div class="metric">
            <div class="metric-label">Puntaje</div>
            <div class="metric-value">{mental_val:.1f}</div>
        </div>
        <p><em>{mensaje_mental}</em></p>
"""
            html += """
    </div>
"""
    
    # ZSAS
    if 'zsas' in resultados:
        zsas = resultados['zsas']
        html += f"""
    <h2>😟 Ansiedad de Zung (ZSAS)</h2>
    <div class="section">
        <div class="metric">
            <div class="metric-label">Puntaje bruto</div>
            <div class="metric-value">{zsas['total']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Nivel</div>
            <div class="metric-value">{zsas['nivel']}</div>
        </div>
    </div>
"""
    
    # Datos genéticos
    gen = resultados.get('datos_geneticos')
    if gen:
        html += f"""
    <h2>🧬 Perfil Genético</h2>
    <div class="section">
        <div class="metric">
            <div class="metric-label">Gen PRKCA</div>
            <div class="metric-value">{gen['prkca']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Gen TCF4</div>
            <div class="metric-value">{gen['tcf4']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Gen CDH20</div>
            <div class="metric-value">{gen['cdh20']}</div>
        </div>
    </div>
"""
    else:
        html += """
    <h2>🧬 Perfil Genético</h2>
    <div class="section">
        <p>Evaluación realizada sin datos genéticos (modo estándar, 13 features)</p>
    </div>
"""

    # Indicar modelo utilizado
    modelo_usado = resultados.get('modelo_usado', 'No especificado')
    html += f"""
    <div class="section">
        <div class="metric">
            <div class="metric-label">Modelo utilizado</div>
            <div class="metric-value">{modelo_usado}</div>
        </div>
    </div>
"""
    
    # Nota final
    html += """
    <div class="warning">
        <p><strong>⚠️ Nota importante:</strong></p>
        <p>Esta herramienta proporciona un análisis preliminar basado en modelos de aprendizaje automático supervisado. Los resultados deben ser interpretados en el contexto clínico completo del paciente y utilizados como apoyo en la toma de decisiones.</p>
    </div>
    
    <div class="footer">
        <p>Reporte generado automáticamente por el Sistema de Evaluación de Ansiedad ANXRISK</p>
        <p>Fecha de generación: """ + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    </div>
</body>
</html>
"""
    
    return html


def generar_pdf_resultados(resultados, registro):
    """Genera PDF completo para exportar usando ReportLab con diseño minimalista para salud"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, KeepTogether
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Backend sin interfaz gráfica
        from io import BytesIO
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4, 
            rightMargin=50, 
            leftMargin=50, 
            topMargin=50, 
            bottomMargin=50
        )
        
        # Contenedor de elementos
        elements = []
        
        # Paleta de colores minimalista para salud
        COLOR_PRIMARIO = colors.HexColor('#2C5F7C')  # Azul salud oscuro
        COLOR_SECUNDARIO = colors.HexColor('#5DA5C8')  # Azul salud claro
        COLOR_ACENTO = colors.HexColor('#7CB9D1')  # Azul pastel
        COLOR_TEXTO = colors.HexColor('#2E2E2E')  # Gris oscuro
        COLOR_FONDO = colors.HexColor('#F8F9FA')  # Gris muy claro
        COLOR_EXITO = colors.HexColor('#4CAF50')  # Verde
        COLOR_ALERTA = colors.HexColor('#FFC107')  # Amarillo
        COLOR_PELIGRO = colors.HexColor('#DC3545')  # Rojo
        
        # Estilos minimalistas
        styles = getSampleStyleSheet()
        
        # Título principal
        title_style = ParagraphStyle(
            'MinimalTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=COLOR_PRIMARIO,
            spaceAfter=8,
            spaceBefore=0,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=26
        )
        
        # Subtítulo
        subtitle_style = ParagraphStyle(
            'MinimalSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=COLOR_TEXTO,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica',
            leading=12
        )
        
        # Encabezados de sección
        heading_style = ParagraphStyle(
            'MinimalHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=COLOR_PRIMARIO,
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderPadding=0,
            leftIndent=0,
            leading=16
        )
        
        # Texto normal
        normal_style = ParagraphStyle(
            'MinimalNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            textColor=COLOR_TEXTO,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=13
        )
        
        # Estilo para métricas
        metric_style = ParagraphStyle(
            'MetricStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=COLOR_TEXTO,
            alignment=TA_CENTER,
            fontName='Helvetica',
            leading=11
        )
        
        # ==================== PORTADA ====================
        elements.append(Spacer(1, 0.5*inch))
        
        # Logo o línea decorativa minimalista
        elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━", 
            ParagraphStyle('Line', alignment=TA_CENTER, textColor=COLOR_SECUNDARIO, fontSize=16)))
        elements.append(Spacer(1, 0.3*inch))
        
        # Título
        elements.append(Paragraph("REPORTE DE EVALUACIÓN", title_style))
        elements.append(Paragraph("RIESGO DE ANSIEDAD", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Línea decorativa
        elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━", 
            ParagraphStyle('Line', alignment=TA_CENTER, textColor=COLOR_SECUNDARIO, fontSize=16)))
        elements.append(Spacer(1, 0.5*inch))

        # Logo o línea decorativa minimalista
        elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━", 
            ParagraphStyle('Line', alignment=TA_CENTER, textColor=COLOR_SECUNDARIO, fontSize=16)))
        elements.append(Spacer(1, 0.3*inch))
        
        # Título
        elements.append(Paragraph("REPORTE DE EVALUACIÓN", title_style))
        elements.append(Paragraph("RIESGO DE ANSIEDAD", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Línea decorativa
        elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━", 
            ParagraphStyle('Line', alignment=TA_CENTER, textColor=COLOR_SECUNDARIO, fontSize=16)))
        
        elements.append(Spacer(1, 0.5*inch))

        # Logo o línea decorativa minimalista
        elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━", 
            ParagraphStyle('Line', alignment=TA_CENTER, textColor=COLOR_SECUNDARIO, fontSize=16)))
        elements.append(Spacer(1, 0.3*inch))
        
        # Título
        elements.append(Paragraph("REPORTE DE EVALUACIÓN", title_style))
        elements.append(Paragraph("RIESGO DE ANSIEDAD", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Línea decorativa
        elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━", 
            ParagraphStyle('Line', alignment=TA_CENTER, textColor=COLOR_SECUNDARIO, fontSize=16)))
        
        elements.append(Spacer(1, 0.5*inch))

        # ==================== DATOS GENERALES ====================
        elements.append(Paragraph("Datos Generales", heading_style))
        
        # Datos demográficos
        try:
            demo_data = resultados.get('datos_demograficos') or st.session_state.get('datos_demograficos')
            if demo_data:
                # Verificar si genero es número o texto
                if isinstance(demo_data.get('genero'), int):
                    genero_txt = "Masculino" if demo_data['genero'] == 0 else "Femenino"
                else:
                    genero_txt = demo_data.get('genero', 'No especificado')
                
                data_demo = [
                    ["Edad", f"{demo_data['edad']} años"],
                    ["Género", genero_txt],
                    ["Nivel educativo", "Superior (≥15 años)" if demo_data.get('años_educacion', 0) >= 15 else "Básico/Secundario (<15 años)"],
                ]
                
                # Tabla de datos demográficos
                table = Table(data_demo, colWidths=[100, 150])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARIO),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ]))
                
                elements.append(table)
            else:
                elements.append(Paragraph("Datos demográficos no disponibles", normal_style))
        except Exception as e:
            elements.append(Paragraph(f"Error al cargar datos demográficos: {str(e)}", normal_style))
        
        elements.append(Spacer(1, 0.3*inch))

        # ==================== EVENTOS VITALES ====================
        elements.append(Paragraph("Eventos Vitales (LTE-12)", heading_style))
        
        # Eventos vitales
        try:
            eventos_data = resultados['eventos_vitales']
            data_eventos = [
                ["Total de eventos significativos", eventos_data.get('total', 0)],
                ["Eventos con impacto moderado a alto", eventos_data.get('impacto_moderado_alto', 0)],
                ["Eventos con impacto bajo", eventos_data.get('impacto_bajo', 0)],
            ]
            
            # Tabla de eventos vitales
            table = Table(data_eventos, colWidths=[200, 100])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARIO),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            
            elements.append(table)
        except Exception as e:
            elements.append(Paragraph(f"Error al cargar datos de eventos vitales: {str(e)}", normal_style))
        
        elements.append(Spacer(1, 0.3*inch))

        # ==================== SF-12 ====================
        elements.append(Paragraph("Salud Física y Mental (SF-12)", heading_style))
        
        # Datos SF-12
        try:
            sf12 = resultados.get('sf12', {})
            puntaje_fisico = sf12.get('puntaje_fisico', '-')
            puntaje_mental = sf12.get('puntaje_mental', '-')
            
            data_sf12 = [
                ["Puntaje Componente Físico", puntaje_fisico],
                ["Puntaje Componente Mental", puntaje_mental],
            ]
            
            # Tabla SF-12
            table = Table(data_sf12, colWidths=[200, 100])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARIO),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            
            elements.append(table)
        except Exception as e:
            elements.append(Paragraph(f"Error al cargar datos SF-12: {str(e)}", normal_style))
        
        elements.append(Spacer(1, 0.3*inch))

        # ==================== HADS ====================
        elements.append(Paragraph("Ansiedad HADS", heading_style))
        
        # Datos HADS
        try:
            hads = resultados.get('hads', {})
            puntaje_hads = hads.get('puntaje', '-')
            nivel_hads = hads.get('nivel', '-')
            
            data_hads = [
                ["Puntaje HADS", puntaje_hads],
                ["Nivel de Ansiedad", nivel_hads],
            ]
            
            # Tabla HADS
            table = Table(data_hads, colWidths=[200, 100])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARIO),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            
            elements.append(table)
        except Exception as e:
            elements.append(Paragraph(f"Error al cargar datos HADS: {str(e)}", normal_style))
        
        elements.append(Spacer(1, 0.3*inch))

        # ==================== ZSAS ====================
        elements.append(Paragraph("Ansiedad de Zung (ZSAS)", heading_style))
        
        # Datos ZSAS
        try:
            zsas = resultados.get('zsas', {})
            puntaje_zsas = zsas.get('total', '-')
            nivel_zsas = zsas.get('nivel', '-')
            
            data_zsas = [
                ["Puntaje bruto ZSAS", puntaje_zsas],
                ["Nivel de Ansiedad", nivel_zsas],
            ]
            
            # Tabla ZSAS
            table = Table(data_zsas, colWidths=[200, 100])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARIO),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            
            elements.append(table)
        except Exception as e:
            elements.append(Paragraph(f"Error al cargar datos ZSAS: {str(e)}", normal_style))
        
        elements.append(Spacer(1, 0.3*inch))

        # ==================== DATOS GENÉTICOS ====================
        elements.append(Paragraph("Perfil Genético", heading_style))
        
        # Datos genéticos
        try:
            genetico_data = resultados.get('datos_geneticos')
            if genetico_data:
                prkca = genetico_data.get('prkca', '-')
                tcf4 = genetico_data.get('tcf4', '-')
                cdh20 = genetico_data.get('cdh20', '-')
                
                data_genetico = [
                    ["Gen PRKCA", prkca],
                    ["Gen TCF4", tcf4],
                    ["Gen CDH20", cdh20],
                ]
                
                # Tabla de datos genéticos
                table = Table(data_genetico, colWidths=[200, 100])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARIO),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ]))
                
                elements.append(table)
            else:
                elements.append(Paragraph("Evaluación realizada sin datos genéticos (modo estándar, 13 features)", normal_style))
        except Exception as e:
            elements.append(Paragraph(f"Error al cargar datos genéticos: {str(e)}", normal_style))
        
        elements.append(Spacer(1, 0.3*inch))

        # ==================== PREDICCIÓN DE RIESGO CON SHAP ====================
        elements.append(PageBreak())
        elements.append(Paragraph("Análisis de Interpretabilidad del Modelo (SHAP)", heading_style))
        
        # Resultado de predicción
        try:
            prob_alto = resultados.get('prob_alto')
            nivel_triple = resultados.get('nivel_triple', 'No disponible')
            
            if prob_alto is not None:
                elements.append(Paragraph(f"Probabilidad de Alto Riesgo: {prob_alto:.1%}", normal_style))
                elements.append(Paragraph(f"Clasificación: {nivel_triple}", normal_style))
                
                # Umbrales fijos
                elements.append(Spacer(1, 0.2*inch))
                elements.append(Paragraph("Umbrales de Clasificación:", heading_style))
                
                data_thresholds = [
                    ["Categoría", "Rango de Probabilidad"],
                    ["Bajo", "0.00 - 0.29"],
                    ["Moderado", "0.30 - 0.59"],
                    ["Alto", "0.60 - 1.00"],
                ]
                
                table = Table(data_thresholds, colWidths=[150, 200])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARIO),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ]))
                
                elements.append(table)
                elements.append(Spacer(1, 0.3*inch))
                
                # Intento de agregar gráfico SHAP si está disponible
                try:
                    # Intentar generar SHAP dentro de la función de PDF
                    import shap
                    import matplotlib.pyplot as plt
                    try:
                        from catboost import CatBoostClassifier
                        has_catboost = True
                    except ImportError:
                        has_catboost = False
                    try:
                        import lightgbm as lgb
                        has_lgb = True
                    except ImportError:
                        has_lgb = False
                    
                    model = resultados.get('model')
                    X_for_model = resultados.get('X_for_model')
                    
                    if model is not None and X_for_model is not None:
                        feature_names = list(X_for_model.columns)
                        X_array = X_for_model.values
                        
                        # Preparar explicador según el tipo de modelo
                        try:
                            if has_catboost and isinstance(model, CatBoostClassifier):
                                explainer = shap.TreeExplainer(model)
                            elif has_lgb and isinstance(model, lgb.LGBMClassifier):
                                explainer = shap.TreeExplainer(model)
                            else:
                                background_data = X_array
                                explainer = shap.KernelExplainer(model.predict_proba, background_data, feature_names=feature_names)
                            
                            # Calcular SHAP values
                            shap_values = explainer.shap_values(X_array)
                            if isinstance(shap_values, list):
                                shap_values = shap_values[1]
                            
                            # Convertir a array si es necesario
                            if hasattr(shap_values, 'values'):
                                shap_array = shap_values.values
                            elif isinstance(shap_values, np.ndarray):
                                shap_array = shap_values
                            else:
                                shap_array = np.array(shap_values)
                            
                            # Asegurar que sea 2D
                            if shap_array.ndim == 1:
                                shap_array = shap_array.reshape(1, -1)
                            elif shap_array.ndim == 3:
                                shap_array = shap_array[:, :, -1]
                            
                            # Top 15 características
                            top_n = 15
                            top_indices = np.argsort(np.abs(shap_array[0]))[-top_n:][::-1]
                            top_shap_values = shap_array[0][top_indices]
                            top_feature_names = [feature_names[i] for i in top_indices]
                            
                            # Crear gráfico SHAP con tamaño más compacto
                            fig, ax = plt.subplots(figsize=(7, 5.5), dpi=100)
                            colors = ['#DC3545' if val > 0 else '#28A745' for val in top_shap_values]
                            ax.barh(range(len(top_shap_values)), top_shap_values, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
                            ax.set_yticks(range(len(top_shap_values)))
                            ax.set_yticklabels(top_feature_names, fontsize=8)
                            ax.set_xlabel('SHAP Value', fontsize=9, fontweight='bold')
                            ax.set_title('Top 15 Características más Influyentes', fontsize=10, fontweight='bold')
                            ax.axvline(x=0, color='black', linestyle='-', linewidth=1.5)
                            ax.grid(axis='x', alpha=0.3, linestyle='--')
                            plt.tight_layout()
                            
                            # Guardar figura en BytesIO
                            img_buffer = BytesIO()
                            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
                            img_buffer.seek(0)
                            plt.close(fig)
                            
                            # Agregar imagen al PDF con tamaño más pequeño
                            elements.append(Paragraph("Top 15 Características Influyentes:", heading_style))
                            img = Image(img_buffer, width=5.5*inch, height=4*inch)
                            elements.append(img)
                            
                            # Agregar interpretaciones de los factores
                            elements.append(Spacer(1, 0.2*inch))
                            elements.append(Paragraph("Explicación Detallada de Factores Clave:", heading_style))
                            
                            for idx_counter, idx in enumerate(top_indices[:10], 1):  # Top 10 para el PDF
                                feature = feature_names[idx]
                                shap_val = shap_array[0][idx]
                                feature_val = X_for_model.iloc[0, idx]
                                efecto = "aumenta" if shap_val > 0 else "disminuye"
                                
                                interpretacion = obtener_interpretacion_feature(feature, feature_val)
                                
                                texto_factor = f"{idx_counter}. {feature}: {interpretacion} ({efecto} riesgo)"
                                elements.append(Paragraph(texto_factor, normal_style))
                                elements.append(Spacer(1, 0.08*inch))
                        
                        except Exception as shap_calc_error:
                            elements.append(Paragraph(f"No fue posible generar el gráfico SHAP (error técnico)", normal_style))
                    else:
                        elements.append(Paragraph("Datos insuficientes para generar análisis SHAP", normal_style))
                
                except ImportError:
                    elements.append(Paragraph("Librerías SHAP no disponibles en este entorno", normal_style))
                except Exception as shap_error:
                    elements.append(Paragraph(f"Error en análisis SHAP: {str(shap_error)[:100]}", normal_style))
            else:
                elements.append(Paragraph("No hay probabilidad disponible para clasificar", normal_style))
        except Exception as e:
            elements.append(Paragraph(f"Error al cargar predicción SHAP: {str(e)[:100]}", normal_style))
        
        elements.append(Spacer(1, 0.3*inch))

        # ==================== NOTA FINAL ====================
        elements.append(Paragraph("Nota Importante", heading_style))
        
        # Nota final
        try:
            elements.append(Paragraph("Esta herramienta proporciona un análisis preliminar basado en modelos de aprendizaje automático supervisado. Los resultados deben ser interpretados en el contexto clínico completo del paciente y utilizados como apoyo en la toma de decisiones.", normal_style))
        except Exception as e:
            elements.append(Paragraph(f"Error al cargar nota final: {str(e)}", normal_style))
        
        elements.append(Spacer(1, 0.5*inch))
        
        # ==================== GRÁFICOS ====================
        # Gráfico de barras de ejemplo (se puede reemplazar por gráficos reales)
        try:
            fig, ax = plt.subplots(figsize=(8, 4))
            categorias = ['Grupo 1', 'Grupo 2', 'Grupo 3', 'Grupo 4']
            valores = [10, 20, 15, 25]
            ax.bar(categorias, valores, color=[COLOR_EXITO, COLOR_ALERTA, COLOR_PELIGRO, COLOR_PRIMARIO])
            ax.set_xlabel('Categorías')
            ax.set_ylabel('Valores')
            ax.set_title('Gráfico de Ejemplo')
            plt.tight_layout()
            
            # Guardar gráfico en buffer
            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            
            # Insertar gráfico en el PDF
            elements.append(Image(buf, width=6*inch, height=3*inch))
            buf.close()
        except Exception as e:
            elements.append(Paragraph(f"Error al generar gráfico: {str(e)}", normal_style))
        
        # ==================== FOOTER ====================
        # Página de agradecimiento o información adicional
        elements.append(PageBreak())
        elements.append(Paragraph("Gracias por utilizar el Sistema de Evaluación de Ansiedad ANXRISK.", normal_style))
        elements.append(Paragraph("Para más información, consulte a su profesional de la salud.", normal_style))
        
        # Construir documento PDF
        doc.build(elements)
        
        # Obtener el PDF como bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    except Exception as e:
        raise RuntimeError(f"Error generando PDF: {str(e)}")

