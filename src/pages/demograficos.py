"""
Formulario de Datos Demográficos
"""
import streamlit as st
from ..utils.calculos import (
    transformar_edad_a_grupo,
    transformar_genero_a_binario,
    transformar_educacion_a_binaria,
)
from ..utils.dataframe_manager import agregar_o_actualizar_registro


def mostrar_demograficos():
    """Muestra y gestiona el formulario de datos demográficos."""

    # CSS general
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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

        _METRIC_CARD = """
        <div style="background:#FFF; padding:1rem 1.25rem; border-radius:8px;
                    border-left:3px solid #2B87D1; margin-bottom:0.75rem;
                    box-shadow:0 1px 4px rgba(0,0,0,.06);">
            <p style="color:#666; margin:0 0 0.25rem; font-size:0.85rem;
                      font-family:'Source Sans 3','Source Sans Pro',sans-serif;">{label}</p>
            <p style="color:#2E2E2E; margin:0; font-size:1.4rem; font-weight:700;
                      font-family:'Source Sans 3','Source Sans Pro',sans-serif;">{value}</p>
        </div>
        """

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(_METRIC_CARD.format(label="Nombre", value=datos['nombre']), unsafe_allow_html=True)
            st.markdown(_METRIC_CARD.format(label="Documento", value=datos.get('documento', '—')), unsafe_allow_html=True)
            st.markdown(_METRIC_CARD.format(label="Edad", value=f"{datos['edad']} años"), unsafe_allow_html=True)
        with col2:
            st.markdown(_METRIC_CARD.format(label="Género", value=datos['genero']), unsafe_allow_html=True)
            st.markdown(_METRIC_CARD.format(label="Educación", value=f"{datos['años_educacion']} años"), unsafe_allow_html=True)

        # Mostrar datos del profesional evaluador si fueron ingresados
        prof_nombre = st.session_state.get('_prof_nombre', '') or st.session_state.get('prof_nombre', '')
        prof_cargo = st.session_state.get('_prof_cargo', '') or st.session_state.get('prof_cargo', '')
        prof_institucion = st.session_state.get('_prof_institucion', '') or st.session_state.get('prof_institucion', '')
        prof_tp = st.session_state.get('_prof_tp', '') or st.session_state.get('prof_tp', '')
        if any([prof_nombre, prof_cargo, prof_institucion, prof_tp]):
            st.markdown("<h4 style='color:#2B87D1; font-size:1.2rem; margin-top:1.5rem; font-family:\"Source Sans 3\",sans-serif;'>👨‍⚕️ Profesional Evaluador</h4>", unsafe_allow_html=True)
            pcol1, pcol2 = st.columns(2)
            with pcol1:
                if prof_nombre:
                    st.markdown(_METRIC_CARD.format(label="Profesional", value=prof_nombre), unsafe_allow_html=True)
                if prof_cargo:
                    st.markdown(_METRIC_CARD.format(label="Cargo / Especialidad", value=prof_cargo), unsafe_allow_html=True)
            with pcol2:
                if prof_institucion:
                    st.markdown(_METRIC_CARD.format(label="Institución", value=prof_institucion), unsafe_allow_html=True)
                if prof_tp:
                    st.markdown(_METRIC_CARD.format(label="Tarjeta Profesional", value=prof_tp), unsafe_allow_html=True)

        st.markdown("---")

        col_edit, col_next = st.columns(2)
        with col_edit:
            if st.button("Editar datos"):
                st.session_state["datos_demograficos"] = None
                # Restaurar datos del profesional a las keys de widget para que aparezcan pre-llenados
                st.session_state["prof_nombre"] = st.session_state.get("_prof_nombre", "")
                st.session_state["prof_cargo"] = st.session_state.get("_prof_cargo", "")
                st.session_state["prof_institucion"] = st.session_state.get("_prof_institucion", "")
                st.session_state["prof_tp"] = st.session_state.get("_prof_tp", "")
                st.rerun()
        with col_next:
            if st.button("Siguiente", key="demo_next", type="primary"):
                st.session_state.pagina_actual = "LTE-12"
                st.rerun()

        return datos

    # ── FORMULARIO ──
    st.markdown("#### Complete la información del paciente:")

    nombre = st.text_input("Nombre completo", placeholder="Nombre completo del paciente *", key="nombre_completo")
    documento = st.text_input("Documento de identidad", placeholder="Número de documento del paciente *", key="documento_paciente")

    col1, col2 = st.columns(2)
    with col1:
        edad = st.number_input(
            "Edad *", min_value=0, max_value=120, step=1,
            value=None, placeholder="Ingrese la edad",
            help="Debe ser mayor a 0", key="edad",
        )
    with col2:
        genero = st.selectbox("Género *", ["Seleccionar", "Masculino", "Femenino"], key="genero")

    max_educacion = max(0, (edad or 0) - 5)

    if edad is None or edad < 5:
        años_educacion = st.number_input(
            "Años de educación formal *", min_value=0, max_value=0,
            value=None, disabled=True, placeholder="—",
            help="Ingrese primero la edad del paciente", key="educacion",
        )
    else:
        if "educacion" in st.session_state and (st.session_state.get("educacion") or 0) > max_educacion:
            st.session_state["educacion"] = max_educacion
        años_educacion = st.number_input(
            "Años de educación formal *", min_value=0, max_value=max_educacion,
            value=None, step=1, placeholder="Ingrese los años",
            help=f"Máximo permitido: {max_educacion} años (edad − 5)", key="educacion",
        )

    # ── DATOS DEL PROFESIONAL EVALUADOR ──
    st.markdown("---")
    st.markdown("""
    <div class="anxrisk-card" style="border-left: 4px solid var(--primary);">
        <h3>👨‍⚕️ Datos del Profesional Evaluador</h3>
        <p style="font-size: 0.9375rem; color: var(--text-secondary); margin-bottom: 0.75rem;">
            Complete estos datos para que aparezcan en el reporte PDF con espacio para su firma.
        </p>
    </div>
    """, unsafe_allow_html=True)

    prof_col1, prof_col2 = st.columns(2)
    with prof_col1:
        prof_nombre = st.text_input(
            "Nombre del profesional", key="prof_nombre",
            placeholder="Dr(a). Nombre Apellido",
        )
        prof_cargo = st.text_input(
            "Cargo / Especialidad", key="prof_cargo",
            placeholder="Psiquiatra / Psicólogo clínico",
        )
    with prof_col2:
        prof_institucion = st.text_input(
            "Institución", key="prof_institucion",
            placeholder="Hospital / Consultorio / IPS",
        )
        prof_tp = st.text_input(
            "Tarjeta Profesional", key="prof_tp",
            placeholder="TP-XXXXX",
        )

    # Botón de guardar
    guardar = st.button("Guardar datos", type="primary")

    if guardar:
        errores = []
        if not nombre.strip():
            errores.append("El nombre completo es obligatorio.")
        if not documento.strip():
            errores.append("El documento de identidad es obligatorio.")
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
            "documento": documento,
            "edad": edad,
            "grupo_edad": transformar_edad_a_grupo(edad),
            "genero": transformar_genero_a_binario(genero),
            "años_educacion": años_educacion,
            "educacion_binaria": transformar_educacion_a_binaria(años_educacion),
        }

        st.session_state["datos_demograficos"] = datos

        # Guardar datos del profesional en claves persistentes
        # (las keys de widget se eliminan cuando el widget deja de renderizarse)
        st.session_state["_prof_nombre"] = st.session_state.get("prof_nombre", "")
        st.session_state["_prof_cargo"] = st.session_state.get("prof_cargo", "")
        st.session_state["_prof_institucion"] = st.session_state.get("prof_institucion", "")
        st.session_state["_prof_tp"] = st.session_state.get("prof_tp", "")

        agregar_o_actualizar_registro(datos, tipo_datos="demograficos")
        st.success("✅ Datos guardados correctamente")
        st.rerun()

    return None
