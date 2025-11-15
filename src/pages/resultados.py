"""
Página de Resultados de la Evaluación
"""
import streamlit as st
from src.utils.dataframe_manager import mostrar_dataframe_actual, obtener_registro_actual
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import datetime

def mostrar_resultados():
    # --- Cargar estilos CSS globales ---
    with open("src/assets/styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Título centrado y en negro
    st.markdown(
        "<h1 style='text-align: center; color: #2E2E2E; font-size: 2rem; font-weight: 700;'>📊 Resultados de la Evaluación</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h3 style='text-align: center; color: #2E2E2E; font-size: 1.25rem; font-weight: 600; margin-bottom: 2rem;'>Análisis completo del riesgo de ansiedad</h3>",
        unsafe_allow_html=True
    )
    
    # Verificar que hay datos para mostrar
    if 'resultados' not in st.session_state or 'datos_geneticos' not in st.session_state.get('resultados', {}):
        st.warning("⚠️ No hay datos disponibles. Por favor, complete todos los cuestionarios primero.")
        if st.button("← Volver a Datos Genéticos"):
            st.session_state.pagina_actual = 'datos_geneticos'
            st.rerun()
        return
    
    # Obtener registro actual
    registro = obtener_registro_actual()
    
    # Generar PDF
    try:
        pdf_bytes = generar_pdf_resultados(st.session_state.resultados, registro)
        pdf_disponible = True
    except Exception as e:
        st.error(f"Error generando PDF: {str(e)}")
        pdf_bytes = None
        pdf_disponible = False
    
    # Contenedor para exportar a PDF
    resultado_html = generar_html_resultados(st.session_state.resultados, registro)
    
    # Botón para exportar a PDF
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if pdf_disponible and pdf_bytes:
            st.download_button(
                label="📄 Descargar Reporte Completo en PDF",
                data=pdf_bytes,
                file_name=f"reporte_completo_ansiedad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
                help="Descarga el reporte completo con todos los resultados, gráficos SHAP, interpretaciones y porcentajes de riesgo"
            )
            st.success("✅ PDF listo para descargar con toda la información de la evaluación")
        else:
            st.download_button(
                label="📄 Descargar Reporte en HTML",
                data=resultado_html,
                file_name="reporte_evaluacion_ansiedad.html",
                mime="text/html",
                type="primary",
                use_container_width=True
            )
            st.info("💡 El archivo HTML descargado puede convertirse a PDF usando el navegador (Archivo → Imprimir → Guardar como PDF)")
            st.warning("⚠️ No se pudo generar el PDF automáticamente. Descargue el HTML como alternativa.")
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Mostrar resultados en tarjeta
    st.markdown("""
    <div style="background: #FFFFFF; padding: 2rem; border-radius: 12px; box-shadow: 0 3px 12px rgba(0,0,0,0.08); border: 1px solid #D1D1D1; margin: 1.5rem 0;">
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #2E2E2E; text-align: center; margin-bottom: 1.5rem;'>📋 Resumen de la Evaluación Completa</h3>", unsafe_allow_html=True)
    
    # Datos Demográficos
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>👤 Datos Demográficos</h4>", unsafe_allow_html=True)
    try:
        # Intentar obtener de resultados primero, luego de session_state directo
        demo_data = st.session_state.resultados.get('datos_demograficos') or st.session_state.get('datos_demograficos')
        if demo_data:
            demo_col1, demo_col2, demo_col3 = st.columns(3)
            with demo_col1:
                st.metric(label="Edad", value=f"{demo_data['edad']} años")
            with demo_col2:
                # Verificar si genero es número o texto
                if isinstance(demo_data.get('genero'), int):
                    genero_texto = "Masculino" if demo_data['genero'] == 0 else "Femenino" if demo_data['genero'] == 1 else "No especificado"
                else:
                    genero_texto = demo_data.get('genero', 'No especificado')
                st.metric(label="Género", value=genero_texto)
            with demo_col3:
                st.metric(label="Educación", value=f"{demo_data['años_educacion']} años")
        else:
            st.info("Datos demográficos no disponibles")
    except (KeyError, TypeError):
        st.info("Datos demográficos no disponibles")
    
    # Eventos Vitales
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>📅 Eventos Vitales (LTE-12)</h4>", unsafe_allow_html=True)
    try:
        eventos_data = st.session_state.resultados['eventos_vitales']
        st.metric(label="Eventos estresantes", value=f"{eventos_data['total']} eventos significativos")
    except KeyError:
        st.info("Datos de eventos vitales no disponibles")
    
    # SF-12
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>🏥 Salud Física y Mental (SF-12)</h4>", unsafe_allow_html=True)
    try:
        sf12_fisica_data = st.session_state.resultados.get('sf12_fisica', {})
        sf12_mental_data = st.session_state.resultados.get('sf12_mental', {})
        
        if sf12_fisica_data or sf12_mental_data:
            sf12_col1, sf12_col2 = st.columns(2)
            with sf12_col1:
                if sf12_fisica_data:
                    st.metric(label="Componente Físico", value=f"{sf12_fisica_data.get('puntaje', 0):.1f}")
                else:
                    st.info("Componente físico no disponible")
            with sf12_col2:
                if sf12_mental_data:
                    st.metric(label="Componente Mental", value=f"{sf12_mental_data.get('puntaje', 0):.1f}")
                else:
                    st.info("Componente mental no disponible")
        else:
            st.info("Datos SF-12 no disponibles")
    except (KeyError, TypeError):
        st.info("Datos SF-12 no disponibles")
    
    # HADS
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>😰 Ansiedad HADS</h4>", unsafe_allow_html=True)
    try:
        hads_data = st.session_state.resultados['hads']
        hads_col1, hads_col2 = st.columns(2)
        with hads_col1:
            st.metric(label="Puntaje", value=hads_data['puntaje'])
        with hads_col2:
            st.metric(label="Nivel", value=hads_data['nivel'])
    except KeyError:
        st.info("Datos HADS no disponibles")
    
    # ZSAS
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>😟 Ansiedad de Zung (ZSAS)</h4>", unsafe_allow_html=True)
    try:
        zsas_data = st.session_state.resultados['zsas']
        zsas_col1, zsas_col2, zsas_col3 = st.columns(3)
        with zsas_col1:
            st.metric(label="Puntaje bruto", value=zsas_data['total'])
        with zsas_col2:
            st.metric(label="Índice normalizado", value=f"{zsas_data['total_normalizado']:.1f}")
        with zsas_col3:
            st.metric(label="Nivel", value=zsas_data['nivel'])
    except KeyError:
        st.info("Datos ZSAS no disponibles")
    
    # Datos Genéticos
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>🧬 Perfil Genético</h4>", unsafe_allow_html=True)
    genetico_data = st.session_state.resultados['datos_geneticos']
    gen_col1, gen_col2, gen_col3 = st.columns(3)
    with gen_col1:
        st.markdown(f"""
        <div style='background: #F5F5F5; padding: 1rem; border-radius: 8px; border-left: 3px solid #4CAF50;'>
            <p style='color: #666; margin: 0; font-size: 0.9rem;'>Gen PRKCA</p>
            <p style='color: #2E2E2E; margin: 0; font-size: 1.3rem; font-weight: 700;'>{genetico_data['prkca']}</p>
        </div>
        """, unsafe_allow_html=True)
    with gen_col2:
        st.markdown(f"""
        <div style='background: #F5F5F5; padding: 1rem; border-radius: 8px; border-left: 3px solid #4CAF50;'>
            <p style='color: #666; margin: 0; font-size: 0.9rem;'>Gen TCF4</p>
            <p style='color: #2E2E2E; margin: 0; font-size: 1.3rem; font-weight: 700;'>{genetico_data['tcf4']}</p>
        </div>
        """, unsafe_allow_html=True)
    with gen_col3:
        st.markdown(f"""
        <div style='background: #F5F5F5; padding: 1rem; border-radius: 8px; border-left: 3px solid #4CAF50;'>
            <p style='color: #666; margin: 0; font-size: 0.9rem;'>Gen CDH20</p>
            <p style='color: #2E2E2E; margin: 0; font-size: 1.3rem; font-weight: 700;'>{genetico_data['cdh20']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Clasificación de ansiedad
    clasificacion_ansiedad = registro.get('hads_zsas_clasificacion') if registro else None
    
    st.markdown("<h4 style='color: #4CAF50; font-size: 1.2rem; margin-top: 1.5rem;'>📊 Clasificación de Ansiedad</h4>", unsafe_allow_html=True)
    if clasificacion_ansiedad == 1:
        st.markdown("""
        <div style='background: #FFE6E6; padding: 1rem; border-radius: 8px; border-left: 4px solid #F44336;'>
            <p style='color: #2E2E2E; margin: 0; font-size: 1.1rem;'><strong>Clasificación: Alto Riesgo (1)</strong></p>
            <p style='color: #666; margin: 0.5rem 0 0 0;'>HADS ≥ 8 y ZSAS ≥ 36</p>
        </div>
        """, unsafe_allow_html=True)
    elif clasificacion_ansiedad == 0:
        st.markdown("""
        <div style='background: #E6F7E6; padding: 1rem; border-radius: 8px; border-left: 4px solid #4CAF50;'>
            <p style='color: #2E2E2E; margin: 0; font-size: 1.1rem;'><strong>Clasificación: Bajo Riesgo (0)</strong></p>
            <p style='color: #666; margin: 0.5rem 0 0 0;'>HADS < 8 o ZSAS < 36</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: #FFF3CD; padding: 1rem; border-radius: 8px; border-left: 4px solid #FFC107;'>
            <p style='color: #2E2E2E; margin: 0; font-size: 1.1rem;'><strong>Clasificación: No disponible</strong></p>
            <p style='color: #666; margin: 0.5rem 0 0 0;'>Datos insuficientes para clasificar</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Mostrar DataFrame completo
    st.markdown("---")
    st.markdown("<h3 style='color: #4CAF50; font-size: 1.5rem; margin-top: 2rem;'>📊 DataFrame Completo de la Evaluación</h3>", unsafe_allow_html=True)
    mostrar_dataframe_actual()
    
    # Predicción de riesgo con modelo
    st.markdown("---")
    st.markdown("<h3 style='color: #4CAF50; font-size: 1.5rem; margin-top: 2rem;'>🤖 Predicción de Riesgo de Ansiedad</h3>", unsafe_allow_html=True)
    
    if registro:
        genero = registro.get('genero')
        if genero == 0:
            model_path = 'src/models/lightgbm_male_model_tuned.joblib'
            model_name = "LightGBM (Masculino)"
        elif genero == 1:
            model_path = 'src/models/mlp_female_model_tuned.joblib'
            model_name = "MLP (Femenino)"
        else:
            st.error("Género no válido para predicción")
            return
        
        try:
            import joblib
            model = joblib.load(model_path)
            
            # Preparar features
            from src.utils.calculos import transformar_lte12_a_clasificacion, transformar_sf12_fisica_a_cuartil, transformar_sf12_mental_a_cuartil, transformar_educacion_a_binaria
            
            edad24 = registro.get('grupo_edad', 0)
            aefgroups = transformar_educacion_a_binaria(registro.get('años_educacion', 0))
            
            lte12_clasif = transformar_lte12_a_clasificacion(registro.get('lte12_puntaje', 0))
            lte12_0 = 1 if lte12_clasif == 0 else 0
            lte12_1 = 1 if lte12_clasif == 1 else 0
            lte12_2 = 1 if lte12_clasif == 2 else 0
            
            sf12f_cuartil = transformar_sf12_fisica_a_cuartil(registro.get('sf12_fisica', 0))
            sf12f_q1 = 1 if sf12f_cuartil == 1 else 0
            sf12f_q2 = 1 if sf12f_cuartil == 2 else 0
            sf12f_q3 = 1 if sf12f_cuartil == 3 else 0
            sf12f_q4 = 1 if sf12f_cuartil == 4 else 0
            
            sf12m_cuartil = transformar_sf12_mental_a_cuartil(registro.get('sf12_mental', 0))
            sf12m_q1 = 1 if sf12m_cuartil == 1 else 0
            sf12m_q2 = 1 if sf12m_cuartil == 2 else 0
            sf12m_q3 = 1 if sf12m_cuartil == 3 else 0
            sf12m_q4 = 1 if sf12m_cuartil == 4 else 0
            
            prkca = registro.get('gen_prkca', 'T/T')
            prkca_cc = 1 if prkca == 'C/C' else 0
            prkca_ct = 1 if prkca == 'C/T' else 0
            prkca_tt = 1 if prkca == 'T/T' else 0
            
            tcf4 = registro.get('gen_tcf4', 'A/A')
            tcf4_aa = 1 if tcf4 == 'A/A' else 0
            tcf4_at = 1 if tcf4 == 'A/T' else 0
            tcf4_tt = 1 if tcf4 == 'T/T' else 0
            
            cdh20 = registro.get('gen_cdh20', 'G/G')
            cdh20_aa = 1 if cdh20 == 'A/A' else 0
            cdh20_ag = 1 if cdh20 == 'G/A' else 0
            cdh20_gg = 1 if cdh20 == 'G/G' else 0
            
            features_dict = {
                'EDAD24': edad24,
                'AEFGROUPS': aefgroups,
                'SF12F_Q1': sf12f_q1,
                'SF12F_Q2': sf12f_q2,
                'SF12F_Q3': sf12f_q3,
                'SF12F_Q4': sf12f_q4,
                'SF12M_Q1': sf12m_q1,
                'SF12M_Q2': sf12m_q2,
                'SF12M_Q3': sf12m_q3,
                'SF12M_Q4': sf12m_q4,
                'PRKCA_C/C': prkca_cc,
                'PRKCA_C/T': prkca_ct,
                'PRKCA_T/T': prkca_tt,
                'TCF4_A/A': tcf4_aa,
                'TCF4_A/T': tcf4_at,
                'TCF4_T/T': tcf4_tt,
                'CDH20_A/A': cdh20_aa,
                'CDH20_A/G': cdh20_ag,
                'CDH20_G/G': cdh20_gg,
                'LTE12_0': lte12_0,
                'LTE12_1': lte12_1,
                'LTE12_2': lte12_2,
            }
            
            X = pd.DataFrame([features_dict])
            
            if hasattr(model, 'feature_names_in_'):
                expected_features = list(model.feature_names_in_)
            elif hasattr(model, 'feature_name_'):
                expected_features = model.feature_name_
            else:
                expected_features = None
            
            if expected_features:
                try:
                    X = X[expected_features]
                except KeyError as e:
                    st.error(f"Error: Columnas en X no coinciden con las esperadas por el modelo: {e}")
                    return
            
            # Mostrar features transformadas
            features_display = {'GENERO': genero, **features_dict}
            X_display = pd.DataFrame([features_display])
            st.markdown("### 📊 Features Transformadas (One-Hot Encoding)")
            st.dataframe(X_display, use_container_width=True, hide_index=True)
            
            # Predicción
            prediction = model.predict(X)[0]
            
            riesgo = "Alto Riesgo" if prediction == 1 else "Bajo Riesgo"
            color = "#F44336" if prediction == 1 else "#4CAF50"
            
            st.markdown(f"""
            <div style='background: #FFFFFF; padding: 2rem; border-radius: 12px; box-shadow: 0 3px 12px rgba(0,0,0,0.08); border: 1px solid #D1D1D1; margin: 1.5rem 0; text-align: center;'>
                <h4 style='color: #2E2E2E; margin-bottom: 1rem;'>Resultado de la Predicción</h4>
                <p style='color: #666; margin-bottom: 1rem;'>Modelo utilizado: {model_name}</p>
                <p style='color: {color}; font-size: 1.5rem; font-weight: 700; margin: 0;'>{riesgo}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if hasattr(model, 'predict_proba'):
                prob = model.predict_proba(X)[0]
                prob_col1, prob_col2 = st.columns(2)
                with prob_col1:
                    st.metric(label="Probabilidad de Alto Riesgo", value=f"{prob[1]:.2%}")
                with prob_col2:
                    st.metric(label="Probabilidad de Bajo Riesgo", value=f"{prob[0]:.2%}")
            
            # SHAP
            mostrar_shap_analysis(model, X, genero)
            
        except FileNotFoundError:
            st.warning(f"Modelo no encontrado: {model_path}")
        except Exception as e:
            st.error(f"Error en la predicción: {str(e)}")
    else:
        st.info("No hay datos disponibles para predicción")
    
    # Nota final
    st.markdown("""
    <div style='margin-top: 1.5rem; padding: 1rem; background: #FFF9E6; border-radius: 8px; border-left: 4px solid #FFC107;'>
        <p style='color: #2E2E2E; margin: 0.5rem 0;'><strong>⚠️ Nota importante:</strong></p>
        <p style='color: #2E2E2E; margin: 0.5rem 0;'>
        Esta evaluación es preliminar y debe ser interpretada por un profesional de la salud.
        Los resultados no constituyen un diagnóstico definitivo. Se recomienda consultar con un especialista
        en salud mental para una evaluación completa y personalizada.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Botones de navegación
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Volver a Datos Genéticos", use_container_width=True):
            st.session_state.pagina_actual = 'datos_geneticos'
            st.rerun()
    with col3:
        if st.button("🔄 Nueva Evaluación", type="primary", use_container_width=True):
            # Limpiar toda la sesión
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            # Establecer página inicial
            st.session_state.pagina_actual = 'Home'
            st.rerun()


def mostrar_shap_analysis(model, X, genero):
    """Muestra el análisis SHAP"""
    st.markdown("### 📈 Explicación de la Predicción (SHAP)")
    try:
        import shap
        import matplotlib.pyplot as plt
        from sklearn.neural_network import MLPClassifier
        import lightgbm as lgb
        
        feature_names = list(X.columns)
        X_array = X.values
        
        if isinstance(model, MLPClassifier):
            background_data = np.random.choice([0, 1], size=(50, X.shape[1]), p=[0.7, 0.3])
        else:
            background_data = X_array
        
        if isinstance(model, lgb.LGBMClassifier):
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_array)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
        elif isinstance(model, MLPClassifier):
            explainer = shap.KernelExplainer(model.predict_proba, background_data, feature_names=feature_names)
            shap_values = explainer.shap_values(X_array)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
        else:
            explainer = shap.KernelExplainer(model.predict_proba, background_data, feature_names=feature_names)
            shap_values = explainer.shap_values(X_array)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
        
        if hasattr(shap_values, 'values'):
            shap_array = shap_values.values
        elif isinstance(shap_values, np.ndarray):
            shap_array = shap_values
        else:
            shap_array = np.array(shap_values)
        
        if shap_array.ndim == 1:
            shap_array = shap_array.reshape(1, -1)
        elif shap_array.ndim == 3:
            shap_array = shap_array[:, :, -1]
        
        # Gráfico SHAP
        st.markdown("#### 📈 Gráfico de Importancia de Características")
        top_n = 15
        top_indices = np.argsort(np.abs(shap_array[0]))[-top_n:][::-1]
        top_shap_values = shap_array[0][top_indices]
        top_feature_names = [feature_names[i] for i in top_indices]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = ['#DC3545' if val > 0 else '#28A745' for val in top_shap_values]
        ax.barh(range(len(top_shap_values)), top_shap_values, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
        ax.set_yticks(range(len(top_shap_values)))
        ax.set_yticklabels(top_feature_names, fontsize=10)
        ax.set_xlabel('SHAP Value (Contribución al Riesgo)', fontsize=12, fontweight='bold')
        ax.set_title(f'Top {top_n} Características más Influyentes', fontsize=14, fontweight='bold')
        ax.axvline(x=0, color='black', linestyle='-', linewidth=1.5)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#DC3545', alpha=0.8, edgecolor='black', label='Aumenta Riesgo Alto'),
            Patch(facecolor='#28A745', alpha=0.8, edgecolor='black', label='Disminuye Riesgo Alto')
        ]
        ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
        
        # Interpretación personalizada
        st.markdown("#### 📋 Interpretación Personalizada")
        generar_interpretacion_shap(shap_array, feature_names, X)
        
    except Exception as e:
        st.error(f"Error generando análisis SHAP: {str(e)}")


def generar_interpretacion_shap(shap_array, feature_names, X):
    """Genera interpretación personalizada de SHAP"""
    top_n = 10
    top_indices = np.argsort(np.abs(shap_array[0]))[-top_n:][::-1]
    
    st.markdown("""
        <div style='background: #FFFFFF; padding: 1.5rem; border-radius: 8px; border: 1px solid #E0E0E0; margin-top: 1rem;'>
            <h4 style='color: #2E2E2E; margin-top: 0; border-bottom: 2px solid #4CAF50; padding-bottom: 0.5rem;'>
                🔍 Factores que Explican la Predicción
            </h4>
        </div>
    """, unsafe_allow_html=True)
    
    for idx in top_indices:
        feature = feature_names[idx]
        shap_val = shap_array[0][idx]
        feature_val = X.iloc[0, idx]
        
        color = "#DC3545" if shap_val > 0 else "#28A745"
        efecto = "AUMENTA" if shap_val > 0 else "DISMINUYE"
        icono = "⬆️" if shap_val > 0 else "⬇️"
        
        interpretacion = obtener_interpretacion_feature(feature, feature_val)
        
        st.markdown(f"""
        <div style='background: #F8F9FA; padding: 1rem; margin: 0.75rem 0; border-radius: 6px; border-left: 4px solid {color};'>
            <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                <span style='font-size: 1.5rem; margin-right: 0.5rem;'>{icono}</span>
                <strong style='color: {color}; font-size: 1.1rem;'>{feature}</strong>
            </div>
            <p style='color: #2E2E2E; margin: 0.5rem 0; font-size: 0.95rem;'>{interpretacion}</p>
            <p style='color: #666; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
                <strong>Impacto:</strong> Esta característica <strong style='color: {color};'>{efecto}</strong> 
                la probabilidad de riesgo alto de ansiedad en <strong>{abs(shap_val):.4f}</strong> unidades SHAP.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #FFF3CD; padding: 1rem; margin-top: 1.5rem; border-radius: 6px; border-left: 4px solid #FFC107;'>
        <p style='color: #856404; margin: 0; font-size: 0.95rem;'>
            <strong>💡 Resumen Clínico:</strong> El modelo considera principalmente la salud mental/física del paciente, 
            factores genéticos y eventos vitales estresantes para determinar el riesgo de ansiedad.
        </p>
    </div>
    """, unsafe_allow_html=True)


def obtener_interpretacion_feature(feature, feature_val):
    """Retorna interpretación clínica de una feature"""
    if feature == "EDAD24":
        return f"Grupo de edad {'24-34 años' if feature_val == 1 else 'fuera de 24-34 años'}"
    elif feature == "AEFGROUPS":
        return f"Nivel educativo {'superior (≥15 años)' if feature_val == 1 else 'básico/secundario (<15 años)'}"
    elif "SF12F" in feature:
        cuartil = feature.split("_")[1]
        if feature_val == 1:
            descripciones = {
                "Q1": "salud física muy baja (cuartil 1)",
                "Q2": "salud física baja (cuartil 2)",
                "Q3": "salud física moderada (cuartil 3)",
                "Q4": "salud física buena (cuartil 4)"
            }
            return f"Paciente presenta {descripciones.get(cuartil, cuartil)}"
        return f"No pertenece a este nivel de salud física ({cuartil})"
    elif "SF12M" in feature:
        cuartil = feature.split("_")[1]
        if feature_val == 1:
            descripciones = {
                "Q1": "salud mental muy baja (cuartil 1)",
                "Q2": "salud mental baja (cuartil 2)",
                "Q3": "salud mental moderada (cuartil 3)",
                "Q4": "salud mental buena (cuartil 4)"
            }
            return f"Paciente presenta {descripciones.get(cuartil, cuartil)}"
        return f"No pertenece a este nivel de salud mental ({cuartil})"
    elif "PRKCA" in feature:
        genotipo = feature.split("_")[1]
        return f"Genotipo PRKCA {genotipo} {'presente' if feature_val == 1 else 'ausente'} (regulación del estrés)"
    elif "TCF4" in feature:
        genotipo = feature.split("_")[1]
        return f"Genotipo TCF4 {genotipo} {'presente' if feature_val == 1 else 'ausente'} (transcripción neuronal)"
    elif "CDH20" in feature:
        genotipo = feature.split("_")[1]
        return f"Genotipo CDH20 {genotipo} {'presente' if feature_val == 1 else 'ausente'} (conectividad neuronal)"
    elif "LTE12" in feature:
        nivel = feature.split("_")[1]
        if feature_val == 1:
            descripciones = {
                "0": "sin eventos vitales estresantes",
                "1": "1 evento vital estresante",
                "2": "2 o más eventos vitales estresantes"
            }
            return f"Paciente experimentó {descripciones.get(nivel, nivel)}"
        return f"No se encuentra en esta categoría de eventos vitales ({nivel})"
    return f"Valor de la característica: {feature_val}"


def generar_html_resultados(resultados, registro):
    """Genera HTML completo para exportar a PDF"""
    html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Evaluación de Ansiedad</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #2E2E2E;
        }
        h1 { color: #4CAF50; text-align: center; }
        h2 { color: #4CAF50; border-bottom: 2px solid #E0E0E0; padding-bottom: 10px; }
        h3 { color: #2E2E2E; }
        .section {
            background: #F8F9FA;
            padding: 15px;
            margin: 15px 0;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
        }
        .metric {
            display: inline-block;
            margin: 10px 20px 10px 0;
        }
        .metric-label {
            color: #666;
            font-size: 0.9rem;
        }
        .metric-value {
            color: #2E2E2E;
            font-size: 1.3rem;
            font-weight: bold;
        }
        .warning {
            background: #FFF9E6;
            padding: 15px;
            border-left: 4px solid #FFC107;
            border-radius: 8px;
            margin: 20px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th, td {
            border: 1px solid #E0E0E0;
            padding: 10px;
            text-align: left;
        }
        th {
            background: #4CAF50;
            color: white;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <h1>📊 Reporte de Evaluación de Ansiedad</h1>
    <p style="text-align: center; color: #666;">Análisis completo del riesgo de ansiedad</p>
"""
    
    # Datos demográficos
    demo_data = resultados.get('datos_demograficos') or st.session_state.get('datos_demograficos')
    if demo_data:
        # Verificar si genero es número o texto
        if isinstance(demo_data.get('genero'), int):
            genero_txt = "Masculino" if demo_data['genero'] == 0 else "Femenino"
        else:
            genero_txt = demo_data.get('genero', 'No especificado')
            
        html += f"""
    <h2>👤 Datos Demográficos</h2>
    <div class="section">
        <div class="metric">
            <div class="metric-label">Edad</div>
            <div class="metric-value">{demo_data['edad']} años</div>
        </div>
        <div class="metric">
            <div class="metric-label">Género</div>
            <div class="metric-value">{genero_txt}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Educación</div>
            <div class="metric-value">{demo_data['años_educacion']} años</div>
        </div>
    </div>
"""
    
    # Eventos vitales
    if 'eventos_vitales' in resultados:
        eventos = resultados['eventos_vitales']
        html += f"""
    <h2>📅 Eventos Vitales (LTE-12)</h2>
    <div class="section">
        <div class="metric">
            <div class="metric-label">Eventos estresantes</div>
            <div class="metric-value">{eventos['total']} eventos significativos</div>
        </div>
    </div>
"""
    
    # HADS
    if 'hads' in resultados:
        hads = resultados['hads']
        html += f"""
    <h2>😰 Ansiedad HADS</h2>
    <div class="section">
        <div class="metric">
            <div class="metric-label">Puntaje</div>
            <div class="metric-value">{hads['puntaje']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Nivel</div>
            <div class="metric-value">{hads['nivel']}</div>
        </div>
    </div>
"""
    
    # ZSAS
    if 'zsas' in resultados:
        zsas = resultados['zsas']
        html += f"""
    <h2>😟 Ansiedad de Zung (ZSAS)</h2>
    <div class="section">
        <div class="metric">
            <div class="metric-label">Puntaje bruto</div>
            <div class="metric-value">{zsas['total']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Índice normalizado</div>
            <div class="metric-value">{zsas['total_normalizado']:.1f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Nivel</div>
            <div class="metric-value">{zsas['nivel']}</div>
        </div>
    </div>
"""
    
    # Datos genéticos
    if 'datos_geneticos' in resultados:
        gen = resultados['datos_geneticos']
        html += f"""
    <h2>🧬 Perfil Genético</h2>
    <div class="section">
        <div class="metric">
            <div class="metric-label">Gen PRKCA</div>
            <div class="metric-value">{gen['prkca']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Gen TCF4</div>
            <div class="metric-value">{gen['tcf4']}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Gen CDH20</div>
            <div class="metric-value">{gen['cdh20']}</div>
        </div>
    </div>
"""
    
    # Clasificación
    if registro:
        clasificacion = registro.get('hads_zsas_clasificacion')
        if clasificacion == 1:
            html += """
    <h2>📊 Clasificación de Ansiedad</h2>
    <div class="section" style="background: #FFE6E6; border-left-color: #F44336;">
        <h3>Clasificación: Alto Riesgo (1)</h3>
        <p>HADS ≥ 8 y ZSAS ≥ 36</p>
    </div>
"""
        elif clasificacion == 0:
            html += """
    <h2>📊 Clasificación de Ansiedad</h2>
    <div class="section" style="background: #E6F7E6; border-left-color: #4CAF50;">
        <h3>Clasificación: Bajo Riesgo (0)</h3>
        <p>HADS < 8 o ZSAS < 36</p>
    </div>
"""
    
    # Nota final
    html += """
    <div class="warning">
        <p><strong>⚠️ Nota importante:</strong></p>
        <p>Esta evaluación es preliminar y debe ser interpretada por un profesional de la salud.
        Los resultados no constituyen un diagnóstico definitivo. Se recomienda consultar con un especialista
        en salud mental para una evaluación completa y personalizada.</p>
    </div>
    
    <div class="footer">
        <p>Reporte generado automáticamente por el Sistema de Evaluación de Ansiedad ANXRISK</p>
        <p>Fecha de generación: """ + pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
    </div>
</body>
</html>
"""
    
    return html


def generar_pdf_resultados(resultados, registro):
    """Genera PDF completo para exportar usando ReportLab con diseño minimalista para salud"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, KeepTogether
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        import matplotlib.pyplot as plt
        import matplotlib
        matplotlib.use('Agg')  # Backend sin interfaz gráfica
        from io import BytesIO as MatplotlibBytesIO
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4, 
            rightMargin=50, 
            leftMargin=50, 
            topMargin=50, 
            bottomMargin=50
        )
        
        # Contenedor de elementos
        elements = []
        
        # Paleta de colores minimalista para salud
        COLOR_PRIMARIO = colors.HexColor('#2C5F7C')  # Azul salud oscuro
        COLOR_SECUNDARIO = colors.HexColor('#5DA5C8')  # Azul salud claro
        COLOR_ACENTO = colors.HexColor('#7CB9D1')  # Azul pastel
        COLOR_TEXTO = colors.HexColor('#2E2E2E')  # Gris oscuro
        COLOR_FONDO = colors.HexColor('#F8F9FA')  # Gris muy claro
        COLOR_EXITO = colors.HexColor('#4CAF50')  # Verde
        COLOR_ALERTA = colors.HexColor('#FFC107')  # Amarillo
        COLOR_PELIGRO = colors.HexColor('#DC3545')  # Rojo
        
        # Estilos minimalistas
        styles = getSampleStyleSheet()
        
        # Título principal
        title_style = ParagraphStyle(
            'MinimalTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=COLOR_PRIMARIO,
            spaceAfter=8,
            spaceBefore=0,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=26
        )
        
        # Subtítulo
        subtitle_style = ParagraphStyle(
            'MinimalSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=COLOR_TEXTO,
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica',
            leading=12
        )
        
        # Encabezados de sección
        heading_style = ParagraphStyle(
            'MinimalHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=COLOR_PRIMARIO,
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold',
            borderWidth=0,
            borderPadding=0,
            leftIndent=0,
            leading=16
        )
        
        # Texto normal
        normal_style = ParagraphStyle(
            'MinimalNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            textColor=COLOR_TEXTO,
            alignment=TA_JUSTIFY,
            fontName='Helvetica',
            leading=13
        )
        
        # Estilo para métricas
        metric_style = ParagraphStyle(
            'MetricStyle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=COLOR_TEXTO,
            alignment=TA_CENTER,
            fontName='Helvetica',
            leading=11
        )
        
        # ==================== PORTADA ====================
        elements.append(Spacer(1, 0.5*inch))
        
        # Logo o línea decorativa minimalista
        elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━", 
            ParagraphStyle('Line', alignment=TA_CENTER, textColor=COLOR_SECUNDARIO, fontSize=16)))
        elements.append(Spacer(1, 0.3*inch))
        
        # Título
        elements.append(Paragraph("REPORTE DE EVALUACIÓN", title_style))
        elements.append(Paragraph("RIESGO DE ANSIEDAD", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Línea decorativa
        elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━", 
            ParagraphStyle('Line', alignment=TA_CENTER, textColor=COLOR_SECUNDARIO, fontSize=16)))
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Información del paciente
        demo_data = resultados.get('datos_demograficos') or st.session_state.get('datos_demograficos')
        if demo_data:
            if isinstance(demo_data.get('genero'), int):
                genero_txt = "Masculino" if demo_data['genero'] == 0 else "Femenino"
            else:
                genero_txt = demo_data.get('genero', 'No especificado')
            
            paciente_info = f"""
            <para alignment="center" fontSize="11" textColor="#2E2E2E">
            <b>Paciente:</b> {demo_data.get('nombre', 'No especificado')}<br/>
            <b>Edad:</b> {demo_data['edad']} años | <b>Género:</b> {genero_txt}<br/>
            <b>Educación:</b> {demo_data['años_educacion']} años
            </para>
            """
            elements.append(Paragraph(paciente_info, normal_style))
        
        elements.append(Spacer(1, 0.5*inch))
        
        # Fecha
        fecha_texto = f"""
        <para alignment="center" fontSize="9" textColor="#666666">
        Fecha de evaluación: {datetime.now().strftime('%d de %B de %Y, %H:%M hrs')}
        </para>
        """
        elements.append(Paragraph(fecha_texto, subtitle_style))
        
        elements.append(Spacer(1, 1*inch))
        
        # Nota de confidencialidad
        confidencial = """
        <para alignment="center" fontSize="8" textColor="#666666" borderWidth="1" borderColor="#CCCCCC" borderPadding="8">
        <b>DOCUMENTO CONFIDENCIAL</b><br/>
        Este reporte contiene información médica sensible y está destinado únicamente<br/>
        para uso del profesional de salud autorizado y el paciente.
        </para>
        """
        elements.append(Paragraph(confidencial, normal_style))
        
        elements.append(PageBreak())
        
        # ==================== RESUMEN EJECUTIVO ====================
        elements.append(Paragraph("RESUMEN DE LA EVALUACIÓN", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Métricas clave en una sola vista
        metricas_texto = """
        <para fontSize="9" textColor="#2E2E2E" alignment="justify" spaceAfter="10">
        Este resumen presenta las métricas clave obtenidas durante la evaluación integral del 
        paciente, incluyendo cuestionarios estandarizados, perfil genético y análisis predictivo 
        mediante inteligencia artificial.
        </para>
        """
        elements.append(Paragraph(metricas_texto, normal_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Tabla de resumen de métricas
        if resultados:
            metricas_data = [['Evaluación', 'Resultado', 'Interpretación']]
            
            # HADS
            if 'hads' in resultados:
                hads = resultados['hads']
                metricas_data.append(['HADS', str(hads['puntaje']), hads['nivel']])
            
            # ZSAS
            if 'zsas' in resultados:
                zsas = resultados['zsas']
                metricas_data.append(['ZSAS', f"{zsas['total']} ({zsas['total_normalizado']:.1f})", zsas['nivel']])
            
            # SF-12
            if 'sf12_fisica' in resultados:
                sf12f = resultados['sf12_fisica']
                metricas_data.append(['SF-12 Física', f"{sf12f.get('puntaje', 0):.1f}", f"Cuartil {sf12f.get('cuartil', 'N/A')}"])
            
            if 'sf12_mental' in resultados:
                sf12m = resultados['sf12_mental']
                metricas_data.append(['SF-12 Mental', f"{sf12m.get('puntaje', 0):.1f}", f"Cuartil {sf12m.get('cuartil', 'N/A')}"])
            
            # LTE-12
            if 'eventos_vitales' in resultados:
                lte = resultados['eventos_vitales']
                metricas_data.append(['LTE-12', str(lte['total']), f"{lte['total']} eventos estresantes"])
            
            metricas_table = Table(metricas_data, colWidths=[2*inch, 2*inch, 2.5*inch])
            metricas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARIO),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('TOPPADDING', (0, 0), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
                ('BACKGROUND', (0, 1), (-1, -1), COLOR_FONDO),
                ('BOX', (0, 0), (-1, -1), 1, COLOR_PRIMARIO),
                ('LINEABOVE', (0, 1), (-1, -1), 0.5, COLOR_SECUNDARIO),
            ]))
            
            elements.append(metricas_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Clasificación de riesgo destacada
        if registro:
            clasificacion = registro.get('hads_zsas_clasificacion')
            
            if clasificacion == 1:
                risk_color = COLOR_PELIGRO
                risk_bg = colors.HexColor('#FFE6E6')
                risk_text = "ALTO RIESGO"
                risk_desc = "HADS ≥ 8 y ZSAS ≥ 36"
            elif clasificacion == 0:
                risk_color = COLOR_EXITO
                risk_bg = colors.HexColor('#E6F7E6')
                risk_text = "BAJO RIESGO"
                risk_desc = "HADS < 8 o ZSAS < 36"
            else:
                risk_color = COLOR_ALERTA
                risk_bg = colors.HexColor('#FFF3CD')
                risk_text = "NO DETERMINADO"
                risk_desc = "Datos insuficientes"
            
            risk_data = [[Paragraph(f'<b>{risk_text}</b><br/>{risk_desc}', 
                ParagraphStyle('RiskText', alignment=TA_CENTER, fontSize=12, textColor=risk_color, leading=16))]]
            
            risk_table = Table(risk_data, colWidths=[6.5*inch])
            risk_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), risk_bg),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 15),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
                ('BOX', (0, 0), (-1, -1), 2, risk_color),
            ]))
            
            elements.append(risk_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # ==================== DATOS DEMOGRÁFICOS ====================
        elements.append(Paragraph("1. DATOS DEMOGRÁFICOS", heading_style))
        
        if demo_data:
            demo_table_data = [
                ['Edad', 'Género', 'Años de Educación'],
                [f"{demo_data['edad']} años", genero_txt, f"{demo_data['años_educacion']} años"]
            ]
            
            demo_table = Table(demo_table_data, colWidths=[2.16*inch]*3)
            demo_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARIO),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 1), (-1, -1), COLOR_FONDO),
                ('GRID', (0, 0), (-1, -1), 0.5, COLOR_SECUNDARIO),
                ('BOX', (0, 0), (-1, -1), 1, COLOR_PRIMARIO),
            ]))
            
            elements.append(demo_table)
            elements.append(Spacer(1, 0.15*inch))
        
        # ==================== CUESTIONARIOS ====================
        elements.append(Paragraph("2. RESULTADOS DE CUESTIONARIOS", heading_style))
        
        # Eventos Vitales
        if 'eventos_vitales' in resultados:
            eventos = resultados['eventos_vitales']
            eventos_data = [
                ['LTE-12: Eventos Vitales Estresantes'],
                [f"{eventos['total']} eventos significativos"]
            ]
            eventos_table = Table(eventos_data, colWidths=[6.5*inch])
            eventos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_SECUNDARIO),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), COLOR_FONDO),
                ('BOX', (0, 0), (-1, -1), 1, COLOR_PRIMARIO),
            ]))
            elements.append(eventos_table)
            elements.append(Spacer(1, 0.1*inch))
        
        # SF-12
        sf12_fisica = resultados.get('sf12_fisica', {})
        sf12_mental = resultados.get('sf12_mental', {})
        
        if sf12_fisica or sf12_mental:
            sf12_data = [['SF-12: Salud Física y Mental', 'Puntaje']]
            
            if sf12_fisica:
                sf12_data.append(['Componente Físico', f"{sf12_fisica.get('puntaje', 0):.1f}"])
            
            if sf12_mental:
                sf12_data.append(['Componente Mental', f"{sf12_mental.get('puntaje', 0):.1f}"])
            
            sf12_table = Table(sf12_data, colWidths=[4.5*inch, 2*inch])
            sf12_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_SECUNDARIO),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), COLOR_FONDO),
                ('BOX', (0, 0), (-1, -1), 1, COLOR_PRIMARIO),
                ('LINEABOVE', (0, 1), (-1, 1), 0.5, COLOR_SECUNDARIO),
                ('LINEABOVE', (0, 2), (-1, -1), 0.5, COLOR_SECUNDARIO),
            ]))
            elements.append(sf12_table)
            elements.append(Spacer(1, 0.1*inch))
        
        # HADS y ZSAS
        cuestionarios_data = [['Cuestionario', 'Puntaje', 'Nivel']]
        
        if 'hads' in resultados:
            hads = resultados['hads']
            cuestionarios_data.append(['HADS (Ansiedad Hospitalaria)', 
                                      str(hads['puntaje']), hads['nivel']])
        
        if 'zsas' in resultados:
            zsas = resultados['zsas']
            cuestionarios_data.append(['ZSAS (Zung)', 
                                      f"{zsas['total']} ({zsas['total_normalizado']:.1f})", 
                                      zsas['nivel']])
        
        if len(cuestionarios_data) > 1:
            cuest_table = Table(cuestionarios_data, colWidths=[3*inch, 1.5*inch, 2*inch])
            cuest_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_SECUNDARIO),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), COLOR_FONDO),
                ('BOX', (0, 0), (-1, -1), 1, COLOR_PRIMARIO),
                ('LINEABOVE', (0, 1), (-1, -1), 0.5, COLOR_SECUNDARIO),
            ]))
            elements.append(cuest_table)
            elements.append(Spacer(1, 0.15*inch))
        
        # ==================== PERFIL GENÉTICO ====================
        elements.append(Paragraph("3. PERFIL GENÉTICO", heading_style))
        
        if 'datos_geneticos' in resultados:
            gen = resultados['datos_geneticos']
            gen_data = [
                ['Gen', 'Genotipo'],
                ['PRKCA (Regulación del estrés)', gen['prkca']],
                ['TCF4 (Transcripción neuronal)', gen['tcf4']],
                ['CDH20 (Conectividad neuronal)', gen['cdh20']]
            ]
            
            gen_table = Table(gen_data, colWidths=[4.5*inch, 2*inch])
            gen_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARIO),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), COLOR_FONDO),
                ('BOX', (0, 0), (-1, -1), 1, COLOR_PRIMARIO),
                ('LINEABOVE', (0, 1), (-1, -1), 0.5, COLOR_SECUNDARIO),
            ]))
            
            elements.append(gen_table)
            elements.append(Spacer(1, 0.15*inch))
        
        elements.append(PageBreak())
        
        # ==================== PREDICCIÓN DEL MODELO ====================
        elements.append(Paragraph("4. PREDICCIÓN DE RIESGO (MODELO IA)", heading_style))
        
        # Realizar predicción si hay datos
        if registro:
            genero = registro.get('genero')
            
            try:
                import joblib
                from src.utils.calculos import transformar_lte12_a_clasificacion, transformar_sf12_fisica_a_cuartil, transformar_sf12_mental_a_cuartil, transformar_educacion_a_binaria
                import pandas as pd
                
                # Seleccionar modelo según género
                if genero == 0:
                    model_path = 'src/models/lightgbm_male_model_tuned.joblib'
                    model_name = "LightGBM (Paciente Masculino)"
                elif genero == 1:
                    model_path = 'src/models/mlp_female_model_tuned.joblib'
                    model_name = "MLP (Paciente Femenino)"
                else:
                    raise ValueError("Género no válido")
                
                model = joblib.load(model_path)
                
                # Preparar features
                edad24 = registro.get('grupo_edad', 0)
                aefgroups = transformar_educacion_a_binaria(registro.get('años_educacion', 0))
                
                lte12_clasif = transformar_lte12_a_clasificacion(registro.get('lte12_puntaje', 0))
                lte12_0 = 1 if lte12_clasif == 0 else 0
                lte12_1 = 1 if lte12_clasif == 1 else 0
                lte12_2 = 1 if lte12_clasif == 2 else 0
                
                sf12f_cuartil = transformar_sf12_fisica_a_cuartil(registro.get('sf12_fisica', 0))
                sf12f_q1 = 1 if sf12f_cuartil == 1 else 0
                sf12f_q2 = 1 if sf12f_cuartil == 2 else 0
                sf12f_q3 = 1 if sf12f_cuartil == 3 else 0
                sf12f_q4 = 1 if sf12f_cuartil == 4 else 0
                
                sf12m_cuartil = transformar_sf12_mental_a_cuartil(registro.get('sf12_mental', 0))
                sf12m_q1 = 1 if sf12m_cuartil == 1 else 0
                sf12m_q2 = 1 if sf12m_cuartil == 2 else 0
                sf12m_q3 = 1 if sf12m_cuartil == 3 else 0
                sf12m_q4 = 1 if sf12m_cuartil == 4 else 0
                
                prkca = registro.get('gen_prkca', 'T/T')
                prkca_cc = 1 if prkca == 'C/C' else 0
                prkca_ct = 1 if prkca == 'C/T' else 0
                prkca_tt = 1 if prkca == 'T/T' else 0
                
                tcf4 = registro.get('gen_tcf4', 'A/A')
                tcf4_aa = 1 if tcf4 == 'A/A' else 0
                tcf4_at = 1 if tcf4 == 'A/T' else 0
                tcf4_tt = 1 if tcf4 == 'T/T' else 0
                
                cdh20 = registro.get('gen_cdh20', 'G/G')
                cdh20_aa = 1 if cdh20 == 'A/A' else 0
                cdh20_ag = 1 if cdh20 == 'G/A' else 0
                cdh20_gg = 1 if cdh20 == 'G/G' else 0
                
                features_dict = {
                    'EDAD24': edad24,
                    'AEFGROUPS': aefgroups,
                    'SF12F_Q1': sf12f_q1,
                    'SF12F_Q2': sf12f_q2,
                    'SF12F_Q3': sf12f_q3,
                    'SF12F_Q4': sf12f_q4,
                    'SF12M_Q1': sf12m_q1,
                    'SF12M_Q2': sf12m_q2,
                    'SF12M_Q3': sf12m_q3,
                    'SF12M_Q4': sf12m_q4,
                    'PRKCA_C/C': prkca_cc,
                    'PRKCA_C/T': prkca_ct,
                    'PRKCA_T/T': prkca_tt,
                    'TCF4_A/A': tcf4_aa,
                    'TCF4_A/T': tcf4_at,
                    'TCF4_T/T': tcf4_tt,
                    'CDH20_A/A': cdh20_aa,
                    'CDH20_A/G': cdh20_ag,
                    'CDH20_G/G': cdh20_gg,
                    'LTE12_0': lte12_0,
                    'LTE12_1': lte12_1,
                    'LTE12_2': lte12_2,
                }
                
                X = pd.DataFrame([features_dict])
                
                if hasattr(model, 'feature_names_in_'):
                    expected_features = list(model.feature_names_in_)
                    X = X[expected_features]
                
                # Predicción
                prediction = model.predict(X)[0]
                
                # Resultado
                if prediction == 1:
                    pred_text = "ALTO RIESGO DE ANSIEDAD"
                    pred_color = COLOR_PELIGRO
                    pred_bg = colors.HexColor('#FFE6E6')
                else:
                    pred_text = "BAJO RIESGO DE ANSIEDAD"
                    pred_color = COLOR_EXITO
                    pred_bg = colors.HexColor('#E6F7E6')
                
                pred_data = [[Paragraph(f'<b>{pred_text}</b><br/>Modelo utilizado: {model_name}', 
                    ParagraphStyle('PredText', alignment=TA_CENTER, fontSize=11, textColor=pred_color, leading=14))]]
                
                pred_table = Table(pred_data, colWidths=[6.5*inch])
                pred_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), pred_bg),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('BOX', (0, 0), (-1, -1), 2, pred_color),
                ]))
                
                elements.append(pred_table)
                elements.append(Spacer(1, 0.15*inch))
                
                # Información del modelo
                modelo_info = f"""
                <para fontSize="8" textColor="#666666" alignment="center">
                <b>Modelo:</b> {model_name} | 
                <b>Características analizadas:</b> {len(X.columns)} variables | 
                <b>Método:</b> Machine Learning con validación cruzada
                </para>
                """
                elements.append(Paragraph(modelo_info, normal_style))
                elements.append(Spacer(1, 0.1*inch))
                
                # Probabilidades
                if hasattr(model, 'predict_proba'):
                    prob = model.predict_proba(X)[0]
                    prob_data = [
                        ['Probabilidad de Alto Riesgo', 'Probabilidad de Bajo Riesgo'],
                        [f"{prob[1]:.2%}", f"{prob[0]:.2%}"]
                    ]
                    
                    prob_table = Table(prob_data, colWidths=[3.25*inch]*2)
                    prob_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACENTO),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('TOPPADDING', (0, 0), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), COLOR_FONDO),
                        ('BOX', (0, 0), (-1, -1), 1, COLOR_PRIMARIO),
                    ]))
                    
                    elements.append(prob_table)
                    elements.append(Spacer(1, 0.1*inch))
                    
                    # Gráfico de probabilidades (barra de progreso visual)
                    prob_visual = f"""
                    <para fontSize="9" textColor="#2E2E2E" alignment="center" spaceAfter="8">
                    <b>Distribución de Probabilidades:</b>
                    </para>
                    """
                    elements.append(Paragraph(prob_visual, normal_style))
                    
                    # Crear barra visual de probabilidad
                    prob_bar_data = [[
                        Paragraph(f'<font color="#DC3545"><b>Alto Riesgo</b></font><br/>{prob[1]:.1%}', 
                                 ParagraphStyle('ProbHigh', alignment=TA_CENTER, fontSize=9, leading=11)),
                        Paragraph(f'<font color="#4CAF50"><b>Bajo Riesgo</b></font><br/>{prob[0]:.1%}', 
                                 ParagraphStyle('ProbLow', alignment=TA_CENTER, fontSize=9, leading=11))
                    ]]
                    
                    # Ancho proporcional a la probabilidad
                    width_high = max(1, prob[1] * 6.5)  # Mínimo 1 inch
                    width_low = max(1, prob[0] * 6.5)
                    total_width = width_high + width_low
                    width_high = (width_high / total_width) * 6.5 * inch
                    width_low = (width_low / total_width) * 6.5 * inch
                    
                    prob_bar = Table(prob_bar_data, colWidths=[width_high, width_low])
                    prob_bar.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#FFE6E6')),
                        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#E6F7E6')),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('TOPPADDING', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                        ('BOX', (0, 0), (0, 0), 1.5, COLOR_PELIGRO),
                        ('BOX', (1, 0), (1, 0), 1.5, COLOR_EXITO),
                    ]))
                    
                    elements.append(prob_bar)
                    elements.append(Spacer(1, 0.1*inch))
                    
                    # Indicador de confianza
                    confianza = max(prob[0], prob[1])
                    if confianza >= 0.8:
                        conf_nivel = "MUY ALTA"
                        conf_color = COLOR_EXITO
                        conf_desc = "El modelo tiene muy alta confianza en esta predicción"
                    elif confianza >= 0.65:
                        conf_nivel = "ALTA"
                        conf_color = COLOR_ACENTO
                        conf_desc = "El modelo tiene alta confianza en esta predicción"
                    elif confianza >= 0.55:
                        conf_nivel = "MODERADA"
                        conf_color = COLOR_ALERTA
                        conf_desc = "El modelo tiene confianza moderada en esta predicción"
                    else:
                        conf_nivel = "BAJA"
                        conf_color = COLOR_PELIGRO
                        conf_desc = "El modelo tiene baja confianza en esta predicción"
                    
                    conf_text = f"""
                    <para fontSize="9" textColor="{conf_color.hexval()}" alignment="center" spaceAfter="5">
                    <b>Nivel de Confianza: {conf_nivel} ({confianza:.1%})</b>
                    </para>
                    <para fontSize="8" textColor="#666666" alignment="center">
                    {conf_desc}
                    </para>
                    """
                    elements.append(Paragraph(conf_text, normal_style))
                    elements.append(Spacer(1, 0.2*inch))
                
                # ==================== GRÁFICO SHAP ====================
                elements.append(Paragraph("5. EXPLICACIÓN DE LA PREDICCIÓN (SHAP)", heading_style))
                elements.append(Spacer(1, 0.1*inch))
                
                try:
                    import shap
                    from sklearn.neural_network import MLPClassifier
                    import lightgbm as lgb
                    
                    feature_names = list(X.columns)
                    X_array = X.values
                    
                    # Crear explainer
                    if isinstance(model, MLPClassifier):
                        background_data = np.random.choice([0, 1], size=(50, X.shape[1]), p=[0.7, 0.3])
                        explainer = shap.KernelExplainer(model.predict_proba, background_data, feature_names=feature_names)
                    else:
                        explainer = shap.TreeExplainer(model)
                    
                    shap_values = explainer.shap_values(X_array)
                    
                    if isinstance(shap_values, list):
                        shap_values = shap_values[1]
                    
                    if hasattr(shap_values, 'values'):
                        shap_array = shap_values.values
                    elif isinstance(shap_values, np.ndarray):
                        shap_array = shap_values
                    else:
                        shap_array = np.array(shap_values)
                    
                    if shap_array.ndim == 1:
                        shap_array = shap_array.reshape(1, -1)
                    elif shap_array.ndim == 3:
                        shap_array = shap_array[:, :, -1]
                    
                    # Generar gráfico SHAP minimalista
                    top_n = 10
                    top_indices = np.argsort(np.abs(shap_array[0]))[-top_n:][::-1]
                    top_shap_values = shap_array[0][top_indices]
                    top_feature_names = [feature_names[i] for i in top_indices]
                    
                    # Crear gráfico con estilo minimalista de salud
                    fig, ax = plt.subplots(figsize=(8, 5))
                    fig.patch.set_facecolor('white')
                    ax.set_facecolor('#F8F9FA')
                    
                    colors_bar = ['#DC3545' if val > 0 else '#4CAF50' for val in top_shap_values]
                    bars = ax.barh(range(len(top_shap_values)), top_shap_values, 
                                   color=colors_bar, alpha=0.85, edgecolor='#2C5F7C', linewidth=1)
                    
                    ax.set_yticks(range(len(top_shap_values)))
                    ax.set_yticklabels(top_feature_names, fontsize=9, color='#2E2E2E')
                    ax.set_xlabel('Contribución al Riesgo de Ansiedad', fontsize=10, 
                                 fontweight='bold', color='#2C5F7C')
                    ax.set_title('Factores más Influyentes en la Predicción', 
                                fontsize=11, fontweight='bold', color='#2C5F7C', pad=15)
                    ax.axvline(x=0, color='#2C5F7C', linestyle='-', linewidth=1.5)
                    ax.grid(axis='x', alpha=0.2, linestyle='--', color='#5DA5C8')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.spines['left'].set_color('#2C5F7C')
                    ax.spines['bottom'].set_color('#2C5F7C')
                    
                    plt.tight_layout()
                    
                    # Guardar gráfico
                    img_buffer = MatplotlibBytesIO()
                    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight', 
                               facecolor='white', edgecolor='none')
                    img_buffer.seek(0)
                    plt.close()
                    
                    # Agregar imagen al PDF
                    img = Image(img_buffer, width=6*inch, height=3.75*inch)
                    elements.append(img)
                    elements.append(Spacer(1, 0.2*inch))
                    
                    # Leyenda
                    leyenda = """
                    <para fontSize="8" textColor="#666666" alignment="center">
                    <b>Leyenda:</b> Barras rojas aumentan el riesgo | Barras verdes disminuyen el riesgo
                    </para>
                    """
                    elements.append(Paragraph(leyenda, normal_style))
                    elements.append(Spacer(1, 0.2*inch))
                    
                    elements.append(PageBreak())
                    
                    # ==================== INTERPRETACIÓN PERSONALIZADA ====================
                    elements.append(Paragraph("6. INTERPRETACIÓN PERSONALIZADA", heading_style))
                    elements.append(Spacer(1, 0.1*inch))
                    
                    intro_text = """
                    <para fontSize="9" textColor="#2E2E2E" alignment="justify">
                    A continuación se presenta una interpretación detallada de los factores más 
                    relevantes que el modelo de inteligencia artificial consideró para realizar 
                    la predicción del riesgo de ansiedad en este caso particular.
                    </para>
                    """
                    elements.append(Paragraph(intro_text, normal_style))
                    elements.append(Spacer(1, 0.15*inch))
                    
                    # Top 8 factores con interpretación
                    top_n_interp = 8
                    top_indices_interp = np.argsort(np.abs(shap_array[0]))[-top_n_interp:][::-1]
                    
                    for i, idx in enumerate(top_indices_interp, 1):
                        feature = feature_names[idx]
                        shap_val = shap_array[0][idx]
                        feature_val = X.iloc[0, idx]
                        
                        # Determinar color y efecto
                        if shap_val > 0:
                            color_dot = COLOR_PELIGRO
                            efecto = "AUMENTA"
                            simbolo = "▲"
                        else:
                            color_dot = COLOR_EXITO
                            efecto = "DISMINUYE"
                            simbolo = "▼"
                        
                        # Obtener interpretación
                        interpretacion = obtener_interpretacion_feature(feature, feature_val)
                        
                        # Crear tarjeta de interpretación minimalista
                        interp_data = [[
                            Paragraph(f'<b>{simbolo} Factor {i}: {feature}</b>', 
                                     ParagraphStyle('FactorTitle', fontSize=9, textColor=color_dot, leading=11)),
                            Paragraph(interpretacion, 
                                     ParagraphStyle('FactorDesc', fontSize=8, textColor=COLOR_TEXTO, leading=10)),
                            Paragraph(f'<b>Impacto:</b> {efecto} el riesgo en {abs(shap_val):.4f} unidades', 
                                     ParagraphStyle('FactorImpact', fontSize=8, textColor='#666666', leading=10))
                        ]]
                        
                        interp_table = Table(interp_data, colWidths=[6.5*inch])
                        interp_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, -1), COLOR_FONDO),
                            ('TOPPADDING', (0, 0), (-1, -1), 6),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                            ('LEFTPADDING', (0, 0), (-1, -1), 10),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('LINEBELOW', (0, 0), (-1, 0), 2, color_dot),
                            ('BOX', (0, 0), (-1, -1), 0.5, COLOR_SECUNDARIO),
                        ]))
                        
                        elements.append(interp_table)
                        elements.append(Spacer(1, 0.08*inch))
                    
                except Exception as e:
                    elements.append(Paragraph(f"No se pudo generar el análisis SHAP: {str(e)}", normal_style))
                
                # ==================== DATAFRAME COMPLETO ====================
                elements.append(PageBreak())
                elements.append(Paragraph("7. DATAFRAME COMPLETO DE LA EVALUACIÓN", heading_style))
                elements.append(Spacer(1, 0.1*inch))
                
                # Obtener todos los datos del registro
                if registro:
                    # Crear tabla con todos los datos del DataFrame
                    df_intro = """
                    <para fontSize="9" textColor="#2E2E2E" alignment="justify">
                    A continuación se presenta el conjunto completo de datos procesados utilizados 
                    por el modelo de inteligencia artificial. Estos datos incluyen todas las transformaciones 
                    y codificaciones necesarias para la predicción.
                    </para>
                    """
                    elements.append(Paragraph(df_intro, normal_style))
                    elements.append(Spacer(1, 0.15*inch))
                    
                    # Datos organizados por categorías
                    df_sections = [
                        ("Datos Demográficos Procesados", [
                            ("Edad", registro.get('edad', 'N/A')),
                            ("Grupo Edad (24-34 años)", "Sí" if registro.get('grupo_edad', 0) == 1 else "No"),
                            ("Género", "Masculino" if registro.get('genero', 0) == 0 else "Femenino"),
                            ("Años Educación", registro.get('años_educacion', 'N/A')),
                            ("Educación Binaria (≥15 años)", "Sí" if registro.get('educacion_binaria', 0) == 1 else "No"),
                        ]),
                        ("Eventos Vitales (LTE-12)", [
                            ("Puntaje LTE-12", registro.get('lte12_puntaje', 'N/A')),
                            ("Clasificación LTE-12", registro.get('lte12_clasificacion', 'N/A')),
                        ]),
                        ("Salud Física (SF-12)", [
                            ("Puntaje SF-12 Física", f"{registro.get('sf12_fisica', 0):.1f}"),
                            ("Cuartil SF-12 Física", registro.get('sf12_fisica_cuartil', 'N/A')),
                        ]),
                        ("Salud Mental (SF-12)", [
                            ("Puntaje SF-12 Mental", f"{registro.get('sf12_mental', 0):.1f}"),
                            ("Cuartil SF-12 Mental", registro.get('sf12_mental_cuartil', 'N/A')),
                        ]),
                        ("Evaluación HADS", [
                            ("Puntaje HADS", registro.get('hads_puntaje', 'N/A')),
                            ("Nivel HADS", registro.get('hads_nivel', 'N/A')),
                        ]),
                        ("Evaluación ZSAS", [
                            ("Puntaje ZSAS Bruto", registro.get('zsas_puntaje', 'N/A')),
                            ("Puntaje ZSAS Normalizado", f"{registro.get('zsas_normalizado', 0):.1f}"),
                            ("Nivel ZSAS", registro.get('zsas_nivel', 'N/A')),
                        ]),
                        ("Perfil Genético", [
                            ("Gen PRKCA", registro.get('gen_prkca', 'N/A')),
                            ("Gen TCF4", registro.get('gen_tcf4', 'N/A')),
                            ("Gen CDH20", registro.get('gen_cdh20', 'N/A')),
                        ]),
                        ("Clasificación Final", [
                            ("HADS-ZSAS Clasificación", "Alto Riesgo (1)" if registro.get('hads_zsas_clasificacion', 0) == 1 else "Bajo Riesgo (0)"),
                        ]),
                    ]
                    
                    for section_title, section_data in df_sections:
                        # Título de sección
                        elements.append(Paragraph(f"<b>{section_title}</b>", 
                            ParagraphStyle('DFSection', fontSize=10, textColor=COLOR_SECUNDARIO, 
                                         spaceAfter=5, leading=12)))
                        
                        # Tabla de datos
                        table_data = [['Campo', 'Valor']]
                        for campo, valor in section_data:
                            table_data.append([campo, str(valor)])
                        
                        df_table = Table(table_data, colWidths=[3.5*inch, 3*inch])
                        df_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), COLOR_ACENTO),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                            ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, -1), 8),
                            ('TOPPADDING', (0, 0), (-1, -1), 5),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                            ('BACKGROUND', (0, 1), (-1, -1), COLOR_FONDO),
                            ('BOX', (0, 0), (-1, -1), 0.5, COLOR_SECUNDARIO),
                            ('LINEABOVE', (0, 1), (-1, -1), 0.25, COLOR_SECUNDARIO),
                        ]))
                        
                        elements.append(df_table)
                        elements.append(Spacer(1, 0.1*inch))
                
            except Exception as e:
                elements.append(Paragraph(f"Error en la predicción: {str(e)}", normal_style))
        
        elements.append(PageBreak())
        
        # ==================== NOTA FINAL ====================
        elements.append(Paragraph("CONSIDERACIONES CLÍNICAS", heading_style))
        elements.append(Spacer(1, 0.1*inch))
        
        nota_final = """
        <para fontSize="9" textColor="#2E2E2E" alignment="justify" spaceBefore="5" spaceAfter="5">
        <b>Importante:</b> Esta evaluación es una herramienta de apoyo preliminar y no constituye 
        un diagnóstico clínico definitivo. Los resultados presentados deben ser interpretados 
        por un profesional de la salud mental calificado, quien considerará el contexto clínico 
        completo del paciente, incluyendo historia médica, síntomas actuales y otros factores 
        relevantes.
        </para>
        <para fontSize="9" textColor="#2E2E2E" alignment="justify" spaceBefore="5" spaceAfter="5">
        <b>Recomendación:</b> Se sugiere que este reporte sea revisado durante una consulta 
        con un psicólogo, psiquiatra u otro profesional de salud mental especializado, quien 
        podrá realizar una evaluación integral y proporcionar el tratamiento o seguimiento 
        adecuado según sea necesario.
        </para>
        <para fontSize="9" textColor="#2E2E2E" alignment="justify" spaceBefore="5">
        <b>Confidencialidad:</b> La información contenida en este documento es estrictamente 
        confidencial y está protegida por las leyes de privacidad médica aplicables.
        </para>
        """
        
        nota_box_data = [[Paragraph(nota_final, normal_style)]]
        nota_box = Table(nota_box_data, colWidths=[6.5*inch])
        nota_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF9E6')),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('BOX', (0, 0), (-1, -1), 2, COLOR_ALERTA),
        ]))
        
        elements.append(nota_box)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer final
        footer_text = f"""
        <para fontSize="8" textColor="#999999" alignment="center">
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br/>
        <b>Sistema ANXRISK</b> | Evaluación de Riesgo de Ansiedad<br/>
        Documento generado el {datetime.now().strftime('%d de %B de %Y a las %H:%M hrs')}<br/>
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        </para>
        """
        elements.append(Paragraph(footer_text, subtitle_style))
        
        # Construir PDF
        doc.build(elements)
        
        # Obtener bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
        
    except ImportError as ie:
        print(f"Error de importación: {str(ie)}")
        return None
    except Exception as e:
        print(f"Error generando PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    """Genera PDF completo para exportar usando ReportLab"""
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # Contenedor de elementos
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4CAF50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#4CAF50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY
        )
        
        # Título
        elements.append(Paragraph("📊 Reporte de Evaluación de Ansiedad", title_style))
        elements.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Datos Demográficos
        demo_data = resultados.get('datos_demograficos') or st.session_state.get('datos_demograficos')
        if demo_data:
            # Verificar si genero es número o texto
            if isinstance(demo_data.get('genero'), int):
                genero_txt = "Masculino" if demo_data['genero'] == 0 else "Femenino"
            else:
                genero_txt = demo_data.get('genero', 'No especificado')
            
            elements.append(Paragraph("👤 Datos Demográficos", heading_style))
            
            demo_table_data = [
                ['Edad', 'Género', 'Educación'],
                [f"{demo_data['edad']} años", genero_txt, f"{demo_data['años_educacion']} años"]
            ]
            
            demo_table = Table(demo_table_data, colWidths=[2*inch, 2*inch, 2*inch])
            demo_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(demo_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Eventos Vitales
        if 'eventos_vitales' in resultados:
            eventos = resultados['eventos_vitales']
            elements.append(Paragraph("📅 Eventos Vitales (LTE-12)", heading_style))
            elements.append(Paragraph(f"Eventos estresantes: <b>{eventos['total']}</b> eventos significativos", normal_style))
            elements.append(Spacer(1, 0.2*inch))
        
        # SF-12
        if 'sf12_fisica' in resultados or 'sf12_mental' in resultados:
            elements.append(Paragraph("🏥 Salud Física y Mental (SF-12)", heading_style))
            sf12_data = [['Componente', 'Puntaje']]
            
            if 'sf12_fisica' in resultados:
                sf12_fisica = resultados['sf12_fisica']
                sf12_data.append(['Componente Físico', f"{sf12_fisica.get('puntaje', 0):.1f}"])
            
            if 'sf12_mental' in resultados:
                sf12_mental = resultados['sf12_mental']
                sf12_data.append(['Componente Mental', f"{sf12_mental.get('puntaje', 0):.1f}"])
            
            sf12_table = Table(sf12_data, colWidths=[3*inch, 3*inch])
            sf12_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(sf12_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # HADS
        if 'hads' in resultados:
            hads = resultados['hads']
            elements.append(Paragraph("😰 Ansiedad HADS", heading_style))
            
            hads_data = [
                ['Puntaje', 'Nivel'],
                [str(hads['puntaje']), hads['nivel']]
            ]
            
            hads_table = Table(hads_data, colWidths=[3*inch, 3*inch])
            hads_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(hads_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # ZSAS
        if 'zsas' in resultados:
            zsas = resultados['zsas']
            elements.append(Paragraph("😟 Ansiedad de Zung (ZSAS)", heading_style))
            
            zsas_data = [
                ['Puntaje Bruto', 'Índice Normalizado', 'Nivel'],
                [str(zsas['total']), f"{zsas['total_normalizado']:.1f}", zsas['nivel']]
            ]
            
            zsas_table = Table(zsas_data, colWidths=[2*inch, 2*inch, 2*inch])
            zsas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(zsas_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Datos Genéticos
        if 'datos_geneticos' in resultados:
            gen = resultados['datos_geneticos']
            elements.append(Paragraph("🧬 Perfil Genético", heading_style))
            
            gen_data = [
                ['Gen PRKCA', 'Gen TCF4', 'Gen CDH20'],
                [gen['prkca'], gen['tcf4'], gen['cdh20']]
            ]
            
            gen_table = Table(gen_data, colWidths=[2*inch, 2*inch, 2*inch])
            gen_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(gen_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Clasificación
        if registro:
            clasificacion = registro.get('hads_zsas_clasificacion')
            elements.append(Paragraph("📊 Clasificación de Ansiedad", heading_style))
            
            if clasificacion == 1:
                clasif_text = "<b>Alto Riesgo (1)</b><br/>HADS ≥ 8 y ZSAS ≥ 36"
                clasif_color = colors.HexColor('#FFE6E6')
            elif clasificacion == 0:
                clasif_text = "<b>Bajo Riesgo (0)</b><br/>HADS &lt; 8 o ZSAS &lt; 36"
                clasif_color = colors.HexColor('#E6F7E6')
            else:
                clasif_text = "<b>No disponible</b><br/>Datos insuficientes"
                clasif_color = colors.HexColor('#FFF3CD')
            
            clasif_data = [['Clasificación'], [clasif_text]]
            clasif_table = Table(clasif_data, colWidths=[6*inch])
            clasif_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), clasif_color),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            elements.append(clasif_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Nota final
        elements.append(PageBreak())
        warning_style = ParagraphStyle(
            'Warning',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#856404'),
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            backColor=colors.HexColor('#FFF3CD'),
            borderPadding=10
        )
        
        elements.append(Paragraph("⚠️ <b>Nota importante:</b>", warning_style))
        elements.append(Paragraph(
            "Esta evaluación es preliminar y debe ser interpretada por un profesional de la salud. "
            "Los resultados no constituyen un diagnóstico definitivo. Se recomienda consultar con un especialista "
            "en salud mental para una evaluación completa y personalizada.",
            warning_style
        ))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("Reporte generado automáticamente por el Sistema de Evaluación de Ansiedad ANXRISK", footer_style))
        elements.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", footer_style))
        
        # Construir PDF
        doc.build(elements)
        
        # Obtener bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
        
    except ImportError:
        # Si reportlab no está instalado, retornar None
        return None
    except Exception as e:
        # Si hay cualquier otro error, retornar None
        print(f"Error generando PDF: {str(e)}")
        return None

