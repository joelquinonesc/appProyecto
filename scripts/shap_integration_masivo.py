"""
Integración de SHAP en Análisis Masivos
========================================
Calcula valores SHAP para las 5 características más importantes
y las integra directamente en los resultados sin generar gráficas.
"""

import pandas as pd
import numpy as np
import joblib
import shap
import warnings
warnings.filterwarnings('ignore')

def procesar_datos_para_modelo(df):
    """Procesa datos para que coincidan con el formato del modelo"""
    features_list = []
    
    for idx, row in df.iterrows():
        edad24 = 0 if row['edad'] <= 24 else 1
        aefgroups = 0 if row['años_educacion'] <= 14 else 1
        
        # LTE-12 con One-Hot Encoding (0 eventos, 1 evento, 2+ eventos)
        lte12_count = row['lte12_count']
        lte12_0 = 1 if lte12_count == 0 else 0
        lte12_1 = 1 if lte12_count == 1 else 0
        lte12_2 = 1 if lte12_count >= 2 else 0
        
        # SF-12 Física - Cuartiles
        sf12f_raw = row['sf12_fisica']
        sf12f_q1 = 1 if sf12f_raw <= 15 else 0
        sf12f_q2 = 1 if 15 < sf12f_raw <= 17 else 0
        sf12f_q3 = 1 if 17 < sf12f_raw <= 19 else 0
        sf12f_q4 = 1 if sf12f_raw > 19 else 0
        
        # SF-12 Mental - Cuartiles
        sf12m_raw = row['sf12_mental']
        sf12m_q1 = 1 if sf12m_raw <= 15 else 0
        sf12m_q2 = 1 if 15 < sf12m_raw <= 18 else 0
        sf12m_q3 = 1 if 18 < sf12m_raw <= 21 else 0
        sf12m_q4 = 1 if sf12m_raw > 21 else 0
        
        # Genotipos - One-Hot Encoding
        prkca = row['prkca']
        prkca_cc = 1 if prkca == 'C/C' else 0
        prkca_ct = 1 if prkca == 'C/T' else 0
        prkca_tt = 1 if prkca == 'T/T' else 0
        
        tcf4 = row['tcf4']
        tcf4_aa = 1 if tcf4 == 'A/A' else 0
        tcf4_at = 1 if tcf4 == 'A/T' else 0
        tcf4_tt = 1 if tcf4 == 'T/T' else 0
        
        cdh20 = row['cdh20']
        cdh20_aa = 1 if cdh20 == 'A/A' else 0
        cdh20_ag = 1 if cdh20 == 'A/G' else 0
        cdh20_gg = 1 if cdh20 == 'G/G' else 0
        
        # ORDEN EXACTO DEL MODELO
        features = [
            edad24, aefgroups,
            lte12_0, lte12_1, lte12_2,
            sf12f_q1, sf12f_q2, sf12f_q3, sf12f_q4,
            sf12m_q1, sf12m_q2, sf12m_q3, sf12m_q4,
            prkca_cc, prkca_ct, prkca_tt,
            tcf4_aa, tcf4_at, tcf4_tt,
            cdh20_aa, cdh20_ag, cdh20_gg
        ]
        
        features_list.append(features)
    
    feature_names = [
        'EDAD24', 'AEFGROUPS',
        'LTE12_0', 'LTE12_1', 'LTE12_2',
        'SF12F_Q1', 'SF12F_Q2', 'SF12F_Q3', 'SF12F_Q4',
        'SF12M_Q1', 'SF12M_Q2', 'SF12M_Q3', 'SF12M_Q4',
        'PRKCA_C/C', 'PRKCA_C/T', 'PRKCA_T/T',
        'TCF4_A/A', 'TCF4_A/T', 'TCF4_T/T',
        'CDH20_A/A', 'CDH20_A/G', 'CDH20_G/G'
    ]
    
    X = pd.DataFrame(features_list, columns=feature_names)
    return X

def calcular_shap_values(model, X_background, X_test):
    """Calcula valores SHAP para los datos de prueba"""
    print("🤖 Calculando valores SHAP...")
    
    # Usar TreeExplainer si es posible (mucho más rápido), si no usar KernelExplainer
    try:
        # Intentar con TreeExplainer (para modelos basados en árboles)
        explainer = shap.TreeExplainer(model)
        print("   ✓ Usando TreeExplainer (rápido)")
        shap_values = explainer.shap_values(X_test)
        # Si devuelve lista [clase_0, clase_1] → tomamos clase 1
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
    except:
        try:
            # KernelExplainer con P(clase=1) para Naive Bayes y otros
            explainer = shap.KernelExplainer(
                lambda x: model.predict_proba(x)[:, 1], X_background
            )
            print("   ✓ Usando KernelExplainer (predict_proba clase 1)")
        except:
            # Fallback: usar permutation explainer (más simple)
            explainer = shap.PermutationExplainer(model.predict, X_background)
            print("   ✓ Usando PermutationExplainer")
        shap_values = explainer.shap_values(X_test)
    
    # Asegurar que sea 2D (n_muestras, n_features)
    shap_values = np.array(shap_values)
    if shap_values.ndim == 3:
        shap_values = shap_values[:, :, -1]
    
    return explainer, shap_values

def obtener_top5_caracteristicas(X, shap_values):
    """Obtiene las 10 características más importantes según SHAP"""
    # Calcular importancia promedio
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    
    # Top 10
    top_n = min(10, len(X.columns))  # Usar 10 o menos si hay menos features
    top10_idx = np.argsort(mean_abs_shap)[-top_n:][::-1]
    top10_names = [X.columns[i] for i in top10_idx]
    top10_importance = mean_abs_shap[top10_idx]
    
    return top10_idx, top10_names, top10_importance, mean_abs_shap

def crear_columnas_shap_para_resultados(df_resultados, X, shap_values, top10_idx):
    """
    Crea nuevas columnas en el dataframe de resultados con los valores SHAP
    de las 10 características más importantes para cada paciente
    """
    top10_names = [X.columns[i] for i in top10_idx]
    
    # Para cada una de las top 10, agregar una columna con su valor SHAP
    for i, feat_idx in enumerate(top10_idx):
        col_name = f"SHAP_{top10_names[i]}"
        df_resultados[col_name] = shap_values[:, feat_idx].round(4)
    
    return df_resultados, top10_names

def generar_resumen_shap(X, shap_values, top10_idx, top10_names, top10_importance):
    """Genera un resumen de importancia SHAP"""
    print("\n" + "="*80)
    print("📊 TOP 10 CARACTERÍSTICAS MÁS IMPORTANTES (SHAP)")
    print("="*80)
    
    for i, (idx, name, importance) in enumerate(zip(top10_idx, top10_names, top10_importance)):
        percentage = (importance / np.abs(shap_values).mean(axis=0).sum() * 100)
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        print(f"{i+1:2}. {name:20} │ {bar:25} │ {percentage:6.2f}% │ SHAP: {importance:.4f}")
    
    return {
        'top10_names': top10_names,
        'top10_importance': top10_importance.tolist()
    }

def main_shap_integration(df):
    """
    Función principal para integrar SHAP en análisis masivos
    Retorna los valores SHAP para agregar a los resultados
    """
    try:
        print("\n📦 Cargando modelo...")
        model = joblib.load('src/models/anxrisk_best_extended.joblib')
        print("✅ Modelo cargado")
        
        # Procesar datos
        print("📝 Procesando datos...")
        X = procesar_datos_para_modelo(df)
        print("✅ Datos procesados")
        
        # Calcular SHAP con background reducido para mayor velocidad
        # Usar solo 30 muestras de background para acelerar (sufficient para aproximación)
        print("⏳ Calculando valores SHAP (esto toma ~15-30 segundos)...")
        background_size = min(30, max(5, len(X) // 3))
        X_background = shap.sample(X, background_size)
        explainer, shap_values = calcular_shap_values(model, X_background, X)
        print("✅ Valores SHAP calculados")
        
        # Obtener top 10
        top10_idx, top10_names, top10_importance, mean_abs_shap = obtener_top5_caracteristicas(X, shap_values)
        
        # Generar resumen
        resumen = generar_resumen_shap(X, shap_values, top10_idx, top10_names, top10_importance)
        
        # Crear columnas para resultados
        df_with_shap, top10_names_final = crear_columnas_shap_para_resultados(df.copy(), X, shap_values, top10_idx)
        
        print("✅ Integración SHAP completada\n")
        
        return {
            'df_with_shap': df_with_shap,
            'top10_names': top10_names_final,
            'top10_importance': top10_importance.tolist(),
            'resumen': resumen,
            'shap_values': shap_values,
            'X': X
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test
    print("Testing SHAP integration...")
    df = pd.read_csv('datos_simulados_100_participantes.csv')
    resultado = main_shap_integration(df.head(10))  # Test con 10 pacientes
    
    if resultado:
        print("\n✅ Resultado de prueba:")
        print(f"Top 5 características: {resultado['top5_names']}")
        print(f"Dataframe con SHAP:\n{resultado['df_with_shap'].head()}")
