"""
Formulario de Datos Demográficos
"""
import streamlit as st
from src.utils.calculos import (
    transformar_edad_a_grupo,
    transformar_genero_a_binario,
    transformar_educacion_a_binaria,
)
from src.utils.dataframe_manager import agregar_o_actualizar_registro


def mostrar_demograficos():
    """Muestra y gestiona el formulario de datos demográficos."""

    # Page header
    st.markdown("""
    <div class="anxrisk-page-header">
        <h1>Datos Demográficos</h1>
        <p>Información base del paciente para la estratificación de riesgo</p>
    </div>
    """, unsafe_allow_html=True)

    # Estado inicial de sesión
    if "datos_demograficos" not in st.session_state:
        st.session_state["datos_demograficos"] = None

    # Si ya existen datos, mostrarlos
    if st.session_state["datos_demograficos"] is not None:
        datos = st.session_state["datos_demograficos"]
        st.success("Datos demográficos registrados correctamente")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Nombre", value=datos['nombre'])
            st.metric(label="Edad", value=f"{datos['edad']} años")
        with col2:
            st.metric(label="Género", value=datos['genero'])
            st.metric(label="Educación", value=f"{datos['años_educacion']} años")

        st.markdown("---")

        col_edit, col_next = st.columns(2)
        with col_edit:
            if st.button("Editar datos"):
                st.session_state["datos_demograficos"] = None
                st.rerun()
        with col_next:
            if st.button("Siguiente", key="demo_next", type="primary"):
                st.session_state.pagina_actual = "LTE-12"
                st.rerun()

        return datos

    # ── FORMULARIO ──
    st.markdown("#### Complete la información del paciente:")

    nombre = st.text_input("Nombre completo", placeholder="Nombre completo *", key="nombre_completo")

    col1, col2 = st.columns(2)
    with col1:
        edad = st.number_input("Edad *", min_value=0, max_value=120, step=1, value=None, placeholder="Ingrese la edad", help="Debe ser mayor a 0", key="edad")
    with col2:
        genero = st.selectbox("Género *", ["Seleccionar", "Masculino", "Femenino"], key="genero")

    max_educacion = max(0, (edad or 0) - 5)

    if edad is None or edad < 5:
        años_educacion = st.number_input("Años de educación formal *", min_value=0, max_value=0, value=None, disabled=True, placeholder="Ingrese los años", help="Ingrese primero la edad del paciente", key="educacion")
    else:
        if "educacion" in st.session_state and (st.session_state.get("educacion") or 0) > max_educacion:
            st.session_state["educacion"] = max_educacion
        años_educacion = st.number_input("Años de educación formal *", min_value=0, max_value=max_educacion, value=None, step=1, placeholder="Ingrese los años", help=f"Máximo permitido: {max_educacion} años (edad - 5)", key="educacion")

    # Validación solo al intentar guardar
    guardar = st.button("Guardar datos", type="primary")

    if guardar:
        errores = []
        if not nombre.strip():
            errores.append("El nombre completo es obligatorio.")
        if genero == "Seleccionar":
            errores.append("Debe seleccionar un género.")
        if edad is None or edad <= 0:
            errores.append("La edad debe ser mayor a 0.")
        if años_educacion is None:
            errores.append("Los años de educación formal son obligatorios.")
        elif años_educacion > max_educacion:
            errores.append(f"Los años de educación no pueden ser mayores a {max_educacion}.")

        if errores:
            st.error("Corrija los siguientes errores:")
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
        }

        st.session_state["datos_demograficos"] = datos
        agregar_o_actualizar_registro(datos, tipo_datos="demograficos")
        st.success("Datos guardados correctamente")
        st.rerun()

    return None
