"""
Página de inicio de la aplicación
"""
import streamlit as st
import base64

def mostrar_home():
    # --- Cargar estilos CSS globales ---
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # --- Estilos personalizados para la página Home ---
    st.markdown("""
    <style>
        /* Fondo con efecto limewash y degradado moderno */
        .stApp {
            background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 25%, #A5D6A7 50%, #81C784 75%, #66BB6A 100%);
            background-attachment: fixed;
            min-height: 100vh;
        }
        
        /* Capa de textura limewash */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(76,175,80,0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 80%, rgba(255,255,255,0.05) 0%, transparent 40%);
            pointer-events: none;
            z-index: -1;
        }
        
        /* Contenedor principal */
        .main-container {
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            margin: 30px auto;
            max-width: 900px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.8);
        }
        
        /* Logo section enhancement */
        .logo-section {
            margin: 20px 0 30px 0;
            animation: fadeInDown 0.8s ease-out;
        }
        
        .logo-section img {
            max-width: 200px;
            height: auto;
            filter: drop-shadow(0 10px 20px rgba(76, 175, 80, 0.2));
            transition: transform 0.3s ease;
        }
        
        .logo-section img:hover {
            transform: translateY(-5px);
        }
        
        /* Título welcome */
        .welcome-title {
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #388E3C 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 30px 0 20px 0;
            text-align: center;
            font-size: 1.8rem;
            font-weight: 600;
        }
        
        /* Texto welcome */
        .welcome-text {
            font-size: 1.05rem;
            line-height: 1.9;
            color: #2E2E2E;
            text-align: justify;
            margin: 25px 0;
            max-width: 100%;
        }
        
        .welcome-text p {
            margin: 0;
            padding: 0;
        }
        
        .animate-fade-in {
            animation: fadeIn 0.8s ease-in-out;
        }
        
        /* Buttons enhancement */
        .stButton > button {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%) !important;
            border: none !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 12px 30px !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.5) !important;
        }
        
        /* Features grid */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        
        .info-card {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(165, 214, 167, 0.1) 100%);
            border: 2px solid rgba(76, 175, 80, 0.3);
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        }
        
        .info-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 30px rgba(76, 175, 80, 0.2);
            border-color: #4CAF50;
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(165, 214, 167, 0.15) 100%);
        }
        
        .info-card h4 {
            color: #1B5E20;
            font-size: 1.3rem;
            margin-bottom: 10px;
        }
        
        .info-card p {
            color: #2E7D32;
            font-size: 0.95rem;
        }
        
        /* Confidentiality note */
        .confidentiality-note {
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.15) 0%, rgba(165, 214, 167, 0.1) 100%);
            border-left: 5px solid #4CAF50;
            border-radius: 8px;
            padding: 20px;
            margin-top: 40px;
            text-align: center;
            color: #1B5E20;
        }
        
        .confidentiality-note p {
            margin: 8px 0;
            font-size: 0.95rem;
        }
        
        /* Animaciones */
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Responsivo */
        @media (max-width: 768px) {
            .main-container {
                padding: 20px;
                margin: 15px;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Logo centrado ---
    with open("src/assets/img/logo.png", "rb") as f:
        logo_data = base64.b64encode(f.read()).decode()
    
    st.markdown(f'''
    <div class="main-container">
        <div class="logo-section">
            <img src="data:image/png;base64,{logo_data}" alt="AnxRisk Logo">
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Título de bienvenida
    st.markdown(
        "<h2 style='text-align: center; background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #388E3C 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>Bienvenido a nuestra herramienta de análisis integral para la evaluación del riesgo de ansiedad.</h2>",
        unsafe_allow_html=True
    )

    # Texto de bienvenida
    st.markdown(
        "<p style='font-size: 1.25rem; line-height: 1.8; text-align: justify;'>Esta aplicación combina datos demográficos, psicosociales, clínicos y marcadores genéticos específicos para proporcionar una evaluación personalizada de su perfil de riesgo. Los trastornos de ansiedad afectan a millones de personas en todo el mundo. Según la OMS, más de mil millones viven con trastornos de salud mental, siendo la ansiedad uno de los más frecuentes. Detectar tempranamente el riesgo permite intervenir antes de que los síntomas afecten la calidad de vida.</p>",
        unsafe_allow_html=True
    )

    # --- Datos del psiquiatra que valida ---
    st.markdown("---")
    st.markdown(
        "<h4 style='text-align:center; color:#2E2E2E; margin-bottom:.5rem;'>"
        "🩺 Datos del Psiquiatra que Valida</h4>",
        unsafe_allow_html=True,
    )
    pc1, pc2 = st.columns(2)
    with pc1:
        psiq_nombre = st.text_input(
            "Nombre completo del psiquiatra *",
            value=st.session_state.get('psiquiatra_nombre', ''),
            key="input_psiq_nombre",
            placeholder="Ej: Dr. Juan Pérez",
        )
    with pc2:
        psiq_cedula = st.text_input(
            "Cédula profesional *",
            value=st.session_state.get('psiquiatra_cedula', ''),
            key="input_psiq_cedula",
            placeholder="Ej: 12345678",
        )

    # Botón principal centrado
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Empezar Análisis ➜", key="start_button", width='stretch'):
            if not psiq_nombre.strip() or not psiq_cedula.strip():
                st.error("⚠️ Ingrese el nombre y la cédula profesional del psiquiatra para continuar.")
            else:
                st.session_state['psiquiatra_nombre'] = psiq_nombre.strip()
                st.session_state['psiquiatra_cedula'] = psiq_cedula.strip()
                st.session_state.pagina_actual = "Datos demograficos"
                st.rerun()
    
    # Botón de análisis masivo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📊 Análisis Masivo (CSV)", key="batch_button", width='stretch'):
            st.session_state.pagina_actual = "Análisis Masivo"
            st.rerun()
    
    # Botón de ayuda/guía de uso
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📖 Ver Guía de Uso", key="guide_button", width='stretch'):
            st.session_state.mostrar_guia = True
            st.rerun()
    
    # Mostrar guía en una sección expandible
    if st.session_state.get('mostrar_guia', False):
        with st.expander("📖 Guía de Uso - ANXRISK (Click para cerrar)", expanded=True):
            st.markdown("""
            ### 1. Introducción a la Aplicación
            ANXRISK es una herramienta integral que evalúa tu riesgo de ansiedad combinando múltiples fuentes de datos:
            - **Datos demográficos:** Edad, género, educación
            - **Datos psicosociales:** Eventos vitales estresantes
            - **Datos clínicos:** Cuestionarios validados de ansiedad y salud
            - **Datos genéticos:** Marcadores genéticos asociados a la ansiedad
            
            ⚠️ **Nota:** Esta herramienta proporciona un análisis preliminar y debe ser interpretada por profesionales de la salud mental.
            
            ### 2. Paso a Paso de la Evaluación
            
            **Paso 1: Datos Demográficos**
            1. Ingresa tu nombre completo
            2. Proporciona tu edad (entre 1 y 120 años)
            3. Selecciona tu género (Masculino/Femenino)
            4. Indica tus años de educación formal
            
            ⚠️ **Restricción de Educación:** El máximo de años de educación permitido es tu edad menos 5 años. Por ejemplo, a los 20 años, máximo 15 años de educación.
            
            **Paso 2: Eventos Vitales (LTE-12)**
            Indica si has experimentado recientemente alguno de estos 12 eventos estresantes:
            - Muerte de un ser querido
            - Ruptura de relación importante
            - Pérdida o cambio de trabajo
            - Problemas financieros serios
            - Diagnóstico de enfermedad grave
            - Y más...
            
            ✓ **Tip:** Piensa en los últimos 6-12 meses al responder estas preguntas.
            
            *Escala validada epidemiológicamente:* Brugha, T., Bebbington, P., Tennant, C., & Hurry, J. (1985). The List of Threatening Experiences: a subset of 12 life event categories with considerable long-term contextual threat. Psychological Medicine, 15(1), 189-194.
            
            **Paso 3: SF-12 - Salud Física**
            Evalúa tu percepción de salud física respondiendo sobre:
            - Estado general de salud
            - Limitaciones en actividades físicas
            - Problemas de salud en trabajo/actividades
            - Dolor corporal y energía
            
            *Escala validada internacionalmente:* Ware, J. E., Kosinski, M., & Keller, S. D. (1996). A 12-item short-form health survey: construction of scales and preliminary tests of reliability and validity. Medical Care, 34(3), 220-233.
            
            **Paso 4: SF-12 - Salud Mental**
            Evalúa tu bienestar emocional respondiendo sobre:
            - Estado emocional general
            - Vitalidad y energía mental
            - Limitaciones emocionales en actividades
            - Salud mental percibida
            
            *Escala validada internacionalmente:* Ware, J. E., Kosinski, M., & Keller, S. D. (1996). A 12-item short-form health survey: construction of scales and preliminary tests of reliability and validity. Medical Care, 34(3), 220-233.
            
            **Paso 5: HADS - Escala de Ansiedad**
            Responde 7 preguntas sobre síntomas de ansiedad de los últimos 7 días. La escala mide:
            - Tensión y nerviosismo
            - Preocupaciones
            - Miedo y pánico
            
            *Escala validada clínicamente:* Zigmond, A. S., & Snaith, R. P. (1983). The hospital anxiety and depression scale. Acta Psychiatrica Scandinavica, 67(6), 361-370.
            
            **Paso 6: ZSAS - Escala de Zung**
            Contesta 20 preguntas sobre síntomas ansiosos. Esta escala evalúa:
            - Síntomas afectivos (emocionales)
            - Síntomas somáticos (físicos)
            
            *Escala ampliamente utilizada y validada:* Zung, W. W. (1971). A rating instrument for anxiety disorders. Psychosomatics, 12(6), 371-379.
            
            **Paso 7: Datos Genéticos**
            Indica si tienes antecedentes genéticos en los siguientes marcadores asociados a ansiedad:
            - **Gen *PRKCA*:** Relacionado con la regulación emocional
            - **Gen *TCF4*:** Asociado con predisposición a trastornos psiquiátricos
            - **Gen *CDH20*:** Vinculado con neurotransmisores y comportamiento
            
            ### 3. Interpretación de Resultados
            
            **¿Qué es SHAP y por qué se utiliza?**
            
            SHAP (SHapley Additive exPlanations) es un método matemático que explica cómo cada factor contribuye a tu predicción de riesgo de ansiedad. Es como un "desglose detallado" que muestra qué preguntas y características fueron más importantes en el resultado final.
            
            **¿Por qué es importante?** La mayoría de herramientas de inteligencia artificial actúan como "cajas negras" - te dan un resultado pero no te explican por qué. SHAP cambia esto: te permite ver exactamente qué factores subieron o bajaron tu riesgo, dándote transparencia y comprensión sobre el resultado.
            
            **¿Cómo interpretar los gráficos SHAP?**
            - **Barras hacia la derecha (rojo):** Factores que AUMENTARON tu riesgo de ansiedad
            - **Barras hacia la izquierda (verde):** Factores que DISMINUYERON tu riesgo de ansiedad
            - **Tamaño de la barra:** Qué tan importante fue cada factor (barras más largas = mayor impacto)
            - **Base:** El valor inicial de riesgo (promedio de la población)
            - **Resultado final:** El riesgo predicho después de considerar todos los factores
            
            **Ejemplo:**
            Si tu gráfico SHAP muestra:
            - Barra roja grande para "síntomas ansiosos altos (HADS)" → Esto aumentó significativamente tu riesgo
            - Barra verde pequeña para "buena salud mental (SF-12)" → Esto redujo un poco tu riesgo
            - El riesgo final es MODERADO → Significa que los factores de riesgo pesan más que los protectores
            
            **¿Qué información se usa para calcular SHAP?**
            El modelo usa información de:
            - Tu edad, género y educación
            - Eventos vitales estresantes (LTE-12)
            - Síntomas de ansiedad (HADS y ZSAS)
            - Salud física y mental percibida (SF-12)
            - Marcadores genéticos (*PRKCA*, *TCF4*, *CDH20*)
            
            Luego, SHAP calcula cuánto cada uno de estos contribuyó a tu predicción final.
            
            **Escala de Riesgo del Modelo**
            | Nivel de Riesgo | Rango de Puntuación | Descripción |
            |---|---|---|
            | **Bajo** | 0.00 - 0.29 | Bajo riesgo de trastorno de ansiedad |
            | **Moderado** | 0.30 - 0.59 | Riesgo moderado; se recomienda monitoreo |
            | **Alto** | 0.60 - 1.00 | Riesgo alto; se recomienda evaluación profesional |
            
            **HADS y ZSAS**
            | Escala | Puntuación Bajo Riesgo | Puntuación Alto Riesgo |
            |---|---|---|
            | HADS | < 8 | ≥ 8 |
            | ZSAS | < 36 | ≥ 36 |
            
            **SF-12**
            El SF-12 se interpreta por cuartiles (Q1-Q4):
            - **Q1 (Muy Baja):** Limitaciones significativas en salud
            - **Q2 (Baja):** Salud por debajo del promedio
            - **Q3 (Moderada):** Salud en nivel intermedio
            - **Q4 (Excelente):** Muy buen nivel de salud
            
            ### 4. Exportar Resultados
            Al finalizar la evaluación, puedes descargar un reporte HTML con todos tus resultados:
            1. Completa todos los cuestionarios
            2. Ve a la sección de Resultados
            3. Haz clic en "Descargar Reporte HTML"
            4. Opcionalmente, convierte el HTML a PDF usando tu navegador (Archivo → Imprimir → Guardar como PDF)
            
            ### 5. Privacidad y Confidencialidad
            🔒 **Seguridad de Datos:** Todos tus datos son confidenciales y se utilizan exclusivamente con fines investigativos. Esta herramienta está destinada a la investigación y debe ser interpretada por profesionales de la salud.
            
            ### 6. Preguntas Frecuentes
            
            **¿Cuánto tiempo toma completar la evaluación?**
            Generalmente entre 20-30 minutos, dependiendo de la velocidad de lectura y respuesta.
            
            **¿Puedo pausar y continuar después?**
            Sí, tus datos se guardan automáticamente al completar cada sección. Puedes volver a cualquier momento.
            
            **¿Qué significa "riesgo moderado"?**
            Significa que existen factores presentes que sugieren un riesgo moderado de ansiedad. Se recomienda monitoreo continuo y posible consulta con un profesional de salud mental.
            
            **¿Los genes definen si tendré ansiedad?**
            No. Los genes son solo un factor de riesgo. La ansiedad resulta de la interacción entre factores genéticos, ambientales, psicosociales y clínicos.
            
            **¿Puede reemplazar una evaluación profesional?**
            No. Esta herramienta es de apoyo y debe complementarse con una evaluación profesional de un psicólogo o psiquiatra.
            """)
            
            if st.button("Cerrar Guía", key="close_guide"):
                st.session_state.mostrar_guia = False
                st.rerun()
    
    # Espaciado antes de las tarjetas
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

    # Características principales
    st.markdown('<div class="features-grid">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>Evaluación Integral</h4>
            <p>Cuestionarios clínicos validados</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>🧬 Análisis Genético</h4>
            <p>Basado en marcadores <i>PRKCA</i>, <i>TCF4</i> y <i>CDH20</i></p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <h4>Resultados Detallados</h4>
            <p>Reporte personalizado con interpretación</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

   

    # Nota final de confidencialidad
    st.markdown("""
    <div class="confidentiality-note">
        <p>Sus datos son confidenciales y utilizados exclusivamente con fines investigativos.</p>
        <p>Esta herramienta está destinada a la investigación y debe ser interpretada por profesionales de la salud.</p>
    </div>
    """, unsafe_allow_html=True)
