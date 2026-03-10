"""
Página de Resultados de la Evaluación
======================================
Flujo:
1. Tras ZSAS → se muestra resumen + pregunta de genética + botón "Generar Evaluación"
2. Al presionar el botón → se ejecuta predicción CatBoost + SHAP
3. Se muestran resultados, gráfico SHAP y botón de descarga PDF (sin HTML)
4. El PDF incluye portada, cuestionarios, predicción, SHAP y firma del profesional.
"""
import streamlit as st
from src.utils.dataframe_manager import obtener_registro_actual
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

# ─────────────────────────────────────────────────────────────────
# Helpers de cuartiles SF-12
# ─────────────────────────────────────────────────────────────────

def _obtener_mensaje_cuartil_fisica(cuartil):
    msgs = {
        1: "Salud Física Muy Baja (Q1)",
        2: "Salud Física Baja (Q2)",
        3: "Salud Física Moderada (Q3)",
        4: "Salud Física Excelente (Q4)",
    }
    return msgs.get(cuartil, "Información no disponible")


def _obtener_mensaje_cuartil_mental(cuartil):
    msgs = {
        1: "Salud Mental Muy Baja (Q1)",
        2: "Salud Mental Baja (Q2)",
        3: "Salud Mental Moderada (Q3)",
        4: "Salud Mental Excelente (Q4)",
    }
    return msgs.get(cuartil, "Información no disponible")


def _obtener_sf12f_cuartil_desde_registro(reg):
    from src.utils.calculos import transformar_sf12_fisica_a_cuartil
    if not reg:
        return transformar_sf12_fisica_a_cuartil(0)
    if reg.get('sf12_fisica_cuartil') is not None:
        try:
            return int(reg['sf12_fisica_cuartil'])
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
        if isinstance(raw, (int, float)) and int(raw) in (1, 2, 3, 4):
            return int(raw)
        return transformar_sf12_fisica_a_cuartil(float(raw))
    except Exception:
        return transformar_sf12_fisica_a_cuartil(0)


# ═══════════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════

def mostrar_resultados():
    # --- Estilos CSS ---
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown("""
    <div class="anxrisk-page-header">
        <h1>Resultados de la Evaluación</h1>
        <p>Análisis completo del riesgo de ansiedad</p>
    </div>
    """, unsafe_allow_html=True)

    # Verificar datos completos
    if 'resultados' not in st.session_state or 'zsas' not in st.session_state.get('resultados', {}):
        st.warning("⚠️ No hay datos disponibles. Complete todos los cuestionarios primero.")
        if st.button("← Volver a Ansiedad (ZSAS)"):
            st.session_state.pagina_actual = 'Ansiedad (ZSAS)'
            st.rerun()
        return

    registro = obtener_registro_actual()

    # ── PASO 1: Genética + botón "Generar" (si aún no se generó) ─
    if not st.session_state.get('evaluacion_generada', False):
        _mostrar_seccion_pregenerada(registro)
        return

    # ── PASO 2: Resultados ya generados ──────────────────────────
    _mostrar_evaluacion_completa(registro)


# ═══════════════════════════════════════════════════════════════════
# PASO 1 — Resumen + genética + botón Generar
# ═══════════════════════════════════════════════════════════════════

def _mostrar_seccion_pregenerada(registro):
    """Muestra resumen de cuestionarios, opción de genética y botón para generar la evaluación."""

    st.markdown("""
    <div style="background:#E3F2FD; padding:1.25rem; border-radius:8px; border-left:4px solid #2B87D1; margin-bottom:1.5rem;">
        <p style="color:#2E2E2E; margin:0; font-size:1rem;">
            <strong>✅ Todos los cuestionarios han sido completados.</strong><br>
            Confirme si desea incluir los datos genéticos y genere la evaluación de riesgo.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Resumen rápido
    _mostrar_resumen_cuestionarios()

    st.markdown("---")

    # ── Confirmación de panel genético ──────────────────────────────
    st.markdown("""
    <div class="anxrisk-card">
        <h3>🧬 Confirmación de Datos Genéticos</h3>
        <p style="margin-bottom: 0.75rem;">
            Si dispone de los datos genéticos del paciente, active el panel para utilizar el
            <strong>modelo extendido (22 features)</strong>. De lo contrario, se utilizará el
            <strong>modelo estándar (13 features)</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tiene_genetica = st.toggle(
        "Confirmar inclusión de panel genético (modelo extendido — 22 features)",
        value=False,
        key="toggle_genetica",
    )

    if tiene_genetica:
        # Recuperar genotipos previamente ingresados (si existen)
        gen_previos = st.session_state.get('resultados', {}).get('datos_geneticos') or {}
        prkca_prev = gen_previos.get('prkca')
        tcf4_prev = gen_previos.get('tcf4')
        cdh20_prev = gen_previos.get('cdh20')

        def _idx(opciones, valor):
            try:
                return opciones.index(valor)
            except (ValueError, AttributeError):
                return None

        st.markdown("""
        <div class="anxrisk-question-card">
            <div class="anxrisk-question-text">Confirme los genotipos del paciente:</div>
        </div>
        """, unsafe_allow_html=True)
        g1, g2, g3 = st.columns(3)
        with g1:
            prkca_sel = st.selectbox("Genotipo PRKCA", GENOTIPOS_PRKCA, key="gen_prkca_sel",
                                     index=_idx(GENOTIPOS_PRKCA, prkca_prev), placeholder="Seleccione")
        with g2:
            tcf4_sel = st.selectbox("Genotipo TCF4", GENOTIPOS_TCF4, key="gen_tcf4_sel",
                                    index=_idx(GENOTIPOS_TCF4, tcf4_prev), placeholder="Seleccione")
        with g3:
            cdh20_sel = st.selectbox("Genotipo CDH20", GENOTIPOS_CDH20, key="gen_cdh20_sel",
                                     index=_idx(GENOTIPOS_CDH20, cdh20_prev), placeholder="Seleccione")

        genotipos_completos = all([prkca_sel, tcf4_sel, cdh20_sel])
        if not genotipos_completos:
            st.warning("Confirme los 3 genotipos para utilizar el modelo extendido.")
    else:
        genotipos_completos = True  # No se requieren genotipos
        prkca_sel = tcf4_sel = cdh20_sel = None

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # ── Botón ─────────────────────────────────────────────────────
    disabled = tiene_genetica and not genotipos_completos
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🚀 Generar Evaluación de Riesgo", type="primary", use_container_width=True, disabled=disabled):
            # Guardar genética
            if tiene_genetica and genotipos_completos:
                st.session_state.resultados['datos_geneticos'] = {
                    'prkca': prkca_sel, 'tcf4': tcf4_sel, 'cdh20': cdh20_sel,
                }
            else:
                st.session_state.resultados['datos_geneticos'] = None
            st.session_state.resultados['tiene_genetica'] = tiene_genetica

            # Predicción
            _ejecutar_prediccion(registro, tiene_genetica)

            st.session_state['evaluacion_generada'] = True
            st.rerun()


# ═══════════════════════════════════════════════════════════════════
# PASO 2 — Evaluación completa
# ═══════════════════════════════════════════════════════════════════

def _mostrar_evaluacion_completa(registro):
    """Muestra resultados, SHAP y descarga PDF."""

    resultados = st.session_state.resultados

    # ── Tarjeta principal de riesgo ───────────────────────────────
    prob_alto = resultados.get('prob_alto')
    nivel_triple = resultados.get('nivel_triple', 'No disponible')
    model_name = resultados.get('modelo_usado', '')

    if prob_alto is not None:
        color = "#F44336" if nivel_triple == 'Alto' else "#FFB74D" if nivel_triple == 'Moderado' else "#2B87D1"
        # Ángulo de la aguja: 0% → -90° (izquierda), 100% → +90° (derecha)
        angle = -90 + (prob_alto * 180)
        pct_text = f"{prob_alto:.1%}"

        import streamlit.components.v1 as components
        gauge_html = f"""
        <link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800&display=swap" rel="stylesheet">
        <div style='background:#FFF; padding:2rem 2rem 1.5rem; border-radius:16px;
                    box-shadow:0 4px 20px rgba(0,0,0,.08); border:1px solid #E0E0E0;
                    margin:0 auto; text-align:center; max-width:560px;
                    font-family:"Source Sans 3", sans-serif;'>

            <svg viewBox="0 0 300 180" style="width:100%; max-width:380px; margin:0 auto; display:block;">
                <path d="M 30 150 A 120 120 0 0 1 270 150" fill="none" stroke="#E8E8E8" stroke-width="22" stroke-linecap="round"/>
                <path d="M 30 150 A 120 120 0 0 1 79.47 52.92" fill="none" stroke="#2B87D1" stroke-width="22" stroke-linecap="round"/>
                <path d="M 79.47 52.92 A 120 120 0 0 1 187.08 35.87" fill="none" stroke="#FFB74D" stroke-width="22"/>
                <path d="M 187.08 35.87 A 120 120 0 0 1 270 150" fill="none" stroke="#F44336" stroke-width="22" stroke-linecap="round"/>

                <text x="28" y="172" font-size="11" fill="#2B87D1" font-weight="600" font-family="'Source Sans 3', sans-serif">Bajo</text>
                <text x="150" y="18" font-size="11" fill="#FFB74D" font-weight="600" font-family="'Source Sans 3', sans-serif" text-anchor="middle">Moderado</text>
                <text x="272" y="172" font-size="11" fill="#F44336" font-weight="600" font-family="'Source Sans 3', sans-serif" text-anchor="end">Alto</text>

                <text x="18" y="155" font-size="9" fill="#999" font-family="'Source Sans 3', sans-serif">0%</text>
                <text x="150" y="6" font-size="9" fill="#999" font-family="'Source Sans 3', sans-serif" text-anchor="middle">50%</text>
                <text x="282" y="155" font-size="9" fill="#999" font-family="'Source Sans 3', sans-serif" text-anchor="end">100%</text>

                <g transform="translate(150, 150)">
                    <line x1="0" y1="0" x2="0" y2="-95"
                          stroke="{color}" stroke-width="3.5" stroke-linecap="round"
                          transform="rotate({angle})"/>
                    <circle cx="0" cy="0" r="8" fill="{color}" stroke="#FFF" stroke-width="2"/>
                </g>

                <text x="150" y="130" font-size="28" font-weight="700" fill="{color}"
                      font-family="'Source Sans 3', sans-serif" text-anchor="middle">{pct_text}</text>
            </svg>

            <h2 style='color:{color}; margin:0.75rem 0 0.25rem; font-size:2rem; font-weight:700;
                        font-family:"Source Sans 3", sans-serif;'>{nivel_triple}</h2>
            <p style='color:#666; margin:0.25rem 0; font-size:1rem;
                       font-family:"Source Sans 3", sans-serif;'>Nivel de Riesgo de Ansiedad</p>
            <p style='color:#2E2E2E; margin:0.5rem 0 0; font-size:0.9rem;
                       font-family:"Source Sans 3", sans-serif;'>
                Modelo: <strong>{model_name}</strong></p>
        </div>
        """
        components.html(gauge_html, height=420, scrolling=False)

    # ── Resumen de cuestionarios ──────────────────────────────────
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    with st.expander("📋 Resumen de la Evaluación — Ver detalles de cuestionarios", expanded=False):
        _mostrar_resumen_cuestionarios()

    # ── Genética ──────────────────────────────────────────────────
    st.markdown("<h4 style='color:#2B87D1; font-size:1.2rem; margin-top:1.5rem;'>🧬 Perfil Genético</h4>", unsafe_allow_html=True)
    gen = resultados.get('datos_geneticos')
    if gen:
        gc1, gc2, gc3 = st.columns(3)
        for col, name, key in [(gc1, 'PRKCA', 'prkca'), (gc2, 'TCF4', 'tcf4'), (gc3, 'CDH20', 'cdh20')]:
            with col:
                st.markdown(f"""
                <div style='background:#F5F5F5; padding:1rem; border-radius:8px; border-left:3px solid #2B87D1;'>
                    <p style='color:#666; margin:0; font-size:.9rem;'>Gen {name}</p>
                    <p style='color:#2E2E2E; margin:0; font-size:1.3rem; font-weight:700;'>{gen[key]}</p>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("Módulo genético no utilizado (modo estándar)")

    # ── SHAP ──────────────────────────────────────────────────────
    model = resultados.get('model')
    X_for_model = resultados.get('X_for_model')
    genero = registro.get('genero') if registro else None
    if model is not None and X_for_model is not None:
        st.markdown("---")
        mostrar_shap_analysis(model, X_for_model, genero)

    # ── Nota clínica ──────────────────────────────────────────────
    st.markdown("""
    <div style='margin-top:1.5rem; padding:1rem; background:#FFF9E6; border-radius:8px; border-left:4px solid #FFC107;'>
        <p style='color:#2E2E2E; margin:.5rem 0;'><strong>⚠️ Nota importante:</strong></p>
        <p style='color:#2E2E2E; margin:.5rem 0;'>
        Esta herramienta proporciona un análisis preliminar basado en modelos de aprendizaje automático supervisado.
        Los resultados deben ser interpretados en el contexto clínico completo del paciente.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Descarga PDF ──────────────────────────────────────────────
    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    dc1, dc2, dc3 = st.columns([1, 2, 1])
    with dc2:
        try:
            pdf_bytes = generar_pdf_resultados(resultados, registro)
            nombre = registro.get('nombre', 'paciente') if registro else 'paciente'
            # Extraer apellido para nombre del archivo
            partes = nombre.strip().split()
            apellido = partes[-1] if len(partes) > 1 else partes[0]
            st.download_button(
                label="📥 Descargar Reporte en PDF",
                data=pdf_bytes,
                file_name=f"ANX_{apellido}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Error generando el PDF: {str(e)}")

    # ── Navegación ────────────────────────────────────────────────
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns([1, 1, 1])
    with n1:
        if st.button("← Volver a ZSAS", use_container_width=True):
            st.session_state['evaluacion_generada'] = False
            st.session_state.pagina_actual = 'Ansiedad (ZSAS)'
            st.rerun()
    with n2:
        if st.button("🔄 Regenerar Evaluación", use_container_width=True):
            st.session_state['evaluacion_generada'] = False
            st.rerun()
    with n3:
        if st.button("🏠 Nueva Evaluación", type="primary", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.session_state.pagina_actual = 'Home'
            st.rerun()


# ═══════════════════════════════════════════════════════════════════
# Resumen de cuestionarios (reutilizable)
# ═══════════════════════════════════════════════════════════════════

def _mostrar_resumen_cuestionarios():
    resultados = st.session_state.get('resultados', {})
    registro = obtener_registro_actual()

    # Plantilla de tarjeta métrica con tipografía Illumina
    _MC = """
    <div style="background:#FFF; padding:1rem 1.25rem; border-radius:8px;
                border-left:3px solid #2B87D1; margin-bottom:0.75rem;
                box-shadow:0 1px 4px rgba(0,0,0,.06);">
        <p style="color:#666; margin:0 0 0.25rem; font-size:0.85rem;
                  font-family:'Source Sans 3','Source Sans Pro',sans-serif;">{label}</p>
        <p style="color:#2E2E2E; margin:0; font-size:1.4rem; font-weight:700;
                  font-family:'Source Sans 3','Source Sans Pro',sans-serif;">{value}</p>
    </div>
    """
    _MC_CAP = """
    <div style="background:#FFF; padding:1rem 1.25rem; border-radius:8px;
                border-left:3px solid #2B87D1; margin-bottom:0.75rem;
                box-shadow:0 1px 4px rgba(0,0,0,.06);">
        <p style="color:#666; margin:0 0 0.25rem; font-size:0.85rem;
                  font-family:'Source Sans 3','Source Sans Pro',sans-serif;">{label}</p>
        <p style="color:#2E2E2E; margin:0; font-size:1.4rem; font-weight:700;
                  font-family:'Source Sans 3','Source Sans Pro',sans-serif;">{value}</p>
        <p style="color:#999; margin:0.25rem 0 0; font-size:0.8rem;
                  font-family:'Source Sans 3','Source Sans Pro',sans-serif;">{caption}</p>
    </div>
    """

    # Demográficos
    st.markdown("<h4 style='color:#2B87D1; font-size:1.2rem; margin-top:1.5rem; font-family:\"Source Sans 3\",sans-serif;'>👤 Datos Demográficos</h4>", unsafe_allow_html=True)
    demo = resultados.get('datos_demograficos') or st.session_state.get('datos_demograficos')
    if demo:
        d1, d2, d3 = st.columns(3)
        with d1:
            st.markdown(_MC.format(label="Edad", value=f"{demo.get('edad', '-')} años"), unsafe_allow_html=True)
        with d2:
            g = demo.get('genero', '-')
            if isinstance(g, int):
                g = "Masculino" if g == 0 else "Femenino"
            st.markdown(_MC.format(label="Género", value=g), unsafe_allow_html=True)
        with d3:
            st.markdown(_MC.format(label="Educación", value=f"{demo.get('años_educacion', '-')} años"), unsafe_allow_html=True)

    # LTE-12
    st.markdown("<h4 style='color:#2B87D1; font-size:1.2rem; margin-top:1.5rem; font-family:\"Source Sans 3\",sans-serif;'>📅 Eventos Vitales (LTE-12)</h4>", unsafe_allow_html=True)
    try:
        ev = resultados['eventos_vitales']
        st.markdown(_MC.format(label="Eventos estresantes", value=ev.get('total', '-')), unsafe_allow_html=True)
    except KeyError:
        st.info("Datos LTE-12 no disponibles")

    # SF-12
    st.markdown("<h4 style='color:#2B87D1; font-size:1.2rem; margin-top:1.5rem; font-family:\"Source Sans 3\",sans-serif;'>🏥 Salud SF-12</h4>", unsafe_allow_html=True)
    try:
        sf12 = resultados['sf12']
        s1, s2 = st.columns(2)
        with s1:
            pf = sf12.get('puntaje_fisico')
            if pf is not None:
                qf = sf12.get('cuartil_fisica')
                cap = _obtener_mensaje_cuartil_fisica(qf) if qf else ""
                if cap:
                    st.markdown(_MC_CAP.format(label="Componente Físico", value=f"{pf:.1f}", caption=cap), unsafe_allow_html=True)
                else:
                    st.markdown(_MC.format(label="Componente Físico", value=f"{pf:.1f}"), unsafe_allow_html=True)
        with s2:
            pm = sf12.get('puntaje_mental')
            if pm is not None:
                qm = sf12.get('cuartil_mental')
                cap = _obtener_mensaje_cuartil_mental(qm) if qm else ""
                if cap:
                    st.markdown(_MC_CAP.format(label="Componente Mental", value=f"{pm:.1f}", caption=cap), unsafe_allow_html=True)
                else:
                    st.markdown(_MC.format(label="Componente Mental", value=f"{pm:.1f}"), unsafe_allow_html=True)
    except KeyError:
        st.info("Datos SF-12 no disponibles")

    # HADS
    st.markdown("<h4 style='color:#2B87D1; font-size:1.2rem; margin-top:1.5rem; font-family:\"Source Sans 3\",sans-serif;'>😰 Ansiedad HADS</h4>", unsafe_allow_html=True)
    try:
        hads = resultados['hads']
        h1, h2 = st.columns(2)
        with h1:
            st.markdown(_MC.format(label="Puntaje", value=hads.get('puntaje', '-')), unsafe_allow_html=True)
        with h2:
            st.markdown(_MC.format(label="Nivel", value=hads.get('nivel', '-')), unsafe_allow_html=True)
    except KeyError:
        st.info("Datos HADS no disponibles")

    # ZSAS
    st.markdown("<h4 style='color:#2B87D1; font-size:1.2rem; margin-top:1.5rem; font-family:\"Source Sans 3\",sans-serif;'>😟 Ansiedad de Zung (ZSAS)</h4>", unsafe_allow_html=True)
    try:
        zsas = resultados['zsas']
        z1, z2 = st.columns(2)
        with z1:
            st.markdown(_MC.format(label="Puntaje bruto", value=zsas.get('total', '-')), unsafe_allow_html=True)
        with z2:
            st.markdown(_MC.format(label="Nivel", value=zsas.get('nivel', '-')), unsafe_allow_html=True)
    except KeyError:
        st.info("Datos ZSAS no disponibles")


# ═══════════════════════════════════════════════════════════════════
# Predicción CatBoost
# ═══════════════════════════════════════════════════════════════════

def _ejecutar_prediccion(registro, tiene_genetica):
    """Carga el modelo CatBoost, construye features y genera predicción."""
    if not registro:
        return

    model_path = MODEL_EXTENDED_PATH if tiene_genetica else MODEL_STANDARD_PATH
    model_name = "CatBoost Extendido (22 features)" if tiene_genetica else "CatBoost Estándar (13 features)"

    try:
        import joblib
        model = joblib.load(model_path)

        from src.utils.calculos import (
            transformar_lte12_a_clasificacion,
            transformar_sf12_mental_a_cuartil,
            transformar_educacion_a_binaria,
        )

        edad24 = registro.get('grupo_edad', 0)
        aefgroups = transformar_educacion_a_binaria(registro.get('años_educacion', 0))

        lte12_clasif = transformar_lte12_a_clasificacion(registro.get('lte12_puntaje', 0))
        lte12_0 = 1 if lte12_clasif == 0 else 0
        lte12_1 = 1 if lte12_clasif == 1 else 0
        lte12_2 = 1 if lte12_clasif == 2 else 0

        sf12f_cuartil = _obtener_sf12f_cuartil_desde_registro(registro)
        sf12m_cuartil = transformar_sf12_mental_a_cuartil(registro.get('sf12_mental', 0))

        features_dict = {
            'EDAD24': edad24,
            'AEFGROUPS': aefgroups,
            'LTE12_0': lte12_0, 'LTE12_1': lte12_1, 'LTE12_2': lte12_2,
            'SF12F_Q1': 1 if sf12f_cuartil == 1 else 0,
            'SF12F_Q2': 1 if sf12f_cuartil == 2 else 0,
            'SF12F_Q3': 1 if sf12f_cuartil == 3 else 0,
            'SF12F_Q4': 1 if sf12f_cuartil == 4 else 0,
            'SF12M_Q1': 1 if sf12m_cuartil == 1 else 0,
            'SF12M_Q2': 1 if sf12m_cuartil == 2 else 0,
            'SF12M_Q3': 1 if sf12m_cuartil == 3 else 0,
            'SF12M_Q4': 1 if sf12m_cuartil == 4 else 0,
        }

        if tiene_genetica:
            gd = st.session_state.resultados['datos_geneticos']
            prkca, tcf4, cdh20 = gd['prkca'], gd['tcf4'], gd['cdh20']
            features_dict.update({
                'PRKCA_C/C': 1 if prkca == 'C/C' else 0,
                'PRKCA_C/T': 1 if prkca == 'C/T' else 0,
                'PRKCA_T/T': 1 if prkca == 'T/T' else 0,
                'TCF4_A/A': 1 if tcf4 == 'A/A' else 0,
                'TCF4_A/T': 1 if tcf4 == 'A/T' else 0,
                'TCF4_T/T': 1 if tcf4 == 'T/T' else 0,
                'CDH20_A/A': 1 if cdh20 == 'A/A' else 0,
                'CDH20_A/G': 1 if cdh20 == 'A/G' else 0,
                'CDH20_G/G': 1 if cdh20 == 'G/G' else 0,
            })

        X = pd.DataFrame([features_dict])
        canonical_order = list(features_dict.keys())

        # Reordenar al orden del modelo si difiere
        model_features = None
        if hasattr(model, 'feature_names_in_'):
            model_features = list(model.feature_names_in_)
        elif hasattr(model, 'feature_name_'):
            model_features = list(model.feature_name_)

        X_for_model = X.copy()
        if model_features is not None:
            if set(model_features) == set(canonical_order):
                if model_features != canonical_order:
                    X_for_model = X[model_features]
            else:
                X_for_model = X.reindex(columns=model_features, fill_value=0)

        prediction = model.predict(X_for_model)[0]

        prob_alto = None
        if hasattr(model, 'predict_proba'):
            try:
                prob_alto = float(model.predict_proba(X_for_model)[0][1])
            except Exception:
                pass

        from src.utils.calculos import clasificar_por_youden
        nivel_triple = clasificar_por_youden(prob_alto, None, ancho=0.10) if prob_alto is not None else ('Alto' if prediction == 1 else 'Bajo')

        st.session_state.resultados.update({
            'prob_alto': prob_alto,
            'nivel_triple': nivel_triple,
            'model': model,
            'X_for_model': X_for_model,
            'modelo_usado': model_name,
        })

    except FileNotFoundError:
        st.session_state.resultados['error'] = f"Modelo no encontrado: {model_path}"
    except Exception as e:
        st.session_state.resultados['error'] = f"Error en la predicción: {str(e)}"


# ═══════════════════════════════════════════════════════════════════
# Análisis SHAP (pantalla)
# ═══════════════════════════════════════════════════════════════════

def mostrar_shap_analysis(model, X, genero):
    """Genera y muestra análisis SHAP con gráfico e interpretación."""
    st.markdown("### 📈 Análisis de Interpretabilidad (SHAP)")
    st.markdown("""
    <div style='background:#E3F2FD; padding:1rem; border-radius:8px; border-left:4px solid #2196F3; margin-bottom:1.5rem;'>
        <p style='color:#1565C0; margin:0; font-size:.95rem;'>
            <strong>ℹ️ SHAP</strong> (SHapley Additive exPlanations) muestra el impacto de cada característica
            en la predicción. Barras rojas → aumentan riesgo. Barras verdes → lo disminuyen.
        </p>
    </div>
    """, unsafe_allow_html=True)

    try:
        import shap
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        try:
            from catboost import CatBoostClassifier
            _has_cb = True
        except ImportError:
            _has_cb = False
        try:
            import lightgbm as lgb
            _has_lgb = True
        except ImportError:
            _has_lgb = False

        feature_names = list(X.columns)
        X_arr = X.values

        # Seleccionar explainer
        if _has_cb and isinstance(model, CatBoostClassifier):
            explainer = shap.TreeExplainer(model)
        elif _has_lgb and isinstance(model, lgb.LGBMClassifier):
            explainer = shap.TreeExplainer(model)
        else:
            explainer = shap.KernelExplainer(model.predict_proba, X_arr, feature_names=feature_names)

        sv = explainer.shap_values(X_arr)
        if isinstance(sv, list):
            sv = sv[1]

        if hasattr(sv, 'values'):
            shap_arr = sv.values
        elif isinstance(sv, np.ndarray):
            shap_arr = sv
        else:
            shap_arr = np.array(sv)

        if shap_arr.ndim == 1:
            shap_arr = shap_arr.reshape(1, -1)
        elif shap_arr.ndim == 3:
            shap_arr = shap_arr[:, :, -1]

        # Guardar para PDF
        st.session_state.resultados['shap_array'] = shap_arr
        st.session_state.resultados['shap_feature_names'] = feature_names

        top_n = min(15, X.shape[1])
        top_idx = np.argsort(np.abs(shap_arr[0]))[-top_n:][::-1]
        top_vals = shap_arr[0][top_idx]
        top_names = [feature_names[i] for i in top_idx]

        fig, ax = plt.subplots(figsize=(10, 8))
        bar_c = ['#DC3545' if v > 0 else '#28A745' for v in top_vals]
        ax.barh(range(len(top_vals)), top_vals, color=bar_c, alpha=0.8, edgecolor='black', linewidth=0.5)
        ax.set_yticks(range(len(top_vals)))
        ax.set_yticklabels(top_names, fontsize=10)
        ax.set_xlabel('SHAP Value (Contribución al Riesgo)', fontsize=12, fontweight='bold')
        ax.set_title('Impacto de Características en la Predicción', fontsize=14, fontweight='bold')
        ax.axvline(x=0, color='black', linewidth=1.5)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        from matplotlib.patches import Patch
        ax.legend(handles=[
            Patch(facecolor='#DC3545', alpha=0.8, edgecolor='black', label='Aumenta Riesgo'),
            Patch(facecolor='#28A745', alpha=0.8, edgecolor='black', label='Disminuye Riesgo'),
        ], loc='lower right', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.markdown("""
        <div style='background:#F8F9FA; padding:1rem; border-radius:8px; border-left:4px solid #6C757D; margin:1rem 0;'>
            <p style='color:#2E2E2E; margin:0; font-weight:600;'>📊 Interpretación:</p>
            <ul style='margin:.5rem 0 0 1rem;'>
                <li style='color:#DC3545;'>🔴 Barras rojas (→): Factores que <strong>AUMENTAN</strong> el riesgo</li>
                <li style='color:#28A745;'>🟢 Barras verdes (←): Factores que <strong>DISMINUYEN</strong> el riesgo</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 📋 Explicación Detallada")
        _mostrar_interpretacion_shap(shap_arr, feature_names, X, top_idx)

    except Exception as e:
        st.error(f"Error generando análisis SHAP: {str(e)}")


def _mostrar_interpretacion_shap(shap_arr, feature_names, X, top_indices):
    st.markdown("""
    <div style='background:#FFF; padding:1.5rem; border-radius:8px; border:1px solid #E0E0E0; margin-top:1rem;'>
        <h4 style='color:#2E2E2E; margin-top:0; border-bottom:2px solid #2B87D1; padding-bottom:.5rem;'>
            🔍 Cómo se Llegó a Esta Predicción
        </h4>
    </div>
    """, unsafe_allow_html=True)

    for idx in top_indices:
        feat = feature_names[idx]
        sv = shap_arr[0][idx]
        fv = X.iloc[0, idx]
        color = "#DC3545" if sv > 0 else "#28A745"
        efecto = "aumenta" if sv > 0 else "disminuye"
        icono = "⬆️" if sv > 0 else "⬇️"
        interp = obtener_interpretacion_feature(feat, fv)
        st.markdown(f"""
        <div style='background:#F9F9F9; padding:.75rem; margin:.5rem 0; border-radius:6px; border-left:4px solid {color};'>
            <strong style='color:{color};'>{icono} {feat}</strong>
            <p style='color:#2E2E2E; margin:.3rem 0; font-size:.9rem;'>{interp}</p>
            <p style='color:#666; margin:0; font-size:.85rem;'>{efecto} riesgo (~{abs(sv):.3f} SHAP)</p>
        </div>""", unsafe_allow_html=True)


def obtener_interpretacion_feature(feature, feature_val):
    """Interpretación clínica legible de una feature."""
    if feature == "EDAD24":
        return f"Grupo de edad {'24-34 años' if feature_val == 1 else 'fuera de 24-34 años'}"
    if feature == "AEFGROUPS":
        return f"Nivel educativo {'superior (≥15 años)' if feature_val == 1 else 'básico/secundario (<15 años)'}"
    if "SF12F" in feature:
        q = feature.split("_")[1]
        d = {"Q1": "salud física muy baja", "Q2": "salud física baja", "Q3": "salud física moderada", "Q4": "salud física buena"}
        return f"Paciente presenta {d.get(q, q)}" if feature_val == 1 else f"No pertenece a {q}"
    if "SF12M" in feature:
        q = feature.split("_")[1]
        d = {"Q1": "salud mental muy baja", "Q2": "salud mental baja", "Q3": "salud mental moderada", "Q4": "salud mental buena"}
        return f"Paciente presenta {d.get(q, q)}" if feature_val == 1 else f"No pertenece a {q}"
    if "PRKCA" in feature:
        g = feature.split("_")[1]
        return f"Genotipo PRKCA {g} {'presente' if feature_val == 1 else 'ausente'} (regulación del estrés)"
    if "TCF4" in feature:
        g = feature.split("_")[1]
        return f"Genotipo TCF4 {g} {'presente' if feature_val == 1 else 'ausente'} (transcripción neuronal)"
    if "CDH20" in feature:
        g = feature.split("_")[1]
        return f"Genotipo CDH20 {g} {'presente' if feature_val == 1 else 'ausente'} (conectividad neuronal)"
    if "LTE12" in feature:
        n = feature.split("_")[1]
        d = {"0": "sin eventos vitales estresantes", "1": "1 evento vital estresante", "2": "2+ eventos vitales estresantes"}
        return f"Paciente experimentó {d.get(n, n)}" if feature_val == 1 else f"No en categoría LTE12_{n}"
    return f"Valor: {feature_val}"


# ═══════════════════════════════════════════════════════════════════
# Generación de PDF con ReportLab
# ═══════════════════════════════════════════════════════════════════

def generar_pdf_resultados(resultados, registro):
    """
    Genera PDF profesional:
    - Portada con datos del paciente
    - Secciones clínicas (demográficos, LTE-12, SF-12, HADS, ZSAS)
    - Genética (si aplica)
    - Predicción de riesgo + umbrales
    - Gráfico SHAP + interpretación textual
    - Nota clínica + Firma del profesional y paciente
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import (
        SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
        PageBreak, Image, HRFlowable,
    )
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=60)
    elems = []

    # ── Paleta ────────────────────────────────────────────────────
    C_PRIM = colors.HexColor('#2C5F7C')
    C_SEC  = colors.HexColor('#5DA5C8')
    C_TXT  = colors.HexColor('#2E2E2E')
    C_BG   = colors.HexColor('#F8F9FA')
    C_OK   = colors.HexColor('#2B87D1')
    C_WARN = colors.HexColor('#FFC107')
    C_DANG = colors.HexColor('#DC3545')

    styles = getSampleStyleSheet()
    title_s  = ParagraphStyle('T', parent=styles['Heading1'], fontSize=22, textColor=C_PRIM,
                               spaceAfter=8, alignment=TA_CENTER, fontName='Helvetica-Bold', leading=26)
    sub_s    = ParagraphStyle('S', parent=styles['Normal'], fontSize=11, textColor=C_TXT,
                               spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica', leading=14)
    head_s   = ParagraphStyle('H', parent=styles['Heading2'], fontSize=14, textColor=C_PRIM,
                               spaceAfter=10, spaceBefore=15, fontName='Helvetica-Bold', leading=16)
    norm_s   = ParagraphStyle('N', parent=styles['Normal'], fontSize=10, spaceAfter=8,
                               textColor=C_TXT, alignment=TA_JUSTIFY, fontName='Helvetica', leading=13)
    small_s  = ParagraphStyle('Sm', parent=styles['Normal'], fontSize=8, textColor=colors.HexColor('#888'),
                               alignment=TA_CENTER, fontName='Helvetica', leading=10)

    def _tbl(data, cw=None):
        t = Table(data, colWidths=cw)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), C_PRIM),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME',  (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE',  (0, 0), (-1, 0), 10),
            ('FONTSIZE',  (0, 1), (-1, -1), 9),
            ('ALIGN',     (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN',    (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING',    (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), C_BG),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCC')),
        ]))
        return t

    fecha_eval = datetime.now().strftime('%d/%m/%Y — %H:%M')
    demo = resultados.get('datos_demograficos') or st.session_state.get('datos_demograficos') or {}
    nombre_pac = demo.get('nombre', registro.get('nombre', '—')) if registro else demo.get('nombre', '—')
    modelo_usado = resultados.get('modelo_usado', '—')

    # ══════════ PORTADA ══════════
    elems.append(Spacer(1, 1.5 * inch))
    elems.append(HRFlowable(width="60%", thickness=2, color=C_SEC, spaceAfter=20))
    elems.append(Paragraph("REPORTE DE EVALUACIÓN", title_s))
    elems.append(Paragraph("RIESGO DE ANSIEDAD", title_s))
    elems.append(Spacer(1, 0.2 * inch))
    elems.append(HRFlowable(width="60%", thickness=2, color=C_SEC, spaceAfter=30))
    elems.append(Paragraph(f"<b>Paciente:</b> {nombre_pac}", sub_s))
    elems.append(Paragraph(f"<b>Fecha:</b> {fecha_eval}", sub_s))
    elems.append(Paragraph(f"<b>Modelo:</b> {modelo_usado}", sub_s))
    elems.append(Spacer(1, 1 * inch))
    elems.append(Paragraph("Sistema ANXRISK · Evaluación Profesional de Riesgo de Ansiedad", small_s))
    elems.append(PageBreak())

    # ══════════ 1. DEMOGRÁFICOS ══════════
    elems.append(Paragraph("1. Datos Demográficos", head_s))
    if demo:
        g = demo.get('genero', '—')
        if isinstance(g, int):
            g = "Masculino" if g == 0 else "Femenino"
        edu = demo.get('años_educacion', '—')
        edu_lbl = f"{edu} años" + (f" — {'Superior' if edu >= 15 else 'Básico/Secundario'}" if isinstance(edu, (int, float)) else "")
        elems.append(_tbl([
            ["Campo", "Valor"],
            ["Nombre", nombre_pac],
            ["Edad", f"{demo.get('edad', '—')} años"],
            ["Género", g],
            ["Nivel educativo", edu_lbl],
        ], cw=[180, 300]))
    else:
        elems.append(Paragraph("Datos demográficos no disponibles.", norm_s))
    elems.append(Spacer(1, 0.3 * inch))

    # ══════════ 2. LTE-12 ══════════
    elems.append(Paragraph("2. Eventos Vitales Estresantes (LTE-12)", head_s))
    ev = resultados.get('eventos_vitales', {})

    # Lista de los 12 eventos del LTE
    lte_preguntas = [
        "Enfermedad, lesión o agresión grave propia",
        "Enfermedad/lesión/agresión grave de un familiar cercano",
        "Muerte de padres, hijos o pareja/cónyuge",
        "Muerte de amigo cercano u otro familiar",
        "Separación por problemas matrimoniales",
        "Ruptura de relación estable",
        "Problema grave con amigo, vecino o familiar",
        "Desempleo o búsqueda sin éxito (>1 mes)",
        "Despido laboral",
        "Crisis económica grave",
        "Problemas con la policía o tribunal",
        "Robo o pérdida de objeto de valor",
    ]
    respuestas_ev = ev.get('respuestas', [])
    total_ev = ev.get('total', sum(r for r in respuestas_ev if r == 1) if respuestas_ev else 0)
    eventos_si = [(i + 1, lte_preguntas[i]) for i, r in enumerate(respuestas_ev) if r == 1 and i < len(lte_preguntas)]

    # Tabla de detalle: cada evento con Sí/No
    ev_table_data = [["#", "Evento Vital", "Presente"]]
    for i, pregunta in enumerate(lte_preguntas):
        resp_val = respuestas_ev[i] if i < len(respuestas_ev) else 0
        ev_table_data.append([str(i + 1), pregunta, "Sí" if resp_val == 1 else "No"])

    ev_tbl = Table(ev_table_data, colWidths=[30, 370, 80])
    ev_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_PRIM),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME',  (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',  (0, 0), (-1, 0), 9),
        ('FONTSIZE',  (0, 1), (-1, -1), 9),
        ('ALIGN',     (0, 0), (0, -1), 'CENTER'),
        ('ALIGN',     (1, 0), (1, -1), 'LEFT'),
        ('ALIGN',     (2, 0), (2, -1), 'CENTER'),
        ('VALIGN',    (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, -1), C_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [C_BG, colors.white]),
    ]))
    # Resaltar filas con "Sí" en rojo suave
    for row_idx, (i, pregunta) in enumerate([(i, lte_preguntas[i]) for i in range(len(lte_preguntas))], start=1):
        resp_val = respuestas_ev[i] if i < len(respuestas_ev) else 0
        if resp_val == 1:
            ev_tbl.setStyle(TableStyle([
                ('TEXTCOLOR', (2, row_idx), (2, row_idx), C_DANG),
                ('FONTNAME',  (2, row_idx), (2, row_idx), 'Helvetica-Bold'),
            ]))
    elems.append(ev_tbl)

    # Resumen al pie
    elems.append(Spacer(1, 0.1 * inch))
    clasif = ev.get('clasificacion', '—')
    clasif_texto = {0: "Sin eventos significativos", 1: "Nivel moderado", 2: "Nivel alto"}.get(clasif, str(clasif))
    elems.append(Paragraph(
        f"<b>Total de eventos reportados:</b> {total_ev} de 12 &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b>Clasificación:</b> {clasif_texto}",
        norm_s,
    ))

    elems.append(Spacer(1, 0.3 * inch))

    # ══════════ 3. SF-12 ══════════
    elems.append(Paragraph("3. Salud Física y Mental (SF-12)", head_s))
    sf12 = resultados.get('sf12', {})
    pf = sf12.get('puntaje_fisico', '—')
    pm = sf12.get('puntaje_mental', '—')
    qf = sf12.get('cuartil_fisica', '—')
    qm = sf12.get('cuartil_mental', '—')
    elems.append(_tbl([
        ["Componente", "Puntaje", "Cuartil"],
        ["Físico", f"{pf:.1f}" if isinstance(pf, (int, float)) else str(pf), f"Q{qf}" if isinstance(qf, int) else str(qf)],
        ["Mental", f"{pm:.1f}" if isinstance(pm, (int, float)) else str(pm), f"Q{qm}" if isinstance(qm, int) else str(qm)],
    ], cw=[160, 160, 160]))
    elems.append(Spacer(1, 0.3 * inch))

    # ══════════ 4. HADS ══════════
    elems.append(Paragraph("4. Ansiedad HADS", head_s))
    hads = resultados.get('hads', {})
    elems.append(_tbl([
        ["Indicador", "Valor"],
        ["Puntaje HADS", str(hads.get('puntaje', '—'))],
        ["Nivel de Ansiedad", str(hads.get('nivel', '—'))],
    ], cw=[250, 230]))
    elems.append(Spacer(1, 0.3 * inch))

    # ══════════ 5. ZSAS ══════════
    elems.append(Paragraph("5. Ansiedad de Zung (ZSAS)", head_s))
    zsas = resultados.get('zsas', {})
    elems.append(_tbl([
        ["Indicador", "Valor"],
        ["Puntaje bruto", str(zsas.get('total', '—'))],
        ["Nivel de Ansiedad", str(zsas.get('nivel', '—'))],
    ], cw=[250, 230]))
    elems.append(Spacer(1, 0.3 * inch))

    # ══════════ 6. GENÉTICA ══════════
    elems.append(Paragraph("6. Perfil Genético", head_s))
    gen = resultados.get('datos_geneticos')
    if gen:
        # Determinar si cada genotipo es de riesgo
        prkca_val = gen.get('prkca', '—')
        tcf4_val = gen.get('tcf4', '—')
        cdh20_val = gen.get('cdh20', '—')

        def _riesgo_prkca(g):
            return "Genotipo de riesgo" if g in ("C/T", "T/T") else "Genotipo sin riesgo asociado"

        def _riesgo_tcf4(g):
            return "Genotipo de riesgo" if g in ("T/T", "C/T") else "Genotipo sin riesgo asociado"

        def _riesgo_cdh20(g):
            return "Genotipo asociado a alto riesgo" if g == "G/G" else "Genotipo sin riesgo asociado"

        elems.append(_tbl([
            ["Gen", "Genotipo", "Interpretación"],
            ["PRKCA", prkca_val, _riesgo_prkca(prkca_val)],
            ["TCF4", tcf4_val, _riesgo_tcf4(tcf4_val)],
            ["CDH20", cdh20_val, _riesgo_cdh20(cdh20_val)],
        ], cw=[120, 120, 240]))

        # Nota explicativa sobre genotipos de riesgo
        elems.append(Spacer(1, 0.1 * inch))
        elems.append(Paragraph(
            "<b>Nota:</b> Los genotipos C/T y T/T en PRKCA, T/T y C/T en TCF4, y G/G en CDH20 "
            "se consideran genotipos asociados a mayor riesgo de ansiedad según la evidencia genética disponible.",
            norm_s,
        ))
    else:
        elems.append(Paragraph("Evaluación sin datos genéticos (modo estándar — 13 features).", norm_s))
    elems.append(Spacer(1, 0.3 * inch))

    # ══════════ 7. PREDICCIÓN ══════════
    elems.append(PageBreak())
    elems.append(Paragraph("7. Predicción de Riesgo", head_s))

    prob_alto = resultados.get('prob_alto')
    nivel_triple = resultados.get('nivel_triple', '—')
    if prob_alto is not None:
        c_nivel = C_DANG if nivel_triple == 'Alto' else C_WARN if nivel_triple == 'Moderado' else C_OK
        nivel_ps = ParagraphStyle('NivelP', parent=norm_s, fontSize=16, textColor=c_nivel,
                                   alignment=TA_CENTER, fontName='Helvetica-Bold', leading=20)
        elems.append(Paragraph(f"Nivel de Riesgo: {nivel_triple}", nivel_ps))
        elems.append(Paragraph(f"Probabilidad de alto riesgo: {prob_alto:.1%}", sub_s))
        elems.append(Spacer(1, 0.15 * inch))
        elems.append(Paragraph("Umbrales de Clasificación:", head_s))
        elems.append(_tbl([
            ["Categoría", "Rango"],
            ["Bajo", "0.00 – 0.29"],
            ["Moderado", "0.30 – 0.59"],
            ["Alto", "0.60 – 1.00"],
        ], cw=[200, 280]))
    else:
        elems.append(Paragraph("Probabilidad no disponible.", norm_s))
    elems.append(Spacer(1, 0.3 * inch))

    # ══════════ 8. SHAP ══════════
    elems.append(Paragraph("8. Análisis de Interpretabilidad (SHAP)", head_s))
    shap_arr = resultados.get('shap_array')
    feat_names = resultados.get('shap_feature_names')
    X_fm = resultados.get('X_for_model')

    if shap_arr is not None and feat_names is not None and X_fm is not None:
        try:
            top_n = min(15, len(feat_names))
            t_idx = np.argsort(np.abs(shap_arr[0]))[-top_n:][::-1]
            t_vals = shap_arr[0][t_idx]
            t_names = [feat_names[i] for i in t_idx]

            fig, ax = plt.subplots(figsize=(7, 5), dpi=120)
            bc = ['#DC3545' if v > 0 else '#28A745' for v in t_vals]
            ax.barh(range(len(t_vals)), t_vals, color=bc, alpha=0.85, edgecolor='black', linewidth=0.4)
            ax.set_yticks(range(len(t_vals)))
            ax.set_yticklabels(t_names, fontsize=8)
            ax.set_xlabel('SHAP Value', fontsize=9, fontweight='bold')
            ax.set_title(f'Top {top_n} Características Influyentes', fontsize=10, fontweight='bold')
            ax.axvline(x=0, color='black', linewidth=1.2)
            ax.grid(axis='x', alpha=0.25, linestyle='--')
            plt.tight_layout()

            img_buf = BytesIO()
            plt.savefig(img_buf, format='png', bbox_inches='tight', dpi=120)
            img_buf.seek(0)
            plt.close(fig)

            elems.append(Image(img_buf, width=5.5 * inch, height=3.8 * inch))
            elems.append(Spacer(1, 0.2 * inch))

            elems.append(Paragraph("Factores Clave:", head_s))
            for rank, idx in enumerate(t_idx[:10], 1):
                feat = feat_names[idx]
                sv = shap_arr[0][idx]
                fv = X_fm.iloc[0, idx]
                efecto = "aumenta" if sv > 0 else "disminuye"
                interp = obtener_interpretacion_feature(feat, fv)
                elems.append(Paragraph(f"{rank}. <b>{feat}</b>: {interp} ({efecto} riesgo)", norm_s))

        except Exception:
            elems.append(Paragraph("No se pudo generar el gráfico SHAP.", norm_s))
    else:
        elems.append(Paragraph("Análisis SHAP no disponible.", norm_s))

    # ══════════ NOTA CLÍNICA ══════════
    elems.append(Spacer(1, 0.4 * inch))
    elems.append(HRFlowable(width="100%", thickness=1, color=C_WARN, spaceAfter=10))
    elems.append(Paragraph(
        "<b>Nota Importante:</b> Esta herramienta proporciona un análisis preliminar basado en modelos "
        "de aprendizaje automático supervisado. Los resultados deben ser interpretados en el contexto "
        "clínico completo del paciente y utilizados como apoyo en la toma de decisiones clínicas. "
        "No sustituye la valoración profesional.", norm_s,
    ))

    # ══════════ FIRMA DEL PROFESIONAL Y PACIENTE ══════════
    elems.append(Spacer(1, 1.2 * inch))
    elems.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CCC'), spaceAfter=15))

    fecha_firma = datetime.now().strftime('%d/%m/%Y')

    # Datos del profesional evaluador (capturados en Demográficos)
    nombre_prof = st.session_state.get('_prof_nombre', '') or st.session_state.get('prof_nombre', '') or '____________________'
    cargo_prof = st.session_state.get('_prof_cargo', '') or st.session_state.get('prof_cargo', '')
    institucion_prof = st.session_state.get('_prof_institucion', '') or st.session_state.get('prof_institucion', '')
    tp_prof = st.session_state.get('_prof_tp', '') or st.session_state.get('prof_tp', '') or '_______________'

    # Nombre del paciente
    nombre_paciente = registro.get('nombre', '____________________') if registro else '____________________'

    firma_data = [
        ["", ""],
        ["_________________________", "_________________________"],
        ["Firma del Profesional", "Firma del Paciente"],
        [f"Nombre: {nombre_prof}", f"Nombre: {nombre_paciente}"],
    ]
    if cargo_prof:
        firma_data.append([f"Cargo: {cargo_prof}", ""])
    if institucion_prof:
        firma_data.append([f"Institución: {institucion_prof}", ""])
    firma_data.append([f"T.P.: {tp_prof}", "Documento: __________________"])
    firma_data.append([f"Fecha: {fecha_firma}", f"Fecha: {fecha_firma}"])
    ft = Table(firma_data, colWidths=[240, 240])
    ft.setStyle(TableStyle([
        ('ALIGN',   (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',  (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('TOPPADDING',    (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TEXTCOLOR', (0, 0), (-1, -1), C_TXT),
    ]))
    elems.append(ft)

    elems.append(Spacer(1, 0.5 * inch))
    elems.append(Paragraph(f"Reporte generado automáticamente por el Sistema ANXRISK · {fecha_eval}", small_s))

    # Build
    doc.build(elems)
    pdf_bytes = buf.getvalue()
    buf.close()
    return pdf_bytes
