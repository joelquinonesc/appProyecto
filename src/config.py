"""
Configuración central de la aplicación ANXRISK.

Define rutas de modelos, listas de features y opciones de genotipos
usados por las páginas de resultados y análisis masivo.
"""
import os

# ── Directorio base del proyecto ──────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Rutas de modelos ──────────────────────────────────────────────
MODEL_STANDARD_PATH = os.path.join(BASE_DIR, "src", "models", "anxrisk_best_standard.joblib")
MODEL_EXTENDED_PATH = os.path.join(BASE_DIR, "src", "models", "anxrisk_best_extended.joblib")

# ── Features del modelo estándar (13) ─────────────────────────────
FEATURES_STANDARD = [
    "EDAD24", "AEFGROUPS",
    "LTE12_0", "LTE12_1", "LTE12_2",
    "SF12F_Q1", "SF12F_Q2", "SF12F_Q3", "SF12F_Q4",
    "SF12M_Q1", "SF12M_Q2", "SF12M_Q3", "SF12M_Q4",
]

# ── Features del modelo extendido (22) ────────────────────────────
FEATURES_EXTENDED = FEATURES_STANDARD + [
    "PRKCA_C/C", "PRKCA_C/T", "PRKCA_T/T",
    "TCF4_A/A", "TCF4_A/T", "TCF4_T/T",
    "CDH20_A/A", "CDH20_A/G", "CDH20_G/G",
]

# ── Opciones de genotipos para selectbox ──────────────────────────
GENOTIPOS_PRKCA = ["T/T", "C/T", "C/C"]
GENOTIPOS_TCF4 = ["A/A", "A/T", "T/T"]
GENOTIPOS_CDH20 = ["G/G", "A/G", "A/A"]
