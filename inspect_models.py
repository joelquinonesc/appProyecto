import joblib
import sys

sys.stdout.flush()

print("Loading standard...", flush=True)
m_std = joblib.load('src/models/anxrisk_mlp_model_standard.joblib')
print(f"STD type: {type(m_std).__name__}", flush=True)
print(f"STD n_features: {getattr(m_std, 'n_features_in_', 'N/A')}", flush=True)
fn = getattr(m_std, 'feature_names_in_', None)
print(f"STD feature_names: {list(fn) if fn is not None else 'N/A'}", flush=True)
if hasattr(m_std, 'coefs_'):
    print(f"STD input layer shape: {m_std.coefs_[0].shape}", flush=True)

print("", flush=True)
print("Loading extended...", flush=True)
m_ext = joblib.load('src/models/anxrisk_mlp_model_extended.joblib')
print(f"EXT type: {type(m_ext).__name__}", flush=True)
print(f"EXT n_features: {getattr(m_ext, 'n_features_in_', 'N/A')}", flush=True)
fn2 = getattr(m_ext, 'feature_names_in_', None)
print(f"EXT feature_names: {list(fn2) if fn2 is not None else 'N/A'}", flush=True)
if hasattr(m_ext, 'coefs_'):
    print(f"EXT input layer shape: {m_ext.coefs_[0].shape}", flush=True)
