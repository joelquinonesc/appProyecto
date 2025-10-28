"""
Cuestionario SF-12 de Salud Física y Mental
"""
import streamlit as st
from ..utils.calculos import calcular_sf12

def mostrar_sf12():
    # --- Cargar estilos CSS globales ---
    with open("src/assets/styles/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Estilos específicos para radio buttons y select sliders con texto negro
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
    /* Color negro para select slider */
    .stSlider label {
        color: #2E2E2E !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Título centrado y en negro
    st.markdown(
        "<h1 style='text-align: center; color: #2E2E2E; font-size: 2rem; font-weight: 700;'>📋 Cuestionario SF-12 de Salud</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align: center; color: #2E2E2E; font-size: 1.25rem; font-weight: 600; margin-bottom: 2rem;'>Evaluación de salud física y mental en las últimas 4 semanas</h3>",
        unsafe_allow_html=True
    )
    
    # Texto explicativo
    st.markdown("""
    <div style="background: #FFFFFF; padding: 1.25rem; margin: 0.75rem 0 1.5rem 0; border-radius: 8px; border: 1px solid #E0E0E0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <h4 style="color: #2E2E2E; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">
        ¿Por qué evaluamos su salud física y mental?
        </h4>
        <p style="color: #2E2E2E; font-size: 1rem; line-height: 1.7; text-align: justify; margin-bottom: 0.75rem;">
        El <strong>SF-12 (Short Form-12)</strong> es un cuestionario validado internacionalmente que evalúa cómo la salud 
        física y mental impacta en su vida diaria. La salud general está relacionada con la ansiedad: problemas físicos 
        crónicos pueden aumentar el estrés, y la ansiedad puede manifestarse como síntomas físicos.
        </p>
        <p style="color: #2E2E2E; font-size: 1rem; line-height: 1.7; text-align: justify; margin: 0;">
        Esta evaluación nos ayuda a entender su estado de salud global y cómo puede estar influyendo en su bienestar emocional.
        </p>
        <p style="color: #666666; font-style: italic; text-align: center; margin-top: 1rem; margin-bottom: 0; font-size: 1.05rem;">
        <strong>⚠️ Todas las preguntas son obligatorias</strong><br>Responda pensando en las últimas 4 semanas
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    respuestas = []
    
    # Sección 1: Estado de Salud General
    _mostrar_seccion_salud_general(respuestas)
    
    # Sección 2: Limitaciones Físicas
    _mostrar_seccion_limitaciones(respuestas)
    
    # Sección 3: Problemas Recientes
    _mostrar_seccion_problemas(respuestas)
    
    # Sección 4: Estado Emocional
    _mostrar_seccion_emocional(respuestas)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if len(respuestas) < 12:
            st.error("❗ Por favor, responde todas las preguntas antes de continuar.")
            disabled = True
        else:
            st.success("✅ Has completado todas las preguntas!")
            disabled = False
    
    with col2:
        if st.button("Siguiente →", key="btn_sf12_next", type="primary", disabled=disabled, use_container_width=True):
            total = calcular_sf12(respuestas)
            mensaje = "mejor" if total > 50 else "menor"
            
            # Mostrar resultados en tarjeta
            st.markdown("""
            <div style="background: #FFFFFF; padding: 2rem; border-radius: 12px; box-shadow: 0 3px 12px rgba(0,0,0,0.08); border: 1px solid #D1D1D1; margin: 1.5rem 0;">
            """, unsafe_allow_html=True)
            
            st.markdown("<h3 style='color: #2E2E2E; text-align: center; margin-bottom: 1.5rem;'>📊 Resultados SF-12</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Puntaje total", value=f"{total:.1f}")
            with col2:
                st.markdown(f"<p style='color: #2E2E2E; font-size: 1rem; line-height: 2;'><em>Su salud está {mensaje} que el promedio</em></p>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style='margin-top: 1rem; padding: 1rem; background: #F5F8FB; border-radius: 8px; border-left: 4px solid #2B87D1;'>
                <p style='color: #2E2E2E; margin: 0.5rem 0;'><strong>Interpretación:</strong></p>
                <ul style='color: #2E2E2E; margin: 0.5rem 0;'>
                    <li>Un puntaje mayor a 50 indica una salud mejor que el promedio</li>
                    <li>Un puntaje menor a 50 indica una salud por debajo del promedio</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Guardar resultados en session state
            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}
            st.session_state.resultados['sf12'] = {
                'puntaje': total,
                'respuestas': respuestas
            }
            
            # Cambiar a la siguiente sección
            st.session_state.pagina_actual = "Ansiedad (HADS)"
            st.rerun()
            
            return total
    return None

def _mostrar_seccion_salud_general(respuestas):
    st.markdown("<h3 style='color: #4CAF50; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1rem 0; border-bottom: 2px solid #E0E0E0; padding-bottom: 0.5rem;'>1️⃣ Estado de Salud General</h3>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem; margin-top: 1rem;'><span style='color: #4CAF50; font-weight: 700;'>1.</span> En general, ¿diría que su salud es?</p>", unsafe_allow_html=True)
    
    opciones_salud = ["Seleccione una opción", "Excelente", "Muy buena", "Buena", "Regular", "Mala"]
    resp = st.selectbox(
        "Pregunta 1",
        options=opciones_salud,
        key="sf12_salud",
        label_visibility="collapsed"
    )
    # La puntuación se invierte: Excelente=1, Mala=5
    if resp != "Seleccione una opción":
        respuestas.append(opciones_salud.index(resp))  # index ya da 1-5 porque añadimos opción inicial
    else:
        respuestas.append(None)  # No se ha seleccionado

def _mostrar_seccion_limitaciones(respuestas):
    st.markdown("<hr style='margin: 2rem 0; border: none; height: 2px; background: #E0E0E0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #4CAF50; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1rem 0; border-bottom: 2px solid #E0E0E0; padding-bottom: 0.5rem;'>2️⃣ Limitaciones en Actividades</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666666; font-style: italic; margin-bottom: 1.5rem; font-size: 1.05rem;'>Las siguientes preguntas se refieren a actividades o cosas que usted podría hacer en un día normal. Su salud actual, ¿le limita para hacer esas actividades o cosas? Si es así, ¿cuánto?</p>", unsafe_allow_html=True)
    
    # Pregunta 2
    st.markdown("<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem; margin-top: 1rem;'><span style='color: #4CAF50; font-weight: 700;'>2.</span> Esfuerzos moderados, como mover una mesa, pasar la aspiradora, jugar a los bolos o caminar más de 1 hora</p>", unsafe_allow_html=True)
    resp = st.radio(
        "Pregunta 2",
        ["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"],
        key="sf12_lim_mod",
        horizontal=True,
        label_visibility="collapsed",
        index=None
    )
    if resp is not None:
        respuestas.append(["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"].index(resp) + 1)
    else:
        respuestas.append(None)
    
    # Pregunta 3
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem;'><span style='color: #4CAF50; font-weight: 700;'>3.</span> Subir varios pisos por la escalera</p>", unsafe_allow_html=True)
    resp = st.radio(
        "Pregunta 3",
        ["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"],
        key="sf12_lim_esc",
        horizontal=True,
        label_visibility="collapsed",
        index=None
    )
    if resp is not None:
        respuestas.append(["Sí, limitado mucho", "Sí, limitado un poco", "No, no limitado en absoluto"].index(resp) + 1)
    else:
        respuestas.append(None)

def _mostrar_seccion_problemas(respuestas):
    st.markdown("<hr style='margin: 2rem 0; border: none; height: 2px; background: #E0E0E0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #4CAF50; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1rem 0; border-bottom: 2px solid #E0E0E0; padding-bottom: 0.5rem;'>3️⃣ Problemas en las Últimas 4 Semanas</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666666; font-style: italic; margin-bottom: 1.5rem; font-size: 1.05rem;'><strong>Salud física:</strong> Durante las 4 últimas semanas, ¿ha tenido alguno de los siguientes problemas en su trabajo o en sus actividades cotidianas, a causa de su salud física?</p>", unsafe_allow_html=True)
    
    # Preguntas 4-5 (Problemas físicos)
    st.markdown("<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem; margin-top: 1rem;'><span style='color: #4CAF50; font-weight: 700;'>4.</span> ¿Hizo menos de lo que hubiera querido hacer?</p>", unsafe_allow_html=True)
    resp = st.radio(
        "Pregunta 4",
        ["Sí", "No"],
        key="sf12_fis_1",
        horizontal=True,
        label_visibility="collapsed",
        index=None
    )
    if resp is not None:
        respuestas.append(1 if resp == "Sí" else 2)
    else:
        respuestas.append(None)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem;'><span style='color: #4CAF50; font-weight: 700;'>5.</span> ¿Tuvo que dejar de hacer algunas tareas en su trabajo o en sus actividades cotidianas?</p>", unsafe_allow_html=True)
    resp = st.radio(
        "Pregunta 5",
        ["Sí", "No"],
        key="sf12_fis_2",
        horizontal=True,
        label_visibility="collapsed",
        index=None
    )
    if resp is not None:
        respuestas.append(1 if resp == "No" else 2)
    else:
        respuestas.append(None)
    
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # Preguntas 6-7 (Problemas emocionales)
    st.markdown("<p style='color: #666666; font-style: italic; margin-bottom: 1.5rem; font-size: 1.05rem;'><strong>Problemas emocionales:</strong> Durante las 4 últimas semanas, ¿ha tenido alguno de los siguientes problemas en su trabajo o en sus actividades cotidianas, a causa de algún problema emocional (como estar triste, deprimido, o nervioso)?</p>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem;'><span style='color: #4CAF50; font-weight: 700;'>6.</span> ¿Hizo menos de lo que hubiera querido hacer, por algún problema emocional?</p>", unsafe_allow_html=True)
    resp = st.radio(
        "Pregunta 6",
        ["Sí", "No"],
        key="sf12_emo_1",
        horizontal=True,
        label_visibility="collapsed",
        index=None
    )
    if resp is not None:
        respuestas.append(1 if resp == "Sí" else 2)
    else:
        respuestas.append(None)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem;'><span style='color: #4CAF50; font-weight: 700;'>7.</span> ¿No hizo su trabajo o sus actividades cotidianas tan cuidadosamente como de costumbre, por algún problema emocional?</p>", unsafe_allow_html=True)
    resp = st.radio(
        "Pregunta 7",
        ["Sí", "No"],
        key="sf12_emo_2",
        horizontal=True,
        label_visibility="collapsed",
        index=None
    )
    if resp is not None:
        respuestas.append(1 if resp == "Sí" else 2)
    else:
        respuestas.append(None)
    
    # Pregunta 8 (Dolor)
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem;'><span style='color: #4CAF50; font-weight: 700;'>8.</span> Durante las 4 últimas semanas, ¿hasta qué punto el dolor le ha dificultado su trabajo habitual (incluido el trabajo fuera de casa y las tareas domésticas)?</p>", unsafe_allow_html=True)
    resp_dolor = st.radio(
        "Pregunta 8",
        ["Nada", "Un poco", "Regular", "Bastante", "Mucho"],
        key="sf12_dolor",
        horizontal=True,
        label_visibility="collapsed",
        index=None
    )
    if resp_dolor is not None:
        respuestas.append(["Nada", "Un poco", "Regular", "Bastante", "Mucho"].index(resp_dolor) + 1)
    else:
        respuestas.append(None)

def _mostrar_seccion_emocional(respuestas):
    st.markdown("<hr style='margin: 2rem 0; border: none; height: 2px; background: #E0E0E0;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #4CAF50; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1rem 0; border-bottom: 2px solid #E0E0E0; padding-bottom: 0.5rem;'>4️⃣ Estado Emocional y Social</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666666; font-style: italic; margin-bottom: 1.5rem; font-size: 1.05rem;'>Las preguntas que siguen se refieren a cómo se ha sentido y cómo han marchado las cosas durante las 4 últimas semanas. En cada pregunta responda lo que se parezca más a cómo se ha sentido usted.</p>", unsafe_allow_html=True)
    
    opciones = [
        "Seleccione una opción",
        "Siempre",
        "Casi siempre",
        "Muchas veces",
        "Algunas veces",
        "Sólo una vez",
        "Nunca"
    ]
    
    # Preguntas 9-11 (Estado emocional)
    preguntas_emocionales = [
        ("9", "¿Se sintió calmado y tranquilo?", False),
        ("10", "¿Tuvo mucha energía?", False),
        ("11", "¿Se sintió desanimado y triste?", True)
    ]
    
    st.markdown("<p style='color: #666666; font-style: italic; margin-bottom: 1.5rem; font-size: 1.05rem;'>Durante las 4 últimas semanas ¿cuánto tiempo...?</p>", unsafe_allow_html=True)
    
    for num, pregunta_texto, es_negativa in preguntas_emocionales:
        st.markdown(f"<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem; margin-top: 1rem;'><span style='color: #4CAF50; font-weight: 700;'>{num}.</span> {pregunta_texto}</p>", unsafe_allow_html=True)
        resp = st.selectbox(
            f"Pregunta {num}",
            options=opciones,
            key=f"sf12_emoc_{num}",
            label_visibility="collapsed"
        )
        if resp != "Seleccione una opción":
            if es_negativa:
                respuestas.append(opciones.index(resp))  # Puntuación directa para pregunta negativa (index ya da 1-6)
            else:
                respuestas.append(7 - opciones.index(resp))  # Puntuación invertida para preguntas positivas
        else:
            respuestas.append(None)
    
    # Pregunta 12 (Actividades sociales)
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem;'><span style='color: #4CAF50; font-weight: 700;'>12.</span> Durante las 4 últimas semanas, ¿con qué frecuencia la salud física o los problemas emocionales le han dificultado sus actividades sociales (como visitar a los amigos o familiares)?</p>", unsafe_allow_html=True)
    resp = st.selectbox(
        "Pregunta 12",
        options=opciones,
        key="sf12_social",
        label_visibility="collapsed"
    )
    if resp != "Seleccione una opción":
        respuestas.append(opciones.index(resp))
    else:
        respuestas.append(None)
