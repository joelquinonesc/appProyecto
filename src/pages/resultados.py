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


def _obtener_mensaje_cuartil_fisica(cuartil):
    """Retorna mensaje interpretativo según el cuartil de salud física"""
    mensajes = {
        1: "Salud Física Muy Baja (Q1): Limitaciones significativas en actividades físicas.",
        2: "Salud Física Baja (Q2): Salud física por debajo del promedio.",
        3: "Salud Física Moderada (Q3): Nivel intermedio, oportunidades de mejora con ejercicio.",
        4: "Salud Física Excelente (Q4): Muy buena salud física.",
    }
    return mensajes.get(cuartil, "Salud Física: Información no disponible")


def _obtener_mensaje_cuartil_mental(cuartil):
    """Retorna mensaje interpretativo según el cuartil de salud mental"""
    mensajes = {
        1: "Salud Mental Muy Baja (Q1): Limitaciones significativas en bienestar emocional.",
        2: "Salud Mental Baja (Q2): Salud mental por debajo del promedio.",
        3: "Salud Mental Moderada (Q3): Nivel intermedio, considere técnicas de bienestar.",
        4: "Salud Mental Excelente (Q4): Muy buen bienestar emocional y mental.",
    }
    return mensajes.get(cuartil, "Salud Mental: Información no disponible")


def _obtener_sf12f_cuartil_desde_registro(reg):
    from src.utils.calculos import transformar_sf12_fisica_a_cuartil
    if not reg:
        return transformar_sf12_fisica_a_cuartil(0)
    if reg.get('sf12_fisica_cuartil') is not None:
        try:
            return int(reg.get('sf12_fisica_cuartil'))
        except Exception:
            pass
    label = reg.get('sf12_fisica_cuartil_label') or reg.get('sf12_fisica')
    if isinstance(label, str) and label.upper().startswith('Q'):
        try:
            return int(label.upper().lstrip('Q'))
        except Exception:
            pass
    raw = reg.get('sf12_fisica')
    try:
        if raw is None:
            return transformar_sf12_fisica_a_cuartil(0)
        if isinstance(raw, (int, float)) and int(raw) in (1,2,3,4):
            return int(raw)
        val = float(raw)
        return transformar_sf12_fisica_a_cuartil(val)
    except Exception:
        return transformar_sf12_fisica_a_cuartil(0)


def _risk_css_class(nivel):
    """Returns CSS class suffix for risk level."""
    mapping = {'Bajo': 'low', 'Moderado': 'moderate', 'Alto': 'high'}
    return mapping.get(nivel, 'moderate')


def mostrar_resultados():
    # Page header
    st.markdown("""
    <div class="anxrisk-page-header">
        <h1>Resultados de la Evaluación</h1>
        <p>Análisis completo del riesgo de ansiedad con interpretabilidad individual</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar datos
    if 'resultados' not in st.session_state or 'zsas' not in st.session_state.get('resultados', {}):
        st.warning("No hay datos disponibles. Complete todos los cuestionarios primero.")
        if st.button("Volver a Ansiedad (ZSAS)"):
            st.session_state.pagina_actual = 'Ansiedad (ZSAS)'
            st.rerun()
        return
    
    registro = obtener_registro_actual()

    # ── PROFESSIONAL DATA (read from persistent keys, set in demograficos) ──
    datos_profesional = {
        'nombre': st.session_state.get('_prof_nombre', '') or st.session_state.get('prof_nombre', ''),
        'cargo': st.session_state.get('_prof_cargo', '') or st.session_state.get('prof_cargo', ''),
        'institucion': st.session_state.get('_prof_institucion', '') or st.session_state.get('prof_institucion', ''),
        'registro_profesional': st.session_state.get('_prof_registro', '') or st.session_state.get('prof_registro', ''),
    }

    # ── CLINICAL SUMMARY ──
    st.markdown("""
    <div class="anxrisk-section-header">
        <h2>Resumen Clínico</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Demographics
    st.markdown("<h3>Datos Demográficos</h3>", unsafe_allow_html=True)
    try:
        demo_data = st.session_state.resultados.get('datos_demograficos') or st.session_state.get('datos_demograficos')
        if demo_data:
            demo_col1, demo_col2, demo_col3 = st.columns(3)
            with demo_col1:
                st.metric(label="Edad", value=f"{demo_data['edad']} años")
            with demo_col2:
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
    
    # Events
    st.markdown("<h3>Eventos Vitales (LTE-12)</h3>", unsafe_allow_html=True)
    try:
        eventos_data = st.session_state.resultados['eventos_vitales']
        st.metric(label="Eventos estresantes", value=f"{eventos_data['total']}")
    except KeyError:
        st.info("Datos de eventos vitales no disponibles")
    
    # SF-12
    st.markdown("<h3>Salud Física y Mental (SF-12)</h3>", unsafe_allow_html=True)
    try:
        sf12 = st.session_state.resultados.get('sf12', {})
        fisica_val = sf12.get('puntaje_fisico') if isinstance(sf12, dict) else None
        mental_val = sf12.get('puntaje_mental') if isinstance(sf12, dict) else None
        cuartil_fisica = sf12.get('cuartil_fisica') if isinstance(sf12, dict) else None
        cuartil_mental = sf12.get('cuartil_mental') if isinstance(sf12, dict) else None

        if fisica_val is not None or mental_val is not None:
            sf12_col1, sf12_col2 = st.columns(2)
            with sf12_col1:
                if fisica_val is not None:
                    st.metric(label="Componente Físico", value=f"{float(fisica_val):.1f}")
                    st.markdown(f'<div class="anxrisk-note"><p>{_obtener_mensaje_cuartil_fisica(cuartil_fisica)}</p></div>', unsafe_allow_html=True)
                else:
                    st.info("Componente físico no disponible")
            with sf12_col2:
                if mental_val is not None:
                    st.metric(label="Componente Mental", value=f"{float(mental_val):.1f}")
                    st.markdown(f'<div class="anxrisk-note"><p>{_obtener_mensaje_cuartil_mental(cuartil_mental)}</p></div>', unsafe_allow_html=True)
                else:
                    st.info("Componente mental no disponible")
        else:
            st.info("Datos SF-12 no disponibles")
    except (KeyError, TypeError, ValueError) as e:
        st.info(f"Datos SF-12 no disponibles ({str(e)})")
    
    # HADS
    st.markdown("<h3>Ansiedad HADS</h3>", unsafe_allow_html=True)
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
    st.markdown("<h3>Ansiedad de Zung (ZSAS)</h3>", unsafe_allow_html=True)
    try:
        zsas_data = st.session_state.resultados['zsas']
        zsas_col1, zsas_col2 = st.columns(2)
        with zsas_col1:
            st.metric(label="Puntaje bruto", value=zsas_data['total'])
        with zsas_col2:
            st.metric(label="Nivel", value=zsas_data['nivel'])
    except KeyError:
        st.info("Datos ZSAS no disponibles")
    
    # Genetic Profile
    st.markdown("<h3>Perfil Genético</h3>", unsafe_allow_html=True)
    genetico_data = st.session_state.resultados.get('datos_geneticos')
    if genetico_data:
        gen_col1, gen_col2, gen_col3 = st.columns(3)
        with gen_col1:
            st.markdown(f'<div class="anxrisk-genetic-tag">PRKCA: {genetico_data["prkca"]}</div>', unsafe_allow_html=True)
        with gen_col2:
            st.markdown(f'<div class="anxrisk-genetic-tag">TCF4: {genetico_data["tcf4"]}</div>', unsafe_allow_html=True)
        with gen_col3:
            st.markdown(f'<div class="anxrisk-genetic-tag">CDH20: {genetico_data["cdh20"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="anxrisk-note"><p>Módulo genético no utilizado en esta evaluación</p></div>', unsafe_allow_html=True)
    
    # DataFrame
    st.markdown("---")
    st.markdown("<h3>DataFrame Completo</h3>", unsafe_allow_html=True)
    mostrar_dataframe_actual()
    
    # ── PREDICTION ──
    st.markdown("---")
    st.markdown("""
    <div class="anxrisk-section-header">
        <h2>Predicción de Riesgo de Ansiedad</h2>
    </div>
    """, unsafe_allow_html=True)

    # Genetics toggle
    st.markdown("#### Panel genético (opcional)")
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
        st.markdown('<div class="anxrisk-note"><p>Estimación basada en perfil clínico. La incorporación del panel genético podría refinar esta estimación.</p></div>', unsafe_allow_html=True)

    # Calculate button
    btn_label = "Calcular Predicción con Panel Genético" if tiene_genetica else "Calcular Predicción (Modo Estándar)"
    calcular_clicked = st.button(btn_label, type="primary", use_container_width=True, key="btn_calcular_prediccion")

    if registro and calcular_clicked:
        genero = registro.get('genero')

        if tiene_genetica:
            model_path = MODEL_EXTENDED_PATH
            model_name = "MLP Extendido (22 features)"
        else:
            model_path = MODEL_STANDARD_PATH
            model_name = "MLP Estándar (13 features)"

        try:
            import joblib
            model = joblib.load(model_path)

            from src.utils.calculos import transformar_lte12_a_clasificacion, transformar_sf12_fisica_a_cuartil, transformar_sf12_mental_a_cuartil, transformar_educacion_a_binaria
            
            edad24 = registro.get('grupo_edad', 0)
            aefgroups = transformar_educacion_a_binaria(registro.get('años_educacion', 0))
            
            lte12_clasif = transformar_lte12_a_clasificacion(registro.get('lte12_puntaje', 0))
            lte12_0 = 1 if lte12_clasif == 0 else 0
            lte12_1 = 1 if lte12_clasif == 1 else 0
            lte12_2 = 1 if lte12_clasif == 2 else 0
            
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
            
            features_dict = {
                'EDAD24': edad24, 'AEFGROUPS': aefgroups,
                'LTE12_0': lte12_0, 'LTE12_1': lte12_1, 'LTE12_2': lte12_2,
                'SF12F_Q1': sf12f_q1, 'SF12F_Q2': sf12f_q2, 'SF12F_Q3': sf12f_q3, 'SF12F_Q4': sf12f_q4,
                'SF12M_Q1': sf12m_q1, 'SF12M_Q2': sf12m_q2, 'SF12M_Q3': sf12m_q3, 'SF12M_Q4': sf12m_q4,
            }

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
            
            expected_features = FEATURES_EXTENDED if tiene_genetica else FEATURES_STANDARD
            X = pd.DataFrame([features_dict])
            X = X[expected_features]

            X_for_model = X.copy()
            if hasattr(model, 'feature_names_in_'):
                model_features = list(model.feature_names_in_)
                if model_features != expected_features:
                    X_for_model = X.reindex(columns=model_features, fill_value=0)

            modo_label = "Extendido (22 features)" if tiene_genetica else "Estándar (13 features)"
            features_display = {'GENERO': genero, **features_dict}
            X_display = pd.DataFrame([features_display])
            st.markdown(f"### Features Transformadas — Modo {modo_label}")
            st.dataframe(X_display, use_container_width=True, hide_index=True)

            prediction = model.predict(X_for_model)[0]

            prob_alto = None
            if hasattr(model, 'predict_proba'):
                try:
                    prob_alto = float(model.predict_proba(X_for_model)[0][1])
                except Exception:
                    prob_alto = None

            from src.utils.calculos import clasificar_por_youden
            if prob_alto is not None:
                nivel_triple = clasificar_por_youden(prob_alto, None, ancho=0.10)
            else:
                nivel_triple = 'Alto' if prediction == 1 else 'Bajo'

            # Save to session_state
            st.session_state.resultados['prob_alto'] = prob_alto
            st.session_state.resultados['nivel_triple'] = nivel_triple
            st.session_state.resultados['model'] = model
            st.session_state.resultados['X_for_model'] = X_for_model
            st.session_state.resultados['modelo_usado'] = model_name
            st.session_state.resultados['tiene_genetica'] = tiene_genetica
            st.session_state.resultados['prediccion_calculada'] = True

            _mostrar_resultado_riesgo(nivel_triple, prob_alto, modo_label)
            _mostrar_explicacion_modelo(modo_label)
            mostrar_shap_analysis(model, X_for_model, genero)
            
        except FileNotFoundError:
            st.warning(f"Modelo no encontrado: {model_path}")
        except Exception as e:
            st.error(f"Error en la predicción: {str(e)}")

    elif not calcular_clicked and st.session_state.resultados.get('prediccion_calculada'):
        prob_alto = st.session_state.resultados.get('prob_alto')
        nivel_triple = st.session_state.resultados.get('nivel_triple', 'N/A')
        cached_genetica = st.session_state.resultados.get('tiene_genetica', False)
        modo_label = "Extendido (22 features)" if cached_genetica else "Estándar (13 features)"

        _mostrar_resultado_riesgo(nivel_triple, prob_alto, modo_label)
        st.caption("Resultado del cálculo anterior. Pulse el botón para recalcular con nuevos parámetros.")
        _mostrar_explicacion_modelo(modo_label)

        cached_model = st.session_state.resultados.get('model')
        cached_X = st.session_state.resultados.get('X_for_model')
        if cached_model is not None and cached_X is not None:
            genero = registro.get('genero') if registro else None
            mostrar_shap_analysis(cached_model, cached_X, genero)

    elif not calcular_clicked:
        st.markdown('<div class="anxrisk-note"><p>Configure las opciones y pulse el botón para calcular la predicción de riesgo.</p></div>', unsafe_allow_html=True)
    
    # ── EXPORT BUTTON (only after prediction is calculated) ──
    if st.session_state.resultados.get('prediccion_calculada'):
        st.markdown("---")
        st.markdown("""
        <div class="anxrisk-section-header">
            <h2>Descargar Reporte</h2>
        </div>
        """, unsafe_allow_html=True)

        # Build filename from patient name
        demo_data_fn = st.session_state.resultados.get('datos_demograficos') or st.session_state.get('datos_demograficos')
        nombre_archivo = "paciente"
        if demo_data_fn and demo_data_fn.get('nombre'):
            import re as _re
            nombre_archivo = demo_data_fn['nombre'].strip()
            nombre_archivo = _re.sub(r'[^\w\s-]', '', nombre_archivo)
            nombre_archivo = _re.sub(r'\s+', '_', nombre_archivo)
        pdf_filename = f"{nombre_archivo}_resultadoansiedad.pdf"

        col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
        with col_dl2:
            try:
                pdf_bytes = generar_pdf_resultados(st.session_state.resultados, registro, datos_profesional)
                st.download_button(
                    label="📄 Descargar Reporte PDF Completo",
                    data=pdf_bytes,
                    file_name=pdf_filename,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generando PDF: {str(e)}")

    # Clinical warning
    st.markdown("""
    <div class="anxrisk-clinical-warning">
        <strong>Nota importante:</strong> Esta herramienta proporciona un análisis preliminar basado en modelos
        de aprendizaje automático supervisado. Los resultados deben ser interpretados en el contexto clínico
        completo del paciente y utilizados como apoyo en la toma de decisiones.
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Volver a Ansiedad (ZSAS)", use_container_width=True):
            st.session_state.pagina_actual = 'Ansiedad (ZSAS)'
            st.rerun()
    with col3:
        if st.button("Nueva Evaluación", type="primary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.pagina_actual = 'Home'
            st.rerun()


def _mostrar_resultado_riesgo(nivel_triple, prob_alto, modo_label):
    """Muestra el resultado de riesgo con gauge semicircular tipo Illumina."""
    css_class = _risk_css_class(nivel_triple)
    prob_text = f"{prob_alto:.1%}" if prob_alto is not None else "N/A"
    prob_value = prob_alto if prob_alto is not None else 0.5

    # Needle rotation: 0% = -90deg (left), 100% = 90deg (right)
    needle_deg = -90 + (prob_value * 180)

    st.markdown(f"""
    <div class="anxrisk-result-header">
        <div class="anxrisk-result-level {css_class}">{nivel_triple.upper()}</div>
        <div class="anxrisk-result-prob">Probabilidad<strong>{prob_text}</strong></div>
        <div class="anxrisk-gauge-container">
            <div class="anxrisk-gauge">
                <div class="anxrisk-gauge-needle" style="transform: rotate({needle_deg}deg);"></div>
                <div class="anxrisk-gauge-center"></div>
            </div>
            <div class="anxrisk-gauge-labels">
                <span style="color: var(--success);">Bajo</span>
                <span style="color: var(--warning);">Moderado</span>
                <span style="color: var(--danger);">Alto</span>
            </div>
        </div>
        <div class="anxrisk-result-model">Modelo: {modo_label}</div>
    </div>
    """, unsafe_allow_html=True)


def _mostrar_explicacion_modelo(modo_label):
    """Muestra una sección explicativa sobre el modelo MLP y sus métricas."""
    st.markdown("""
    <div class="anxrisk-section-header">
        <h2>Metodología del Modelo Predictivo</h2>
    </div>
    """, unsafe_allow_html=True)

    col_modelo, col_roc = st.columns(2)

    with col_modelo:
        st.markdown("""
        <div class="anxrisk-card" style="border-top: 3px solid var(--primary);">
            <h4 style="color: var(--primary) !important;">🧠 Red Neuronal MLP</h4>
            <p style="font-size: 0.9375rem; line-height: 1.6; color: var(--text-secondary);">
                El modelo utilizado es una <b>Red Neuronal Artificial de tipo MLP</b> (Multi-Layer Perceptron),
                un algoritmo de aprendizaje supervisado que procesa las variables clínicas, demográficas y
                (opcionalmente) genéticas del paciente a través de una capa oculta de 100 neuronas con
                función de activación tangente hiperbólica (tanh).
            </p>
            <p style="font-size: 0.9375rem; line-height: 1.6; color: var(--text-secondary);">
                A diferencia de modelos lineales, la red neuronal MLP captura <b>relaciones no lineales complejas</b>
                entre los factores de riesgo, lo que permite identificar interacciones sutiles entre variables
                que podrían pasar desapercibidas con métodos estadísticos tradicionales. El entrenamiento se
                realiza mediante descenso de gradiente estocástico (SGD) con tasa de aprendizaje adaptativa.
            </p>
            <p style="font-size: 0.875rem; color: var(--text-muted); margin-top: 0.5rem;">
                <b>Modo actual:</b> """ + modo_label + """
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_roc:
        st.markdown("""
        <div class="anxrisk-card" style="border-top: 3px solid var(--accent);">
            <h4 style="color: var(--primary) !important;">📈 Curva ROC y Validación</h4>
            <p style="font-size: 0.9375rem; line-height: 1.6; color: var(--text-secondary);">
                La <b>Curva ROC</b> (Receiver Operating Characteristic) es la herramienta estándar para evaluar
                la capacidad discriminativa de un modelo clasificador. Representa la relación entre la
                <b>Sensibilidad</b> (tasa de verdaderos positivos) y <b>1 – Especificidad</b>
                (tasa de falsos positivos) en todos los umbrales posibles.
            </p>
            <p style="font-size: 0.9375rem; line-height: 1.6; color: var(--text-secondary);">
                El <b>AUC-ROC</b> (Área Bajo la Curva) resume esta capacidad en un solo valor entre 0 y 1.
                Un AUC de <b>0.5</b> equivale a clasificar al azar, mientras que un AUC cercano a <b>1.0</b>
                indica discriminación perfecta entre pacientes con y sin riesgo elevado de ansiedad.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Metrics table
    with st.expander("📊 Métricas de Rendimiento del Modelo", expanded=False):
        st.markdown("""
        | Métrica | Descripción | Interpretación |
        |---------|-------------|----------------|
        | **AUC-ROC** | Área bajo la curva ROC | Capacidad global de discriminación entre clases |
        | **Sensibilidad (Recall)** | Proporción de casos positivos correctamente detectados | ¿Cuántos pacientes de alto riesgo identifica? |
        | **Especificidad** | Proporción de casos negativos correctamente clasificados | ¿Cuántos pacientes sanos clasifica bien? |
        | **Precisión (PPV)** | Proporción de predicciones positivas que son correctas | De los que marca como riesgo, ¿cuántos realmente lo son? |
        | **F1-Score** | Media armónica de precisión y sensibilidad | Balance entre detectar riesgo y evitar falsas alarmas |
        | **Índice de Youden** | Sensibilidad + Especificidad – 1 | Punto de corte óptimo en la curva ROC |

        **Clasificación triclásica:** El modelo genera una probabilidad continua (0–1) que se clasifica en tres niveles
        mediante umbrales fijos: **Bajo** (< 0.30), **Moderado** (0.30 – 0.59), **Alto** (≥ 0.60).
        Estos umbrales priorizan la sensibilidad clínica para no dejar pasar casos de riesgo elevado.
        """)


def mostrar_shap_analysis(model, X, genero):
    """Muestra el análisis SHAP"""
    st.markdown("""
    <div class="anxrisk-section-header">
        <h2>Análisis de Interpretabilidad (SHAP)</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="anxrisk-note">
        <p><strong>SHAP (SHapley Additive exPlanations)</strong> explica cada predicción mostrando el impacto
        de cada característica. Las barras rojas indican factores que aumentan el riesgo; las verdes, factores
        que lo disminuyen.</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        import shap
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from sklearn.neural_network import MLPClassifier
        try:
            import lightgbm as lgb
            has_lgb = True
        except ImportError:
            has_lgb = False
        
        feature_names = list(X.columns)
        X_array = X.values
        
        if isinstance(model, MLPClassifier):
            background_data = np.random.choice([0, 1], size=(50, X.shape[1]), p=[0.7, 0.3])
        else:
            background_data = X_array
        
        if has_lgb and isinstance(model, lgb.LGBMClassifier):
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_array)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
        elif isinstance(model, MLPClassifier):
            explainer = shap.KernelExplainer(model.predict_proba, background_data, feature_names=feature_names)
            shap_values = explainer.shap_values(X_array)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
        else:
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
        
        n_features = X.shape[1]
        top_n = min(15, n_features) if n_features > 13 else 13
        st.markdown(f"#### Top {top_n} Características más Influyentes")
        top_indices = np.argsort(np.abs(shap_array[0]))[-top_n:][::-1]
        top_shap_values = shap_array[0][top_indices]
        top_feature_names = [feature_names[i] for i in top_indices]
        
        # SHAP chart with Illumina design system colors
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = ['#E53935' if val > 0 else '#00B4D8' for val in top_shap_values]
        ax.barh(range(len(top_shap_values)), top_shap_values, color=colors, alpha=0.88, edgecolor='#E2E8F0', linewidth=0.5)
        ax.set_yticks(range(len(top_shap_values)))
        ax.set_yticklabels(top_feature_names, fontsize=10, fontfamily='sans-serif', color='#334155')
        ax.set_xlabel('SHAP Value (Contribución al Riesgo)', fontsize=11, fontweight='600', color='#0033A0')
        ax.set_title('Impacto de Características en la Predicción', fontsize=13, fontweight='700', color='#0033A0', pad=16)
        ax.axvline(x=0, color='#0033A0', linestyle='-', linewidth=1.5, alpha=0.6)
        ax.grid(axis='x', alpha=0.12, linestyle='-', color='#94A3B8')
        ax.set_facecolor('#FAFBFC')
        fig.patch.set_facecolor('#FAFBFC')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#CBD5E1')
        ax.spines['bottom'].set_color('#CBD5E1')
        ax.tick_params(colors='#64748B')
        
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#E53935', alpha=0.88, label='Aumenta Riesgo'),
            Patch(facecolor='#00B4D8', alpha=0.88, label='Disminuye Riesgo')
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=9, framealpha=0.95,
                  edgecolor='#CBD5E1', facecolor='#FFFFFF')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # SHAP interpretation
        st.markdown("""
        <div class="anxrisk-note">
            <p><strong>Interpretación:</strong> Barras rojas (derecha) = factores que aumentaron el riesgo.
            Barras verdes (izquierda) = factores que disminuyeron el riesgo.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Explicación Detallada de los Factores")
        generar_interpretacion_shap(shap_array, feature_names, X, top_indices)
        
    except Exception as e:
        st.error(f"Error generando análisis SHAP: {str(e)}")


def generar_interpretacion_shap(shap_array, feature_names, X, top_indices):
    """Genera interpretación personalizada de SHAP"""
    
    for idx in top_indices:
        feature = feature_names[idx]
        shap_val = shap_array[0][idx]
        feature_val = X.iloc[0, idx]
        
        css_class = "anxrisk-shap-increase" if shap_val > 0 else "anxrisk-shap-decrease"
        efecto = "aumenta" if shap_val > 0 else "disminuye"
        arrow = "&#9650;" if shap_val > 0 else "&#9660;"
        border_color = "var(--danger)" if shap_val > 0 else "var(--success)"
        
        interpretacion = obtener_interpretacion_feature(feature, feature_val)
        
        st.markdown(f"""
        <div style="background: var(--surface); padding: 0.75rem 1rem; margin: 0.375rem 0; border-radius: 8px; border-left: 3px solid {border_color};">
            <strong class="{css_class}">{arrow} {feature}</strong>
            <p style="color: var(--text-primary); margin: 0.25rem 0; font-size: 1rem;">{interpretacion}</p>
            <p style="color: var(--text-secondary); margin: 0; font-size: 0.9375rem;">{efecto} riesgo (~{abs(shap_val):.3f} SHAP)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="anxrisk-clinical-warning">
        <strong>Resumen Clínico:</strong> El modelo considera principalmente la salud mental/física del paciente,
        factores genéticos y eventos vitales estresantes para determinar el riesgo de ansiedad.
    </div>
    """, unsafe_allow_html=True)


def obtener_interpretacion_feature(feature, feature_val):
    """Retorna interpretación clínica de una feature"""
    if feature == "EDAD24":
        return f"Grupo de edad {'> 24 años' if feature_val == 1 else '≤ 24 años'}"
    elif feature == "AEFGROUPS":
        return f"Nivel educativo {'superior (≥ 15 años)' if feature_val == 1 else 'básico/secundario (< 15 años)'}"
    elif "SF12F" in feature:
        cuartil = feature.split("_")[1]
        if feature_val == 1:
            descripciones = {"Q1": "salud física muy baja (cuartil 1)", "Q2": "salud física baja (cuartil 2)", "Q3": "salud física moderada (cuartil 3)", "Q4": "salud física buena (cuartil 4)"}
            return f"Paciente presenta {descripciones.get(cuartil, cuartil)}"
        return f"No pertenece a este nivel de salud física ({cuartil})"
    elif "SF12M" in feature:
        cuartil = feature.split("_")[1]
        if feature_val == 1:
            descripciones = {"Q1": "salud mental muy baja (cuartil 1)", "Q2": "salud mental baja (cuartil 2)", "Q3": "salud mental moderada (cuartil 3)", "Q4": "salud mental buena (cuartil 4)"}
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
            descripciones = {"0": "sin eventos vitales estresantes", "1": "1 evento vital estresante", "2": "2 o más eventos vitales estresantes"}
            return f"Paciente experimentó {descripciones.get(nivel, nivel)}"
        return f"No se encuentra en esta categoría de eventos vitales ({nivel})"
    return f"Valor de la característica: {feature_val}"


def generar_pdf_resultados(resultados, registro, datos_profesional=None):
    """Genera PDF completo con TODA la información del paciente, escalas, SHAP y datos del profesional."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch, cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, KeepTogether, HRFlowable
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')
        from io import BytesIO

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=40, bottomMargin=50)
        elements = []

        # Design system colors — Illumina palette
        COLOR_PRIMARY = colors.HexColor('#0033A0')
        COLOR_PRIMARY_LIGHT = colors.HexColor('#E8F0FE')
        COLOR_TEXT = colors.HexColor('#1A202C')
        COLOR_TEXT_SECONDARY = colors.HexColor('#64748B')
        COLOR_SURFACE = colors.HexColor('#F1F5F9')
        COLOR_BORDER = colors.HexColor('#CBD5E1')
        COLOR_SUCCESS = colors.HexColor('#00C853')
        COLOR_WARNING = colors.HexColor('#FF9800')
        COLOR_DANGER = colors.HexColor('#E53935')
        COLOR_WHITE = colors.white
        COLOR_GENETIC = colors.HexColor('#7B1FA2')
        COLOR_ACCENT = colors.HexColor('#00B4D8')

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=22, textColor=COLOR_PRIMARY, spaceAfter=4, alignment=TA_CENTER, fontName='Helvetica-Bold', leading=26)
        subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=10, textColor=COLOR_TEXT_SECONDARY, spaceAfter=6, alignment=TA_CENTER, fontName='Helvetica', leading=13)
        heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=13, textColor=COLOR_PRIMARY, spaceAfter=8, spaceBefore=14, fontName='Helvetica-Bold', leading=16)
        subheading_style = ParagraphStyle('SubHeading', parent=styles['Heading3'], fontSize=11, textColor=COLOR_TEXT, spaceAfter=6, spaceBefore=8, fontName='Helvetica-Bold', leading=14)
        normal_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=10, spaceAfter=6, textColor=COLOR_TEXT, alignment=TA_JUSTIFY, fontName='Helvetica', leading=13)
        small_style = ParagraphStyle('Small', parent=styles['Normal'], fontSize=9, textColor=COLOR_TEXT_SECONDARY, alignment=TA_LEFT, fontName='Helvetica', leading=11)
        center_style = ParagraphStyle('Center', parent=styles['Normal'], fontSize=10, textColor=COLOR_TEXT, alignment=TA_CENTER, fontName='Helvetica', leading=13)
        bold_style = ParagraphStyle('Bold', parent=styles['Normal'], fontSize=10, spaceAfter=4, textColor=COLOR_TEXT, fontName='Helvetica-Bold', leading=13)
        risk_high_style = ParagraphStyle('RiskHigh', parent=styles['Normal'], fontSize=14, textColor=COLOR_DANGER, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=4)
        risk_mod_style = ParagraphStyle('RiskMod', parent=styles['Normal'], fontSize=14, textColor=COLOR_WARNING, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=4)
        risk_low_style = ParagraphStyle('RiskLow', parent=styles['Normal'], fontSize=14, textColor=COLOR_SUCCESS, fontName='Helvetica-Bold', alignment=TA_CENTER, spaceAfter=4)

        table_style_base = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_WHITE),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -1), COLOR_WHITE),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_WHITE, COLOR_SURFACE]),
            ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ])

        fecha_actual = pd.Timestamp.now().strftime('%d/%m/%Y')
        hora_actual = pd.Timestamp.now().strftime('%H:%M')

        # ═══════════════════════════════════════════════════════
        # PORTADA
        # ═══════════════════════════════════════════════════════
        
        # Professional cover logo using ReportLab drawing
        try:
            from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Group
            from reportlab.graphics import renderPDF
            from reportlab.lib.colors import HexColor

            logo_w, logo_h = 100, 100
            d = Drawing(logo_w, logo_h)

            # Navy background with rounded appearance
            d.add(Rect(0, 0, logo_w, logo_h, fillColor=HexColor('#0033A0'), strokeColor=None, rx=18, ry=18))

            # "A" letter — stylized monogram
            d.add(String(50, 28, "A", fontSize=56, fontName='Helvetica-Bold',
                         fillColor=HexColor('#00B4D8'), textAnchor='middle'))

            # Thin horizontal line through the A (EEG pulse style)
            d.add(Line(12, 52, 25, 52, strokeColor=HexColor('#FFFFFF'), strokeWidth=1.8))
            d.add(Line(25, 52, 30, 62, strokeColor=HexColor('#FFFFFF'), strokeWidth=1.8))
            d.add(Line(30, 62, 35, 42, strokeColor=HexColor('#FFFFFF'), strokeWidth=1.8))
            d.add(Line(35, 42, 40, 58, strokeColor=HexColor('#FFFFFF'), strokeWidth=1.8))
            d.add(Line(40, 58, 45, 46, strokeColor=HexColor('#FFFFFF'), strokeWidth=1.8))
            d.add(Line(45, 46, 50, 56, strokeColor=HexColor('#FFFFFF'), strokeWidth=1.8))
            d.add(Line(50, 56, 55, 44, strokeColor=HexColor('#FFFFFF'), strokeWidth=1.8))
            d.add(Line(55, 44, 60, 60, strokeColor=HexColor('#FFFFFF'), strokeWidth=1.8))
            d.add(Line(60, 60, 65, 48, strokeColor=HexColor('#FFFFFF'), strokeWidth=1.8))
            d.add(Line(65, 48, 70, 52, strokeColor=HexColor('#FFFFFF'), strokeWidth=1.8))
            d.add(Line(70, 52, 88, 52, strokeColor=HexColor('#FFFFFF'), strokeWidth=1.8))

            # Small accent dots
            d.add(Circle(30, 62, 2, fillColor=HexColor('#00E5FF'), strokeColor=None))
            d.add(Circle(50, 56, 2, fillColor=HexColor('#00E5FF'), strokeColor=None))
            d.add(Circle(60, 60, 2, fillColor=HexColor('#00E5FF'), strokeColor=None))

            # Render drawing to image
            logo_buf = BytesIO()
            from reportlab.graphics import renderPM
            renderPM.drawToFile(d, logo_buf, fmt='PNG', dpi=150)
            logo_buf.seek(0)

            elements.append(Spacer(1, 0.6 * inch))
            elements.append(Image(logo_buf, width=1.2*inch, height=1.2*inch, hAlign='CENTER'))
            elements.append(Spacer(1, 0.2 * inch))
        except Exception:
            elements.append(Spacer(1, 0.8 * inch))
        elements.append(Paragraph("ANXRISK", title_style))
        elements.append(Paragraph("Sistema de Evaluación de Riesgo de Ansiedad", subtitle_style))
        elements.append(HRFlowable(width="60%", thickness=2, color=COLOR_PRIMARY, spaceAfter=20, spaceBefore=10))
        elements.append(Paragraph("REPORTE CLÍNICO DE EVALUACIÓN", ParagraphStyle('Cover', parent=styles['Heading2'], fontSize=16, textColor=COLOR_TEXT, alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=30)))

        # Info box: fecha, profesional
        demo_data = resultados.get('datos_demograficos') or st.session_state.get('datos_demograficos')
        nombre_paciente = demo_data.get('nombre', 'No especificado') if demo_data else 'No especificado'

        prof_nombre = datos_profesional.get('nombre', '') if datos_profesional else ''
        prof_cargo = datos_profesional.get('cargo', '') if datos_profesional else ''
        prof_institucion = datos_profesional.get('institucion', '') if datos_profesional else ''
        prof_registro = datos_profesional.get('registro_profesional', '') if datos_profesional else ''

        cover_data = [
            ['Campo', 'Información'],
            ['Fecha del reporte', f'{fecha_actual}  —  {hora_actual}'],
            ['Paciente', nombre_paciente],
        ]
        if prof_nombre:
            cover_data.append(['Profesional evaluador', prof_nombre])
        if prof_cargo:
            cover_data.append(['Cargo / Especialidad', prof_cargo])
        if prof_institucion:
            cover_data.append(['Institución', prof_institucion])
        if prof_registro:
            cover_data.append(['Registro profesional', prof_registro])

        cover_table = Table(cover_data, colWidths=[170, 320])
        cover_table.setStyle(table_style_base)
        elements.append(cover_table)

        elements.append(Spacer(1, 0.5 * inch))
        elements.append(Paragraph(
            "Este reporte ha sido generado automáticamente por ANXRISK como apoyo a la decisión clínica. "
            "Los resultados deben ser interpretados por un profesional de la salud en el contexto clínico completo del paciente.",
            ParagraphStyle('Disclaimer', parent=normal_style, fontSize=9, textColor=COLOR_TEXT_SECONDARY, alignment=TA_CENTER)
        ))

        elements.append(PageBreak())

        # ═══════════════════════════════════════════════════════
        # 1. DATOS DEMOGRÁFICOS
        # ═══════════════════════════════════════════════════════
        elements.append(Paragraph("1. Datos Demográficos del Paciente", heading_style))
        elements.append(Paragraph(
            "Los datos demográficos proporcionan contexto clínico fundamental. La edad y el nivel educativo "
            "son variables predictoras en el modelo: pacientes jóvenes (≤ 24 años) y con menor nivel educativo "
            "presentan mayor vulnerabilidad según la evidencia epidemiológica.",
            normal_style
        ))

        if demo_data:
            if isinstance(demo_data.get('genero'), int):
                genero_txt = "Masculino" if demo_data['genero'] == 0 else "Femenino"
            else:
                genero_txt = demo_data.get('genero', 'No especificado')

            grupo_edad_txt = "> 24 años" if demo_data.get('grupo_edad', 0) == 1 else "≤ 24 años"
            edu_bin_txt = "Superior (≥ 15 años)" if demo_data.get('educacion_binaria', 0) == 1 else "Básico/Secundario (< 15 años)"

            demo_table_data = [
                ['Variable', 'Valor', 'Codificación modelo'],
                ['Nombre completo', Paragraph(nombre_paciente, normal_style), '—'],
                ['Edad', f"{demo_data.get('edad', '-')} años", Paragraph(f"EDAD24 = {demo_data.get('grupo_edad', '-')} ({grupo_edad_txt})", small_style)],
                ['Género', genero_txt, f"GENERO = {demo_data.get('genero', '-')}"],
                ['Años de educación', f"{demo_data.get('años_educacion', '-')} años", Paragraph(f"AEFGROUPS = {demo_data.get('educacion_binaria', '-')} ({edu_bin_txt})", small_style)],
            ]
            demo_table = Table(demo_table_data, colWidths=[110, 130, 250])
            demo_table.setStyle(table_style_base)
            elements.append(demo_table)
        else:
            elements.append(Paragraph("Datos demográficos no disponibles.", normal_style))

        elements.append(Spacer(1, 0.3 * inch))

        # ═══════════════════════════════════════════════════════
        # 2. EVENTOS VITALES (LTE-12)
        # ═══════════════════════════════════════════════════════
        elements.append(Paragraph("2. Eventos Vitales Estresantes (LTE-12)", heading_style))
        elements.append(Paragraph(
            "La Lista de Experiencias Amenazantes (LTE-12) identifica eventos vitales estresantes experimentados "
            "en los últimos 12 meses. Estos eventos actúan como factores precipitantes o agravantes de trastornos "
            "de ansiedad. A mayor número de eventos, mayor carga alostática y vulnerabilidad emocional.",
            normal_style
        ))
        try:
            eventos_data = resultados.get('eventos_vitales', {})
            total_eventos = eventos_data.get('total', 0)
            from src.utils.calculos import transformar_lte12_a_clasificacion
            lte12_clasif = transformar_lte12_a_clasificacion(total_eventos)
            clasif_labels = {0: "Sin eventos significativos", 1: "1 evento significativo", 2: "2 o más eventos significativos"}

            lte_table_data = [
                ['Indicador', 'Valor'],
                ['Total de eventos estresantes', str(total_eventos)],
                ['Clasificación LTE-12', clasif_labels.get(lte12_clasif, str(lte12_clasif))],
            ]

            # Interpretación clínica
            if total_eventos == 0:
                lte_interp = "El paciente no reporta eventos vitales estresantes recientes. Esto sugiere un entorno relativamente estable."
            elif total_eventos == 1:
                lte_interp = "El paciente reporta 1 evento estresante. Se recomienda explorar el impacto subjetivo de este evento durante la entrevista clínica."
            else:
                lte_interp = f"El paciente reporta {total_eventos} eventos estresantes, lo cual indica una carga significativa de estrés. Esto puede ser un factor de riesgo importante para el desarrollo o agravamiento de ansiedad."
            lte_table_data.append([Paragraph('<b>Interpretación</b>', small_style), Paragraph(lte_interp, small_style)])

            lte_table = Table(lte_table_data, colWidths=[160, 330])
            lte_table.setStyle(table_style_base)
            elements.append(lte_table)

            # Individual events as a separate list (not crammed into a table cell)
            respuestas = eventos_data.get('respuestas', [])
            if respuestas and isinstance(respuestas, list):
                preguntas_lte = [
                    "Enfermedad, lesión o agresión propia",
                    "Enfermedad, lesión o agresión de familiar cercano",
                    "Muerte de padres, hijos o pareja",
                    "Muerte de amigo cercano u otro familiar",
                    "Separación matrimonial por problemas",
                    "Ruptura de relación estable",
                    "Problema grave con amigo, vecino o familiar",
                    "Desempleo prolongado (más de un mes)",
                    "Despido laboral",
                    "Crisis económica grave",
                    "Problemas legales o con la policía",
                    "Robo o pérdida de objetos de valor",
                ]
                eventos_si = [preguntas_lte[i] for i, v in enumerate(respuestas) if v == 1 and i < len(preguntas_lte)]
                eventos_no = [preguntas_lte[i] for i, v in enumerate(respuestas) if v == 0 and i < len(preguntas_lte)]

                if eventos_si:
                    elements.append(Spacer(1, 0.15 * inch))
                    elements.append(Paragraph("Eventos reportados por el paciente:", bold_style))
                    for ev in eventos_si:
                        elements.append(Paragraph(f"  •  <font color='#DC2626'>Sí</font> — {ev}", normal_style))

                if eventos_no:
                    elements.append(Spacer(1, 0.1 * inch))
                    elements.append(Paragraph("Eventos no reportados:", small_style))
                    for ev in eventos_no:
                        elements.append(Paragraph(f"  •  No — {ev}", small_style))
        except Exception:
            elements.append(Paragraph("Datos de eventos vitales no disponibles.", normal_style))

        elements.append(Spacer(1, 0.3 * inch))

        # ═══════════════════════════════════════════════════════
        # 3. SALUD FÍSICA Y MENTAL (SF-12)
        # ═══════════════════════════════════════════════════════
        elements.append(Paragraph("3. Calidad de Vida Relacionada con Salud (SF-12)", heading_style))
        elements.append(Paragraph(
            "El SF-12 evalúa la calidad de vida percibida en dos componentes. El Componente Físico (PCS) mide "
            "limitaciones físicas, dolor y salud general. El Componente Mental (MCS) mide vitalidad, función social "
            "y salud emocional. Puntajes más bajos (cuartiles Q1-Q2) indican peor percepción de salud y se asocian "
            "a mayor riesgo de trastornos de ansiedad.",
            normal_style
        ))
        try:
            sf12 = resultados.get('sf12', {})
            pf = sf12.get('puntaje_fisico')
            pm = sf12.get('puntaje_mental')
            qf = sf12.get('cuartil_fisica')
            qm = sf12.get('cuartil_mental')

            sf12_table_data = [['Componente', 'Puntaje', 'Cuartil', 'Interpretación']]

            if pf is not None:
                sf12_table_data.append([
                    'Físico (PCS)',
                    f"{float(pf):.1f}",
                    f"Q{qf}" if qf else "—",
                    Paragraph(_obtener_mensaje_cuartil_fisica(qf), small_style) if qf else "—"
                ])
            if pm is not None:
                sf12_table_data.append([
                    'Mental (MCS)',
                    f"{float(pm):.1f}",
                    f"Q{qm}" if qm else "—",
                    Paragraph(_obtener_mensaje_cuartil_mental(qm), small_style) if qm else "—"
                ])

            if len(sf12_table_data) > 1:
                sf12_table = Table(sf12_table_data, colWidths=[80, 60, 50, 300])
                sf12_table.setStyle(table_style_base)
                elements.append(sf12_table)
            else:
                elements.append(Paragraph("Datos SF-12 no disponibles.", normal_style))
        except Exception:
            elements.append(Paragraph("Datos SF-12 no disponibles.", normal_style))

        elements.append(Spacer(1, 0.3 * inch))

        # ═══════════════════════════════════════════════════════
        # 4. ANSIEDAD HADS
        # ═══════════════════════════════════════════════════════
        elements.append(Paragraph("4. Escala Hospitalaria de Ansiedad y Depresión (HADS)", heading_style))
        elements.append(Paragraph(
            "La HADS es un instrumento de cribado validado para detectar ansiedad en contextos clínicos. "
            "Puntajes de 0-7 se consideran normales, 8-10 indican un caso dudoso o ansiedad leve, y ≥ 11 "
            "señalan ansiedad clínicamente significativa que amerita intervención.",
            normal_style
        ))
        try:
            hads = resultados.get('hads', {})
            hads_puntaje = hads.get('puntaje', '-')
            hads_nivel = hads.get('nivel', '-')

            hads_table_data = [
                ['Indicador', 'Valor'],
                ['Puntaje total (subescala ansiedad)', str(hads_puntaje)],
                ['Clasificación', str(hads_nivel)],
            ]

            # Interpretation
            try:
                p = int(hads_puntaje)
                if p <= 7:
                    interp = "Sin ansiedad clínica significativa (0-7). El paciente no presenta sintomatología ansiosa que requiera intervención inmediata."
                elif p <= 10:
                    interp = "Ansiedad leve / caso dudoso (8-10). Se recomienda seguimiento y reevaluación en consultas posteriores."
                else:
                    interp = "Ansiedad clínicamente significativa (≥ 11). Se sugiere intervención terapéutica y/o farmacológica según criterio clínico."
                hads_table_data.append(['Interpretación', Paragraph(interp, small_style)])
            except (ValueError, TypeError):
                pass

            hads_table = Table(hads_table_data, colWidths=[200, 290])
            hads_table.setStyle(table_style_base)
            elements.append(hads_table)
        except Exception:
            elements.append(Paragraph("Datos HADS no disponibles.", normal_style))

        elements.append(Spacer(1, 0.3 * inch))

        # ═══════════════════════════════════════════════════════
        # 5. ANSIEDAD ZSAS (ZUNG)
        # ═══════════════════════════════════════════════════════
        elements.append(Paragraph("5. Escala de Ansiedad de Zung (ZSAS)", heading_style))
        elements.append(Paragraph(
            "La Escala de Automedición de Ansiedad de Zung (ZSAS) evalúa síntomas somáticos y cognitivos de ansiedad. "
            "Un puntaje bruto < 36 indica ausencia de ansiedad significativa, 36-47 ansiedad leve a moderada, "
            "48-59 ansiedad moderada a severa, y ≥ 60 ansiedad severa.",
            normal_style
        ))
        try:
            zsas = resultados.get('zsas', {})
            zsas_total = zsas.get('total', '-')
            zsas_nivel = zsas.get('nivel', '-')

            zsas_table_data = [
                ['Indicador', 'Valor'],
                ['Puntaje bruto', str(zsas_total)],
                ['Clasificación', str(zsas_nivel)],
            ]

            try:
                t = int(zsas_total)
                if t < 36:
                    interp = "Sin ansiedad significativa (< 36). No se evidencian síntomas de ansiedad clínicamente relevantes."
                elif t <= 47:
                    interp = "Ansiedad leve a moderada (36-47). Se sugiere monitoreo y estrategias de manejo del estrés."
                elif t <= 59:
                    interp = "Ansiedad moderada a severa (48-59). Se recomienda evaluación clínica detallada e intervención terapéutica."
                else:
                    interp = "Ansiedad severa (≥ 60). Se indica intervención inmediata con abordaje multimodal (psicoterapia + evaluación farmacológica)."
                zsas_table_data.append(['Interpretación', Paragraph(interp, small_style)])
            except (ValueError, TypeError):
                pass

            zsas_table = Table(zsas_table_data, colWidths=[200, 290])
            zsas_table.setStyle(table_style_base)
            elements.append(zsas_table)
        except Exception:
            elements.append(Paragraph("Datos ZSAS no disponibles.", normal_style))

        elements.append(Spacer(1, 0.3 * inch))

        # ═══════════════════════════════════════════════════════
        # 6. PERFIL GENÉTICO
        # ═══════════════════════════════════════════════════════
        elements.append(Paragraph("6. Perfil Genético", heading_style))
        elements.append(Paragraph(
            "El panel genético evalúa tres polimorfismos de nucleótido único (SNPs) asociados a la vulnerabilidad "
            "a trastornos de ansiedad: PRKCA (regulación de la respuesta al estrés), TCF4 (transcripción neuronal) "
            "y CDH20 (conectividad sináptica). La inclusión de estos marcadores refina la predicción del modelo.",
            normal_style
        ))
        gen = resultados.get('datos_geneticos')
        if gen:
            gen_table_data = [
                ['Gen / Polimorfismo', 'Genotipo', 'Función'],
                ['PRKCA (rs2244497)', gen.get('prkca', '-'), 'Regulación de la respuesta al estrés'],
                ['TCF4 (rs1452789)', gen.get('tcf4', '-'), 'Factor de transcripción neuronal'],
                ['CDH20 (rs7243203)', gen.get('cdh20', '-'), 'Conectividad neuronal (cadherinas)'],
            ]
            gen_table = Table(gen_table_data, colWidths=[150, 80, 260])
            gen_table.setStyle(table_style_base)
            elements.append(gen_table)
        else:
            elements.append(Paragraph("Evaluación realizada sin datos genéticos (modo estándar, 13 features).", normal_style))

        elements.append(PageBreak())

        # ═══════════════════════════════════════════════════════
        # 7. METODOLOGÍA DEL MODELO Y PREDICCIÓN DE RIESGO
        # ═══════════════════════════════════════════════════════
        elements.append(Paragraph("7. Metodología del Modelo Predictivo y Resultado", heading_style))

        # 7a. Model explanation
        elements.append(Paragraph("7.1 Red Neuronal MLP (Perceptrón Multicapa)", subheading_style))
        elements.append(Paragraph(
            "ANXRISK emplea una <b>Red Neuronal Artificial de tipo MLP</b> (Multi-Layer Perceptron), un algoritmo "
            "de aprendizaje automático supervisado que pertenece a la familia de redes neuronales artificiales. "
            "El modelo procesa las variables clínicas, demográficas y (opcionalmente) genéticas del paciente "
            "a través de una capa oculta de 100 neuronas con función de activación tangente hiperbólica (tanh).",
            normal_style
        ))
        elements.append(Spacer(1, 0.08 * inch))
        elements.append(Paragraph(
            "<b>¿Cómo funciona?</b> La capa de entrada recibe las variables clínicas codificadas (edad, educación, "
            "escalas psicométricas, eventos vitales, y opcionalmente marcadores genéticos). La capa oculta "
            "aplica transformaciones no lineales mediante la función tanh, aprendiendo representaciones abstractas "
            "de los patrones de riesgo. Finalmente, la capa de salida genera una <b>probabilidad continua</b> "
            "(0 a 1) que estima el riesgo de ansiedad patológica. El entrenamiento se realiza mediante descenso "
            "de gradiente estocástico (SGD) con tasa de aprendizaje adaptativa.",
            normal_style
        ))
        elements.append(Spacer(1, 0.08 * inch))
        elements.append(Paragraph(
            "A diferencia de modelos lineales (como la regresión logística), la red neuronal MLP captura "
            "<b>relaciones no lineales complejas</b> e interacciones entre variables que podrían pasar "
            "desapercibidas con métodos estadísticos convencionales. Esto permite una estimación más precisa "
            "del riesgo individual de cada paciente.",
            normal_style
        ))

        # Model architecture table
        elements.append(Spacer(1, 0.12 * inch))
        modelo_usado = resultados.get('modelo_usado', 'No especificado')
        tiene_genetica = resultados.get('tiene_genetica', False)
        modo_txt = 'Extendido (22 features)' if tiene_genetica else 'Estándar (13 features)'

        arch_table_data = [
            ['Componente', 'Descripción'],
            ['Tipo de modelo', 'MLP (Multi-Layer Perceptron) — Red Neuronal Multicapa'],
            ['Variables de entrada', modo_txt],
            ['Capa oculta', '1 capa de 100 neuronas con función de activación tanh'],
            ['Capa de salida', 'Sigmoide — probabilidad de riesgo alto (0 a 1)'],
            ['Optimización', 'Backpropagation con SGD (Stochastic Gradient Descent), learning rate adaptativo'],
            ['Regularización', 'Penalización L2 (alpha=0.001), max_iter=2000'],
        ]
        arch_table = Table(arch_table_data, colWidths=[140, 350])
        arch_table.setStyle(table_style_base)
        elements.append(arch_table)

        # 7b. ROC Curve and metrics explanation
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph("7.2 Validación del Modelo: Curva ROC y Métricas Clave", subheading_style))
        elements.append(Paragraph(
            "La validación del modelo se realiza mediante la <b>Curva ROC</b> (Receiver Operating Characteristic), "
            "el estándar de referencia en la evaluación de modelos de clasificación en ciencias de la salud. "
            "La curva ROC representa gráficamente la relación entre la <b>Sensibilidad</b> (tasa de verdaderos "
            "positivos: pacientes de alto riesgo correctamente identificados) y <b>1 – Especificidad</b> "
            "(tasa de falsos positivos: pacientes sanos incorrectamente clasificados como riesgo) en todos "
            "los umbrales de decisión posibles.",
            normal_style
        ))
        elements.append(Spacer(1, 0.08 * inch))
        elements.append(Paragraph(
            "El <b>AUC-ROC</b> (Área Bajo la Curva ROC) resume la capacidad discriminativa del modelo en un "
            "valor entre 0 y 1. Un AUC de 0.5 equivale a una clasificación al azar (sin capacidad predictiva), "
            "mientras que un AUC cercano a 1.0 indica una discriminación perfecta entre pacientes con y sin "
            "riesgo elevado de ansiedad. Valores superiores a 0.80 se consideran <b>excelentes</b> en contextos clínicos.",
            normal_style
        ))

        # Metrics explanation table
        elements.append(Spacer(1, 0.12 * inch))
        metrics_table_data = [
            ['Métrica', 'Definición', 'Relevancia Clínica'],
            ['AUC-ROC', Paragraph('Área bajo la curva ROC (0–1)', small_style),
             Paragraph('Capacidad global del modelo para distinguir entre pacientes con riesgo alto y bajo', small_style)],
            ['Sensibilidad\n(Recall)', Paragraph('Proporción de pacientes de alto riesgo correctamente detectados', small_style),
             Paragraph('Prioridad clínica: minimizar pacientes de riesgo no detectados', small_style)],
            ['Especificidad', Paragraph('Proporción de pacientes sanos correctamente clasificados', small_style),
             Paragraph('Reducir falsas alarmas que generen intervenciones innecesarias', small_style)],
            ['Precisión\n(PPV)', Paragraph('De los clasificados como riesgo, cuántos realmente lo son', small_style),
             Paragraph('Confianza en la predicción positiva del modelo', small_style)],
            ['F1-Score', Paragraph('Media armónica de precisión y sensibilidad', small_style),
             Paragraph('Balance entre detectar riesgo y evitar falsos positivos', small_style)],
            ['Índice de\nYouden', Paragraph('Sensibilidad + Especificidad – 1', small_style),
             Paragraph('Determina el punto de corte óptimo en la curva ROC', small_style)],
        ]
        metrics_table = Table(metrics_table_data, colWidths=[75, 175, 240])
        metrics_table.setStyle(table_style_base)
        elements.append(metrics_table)

        # 7c. Classification thresholds
        elements.append(Spacer(1, 0.15 * inch))
        elements.append(Paragraph("7.3 Clasificación Triclásica del Riesgo", subheading_style))
        elements.append(Paragraph(
            "El modelo genera una probabilidad continua (0 a 1) que se clasifica en tres niveles de riesgo "
            "mediante umbrales clínicamente definidos. Estos umbrales fueron establecidos priorizando la "
            "<b>sensibilidad clínica</b> para minimizar el riesgo de no detectar pacientes con ansiedad patológica:",
            normal_style
        ))
        elements.append(Spacer(1, 0.08 * inch))

        thresh_table_data = [
            ['Nivel', 'Rango de Probabilidad', 'Interpretación Clínica'],
            ['BAJO', '< 0.30 (< 30%)', Paragraph('Perfil de bajo riesgo. Mantener estrategias preventivas y reevaluar ante nuevos factores de riesgo.', small_style)],
            ['MODERADO', '0.30 – 0.59 (30–59%)', Paragraph('Zona de incertidumbre. Se recomienda monitoreo activo, psicoeducación y reevaluación en 4–6 semanas.', small_style)],
            ['ALTO', '≥ 0.60 (≥ 60%)', Paragraph('Riesgo elevado. Se sugiere evaluación clínica completa, intervención psicoterapéutica y/o farmacológica.', small_style)],
        ]
        thresh_table = Table(thresh_table_data, colWidths=[65, 130, 295])
        thresh_table.setStyle(table_style_base)
        elements.append(thresh_table)

        elements.append(PageBreak())

        # 7d. Prediction result
        elements.append(Paragraph("7.4 Resultado de la Predicción", subheading_style))

        prob_alto = resultados.get('prob_alto')
        nivel_triple = resultados.get('nivel_triple', 'No calculado')

        if prob_alto is not None:
            # Risk level with color
            risk_style = risk_high_style if nivel_triple == 'Alto' else risk_mod_style if nivel_triple == 'Moderado' else risk_low_style
            elements.append(Paragraph(f"NIVEL DE RIESGO: {nivel_triple.upper()}", risk_style))
            elements.append(Spacer(1, 0.1 * inch))

            pred_table_data = [
                ['Parámetro', 'Valor'],
                ['Probabilidad de alto riesgo', f"{prob_alto:.1%}"],
                ['Clasificación', nivel_triple],
                ['Modelo utilizado', modelo_usado],
                ['Modo', 'Extendido (22 features)' if tiene_genetica else 'Estándar (13 features)'],
            ]
            pred_table = Table(pred_table_data, colWidths=[200, 290])
            pred_table.setStyle(table_style_base)
            elements.append(pred_table)

            # Clinical recommendation based on risk level
            elements.append(Spacer(1, 0.15 * inch))
            if nivel_triple == 'Alto':
                rec = (
                    "<b>Recomendación clínica:</b> El perfil del paciente sugiere un riesgo elevado de ansiedad patológica. "
                    "Se recomienda: (1) evaluación clínica completa con entrevista estructurada, "
                    "(2) considerar intervención psicoterapéutica (TCC u otro enfoque basado en evidencia), "
                    "(3) valorar la necesidad de tratamiento farmacológico, y "
                    "(4) programar seguimiento a corto plazo."
                )
            elif nivel_triple == 'Moderado':
                rec = (
                    "<b>Recomendación clínica:</b> El resultado se encuentra en zona de incertidumbre. "
                    "Se sugiere: (1) monitoreo activo con reevaluación en 4-6 semanas, "
                    "(2) psicoeducación sobre manejo del estrés y técnicas de relajación, "
                    "(3) considerar factores contextuales no capturados por el modelo."
                )
            else:
                rec = (
                    "<b>Recomendación clínica:</b> El perfil actual no sugiere riesgo elevado de ansiedad. "
                    "Se recomienda mantener estrategias preventivas, promover hábitos de vida saludable "
                    "y reevaluar si aparecen nuevos factores de riesgo o sintomatología."
                )
            elements.append(Paragraph(rec, ParagraphStyle('Rec', parent=normal_style, fontSize=9, textColor=COLOR_TEXT_SECONDARY, backColor=COLOR_SURFACE, borderPadding=8)))
        else:
            elements.append(Paragraph("La predicción de riesgo no fue calculada durante esta sesión.", normal_style))

        elements.append(Spacer(1, 0.3 * inch))

        # ═══════════════════════════════════════════════════════
        # 8. ANÁLISIS SHAP
        # ═══════════════════════════════════════════════════════
        elements.append(Paragraph("8. Análisis de Interpretabilidad (SHAP)", heading_style))
        elements.append(Paragraph(
            "SHAP (SHapley Additive exPlanations) es un método de interpretabilidad basado en la teoría de juegos "
            "que cuantifica la contribución individual de cada variable a la predicción del modelo. "
            "Valores positivos (rojos) indican factores que <b>aumentan</b> el riesgo de ansiedad; "
            "valores negativos (verdes) indican factores <b>protectores</b> que disminuyen el riesgo. "
            "Esto permite al clínico identificar las áreas de intervención prioritarias para cada paciente.",
            normal_style
        ))

        shap_generated = False
        try:
            import shap
            from sklearn.neural_network import MLPClassifier
            model = resultados.get('model')
            X_for_model = resultados.get('X_for_model')

            if model is not None and X_for_model is not None:
                feature_names = list(X_for_model.columns)
                X_array = X_for_model.values

                if isinstance(model, MLPClassifier):
                    bg = np.random.choice([0, 1], size=(50, X_array.shape[1]), p=[0.7, 0.3])
                    explainer = shap.KernelExplainer(model.predict_proba, bg, feature_names=feature_names)
                else:
                    explainer = shap.KernelExplainer(model.predict_proba, X_array, feature_names=feature_names)

                sv = explainer.shap_values(X_array)
                if isinstance(sv, list):
                    sv = sv[1]
                sa = sv.values if hasattr(sv, 'values') else np.array(sv)
                if sa.ndim == 1:
                    sa = sa.reshape(1, -1)
                elif sa.ndim == 3:
                    sa = sa[:, :, -1]

                n_features = X_for_model.shape[1]
                top_n = min(15, n_features)
                ti = np.argsort(np.abs(sa[0]))[-top_n:][::-1]
                tsv = sa[0][ti]
                tfn = [feature_names[i] for i in ti]

                # Generate SHAP chart
                fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=120)
                clrs = ['#DC2626' if v > 0 else '#059669' for v in tsv]
                bars = ax.barh(range(len(tsv)), tsv, color=clrs, alpha=0.85, edgecolor='#D4D0CC', linewidth=0.5)
                ax.set_yticks(range(len(tsv)))
                ax.set_yticklabels(tfn, fontsize=9, fontfamily='sans-serif')
                ax.set_xlabel('SHAP Value (Contribución al Riesgo)', fontsize=10, fontweight='600', color='#2D2D2D')
                ax.set_title('Impacto de Características en la Predicción Individual', fontsize=12, fontweight='600', color='#2D2D2D', pad=14)
                ax.axvline(x=0, color='#2D2D2D', linestyle='-', linewidth=1.5)
                ax.grid(axis='x', alpha=0.15, linestyle='-', color='#D4D0CC')
                ax.set_facecolor('#FAFAFA')
                fig.patch.set_facecolor('#FFFFFF')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color('#D4D0CC')
                ax.spines['bottom'].set_color('#D4D0CC')
                ax.tick_params(colors='#6B6B6B')
                ax.invert_yaxis()

                from matplotlib.patches import Patch
                legend_elements = [
                    Patch(facecolor='#DC2626', alpha=0.85, label='Aumenta Riesgo'),
                    Patch(facecolor='#059669', alpha=0.85, label='Disminuye Riesgo')
                ]
                ax.legend(handles=legend_elements, loc='lower right', fontsize=9, framealpha=0.95)
                plt.tight_layout()

                img_buffer = BytesIO()
                plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=120)
                img_buffer.seek(0)
                plt.close(fig)

                elements.append(Spacer(1, 0.15 * inch))
                elements.append(Image(img_buffer, width=6 * inch, height=4.2 * inch))
                elements.append(Spacer(1, 0.2 * inch))

                # SHAP values table
                elements.append(Paragraph("Detalle de Contribuciones SHAP", subheading_style))
                shap_table_data = [['Característica', 'Valor SHAP', 'Efecto', 'Interpretación']]
                for idx_pos, idx in enumerate(ti):
                    feat = feature_names[idx]
                    val = sa[0][idx]
                    feat_val = X_for_model.iloc[0, idx]
                    efecto = 'Aumenta riesgo' if val > 0 else 'Disminuye riesgo'
                    interp = obtener_interpretacion_feature(feat, feat_val)
                    shap_table_data.append([feat, f"{val:.4f}", efecto, Paragraph(interp, small_style)])

                shap_table = Table(shap_table_data, colWidths=[85, 65, 85, 255])
                shap_ts = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARY),
                    ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_WHITE),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('BACKGROUND', (0, 1), (-1, -1), COLOR_WHITE),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [COLOR_WHITE, COLOR_SURFACE]),
                    ('GRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
                ])
                shap_table.setStyle(shap_ts)
                elements.append(shap_table)
                shap_generated = True

        except Exception as e:
            elements.append(Paragraph(f"No fue posible generar el análisis SHAP: {str(e)}", normal_style))

        if not shap_generated and prob_alto is None:
            elements.append(Paragraph("El análisis SHAP no está disponible porque la predicción no fue calculada.", normal_style))

        # ═══════════════════════════════════════════════════════
        # 9. RESUMEN CLÍNICO
        # ═══════════════════════════════════════════════════════
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(Paragraph("9. Resumen Clínico Integrado", heading_style))

        resumen_items = []
        if demo_data:
            resumen_items.append(f"Paciente de {demo_data.get('edad', '?')} años, género {'masculino' if demo_data.get('genero') == 0 else 'femenino' if demo_data.get('genero') == 1 else str(demo_data.get('genero', '?'))}.")
        try:
            ev_total = resultados.get('eventos_vitales', {}).get('total', 0)
            resumen_items.append(f"Reporta {ev_total} evento(s) vital(es) estresante(s) en los últimos 12 meses.")
        except Exception:
            pass
        try:
            sf12d = resultados.get('sf12', {})
            if sf12d.get('puntaje_fisico') is not None:
                resumen_items.append(f"Componente físico SF-12: {float(sf12d['puntaje_fisico']):.1f} (Q{sf12d.get('cuartil_fisica', '?')}). Componente mental SF-12: {float(sf12d.get('puntaje_mental', 0)):.1f} (Q{sf12d.get('cuartil_mental', '?')}).")
        except Exception:
            pass
        try:
            hads_d = resultados.get('hads', {})
            resumen_items.append(f"HADS ansiedad: {hads_d.get('puntaje', '?')} puntos — {hads_d.get('nivel', '?')}.")
        except Exception:
            pass
        try:
            zsas_d = resultados.get('zsas', {})
            resumen_items.append(f"ZSAS: {zsas_d.get('total', '?')} puntos — {zsas_d.get('nivel', '?')}.")
        except Exception:
            pass
        if prob_alto is not None:
            resumen_items.append(f"Predicción de riesgo: {nivel_triple} (probabilidad {prob_alto:.1%}).")

        for item in resumen_items:
            elements.append(Paragraph(f"• {item}", normal_style))

        # ═══════════════════════════════════════════════════════
        # NOTA CLÍNICA + FIRMA
        # ═══════════════════════════════════════════════════════
        elements.append(Spacer(1, 0.4 * inch))
        elements.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER, spaceAfter=12))

        elements.append(Paragraph(
            "<b>Nota importante:</b> Este reporte es generado como herramienta de apoyo a la decisión clínica. "
            "Los resultados del modelo predictivo deben complementarse con la entrevista clínica, la observación directa "
            "y el juicio profesional. No constituye un diagnóstico definitivo.",
            ParagraphStyle('Warning', parent=normal_style, fontSize=9, textColor=COLOR_TEXT_SECONDARY, spaceAfter=20)
        ))

        # Signature block
        elements.append(Spacer(1, 0.6 * inch))
        elements.append(Paragraph("FIRMA DEL PROFESIONAL EVALUADOR", ParagraphStyle('FirmaTitle', parent=bold_style, fontSize=10, alignment=TA_CENTER, textColor=COLOR_TEXT_SECONDARY, spaceAfter=4)))
        elements.append(Spacer(1, 0.8 * inch))  # Space for handwritten signature

        firma_data = [
            ['_' * 45, '_' * 30],
            [
                Paragraph(f"<b>{prof_nombre}</b>" if prof_nombre else "<b>Nombre y firma del profesional</b>", center_style),
                Paragraph(f"Fecha: {fecha_actual}", center_style)
            ],
        ]
        if prof_cargo:
            firma_data.append([Paragraph(prof_cargo, ParagraphStyle('FirmaCargo', parent=center_style, fontSize=9, textColor=COLOR_TEXT_SECONDARY)), ''])
        if prof_institucion:
            firma_data.append([Paragraph(prof_institucion, ParagraphStyle('FirmaInst', parent=center_style, fontSize=9, textColor=COLOR_TEXT_SECONDARY)), ''])
        if prof_registro:
            firma_data.append([Paragraph(f"Reg. Prof.: {prof_registro}", ParagraphStyle('FirmaReg', parent=center_style, fontSize=9, textColor=COLOR_TEXT_SECONDARY)), ''])

        firma_table = Table(firma_data, colWidths=[300, 190])
        firma_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(firma_table)

        # Footer
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=COLOR_BORDER, spaceAfter=8))
        elements.append(Paragraph(
            f"Generado por ANXRISK v1.0 — {fecha_actual} {hora_actual}",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=COLOR_TEXT_SECONDARY, alignment=TA_CENTER)
        ))

        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    except Exception as e:
        raise RuntimeError(f"Error generando PDF: {str(e)}")

