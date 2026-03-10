"""
Sección de Datos Genéticos
"""
import streamlit as st
from src.utils.dataframe_manager import mostrar_dataframe_actual, agregar_o_actualizar_registro, obtener_registro_actual

def mostrar_datos_geneticos():
    # --- Cargar estilos CSS globales ---
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Page header
    st.markdown("""
    <div class="anxrisk-page-header">
        <h1>Datos Genéticos</h1>
        <p>Información genética relacionada con la predisposición a la ansiedad</p>
    </div>
    """, unsafe_allow_html=True)

    # Context card
    st.markdown("""
    <div class="anxrisk-card">
        <h3>¿Por qué evaluamos factores genéticos?</h3>
        <p style="margin-bottom: 0.75rem;">
            Los <strong>factores genéticos</strong> juegan un papel importante en la predisposición a trastornos de ansiedad.
            Estudios científicos han identificado varios genes asociados con una mayor vulnerabilidad a la ansiedad, incluyendo
            <strong><em>PRKCA</em>, <em>TCF4</em> y <em>CDH20</em></strong>.
        </p>
        <p style="margin-bottom: 0.75rem;">
            Esta información genética, combinada con los cuestionarios clínicos, nos permite realizar una evaluación más
            completa y personalizada del riesgo de ansiedad según el modelo de diátesis-estrés.
        </p>
        <p style="font-size: 0.9375rem; color: var(--text-secondary); font-style: italic; text-align: center; margin-bottom: 0;">
            <strong>⚠️ Todos los genotipos son obligatorios</strong> — Seleccione el genotipo correspondiente para cada gen
        </p>
    </div>
    """, unsafe_allow_html=True)

    # PRKCA
    st.markdown("""
    <div class="anxrisk-question-card section-hads" style="border-left: 3px solid var(--genetic);">
        <div class="anxrisk-question-number" style="background: var(--genetic); color: white;">Gen PRKCA</div>
        <div class="anxrisk-question-text"><em>PRKCA</em> — Proteína Quinasa C Alfa</div>
        <p style="color: var(--text-secondary); font-size: 0.9375rem; font-style: italic; margin: 0;">Relacionada con la regulación del estrés y la respuesta emocional</p>
    </div>
    """, unsafe_allow_html=True)
    prkca_genotipo = st.selectbox(
        "Seleccione el genotipo para PRKCA:",
        options=["Seleccione una opción", "T/T", "C/T", "C/C"],
        key="prkca_select",
        label_visibility="collapsed"
    )
    
    # TCF4
    st.markdown("""
    <div class="anxrisk-question-card section-hads" style="border-left: 3px solid var(--genetic);">
        <div class="anxrisk-question-number" style="background: var(--genetic); color: white;">Gen TCF4</div>
        <div class="anxrisk-question-text"><em>TCF4</em> — Factor de Transcripción 4</div>
        <p style="color: var(--text-secondary); font-size: 0.9375rem; font-style: italic; margin: 0;">Implicado en el desarrollo neuronal y predisposición a trastornos psiquiátricos</p>
    </div>
    """, unsafe_allow_html=True)
    tcf4_genotipo = st.selectbox(
        "Seleccione el genotipo para TCF4:",
        options=["Seleccione una opción", "A/A", "A/T", "T/T"],
        key="tcf4_select",
        label_visibility="collapsed"
    )
    
    # CDH20
    st.markdown("""
    <div class="anxrisk-question-card section-hads" style="border-left: 3px solid var(--genetic);">
        <div class="anxrisk-question-number" style="background: var(--genetic); color: white;">Gen CDH20</div>
        <div class="anxrisk-question-text"><em>CDH20</em> — Cadherina 20</div>
        <p style="color: var(--text-secondary); font-size: 0.9375rem; font-style: italic; margin: 0;">Asociada con la conectividad neuronal y neurotransmisión</p>
    </div>
    """, unsafe_allow_html=True)
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
