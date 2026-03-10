"""
Formulario de Datos Demográficos
"""
import streamlit as st
from src.utils.calculos import (
    transformar_edad_a_grupo,
    transformar_genero_a_binario,
    transformar_educacion_a_binaria,
)
from src.utils.dataframe_manager import agregar_o_actualizar_registro, mostrar_dataframe_actual


def mostrar_demograficos():
    """
    Muestra y gestiona el formulario de datos demográficos.
    Retorna un diccionario con los datos del paciente o None si no están completos.
    """

    # CSS general
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Título de página
    st.markdown(
        "<h1 style='text-align: center;'>Datos Demográficos</h1>",
        unsafe_allow_html=True
    )

    # Estado inicial de sesión
    if "datos_demograficos" not in st.session_state:
        st.session_state["datos_demograficos"] = None

    # Si ya existen datos, mostrarlos
    if st.session_state["datos_demograficos"] is not None:
        datos = st.session_state["datos_demograficos"]
        st.success("Datos demográficos ya registrados")

        col1, col2 = st.columns(2)

        with col1:
            st.info(f" **Nombre:** {datos['nombre']}")
            st.info(f" **Edad:** {datos['edad']} años")

        with col2:
            st.info(f" **Género:** {datos['genero']}")
            st.info(f" **Años de educación:** {datos['años_educacion']} años")

        st.markdown("#### 🩺 Evaluador")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.info(f" **Psiquiatra:** {datos.get('nombre_psiquiatra', '—')}")
        with col_p2:
            st.info(f" **Cédula Prof.:** {datos.get('cedula_psiquiatra', '—')}")

        st.markdown("---")
        st.markdown("### Vista de Datos en DataFrame")
        with st.expander("Ver DataFrame completo"):
            mostrar_dataframe_actual()

        col_edit, col_next = st.columns(2)
        with col_edit:
            if st.button("Editar datos"):
                st.session_state["datos_demograficos"] = None
                st.rerun()

        with col_next:
            if st.button("Siguiente →"):
                st.session_state.pagina_actual = "LTE-12"
                st.rerun()

        return datos

    # -------- FORMULARIO ---------
    # Estilos locales para fondo blanco y minimalista (anulan temporalmente el tema global)
    st.markdown(
        """
        <style>
        /* Hacer el contenedor principal blanco y minimalista para esta página */
        .block-container {
            background: #ffffff !important;
            border-radius: 10px !important;
            box-shadow: 0 6px 18px rgba(0,0,0,0.06) !important;
            padding: 24px !important;
        }
        /* Etiquetas y entradas limpias */
        .stTextInput > label, .stNumberInput > label, .stSelectbox > label {
            color: #2E2E2E !important;
            font-weight: 600 !important;
        }
        /* Ocultar labels vacíos */
        .stTextInput > label:empty, .stNumberInput > label:empty {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Complete la información:")

    # Nombre (encabezando, ocupa full-width)
    nombre = st.text_input("", placeholder="Nombre completo *", key="nombre_completo")

    # Crear dos columnas para Edad / Género
    col1, col2 = st.columns(2)

    with col1:
        edad = st.number_input(
            "Edad *",
            min_value=0,
            max_value=120,
            step=1,
            value=0,
            help="Debe ser mayor a 0",
            key="edad"
        )

    with col2:
        genero = st.selectbox("Género *", ["Seleccionar", "Masculino", "Femenino"], key="genero")

    # Máximo permitido para años de educación
    max_educacion = max(0, edad - 5)

    # Años de educación (ocupa full-width debajo)
    if edad < 5:
        años_educacion = st.number_input(
            "Años de educación formal *",
            min_value=0,
            max_value=0,
            value=0,
            disabled=True,
            help="No aplica educación formal a esta edad",
            key="educacion",
        )
    else:
        # Si el usuario había ingresado antes un valor mayor al nuevo máximo, forzarlo al máximo permitido
        if "educacion" in st.session_state and st.session_state.get("educacion", 0) > max_educacion:
            st.session_state["educacion"] = max_educacion

        años_educacion = st.number_input(
            "Años de educación formal *",
            min_value=0,
            max_value=max_educacion,
            value=st.session_state.get("educacion", 0),
            step=1,
            help=f"Máximo permitido: {max_educacion} años (edad - 5)",
            key="educacion",
        )

    # ── Datos del evaluador (psiquiatra) ─────────────────────────
    st.markdown("---")
    st.markdown("#### 🩺 Datos del Evaluador")

    col_psq1, col_psq2 = st.columns(2)
    with col_psq1:
        nombre_psiquiatra = st.text_input(
            "Nombre del Psiquiatra *",
            placeholder="Nombre completo del profesional",
            key="nombre_psiquiatra",
        )
    with col_psq2:
        cedula_psiquiatra = st.text_input(
            "Cédula Profesional *",
            placeholder="Número de cédula profesional",
            key="cedula_psiquiatra",
        )

    # Validación en tiempo real y control del botón guardar
    live_errores = []
    if not nombre.strip():
        live_errores.append("El nombre completo es obligatorio")
    if genero == "Seleccionar":
        live_errores.append("Debe seleccionar un género")
    if not nombre_psiquiatra.strip():
        live_errores.append("El nombre del psiquiatra es obligatorio")
    if not cedula_psiquiatra.strip():
        live_errores.append("La cédula profesional del psiquiatra es obligatoria")
    # Solo validar educación si la edad es válida (mayor a 0)
    if edad > 0:
        if años_educacion < 0:
            live_errores.append("Los años de educación no pueden ser negativos")
        elif años_educacion > max_educacion:
            live_errores.append(f"Los años de educación ({años_educacion}) no pueden ser más de {max_educacion} años (edad - 5)")

    if live_errores:
        st.error(" No se puede guardar. Corrija los siguientes errores:")
        for e in live_errores:
            st.markdown(f"- {e}")

    # Botón de guardar (deshabilitado si hay errores en tiempo real)
    guardar = st.button("Guardar datos", disabled=bool(live_errores))

    if guardar:
        # Validaciones finales (seguridad)
        errores = []
        if not nombre.strip():
            errores.append("El nombre completo es obligatorio.")
        if genero == "Seleccionar":
            errores.append("Debe seleccionar un género.")
        if años_educacion > max_educacion:
            errores.append(f"Los años de educación no pueden ser mayores a {max_educacion}.")
        if not nombre_psiquiatra.strip():
            errores.append("El nombre del psiquiatra es obligatorio.")
        if not cedula_psiquiatra.strip():
            errores.append("La cédula profesional del psiquiatra es obligatoria.")

        if errores:
            st.error(" No se pudieron guardar los datos:")
            for e in errores:
                st.markdown(f"- {e}")
            return None

        datos = {
            "nombre": nombre,
            "edad": edad,
            "grupo_edad": transformar_edad_a_grupo(edad),
            "genero": transformar_genero_a_binario(genero),
            "años_educacion": años_educacion,
            "educacion_binaria": transformar_educacion_a_binaria(años_educacion),
            "nombre_psiquiatra": nombre_psiquiatra.strip(),
            "cedula_psiquiatra": cedula_psiquiatra.strip(),
        }

        st.session_state["datos_demograficos"] = datos
        agregar_o_actualizar_registro(datos, tipo_datos="demograficos")

        st.success(f"✅ Datos guardados correctamente")
        st.rerun()

    # Mostrar DataFrame actual en un expander para monitoreo desde el formulario
    st.markdown("---")
    with st.expander("Ver DataFrame completo"):
        mostrar_dataframe_actual()

    return None
