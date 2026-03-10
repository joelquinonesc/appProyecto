"""
Escala de Ansiedad de Zung (ZSAS)
"""
import streamlit as st
from ..utils.calculos import calcular_nivel_zsas
from ..utils.dataframe_manager import agregar_o_actualizar_registro

def mostrar_zsas():
    # Page header
    st.markdown("""
    <div class="anxrisk-page-header">
        <h1>Escala de Ansiedad de Zung (ZSAS)</h1>
        <p>Evaluación detallada de síntomas afectivos y somáticos de ansiedad — 20 ítems</p>
    </div>
    """, unsafe_allow_html=True)

    # Context card
    st.markdown("""
    <div class="anxrisk-card">
        <h3>Contexto clínico</h3>
        <p style="margin-bottom: 0.75rem; text-align: center;">
            La <strong>Escala de Ansiedad de Zung (ZSAS)</strong> es una herramienta ampliamente
            utilizada que evalúa tanto los aspectos afectivos como somáticos de la ansiedad. Con
            20 ítems, proporciona una evaluación comprensiva de síntomas físicos y emocionales.
        </p>
        <p style="font-size: 0.9375rem; color: var(--text-secondary); font-style: italic; text-align: center; margin-bottom: 0.5rem;">
            Todas las preguntas son obligatorias — Responda pensando en la última semana
        </p>
        <p style="font-size: 0.875rem; color: var(--text-secondary); text-align: center; margin: 0;">
            Zung, W. W. (1971). <em>Psychosomatics</em>, 12(6), 371-379.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    respuestas = []
    _mostrar_todas_preguntas(respuestas)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        respuestas_validas = [r for r in respuestas if r is not None]
        if len(respuestas_validas) < 20:
            st.error("Responda todas las preguntas antes de continuar.")
            disabled = True
        else:
            st.success("Todas las preguntas completadas")
            disabled = False
    
    with col2:
        if st.button("Siguiente", key="btn_zsas_next", type="primary", disabled=disabled, use_container_width=True):
            respuestas_validas = [r for r in respuestas if r is not None]
            total = sum(respuestas_validas)
            total_normalizado = total * 1.25
            nivel = calcular_nivel_zsas(total_normalizado)

            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}

            st.session_state.resultados['zsas'] = {
                'total': total,
                'total_normalizado': total_normalizado,
                'nivel': nivel,
            }
            agregar_o_actualizar_registro({'puntaje_normalizado': total_normalizado}, tipo_datos='zsas')

            st.session_state.pagina_actual = "resultados"
            st.rerun()
            return total, total_normalizado, nivel

    return None

def _mostrar_todas_preguntas(respuestas):
    """Muestra todas las preguntas del ZSAS en orden del 1 al 20"""
    
    preguntas_ordenadas = [
        ("1. Me siento más nervioso y ansioso de lo habitual", True),
        ("2. Me siento con temor sin razón", True),
        ("3. Me irrito con facilidad o siento pánico", True),
        ("4. Me siento como si fuera a reventar y partirme en pedazos", True),
        ("5. Siento que todo está bien y nada malo pasará", False),
        ("6. Mis brazos y piernas tiemblan", True),
        ("7. Me mortifican los dolores de la cabeza, cuello o cintura", True),
        ("8. Me siento débil y me canso fácilmente", True),
        ("9. Me siento tranquilo(a) y puedo permanecer en calma fácilmente", False),
        ("10. Puedo sentir que me late muy rápido el corazón", True),
        ("11. Sufro de mareos", True),
        ("12. Sufro de desmayos o siento que me voy a desmayar", True),
        ("13. Puedo inspirar y expirar fácilmente", False),
        ("14. Siento hormigueo/falta de sensibilidad en los dedos de las manos y pies", True),
        ("15. Sufro de molestias estomacales o indigestión", True),
        ("16. Orino con mucha frecuencia", True),
        ("17. Generalmente mis manos están secas y calientes", False),
        ("18. Siento bochornos / me he ruborizado con frecuencia", True),
        ("19. Me quedo dormido con facilidad y descanso durante la noche", False),
        ("20. Tengo pesadillas", True)
    ]
    
    opciones = ["Nunca o casi nunca", "A veces", "Con bastante frecuencia", "Siempre o casi siempre"]
    opciones_invertidas = list(reversed(opciones))
    
    total_preguntas = len(preguntas_ordenadas)

    for pregunta, es_regular in preguntas_ordenadas:
        numero = pregunta.split('.')[0]
        texto = pregunta.split('. ', 1)[1]
        
        st.markdown(f"""
        <div class="anxrisk-question-card">
            <div class="anxrisk-question-number">Pregunta {numero} de {total_preguntas}</div>
            <div class="anxrisk-question-text">{texto}</div>
        </div>
        """, unsafe_allow_html=True)

        resp = None
        _, col_radio, _ = st.columns([1, 3, 1])
        with col_radio:
            resp = st.radio(
                pregunta,
                options=opciones if es_regular else opciones_invertidas,
                key=f"zsas_{pregunta[:10]}",
                horizontal=True,
                label_visibility="collapsed",
                index=None
            )
        
        if resp is not None:
            if es_regular:
                respuestas.append(opciones.index(resp) + 1)
            else:
                respuestas.append(opciones_invertidas.index(resp) + 1)
        else:
            respuestas.append(None)
