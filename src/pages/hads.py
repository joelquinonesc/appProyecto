"""
Escala HADS de Ansiedad
"""
import streamlit as st
from ..utils.calculos import calcular_nivel_hads
from ..utils.dataframe_manager import mostrar_dataframe_actual, agregar_o_actualizar_registro

def mostrar_hads():
    # --- Cargar estilos CSS globales ---
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Estilos específicos para radio buttons con texto negro
    st.markdown("""
    <style>
    /* Color negro para las opciones de radio button */
    .stRadio label {
        color: #2E2E2E !important;
    }
    .stRadio div[role="radiogroup"] label {
        color: #2E2E2E !important;
    }
    .stRadio div[role="radiogroup"] label p {
        color: #2E2E2E !important;
        font-weight: 500 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Título centrado y en negro
    st.markdown(
        "<h1 style='text-align: center; color: #2E2E2E; font-size: 2rem; font-weight: 700;'>😰 Escala HADS de Ansiedad</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align: center; color: #2E2E2E; font-size: 1.25rem; font-weight: 600; margin-bottom: 2rem;'>Evaluación de síntomas de ansiedad en la última semana</h3>",
        unsafe_allow_html=True
    )
    
    # Texto explicativo
    st.markdown("""
    <div style="background: #FFFFFF; padding: 1.25rem; margin: 0.75rem 0 1.5rem 0; border-radius: 8px; border: 1px solid #E0E0E0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <h4 style="color: #2E2E2E; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">
        ¿Por qué evaluamos la ansiedad con HADS?
        </h4>
        <p style="color: #2E2E2E; font-size: 1rem; line-height: 1.7; text-align: justify; margin-bottom: 0.75rem;">
        La <strong>Escala HADS (Hospital Anxiety and Depression Scale)</strong> es una herramienta clínica validada 
        internacionalmente que evalúa la presencia y severidad de síntomas de ansiedad. Esta escala se enfoca en 
        manifestaciones emocionales y psicológicas de la ansiedad, complementando otras evaluaciones.
        </p>
        <p style="color: #2E2E2E; font-size: 1rem; line-height: 1.7; text-align: justify; margin: 0;">
        Los resultados nos ayudan a comprender la intensidad de sus síntomas ansiosos y su impacto en su vida diaria.
        </p>
        <p style="color: #666666; font-style: italic; text-align: center; margin-top: 1rem; margin-bottom: 0.5rem; font-size: 1.05rem;">
        <strong>⚠️ Todas las preguntas son obligatorias</strong><br>Responda pensando en la última semana
        </p>
        <p style="color: #888888; font-size: 0.9rem; text-align: center; margin: 0.5rem 0 0 0;">
        <em>Zigmond, A. S., & Snaith, R. P. (1983). The hospital anxiety and depression scale. Acta Psychiatrica Scandinavica, 67(6), 361-370.</em>
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
    for pregunta, opciones in preguntas_hads.items():
        contador += 1
        st.markdown(f"<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem; margin-top: 1.5rem;'><span style='color: #4CAF50; font-weight: 700;'>{contador}.</span> {pregunta.split('. ', 1)[1]}</p>", unsafe_allow_html=True)
        resp = st.radio(
            pregunta,
            opciones,
            key=f"hads_{pregunta[:10]}",
            horizontal=True,
            label_visibility="collapsed",
            index=None
        )
        # Las preguntas están ordenadas de 0 a 3 puntos en orden ascendente
        if resp is not None:
            respuestas.append(opciones.index(resp))
        else:
            respuestas.append(None)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Asegurarse de que no haya respuestas None (la longitud puede ser igual si se añadieron None)
        if any(r is None for r in respuestas) or len(respuestas) < len(preguntas_hads):
            st.error("❗ Por favor, responde todas las preguntas antes de continuar.")
            disabled = True
        else:
            st.success("✅ Has completado todas las preguntas!")
            disabled = False
    
    with col2:
        if st.button("Siguiente →", key="btn_hads_next", type="primary", disabled=disabled, width='stretch'):
            total = sum(respuestas)
            nivel = calcular_nivel_hads(total)

            # Mostrar resultados en tarjeta
            st.markdown(
                """
            <div style="background: #FFFFFF; padding: 2rem; border-radius: 12px; box-shadow: 0 3px 12px rgba(0,0,0,0.08); border: 1px solid #D1D1D1; margin: 1.5rem 0;">
            """,
                unsafe_allow_html=True,
            )

            st.markdown(
                "<h3 style='color: #2E2E2E; text-align: center; margin-bottom: 1.5rem;'>📊 Resultados HADS - Ansiedad</h3>",
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Puntaje total", value=total)
            with col2:
                st.metric(label="Nivel de ansiedad", value=nivel)

            # Determinar riesgo basado en umbral de 8
            riesgo_text = "⚠️ Riesgo de Ansiedad" if total >= 8 else "✅ Riesgo Bajo"
            riesgo_color = "#F44336" if total >= 8 else "#4CAF50"
            
            st.markdown(
                f"""
            <div style='margin-top: 1.5rem; padding: 1rem; background: #F5F8FB; border-radius: 8px; border-left: 4px solid {riesgo_color};'>
                <p style='color: {riesgo_color}; margin: 0; font-weight: 700; font-size: 1.1rem;'>{riesgo_text}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)

            # Guardar resultados en session state
            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}
            st.session_state.resultados['hads'] = {
                'puntaje': total,
                'nivel': nivel,
                'respuestas': respuestas,
            }

            # Guardar en DataFrame
            agregar_o_actualizar_registro({'ansiedad': total, 'depresion': None}, tipo_datos='hads')

            # Cambiar a la siguiente sección
            st.session_state.pagina_actual = "Ansiedad (ZSAS)"
            st.rerun()

            return total, nivel
    # Mostrar DataFrame actual para monitoreo
    st.markdown("---")
    with st.expander("Ver DataFrame completo"):
        mostrar_dataframe_actual()

    return None
