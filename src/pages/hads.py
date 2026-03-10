"""
Escala HADS de Ansiedad
"""
import streamlit as st
from ..utils.calculos import calcular_nivel_hads
from ..utils.dataframe_manager import agregar_o_actualizar_registro

def mostrar_hads():
    # Page header
    st.markdown("""
    <div class="anxrisk-page-header">
        <h1>Escala HADS de Ansiedad</h1>
        <p>Evaluación de síntomas de ansiedad en la última semana</p>
    </div>
    """, unsafe_allow_html=True)

    # Context card
    st.markdown("""
    <div class="anxrisk-card">
        <h3>¿Por qué evaluamos la ansiedad con HADS?</h3>
        <p style="margin-bottom: 0.75rem;">
            La <strong>Escala HADS (Hospital Anxiety and Depression Scale)</strong> es una herramienta clínica validada
            internacionalmente que evalúa la presencia y severidad de síntomas de ansiedad. Esta escala se enfoca en
            manifestaciones emocionales y psicológicas de la ansiedad, complementando otras evaluaciones.
        </p>
        <p style="margin-bottom: 0.75rem;">
            Los resultados nos ayudan a comprender la intensidad de sus síntomas ansiosos y su impacto en su vida diaria.
        </p>
        <p style="font-size: 0.9375rem; color: var(--text-secondary); font-style: italic; text-align: center; margin-bottom: 0.5rem;">
            Todas las preguntas son obligatorias — Responda pensando en la última semana
        </p>
        <p style="font-size: 0.875rem; color: var(--text-secondary); text-align: center; margin: 0;">
            Zigmond, A. S., & Snaith, R. P. (1983). <em>The hospital anxiety and depression scale. Acta Psychiatrica Scandinavica</em>, 67(6), 361-370.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    preguntas_hads = {
        "1. Me siento tenso(a) o nervioso(a)": [
            "Nunca",
            "A veces",
            "Muchas veces",
            "Todos los días"
        ],
        "2. Todavía disfruto con lo que me ha gustado hacer": [
            "Nada",
            "Sólo un poco",
            "No mucho",
            "Como siempre"
        ],
        "3. Tengo una sensación de miedo, como si algo horrible fuera a suceder": [
            "Nada",
            "Un poco, pero no me preocupa",
            "Si, pero no es muy fuerte",
            "Definitivamente y es muy fuerte"
        ],
        "4. Puedo estar sentado(a) tranquilamente y sentirme relajado(a)": [
            "Nunca",
            "No muy seguido",
            "Generalmente",
            "Siempre"
        ],
        "5. Tengo una sensación extraña, como de aleteo o vacío en el estómago": [
            "Nunca",
            "En ciertas ocasiones",
            "Con bastante frecuencia",
            "Muy seguido"
        ],
        "6. Me siento inquieto(a), como si no pudiera parar de moverme": [
            "Nunca",
            "No mucho",
            "Mucho",
            "Bastante"
        ],
        "7. Presento una sensación de miedo muy intenso de un momento a otro": [
            "Nunca",
            "No muy seguido",
            "Muy frecuentemente",
            "Bastante seguido"
        ]
    }
    
    respuestas = []
    contador = 0

    # Inline progress bar
    hads_keys = [f"hads_{p[:10]}" for p in preguntas_hads.keys()]
    answered = sum(1 for k in hads_keys if st.session_state.get(k) is not None)
    progress_pct = (answered / len(preguntas_hads)) * 100
    st.markdown(f"""
    <div class="anxrisk-inline-progress">
        <div class="anxrisk-inline-progress-bar" style="width: {progress_pct}%;"></div>
    </div>
    """, unsafe_allow_html=True)

    for pregunta, opciones in preguntas_hads.items():
        contador += 1
        texto = pregunta.split('. ', 1)[1]

        st.markdown(f"""
        <div class="anxrisk-question-card section-hads">
            <div class="anxrisk-question-number section-hads">Pregunta {contador} de {len(preguntas_hads)}</div>
            <div class="anxrisk-question-text">{texto}</div>
        </div>
        """, unsafe_allow_html=True)

        resp = None
        _, col_radio, _ = st.columns([1, 3, 1])
        with col_radio:
            resp = st.radio(
                pregunta,
                opciones,
                key=f"hads_{pregunta[:10]}",
                horizontal=True,
                label_visibility="collapsed",
                index=None
            )
        if resp is not None:
            respuestas.append(opciones.index(resp))
        else:
            respuestas.append(None)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if any(r is None for r in respuestas) or len(respuestas) < len(preguntas_hads):
            st.error("Responda todas las preguntas antes de continuar.")
            disabled = True
        else:
            st.success("Todas las preguntas completadas")
            disabled = False
    
    with col2:
        if st.button("Siguiente", key="btn_hads_next", type="primary", disabled=disabled, use_container_width=True):
            total = sum(respuestas)
            nivel = calcular_nivel_hads(total)

            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}
            st.session_state.resultados['hads'] = {
                'puntaje': total,
                'nivel': nivel,
                'respuestas': respuestas,
            }
            agregar_o_actualizar_registro({'ansiedad': total, 'depresion': None}, tipo_datos='hads')

            st.session_state.pagina_actual = "Ansiedad (ZSAS)"
            st.rerun()
            return total, nivel

    return None
