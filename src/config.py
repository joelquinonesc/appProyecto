"""
Configuración centralizada del sistema ANXRISK.

Constantes canónicas alineadas con la arquitectura de patente:
- Rutas de modelos (estándar y extendido)
- Orden de features para cada modelo
- Umbrales triclásicos de riesgo
- Genotipos válidos del panel SNPs
"""

# ── Rutas de modelos ──────────────────────────────────────────────
MODEL_STANDARD_PATH = "src/models/anxrisk_mlp_model_standard.joblib"
MODEL_EXTENDED_PATH = "src/models/anxrisk_mlp_model_extended.joblib"

# ── Orden canónico de features (Patente §0021) ───────────────────
FEATURES_STANDARD = [
    'EDAD24',
    'LTE12_0', 'LTE12_1', 'LTE12_2',
    'SF12F_Q1', 'SF12F_Q2', 'SF12F_Q3', 'SF12F_Q4',
    'SF12M_Q1', 'SF12M_Q2', 'SF12M_Q3', 'SF12M_Q4',
]

FEATURES_EXTENDED = FEATURES_STANDARD + [
    'PRKCA_C/C', 'PRKCA_C/T', 'PRKCA_T/T',
    'CDH20_A/A', 'CDH20_A/G', 'CDH20_G/G',
]

# ── Umbrales triclásicos (Patente §0025-§0026) ───────────────────
THRESHOLD_LOW = 0.30
THRESHOLD_HIGH = 0.60

# ── Genotipos válidos ─────────────────────────────────────────────
GENOTIPOS_PRKCA = ['C/C', 'C/T', 'T/T']
GENOTIPOS_CDH20 = ['A/A', 'A/G', 'G/G']
