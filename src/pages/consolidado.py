import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# Funciones de clasificación
# -----------------------------
def calcular_clasificacion_educacion(anios):
    try:
        a = int(anios)
    except Exception:
        return None
    return 0 if a <= 14 else 1


def calcular_grupo_LTE(respuestas):
    """
    respuestas: iterable de 12 elementos. Cada elemento puede ser:
      - 'Sí' / 'No'
      - True/False
      - 1/0
    Retorna: 0,1,2 según reglas
    """
    if respuestas is None:
        return None
    puntaje = 0
    for r in respuestas:
        if r is None:
            continue
        if isinstance(r, str):
            val = 1 if r.strip().lower() in ['sí','si','s','yes','y','1'] else 0
        elif isinstance(r, bool):
            val = 1 if r else 0
        else:
            try:
                val = 1 if int(r) != 0 else 0
            except Exception:
                val = 0
        puntaje += val

    if puntaje == 0:
        return 0
    if puntaje == 1:
        return 1
    return 2


def calcular_SF12_fisica(puntaje_total):
    """
    Clasificación por cuartiles para componente física:
    Q1 <= 15
    Q2 <= 17
    Q3 <= 19
    Q4 >= 20
    """
    try:
        p = float(puntaje_total)
    except Exception:
        return None
    if p <= 15:
        return 'Q1'
    if p <= 17:
        return 'Q2'
    if p <= 19:
        return 'Q3'
    return 'Q4'


def calcular_SF12_mental(puntaje_total):
    """
    Clasificación por cuartiles para componente mental:
    Q1 <= 15
    Q2 <= 18
    Q3 <= 21
    Q4 >= 22
    """
    try:
        p = float(puntaje_total)
    except Exception:
        return None
    if p <= 15:
        return 'Q1'
    if p <= 18:
        return 'Q2'
    if p <= 21:
        return 'Q3'
    return 'Q4'


# -----------------------------
# Inicializar DataFrame en session_state
# -----------------------------
def inicializar_data():
    if 'data' not in st.session_state:
        cols = [
            'timestamp',
            # demograficos / educacion
            'años_educacion',
            'clasificacion_educacion',
            # LTE-12
            'lte12_puntaje',
            'grupo_LTE',
            # SF-12 (fisica)
            'sf12_fisica_puntaje',
            'clasificacion_fisica',
            # SF-12 (mental)
            'sf12_mental_puntaje',
            'clasificacion_mental'
        ]
        st.session_state['data'] = pd.DataFrame(columns=cols)


inicializar_data()

st.title("Consolidado: Educación / LTE-12 / SF-12")
st.write("Completa cada formulario; cada envío agrega una fila al DataFrame mostrado al final.")

# -----------------------------
# Formulario 1: Clasificación años educación
# -----------------------------
with st.form("form_educacion", clear_on_submit=False):
    st.subheader("1) Años de educación formal")
    años = st.number_input("Años de educación", min_value=0, max_value=100, step=1, key="input_anios_educ")
    submitted = st.form_submit_button("Guardar educación")
    if submitted:
        clas = calcular_clasificacion_educacion(años)
        row = {
            'timestamp': datetime.now().isoformat(),
            'años_educacion': int(años),
            'clasificacion_educacion': clas,
            'lte12_puntaje': None,
            'grupo_LTE': None,
            'sf12_fisica_puntaje': None,
            'clasificacion_fisica': None,
            'sf12_mental_puntaje': None,
            'clasificacion_mental': None
        }
        st.session_state['data'] = pd.concat([st.session_state['data'], pd.DataFrame([row])], ignore_index=True)
        st.success("Registro de educación agregado.")

# -----------------------------
# Formulario 2: LTE-12
# -----------------------------
with st.form("form_lte12", clear_on_submit=False):
    st.subheader("2) LTE-12 — Eventos estresantes (12 preguntas)")
    cols = st.columns(3)
    lte_answers = []
    for i in range(12):
        col = cols[i % 3]
        with col:
            ans = st.radio(f"{i+1}. ¿Evento {i+1}?", ("No", "Sí"), index=0, key=f"lte_q_{i}")
            lte_answers.append(ans)
    submitted_lte = st.form_submit_button("Guardar LTE-12")
    if submitted_lte:
        puntaje = sum(1 if (str(x).strip().lower() in ['sí','si','s','yes','1']) else 0 for x in lte_answers)
        grupo = calcular_grupo_LTE(lte_answers)
        row = {
            'timestamp': datetime.now().isoformat(),
            'años_educacion': None,
            'clasificacion_educacion': None,
            'lte12_puntaje': int(puntaje),
            'grupo_LTE': int(grupo),
            'sf12_fisica_puntaje': None,
            'clasificacion_fisica': None,
            'sf12_mental_puntaje': None,
            'clasificacion_mental': None
        }
        st.session_state['data'] = pd.concat([st.session_state['data'], pd.DataFrame([row])], ignore_index=True)
        st.success("Registro LTE-12 agregado.")

# -----------------------------
# Formulario 3: SF-12 (Física y Mental) - simplificado
# -----------------------------
with st.form("form_sf12", clear_on_submit=False):
    st.subheader("3) SF-12 — Respuestas (simplificado)")

    st.markdown("Responde la sección física (valores enteros).")
    colA, colB = st.columns(2)
    with colA:
        sf_f_1 = st.number_input("F1", min_value=1, max_value=5, value=1, key="sf_f_1")
        sf_f_2 = st.number_input("F2", min_value=1, max_value=5, value=1, key="sf_f_2")
        sf_f_3 = st.number_input("F3", min_value=1, max_value=5, value=1, key="sf_f_3")
    with colB:
        sf_f_4 = st.number_input("F4", min_value=1, max_value=5, value=1, key="sf_f_4")
        sf_f_5 = st.number_input("F5", min_value=1, max_value=5, value=1, key="sf_f_5")
        sf_f_6 = st.number_input("F6", min_value=1, max_value=5, value=1, key="sf_f_6")

    st.markdown("Responde la sección mental (valores enteros).")
    colC, colD = st.columns(2)
    with colC:
        sf_m_1 = st.number_input("M1", min_value=1, max_value=6, value=1, key="sf_m_1")
        sf_m_2 = st.number_input("M2", min_value=1, max_value=6, value=1, key="sf_m_2")
        sf_m_3 = st.number_input("M3", min_value=1, max_value=6, value=1, key="sf_m_3")
    with colD:
        sf_m_4 = st.number_input("M4", min_value=1, max_value=6, value=1, key="sf_m_4")
        sf_m_5 = st.number_input("M5", min_value=1, max_value=6, value=1, key="sf_m_5")
        sf_m_6 = st.number_input("M6", min_value=1, max_value=6, value=1, key="sf_m_6")

    submitted_sf12 = st.form_submit_button("Guardar SF-12")
    if submitted_sf12:
        total_fisica = sum([sf_f_1, sf_f_2, sf_f_3, sf_f_4, sf_f_5, sf_f_6])
        total_mental = sum([sf_m_1, sf_m_2, sf_m_3, sf_m_4, sf_m_5, sf_m_6])
        clas_fis = calcular_SF12_fisica(total_fisica)
        clas_men = calcular_SF12_mental(total_mental)
        row = {
            'timestamp': datetime.now().isoformat(),
            'años_educacion': None,
            'clasificacion_educacion': None,
            'lte12_puntaje': None,
            'grupo_LTE': None,
            'sf12_fisica_puntaje': int(total_fisica),
            'clasificacion_fisica': clas_fis,
            'sf12_mental_puntaje': int(total_mental),
            'clasificacion_mental': clas_men
        }
        st.session_state['data'] = pd.concat([st.session_state['data'], pd.DataFrame([row])], ignore_index=True)
        st.success("Registro SF-12 agregado.")

st.markdown("---")
st.subheader("DataFrame consolidado")
df = st.session_state['data']
st.dataframe(df.fillna(''))

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Descargar CSV", data=csv, file_name=f"consolidado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")
