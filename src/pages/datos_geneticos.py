"""
Sección de Datos Genéticos
"""
import streamlit as st
from src.utils.dataframe_manager import mostrar_dataframe_actual, agregar_o_actualizar_registro, obtener_registro_actual

def mostrar_datos_geneticos():
    # --- Cargar estilos CSS globales ---
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Estilos específicos para selectbox con texto negro
    st.markdown("""
    <style>
    /* Color negro para las opciones de selectbox */
    .stSelectbox label {
        color: #2E2E2E !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        color: #2E2E2E !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Título centrado y en negro
    st.markdown(
        "<h1 style='text-align: center; color: #2E2E2E; font-size: 2rem; font-weight: 700;'> Datos Genéticos</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align: center; color: #2E2E2E; font-size: 1.25rem; font-weight: 600; margin-bottom: 2rem;'>Información genética relacionada con la ansiedad</h3>",
        unsafe_allow_html=True
    )
    
    # Texto explicativo
    st.markdown("""
    <div style="background: #FFFFFF; padding: 1.25rem; margin: 0.75rem 0 1.5rem 0; border-radius: 8px; border: 1px solid #E0E0E0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <h4 style="color: #2E2E2E; font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; text-align: center;">
        ¿Por qué evaluamos factores genéticos?
        </h4>
        <p style="color: #2E2E2E; font-size: 1rem; line-height: 1.7; text-align: justify; margin-bottom: 0.75rem;">
        Los <strong>factores genéticos</strong> juegan un papel importante en la predisposición a trastornos de ansiedad. 
        Estudios científicos han identificado varios genes asociados con una mayor vulnerabilidad a la ansiedad, incluyendo 
        <strong>PRKCA, TCF4 y CDH20</strong>.
        </p>
        <p style="color: #2E2E2E; font-size: 1rem; line-height: 1.7; text-align: justify; margin: 0;">
        Esta información genética, combinada con los cuestionarios clínicos, nos permite realizar una evaluación más 
        completa y personalizada del riesgo de ansiedad según el modelo de diátesis-estrés.
        </p>
        <p style="color: #666666; font-style: italic; text-align: center; margin-top: 1rem; margin-bottom: 0; font-size: 1.05rem;">
        <strong>⚠️ Todos los genotipos son obligatorios</strong><br>Seleccione el genotipo correspondiente para cada gen
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sección de Genes
    st.markdown("<h3 style='color: #4CAF50; font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1rem 0; border-bottom: 2px solid #E0E0E0; padding-bottom: 0.5rem;'>Selección de Genotipos</h3>", unsafe_allow_html=True)
    
    # PRKCA
    st.markdown("<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem; margin-top: 1.5rem;'><span style='color: #4CAF50; font-weight: 700;'>Gen PRKCA</span></p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666666; font-size: 0.95rem; font-style: italic; margin-bottom: 0.75rem;'>Proteína quinasa C alfa - relacionada con la regulación del estrés</p>", unsafe_allow_html=True)
    prkca_genotipo = st.selectbox(
        "Seleccione el genotipo para PRKCA:",
        options=["Seleccione una opción", "T/T", "C/T", "C/C"],
        key="prkca_select",
        label_visibility="collapsed"
    )
    
    # TCF4
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem;'><span style='color: #4CAF50; font-weight: 700;'>Gen TCF4</span></p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666666; font-size: 0.95rem; font-style: italic; margin-bottom: 0.75rem;'>Factor de transcripción 4 - implicado en el desarrollo neuronal</p>", unsafe_allow_html=True)
    tcf4_genotipo = st.selectbox(
        "Seleccione el genotipo para TCF4:",
        options=["Seleccione una opción", "A/A", "A/T", "T/T"],
        key="tcf4_select",
        label_visibility="collapsed"
    )
    
    # CDH20
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #2E2E2E; font-size: 1.5rem; font-weight: 500; margin-bottom: 0.75rem;'><span style='color: #4CAF50; font-weight: 700;'>Gen CDH20</span></p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666666; font-size: 0.95rem; font-style: italic; margin-bottom: 0.75rem;'>Cadherina 20 - asociada con la conectividad neuronal</p>", unsafe_allow_html=True)
    cdh20_genotipo = st.selectbox(
        "Seleccione el genotipo para CDH20:",
        options=["Seleccione una opción", "G/G", "G/A", "A/A"],
        key="cdh20_select",
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Verificar si todos los datos están completos
    genotipos_validos = (
        prkca_genotipo != "Seleccione una opción" and
        tcf4_genotipo != "Seleccione una opción" and
        cdh20_genotipo != "Seleccione una opción"
    )
    
    # Verificar si todos los cuestionarios anteriores están completos
    cuestionarios_requeridos = ['hads', 'zsas']
    cuestionarios_completos = all(cuest in st.session_state.get('resultados', {}) for cuest in cuestionarios_requeridos)
    
    # Mostrar estado de validación
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if not genotipos_validos:
            st.error("❗ Por favor, seleccione todos los genotipos antes de continuar.")
        elif not cuestionarios_completos:
            faltantes = [c for c in cuestionarios_requeridos if c not in st.session_state.get('resultados', {})]
            st.warning(f"⚠️ Asegúrese de haber completado HADS y ZSAS. Faltan: {', '.join(faltantes)}")
        else:
            st.success("✅ Todos los datos están completos. ¡Puede calcular el riesgo de ansiedad!")
    
    with col2:
        # Botón deshabilitado si faltan datos
        disabled = not (genotipos_validos and cuestionarios_completos)
    
    # Mostrar el DataFrame actual también en el formulario de selección de genotipos (opcional, quitar si no se quiere)
    # st.markdown("---")
    # with st.expander("Ver DataFrame actual"):
    #     mostrar_dataframe_actual()
        
        if st.button("Ver Resultados →", key="btn_calcular_riesgo", type="primary", disabled=disabled, use_container_width=True):
            # Guardar los datos genéticos
            if 'resultados' not in st.session_state:
                st.session_state.resultados = {}
            
            st.session_state.resultados['datos_geneticos'] = {
                'prkca': prkca_genotipo,
                'tcf4': tcf4_genotipo,
                'cdh20': cdh20_genotipo
            }

            # Guardar en DataFrame
            agregar_o_actualizar_registro({
                'prkca': prkca_genotipo,
                'tcf4': tcf4_genotipo,
                'cdh20': cdh20_genotipo
            }, tipo_datos='geneticos')
            
            # Redirigir a la página de resultados
            st.session_state.pagina_actual = 'resultados'
            st.rerun()
    
    return None
