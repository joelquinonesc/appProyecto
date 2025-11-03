"""
Gestor de DataFrame dinámico para almacenar datos de pacientes
"""
import pandas as pd
import streamlit as st
from datetime import datetime
from src.utils.calculos import transformar_edad_a_grupo


def inicializar_dataframe():
    """
    Inicializa el DataFrame en session_state si no existe
    """
    if 'df_pacientes' not in st.session_state:
        st.session_state['df_pacientes'] = pd.DataFrame(columns=[
            'timestamp',
            'nombre',
            'edad',
            'grupo_edad',
            'genero',
            'genero_binario',
            'años_educacion',
            'lte12_puntaje',
            'sf12_fisica',
            'sf12_mental',
            'hads_ansiedad',
            'hads_depresion',
            'zsas_puntaje',
            'gen_prkca',
            'gen_tcf4',
            'gen_cdh20'
        ])


def agregar_o_actualizar_registro(datos, tipo_datos='demograficos'):
    """
    Agrega o actualiza un registro en el DataFrame
    
    Args:
        datos (dict): Datos a agregar/actualizar
        tipo_datos (str): Tipo de datos ('demograficos', 'eventos', 'sf12', etc.)
    """
    inicializar_dataframe()
    
    df = st.session_state['df_pacientes']
    
    # Buscar si ya existe un registro para esta sesión
    # Usamos el timestamp de inicio de sesión como identificador
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    session_id = st.session_state['session_id']
    
    # Buscar índice del registro actual
    if 'registro_index' not in st.session_state:
        # Crear nuevo registro
        nuevo_registro = {
            'timestamp': session_id,
            'nombre': None,
            'edad': None,
            'grupo_edad': None,
            'genero': None,
            'genero_binario': None,
            'años_educacion': None,
            'lte12_puntaje': None,
            'sf12_fisica': None,
            'sf12_mental': None,
            'hads_ansiedad': None,
            'hads_depresion': None,
            'zsas_puntaje': None,
            'gen_prkca': None,
            'gen_tcf4': None,
            'gen_cdh20': None
        }
        st.session_state['df_pacientes'] = pd.concat(
            [df, pd.DataFrame([nuevo_registro])], 
            ignore_index=True
        )
        st.session_state['registro_index'] = len(st.session_state['df_pacientes']) - 1
    
    idx = st.session_state['registro_index']
    
    # Actualizar datos según el tipo
    if tipo_datos == 'demograficos':
        st.session_state['df_pacientes'].at[idx, 'nombre'] = datos.get('nombre')
        st.session_state['df_pacientes'].at[idx, 'edad'] = datos.get('edad')
        st.session_state['df_pacientes'].at[idx, 'grupo_edad'] = datos.get('grupo_edad')
        st.session_state['df_pacientes'].at[idx, 'genero'] = datos.get('genero')
        st.session_state['df_pacientes'].at[idx, 'genero_binario'] = datos.get('genero_binario')
        st.session_state['df_pacientes'].at[idx, 'años_educacion'] = datos.get('años_educacion')
    
    elif tipo_datos == 'eventos_vitales':
        st.session_state['df_pacientes'].at[idx, 'lte12_puntaje'] = datos.get('puntaje_total')
    
    elif tipo_datos == 'sf12':
        st.session_state['df_pacientes'].at[idx, 'sf12_fisica'] = datos.get('salud_fisica')
        st.session_state['df_pacientes'].at[idx, 'sf12_mental'] = datos.get('salud_mental')
    
    elif tipo_datos == 'hads':
        st.session_state['df_pacientes'].at[idx, 'hads_ansiedad'] = datos.get('ansiedad')
        st.session_state['df_pacientes'].at[idx, 'hads_depresion'] = datos.get('depresion')
    
    elif tipo_datos == 'zsas':
        st.session_state['df_pacientes'].at[idx, 'zsas_puntaje'] = datos.get('puntaje_normalizado')
    
    elif tipo_datos == 'geneticos':
        st.session_state['df_pacientes'].at[idx, 'gen_prkca'] = datos.get('prkca')
        st.session_state['df_pacientes'].at[idx, 'gen_tcf4'] = datos.get('tcf4')
        st.session_state['df_pacientes'].at[idx, 'gen_cdh20'] = datos.get('cdh20')


def obtener_dataframe():
    """
    Retorna el DataFrame completo
    """
    inicializar_dataframe()
    return st.session_state['df_pacientes']


def obtener_registro_actual():
    """
    Retorna el registro actual del paciente
    """
    inicializar_dataframe()
    
    if 'registro_index' in st.session_state:
        idx = st.session_state['registro_index']
        return st.session_state['df_pacientes'].iloc[idx].to_dict()
    return None


def exportar_dataframe_csv():
    """
    Exporta el DataFrame a CSV
    """
    df = obtener_dataframe()
    return df.to_csv(index=False).encode('utf-8')


def mostrar_dataframe_actual():
    """
    Muestra el DataFrame actual en la interfaz
    """
    df = obtener_dataframe()
    
    if len(df) > 0:
        st.subheader("📊 Datos Recolectados")
        st.dataframe(df, use_container_width=True)
        
        # Botón de descarga
        csv = exportar_dataframe_csv()
        st.download_button(
            label="⬇️ Descargar datos (CSV)",
            data=csv,
            file_name=f"datos_pacientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No hay datos recolectados aún")


def obtener_estadisticas():
    """
    Retorna estadísticas del DataFrame
    """
    df = obtener_dataframe()
    
    if len(df) == 0:
        return None
    
    stats = {
        'total_registros': len(df),
        'registros_completos': df.dropna().shape[0],
        'edad_promedio': df['edad'].mean() if df['edad'].notna().any() else None,
        'distribucion_grupos': df['grupo_edad'].value_counts().to_dict() if df['grupo_edad'].notna().any() else None,
        'completitud': {
            'demograficos': df[['nombre', 'edad', 'genero', 'años_educacion']].notna().all(axis=1).sum(),
            'eventos_vitales': df['lte12_puntaje'].notna().sum(),
            'sf12': df[['sf12_fisica', 'sf12_mental']].notna().all(axis=1).sum(),
            'hads': df[['hads_ansiedad', 'hads_depresion']].notna().all(axis=1).sum(),
            'zsas': df['zsas_puntaje'].notna().sum(),
            'geneticos': df[['gen_prkca', 'gen_tcf4', 'gen_cdh20']].notna().all(axis=1).sum()
        }
    }
    
    return stats
