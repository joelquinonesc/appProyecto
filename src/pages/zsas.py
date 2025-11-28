"""
Escala de Ansiedad de Zung (ZSAS)
"""
import streamlit as st
from ..utils.calculos import calcular_nivel_zsas
from ..utils.dataframe_manager import mostrar_dataframe_actual, agregar_o_actualizar_registro

def mostrar_zsas():
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
        "<h1 style='text-align: center; color: #2E2E2E; font-size: 2rem; font-weight: 700;'>😟 Escala de Ansiedad de Zung (ZSAS)</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align: center; color: #2E2E2E; font-size: 1.25rem; font-weight: 600; margin-bottom: 2rem;'>Evaluación detallada de síntomas de ansiedad</h3>",
        unsafe_allow_html=True
    )
    
    # Texto explicativo
    st.markdown("""
    <div style="background: #FFFFFF; padding: 1.25rem; margin: 0.75rem 0 1.5rem 0; border-radius: 8px; border: 1px solid #E0E0E0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <h4 style="color: #2E2E2E; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">
        ¿Por qué evaluamos la ansiedad con la Escala de Zung?
        </h4>
        <p style="color: #2E2E2E; font-size: 1rem; line-height: 1.7; text-align: justify; margin-bottom: 0.75rem;">
        La <strong>Escala de Ansiedad de Zung (ZSAS)</strong> es una herramienta ampliamente utilizada que evalúa 
        tanto los aspectos afectivos como somáticos de la ansiedad. Con 20 ítems, proporciona una evaluación 
        comprensiva de síntomas físicos y emocionales de la ansiedad.
        </p>
        <p style="color: #2E2E2E; font-size: 1rem; line-height: 1.7; text-align: justify; margin: 0;">
        Esta escala nos ayuda a identificar la severidad de sus síntomas ansiosos y a establecer un índice 
        cuantificable de ansiedad.
        </p>
        <p style="color: #666666; font-style: italic; text-align: center; margin-top: 1rem; margin-bottom: 0.5rem; font-size: 1.05rem;">
        <strong>⚠️ Todas las preguntas son obligatorias</strong><br>Responda pensando en la última semana
        </p>
        <p style="color: #888888; font-size: 0.9rem; text-align: center; margin: 0.5rem 0 0 0;">
        <em>Zung, W. W. (1971). A rating instrument for anxiety disorders. Psychosomatics, 12(6), 371-379.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Lista completa de preguntas ZSAS con sus respuestas
    respuestas = []
    
    # Mostrar todas las preguntas en orden
    _mostrar_todas_preguntas(respuestas)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Filtrar respuestas válidas (no None)
        respuestas_validas = [r for r in respuestas if r is not None]
        if len(respuestas_validas) < 20:  # Total de preguntas en ZSAS
            st.error("❗ Por favor, responde todas las preguntas antes de continuar.")
            disabled = True
        else:
            st.success("✅ Has completado todas las preguntas!")
            disabled = False
    
    with col2:
        if st.button("Siguiente →", key="btn_zsas_next", type="primary", disabled=disabled, width='stretch'):
            # Asegurarse de que todas las respuestas sean válidas
            respuestas_validas = [r for r in respuestas if r is not None]
            total = sum(respuestas_validas)
            total_normalizado = total * 1.25
            nivel = calcular_nivel_zsas(total_normalizado)

            # Mostrar resultados en tarjeta
            st.markdown(
                """
            <div style="background: #FFFFFF; padding: 2rem; border-radius: 12px; box-shadow: 0 3px 12px rgba(0,0,0,0.08); border: 1px solid #D1D1D1; margin: 1.5rem 0;">
            """,
                unsafe_allow_html=True,
            )

            st.markdown(
                "<h3 style='color: #2E2E2E; text-align: center; margin-bottom: 1.5rem;'>📊 Resultados ZSAS - Ansiedad de Zung</h3>",
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Puntaje bruto", value=total)
            with col2:
                st.metric(label="Índice de ansiedad", value=f"{total_normalizado:.1f}")

            st.markdown(
                f"""
            <div style='margin-top: 1rem; padding: 1rem; background: #F0F0F0; border-radius: 8px; text-align: center;'>
                <p style='color: #2E2E2E; margin: 0; font-size: 1.1rem;'><strong>Resultado:</strong> <span style='color: #4CAF50; font-weight: 700;'>{nivel}</span></p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown("</div>", unsafe_allow_html=True)

            # Guardar resultados en session state
            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}

            st.session_state.resultados['zsas'] = {
                'total': total,
                'total_normalizado': total_normalizado,
                'nivel': nivel,
            }

            # Guardar en DataFrame
            agregar_o_actualizar_registro({'puntaje_normalizado': total_normalizado}, tipo_datos='zsas')

            # Cambiar a la página de datos genéticos
            st.session_state.pagina_actual = "Datos Genéticos"
            st.rerun()

            return total, total_normalizado, nivel
    # Mostrar DataFrame actual para monitoreo
    st.markdown("---")
    with st.expander("Ver DataFrame completo"):
        mostrar_dataframe_actual()

    return None

def _mostrar_todas_preguntas(respuestas):
    """Muestra todas las preguntas del ZSAS en orden del 1 al 20"""
    
    # Definir todas las preguntas en orden con su tipo (True=regular, False=invertida)
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
    
    for pregunta, es_regular in preguntas_ordenadas:
        # Extraer el número de la pregunta
        numero = pregunta.split('.')[0]
        texto = pregunta.split('. ', 1)[1]
        
        st.markdown(f"<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem; margin-top: 1.5rem;'><span style='color: #4CAF50; font-weight: 700;'>{numero}.</span> {texto}</p>", unsafe_allow_html=True)
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
