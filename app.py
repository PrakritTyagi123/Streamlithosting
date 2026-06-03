# app.py
"""
Main application file for Weather Prediction Dashboard
Clean and modular structure
"""
import streamlit as st
import streamlit.components.v1 as components
import re
from ui.styles import (

    apply_custom_css,
    create_section_header,
    create_info_box,
    create_metric_card
)

import pandas as pd
from config.constants import REGRESSION_METRICS
import time
# Import configuration
from config.constants import CITIES, CLASSICAL_ALGORITHMS, QUANTUM_ALGORITHMS, ALGORITHM_SHORT_NAMES
from ui.meteogram_tab import render_meteogram_tab
# Import data functions
from data.loader import get_available_dates
from ui.splash_screen import show_splash_screen
# Import utilities
from utils.helpers import get_chart_title_with_dates
# In app.py — add this ONCE near the top

from ui.meteogram_loader import load_meteogram_data
load_meteogram_data()
# Import insites tab components
# from ui.model_insights_tab import load_model_insights_data, render_model_insights_tab 
# load_model_insights_data()
from visualization.charts import (
    create_quantum_resource_charts,
    create_combined_prediction_chart
)
from visualization.tables import create_metrics_table_with_state, create_metrics_table_html, create_rainfall_metrics_table_with_state
from visualization.maps import create_zoom_map

# Import UI components
from ui.styles import apply_custom_css
from ui.header import render_header, render_footer
from ui.components import (
    render_configuration_section,
    render_algorithm_selection,
    render_prediction_column,
    render_training_params_section,
    render_temperature_config_and_graph_fragment
)
from ui.final_home import render_final_home_content
from ui.conclusion_tab import render_conclusion_tab
from ui.noise_components import render_temperature_noise_section, render_rain_noise_section
import logging
from ui.ncmrwf_components import render_ncmrwf_section
from config.constants import (
    NCMRWF_CLASSICAL_ALGORITHMS,
    NCMRWF_QUANTUM_ALGORITHMS,
    NCMRWF_ALGORITHM_SHORT_NAMES,
    NCMRWF_REGRESSION_METRICS
)

# ==================== HELPER FUNCTIONS ====================
def check_config_changed():
    """Check if configuration has changed and needs regeneration"""
    if 'config_hash' not in st.session_state:
        return False

    current_hash = hash((
        st.session_state.get('last_time_interval'),
        st.session_state.get('last_start_date'),
        st.session_state.get('last_end_date')
    ))

    return st.session_state.config_hash != current_hash

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Weather Prediction & Modeling",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

st.markdown("""
<style>
    [data-testid="stToolbar"] { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
    .stAppToolbar { display: none !important; }
    div[data-testid="stStatusWidget"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE INITIALIZATION ====================
if 'classical_data' not in st.session_state:
    st.session_state.classical_data = None
if 'quantum_data' not in st.session_state:
    st.session_state.quantum_data = None
if 'last_classical_algo' not in st.session_state:
    st.session_state.last_classical_algo = None
if 'last_quantum_algo' not in st.session_state:
    st.session_state.last_quantum_algo = None

if 'imd_noise_left_algo' not in st.session_state:
    st.session_state.imd_noise_left_algo = "Select Quantum Algorithm"
if 'imd_noise_right_algo' not in st.session_state:
    st.session_state.imd_noise_right_algo = "Select Quantum Algorithm"
if 'imd_noise_left_type' not in st.session_state:
    st.session_state.imd_noise_left_type = "Without Noise"
if 'imd_noise_right_type' not in st.session_state:
    st.session_state.imd_noise_right_type = "Without Noise"

if 'ncmr_classical_data' not in st.session_state:
    st.session_state.ncmr_classical_data = None
if 'ncmr_quantum_data' not in st.session_state:
    st.session_state.ncmr_quantum_data = None
if 'ncmr_predictions_generated' not in st.session_state:
    st.session_state.ncmr_predictions_generated = False

if 'ncmrwf_analysis_type' not in st.session_state:
    st.session_state.ncmrwf_analysis_type = 'Univariate'
if 'classical_rain_data' not in st.session_state:
    st.session_state.classical_rain_data = None
if 'quantum_rain_data' not in st.session_state:
    st.session_state.quantum_rain_data = None
if 'combined_rain_data' not in st.session_state:
    st.session_state.combined_rain_data = None
if 'actual_displayed' not in st.session_state:
    st.session_state.actual_displayed = False

if 'temp_generation_city' not in st.session_state:
    st.session_state.temp_generation_city = "Delhi"
if 'rain_generation_city' not in st.session_state:
    st.session_state.rain_generation_city = "Delhi"

# ==================== SPLASH SCREEN ====================
if 'splash_shown' not in st.session_state:
    st.session_state.splash_shown = False

if not st.session_state.splash_shown:
    show_splash_screen()
    time.sleep(3.5)
    st.session_state.splash_shown = True
    st.rerun()
    st.stop()

# ==================== APPLY STYLING ====================
apply_custom_css()

# ==================== RENDER HEADER ====================
render_header()

st.markdown("""<style>.stTabs {margin-top: 0px !important;}
[data-baseweb="tab-list"] {
        margin-top: 0 !important;
        padding-top: 0 !important;
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
    }
    .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    .main > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
</style>""", unsafe_allow_html=True)

# ==================== CREATE TABS ====================


tab1, tab_interp, tab3, tab4 = st.tabs([
    "🏠 Home",
    "🔬 Interpolation Methods - Metrics",
    "📋 Prediction",
    "🛰️ Meteogram"
])
# ==================== TAB 1: HOME ====================
with tab1:
    from ui.final_home import render_final_home_content
    render_final_home_content()

    st.markdown("""
    <div style="margin-top: 20px; padding: 15px; background:#3b82f6; 
                border-radius: 12px; border-left: 5px solid #3b82f6; margin-bottom: 20px;">
        <h3 style="color:White ; margin-bottom: 15px;">
            <i class="fas fa-compass"></i> Quick Navigation Guide
        </h3>
    </div>
    <div style="color: #000000; padding: 16px; line-height: 2; border-radius: 8px; border-left: 5px solid #3b82f6;">
        <p style="color: #000000; font-size: 16px; line-height: 1.8; margin: 0;">
            🌡️ <strong>Temperature Prediction:</strong> Configure date range, location, and algorithms to generate temperature forecasts<br>
            🌧️ <strong>Rain Prediction:</strong> Predict rainfall patterns using advanced modeling techniques<br>
            📊 <strong>Conclusion:</strong> View comprehensive analysis and comparison of prediction results<br>
            🛰️ <strong>Meteogram:</strong> View Meteogram data and visualizations
        </p>
    </div>
    """, unsafe_allow_html=True)
# ==================== TAB: INTERPOLATION METHODS - METRICS ====================
with tab_interp:
    import streamlit.components.v1 as components

    st.markdown("""
        <div style="background:linear-gradient(135deg,#4c1d95 0%,#7c3aed 100%);
                    border-radius:12px; padding:14px 22px; margin-bottom:18px; color:#fff;">
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:6px;">
                <span style="font-size:22px; font-weight:800;">🔬 Interpolation Methods - Metrics</span>
                <span style="background:rgba(255,255,255,0.20); border:1px solid rgba(255,255,255,0.45);
                            border-radius:6px; padding:3px 12px; font-size:12px; font-weight:700;
                            letter-spacing:0.4px; white-space:nowrap;">
                    📦 Source: IMD Dataset — India Meteorological Department
                </span>
            </div>
            <div style="font-size:13px; opacity:0.85;">
                These metrics reflect model performance <strong>after filling missing (NaN) values</strong>
                in the IMD dataset using various imputation algorithms — evaluated at 10% gap rate.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── NUMERIC TABLE ────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1d4ed8 0%,#3b82f6 100%);
                border-radius:10px; padding:10px 18px; margin-bottom:12px; color:#fff;">
        <span style="font-size:16px; font-weight:700;">📐 Numerical Data — MAX Column (Numeric Imputation)</span>
    </div>
    """, unsafe_allow_html=True)

    numeric_data = [
        {"Algorithm": "Linear Interpolation",       "MAE": 1.1659, "RMSE": 1.6374, "Adjusted R²": 0.9413, "MAPE": 4.0173},
        {"Algorithm": "Time-Based Interpolation",   "MAE": 1.1662, "RMSE": 1.6399, "Adjusted R²": 0.9411, "MAPE": 4.0176},
        {"Algorithm": "Random Forest Regressor",    "MAE": 1.3408, "RMSE": 1.8046, "Adjusted R²": 0.9287, "MAPE": 4.6524},
        {"Algorithm": "Neural Network MLP",         "MAE": 1.3208, "RMSE": 1.8081, "Adjusted R²": 0.9284, "MAPE": 4.5713},
        {"Algorithm": "Polynomial Interpolation",   "MAE": 1.2975, "RMSE": 1.8082, "Adjusted R²": 0.9285, "MAPE": 4.4885},
    ]

    best_mae  = min(r["MAE"]         for r in numeric_data)
    best_rmse = min(r["RMSE"]        for r in numeric_data)
    best_r2   = max(r["Adjusted R²"] for r in numeric_data)
    best_mape = min(r["MAPE"]        for r in numeric_data)

    hdr = ("background:linear-gradient(135deg,#1d4ed8,#3b82f6);color:#fff;font-weight:700;"
           "font-size:12px;padding:10px 14px;text-align:center;border:1px solid rgba(0,0,0,0.08);")

    rows_html = ""
    for i, row in enumerate(numeric_data):
        bg = "#ffffff" if i % 2 == 0 else "#f8fafc"

        def _num_cell(val, is_best, fmt=".4f"):
            color  = "#16a34a" if is_best else "#0f172a"
            weight = "800"     if is_best else "500"
            star   = " ★"     if is_best else ""
            return (f'<td style="padding:9px 12px;font-size:12px;text-align:center;'
                    f'background:{bg};color:{color};font-weight:{weight};'
                    f'border-bottom:1px solid #e2e8f0;border-right:1px solid #e2e8f0;">'
                    f'{val:{fmt}}{star}</td>')

        rows_html += f"""<tr>
            <td style="padding:9px 14px;font-weight:600;font-size:12px;color:#1e293b;
                background:{bg};border-bottom:1px solid #e2e8f0;border-right:2px solid #bfdbfe;
                white-space:nowrap;">{row['Algorithm']}</td>
            {_num_cell(row['MAE'],         row['MAE']         == best_mae)}
            {_num_cell(row['RMSE'],        row['RMSE']        == best_rmse)}
            {_num_cell(row['Adjusted R²'], row['Adjusted R²'] == best_r2)}
            {_num_cell(row['MAPE'],        row['MAPE']        == best_mape)}
        </tr>"""

    numeric_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <style>* {{box-sizing:border-box;margin:0;padding:0;}}
    html,body{{background:transparent;font-family:Arial,sans-serif;overflow:hidden;}}
    .wrap{{overflow-x:auto;border-radius:10px;border:1px solid #bfdbfe;
           box-shadow:0 2px 10px rgba(0,0,0,0.06);}}
    table{{border-collapse:collapse;width:100%;}}
    th,td{{white-space:nowrap;}}</style></head><body>
    <div class="wrap"><table>
      <thead><tr>
        <th style="{hdr} text-align:left;min-width:200px;border-right:2px solid rgba(255,255,255,0.3);">Algorithm</th>
        <th style="{hdr}">MAE ↓</th>
        <th style="{hdr}">RMSE ↓</th>
        <th style="{hdr}">Adjusted R² ↑</th>
        <th style="{hdr}">MAPE ↓</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table></div>
    <div style="font-size:11px;color:#16a34a;margin-top:6px;padding:0 4px;">
        ★ Best value per metric &nbsp;|&nbsp; Column: MAX &nbsp;|&nbsp; Type: Numeric &nbsp;|&nbsp; Gap: 10%
    </div>
    </body></html>"""

    components.html(numeric_html, height=5 * 38 + 80, scrolling=False)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── BINARY TABLE ─────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#065f46 0%,#059669 100%);
                border-radius:10px; padding:10px 18px; margin-bottom:12px; color:#fff;">
        <span style="font-size:16px; font-weight:700;">🔘 Binary Data — DZ Column (Binary Classification Imputation)</span>
    </div>
    """, unsafe_allow_html=True)

    binary_data = [
        {"Algorithm": "Logistic Regression",        "Accuracy": 0.8341, "Precision": 0.8381, "Recall": 0.8281, "F1 Score": 0.8331},
        {"Algorithm": "Decision Tree Classifier",   "Accuracy": 0.7556, "Precision": 0.8947, "Recall": 0.5793, "F1 Score": 0.7032},
        {"Algorithm": "Random Forest Classifier",   "Accuracy": 0.5407, "Precision": 0.9104, "Recall": 0.0904, "F1 Score": 0.1644},
    ]

    best_acc  = max(r["Accuracy"]  for r in binary_data)
    best_prec = max(r["Precision"] for r in binary_data)
    best_rec  = max(r["Recall"]    for r in binary_data)
    best_f1   = max(r["F1 Score"]  for r in binary_data)

    hdr_g = ("background:linear-gradient(135deg,#065f46,#059669);color:#fff;font-weight:700;"
             "font-size:12px;padding:10px 14px;text-align:center;border:1px solid rgba(0,0,0,0.08);")

    b_rows = ""
    for i, row in enumerate(binary_data):
        bg = "#ffffff" if i % 2 == 0 else "#f0fdf4"

        def _bin_cell(val, is_best):
            color  = "#16a34a" if is_best else "#0f172a"
            weight = "800"     if is_best else "500"
            star   = " ★"     if is_best else ""
            return (f'<td style="padding:9px 12px;font-size:12px;text-align:center;'
                    f'background:{bg};color:{color};font-weight:{weight};'
                    f'border-bottom:1px solid #d1fae5;border-right:1px solid #d1fae5;">'
                    f'{val:.4f}{star}</td>')

        b_rows += f"""<tr>
            <td style="padding:9px 14px;font-weight:600;font-size:12px;color:#1e293b;
                background:{bg};border-bottom:1px solid #d1fae5;border-right:2px solid #6ee7b7;
                white-space:nowrap;">{row['Algorithm']}</td>
            {_bin_cell(row['Accuracy'],  row['Accuracy']  == best_acc)}
            {_bin_cell(row['Precision'], row['Precision'] == best_prec)}
            {_bin_cell(row['Recall'],    row['Recall']    == best_rec)}
            {_bin_cell(row['F1 Score'],  row['F1 Score']  == best_f1)}
        </tr>"""

    binary_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <style>* {{box-sizing:border-box;margin:0;padding:0;}}
    html,body{{background:transparent;font-family:Arial,sans-serif;overflow:hidden;}}
    .wrap{{overflow-x:auto;border-radius:10px;border:1px solid #6ee7b7;
           box-shadow:0 2px 10px rgba(0,0,0,0.06);}}
    table{{border-collapse:collapse;width:100%;}}
    th,td{{white-space:nowrap;}}</style></head><body>
    <div class="wrap"><table>
      <thead><tr>
        <th style="{hdr_g} text-align:left;min-width:200px;border-right:2px solid rgba(255,255,255,0.3);">Algorithm</th>
        <th style="{hdr_g}">Accuracy ↑</th>
        <th style="{hdr_g}">Precision ↑</th>
        <th style="{hdr_g}">Recall ↑</th>
        <th style="{hdr_g}">F1 Score ↑</th>
      </tr></thead>
      <tbody>{b_rows}</tbody>
    </table></div>
    <div style="font-size:11px;color:#16a34a;margin-top:6px;padding:0 4px;">
        ★ Best value per metric &nbsp;|&nbsp; Column: DZ &nbsp;|&nbsp; Type: Binary &nbsp;|&nbsp; Gap: 10%
    </div>
    </body></html>"""

    components.html(binary_html, height=3 * 38 + 80, scrolling=False)
# ==================== TAB 3: Preferences ====================
with tab3:
    pre_tab1, pre_tab2, pre_tab3 = st.tabs([
        "🌡️ Temperature Prediction",
        "🌧️ Rain Prediction",
        "📊 Conclusion"
    ])

    # ==================== Prediction SUB-TAB 1: TEMPERATURE PREDICTION ====================
    with pre_tab1:
        col_title, col_spacer, col_datasource = st.columns([2, 1, 2])

        with col_title:
            st.markdown('<h3>📊 Temperature Predictions Dashboard</h3>', unsafe_allow_html=True)

        with col_spacer:
            st.write("")

        with col_datasource:
            st.markdown("<div style='margin-top: 10px;'>", unsafe_allow_html=True)
            data_source = st.selectbox(
                "**📂 Data Source:**",
                options=["IMD", "NCMRWF"],
                key="temp_data_source",
                help="Select dataset for temperature predictions"
            )

        st.markdown("---")

        if 'imd_selected_classical' not in st.session_state:
            st.session_state.imd_selected_classical = "Select Classical Algorithm"
        if 'imd_selected_quantum' not in st.session_state:
            st.session_state.imd_selected_quantum = "Select Quantum Algorithm"

        if 'ncmrwf_selected_classical' not in st.session_state:
            st.session_state.ncmrwf_selected_classical = "Select Classical Algorithm"
        if 'ncmrwf_selected_quantum' not in st.session_state:
            st.session_state.ncmrwf_selected_quantum = "Select Quantum Algorithm"

        if data_source == "IMD":
            temp_subtab1, temp_subtab2 = st.tabs([
                "🌡️ Without Noise",
                "🔬 With Noise"
            ])

            with temp_subtab1:
                col_algo1, col_algo2 = st.columns(2)

                with col_algo1:
                    st.markdown("**🖥️ Classical Algorithm**")

                    classical_options = list(CLASSICAL_ALGORITHMS.keys())

                    def update_imd_classical():
                        st.session_state.imd_selected_classical = st.session_state.temp_classical_algo_select

                    try:
                        default_classical_idx = classical_options.index(st.session_state.imd_selected_classical)
                    except (ValueError, KeyError):
                        default_classical_idx = 0

                    classical_algo = st.selectbox(
                        "Select algorithm",
                        classical_options,
                        index=default_classical_idx,
                        key="temp_classical_algo_select",
                        on_change=update_imd_classical
                    )

                with col_algo2:
                    st.markdown("**⚛️ Quantum Algorithm**")

                    quantum_options = list(QUANTUM_ALGORITHMS.keys())

                    def update_imd_quantum():
                        st.session_state.imd_selected_quantum = st.session_state.temp_quantum_algo_select

                    try:
                        default_quantum_idx = quantum_options.index(st.session_state.imd_selected_quantum)
                    except (ValueError, KeyError):
                        default_quantum_idx = 0

                    quantum_algo = st.selectbox(
                        "Select algorithm",
                        quantum_options,
                        index=default_quantum_idx,
                        key="temp_quantum_algo_select",
                        on_change=update_imd_quantum
                    )

                classical_algo_short = ALGORITHM_SHORT_NAMES.get(classical_algo, classical_algo)
                quantum_algo_short = ALGORITHM_SHORT_NAMES.get(quantum_algo, quantum_algo)

                METRICS_KEY_MAPPING = {
                    "LSTM": "LSTM",
                    "GRU": "GRU",
                    "ANN": "ANN",
                    "Dense ANN": "Dense ANN",
                    "SVM": "SVM",
                    "QLSTM": "QLSTM",
                    "QGRU": "QGRU",
                    "QSVM": "QSVM",
                    "VQC": "VQC",
                    "Hybrid QNN": "Hybrid_QNN",
                    "QNN-SE": "QNN_SE",
                    "QNN-Ising": "QNN_IS"
                }

                classical_metrics_key = METRICS_KEY_MAPPING.get(classical_algo_short, classical_algo_short)
                quantum_metrics_key = METRICS_KEY_MAPPING.get(quantum_algo_short, quantum_algo_short)

                both_selected = (classical_algo != "Select Classical Algorithm" and
                                 quantum_algo != "Select Quantum Algorithm")

                if both_selected:
                    st.info(f"📌 Selected: **{classical_algo_short}** (Classical) vs **{quantum_algo_short}** (Quantum)")

                    if st.button("🎯 GENERATE COMBINED TEMPERATURE PREDICTIONS", key="gen_combined_temp", type="primary"):
                        sample_file = "files/SVM_forecast.csv"
                        available_dates = get_available_dates(sample_file)

                        if not available_dates:
                            st.error("No dates available. Please check your data files.")
                            st.stop()

                        min_date = min(available_dates)
                        max_date = max(available_dates)

                        import datetime
                        default_end = max_date
                        default_start = max_date - datetime.timedelta(days=6)

                        if 'temp_generation_start_date' not in st.session_state:
                            st.session_state.temp_generation_start_date = default_start
                            st.session_state.temp_generation_end_date = default_end
                            st.session_state.temp_generation_interval = "1 Hour"
                            st.session_state.temp_generation_city = "Delhi"

                        start_date = st.session_state.temp_generation_start_date
                        end_date = st.session_state.temp_generation_end_date
                        time_interval = st.session_state.temp_generation_interval
                        city = st.session_state.temp_generation_city

                        with st.spinner(f"Loading predictions for {classical_algo_short} and {quantum_algo_short}..."):
                            from data.processor import get_algorithm_data_with_dates

                            classical_data = get_algorithm_data_with_dates(
                                'classical', classical_algo, start_date, end_date, time_interval
                            )

                            quantum_data = get_algorithm_data_with_dates(
                                'quantum', quantum_algo, start_date, end_date, time_interval
                            )

                            if classical_data is not None and quantum_data is not None:
                                classical_pred_col = [col for col in classical_data.columns if col not in ['Datetime', 'T2M']][0]
                                quantum_pred_col = [col for col in quantum_data.columns if col not in ['Datetime', 'T2M']][0]

                                st.session_state.classical_data = {
                                    'data': classical_data,
                                    'algorithm': classical_algo_short,
                                    'metrics_key': classical_metrics_key,
                                    'prediction_column': classical_pred_col,
                                    'time_interval': time_interval,
                                    'start_date': start_date,
                                    'end_date': end_date,
                                    'prediction': classical_data[classical_pred_col].iloc[-1],
                                    'actual_temp': classical_data['T2M'].iloc[-1],
                                    'last_datetime': classical_data['Datetime'].iloc[-1]
                                }

                                st.session_state.quantum_data = {
                                    'data': quantum_data,
                                    'algorithm': quantum_algo_short,
                                    'metrics_key': quantum_metrics_key,
                                    'prediction_column': quantum_pred_col,
                                    'time_interval': time_interval,
                                    'start_date': start_date,
                                    'end_date': end_date,
                                    'prediction': quantum_data[quantum_pred_col].iloc[-1],
                                    'actual_temp': quantum_data['T2M'].iloc[-1],
                                    'last_datetime': quantum_data['Datetime'].iloc[-1]
                                }

                                st.session_state.temp_predictions_generated = True
                                st.success("✅ Predictions loaded successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Could not load prediction data for one or both algorithms")

                else:
                    missing = []
                    if classical_algo == "Select Classical Algorithm":
                        missing.append("Classical Algorithm")
                    if quantum_algo == "Select Quantum Algorithm":
                        missing.append("Quantum Algorithm")
                    st.warning(f"⚠️ Please select: {' and '.join(missing)} to enable prediction generation")

                if st.session_state.get('temp_predictions_generated', False):
                    render_temperature_config_and_graph_fragment(
                        classical_algo, quantum_algo,
                        classical_algo_short, quantum_algo_short
                    )

                # ==================== METRICS TABLE ====================
                st.markdown("---")
                metrics_df, classical_header, quantum_header = create_metrics_table_with_state()

                st.markdown("#### Algorithm Performance Metrics Comparison: Classical vs Quantum")

                from visualization.tables import create_metrics_table_html
                table_html = create_metrics_table_html(classical_header, quantum_header, metrics_df)
                st.markdown(table_html, unsafe_allow_html=True)

                classical_generated = (st.session_state.classical_data and
                                       st.session_state.classical_data.get('algorithm') != "Select Classical Algorithm")
                quantum_generated = (st.session_state.quantum_data and
                                     st.session_state.quantum_data.get('algorithm') != "Select Quantum Algorithm")

                if not classical_generated and not quantum_generated:
                    st.info("Generate predictions to see performance metrics populate in the table above.")
                elif classical_generated and not quantum_generated:
                    st.info("Generate quantum prediction to see quantum metrics populate in the table above.")
                elif not classical_generated and quantum_generated:
                    st.info("Generate classical prediction to see classical metrics populate in the table above.")
                else:
                    st.success("Both predictions generated! Performance metrics are now displayed in the table above.")

                with st.expander("Regression Metrics (Performance Evaluation & Comparisons)", expanded=False):
                    st.markdown("""
                    **Each metric has a specific role in comparing models:**

                    **Mean Squared Error (MSE):**  
                    Penalizes large errors heavily. Useful for spotting models that occasionally make very bad predictions.

                    **Root Mean Squared Error (RMSE):**  
                    Same as MSE but in original units, making it more interpretable.

                    **Mean Absolute Error (MAE):**  
                    Treats all errors equally. Good for understanding average prediction deviation.

                    **Mean Absolute Percentage Error (MAPE):**  
                    Expresses error as a percentage of actual values. Useful for comparing across datasets with different scales.

                    **R² Score:**  
                    Shows how much variance is explained by the model. Higher = better fit.

                    **Adjusted R²:**  
                    Adjusts R² for number of predictors. Useful when comparing models with different complexities.
                    """)

                # ==================== TRAINING PARAMETERS & QUANTUM RESOURCES ====================
                col_train, col_quantum_resource = st.columns(2)

                with col_train:
                    render_training_params_section()

                    with st.expander("Training Parameters and Device Information(Model Design & Hyperparameters)", expanded=False):
                        st.markdown("""
                        **These define how the models are built and optimized:**

                        ● Package:
                        Framework choice (Pennylane, Qiskit) affects available algorithms, encodings, and hardware compatibility.

                        ● Optimizer:
                        Gradient-based (Adam) vs. gradient-free (COBYLA) optimizers
                        impact convergence speed and stability.

                        ● Learning Rate:
                        Controls step size in optimization. Too high = unstable; too low = slow convergence.

                        ● Training Epochs:
                        More epochs = more training time but better convergence (risk of overfitting if too many).

                        ● Executing Device:
                        Determines whether training is simulated (CPU/GPU) or run on actual quantum hardware.

                        ● Classical Trainable Parameters:
                        Larger parameter counts = more expressive models but higher risk of overfitting.

                        ● Quantum Trainable Parameters:
                        More quantum parameters = richer quantum expressivity, but harder to optimize due to barren plateaus.

                        ● Sequence Length:
                        Defines time-series window size. Longer sequences capture more context but increase complexity.

                        ● Classical-to-Quantum Data Encoding:
                        Feature maps (e.g., ZZFeatureMap) determine how classical data is embedded into quantum states.
                        """)

                with col_quantum_resource:
                    st.markdown("#### Quantum Resource Estimates")

                    if st.session_state.get('quantum_data') and st.session_state.quantum_data.get('algorithm') != "Select Quantum Algorithm":
                        try:
                            from visualization.charts import create_combined_resource_chart_for_algorithm
                            quantum_algo_name = st.session_state.quantum_data['algorithm']
                            fig_combined = create_combined_resource_chart_for_algorithm(quantum_algo_name)
                            st.plotly_chart(fig_combined, use_container_width=True)
                        except ImportError as e:
                            st.error(f"Function not found. Please add the function to charts.py")
                            st.code(str(e))

                    with st.expander("Quantum Resource Estimate (Model Complexity & Deployability)", expanded=False):
                        st.markdown("""
                        Each metric reflects how feasible it is to run the model on real quantum hardware:

                        **Single-Qubit Gate Count:**
                        More single-qubit gates increase runtime but are relatively cheap. Excessive counts may still stress coherence times.

                        **Multi-Qubit Gate Count:**
                        Multi-qubit (entangling) gates are the bottleneck in today's hardware. High counts reduce deployability due to noise.

                        **Total Circuit Depth:**
                        Circuit depth directly impacts error rates. Shallow circuits are more deployable on NISQ devices.

                        **Total Qubit Count:**
                        Current devices have limited qubits (tens to hundreds). Models requiring fewer qubits are more practical.

                        **Measurement Shots:**
                        More shots = more repetitions needed to reduce statistical noise. High shot requirements increase runtime and cost.

                        **Number of Measurement Qubits:**
                        Determines how much classical post-processing is needed. Fewer measurements = faster inference.
                        """)

            with temp_subtab2:
                render_temperature_noise_section()

            # ==================== TEMPERATURE LOCATION MAP ====================
            st.markdown("---")
            st.markdown('<h3>Location Map</h3>', unsafe_allow_html=True)

            col_map1, col_map2 = st.columns([1, 3])
            selected_subzone = None

            with col_map1:
                st.subheader("Selected Location")
                city = st.session_state.get('temp_generation_city', 'Delhi')

                if city and city in CITIES:
                    city_info = CITIES[city]
                    st.info(f"**Location:** {city}")
                    st.write(f"**Region:** {city_info['region']}")
                    st.write(f"**Coordinates:** {city_info['lat']:.4f}°N, {city_info['lon']:.4f}°E")

                    if 'subzones' in city_info and city_info['subzones']:
                        st.markdown("---")
                        st.subheader("Subzone Selection")

                        subzone_options = ["None (City Level)"] + [f"{city} - {subzone}" for subzone in city_info['subzones'].keys()]

                        selected_subzone = st.selectbox(
                            "Select Subzone",
                            options=subzone_options,
                            key="temp_subzone_selector",
                            help="Select a specific subzone to view detailed predictions"
                        )

                        if selected_subzone != "None (City Level)":
                            subzone_name = selected_subzone.split(" - ")[1]
                            subzone_info = city_info['subzones'][subzone_name]
                            st.write(f"**Subzone Region:** {subzone_info['region']}")
                            st.write(f"**Coordinates:** {subzone_info['lat']:.4f}°N, {subzone_info['lon']:.4f}°E")

                st.markdown("---")
                st.subheader("📅 Custom Date/Time")

                if st.session_state.get('classical_data') or st.session_state.get('quantum_data'):
                    data_source_map = (st.session_state.classical_data or st.session_state.quantum_data)['data']

                    min_date = data_source_map['Datetime'].min().date()
                    max_date = data_source_map['Datetime'].max().date()

                    selected_date = st.date_input(
                        "Select Date",
                        value=st.session_state.get('temp_selected_map_date', max_date),
                        min_value=min_date,
                        max_value=max_date,
                        key="temp_map_date_input"
                    )

                    available_times = data_source_map[
                        data_source_map['Datetime'].dt.date == selected_date
                    ]['Datetime'].dt.time.unique()

                    if len(available_times) > 0:
                        available_times_sorted = sorted(available_times)

                        default_time_index = len(available_times_sorted) - 1
                        if 'temp_selected_map_time' in st.session_state:
                            try:
                                default_time_index = available_times_sorted.index(st.session_state.temp_selected_map_time)
                            except ValueError:
                                default_time_index = len(available_times_sorted) - 1

                        selected_time = st.selectbox(
                            "Select Time",
                            options=available_times_sorted,
                            index=default_time_index,
                            key="temp_map_time_input"
                        )

                        if st.button("🔄 Update Map", key="temp_update_map_btn", type="primary"):
                            from datetime import datetime
                            st.session_state.temp_selected_map_date = selected_date
                            st.session_state.temp_selected_map_time = selected_time
                            st.session_state.temp_custom_map_datetime = datetime.combine(selected_date, selected_time)
                            st.success(f"✅ Map updated to {selected_date} {selected_time}")
                            st.rerun()

                        if 'temp_custom_map_datetime' in st.session_state:
                            st.info(f"📍 Showing: {st.session_state.temp_custom_map_datetime.strftime('%d-%m-%Y %H:%M')}")
                        else:
                            st.info("📍 Showing: Latest prediction")
                    else:
                        st.warning("No data available for selected date")
                else:
                    st.info("Generate predictions first to enable custom date/time selection")

            with col_map2:
                st.subheader("Interactive Map")

                if 'temp_custom_map_datetime' in st.session_state:
                    st.session_state.custom_map_datetime = st.session_state.temp_custom_map_datetime
                else:
                    st.session_state.custom_map_datetime = None

                city = st.session_state.get('temp_generation_city', 'Delhi')

                if city and city in CITIES:
                    # FIX: create_zoom_map now returns HTML string, render with components.html
                    map_html = create_zoom_map(
                        city, CITIES, selected_subzone,
                        classical_data=st.session_state.get('classical_data'),
                        quantum_data=st.session_state.get('quantum_data'),
                        custom_datetime=st.session_state.get('custom_map_datetime')
                    )
                    components.html(map_html, height=500)
                else:
                    st.warning("Please select a valid city from the configuration section")

        elif data_source == "NCMRWF":
            render_ncmrwf_section()

    # ==================== Prediction SUB-TAB 2: RAIN PREDICTION ====================
    with pre_tab2:
        st.markdown('<h3>🌧️ Rain Predictions Dashboard</h3>', unsafe_allow_html=True)

        rain_subtab1, rain_subtab2 = st.tabs([
            "🌧️ Without Noise",
            "🔬 With Noise"
        ])

        with rain_subtab1:
            st.markdown("### ⚙️ Configuration")

            classical_list = list(CLASSICAL_ALGORITHMS.keys())
            quantum_list = list(QUANTUM_ALGORITHMS.keys())

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**🖥️ Classical Algorithm**")
                classical_algo = st.selectbox(
                    "Select algorithm",
                    classical_list,
                    key="rain_classical_algo"
                )

            with col2:
                st.markdown("**⚛️ Quantum Algorithm**")
                quantum_algo = st.selectbox(
                    "Select algorithm",
                    quantum_list,
                    key="rain_quantum_algo"
                )

            classical_algo_short = ALGORITHM_SHORT_NAMES.get(classical_algo, classical_algo)
            quantum_algo_short = ALGORITHM_SHORT_NAMES.get(quantum_algo, quantum_algo)

            both_selected = (classical_algo != "Select Classical Algorithm" and
                             quantum_algo != "Select Quantum Algorithm")

            if both_selected:
                st.info(f"📌 Selected: **{classical_algo_short}** (Classical) vs **{quantum_algo_short}** (Quantum)")

                if st.button("🎯 Generate Combined Rain Predictions", key="gen_combined_rain", type="primary"):
                    with st.spinner(f"Loading predictions for {classical_algo_short} and {quantum_algo_short}..."):
                        from data.loader import get_rainfall_data_for_display
                        from config.constants import CLASSIFICATION_METRICS

                        classical_data = get_rainfall_data_for_display(classical_algo_short)
                        quantum_data = get_rainfall_data_for_display(quantum_algo_short)

                        if classical_data and quantum_data:
                            classical_data['metrics'] = CLASSIFICATION_METRICS.get(classical_algo_short, {})
                            quantum_data['metrics'] = CLASSIFICATION_METRICS.get(quantum_algo_short, {})

                            st.session_state.combined_rain_data = {
                                'classical': classical_data,
                                'quantum': quantum_data
                            }

                            st.session_state.classical_rain_data = classical_data
                            st.session_state.quantum_rain_data = quantum_data

                            st.success(f"✅ Predictions loaded successfully!")
                        else:
                            st.error("❌ Could not load prediction data for one or both algorithms")

                if st.session_state.get('combined_rain_data'):
                    classical_info = st.session_state.combined_rain_data['classical']
                    quantum_info = st.session_state.combined_rain_data['quantum']
                    classical_data = classical_info['data']
                    quantum_data = quantum_info['data']

                    from visualization.charts import show_rain_forecast_with_tabs

                    show_rain_forecast_with_tabs(
                        classical_data=classical_data,
                        quantum_data=quantum_data,
                        classical_pred_col=classical_info['prediction_column'],
                        quantum_pred_col=quantum_info['prediction_column'],
                        classical_algo=classical_info['algorithm'],
                        quantum_algo=quantum_info['algorithm']
                    )

                    st.markdown("---")

                    col_metrics1, col_metrics2 = st.columns(2)

                    with col_metrics1:
                        st.markdown(f"#### 🖥️ {classical_info['algorithm']} Metrics")
                        if classical_info.get('metrics'):
                            from visualization.charts import create_confusion_matrix_chart
                            fig_cm = create_confusion_matrix_chart(
                                classical_info['metrics'],
                                classical_info['algorithm']
                            )
                            st.plotly_chart(fig_cm, use_container_width=True)
                        else:
                            st.warning("No metrics available")

                    with col_metrics2:
                        st.markdown(f"#### ⚛️ {quantum_info['algorithm']} Metrics")
                        if quantum_info.get('metrics'):
                            from visualization.charts import create_confusion_matrix_chart
                            fig_cm = create_confusion_matrix_chart(
                                quantum_info['metrics'],
                                quantum_info['algorithm']
                            )
                            st.plotly_chart(fig_cm, use_container_width=True)
                        else:
                            st.warning("No metrics available")
                else:
                    st.info("👆 Click 'Generate Combined Rain Predictions' to view the unified comparison")

            else:
                missing = []
                if classical_algo == "Select Classical Algorithm":
                    missing.append("Classical Algorithm")
                if quantum_algo == "Select Quantum Algorithm":
                    missing.append("Quantum Algorithm")
                st.warning(f"⚠️ Please select: {' and '.join(missing)} from Configuration section above")

            # ========== METRICS TABLE ==========
            st.markdown("---")
            from visualization.tables import create_rainfall_metrics_table_with_state
            metrics_df, classical_header, quantum_header = create_rainfall_metrics_table_with_state()

            st.markdown("#### Performance Metrics: Classical vs Quantum")

            table_html = create_metrics_table_html(classical_header, quantum_header, metrics_df)
            st.markdown(table_html, unsafe_allow_html=True)

            classical_generated = (
                st.session_state.classical_rain_data is not None and
                st.session_state.classical_rain_data.get('algorithm') != "Select Classical Algorithm"
            )
            quantum_generated = (
                st.session_state.quantum_rain_data is not None and
                st.session_state.quantum_rain_data.get('algorithm') != "Select Quantum Algorithm"
            )

            if not classical_generated and not quantum_generated:
                st.info("Generate predictions to see performance metrics populate in the table above.")
            elif classical_generated and not quantum_generated:
                st.info("Generate quantum prediction to see quantum metrics populate in the table above.")
            elif not classical_generated and quantum_generated:
                st.info("Generate classical prediction to see classical metrics populate in the table above.")
            else:
                st.success("Both predictions generated! Performance metrics are now displayed in the table above.")

            with st.expander("Classification Metrics Explanation (Model Evaluation)", expanded=False):
                st.markdown("""
                **Understanding Classification Metrics for Rainfall Prediction:**

                **Confusion Matrix Components:**
                - **True Negatives (TN):** Correctly predicted "No Rain" days
                - **False Positives (FP):** Incorrectly predicted "Rain" when it didn't rain (Type I Error)
                - **False Negatives (FN):** Incorrectly predicted "No Rain" when it rained (Type II Error)
                - **True Positives (TP):** Correctly predicted "Rain" days

                **Performance Metrics:**
                - **Accuracy:** Overall correctness = (TP + TN) / Total. Shows general performance.
                - **Precision:** How many predicted rain days were actually rainy = TP / (TP + FP). High precision means fewer false alarms.
                - **Recall (Sensitivity):** How many actual rain days were caught = TP / (TP + FN). High recall means fewer missed rain events.
                - **F1-Score:** Harmonic mean of Precision and Recall = 2 × (Precision × Recall) / (Precision + Recall). Balances both metrics.

                **Why Both Classes Matter:**
                - **No Rain Metrics:** Important for planning outdoor activities, agriculture scheduling
                - **Rain Metrics:** Critical for flood warnings, water resource management

                **Ideal Values:** 
                - Accuracy, Precision, Recall, F1-Score should be close to 1.0
                - TN and TP should be high; FP and FN should be low
                """)

            st.markdown("---")

        with rain_subtab2:
            render_rain_noise_section()

        # ==================== RAIN LOCATION MAP ====================
        st.markdown('<h3>Location Map</h3>', unsafe_allow_html=True)

        col_map1, col_map2 = st.columns([1, 3])
        selected_subzone = None

        with col_map1:
            st.subheader("Selected Location")
            city = st.session_state.get('rain_generation_city', 'Delhi')

            if city and city in CITIES:
                city_info = CITIES[city]
                st.info(f"**Location:** {city}")
                st.write(f"**Region:** {city_info['region']}")
                st.write(f"**Coordinates:** {city_info['lat']:.4f}°N, {city_info['lon']:.4f}°E")

                if 'subzones' in city_info and city_info['subzones']:
                    st.markdown("---")
                    st.subheader("Subzone Selection")

                    subzone_options = ["None (City Level)"] + [f"{city} - {subzone}" for subzone in city_info['subzones'].keys()]

                    selected_subzone = st.selectbox(
                        "Select Subzone",
                        options=subzone_options,
                        key="rain_subzone_selector",
                        help="Select a specific subzone to view detailed predictions"
                    )

                    if selected_subzone != "None (City Level)":
                        subzone_name = selected_subzone.split(" - ")[1]
                        subzone_info = city_info['subzones'][subzone_name]
                        st.write(f"**Subzone Region:** {subzone_info['region']}")
                        st.write(f"**Coordinates:** {subzone_info['lat']:.4f}°N, {subzone_info['lon']:.4f}°E")
            else:
                st.warning("City information not available. Please configure city in settings.")

        with col_map2:
            st.subheader("Interactive Map")
            city = st.session_state.get('rain_generation_city', 'Delhi')

            if city and city in CITIES:
                # FIX: create_zoom_map now returns HTML string, render with components.html
                map_html = create_zoom_map(
                    city, CITIES, selected_subzone,
                    classical_data=st.session_state.get('classical_data'),
                    quantum_data=st.session_state.get('quantum_data'),
                    custom_datetime=st.session_state.get('custom_map_datetime')
                )
                components.html(map_html, height=500)
            else:
                st.warning("Please select a valid city")

    # ==================== Prediction SUB-TAB 3: CONCLUSION ====================
    with pre_tab3:
        render_conclusion_tab(REGRESSION_METRICS)


    
# ==================== TAB 4: Meteogram (METEOGRAM) ====================
with tab4:
    render_meteogram_tab()
# ==================== FOOTER ====================
render_footer()