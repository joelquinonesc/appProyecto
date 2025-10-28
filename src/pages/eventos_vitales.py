"""
Cuestionario de Eventos Vitales (LTE-12)
"""
import streamlit as st

def mostrar_eventos_vitales():
    # --- Cargar estilos CSS globales ---
    with open("src/assets/styles/main.css") as f:
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
        "<h1 style='text-align: center; color: #2E2E2E; font-size: 2rem; font-weight: 700;'>Evaluación de Eventos Estresantes (LTE-12)</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align: center; color: #2E2E2E; font-size: 1.25rem; font-weight: 600; margin-bottom: 2rem;'>Responde a las siguientes preguntas sobre experiencias recientes</h3>",
        unsafe_allow_html=True
    )
    
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
    
    # Texto explicativo
    st.markdown("""
    <div style="background: #FFFFFF; padding: 1.25rem; margin: 0.75rem 0 1.5rem 0; border-radius: 8px; border: 1px solid #E0E0E0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <h4 style="color: #2E2E2E; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">
        ¿Por qué evaluamos eventos estresantes?
        </h4>
        <p style="color: #2E2E2E; font-size: 1rem; line-height: 1.7; text-align: justify; margin-bottom: 0.75rem;">
        Los eventos estresantes recientes, como pérdidas, conflictos o cambios vitales, son especialmente relevantes 
        porque pueden precipitar o agravar síntomas de ansiedad, según modelos como el <strong>diathesis-stress</strong> 
        (donde una predisposición se activa por estrés). Evaluarlos ayuda a entender el contexto y personalizar 
        intervenciones, previniendo cronificación.
        </p>
        <p style="color: #2E2E2E; font-size: 1rem; line-height: 1.7; text-align: justify; margin: 0;">
        Por eso, incorporamos la <strong>Lista de Experiencias Amenazantes (LTE-12)</strong>, que mide 12 eventos 
        comunes con impacto a largo plazo.
        </p>
        <p style="color: #666666; font-style: italic; text-align: center;margin-top: 1rem; margin-bottom: 1.5rem; font-size: 1.05rem;">
        <strong>⚠️ Todas las preguntas son obligatorias</strong><br>Seleccione 'Sí' para los eventos que haya experimentado recientemente
        </p>
    </div>
    """, unsafe_allow_html=True)
    
   
    
    respuestas = []
    
    # Inicializar las keys en session_state si no existen
    for i in range(len(preguntas)):
        if f"ev_pregunta_{i}" not in st.session_state:
            st.session_state[f"ev_pregunta_{i}"] = None
    
    for i, pregunta in enumerate(preguntas):
        st.markdown(f"<p style='color: #2E2E2E; font-size: 1.5em; font-weight: 500; margin-bottom: 0.75rem; margin-top: 1rem;'><span style='color: #4CAF50; font-weight: 700;'>{i+1}.</span> {pregunta}</p>", unsafe_allow_html=True)
        
        respuesta = st.radio(
            f"Pregunta {i+1}",
            options=["No", "Sí"],
            key=f"ev_pregunta_{i}",
            horizontal=True,
            index=None,  # No hay opción preseleccionada
            label_visibility="collapsed"
        )
        
        # Solo agregar respuesta si se ha seleccionado algo
        if respuesta is not None:
            respuestas.append(1 if respuesta == "Sí" else 0)
        else:
            respuestas.append(None)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    # Contar solo respuestas válidas (no None)
    respuestas_validas = [r for r in respuestas if r is not None]
    total = sum(respuestas_validas)
    todas_respondidas = len(respuestas_validas) == len(preguntas)
    
    with col1:
        if not todas_respondidas:
            st.error("❗ Por favor, responde todas las preguntas antes de continuar.")
            disabled = True
        else:
            st.success("✅ Has completado todas las preguntas!")
            disabled = False
    
    with col2:
        if st.button("Siguiente →", key="btn_eventos_next", type="primary", disabled=disabled, use_container_width=True):
            # Mostrar resultados en tarjeta
            st.markdown("""
            <div style="background: #FFFFFF; padding: 2rem; border-radius: 12px; box-shadow: 0 3px 12px rgba(0,0,0,0.08); border: 1px solid #D1D1D1; margin: 1.5rem 0;">
            """, unsafe_allow_html=True)
            
            st.markdown("<h3 style='color: #2E2E2E; text-align: center; margin-bottom: 1.5rem;'>📊 Resultados LTE-12</h3>", unsafe_allow_html=True)
            
            st.metric(label="Total de eventos vitales experimentados", value=total)
            
            st.markdown("""
            <div style='margin-top: 1rem; padding: 1rem; background: #F5F8FB; border-radius: 8px; border-left: 4px solid #2B87D1;'>
                <p style='color: #2E2E2E; margin: 0.5rem 0;'><strong>Interpretación:</strong></p>
                <p style='color: #2E2E2E; margin: 0.5rem 0;'>Un mayor número de eventos vitales estresantes puede estar asociado con un mayor riesgo de problemas de salud mental.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Guardar resultados en session state
            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}
            st.session_state.resultados['eventos_vitales'] = {
                'total': total,
                'respuestas': respuestas
            }
            
            # Cambiar a la siguiente sección
            st.session_state.pagina_actual = "SF-12 Salud"
            st.rerun()
            
            return total
    return None
