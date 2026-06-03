"""
Simplified Model Insights Tab
Shows only AI model names with basic metrics
for Temperature, Pressure, and Humidity.
"""

import os
import re
import streamlit as st
import pandas as pd

# ── File paths ────────────────────────────────────────────────────────────────
METRICS_DIR       = "files/metrics"
TEMPERATURE_CSV   = os.path.join(METRICS_DIR, "temperature_metrics.csv")
PRESSURE_CSV      = os.path.join(METRICS_DIR, "pressure_metrics.csv")
HUMIDITY_CSV      = os.path.join(METRICS_DIR, "humidity_metrics.csv")

# ── Safe CSV Reader ───────────────────────────────────────────────────────────
def _safe_read(path: str) -> pd.DataFrame:
    if os.path.exists(path):
        try:
            return pd.read_csv(path)
        except Exception as e:
            st.warning(f"Error reading {os.path.basename(path)}: {e}")
    return pd.DataFrame()

def _slugify_part(value: str) -> str:
    """Safely converts a string to a filename-friendly format."""
    if not value:
        return "export"
    # re.sub replaces any non-alphanumeric character with an underscore
    text = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower())
    return text.strip("_") or "export"

def _csv_filename(title: str) -> str:
    return f"{_slugify_part(title)}.csv"
# ── Load Data (call once in app.py) ───────────────────────────────────────────
def load_model_insights_data():
    mapping = {
        "mi_temp_df": TEMPERATURE_CSV,
        "mi_pressure_df": PRESSURE_CSV,
        "mi_humidity_df": HUMIDITY_CSV,
    }

    for key, path in mapping.items():
        if key not in st.session_state:
            df = _safe_read(path)
            st.session_state[key] = df if not df.empty else None

# ── Sample Data (fallback) ────────────────────────────────────────────────────
def _sample_data():
    return pd.DataFrame({
        "Model": ["LSTM", "GRU", "ANN"],
        "MSE": [0.85, 0.80, 0.90],
        "RMSE": [0.92, 0.89, 0.95],
        "MAE": [0.70, 0.68, 0.75],
        "MAPE": [3.3, 3.1, 3.5],
        "R2": [0.92, 0.93, 0.91],
    })

def _get_df(key):
    df = st.session_state.get(key)
    if df is None or df.empty:
        return _sample_data()
    return df


def _slugify_part(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower())
    return text.strip("_") or "export"


def _csv_filename(title: str) -> str:
    return f"{_slugify_part(title)}.csv"

# ── Simple Table Display ──────────────────────────────────────────────────────
def _show_table(df: pd.DataFrame, title: str):
    st.subheader(title)

    if df is None or df.empty:
        st.warning("No data available")
        return

    # Keep only relevant columns
    cols = [c for c in ["Model", "MSE", "RMSE", "MAE", "MAPE", "R2"] if c in df.columns]
    df = df[cols]

    st.download_button(
        label=f"Download CSV Data: {title}",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=_csv_filename(title),
        mime="text/csv",
        key=f"download_{_slugify_part(title)}",
        help="Downloads the metrics table as CSV.",
    )
    st.dataframe(df, use_container_width=True)

# ── Main UI ───────────────────────────────────────────────────────────────────
def render_model_insights_tab():
    st.title("📊 AI Model Metrics")

    temp_df = _get_df("mi_temp_df")
    pres_df = _get_df("mi_pressure_df")
    hum_df  = _get_df("mi_humidity_df")

    tab1, tab2, tab3 = st.tabs([
        "🌡️ Temperature",
        "🌬️ Pressure",
        "💧 Humidity"
    ])

    with tab1:
        _show_table(temp_df, "Temperature Metrics")

    with tab2:
        _show_table(pres_df, "Pressure Metrics")

    with tab3:
        _show_table(hum_df, "Humidity Metrics")
