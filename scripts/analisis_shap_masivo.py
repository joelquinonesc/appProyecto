"""
Análisis SHAP Completo para Análisis Masivos
==============================================
Genera visualizaciones SHAP para entender la importancia de cada característica
en las predicciones del modelo CatBoost para análisis masivos.
"""

import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
from matplotlib import rcParams
import warnings
warnings.filterwarnings('ignore')

# Configuración de matplotlib
rcParams['figure.figsize'] = (14, 8)
rcParams['font.size'] = 10

def cargar_modelo_y_datos():
    """Carga el modelo y los datos de prueba"""
    print("\n" + "="*80)
    print("ANÁLISIS SHAP - ANÁLISIS MASIVOS (22 CARACTERÍSTICAS)")
    print("="*80)
    
    # Cargar modelo
    print("\n📦 Cargando modelo CatBoost...")
    model = joblib.load('src/models/anxrisk_best_extended.joblib')
    
    # Cargar datos simulados
    print("📊 Cargando datos simulados...")
    df = pd.read_csv('datos_simulados_100_participantes.csv')
    
    print(f"✅ Modelo cargado: {type(model).__name__}")
    print(f"✅ Datos cargados: {len(df)} participantes")
    
    return model, df

def procesar_datos_para_modelo(df):
    """Procesa datos para que coincidan con el formato del modelo"""
    print("\n📝 Procesando datos para el modelo...")
    
    # Crear lista para almacenar features
    features_list = []
    
    # Diccionario de órdenes canónico (EXACTO del modelo)
    for idx, row in df.iterrows():
        edad24 = 1 if row['edad'] >= 24 else 0
        aefgroups = 1 if row['años_educacion'] >= 12 else 0
        
        # LTE-12 con One-Hot Encoding (0-2 eventos, 3-5 eventos, 6+ eventos)
        lte12_count = row['lte12_count']
        lte12_0 = 1 if lte12_count <= 2 else 0
        lte12_1 = 1 if 3 <= lte12_count <= 5 else 0
        lte12_2 = 1 if lte12_count >= 6 else 0
        
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
        
        # ORDEN EXACTO DEL MODELO: EDAD24, AEFGROUPS, LTE12_0-2, SF12F_Q1-Q4, SF12M_Q1-Q4, PRKCA, TCF4, CDH20
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
    
    # Crear DataFrame con nombres de características (EXACTO al modelo)
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
    
    print(f"✅ Datos procesados: {X.shape[0]} pacientes × {X.shape[1]} características")
    print(f"✅ Características: {', '.join(X.columns)}")
    
    return X

def crear_explicador_shap(model, X):
    """Crea el explicador SHAP"""
    print("\n🤖 Creando explicador SHAP...")
    print("⏳ Esto puede tardar 1-2 minutos...")
    
    # Usar KernelExplainer para máxima compatibilidad
    explainer = shap.KernelExplainer(model.predict, shap.sample(X, min(100, len(X))))
    
    # Calcular valores SHAP para todos los datos
    shap_values = explainer.shap_values(X)
    
    print("✅ Explicador SHAP creado exitosamente")
    
    return explainer, shap_values

def generar_visualizaciones_shap(model, X, explainer, shap_values, output_dir='./'):
    """Genera todas las visualizaciones SHAP"""
    print("\n📊 Generando visualizaciones SHAP...")
    
    # 1. FORCE PLOT - Primeros 5 pacientes
    print("  1️⃣  Force plot (primeros 5 pacientes)...")
    plt.figure(figsize=(16, 10))
    for i in range(min(5, len(X))):
        plt.subplot(5, 1, i+1)
        shap.force_plot(explainer.expected_value, shap_values[i], X.iloc[i], matplotlib=True)
    plt.tight_layout()
    plt.savefig(f'{output_dir}shap_force_plots_top5.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("     ✅ Guardado: shap_force_plots_top5.png")
    
    # 2. SUMMARY PLOT (Bar - Importancia promedio)
    print("  2️⃣  Summary plot (importancia por característica)...")
    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X, plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig(f'{output_dir}shap_summary_bar.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("     ✅ Guardado: shap_summary_bar.png")
    
    # 3. SUMMARY PLOT (Violin - Distribución de impacto)
    print("  3️⃣  Summary plot (distribución de impacto)...")
    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values, X, plot_type="violin", show=False)
    plt.tight_layout()
    plt.savefig(f'{output_dir}shap_summary_violin.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("     ✅ Guardado: shap_summary_violin.png")
    
    # 4. DEPENDENCE PLOTS - Top 6 características
    print("  4️⃣  Dependence plots (relación característica-predicción)...")
    
    # Calcular importancia promedio
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    top_features_idx = np.argsort(mean_abs_shap)[-6:][::-1]
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    
    for idx, feat_idx in enumerate(top_features_idx):
        shap.dependence_plot(feat_idx, shap_values, X, ax=axes[idx], show=False)
        axes[idx].set_title(f'Dependencia: {X.columns[feat_idx]}', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}shap_dependence_top6.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("     ✅ Guardado: shap_dependence_top6.png")
    
    # 5. WATERFALL PLOT - Paciente de mayor riesgo
    print("  5️⃣  Waterfall plot (explicación paciente de alto riesgo)...")
    predictions = model.predict(X)
    high_risk_idx = np.argmax(predictions)
    
    plt.figure(figsize=(12, 8))
    shap.waterfall_plot(shap.Explanation(shap_values[high_risk_idx], 
                                         explainer.expected_value, 
                                         X.iloc[high_risk_idx],
                                         feature_names=X.columns), 
                       show=False)
    plt.tight_layout()
    plt.savefig(f'{output_dir}shap_waterfall_high_risk.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("     ✅ Guardado: shap_waterfall_high_risk.png")
    
    # 6. WATERFALL PLOT - Paciente de menor riesgo
    print("  6️⃣  Waterfall plot (explicación paciente de bajo riesgo)...")
    low_risk_idx = np.argmin(predictions)
    
    plt.figure(figsize=(12, 8))
    shap.waterfall_plot(shap.Explanation(shap_values[low_risk_idx], 
                                         explainer.expected_value, 
                                         X.iloc[low_risk_idx],
                                         feature_names=X.columns), 
                       show=False)
    plt.tight_layout()
    plt.savefig(f'{output_dir}shap_waterfall_low_risk.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("     ✅ Guardado: shap_waterfall_low_risk.png")
    
    # 7. HEATMAP - Interacciones entre características
    print("  7️⃣  Heatmap SHAP (matriz de valores)...")
    plt.figure(figsize=(14, 10))
    shap.summary_plot(shap_values, X, plot_type="heatmap", max_display=22, show=False)
    plt.tight_layout()
    plt.savefig(f'{output_dir}shap_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("     ✅ Guardado: shap_heatmap.png")

def analizar_importancia_caracteristicas(model, X, shap_values):
    """Analiza e imprime la importancia de características"""
    print("\n" + "="*80)
    print("📊 ANÁLISIS DE IMPORTANCIA DE CARACTERÍSTICAS")
    print("="*80)
    
    # Calcular importancia promedio
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    
    # Ordenar por importancia
    feature_importance = pd.DataFrame({
        'Característica': X.columns,
        'SHAP Promedio': mean_abs_shap,
        'Importancia (%)': (mean_abs_shap / mean_abs_shap.sum() * 100).round(2)
    }).sort_values('SHAP Promedio', ascending=False)
    
    print("\n🏆 TOP 15 CARACTERÍSTICAS MÁS IMPORTANTES:")
    print("-" * 80)
    for i, row in feature_importance.head(15).iterrows():
        bar_length = int(row['Importancia (%)'] / 2)
        bar = "█" * bar_length
        print(f"{row['Característica']:20} │ {bar:25} │ {row['Importancia (%)']:6.2f}% │ SHAP: {row['SHAP Promedio']:.4f}")
    
    print("\n📋 RANKING COMPLETO (22 CARACTERÍSTICAS):")
    print("-" * 80)
    print(feature_importance.to_string(index=False))
    
    # Agrupar por categoría
    print("\n\n🔍 ANÁLISIS POR CATEGORÍA:")
    print("-" * 80)
    
    categorias = {
        'Demográficas': ['EDAD24', 'AEFGROUPS'],
        'Eventos Vitales (LTE-12)': ['LTE12_0-2', 'LTE12_3-5', 'LTE12_6+'],
        'SF-12 Física': ['SF12F_Q1', 'SF12F_Q2', 'SF12F_Q3', 'SF12F_Q4'],
        'SF-12 Mental': ['SF12M_Q1', 'SF12M_Q2', 'SF12M_Q3', 'SF12M_Q4'],
        'PRKCA (Genotipo)': ['PRKCA_C/C', 'PRKCA_C/T', 'PRKCA_T/T'],
        'TCF4 (Genotipo)': ['TCF4_A/A', 'TCF4_A/T', 'TCF4_T/T'],
        'CDH20 (Genotipo)': ['CDH20_A/A', 'CDH20_A/G', 'CDH20_G/G']
    }
    
    for categoria, features in categorias.items():
        features_df = feature_importance[feature_importance['Característica'].isin(features)]
        importancia_total = features_df['Importancia (%)'].sum()
        shap_total = features_df['SHAP Promedio'].sum()
        
        print(f"\n{categoria}:")
        print(f"  Importancia Total: {importancia_total:.2f}%")
        print(f"  SHAP Promedio: {shap_total:.4f}")
        for _, row in features_df.iterrows():
            print(f"    • {row['Característica']:20} {row['Importancia (%)']:6.2f}% (SHAP: {row['SHAP Promedio']:.4f})")
    
    return feature_importance

def generar_reporte_html(X, model, feature_importance, output_file='shap_reporte_masivo.html'):
    """Genera un reporte HTML con todos los análisis"""
    print(f"\n📄 Generando reporte HTML: {output_file}...")
    
    predictions = model.predict(X)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Análisis SHAP - Análisis Masivos</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
                color: #333;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 30px;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 15px;
                text-align: center;
            }}
            h2 {{
                color: #34495e;
                margin-top: 30px;
                border-left: 4px solid #3498db;
                padding-left: 15px;
            }}
            .stats {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin: 20px 0;
            }}
            .stat-box {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
            }}
            .stat-box h3 {{
                margin: 0;
                font-size: 14px;
                opacity: 0.9;
            }}
            .stat-box .value {{
                font-size: 28px;
                font-weight: bold;
                margin: 10px 0 0 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            th {{
                background-color: #3498db;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }}
            td {{
                padding: 12px;
                border-bottom: 1px solid #ecf0f1;
            }}
            tr:hover {{
                background-color: #f9f9f9;
            }}
            .progress-bar {{
                background-color: #ecf0f1;
                height: 24px;
                border-radius: 4px;
                overflow: hidden;
            }}
            .progress-fill {{
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                height: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 12px;
                font-weight: bold;
                transition: width 0.3s ease;
            }}
            .category-section {{
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
                border-left: 4px solid #3498db;
            }}
            .visualization {{
                text-align: center;
                margin: 30px 0;
            }}
            .visualization img {{
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            .visualization p {{
                color: #7f8c8d;
                font-size: 14px;
                margin-top: 10px;
            }}
            .footer {{
                text-align: center;
                color: #95a5a6;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ecf0f1;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Análisis SHAP - Análisis Masivos (22 Características)</h1>
            
            <div class="stats">
                <div class="stat-box">
                    <h3>Pacientes Analizados</h3>
                    <div class="value">{len(X)}</div>
                </div>
                <div class="stat-box">
                    <h3>Características</h3>
                    <div class="value">{X.shape[1]}</div>
                </div>
                <div class="stat-box">
                    <h3>Riesgo Promedio</h3>
                    <div class="value">{predictions.mean():.1%}</div>
                </div>
                <div class="stat-box">
                    <h3>Riesgo Máximo</h3>
                    <div class="value">{predictions.max():.1%}</div>
                </div>
            </div>
            
            <h2>📊 Top 15 Características Más Importantes</h2>
            <table>
                <thead>
                    <tr>
                        <th>Característica</th>
                        <th>Importancia SHAP (%)</th>
                        <th>Visualización</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for i, (_, row) in enumerate(feature_importance.head(15).iterrows()):
        percentage = row['Importancia (%)']
        html_content += f"""
                    <tr>
                        <td><strong>{row['Característica']}</strong></td>
                        <td>{percentage:.2f}%</td>
                        <td>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: {percentage}%">
                                    {percentage:.1f}%
                                </div>
                            </div>
                        </td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
            
            <h2>🏷️ Análisis por Categoría</h2>
    """
    
    categorias = {
        'Demográficas': ['EDAD24', 'AEFGROUPS'],
        'Eventos Vitales (LTE-12)': ['LTE12_0-2', 'LTE12_3-5', 'LTE12_6+'],
        'SF-12 Física': ['SF12F_Q1', 'SF12F_Q2', 'SF12F_Q3', 'SF12F_Q4'],
        'SF-12 Mental': ['SF12M_Q1', 'SF12M_Q2', 'SF12M_Q3', 'SF12M_Q4'],
        'PRKCA': ['PRKCA_C/C', 'PRKCA_C/T', 'PRKCA_T/T'],
        'TCF4': ['TCF4_A/A', 'TCF4_A/T', 'TCF4_T/T'],
        'CDH20': ['CDH20_A/A', 'CDH20_A/G', 'CDH20_G/G']
    }
    
    for categoria, features in categorias.items():
        features_df = feature_importance[feature_importance['Característica'].isin(features)]
        importancia_total = features_df['Importancia (%)'].sum()
        
        html_content += f"""
            <div class="category-section">
                <h3>{categoria}</h3>
                <p><strong>Importancia Total: {importancia_total:.2f}%</strong></p>
                <table>
                    <thead>
                        <tr>
                            <th>Característica</th>
                            <th>Importancia (%)</th>
                            <th>Visualización</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for _, row in features_df.iterrows():
            percentage = row['Importancia (%)']
            html_content += f"""
                        <tr>
                            <td>{row['Característica']}</td>
                            <td>{percentage:.2f}%</td>
                            <td>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: {percentage * 4}%">
                                        {percentage:.1f}%
                                    </div>
                                </div>
                            </td>
                        </tr>
            """
        
        html_content += """
                    </tbody>
                </table>
            </div>
        """
    
    html_content += """
            <h2>📈 Visualizaciones SHAP</h2>
            
            <div class="visualization">
                <h3>1. Importancia Promedio de Características</h3>
                <img src="shap_summary_bar.png" alt="Summary Bar Plot">
                <p>Muestra la importancia promedio de cada característica en las predicciones</p>
            </div>
            
            <div class="visualization">
                <h3>2. Distribución del Impacto de Características</h3>
                <img src="shap_summary_violin.png" alt="Summary Violin Plot">
                <p>Visualiza cómo varía el impacto de cada característica entre pacientes</p>
            </div>
            
            <div class="visualization">
                <h3>3. Relación Característica-Predicción (Top 6)</h3>
                <img src="shap_dependence_top6.png" alt="Dependence Plots">
                <p>Muestra cómo cada característica se relaciona con las predicciones del modelo</p>
            </div>
            
            <div class="visualization">
                <h3>4. Explicación Paciente de Alto Riesgo</h3>
                <img src="shap_waterfall_high_risk.png" alt="Waterfall High Risk">
                <p>Desglose de factores que llevan a predicción de alto riesgo</p>
            </div>
            
            <div class="visualization">
                <h3>5. Explicación Paciente de Bajo Riesgo</h3>
                <img src="shap_waterfall_low_risk.png" alt="Waterfall Low Risk">
                <p>Desglose de factores que llevan a predicción de bajo riesgo</p>
            </div>
            
            <div class="visualization">
                <h3>6. Matriz de Valores SHAP (Heatmap)</h3>
                <img src="shap_heatmap.png" alt="SHAP Heatmap">
                <p>Visualización completa de los valores SHAP para todos los pacientes y características</p>
            </div>
            
            <div class="footer">
                <p>📊 Análisis SHAP Completo - ANXRISK Model</p>
                <p>Generado automáticamente desde datos de análisis masivos</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Reporte HTML guardado: {output_file}")

def main():
    """Función principal"""
    try:
        # Cargar modelo y datos
        model, df = cargar_modelo_y_datos()
        
        # Procesar datos
        X = procesar_datos_para_modelo(df)
        
        # Crear explicador SHAP
        explainer, shap_values = crear_explicador_shap(model, X)
        
        # Generar visualizaciones
        generar_visualizaciones_shap(model, X, explainer, shap_values)
        
        # Analizar importancia
        feature_importance = analizar_importancia_caracteristicas(model, X, shap_values)
        
        # Generar reporte HTML
        generar_reporte_html(X, model, feature_importance)
        
        print("\n" + "="*80)
        print("✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("="*80)
        print("\n📊 Archivos generados:")
        print("  • shap_summary_bar.png - Importancia promedio")
        print("  • shap_summary_violin.png - Distribución de impacto")
        print("  • shap_dependence_top6.png - Relación característica-predicción")
        print("  • shap_waterfall_high_risk.png - Explicación alto riesgo")
        print("  • shap_waterfall_low_risk.png - Explicación bajo riesgo")
        print("  • shap_heatmap.png - Matriz de valores SHAP")
        print("  • shap_force_plots_top5.png - Force plots primeros 5 pacientes")
        print("  • shap_reporte_masivo.html - Reporte interactivo HTML")
        print("\n🌐 Abre 'shap_reporte_masivo.html' en tu navegador para ver el análisis completo")
        
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
