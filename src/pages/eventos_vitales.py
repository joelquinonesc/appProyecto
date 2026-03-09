"""
Cuestionario de Eventos Vitales (LTE-12)
"""
import streamlit as st
from src.utils.dataframe_manager import agregar_o_actualizar_registro
from src.utils.calculos import transformar_lte12_a_clasificacion

def mostrar_eventos_vitales():
    # Page header
    st.markdown("""
    <div class="anxrisk-page-header">
        <h1>Eventos Vitales Estresantes (LTE-12)</h1>
        <p>Evalúa experiencias recientes con impacto potencial en la salud mental</p>
    </div>
    """, unsafe_allow_html=True)

    # Context card
    st.markdown("""
    <div class="anxrisk-card">
        <h3>Contexto clínico</h3>
        <p style="margin-bottom: 0.75rem;">
            Los eventos estresantes recientes pueden precipitar o agravar síntomas de ansiedad,
            según el modelo <strong>diathesis-stress</strong>. Evaluarlos ayuda a personalizar
            intervenciones y prevenir cronificación.
        </p>
        <p style="margin-bottom: 0.75rem;">
            La <strong>Lista de Experiencias Amenazantes (LTE-12)</strong> mide 12 eventos
            comunes con impacto a largo plazo.
        </p>
        <p style="font-size: 0.9375rem; color: var(--text-secondary); margin-bottom: 0.5rem; font-style: italic; text-align: center;">
            Todas las preguntas son obligatorias — Seleccione "Sí" para los eventos experimentados recientemente
        </p>
        <p style="font-size: 0.875rem; color: var(--text-secondary); text-align: center; margin: 0;">
            Brugha, T., Bebbington, P., Tennant, C., & Hurry, J. (1985). <em>Psychological Medicine</em>, 15(1), 189-194.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    preguntas = [
        "¿Ha sufrido usted mismo(a) una enfermedad, lesión o agresión grave?",
        "¿Algún familiar cercano ha sufrido una enfermedad, lesión o agresión grave?",
        "¿Ha muerto uno de sus padres, hijos o su pareja/cónyuge?",
        "¿Ha muerto un amigo cercano a la familia o algún otro familiar?",
        "¿Se ha separado a causa de problemas en su matrimonio?",
        "¿Ha roto una relación estable?",
        "¿Ha tenido un problema grave con algún amigo cercano, vecino o familiar?",
        "¿Se ha quedado sin empleo o ha buscado empleo durante más de un mes sin éxito?",
        "¿Le han despedido de su trabajo?",
        "¿Ha tenido una crisis económica grave?",
        "¿Ha tenido problemas con la policía o ha comparecido ante un tribunal?",
        "¿Le han robado o ha perdido algún objeto de valor?"
    ]
    
    respuestas = []
    
    for i in range(len(preguntas)):
        if f"ev_pregunta_{i}" not in st.session_state:
            st.session_state[f"ev_pregunta_{i}"] = None
    
    for i, pregunta in enumerate(preguntas):
        st.markdown(f"""
        <div class="anxrisk-question-card">
            <div class="anxrisk-question-number">Pregunta {i+1} de {len(preguntas)}</div>
            <div class="anxrisk-question-text">{pregunta}</div>
        </div>
        """, unsafe_allow_html=True)
        
        _, col_radio, _ = st.columns([1, 2, 1])
        with col_radio:
            respuesta = st.radio(
                f"Pregunta {i+1}",
                options=["No", "Sí"],
                key=f"ev_pregunta_{i}",
                horizontal=True,
                index=None,
                label_visibility="collapsed"
            )
        
        if respuesta is not None:
            respuestas.append(1 if respuesta == "Sí" else 0)
        else:
            respuestas.append(None)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    respuestas_validas = [r for r in respuestas if r is not None]
    total = sum(respuestas_validas)
    todas_respondidas = len(respuestas_validas) == len(preguntas)
    
    with col1:
        if not todas_respondidas:
            st.error("Responda todas las preguntas antes de continuar.")
            disabled = True
        else:
            st.success("Todas las preguntas completadas")
            disabled = False
    
    with col2:
        if st.button("Siguiente", key="btn_eventos_next", type="primary", disabled=disabled, use_container_width=True):
            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}
            st.session_state.resultados['eventos_vitales'] = {
                'total': total,
                'respuestas': respuestas,
                'clasificacion': transformar_lte12_a_clasificacion(total),
            }
            agregar_o_actualizar_registro(
                {'puntaje_total': total, 'lte12_clasificacion': transformar_lte12_a_clasificacion(total)},
                tipo_datos='eventos_vitales',
            )
            st.session_state.pagina_actual = "SF-12 Física"
            st.rerun()
            return total

    return None
