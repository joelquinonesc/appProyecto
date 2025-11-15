import pandas as pd
import joblib
import numpy as np
import shap
import matplotlib.pyplot as plt
import lightgbm as lgb
from sklearn.neural_network import MLPClassifier

# Cargar el CSV
csv_path = 'c:/Users/Taylor/Downloads/2025-11-15T01-20_export.csv'
data = pd.read_csv(csv_path)

# Tomar la primera fila (única)
row = data.iloc[0]

# Determinar el modelo basado en GENERO
genero = row['GENERO']
if genero == 0:
    model_path = 'src/models/lightgbm_male_model_tuned.joblib'
    model_name = "LightGBM (Masculino)"
elif genero == 1:
    model_path = 'src/models/mlp_female_model_tuned.joblib'
    model_name = "MLP (Femenino)"
else:
    raise ValueError("Género inválido")

# Cargar el modelo
model = joblib.load(model_path)

# Preparar las features en el orden exacto
features_dict = {
    'EDAD24': row['EDAD24'],
    'AEFGROUPS': row['AEFGROUPS'],
    'SF12F_Q1': row['SF12F_Q1'],
    'SF12F_Q2': row['SF12F_Q2'],
    'SF12F_Q3': row['SF12F_Q3'],
    'SF12F_Q4': row['SF12F_Q4'],
    'SF12M_Q1': row['SF12M_Q1'],
    'SF12M_Q2': row['SF12M_Q2'],
    'SF12M_Q3': row['SF12M_Q3'],
    'SF12M_Q4': row['SF12M_Q4'],
    'PRKCA_C/C': row['PRKCA_C/C'],
    'PRKCA_C/T': row['PRKCA_C/T'],
    'PRKCA_T/T': row['PRKCA_T/T'],
    'TCF4_A/A': row['TCF4_A/A'],
    'TCF4_A/T': row['TCF4_A/T'],
    'TCF4_T/T': row['TCF4_T/T'],
    'CDH20_A/A': row['CDH20_A/A'],
    'CDH20_A/G': row['CDH20_A/G'],
    'CDH20_G/G': row['CDH20_G/G'],
    'LTE12_0': row['LTE12_0'],
    'LTE12_1': row['LTE12_1'],
    'LTE12_2': row['LTE12_2'],
}

X = pd.DataFrame([features_dict])

print(f"Modelo utilizado: {model_name}")
print("Features:")
print(X)

# Predicción
prediction = model.predict(X)[0]
prob = model.predict_proba(X)[0]

print(f"\nPredicción: {'Alto Riesgo' if prediction == 1 else 'Bajo Riesgo'}")
print(f"Probabilidad Alto Riesgo: {prob[1]:.2%}")
print(f"Probabilidad Bajo Riesgo: {prob[0]:.2%}")

# SHAP
feature_names = list(X.columns)

if isinstance(model, lgb.LGBMClassifier):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
elif isinstance(model, MLPClassifier):
    explainer = shap.KernelExplainer(model.predict_proba, X, feature_names=feature_names)
    shap_values = explainer.shap_values(X)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
else:
    explainer = shap.KernelExplainer(model.predict_proba, X, feature_names=feature_names)
    shap_values = explainer.shap_values(X)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

if hasattr(shap_values, 'values'):
    shap_array = shap_values.values
else:
    shap_array = shap_values

# Importancia global
mean_abs_shap = np.mean(np.abs(shap_array), axis=0)
feature_importance = pd.DataFrame({
    'Feature': feature_names,
    'Mean_Abs_SHAP': mean_abs_shap
}).sort_values(by='Mean_Abs_SHAP', ascending=False)

print("\nImportancia Global de Características (Mean Absolute SHAP):")
print(feature_importance)

# Valores SHAP detallados
shap_df = pd.DataFrame({
    'Feature': feature_names,
    'SHAP Value': shap_array[0],
    'Feature Value': X.iloc[0].values
})

print("\nValores SHAP Detallados:")
print(shap_df)

# Gráfico SHAP
fig, ax = plt.subplots(figsize=(10, 6))
shap.summary_plot(shap_values, X, plot_type="dot", show=False)
plt.savefig('shap_plot.png')
print("\nGráfico SHAP guardado como 'shap_plot.png'")