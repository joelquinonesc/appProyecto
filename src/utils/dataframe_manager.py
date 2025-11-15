"""
Gestor de DataFrame dinámico para almacenar datos de pacientes
"""
import pandas as pd
import streamlit as st
from datetime import datetime
from src.utils.calculos import transformar_edad_a_grupo, transformar_sf12_fisica_a_label, transformar_sf12_mental_a_label


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
            'educacion_binaria',
            'lte12_clasificacion',
            'sf12_fisica_cuartil',
            'sf12_fisica_cuartil_label',
            # Cuartiles para componente mental SF-12
            'sf12_mental_cuartil',
            'sf12_mental_cuartil_label',
            # Clasificación combinada HADS + ZSAS (0/1)
            'hads_zsas_clasificacion',
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
        # Sincronizar etiquetas de cuartiles SF-12 si existen puntajes numéricos previos
        sincronizar_sf12_cuartil_labels()


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
            'educacion_binaria': None,
            'lte12_clasificacion': None,
            'sf12_fisica_cuartil': None,
            'sf12_fisica_cuartil_label': None,
            'sf12_mental_cuartil': None,
            'sf12_mental_cuartil_label': None,
            'hads_zsas_clasificacion': None,
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
        st.session_state['df_pacientes'].at[idx, 'educacion_binaria'] = datos.get('educacion_binaria')
        st.session_state['df_pacientes'].at[idx, 'genero'] = datos.get('genero')
        st.session_state['df_pacientes'].at[idx, 'genero_binario'] = datos.get('genero_binario')
        st.session_state['df_pacientes'].at[idx, 'años_educacion'] = datos.get('años_educacion')
    
    elif tipo_datos == 'eventos_vitales':
        st.session_state['df_pacientes'].at[idx, 'lte12_puntaje'] = datos.get('puntaje_total')
        # Guardar clasificación LTE-12 (0,1,2)
        st.session_state['df_pacientes'].at[idx, 'lte12_clasificacion'] = datos.get('lte12_clasificacion')
    
    elif tipo_datos == 'sf12':
        st.session_state['df_pacientes'].at[idx, 'sf12_fisica'] = datos.get('salud_fisica')
        st.session_state['df_pacientes'].at[idx, 'sf12_mental'] = datos.get('salud_mental')
        # Guardar clasificación en cuartiles para la componente física si se provee (la página física debe ser quien la envie)
        if datos.get('sf12_fisica_cuartil') is not None:
            st.session_state['df_pacientes'].at[idx, 'sf12_fisica_cuartil'] = datos.get('sf12_fisica_cuartil')
        if datos.get('sf12_fisica_cuartil_label') is not None:
            st.session_state['df_pacientes'].at[idx, 'sf12_fisica_cuartil_label'] = datos.get('sf12_fisica_cuartil_label')

        # Guardar clasificación en cuartiles para la componente mental si se provee (la página mental debe ser quien la envie)
        if datos.get('sf12_mental_cuartil') is not None:
            st.session_state['df_pacientes'].at[idx, 'sf12_mental_cuartil'] = datos.get('sf12_mental_cuartil')
        if datos.get('sf12_mental_cuartil_label') is not None:
            st.session_state['df_pacientes'].at[idx, 'sf12_mental_cuartil_label'] = datos.get('sf12_mental_cuartil_label')

        # Asegurar que, si por alguna razón falta la etiqueta textual para cualquiera de las componentes,
        # la generamos a partir del valor numérico
        sincronizar_sf12_cuartil_labels()
    
    elif tipo_datos == 'hads':
        st.session_state['df_pacientes'].at[idx, 'hads_ansiedad'] = datos.get('ansiedad')
        st.session_state['df_pacientes'].at[idx, 'hads_depresion'] = datos.get('depresion')
        # Recalcular clasificación combinada HADS+ZSAS si hay suficientes datos
        try:
            hads_val = st.session_state['df_pacientes'].at[idx, 'hads_ansiedad']
        except Exception:
            hads_val = None
        try:
            zsas_val = st.session_state['df_pacientes'].at[idx, 'zsas_puntaje']
        except Exception:
            zsas_val = None

        # Clasificación: 1 si HADS >=8 y ZSAS >=36; 0 si HADS <8 and ZSAS <36; None otherwise
        if hads_val is not None and zsas_val is not None:
            try:
                if float(hads_val) >= 8 and float(zsas_val) >= 36:
                    st.session_state['df_pacientes'].at[idx, 'hads_zsas_clasificacion'] = 1
                elif float(hads_val) < 8 and float(zsas_val) < 36:
                    st.session_state['df_pacientes'].at[idx, 'hads_zsas_clasificacion'] = 0
                else:
                    st.session_state['df_pacientes'].at[idx, 'hads_zsas_clasificacion'] = None
            except Exception:
                st.session_state['df_pacientes'].at[idx, 'hads_zsas_clasificacion'] = None
    
    elif tipo_datos == 'zsas':
        st.session_state['df_pacientes'].at[idx, 'zsas_puntaje'] = datos.get('puntaje_normalizado')
        # Recalcular clasificación combinada HADS+ZSAS si hay suficientes datos
        try:
            hads_val = st.session_state['df_pacientes'].at[idx, 'hads_ansiedad']
        except Exception:
            hads_val = None
        try:
            zsas_val = st.session_state['df_pacientes'].at[idx, 'zsas_puntaje']
        except Exception:
            zsas_val = None

        if hads_val is not None and zsas_val is not None:
            try:
                if float(hads_val) >= 8 and float(zsas_val) >= 36:
                    st.session_state['df_pacientes'].at[idx, 'hads_zsas_clasificacion'] = 1
                elif float(hads_val) < 8 and float(zsas_val) < 36:
                    st.session_state['df_pacientes'].at[idx, 'hads_zsas_clasificacion'] = 0
                else:
                    st.session_state['df_pacientes'].at[idx, 'hads_zsas_clasificacion'] = None
            except Exception:
                st.session_state['df_pacientes'].at[idx, 'hads_zsas_clasificacion'] = None
    
    elif tipo_datos == 'geneticos':
        st.session_state['df_pacientes'].at[idx, 'gen_prkca'] = datos.get('prkca')
        st.session_state['df_pacientes'].at[idx, 'gen_tcf4'] = datos.get('tcf4')
        st.session_state['df_pacientes'].at[idx, 'gen_cdh20'] = datos.get('cdh20')


def obtener_dataframe():
    """
    Retorna el DataFrame completo
    """
    inicializar_dataframe()
    # Asegurar sincronización antes de devolver
    sincronizar_sf12_cuartil_labels()
    return st.session_state['df_pacientes']


def sincronizar_sf12_cuartil_labels():
    """
    Completa la columna `sf12_fisica_cuartil_label` a partir de
    `sf12_fisica_cuartil` cuando la etiqueta esté ausente.
    Esta función no sobrescribe la columna numérica; sólo rellena labels faltantes.
    """
    inicializar_dataframe()
    df = st.session_state['df_pacientes']

    if 'sf12_fisica_cuartil' not in df.columns:
        return

    # Aplicar mapeo sólo en filas donde existe el cuartil numérico pero falta la etiqueta
    def _label_from_num(row):
        num = row.get('sf12_fisica_cuartil')
        label = row.get('sf12_fisica_cuartil_label')
        if (label is None or (isinstance(label, float) and pd.isna(label))) and num is not None:
            try:
                return transformar_sf12_fisica_a_label(num)
            except Exception:
                return None
        return label

    # Generar la serie de etiquetas y asignarla sólo donde corresponda
    try:
        etiquetas = df.apply(_label_from_num, axis=1)
        # Asignar etiquetas generadas (si no son None)
        for i, val in etiquetas.items():
            if val is not None:
                st.session_state['df_pacientes'].at[i, 'sf12_fisica_cuartil_label'] = val
    except Exception:
        # En caso de error, no bloquear la app; dejar como estaba
        return

    # Ahora hacer lo mismo para la componente mental (si las columnas existen)
    if 'sf12_mental_cuartil' not in df.columns:
        return

    def _label_from_num_mental(row):
        num = row.get('sf12_mental_cuartil')
        label = row.get('sf12_mental_cuartil_label')
        if (label is None or (isinstance(label, float) and pd.isna(label))) and num is not None:
            try:
                return transformar_sf12_mental_a_label(num)
            except Exception:
                return None
        return label

    try:
        etiquetas_m = df.apply(_label_from_num_mental, axis=1)
        for i, val in etiquetas_m.items():
            if val is not None:
                st.session_state['df_pacientes'].at[i, 'sf12_mental_cuartil_label'] = val
    except Exception:
        return


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
    # Renombrar columnas para exportación
    rename_dict = {
        'años_educacion': 'AEFGROUPS',
        'lte12_puntaje': 'LTE12',
        'sf12_fisica_cuartil_label': 'SF12F',
        'sf12_mental_cuartil_label': 'SF12M',
        'gen_prkca': 'PRKCA',
        'gen_tcf4': 'TCF4',
        'gen_cdh20': 'CDH20',
        'grupo_edad': 'edad24',
        'genero': 'genero',
    }
    df = df.rename(columns=rename_dict)
    # Seleccionar solo las columnas finales
    columnas_finales = ['timestamp', 'nombre', 'genero', 'edad24', 'AEFGROUPS', 'LTE12', 'SF12F', 'SF12M', 'PRKCA', 'TCF4', 'CDH20']
    df = df[columnas_finales]
    return df.to_csv(index=False).encode('utf-8')


def mostrar_dataframe_actual():
    """
    Muestra el DataFrame actual en la interfaz
    """
    df = obtener_dataframe()
    
    if len(df) > 0:
        # Renombrar columnas según los requerimientos finales
        rename_dict = {
            'años_educacion': 'AEFGROUPS',
            'lte12_puntaje': 'LTE12',
            'sf12_fisica_cuartil_label': 'SF12F',
            'sf12_mental_cuartil_label': 'SF12M',
            'gen_prkca': 'PRKCA',
            'gen_tcf4': 'TCF4',
            'gen_cdh20': 'CDH20',
            'grupo_edad': 'edad24',
            'genero': 'genero',  # Cambiar a genero
        }
        df = df.rename(columns=rename_dict)
        
        # Seleccionar solo las columnas finales deseadas
        columnas_finales = ['timestamp', 'nombre', 'genero', 'edad24', 'AEFGROUPS', 'LTE12', 'SF12F', 'SF12M', 'PRKCA', 'TCF4', 'CDH20']
        df = df[columnas_finales]
        
        st.subheader("📊 Datos Recolectados")
        st.dataframe(df, width='stretch')

        # Botón de descarga
        csv = df.to_csv(index=False).encode('utf-8')  # Usar df final para descarga
        st.download_button(
            label="⬇️ Descargar datos (CSV)",
            data=csv,
            file_name=f"datos_pacientes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
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
