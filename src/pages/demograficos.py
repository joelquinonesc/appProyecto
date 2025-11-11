"""
Formulario de Datos Demográficos
"""
import streamlit as st
from src.utils.calculos import transformar_edad_a_grupo, transformar_genero_a_binario
from src.utils.dataframe_manager import agregar_o_actualizar_registro, mostrar_dataframe_actual

def mostrar_demograficos():
    """
    Muestra y gestiona el formulario de datos demográficos.
    Retorna un diccionario con los datos del paciente o None si no están completos.
    """
    # --- Cargar estilos CSS globales ---
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Título centrado y en negro
    st.markdown(
        "<h1 style='text-align: center; color: #2E2E2E; font-size: 2rem; font-weight: 700;'>Datos Demográficos del Paciente</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align: center; color: #2E2E2E; font-size: 1.25rem; font-weight: 600; margin-bottom: 2rem;'>Información Personal</h3>",
        unsafe_allow_html=True
    )
    
    # Crear una clave única para la sesión si no existe
    if 'datos_demograficos' not in st.session_state:
        st.session_state['datos_demograficos'] = None
    
    # Si ya hay datos guardados, mostrarlos
    if st.session_state['datos_demograficos'] is not None:
        # Mensaje de éxito con estilo
        st.markdown("""
        <div style="background: #F5F5F5; text-align: center; font-size: 1.1rem; 
        margin-bottom: 2rem; padding: 1rem; border-radius: 8px; border-left: 5px solid #4CAF50;">
            <strong style="color: #2E2E2E;">✅ Datos demográficos ya registrados</strong>
        </div>
        """, unsafe_allow_html=True)
        
        datos = st.session_state['datos_demograficos']
        
        # Contenedor principal con fondo blanco
        
        
        st.markdown("""
        <h2 style="color: #2E2E2E; font-size: 1.75rem; font-weight: 700; text-align: center; 
        margin-bottom: 2rem; border-bottom: 2px solid #E0E0E0; padding-bottom: 1rem;">
        📋 Información del Paciente
        </h2>
        """, unsafe_allow_html=True)

        # Grid de 2 columnas para las cards
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            # Card Nombre
            st.markdown(f"""
            <div style="background: #F5F5F5; 
            padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4CAF50; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1.5rem;">
                <p style="color: #666666; font-size: 0.9rem; font-weight: 600; 
                text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">
                👤 Nombre Completo
                </p>
                <p style="color: #2E2E2E; font-size: 1.4rem; font-weight: 700; margin: 0;">
                {datos['nombre']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Card Edad
            st.markdown(f"""
            <div style="background: #F5F5F5; 
            padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4CAF50; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                <p style="color: #666666; font-size: 0.9rem; font-weight: 600; 
                text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">
                🎂 Edad
                </p>
                <p style="color: #2E2E2E; font-size: 1.4rem; font-weight: 700; margin: 0;">
                {datos['edad']} años
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Card Género
            st.markdown(f"""
            <div style="background: #F5F5F5; 
            padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4CAF50; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1.5rem;">
                <p style="color: #666666; font-size: 0.9rem; font-weight: 600; 
                text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">
                ⚧ Género
                </p>
                <p style="color: #2E2E2E; font-size: 1.4rem; font-weight: 700; margin: 0;">
                {datos['genero']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Card Educación
            st.markdown(f"""
            <div style="background: #F5F5F5; 
            padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4CAF50; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                <p style="color: #666666; font-size: 0.9rem; font-weight: 600; 
                text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;">
                🎓 Años de Educación
                </p>
                <p style="color: #2E2E2E; font-size: 1.4rem; font-weight: 700; margin: 0;">
                {datos['años_educacion']} años
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
        
        # Botones con mejor estilo
        col_edit, col_next = st.columns([1, 1], gap="medium")
        with col_edit:
            if st.button("✏️ Editar datos", key="edit_demo", use_container_width=True):
                st.session_state['datos_demograficos'] = None
                st.rerun()
        with col_next:
            if st.button("Siguiente →", type="primary", key="next_demo", use_container_width=True):
                st.session_state.pagina_actual = "LTE-12"
                st.rerun()
        
        # Mostrar DataFrame actualizado
        st.markdown("---")
        st.markdown("### 📊 Vista de Datos en DataFrame")
        with st.expander("Ver DataFrame completo", expanded=False):
            mostrar_dataframe_actual()
        
        return datos
    
    # Estilos personalizados para el campo nombre - eliminar TODO fondo gris
    st.markdown("""
    <style>
    /* Eliminar TODOS los fondos grises del campo "Nombre completo" */
    div[data-testid="stTextInput"]:has(input[id*="nombre_completo"]) label,
    div[data-testid="stTextInput"]:has(input[id*="nombre_completo"]) > div,
    div[data-testid="stTextInput"]:has(input[id*="nombre_completo"]) > div > div,
    div[data-testid="stTextInput"]:has(input[id*="nombre_completo"]) > div > div > div,
    div[data-testid="stTextInput"]:has(input[id*="nombre_completo"]) * {
        background: transparent !important;
        background-color: transparent !important;
    }
    /* Mantener el input con fondo blanco */
    div[data-testid="stTextInput"]:has(input[id*="nombre_completo"]) input {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="form-instruction">Complete la siguiente información:</p>', unsafe_allow_html=True)
    st.markdown('<div class="spacer-sm"></div>', unsafe_allow_html=True)
    
    # Formulario con campos en el orden: Nombre, Edad, Género, Educación
    with st.form("formulario_demografico"):
        # 1. Nombre completo
        nombre = st.text_input("Nombre completo", key="nombre_completo", placeholder="Ingrese su nombre completo")
        
        # 2. Edad FUERA del formulario para actualización en tiempo real
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1, key="edad_temp", help="Ingrese su edad en años")
        
        # Calcular el máximo de años de educación permitidos (ahora se actualiza en tiempo real)
        max_educacion = max(0, edad - 5) if edad > 0 else 0
        
        # Mensaje informativo sobre años de educación con texto ROJO
        if edad > 0:
            st.markdown(f"""
            <div style="padding: 1rem; background-color: #FFF3CD; border-left: 4px solid #FF6B6B; border-radius: 4px; margin: 1rem 0;">
                <p style="margin: 0; color: #DC3545; font-weight: 600; font-size: 0.95rem;">
                    ⚠️ Según tu edad ({edad} años), puedes tener un <strong>máximo de {max_educacion} años</strong> de educación formal.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="padding: 1rem; background-color: #FFF3CD; border-left: 4px solid #FF6B6B; border-radius: 4px; margin: 1rem 0;">
                <p style="margin: 0; color: #DC3545; font-weight: 600; font-size: 0.95rem;">
                    ⚠️ Por favor, ingrese primero su edad para calcular los años de educación válidos.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # 3. Género
        genero = st.selectbox(
            "Género",
            ["Seleccionar", "Masculino", "Femenino"],
            key="genero"
        )
        
        # 4. Años de educación formal
        años_educacion = st.number_input(
            "Años de educación formal",
            min_value=0,
            max_value=max_educacion if edad > 0 else 30,
            step=1,
            value=0,
            help=f"Máximo permitido: {max_educacion} años (calculado como edad - 5)",
            key="educacion"
        )
        
        # Mostrar estado de validación visualmente
        if edad > 0 and años_educacion > 0:
            if años_educacion <= max_educacion:
                st.success(f"✅ Años de educación válidos ({años_educacion}/{max_educacion})")
            else:
                st.error(f"❌ Excede el máximo permitido. Máximo: {max_educacion} años")
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        col_submit, col_space = st.columns([1, 2])
        with col_submit:
            submitted = st.form_submit_button("Guardar datos", type="primary", use_container_width=True)

        if submitted:
            # VALIDACIONES COMPLETAS - No permitir guardar si no cumplen TODAS
            errores = []
            
            # 1. Validar nombre
            if not nombre.strip():
                errores.append("El nombre completo es obligatorio")
            
            # 2. Validar edad
            if edad <= 0:
                errores.append("Debe ingresar una edad válida (mayor a 0)")
            
            # 3. Validar género
            if genero == "Seleccionar":
                errores.append("Debe seleccionar un género")
            
            # 4. Validar años de educación
            max_educacion_permitido = max(0, edad - 5)
            if años_educacion < 0:
                errores.append("Los años de educación no pueden ser negativos")
            elif años_educacion > max_educacion_permitido:
                errores.append(f"Los años de educación ({años_educacion}) no pueden ser más de {max_educacion_permitido} años (edad - 5)")
            
            # Si hay errores, mostrarlos y NO GUARDAR
            if errores:
                st.error("❌ **No se pueden guardar los datos. Corrija los siguientes errores:**")
                for error in errores:
                    st.markdown(f"- {error}")
                return None
            
            # Si todas las validaciones pasan
            grupo_edad = transformar_edad_a_grupo(edad)
            genero_binario = transformar_genero_a_binario(genero)
            
            datos = {
                "nombre": nombre,
                "edad": edad,
                "grupo_edad": grupo_edad,
                "genero": genero,
                "genero_binario": genero_binario,
                "años_educacion": años_educacion,
            }
            st.session_state['datos_demograficos'] = datos
            
            # Agregar/actualizar en el DataFrame dinámico
            agregar_o_actualizar_registro(datos, tipo_datos='demograficos')
            
            # Mensaje de éxito
            st.success(f"✅ Datos guardados correctamente para {nombre}")
            
            st.rerun()
    
    return None
