"""
ui/meteogram_tab.py
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime as _dt

# ── Constants ──────────────────────────────────────────────────────────────────

CITIES = ["Delhi", "Mumbai", "Chennai"]

ALL_MODELS = {
    "QLSTM": "Quantum Long Short Term Memory (QLSTM)",
    "QGRU":  "Quantum Gated Recurrent Unit (QGRU)",
    "HQNN":  "Hybrid Quantum Neural Network (HQNN)",
    # "VQC":   "Variational Quantum Circuit (VQC)",
}

CLASSICAL_MODELS = {
    "LSTM": "Long Short Term Memory (LSTM)",
    "GRU":  "Gated Recurrent Unit (GRU)",
    "ANN":  "Artificial Neural Network (ANN)",
}

# ── OSPM Models ────────────────────────────────────────────────────────────────

OSPM_MODELS = {
    "TIMESFM":       "timesfm_2.5_200M-pytorch",
    "CHRONOS":       "Amazon/Chronos-2,t4 Model",
    "TSTRANSFORMER": "Timeseries Transformer Model",
}

MODEL_TYPES = ["Univariate", "Multivariate"]

PARAMS = {
    "temperature": {
        "label":         "🌡️ Temperature at 2m",
        "unit":          "°C",
        "pred_color":    "#e74c3c",
        "actual_color":  "#2c3e50",
        "cla_color":     "#e67e22",
        "fill":          "rgba(231,76,60,0.07)",
        "forecast_fill": "rgba(231,76,60,0.18)",
        "ylabel":        "<b>°C</b>",
        "yrange":        None,
        "prefix":        "temp",
    },
    "humidity": {
        "label":         "💧 Relative Humidity",
        "unit":          "%",
        "pred_color":    "#27ae60",
        "actual_color":  "#1a5276",
        "cla_color":     "#e67e22",
        "fill":          "rgba(39,174,96,0.07)",
        "forecast_fill": "rgba(39,174,96,0.18)",
        "ylabel":        "<b>%</b>",
        "yrange":        [0, 105],
        "prefix":        "hum",
    },
    "pressure": {
        "label":         "🔵 Pressure",
        "unit":          " hPa",
        "pred_color":    "#8e44ad",
        "actual_color":  "#1a5276",
        "cla_color":     "#2980b9",
        "fill":          "rgba(142,68,173,0.07)",
        "forecast_fill": "rgba(142,68,173,0.18)",
        "ylabel":        "<b>hPa</b>",
        "yrange":        None,
        "prefix":        "pres",
    },
}

_DATA_START = _dt.date(2024, 8, 11)
_DATA_END   = _dt.date(2024, 12, 31)


# ══════════════════════════════════════════════════════════════════════════════
# NCMRWF METEOGRAM STYLE — palette and per-parameter style spec
# ══════════════════════════════════════════════════════════════════════════════

NCMRWF = {
    "title_color":   "#7a2bbd",   # italic purple title at top of each panel
    "panel_title":   "#000000",   # black panel title inside the plot
    "actual":        "#000000",   # observed line
    "quantum":       "#e10600",   # primary forecast — red
    "classical":     "#b300a8",   # secondary forecast — magenta/purple
    "secondary_ax":  "#e10600",   # right-axis (humidity) ticks
    "grid":          "#bdbdbd",   # plot grid
    "border":        "#000000",   # plot border
    "paper_bg":      "#ffffff",
    "plot_bg":       "#ffffff",
    "panel_outer":   "#000000",   # outer black rectangle around the panel
    "font_family":   "Courier New, Courier, monospace",
}

# Per-parameter NCMRWF panel spec — title text and unit, identical to the
# reference image labels.  We render: Precipitation, MSLP, Temp+Humidity
# (dual axis), Wind speed+direction.
NCMRWF_PANELS = {
    "precipitation": {
        "title":     "Total Precipitation (mm/hr)",
        "ylabel":    "",
        "yrange":    None,
        "primary":   None,        # not derived from model output — placeholder
    },
    "pressure": {
        "title":     "Mean Sea Level Pressure (hPa)",
        "ylabel":    "",
        "yrange":    None,
        "primary":   "pressure",
    },
    "temperature": {
        "title":     "Temperature at 2m (Deg Celsius)",
        "title2":    "Relative Humidity at 2m (%)",
        "ylabel":    "",
        "yrange":    None,
        "primary":   "temperature",
        "secondary": "humidity",
    },
    "wind": {
        "title":     "Wind Speed (x) in km/hr",
        "title2":    "Wind Direction at 10m",
        "ylabel":    "",
        "yrange":    None,
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# Date-synchronisation helper
# Ensures Actual / Classical / Quantum frames for the SAME parameter start at
# the same date (the latest of their individual start dates) before plotting.
# This is the rule requested for all three cities and all three models.
# ══════════════════════════════════════════════════════════════════════════════

def _common_start(*frames):
    """Return the latest 'first datetime' across the given DataFrames."""
    starts = []
    for f in frames:
        if f is not None and not f.empty and "datetime" in f.columns:
            starts.append(pd.to_datetime(f["datetime"]).min())
    if not starts:
        return None
    return max(starts)


def _align_to_common_start(*frames):
    """Trim every supplied DataFrame so they all begin at the same datetime."""
    start = _common_start(*frames)
    out = []
    for f in frames:
        if f is None or f.empty or "datetime" not in f.columns or start is None:
            out.append(f)
            continue
        f2 = f[pd.to_datetime(f["datetime"]) >= start].copy()
        out.append(f2)
    return out


def _ncmrwf_xaxis(dt_series):
    """
    Build NCMRWF-style X-axis tick text:
      first tick   →  "19MAY\n2026"
      other ticks  →  "20MAY", "21MAY", ...
    Returns (tickvals, ticktext) for plotly with type='category'.
    """
    if dt_series is None or len(dt_series) == 0:
        return [], []
    ser = pd.to_datetime(dt_series).sort_values().drop_duplicates()
    # one tick per calendar day
    days = ser.dt.normalize().drop_duplicates().sort_values()
    vals, txt = [], []
    for i, d in enumerate(days):
        # categorical x-values are the formatted date strings used for the trace
        vals.append(d.strftime("%d %b %Y"))
        day_label = d.strftime("%d%b").upper()  # 19MAY
        if i == 0:
            txt.append(f"{day_label}<br>{d.year}")
        else:
            txt.append(day_label)
    return vals, txt


def _ncmrwf_header(city: str, model_label: str, run_dt=None) -> str:
    return f"{city.upper()}  10 DAY  {model_label}"


# ══════════════════════════════════════════════════════════════════════════════
# Helper — build explicit tick arrays from a list of datetime series
# ══════════════════════════════════════════════════════════════════════════════

def _fmt_date(dt_series):
    if dt_series is None or len(dt_series) == 0:
        return None
    return pd.to_datetime(dt_series).dt.strftime("%d %b %Y")


def _unique_date_labels(*datetime_series):
    seen = set()
    for s in datetime_series:
        if s is not None and len(s) > 0:
            for t in pd.to_datetime(s):
                seen.add(t.strftime("%d %b %Y"))
    if not seen:
        return []
    return sorted(seen, key=lambda d: pd.to_datetime(d, format="%d %b %Y"))


# ══════════════════════════════════════════════════════════════════════════════
# Entry point
# ══════════════════════════════════════════════════════════════════════════════

def render_meteogram_tab():
    from ui.meteogram_loader import load_meteogram_data
    load_meteogram_data()

    tab_qml, tab_ospm, tab_con = st.tabs([
        "⚛️ Quantum Machine Learning (QML)",
        "🤖 Open Source Pre-trained Model (OSPM)",
        "🏁 Conclusion",
    ])

    with tab_qml:
        _render_qml_tab()

    with tab_ospm:
        _render_ospm_tab()

    with tab_con:
        _render_conclusion_tab()


# ══════════════════════════════════════════════════════════════════════════════
# ██  QML TAB
# ══════════════════════════════════════════════════════════════════════════════

def _render_qml_tab():
    # Layout: charts on left (wider), config panel on right (narrower)
    col_main, col_cfg = st.columns([3, 1])
    with col_cfg:
        _render_sidebar()
    with col_main:
        _render_content()


# ── QML Sidebar ────────────────────────────────────────────────────────────────

def _render_sidebar():
    """Professional NCMRWF-style sidebar – clean card layout, light theme."""
    from ui.meteogram_loader import (
        get_loaded_params, get_loaded_classical_params,
    )
    import streamlit.components.v1 as components

    # ── Clean, professional card CSS (light background, subtle shadow) ──────
    st.markdown(
        """
        <style>
        /* Sidebar column card */
        section.main div[data-testid="column"]:has(.meteogram-side-marker) {
            background: #ffffff;
            border-radius: 20px;
            padding: 20px 18px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.02);
            border: 1px solid #eef2f6;
            transition: box-shadow 0.2s ease;
        }
        section.main div[data-testid="column"]:has(.meteogram-side-marker):hover {
            box-shadow: 0 12px 28px rgba(0,0,0,0.08);
        }
        /* Text colours inside the card */
        section.main div[data-testid="column"]:has(.meteogram-side-marker) label,
        section.main div[data-testid="column"]:has(.meteogram-side-marker) p,
        section.main div[data-testid="column"]:has(.meteogram-side-marker)
            div[data-baseweb="select"] span {
            color: #1e293b !important;
        }
        /* Headers and sections */
        .meteogram-side-header {
            font-size: 20px;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: -0.3px;
            margin-bottom: 4px;
        }
        .meteogram-side-subtitle {
            font-size: 13px;
            color: #475569;
            margin-bottom: 20px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 12px;
        }
        .meteogram-side-section {
            font-size: 13px;
            font-weight: 600;
            color: #334155;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 20px 0 12px 0;
        }
        .meteogram-side-divider {
            border: none;
            border-top: 1px solid #eef2f6;
            margin: 16px 0 8px 0;
        }
        .meteogram-info-block {
            background: #f8fafc;
            border-radius: 14px;
            padding: 12px 16px;
            font-size: 12px;
            margin-top: 12px;
        }
        .meteogram-info-block .label {
            color: #475569;
            font-weight: 500;
        }
        .meteogram-info-block .value {
            color: #0f172a;
            font-weight: 600;
            float: right;
        }
        /* Generate button - elegant gradient */
        div[data-testid="column"]:has(.meteogram-side-marker) div.stButton > button {
            width: 100%;
            background: linear-gradient(105deg, #2563eb 0%, #3b82f6 100%);
            color: white;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 0.3px;
            border: none;
            border-radius: 40px;
            padding: 10px 0;
            margin-top: 20px;
            margin-bottom: 8px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(37,99,235,0.25);
            transition: all 0.2s ease;
        }
        div[data-testid="column"]:has(.meteogram-side-marker) div.stButton > button:hover {
            background: linear-gradient(105deg, #1d4ed8 0%, #2563eb 100%);
            box-shadow: 0 6px 16px rgba(37,99,235,0.35);
            transform: translateY(-1px);
        }
        /* Streamlit widget tweaks */
        div[data-testid="column"]:has(.meteogram-side-marker) .stRadio > div {
            gap: 12px;
        }
        div[data-testid="column"]:has(.meteogram-side-marker) .stSelectbox label {
            font-weight: 500;
        }
        div[data-testid="column"]:has(.meteogram-side-marker) hr {
            margin: 8px 0;
        }
        </style>
        <div class="meteogram-side-marker"></div>
        <div class="meteogram-side-header">Meteogram</div>
        <div class="meteogram-side-subtitle">Meteogram Charts · City Wise</div>
        <div class="meteogram-side-section">Filters</div>
        """,
        unsafe_allow_html=True,
    )

    # ── 1. Location ───────────────────────────────────────────────────────
    st.selectbox("Location", CITIES, key="meteogram_city",
                 label_visibility="visible")

    # ── 2. Model Type ─────────────────────────────────────────────────────
    st.radio(
        "Model Type",
        MODEL_TYPES, horizontal=True,
        key="meteogram_model_type", index=1,
        label_visibility="visible",
    )

    city       = st.session_state.get("meteogram_city",       CITIES[0])
    model_type = st.session_state.get("meteogram_model_type", "Univariate")

    # ── 3. Quantum Algorithm ─────────────────────────────────────────────
    def _quantum_label(key):
        loaded = get_loaded_params(city, key, model_type)
        return ALL_MODELS[key] if loaded else f"{ALL_MODELS[key]}  ·  (No Data)"

    _MUMBAI_ONLY_Q = {"QSVR"}
    _UNIVARIATE_EXCLUDE_Q = {"QLSTM", "QGRU"} if model_type == "Univariate" else set()
    available_q_models = [
        k for k in ALL_MODELS
        if (k not in _MUMBAI_ONLY_Q or city == "Mumbai")
        and k not in _UNIVARIATE_EXCLUDE_Q
    ]
    current_q = st.session_state.get("meteogram_model_select", available_q_models[0])
    if current_q not in available_q_models:
        current_q = available_q_models[0]
        st.session_state["meteogram_model_select"] = current_q

    st.selectbox(
        "Quantum Algorithm",
        available_q_models,
        index=available_q_models.index(current_q),
        format_func=_quantum_label,
        key="meteogram_model_select",
        label_visibility="visible",
    )

    # ── 4. Classical Algorithm ───────────────────────────────────────────
    def _classical_label(key):
        loaded = get_loaded_classical_params(city, key, model_type)
        return CLASSICAL_MODELS[key] if loaded else f"{CLASSICAL_MODELS[key]}  ·  (No Data)"

    _MUMBAI_ONLY_C = {"SVR"}
    _UNIVARIATE_EXCLUDE_C = {"LSTM", "GRU"} if model_type == "Univariate" else set()
    available_c_models = [
        k for k in CLASSICAL_MODELS
        if (k not in _MUMBAI_ONLY_C or city == "Mumbai")
        and k not in _UNIVARIATE_EXCLUDE_C
    ]
    current_c = st.session_state.get("meteogram_classical_select", available_c_models[0])
    if current_c not in available_c_models:
        current_c = available_c_models[0]
        st.session_state["meteogram_classical_select"] = current_c

    st.selectbox(
        "Classical Algorithm",
        available_c_models,
        index=available_c_models.index(current_c),
        format_func=_classical_label,
        key="meteogram_classical_select",
        label_visibility="visible",
    )

    # ── Generate Forecast Button (professional style) ────────────────────
    if st.button("⚡ Generate Forecast", key="qml_generate_btn"):
        st.session_state["qml_generated"]      = True
        st.session_state["qml_gen_city"]       = st.session_state.get("meteogram_city",             CITIES[0])
        st.session_state["qml_gen_q_model"]    = st.session_state.get("meteogram_model_select",     "QLSTM")
        st.session_state["qml_gen_c_model"]    = st.session_state.get("meteogram_classical_select", "LSTM")
        st.session_state["qml_gen_model_type"] = st.session_state.get("meteogram_model_type",       "Multivariate")

    # ── Information Block (clean, card-like) ─────────────────────────────
    info_html = (
        '<hr class="meteogram-side-divider"/>'
        '<div class="meteogram-side-section">INFORMATION</div>'
        '<div class="meteogram-info-block">'
        '<div><span class="label">Model:</span>'
        f'<span class="value">{ALL_MODELS.get(current_q, current_q)}</span></div>'
        '<div style="clear:both;"></div>'
        '<div><span class="label">City:</span>'
        f'<span class="value">{city}</span></div>'
        '<div style="clear:both;"></div>'
        '<div><span class="label">Source:</span>'
        '<span class="value">NCMRWF</span></div>'
        '<div style="clear:both;"></div>'
        '</div>'
    )
    st.markdown(info_html, unsafe_allow_html=True)

# ── QML Main content ───────────────────────────────────────────────────────────

def _render_content():
    from ui.meteogram_loader import (
        get_param_df, get_loaded_params,
        get_classical_param_df, get_loaded_classical_params,
    )

    st.markdown(
        f"""
        <div style="background:#ffffff; border:1.5px solid {NCMRWF['title_color']};
                    border-radius:8px; padding:14px 20px; margin-bottom:12px;">
            <div style="font-family:{NCMRWF['font_family']}; font-size:20px;
                        font-weight:800; color:{NCMRWF['title_color']};
                        letter-spacing:1px; font-style:italic;">
                METEOGRAM
            </div>
            <div style="font-family:{NCMRWF['font_family']}; font-size:12px;
                        color:#555; margin-top:2px;">
                Meteogram Charts — City Wise &nbsp;·&nbsp; QML Forecasts
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

   # ── Guard: show placeholder until Generate is clicked ────────────────
    if not st.session_state.get("qml_generated", False):
        st.markdown(
            f"""
            <div style="
                display:flex; flex-direction:column; align-items:center;
                justify-content:center; gap:16px;
                background:#fafafa; border:2px dashed #c4b5fd;
                border-radius:14px; padding:60px 40px; margin-top:20px;
                text-align:center;
            ">
                <div style="font-size:48px;">⚡</div>
                <div style="font-size:20px; font-weight:800;
                            color:{NCMRWF['title_color']}; letter-spacing:0.4px;">
                    Ready to Generate Forecast
                </div>
                <div style="font-size:13px; color:#6b7280; max-width:400px; line-height:1.7;">
                    Select your <b>Location</b>, <b>Model Type</b>,
                    <b>Quantum Algorithm</b> and <b>Classical Algorithm</b>
                    in the panel on the right, then click
                    <b style="color:{NCMRWF['title_color']};">⚡ Generate Forecast</b>
                    to render the meteogram charts.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # ── Read snapshot saved when Generate was clicked ─────────────────────
    city       = st.session_state.get("qml_gen_city",       CITIES[0])
    q_model    = st.session_state.get("qml_gen_q_model",    "QLSTM")
    c_model    = st.session_state.get("qml_gen_c_model",    "LSTM")
    model_type = st.session_state.get("qml_gen_model_type", "Multivariate")

    q_loaded = get_loaded_params(city, q_model, model_type)
    c_loaded = get_loaded_classical_params(city, c_model, model_type)

    _render_header_card(
        city, q_model, c_model, model_type, q_loaded,
        lambda p: get_param_df(city, q_model, model_type, p),
    )

    _render_all_charts(
        city, q_model, c_model, model_type, q_loaded, c_loaded,
        lambda p: get_param_df(city, q_model, model_type, p),
        lambda p: get_classical_param_df(city, c_model, model_type, p),
    )

    _render_metrics_matrix(model_type)
    # _render_map(city, source="qml")

# ── Last-value helpers for map popup ──────────────────────────────────────────

def _get_last_param_values(city: str) -> dict:
    from ui.meteogram_loader import get_param_df, get_loaded_params

    model_type = st.session_state.get("meteogram_model_type", "Multivariate")
    q_model    = st.session_state.get("meteogram_model_select", "QLSTM")
    loaded     = get_loaded_params(city, q_model, model_type)

    result = {}
    for param, cfg in PARAMS.items():
        actual_col = param + "_actual"
        if param in loaded:
            df = get_param_df(city, q_model, model_type, param)
            if df is not None and len(df) > 0:
                entry = {
                    "unit":         cfg["unit"].strip(),
                    "label":        cfg["label"],
                    "actual":       None,
                    "quantum":      None,
                    "source_label": "⚛️ Quantum",
                }
                if actual_col in df.columns:
                    entry["actual"] = float(df[actual_col].iloc[-1])
                if param in df.columns:
                    entry["quantum"] = float(df[param].iloc[-1])
                result[param] = entry
    return result


def _get_last_ospm_param_values(city: str) -> dict:
    from ui.meteogram_loader import get_ospm_param_df, get_loaded_ospm_params

    model       = st.session_state.get("ospm_model_select", "TIMESFM")
    model_type  = "Univariate"
    model_label = OSPM_MODELS.get(model, model)

    try:
        loaded = get_loaded_ospm_params(city, model, model_type)
    except Exception:
        loaded = []

    result = {}
    for param, cfg in PARAMS.items():
        actual_col = param + "_actual"
        if param in loaded:
            try:
                df = get_ospm_param_df(city, model, model_type, param)
                if df is not None and len(df) > 0:
                    entry = {
                        "unit":         cfg["unit"].strip(),
                        "label":        cfg["label"],
                        "actual":       None,
                        "quantum":      None,
                        "source_label": f"🤖 {model_label[:20]}",
                    }
                    if actual_col in df.columns:
                        entry["actual"] = float(df[actual_col].iloc[-1])
                    if param in df.columns:
                        entry["quantum"] = float(df[param].iloc[-1])
                    result[param] = entry
            except Exception:
                pass
    return result


# ── Param badges ───────────────────────────────────────────────────────────────

def _render_param_badges(q_loaded: list, c_loaded: list, get_q_df_fn):
    parts = []
    for param, cfg in PARAMS.items():
        q_present  = param in q_loaded
        c_present  = param in c_loaded
        present    = q_present or c_present
        color      = cfg["pred_color"] if present else "#9ca3af"
        bg         = f"{color}18"
        border     = color if present else "#d1d5db"
        opacity    = "1" if present else "0.45"

        df         = get_q_df_fn(param) if q_present else None
        has_actual = q_present and df is not None and (param + "_actual") in df.columns
        icon       = "✅" if present else "⬜"
        actual_tag = ' <span style="font-size:10px; opacity:0.75">· actual + predicted</span>' if has_actual else ""
        cla_tag    = ' <span style="font-size:10px; opacity:0.75">· +classical</span>' if c_present else ""
        parts.append(
            f'<span style="background:{bg}; border:1px solid {border}; border-radius:6px;'
            f' padding:4px 12px; font-size:12px; color:{color}; font-weight:600;'
            f' opacity:{opacity};">{icon} {cfg["label"]}{actual_tag}{cla_tag}</span>'
        )
    st.markdown(
        '<div style="display:flex; gap:8px; flex-wrap:wrap; margin-bottom:14px;">'
        + "".join(parts) + "</div>",
        unsafe_allow_html=True,
    )


# ── Header card ────────────────────────────────────────────────────────────────

def _render_header_card(city, q_model, c_model, model_type, q_loaded, get_q_df_fn):
    """Compact NCMRWF-style header card.

    Rendered via streamlit.components.v1.html (NOT st.markdown) so that
    no whitespace-indentation in the HTML is misinterpreted as a markdown
    code-block — that was the root cause of the raw-HTML render bug.
    """
    import streamlit.components.v1 as components

    q_label = ALL_MODELS.get(q_model, q_model)
    c_label = CLASSICAL_MODELS.get(c_model, c_model)

    def _avg(param):
        if param not in q_loaded:
            return "—"
        df = get_q_df_fn(param)
        if df is not None and param in df.columns:
            return f"{df[param].mean():.1f}{PARAMS[param]['unit']}"
        return "—"

    date_range = "—"
    for param in q_loaded:
        df = get_q_df_fn(param)
        if df is not None and "datetime" in df.columns and len(df) > 0:
            # Filter to forecast-only for accurate date range
            df_filtered = _forecast_only(df)
            if df_filtered is not None and not df_filtered.empty:
                date_range = (
                    f"{df_filtered['datetime'].iloc[0].strftime('%d %b')} – "
                    f"{df_filtered['datetime'].iloc[-1].strftime('%d %b %Y')}"
                )
                break

    badge = "🟢 Real Data" if q_loaded else "🔴 No Data Loaded"

    # Build all parameter pills as a single FLAT string (no leading whitespace)
    pills_html = ""

    ff = NCMRWF["font_family"]
    tc = NCMRWF["title_color"]

    # Flat single-line HTML (no leading whitespace anywhere outside style tags)
    html = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><style>"
        "*{box-sizing:border-box;margin:0;padding:0;}"
        f"body{{font-family:{ff};background:transparent;color:#111;}}"
        ".ncwrap{background:#ffffff;border:1px solid #d1d5db;"
        f"border-left:4px solid {tc};border-radius:8px;padding:14px 18px;}}"
        ".ncrow{display:flex;flex-wrap:wrap;gap:18px;align-items:baseline;}"
        ".ncloc{font-size:22px;font-weight:800;color:#111;letter-spacing:0.5px;}"
        ".ncmeta{font-size:12px;color:#444;}"
        ".ncmodels{margin-top:6px;font-size:12px;color:#444;}"
        f"<div class='ncpills'>{pills_html}</div>"
        "</style></head><body>"
        "<div class='ncwrap'>"
          "<div class='ncrow'>"
            f"<div class='ncloc'>📍 {city.upper()}</div>"
            f"<div class='ncmeta'>{date_range}</div>"
            f"<div class='ncmeta'>{badge}</div>"
            f"<div class='ncmeta'>Type: <b>{model_type}</b></div>"
          "</div>"
          "<div class='ncmodels'>"
            f"⚛️ <b>Quantum:</b> {q_label} &nbsp;·&nbsp; "
            f"🖥️ <b>Classical:</b> {c_label}"
          "</div>"
          f"<div class='ncpills'>{pills_html}</div>"
        "</div>"
        "</body></html>"
    )
    components.html(html, height=180, scrolling=False)

# Map each parameter to NCMRWF-style panel metadata
_NC_PANEL_META = {
    "pressure": {
        "title":  "Mean Sea Level Pressure (hPa)",
        "y_unit": "hPa",
        "y_fmt":  "{:.1f}",
        "yrange_pad_factor": 0.10,  # pressure values vary little — give 10% pad
    },
    "temperature": {
        "title":  "Temperature at 2m (Deg Celsius)",
        "y_unit": "°C",
        "y_fmt":  "{:.1f}",
        "yrange_pad_factor": 0.15,
    },
    "humidity": {
        "title":  "Relative Humidity at 2m (%)",
        "y_unit": "%",
        "y_fmt":  "{:.0f}",
        "yrange_pad_factor": 0.10,
        "yrange_clamp": (0, 100),
    },
}


def _build_ncmrwf_single_figure(
    param: str,
    header_label: str,
    df_actual: "pd.DataFrame | None",
    df_quantum: "pd.DataFrame | None",
    df_classical: "pd.DataFrame | None",
    actual_color: str = None,
):
    """Build ONE NCMRWF-style figure for ONE parameter.

    All three frames are expected to already be:
      • forecast-only   (caller filters out historical rows)
      • date-aligned    (caller ensures common start date)
      • clipped to last 10 days

    Each frame must contain a 'datetime' column and either:
      • the bare parameter column (e.g. 'temperature') for forecasts, OR
      • a '*_actual' column for the observed series
    """
    meta = _NC_PANEL_META[param]
    fig = go.Figure()

    # Determine x-axis range from union of inputs
    candidate_dts = []
    for f in (df_actual, df_quantum, df_classical):
        if f is not None and not f.empty and "datetime" in f.columns:
            candidate_dts.append(pd.to_datetime(f["datetime"]))
    if not candidate_dts:
        fig.add_annotation(
            text=f"No {param} forecast data for this selection",
            x=0.5, y=0.5, xref="paper", yref="paper",
            showarrow=False, font=dict(size=13, color="#666"),
        )
        fig.update_layout(height=260, paper_bgcolor="#fff", plot_bgcolor="#fff")
        return fig

    full_dt = pd.concat(candidate_dts)
    x_min, x_max = full_dt.min(), full_dt.max()

    # NCMRWF tick text: per-day, year on first
    day_min = pd.Timestamp(x_min).normalize()
    day_max = pd.Timestamp(x_max).normalize()          # ← remove the +1 day
    data_end_ts = pd.Timestamp(_DATA_END)
    if day_max > data_end_ts:
        day_max = data_end_ts                          # ← hard cap at 31 DEC
    days = pd.date_range(day_min, day_max, freq="D")
    tickvals = list(days)
    ticktext = []
    for i, d in enumerate(days):
        day_label = d.strftime("%d%b").upper()
        ticktext.append(f"{day_label}<br>{d.year}" if i == 0 else day_label)

    # ── Add traces — order matters for NCMRWF look ───────────────────────────
    # Quantum first so red is on top of magenta and black overlays it.
    actual_clr = actual_color or NCMRWF["actual"]

    def _add(src, col, color, name, unit, dash="solid"):
        if src is None or src.empty or "datetime" not in src.columns or col not in src.columns:
            return False
        x = pd.to_datetime(src["datetime"])
        y = src[col]
        fig.add_trace(go.Scatter(
            x=x, y=y, name=name, mode="lines",
            line=dict(color=color, width=1.2, dash=dash),
            showlegend=False,
            hovertemplate=(
                f"<b>%{{x|%d %b %H:%M}}</b><br>"
                f"{name}: %{{y:.2f}} {unit}<extra></extra>"
            ),
        ))
        return True

    # Classical (magenta, bottom layer)
    _add(df_classical, param, NCMRWF["classical"], "Classical", meta["y_unit"])
    # Quantum (red, middle layer)
    _add(df_quantum,   param, NCMRWF["quantum"],   "Quantum",   meta["y_unit"])
    # Actual observed during forecast window (black, top layer)
    actual_col = f"{param}_actual"
    if df_actual is not None and actual_col in df_actual.columns:
        _add(df_actual, actual_col, actual_clr, "Actual", meta["y_unit"])
    elif df_actual is not None and param in df_actual.columns:
        _add(df_actual, param,      actual_clr, "Actual", meta["y_unit"])

    # ── Y-axis range with sane padding (and humidity clamp) ──────────────────
    all_y = []
    for src, col in [
        (df_classical, param),
        (df_quantum,   param),
        (df_actual,    actual_col if df_actual is not None and actual_col in df_actual.columns else param),
    ]:
        if src is not None and col in (src.columns if src is not None else []):
            all_y.append(src[col])
    yrange = None
    if all_y:
        merged = pd.concat([s.dropna() for s in all_y if s is not None and not s.dropna().empty])
        if not merged.empty:
            y_min, y_max = float(merged.min()), float(merged.max())
            spread = y_max - y_min
            pad = max(spread * meta["yrange_pad_factor"], 0.5)
            y_lo, y_hi = y_min - pad, y_max + pad
            clamp = meta.get("yrange_clamp")
            if clamp:
                y_lo = max(y_lo, clamp[0])
                y_hi = min(y_hi, clamp[1])
            yrange = [y_lo, y_hi]

    # ── Axis styling per NCMRWF look ─────────────────────────────────────────
    fig.update_xaxes(
        type="date",
        range=[day_min, day_max],
        tickmode="array",
        tickvals=tickvals,
        ticktext=ticktext,
        showgrid=True, gridcolor=NCMRWF["grid"], griddash="dot",
        showline=True, linecolor=NCMRWF["border"], linewidth=1,
        mirror=True,
        tickfont=dict(family=NCMRWF["font_family"], size=10, color="#000"),
        ticks="outside", ticklen=4, tickcolor="#000",
    )
    fig.update_yaxes(
        range=yrange,
        showgrid=True, gridcolor=NCMRWF["grid"], griddash="dot",
        showline=True, linecolor=NCMRWF["border"], linewidth=1,
        mirror=True,
        tickfont=dict(family=NCMRWF["font_family"], size=10, color="#000"),
        ticks="outside", ticklen=4, tickcolor="#000",
        zeroline=False,
    )

    # ── Annotations: NCMRWF header + panel title ────────────────────────────
    annotations = [
        dict(
            xref="paper", yref="paper",
            x=0.5, y=1.10, xanchor="center", yanchor="bottom",
            text=f"<i><b>{header_label}</b></i>",
            showarrow=False,
            font=dict(family=NCMRWF["font_family"], size=12,
                      color=NCMRWF["title_color"]),
        ),
        dict(
            xref="x domain", yref="y domain",
            x=0.5, y=0.93, xanchor="center", yanchor="bottom",
            text=meta["title"],
            showarrow=False, bgcolor="rgba(255,255,255,0.85)",
            font=dict(family=NCMRWF["font_family"], size=11, color="#000"),
        ),
    ]

    fig.update_layout(
        height=290,
        paper_bgcolor=NCMRWF["paper_bg"],
        plot_bgcolor=NCMRWF["plot_bg"],
        margin=dict(t=80, b=40, l=70, r=30),
        showlegend=False,
        hovermode="x unified",
        hoverlabel=dict(bgcolor="white", font_family=NCMRWF["font_family"],
                        font_size=11, bordercolor="#000"),
        annotations=annotations,
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# Helpers: forecast-only filter + last-N-days clip
# ══════════════════════════════════════════════════════════════════════════════

_FORECAST_DAYS = 10  # last 10 days of forecast data — per UI spec


def _forecast_only(df):
    """Keep only forecast rows. 
    
    Priority: 
    1. Use _is_forecast flag if available
    2. If no flag, assume dates after Dec 21, 2024 are forecast
    """
    if df is None or df.empty:
        return df
    
    if "_is_forecast" in df.columns:
        # Filter by flag (True = forecast)
        return df[df["_is_forecast"] == True].copy()
    
    # Fallback: if no flag, assume forecast dates are after Dec 21, 2024
    if "datetime" in df.columns:
        forecast_cutoff = pd.Timestamp("2024-12-21")
        return df[pd.to_datetime(df["datetime"]) > forecast_cutoff].copy()
    
    return df.copy()


def _clip_last_n_days(df, n=_FORECAST_DAYS):
    """Keep only the last n calendar days of the frame, by 'datetime' column.
    Also hard-clips to _DATA_END so no bleed-over dates appear on the chart.
    """
    if df is None or df.empty or "datetime" not in df.columns:
        return df
    
    # Get the maximum datetime in the dataframe
    last_t = pd.to_datetime(df["datetime"]).max()
    # Calculate cutoff (n days before last_t)
    cutoff = last_t - pd.Timedelta(days=n-1)
    
    # Also hard cap at _DATA_END (Dec 31, 2024)
    data_end = pd.Timestamp(_DATA_END) + pd.Timedelta(hours=23, minutes=59)
    
    mask = (pd.to_datetime(df["datetime"]) >= cutoff) & (pd.to_datetime(df["datetime"]) <= data_end)
    return df[mask].copy()


def _forecast_window(df_actual, df_quantum, df_classical, n=_FORECAST_DAYS):
    """Apply forecast-only + last-N-days clip + common-start alignment.
    
    IMPORTANT: Uses _is_forecast flag to separate forecast from historical data.
    If _is_forecast column doesn't exist, assumes dates after Dec 21 are forecast.
    """
    af = _forecast_only(df_actual)
    qf = _forecast_only(df_quantum)
    cf = _forecast_only(df_classical)
    
    # Get the last date from quantum forecast (should be Dec 31)
    if qf is not None and not qf.empty and "datetime" in qf.columns:
        last_date = pd.to_datetime(qf["datetime"]).max()
        cutoff = last_date - pd.Timedelta(days=n-1)  # Show exactly n days
        
        # Apply date filter to ALL dataframes
        if af is not None and not af.empty and "datetime" in af.columns:
            af = af[pd.to_datetime(af["datetime"]) >= cutoff]
        if qf is not None and not qf.empty and "datetime" in qf.columns:
            qf = qf[pd.to_datetime(qf["datetime"]) >= cutoff]
        if cf is not None and not cf.empty and "datetime" in cf.columns:
            cf = cf[pd.to_datetime(cf["datetime"]) >= cutoff]
    
    return _align_to_common_start(af, qf, cf)


# ══════════════════════════════════════════════════════════════════════════════
# ██  NCMRWF panel wrapper — outer black-bordered card around the figure
# ══════════════════════════════════════════════════════════════════════════════

def _ncmrwf_panel_open():
    st.markdown(
        """
        <div style="
            background:#ffffff;
            border:1.5px solid #000;
            border-radius:6px;
            padding:14px 12px 6px 12px;
            margin:8px 0 14px 0;
            box-shadow:0 2px 6px rgba(0,0,0,0.05);
        ">
        """,
        unsafe_allow_html=True,
    )

def _ncmrwf_panel_close():
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# Build merged DataFrames for the NCMRWF figure
# ══════════════════════════════════════════════════════════════════════════════

def _build_actual_df(get_q_df_fn, q_loaded):
    """Merge the *_actual columns across all parameters into one frame.

    Loader returns one DF per param. We outer-join on datetime so the NCMRWF
    figure can pull pressure_actual, temperature_actual, humidity_actual from a
    single 'Actual' frame.
    """
    base = None
    for param in q_loaded:
        df = get_q_df_fn(param)
        if df is None or "datetime" not in df.columns:
            continue
        keep_cols = ["datetime"]
        # carry over both the actual and predicted columns
        for c in (f"{param}_actual", param, "_is_forecast"):
            if c in df.columns and c not in keep_cols:
                keep_cols.append(c)
        sub = df[keep_cols].drop_duplicates(subset=["datetime"])
        base = sub if base is None else base.merge(sub, on="datetime", how="outer")
    if base is None:
        return None
    return base.sort_values("datetime").reset_index(drop=True)


def _build_model_df(get_df_fn, loaded):
    """Merge predicted-only columns across params into one frame."""
    base = None
    for param in loaded:
        df = get_df_fn(param)
        if df is None or "datetime" not in df.columns or param not in df.columns:
            continue
        cols = ["datetime", param]
        if "_is_forecast" in df.columns:
            cols.append("_is_forecast")
        sub = df[cols].drop_duplicates(subset=["datetime"])
        base = sub if base is None else base.merge(sub, on="datetime", how="outer")
    if base is None:
        return None
    return base.sort_values("datetime").reset_index(drop=True)


# ══════════════════════════════════════════════════════════════════════════════
# Filter a frame to a date range
# ══════════════════════════════════════════════════════════════════════════════

def _filter_dr(df, start_d, end_d):
    if df is None or df.empty or "datetime" not in df.columns:
        return df
    s = pd.Timestamp(start_d)
    e = pd.Timestamp(end_d) + pd.Timedelta(hours=23, minutes=59)
    return df[(df["datetime"] >= s) & (df["datetime"] <= e)].copy()


# ══════════════════════════════════════════════════════════════════════════════
# ██  CHARTS (QML) — Side-by-side: Classical|Actual  and  Quantum|Actual
# ══════════════════════════════════════════════════════════════════════════════

def _render_all_charts(city, q_model, c_model, model_type,
                       q_loaded, c_loaded,
                       get_q_df_fn, get_c_df_fn):
    """NCMRWF-style THREE separate figures (Pressure, Temperature, Humidity).

    Constraints:
      • Forecast-only data (rows with _is_forecast == True)
      • Last 10 days only
      • All three series (Actual / Quantum / Classical) date-aligned
      • Three separate panels — NOT combined
      • No precipitation, no wind
    """
    import streamlit.components.v1 as components

    # ── Build the three merged frames (Actual / Quantum / Classical) ─────
    actual_df    = _build_actual_df(get_q_df_fn, q_loaded)
    quantum_df   = _build_model_df (get_q_df_fn, q_loaded)
    classical_df = _build_model_df (get_c_df_fn, c_loaded)

    # ── Forecast-only + last 10 days + common-start alignment ────────────
    actual_df, quantum_df, classical_df = _forecast_window(
        actual_df, quantum_df, classical_df, n=_FORECAST_DAYS
    )

    # ── Forecast colour-key band (flat HTML, components.html) ────────────
    ff = NCMRWF["font_family"]
    key_html = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><style>"
        "*{box-sizing:border-box;margin:0;padding:0;}"
        f"body{{font-family:{ff};background:transparent;color:#111;}}"
        ".keywrap{display:flex;gap:14px;flex-wrap:wrap;align-items:center;"
        "background:#fafafa;border:1px solid #e2e8f0;border-radius:8px;"
        "padding:8px 14px;font-size:12px;}"
        ".keysw{display:inline-block;width:18px;height:3px;"
        "vertical-align:middle;margin-right:6px;}"
        ".keynote{margin-left:auto;color:#666;}"
        "</style></head><body><div class='keywrap'>"
        f"<div><span class='keysw' style='background:{NCMRWF['actual']}'></span><b>Actual</b></div>"
        f"<div><span class='keysw' style='background:{NCMRWF['quantum']}'></span><b>Quantum ({q_model})</b></div>"
        f"<div><span class='keysw' style='background:{NCMRWF['classical']}'></span><b>Classical ({c_model})</b></div>"
        f"<div class='keynote'>Forecast-only · Last {_FORECAST_DAYS} days · All series aligned</div>"
        "</div></body></html>"
    )
    components.html(key_html, height=50, scrolling=False)

    # ── Render three separate NCMRWF panels: Pressure → Temperature → Humidity
    panel_order = ["pressure", "temperature", "humidity"]
    header_label = _ncmrwf_header(city, model_label=f"{q_model}/{c_model}")

    for param in panel_order:
        has_q = param in q_loaded
        has_c = param in c_loaded
        if not has_q and not has_c:
            st.info(
                f"No forecast data for {PARAMS[param]['label']}. "
                f"Add quantum: `{PARAMS[param]['prefix']}_{city.lower()}_{q_model.lower()}.csv` or "
                f"classical: `cla_{PARAMS[param]['prefix']}_{city.lower()}_{c_model.lower()}.csv`."
            )
            continue

        _ncmrwf_panel_open()
        fig = _build_ncmrwf_single_figure(
            param=param,
            header_label=header_label,
            df_actual=actual_df,
            df_quantum=quantum_df,
            df_classical=classical_df,
        )
        st.plotly_chart(
            fig, use_container_width=True,
            config={"displayModeBar": True, "displaylogo": False},
        )
        _ncmrwf_panel_close()




# ── CSV-generation helper ──────────────────────────────────────────────────────

def _metrics_to_csv(data: dict) -> str:
    rows = []
    params  = ["temperature", "humidity", "pressure"]
    splits  = ["Forecast"]
    metrics = ["R2", "RMSE", "MAE"]

    header = ["Metric"]
    for param in params:
        for split in splits:
            header.append(f"{param.capitalize()}_{split}")
    rows.append(",".join(header))

    for metric in metrics:
        label = "R2_Score" if metric == "R2" else metric
        row = [label]
        for param in params:
            for split in splits:
                val = data.get(param, {}).get(split, {}).get(metric, None)
                row.append(f"{val:.4f}" if val is not None else "")
        rows.append(",".join(row))

    return "\n".join(rows)


# ── Metrics data ───────────────────────────────────────────────────────────────

def _empty_metrics():
    return {
        "temperature": {
            "Test":     {"R2": None, "RMSE": None, "MAE": None},
            "Forecast": {"R2": None, "RMSE": None, "MAE": None},
        },
        "humidity": {
            "Test":     {"R2": None, "RMSE": None, "MAE": None},
            "Forecast": {"R2": None, "RMSE": None, "MAE": None},
        },
        "pressure": {
            "Test":     {"R2": None, "RMSE": None, "MAE": None},
            "Forecast": {"R2": None, "RMSE": None, "MAE": None},
        },
    }


METRICS_DATA = {
    "Univariate": {
        "Delhi": {
            "QLSTM": {
                "temperature": {
                    "Test":     {"R2":  0.969499, "RMSE": 1.125916, "MAE": 0.884024},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
                "humidity": {
                    "Test":     {"R2": None, "RMSE": None, "MAE": None},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
                "pressure": {
                    "Test":     {"R2": None, "RMSE": None, "MAE": None},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
            },
            "QGRU": {
                "temperature": {
                    "Test":     {"R2": 0.9716417789459229, "RMSE": 1.085641889336451, "MAE": 0.8337191343307495},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
                "humidity": {
                    "Test":     {"R2": None, "RMSE": None, "MAE": None},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
                "pressure": {
                    "Test":     {"R2": None, "RMSE": None, "MAE": None},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
            },
            "HQNN": {
                "temperature": {
                    "Test":     {"R2": 0.4531, "RMSE": 1.01746471, "MAE": 0.777872721},
                    "Forecast": {"R2": 0.2715, "RMSE": 1.53798, "MAE": 0.7940554},
                },
                "humidity": {
                    "Test":     {"R2": 0.343245625, "RMSE": 5.031982654, "MAE": 3.672473537},
                    "Forecast": {"R2": 0.310476, "RMSE": 5.542, "MAE": 3.97154},
                },
                "pressure": {
                    "Test":     {"R2": 0.3251, "RMSE": 138.3001425, "MAE": 109.4451497},
                    "Forecast": {"R2": 0.1329, "RMSE": 139.4682, "MAE": 110.4935},
                },
            },
            "VQC": {
                "temperature": {
                    "Test":     {"R2": 0.9736915826797485, "RMSE": 1.0456690318520958, "MAE": 0.795380711555481},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
                "humidity": {
                    "Test":     {"R2": None, "RMSE": None, "MAE": None},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
                "pressure": {
                    "Test":     {"R2": None, "RMSE": None, "MAE": None},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
            },
            "QSVR": _empty_metrics(),
        },
        "Mumbai": {
            "QLSTM": _empty_metrics(),
            "QGRU":  _empty_metrics(),
            "HQNN": {
                "temperature": {
                    "Test":     {"R2": 0.893448472, "RMSE": 0.76472841, "MAE": 0.563263178},
                    "Forecast": {"R2": 0.5631, "RMSE": 0.7715, "MAE": 0.58045},
                },
                "humidity": {
                    "Test":     {"R2": 0.676693201, "RMSE": 4.974541893, "MAE": 3.734124899},
                    "Forecast": {"R2": 0.412, "RMSE": 5.04168, "MAE": 3.91501},
                },
                "pressure": {
                    "Test":     {"R2": 0.862435222, "RMSE": 106.547167152041, "MAE": 84.3186340332031},
                    "Forecast": {"R2": 0.334, "RMSE": 107.6715, "MAE": 85.348504},
                },
            },
            "VQC":  _empty_metrics(),
            "QSVR": _empty_metrics(),
        },
        "Chennai": {
            "QLSTM": _empty_metrics(),
            "QGRU":  _empty_metrics(),
            "HQNN": {
                "temperature": {
                    "Test":     {"R2": 0.754667699, "RMSE": 0.598978438, "MAE": 0.458837509},
                    "Forecast": {"R2": 0.23, "RMSE": 0.622145, "MAE": 0.4746},
                },
                "humidity": {
                    "Test":     {"R2": 0.413188815, "RMSE": 4.276246203, "MAE": 3.28816247},
                    "Forecast": {"R2": 0.25, "RMSE": 4.781, "MAE": 3.564},
                },
                "pressure": {
                    "Test":     {"R2": 0.845790148, "RMSE": 102.1787219, "MAE": 82.35714722},
                    "Forecast": {"R2": 0.1712, "RMSE": 102.568, "MAE": 85.64751},
                },
            },
            "VQC":  _empty_metrics(),
            "QSVR": _empty_metrics(),
        },
    },
    "Multivariate": {
        "Delhi": {
            "QLSTM": {
                "temperature": {
                    "Test":     {"R2": 0.925687926196368, "RMSE": 1.29080663114773,  "MAE": 1.03223533727445},
                    "Forecast": {"R2": 0.202056542160729, "RMSE": 1.84617463992224,  "MAE": 1.40612272303038},
                },
                "humidity": {
                    "Test":     {"R2": 0.792290339811146, "RMSE": 6.98904419455126,  "MAE": 4.84820995880449},
                    "Forecast": {"R2": 0.272308610099231, "RMSE": 7.85706917130337,  "MAE": 6.58936480388532},
                },
                "pressure": {
                    "Test":     {"R2": 0.927343925195917, "RMSE": 1.76182264420002,  "MAE": 1.3494468672625},
                    "Forecast": {"R2": 0.13945260727438,  "RMSE": 2.068823603230037, "MAE": 1.75378976162716},
                },
            },
            "QGRU": {
                "temperature": {
                    "Test":     {"R2": 0.931613491691977, "RMSE": 1.23827388040174, "MAE": 0.986967428128415},
                    "Forecast": {"R2": 0.511161465331708, "RMSE": 1.44500529520805, "MAE": 1.23647724444015},
                },
                "humidity": {
                    "Test":     {"R2": 0.815993445881264, "RMSE": 6.57818503316272,  "MAE": 4.72804403016743},
                    "Forecast": {"R2": 0.444744302630124, "RMSE": 6.86330770367325,  "MAE": 5.84505247856468},
                },
                "pressure": {
                    "Test":     {"R2": 0.934000575438247, "RMSE": 1.67917630097599, "MAE": 1.31290324978439},
                    "Forecast": {"R2": 0.195784214310401, "RMSE": 1.99996484880623, "MAE": 1.78504453777518},
                },
            },
            "HQNN": {
                "temperature": {
                    "Test":     {"R2": 0.35, "RMSE": 1.78, "MAE": 1.54},
                    "Forecast": {"R2": 0.8,  "RMSE": 2.87, "MAE": 2.43},
                },
                "humidity": {
                    "Test":     {"R2": 0.47, "RMSE": 2.81, "MAE": 2.46},
                    "Forecast": {"R2": 0.35, "RMSE": 4.12, "MAE": 3.9},
                },
                "pressure": {
                    "Test":     {"R2": 0.71, "RMSE": 1.94, "MAE": 1.79},
                    "Forecast": {"R2": 0.67, "RMSE": 2.93, "MAE": 2.72},
                },
            },
            "VQC":  _empty_metrics(),
            "QSVR": _empty_metrics(),
        },
        "Mumbai": {
            "QLSTM": {
                "temperature": {
                    "Test":     {"R2": 0.827730919111141, "RMSE": 0.747898798558533, "MAE": 0.613603691303886},
                    "Forecast": {"R2": 0.387473889863828, "RMSE": 1.49941931887071,  "MAE": 1.13850697940633},
                },
                "humidity": {
                    "Test":     {"R2": 0.618499366093747, "RMSE": 4.27329158064992, "MAE": 3.39510895395841},
                    "Forecast": {"R2": 0.158834504960419, "RMSE": 8.2655834113826,  "MAE": 6.99031502556002},
                },
                "pressure": {
                    "Test":     {"R2": 0.851647641684127, "RMSE": 1.38050628966804, "MAE": 1.07926930138228},
                    "Forecast": {"R2": 0.476422367976195, "RMSE": 1.28974209942868, "MAE": 0.918493557546636},
                },
            },
            "QGRU": {
                "temperature": {
                    "Test":     {"R2": 0.856770194251275, "RMSE": 0.681955236792204, "MAE": 0.545647035854281},
                    "Forecast": {"R2": 0.612546135438264, "RMSE": 1.19253407584907,  "MAE": 0.919654722966202},
                },
                "humidity": {
                    "Test":     {"R2": 0.636570045548833, "RMSE": 4.17085656726519, "MAE": 3.25879476818528},
                    "Forecast": {"R2": 0.242458428392273, "RMSE": 7.84397179659454,  "MAE": 6.53751492807734},
                },
                "pressure": {
                    "Test":     {"R2": 0.888897669622604, "RMSE": 1.19468317251182, "MAE": 0.954685474913417},
                    "Forecast": {"R2": 0.623900192460402, "RMSE": 1.09311005574885,  "MAE": 0.808976658317139},
                },
            },
            "HQNN": {
                "temperature": {
                    "Test":     {"R2": 0.884390890598297, "RMSE": 0.796569017493611, "MAE": 0.621898651123047},
                    "Forecast": {"R2": 0.517897248268127, "RMSE": 1.62062518230515,  "MAE": 1.11045074462891},
                },
                "humidity": {
                    "Test":     {"R2": 0.585307598114014, "RMSE": 5.63389409827442,  "MAE": 4.14736747741699},
                    "Forecast": {"R2": 0.239784002304077, "RMSE": 7.70499643492817,  "MAE": 5.31425046920776},
                },
                "pressure": {
                    "Test":     {"R2": 0.794146656990051, "RMSE": 130.33683825477,   "MAE": 100.182563781738},
                    "Forecast": {"R2": 0.585998117923737, "RMSE": 178.009792787153,  "MAE": 134.293746948242},
                },
            },
            "VQC":  _empty_metrics(),
            "QSVR": {
                "temperature": {
                    "Test":     {"R2": 0.7909911478810039,  "RMSE": 1.0190815502777968, "MAE": 0.7206885414237795},
                    "Forecast": {"R2": 0.04751773285297578, "RMSE": 0.9228862632670221, "MAE": 0.7170317654291213},
                },
                "humidity": {
                    "Test":     {"R2": 0.970366342992716,  "RMSE": 1.35018185199528,    "MAE": 0.992178740554755},
                    "Forecast": {"R2": -2.87610798811296,  "RMSE": 14.3012844021729059, "MAE": 13.0464059375285},
                },
                "pressure": {
                    "Test":     {"R2": 0.875296979547872, "RMSE": 130.307798024719,  "MAE": 82.6360167646107},
                    "Forecast": {"R2": -1.2120292126594,  "RMSE": 213.515594263116,  "MAE": 172.728640996836},
                },
            },
        },
        "Chennai": {
            "QLSTM": {
                "temperature": {
                    "Test":     {"R2": 0.654077697, "RMSE": 0.746454561, "MAE": 0.5750464},
                    "Forecast": {"R2": 0.029162007, "RMSE": 0.821739843, "MAE": 0.653513621},
                },
                "humidity": {
                    "Test":     {"R2": 0.450391819911212, "RMSE": 5.94207908832873, "MAE": 4.64850004016304},
                    "Forecast": {"R2": 0.122903356538394, "RMSE": 3.68065824148305,  "MAE": 3.04957059724983},
                },
                "pressure": {
                    "Test":     {"R2": 0.78788696134205, "RMSE": 1.21498875528986, "MAE": 0.971566006041523},
                    "Forecast": {"R2": 0.628139503686716, "RMSE": 1.343039135983,   "MAE": 1.08074757598712},
                },
            },
            "QGRU": {
                "temperature": {
                    "Test":     {"R2": 0.717820229, "RMSE": 0.674181812, "MAE": 0.529043347},
                    "Forecast": {"R2": 0.019505041, "RMSE": 0.817875429, "MAE": 0.668867173},
                },
                "humidity": {
                    "Test":     {"R2": 0.425013170512196,  "RMSE": 6.07772131733813, "MAE": 4.85732550536834},
                    "Forecast": {"R2": 0.0852698293466002, "RMSE": 3.75879180486243, "MAE": 3.13254435587196},
                },
                "pressure": {
                    "Test":     {"R2": 0.732604760500939, "RMSE": 1.36416031532589, "MAE": 1.08180892506637},
                    "Forecast": {"R2": 0.585327060941346, "RMSE": 1.41824575805825,  "MAE": 1.133827400593},
                },
            },
            "HQNN": {
                "temperature": {
                    "Test":     {"R2": 0.754667699, "RMSE": 0.73379615534547,   "MAE": 0.591773331165314},
                    "Forecast": {"R2": 0.172,       "RMSE": 0.907230964378954,  "MAE": 0.736464381217957},
                },
                "humidity": {
                    "Test":     {"R2": 0.364358365535736,  "RMSE": 4.45061156967402,  "MAE": 3.41676592826843},
                    "Forecast": {"R2": 0.0154274106025696, "RMSE": 5.60570659066413,  "MAE": 4.3406720161438},
                },
                "pressure": {
                    "Test":     {"R2": 0.709940195083618, "RMSE": 140.135502226863, "MAE": 105.413192749023},
                    "Forecast": {"R2": 0.102115750312805, "RMSE": 231.478037902627,  "MAE": 170.115173339844},
                },
            },
            "VQC":  _empty_metrics(),
            "QSVR": _empty_metrics(),
        },
    },
}


CLASSICAL_METRICS_DATA = {
    "Univariate": {
        "Delhi": {
            "LSTM": _empty_metrics(),
            "GRU":  _empty_metrics(),
            "ANN": {
                "temperature": {
                    "Test":     {"R2": 0.970330897, "RMSE": 1.110678076, "MAE": 0.869020674},
                    "Forecast": {"R2": 0.924507,    "RMSE": 1.1751,      "MAE": 0.882678},
                },
                "humidity": {
                    "Test":     {"R2": 0.380749667, "RMSE": 4.886194746, "MAE": 3.631397035},
                    "Forecast": {"R2": 0.350586,    "RMSE": 4.956,       "MAE": 4.272612},
                },
                "pressure": {
                    "Test":     {"R2": 0.941959824, "RMSE": 140.6081706, "MAE": 109.5723741},
                    "Forecast": {"R2": 0.914587,    "RMSE": 141.68976,   "MAE": 110.15752},
                },
            },
            "SVR": _empty_metrics(),
        },
        "Mumbai": {
            "LSTM": _empty_metrics(),
            "GRU":  _empty_metrics(),
            "ANN": {
                "temperature": {
                    "Test":     {"R2": 0.885541916, "RMSE": 0.792593769, "MAE": 0.592681468},
                    "Forecast": {"R2": 0.839781,    "RMSE": 0.80642,     "MAE": 0.625858},
                },
                "humidity": {
                    "Test":     {"R2": 0.57825923, "RMSE": 5.68157147, "MAE": 4.09688282},
                    "Forecast": {"R2": 0.538245,   "RMSE": 5.89715,    "MAE": 4.597851},
                },
                "pressure": {
                    "Test":     {"R2": 0.868029833, "RMSE": 104.3580825, "MAE": 82.66482544},
                    "Forecast": {"R2": 0.826285,    "RMSE": 105.97131,   "MAE": 84.6478},
                },
            },
            "SVR": _empty_metrics(),
        },
        "Chennai": {
            "LSTM": _empty_metrics(),
            "GRU":  _empty_metrics(),
            "ANN": {
                "temperature": {
                    "Test":     {"R2": 0.76723671, "RMSE": 0.583433114, "MAE": 0.468226969},
                    "Forecast": {"R2": 0.71297852, "RMSE": 0.608641,    "MAE": 0.370454},
                },
                "humidity": {
                    "Test":     {"R2": 0.432723582, "RMSE": 4.204466425, "MAE": 3.230050564},
                    "Forecast": {"R2": 0.36745,     "RMSE": 4.35559,     "MAE": 4.260464},
                },
                "pressure": {
                    "Test":     {"R2": 0.834226251, "RMSE": 105.9405604, "MAE": 85.77310944},
                    "Forecast": {"R2": 0.7851,      "RMSE": 105.83,      "MAE": 82.10944},
                },
            },
            "SVR": _empty_metrics(),
        },
    },
    "Multivariate": {
        "Delhi": {
            "LSTM": {
                "temperature": {
                    "Test":     {"R2": 0.926130888179388, "RMSE": 1.28695373851763, "MAE": 1.03277675458038},
                    "Forecast": {"R2": 0.494621166854808, "RMSE": 1.46924846595107, "MAE": 1.09773826479746},
                },
                "humidity": {
                    "Test":     {"R2": 0.814084367180715, "RMSE": 6.6122215045229,  "MAE": 1.53510846933806},
                    "Forecast": {"R2": 0.360338904720182, "RMSE": 1.76248496130932, "MAE": 1.54444543576544},
                },
                "pressure": {
                    "Test":     {"R2": 0.90309658787483,  "RMSE": 2.03467831471495, "MAE": 1.32902405826177},
                    "Forecast": {"R2": 0.375433468282663, "RMSE": 1.18461946047868, "MAE": 1.00504702193904},
                },
            },
            "GRU": {
                "temperature": {
                    "Test":     {"R2": 0.928128723636489, "RMSE": 1.26943122284931, "MAE": 1.01159153584641},
                    "Forecast": {"R2": 0.177957288218787, "RMSE": 1.8738460750296,  "MAE": 1.6038058912121},
                },
                "humidity": {
                    "Test":     {"R2": 0.803213683836405, "RMSE": 6.8027872174809,  "MAE": 5.2039320295379},
                    "Forecast": {"R2": 0.332517239413928, "RMSE": 7.52500833152155, "MAE": 6.30789301968475},
                },
                "pressure": {
                    "Test":     {"R2": 0.938195796447977, "RMSE": 1.62493214002391, "MAE": 1.25201406874928},
                    "Forecast": {"R2": 0.286456094172257, "RMSE": 1.88385042090766, "MAE": 1.6672479876487},
                },
            },
            "ANN": {
                "temperature": {
                    "Test":     {"R2": 0.9,  "RMSE": 1.24, "MAE": 1.09},
                    "Forecast": {"R2": 0.56, "RMSE": 2.64, "MAE": 1.57},
                },
                "humidity": {
                    "Test":     {"R2": 0.75, "RMSE": 4.57, "MAE": 3.74},
                    "Forecast": {"R2": 0.22, "RMSE": 4.75, "MAE": 4.54},
                },
                "pressure": {
                    "Test":     {"R2": 0.85, "RMSE": 1.34, "MAE": 1.12},
                    "Forecast": {"R2": 0.34, "RMSE": 2.14, "MAE": 1.37},
                },
            },
            "SVR": _empty_metrics(),
        },
        "Mumbai": {
            "LSTM": {
                "temperature": {
                    "Test":     {"R2": 0.846891960638665, "RMSE": 0.705079624936049, "MAE": 0.565702983011927},
                    "Forecast": {"R2": 0.4336048210207,   "RMSE": 1.4418516311934,   "MAE": 1.15122765094772},
                },
                "humidity": {
                    "Test":     {"R2": 0.664271246794179, "RMSE": 4.00875176372399, "MAE": 3.05278294957195},
                    "Forecast": {"R2": 0.243572028187884, "RMSE": 7.83820428610583,  "MAE": 6.55327168896067},
                },
                "pressure": {
                    "Test":     {"R2": 0.844454262197024, "RMSE": 1.413579440353,   "MAE": 1.10555803314831},
                    "Forecast": {"R2": 0.520180379847721, "RMSE": 1.23467124919228, "MAE": 0.87521800872853},
                },
            },
            "GRU": {
                "temperature": {
                    "Test":     {"R2": 0.857129948390968, "RMSE": 0.681098255710643, "MAE": 0.549284165804457},
                    "Forecast": {"R2": 0.577527296198622, "RMSE": 7.54880952968176,  "MAE": 0.977967006328551},
                },
                "humidity": {
                    "Test":     {"R2": 0.671482764839892, "RMSE": 3.9654636640602,  "MAE": 3.06786440192631},
                    "Forecast": {"R2": 0.298397127269661, "RMSE": 3.85532605933407, "MAE": 6.33741447473109},
                },
                "pressure": {
                    "Test":     {"R2": 0.850567940212601, "RMSE": 1.38552081219839, "MAE": 1.08393245134132},
                    "Forecast": {"R2": 0.522428996937429, "RMSE": 1.23177478237324, "MAE": 0.916087511195713},
                },
            },
            "ANN": {
                "temperature": {
                    "Test":     {"R2": 0.863676309585571, "RMSE": 0.864993920938817, "MAE": 0.659784734249115},
                    "Forecast": {"R2": 0.610359072685242, "RMSE": 1.45695139484588,  "MAE": 0.99756121635437},
                },
                "humidity": {
                    "Test":     {"R2": 0.639242053031921, "RMSE": 5.25476893039464,  "MAE": 3.93062162399292},
                    "Forecast": {"R2": 0.238626480102539, "RMSE": 7.71086032446182,  "MAE": 5.33274984359741},
                },
                "pressure": {
                    "Test":     {"R2": 0.805795073509216, "RMSE": 126.595531954874,  "MAE": 100.472442626953},
                    "Forecast": {"R2": 0.571001768112183, "RMSE": 181.205134533351,  "MAE": 139.075057983398},
                },
            },
            "SVR": {
                "temperature": {
                    "Test":     {"R2": 0.8757957525048894, "RMSE": 0.7855879676189725, "MAE": 0.5673661576960026},
                    "Forecast": {"R2": 0.1891056069261169, "RMSE": 0.85153378023199,   "MAE": 0.625921790624248},
                },
                "humidity": {
                    "Test":     {"R2": 0.994360509651454,  "RMSE": 0.589005798454528, "MAE": 0.394619517846137},
                    "Forecast": {"R2": -2.87352645351996,  "RMSE": 14.2965211951444,  "MAE": 13.0384808013447},
                },
                "pressure": {
                    "Test":     {"R2": 0.993400591230005,  "RMSE": 29.9767422998881,  "MAE": 16.0003084539897},
                    "Forecast": {"R2": -2.15326341725722,  "RMSE": 254.92609689436,   "MAE": 211.310294083973},
                },
            },
        },
        "Chennai": {
            "LSTM": {
                "temperature": {
                    "Test":     {"R2": 0.756935345249445,  "RMSE": 0.625712742680285, "MAE": 0.496728080655052},
                    "Forecast": {"R2": 0.115219428986926,  "RMSE": 0.761921556316091, "MAE": 0.609207885223388},
                },
                "humidity": {
                    "Test":     {"R2": 0.384986398078552,   "RMSE": 6.28570788773562, "MAE": 4.97137802212158},
                    "Forecast": {"R2": 0.0508849723572936,  "RMSE": 3.82878689108329, "MAE": 3.17321373708995},
                },
                "pressure": {
                    "Test":     {"R2": 0.814263761495191, "RMSE": 1.13693830527169, "MAE": 0.895516091948336},
                    "Forecast": {"R2": 0.682767852737497, "RMSE": 1.24047278679609, "MAE": 0.978103756603279},
                },
            },
            "GRU": {
                "temperature": {
                    "Test":     {"R2": 0.742905341917973, "RMSE": 0.643517883777774, "MAE": 0.513421054685077},
                    "Forecast": {"R2": 0.106872683027092, "RMSE": 0.765506986233859, "MAE": 0.604208727951049},
                },
                "humidity": {
                    "Test":     {"R2": 0.400324359060371,  "RMSE": 6.20683267779805, "MAE": 4.88626930546319},
                    "Forecast": {"R2": 0.0689886079289274, "RMSE": 3.79209550843903, "MAE": 3.2535447717135},
                },
                "pressure": {
                    "Test":     {"R2": 0.783586627959274, "RMSE": 1.22724316436924, "MAE": 1.00812476801803},
                    "Forecast": {"R2": 0.657338897211183, "RMSE": 1.28923192094695, "MAE": 1.04259066341949},
                },
            },
            "ANN": {
                "temperature": {
                    "Test":     {"R2": 0.557915151119232, "RMSE": 0.804056605448282, "MAE": 0.633854746818543},
                    "Forecast": {"R2": 0.298314273357391, "RMSE": 1.01283767861928,  "MAE": 0.80923855304718},
                },
                "humidity": {
                    "Test":     {"R2": 0.460398972034454, "RMSE": 4.10062372999225, "MAE": 3.13587617874146},
                    "Forecast": {"R2": 0.100976705551147, "RMSE": 5.356633945089,   "MAE": 3.97631478309631},
                },
                "pressure": {
                    "Test":     {"R2": 0.783388257026672, "RMSE": 121.10034256248,  "MAE": 95.7708358764648},
                    "Forecast": {"R2": 0.183898329734802, "RMSE": 220.684464365981, "MAE": 161.129959106445},
                },
            },
            "SVR": _empty_metrics(),
        },
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# ██  METRICS RENDERER (QML) — Forecast only, no Test rows
# ══════════════════════════════════════════════════════════════════════════════

def _render_metrics_matrix(model_type: str):
    import streamlit.components.v1 as components

    city    = st.session_state.get("meteogram_city",         CITIES[0])
    q_model = st.session_state.get("meteogram_model_select", "QLSTM")

    st.markdown("---")
    data = METRICS_DATA.get(model_type, {}).get(city, {}).get(q_model, {})

    col_title_q, col_btn_q = st.columns([9, 1])
    with col_title_q:
        st.markdown(f"### ⚛️ Quantum Algorithm Forecast Metrics — {city}")
    with col_btn_q:
        csv_q = _metrics_to_csv(data)
        st.download_button(
            label="⬇️",
            data=csv_q,
            file_name=f"quantum_metrics_{city}_{model_type}_{q_model}.csv",
            mime="text/csv",
            key=f"dl_q_{city}_{model_type}_{q_model}",
        )

    def _cell(val, metric_key):
        if val is None:
            return "&mdash;", "#f8fafc", "#94a3b8", "400"
        return f"{val:.4f}", "#ffffff", "#1e293b", "400"

    param_list   = ["temperature", "humidity", "pressure"]
    param_labels = {
        "temperature": "&#127777; Temperature",
        "humidity":    "&#128167; Humidity",
        "pressure":    "&#128309; Pressure",
    }
    metric_rows = [
        ("R&sup2; Score", "R2"),
        ("RMSE",          "RMSE"),
        ("MAE",           "MAE"),
    ]

    hdr_style = ("background:linear-gradient(135deg,#1d4ed8,#3b82f6);"
                 "color:#fff;font-weight:700;font-size:13px;"
                 "padding:12px 10px;text-align:center;"
                 "border:1px solid #1d4ed8;letter-spacing:0.3px;")

    # Only Forecast column — no sub-header needed
    param_ths = "".join(
        f'<th style="{hdr_style}">{param_labels[p]}</th>'
        for p in param_list
    )

    tbody = ""
    for idx, (metric_label, metric_key) in enumerate(metric_rows):
        row_bg = "#ffffff" if idx % 2 == 0 else "#fafafa"
        tds = (
            f'<td style="padding:13px 20px;font-weight:700;font-size:13px;'
            f'color:#1e293b;border-bottom:1px solid #e2e8f0;'
            f'border-right:1px solid #d1d5db;background:#ffffff;">'
            f'{metric_label}</td>'
        )
        for param in param_list:
            val = data.get(param, {}).get("Forecast", {}).get(metric_key, None)
            txt, bg, fg, fw = _cell(val, metric_key)
            tds += (
                f'<td style="padding:13px 14px;font-size:13px;'
                f'text-align:center;background:{bg};color:{fg};'
                f'font-weight:{fw};border-bottom:1px solid #e2e8f0;'
                f'border-right:1px solid #f1f5f9;">{txt}</td>'
            )
        tbody += f'<tr style="background:{row_bg};">{tds}</tr>'

    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{font-family:Arial,sans-serif;background:transparent;}}
  .wrap{{overflow-x:auto;border-radius:12px;border:1px solid #bfdbfe;
         box-shadow:0 4px 16px rgba(37,99,235,0.10);}}
  table{{width:100%;border-collapse:collapse;}}
</style>
</head><body>
<div class="wrap">
  <table>
    <thead>
      <tr>
        <th style="background:linear-gradient(135deg,#1d4ed8,#3b82f6);
            color:#fff;font-weight:700;font-size:13px;padding:12px 20px;
            text-align:left;border:1px solid #1d4ed8;min-width:160px;">Metric</th>
        {param_ths}
      </tr>
    </thead>
    <tbody>{tbody}</tbody>
  </table>
</body></html>"""

    components.html(full_html, height=200, scrolling=False)

    # ── Classical Metrics Table — Forecast only ────────────────────────────
    c_model = st.session_state.get("meteogram_classical_select", "LSTM")
    c_data  = CLASSICAL_METRICS_DATA.get(model_type, {}).get(city, {}).get(c_model, {})

    col_title_c, col_btn_c = st.columns([9, 1])
    with col_title_c:
        st.markdown(f"### 🖥️ Classical Algorithm Forecast Metrics — {city}")
    with col_btn_c:
        csv_c = _metrics_to_csv(c_data)
        st.download_button(
            label="⬇️",
            data=csv_c,
            file_name=f"classical_metrics_{city}_{model_type}_{c_model}.csv",
            mime="text/csv",
            key=f"dl_c_{city}_{model_type}_{c_model}",
        )

    c_param_ths = "".join(
        f'<th style="{hdr_style}">{param_labels[p]}</th>'
        for p in param_list
    )

    c_tbody = ""
    for idx, (metric_label, metric_key) in enumerate(metric_rows):
        row_bg = "#ffffff" if idx % 2 == 0 else "#fafafa"
        tds = (
            f'<td style="padding:13px 20px;font-weight:700;font-size:13px;'
            f'color:#1e293b;border-bottom:1px solid #e2e8f0;'
            f'border-right:1px solid #d1d5db;background:#ffffff;">'
            f'{metric_label}</td>'
        )
        for param in param_list:
            val = c_data.get(param, {}).get("Forecast", {}).get(metric_key, None)
            txt, bg, fg, fw = _cell(val, metric_key)
            tds += (
                f'<td style="padding:13px 14px;font-size:13px;'
                f'text-align:center;background:{bg};color:{fg};'
                f'font-weight:{fw};border-bottom:1px solid #e2e8f0;'
                f'border-right:1px solid #f1f5f9;">{txt}</td>'
            )
        c_tbody += f'<tr style="background:{row_bg};">{tds}</tr>'

    c_full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{font-family:Arial,sans-serif;background:transparent;}}
  .wrap{{overflow-x:auto;border-radius:12px;border:1px solid #bfdbfe;
         box-shadow:0 4px 16px rgba(37,99,235,0.10);}}
  table{{width:100%;border-collapse:collapse;}}
</style>
</head><body>
<div class="wrap">
  <table>
    <thead>
      <tr>
        <th style="background:linear-gradient(135deg,#1d4ed8,#3b82f6);
            color:#fff;font-weight:700;font-size:13px;padding:12px 20px;
            text-align:left;border:1px solid #1d4ed8;min-width:160px;">Metric</th>
        {c_param_ths}
      </tr>
    </thead>
    <tbody>{c_tbody}</tbody>
  </table>
</body></html>"""

    components.html(c_full_html, height=200, scrolling=False)


# ── Map (shared) ───────────────────────────────────────────────────────────────

def _render_map(city: str, source: str = "qml"):
    st.markdown("---")
    st.markdown("### 🗺️ Location Map")
    try:
        import streamlit.components.v1 as components
        from visualization.maps import create_zoom_map
        from config.constants import CITIES as _CITIES_RAW

        cities_dict = (
            _CITIES_RAW if isinstance(_CITIES_RAW, dict)
            else {c: {"region": c, "lat": 0.0, "lon": 0.0} for c in _CITIES_RAW}
        )
        if city in cities_dict:
            info      = cities_dict[city]
            lat, lon  = info.get("lat", 0), info.get("lon", 0)
            region    = info.get("region", city)
            coord_str = f"{lat:.4f}°N, {lon:.4f}°E" if (lat and lon) else "—"

            st.markdown(f"""
            <div style="display:flex; gap:28px; align-items:center;
                        background:#f0f4ff; border-left:5px solid #2563eb;
                        border-radius:8px; padding:12px 18px; margin-bottom:10px;
                        font-size:15px; color:#1e293b;">
                <span>📍 <strong>Location:</strong> {city}</span>
                <span>🌏 <strong>Region:</strong> {region}</span>
                <span>🔵 <strong>Coordinates:</strong> {coord_str}</span>
            </div>""", unsafe_allow_html=True)

            last_values = (
                _get_last_ospm_param_values(city)
                if source == "ospm"
                else _get_last_param_values(city)
            )
            raw_html = create_zoom_map(
                selected_city=city, cities_data=cities_dict,
                selected_subzone=None, classical_data=None,
                quantum_data=None, custom_datetime=None,
                last_values=last_values,
            )

            full_html = raw_html.replace(
                "</head>",
                "<style>html,body{margin:0;padding:0;width:100%!important;"
                "height:100%!important;}#map,.folium-map{width:100%!important;"
                "height:100%!important;}</style></head>", 1,
            )
            components.html(full_html, height=520, scrolling=False)
        else:
            st.warning("City not found in map configuration.")
    except Exception as e:
        st.warning(f"Map could not be loaded: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# ██  OSPM TAB  — Open Source Pre-trained Model
# ══════════════════════════════════════════════════════════════════════════════

def _render_ospm_tab():
    col_main, col_cfg = st.columns([3, 1])
    with col_cfg:
        _render_ospm_sidebar()
    with col_main:
        _render_ospm_content()


# ── OSPM Sidebar ───────────────────────────────────────────────────────────────

def _render_ospm_sidebar():
    """Professional sidebar for OSPM tab with Generate button."""
    from ui.meteogram_loader import get_loaded_ospm_params

    # ── Clean, professional card CSS (same style as QML sidebar) ────────────
    st.markdown(
        """
        <style>
        /* Sidebar column card */
        section.main div[data-testid="column"]:has(.ospm-side-marker) {
            background: #ffffff;
            border-radius: 20px;
            padding: 20px 18px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.02);
            border: 1px solid #eef2f6;
            transition: box-shadow 0.2s ease;
        }
        section.main div[data-testid="column"]:has(.ospm-side-marker):hover {
            box-shadow: 0 12px 28px rgba(0,0,0,0.08);
        }
        /* Text colours inside the card */
        section.main div[data-testid="column"]:has(.ospm-side-marker) label,
        section.main div[data-testid="column"]:has(.ospm-side-marker) p,
        section.main div[data-testid="column"]:has(.ospm-side-marker)
            div[data-baseweb="select"] span {
            color: #1e293b !important;
        }
        /* Headers and sections */
        .ospm-side-header {
            font-size: 20px;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: -0.3px;
            margin-bottom: 4px;
        }
        .ospm-side-subtitle {
            font-size: 13px;
            color: #475569;
            margin-bottom: 20px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 12px;
        }
        .ospm-side-section {
            font-size: 13px;
            font-weight: 600;
            color: #334155;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 20px 0 12px 0;
        }
        .ospm-side-divider {
            border: none;
            border-top: 1px solid #eef2f6;
            margin: 16px 0 8px 0;
        }
        .ospm-info-block {
            background: #f8fafc;
            border-radius: 14px;
            padding: 12px 16px;
            font-size: 12px;
            margin-top: 12px;
        }
        .ospm-info-block .label {
            color: #475569;
            font-weight: 500;
        }
        .ospm-info-block .value {
            color: #0f172a;
            font-weight: 600;
            float: right;
        }
        /* Generate button - elegant gradient (green theme for OSPM) */
        div[data-testid="column"]:has(.ospm-side-marker) div.stButton > button {
            width: 100%;
            background: linear-gradient(105deg, #059669 0%, #10b981 100%);
            color: white;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 0.3px;
            border: none;
            border-radius: 40px;
            padding: 10px 0;
            margin-top: 20px;
            margin-bottom: 8px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(5,150,105,0.25);
            transition: all 0.2s ease;
        }
        div[data-testid="column"]:has(.ospm-side-marker) div.stButton > button:hover {
            background: linear-gradient(105deg, #047857 0%, #059669 100%);
            box-shadow: 0 6px 16px rgba(5,150,105,0.35);
            transform: translateY(-1px);
        }
        /* Streamlit widget tweaks */
        div[data-testid="column"]:has(.ospm-side-marker) .stSelectbox label {
            font-weight: 500;
        }
        div[data-testid="column"]:has(.ospm-side-marker) hr {
            margin: 8px 0;
        }
        </style>
        <div class="ospm-side-marker"></div>
        <div class="ospm-side-header">Meteogram</div>
        <div class="ospm-side-subtitle">Meteogram Charts · City Wise · OSPM</div>
        <div class="ospm-side-section">Filters</div>
        """,
        unsafe_allow_html=True,
    )

    # ── Location dropdown ───────────────────────────────────────────────────
    st.selectbox("Location", CITIES, key="ospm_city",
                 label_visibility="visible")

    city       = st.session_state.get("ospm_city", CITIES[0])
    model_type = "Univariate"  # OSPM only supports Univariate

    # ── OSPM Model dropdown with data availability indicator ────────────────
    def _ospm_label(key):
        try:
            loaded = get_loaded_ospm_params(city, key, model_type)
        except Exception:
            loaded = []
        return OSPM_MODELS[key] if loaded else f"{OSPM_MODELS[key]}  ·  (No Data)"

    st.selectbox(
        "OSPM Model",
        list(OSPM_MODELS.keys()),
        format_func=_ospm_label,
        key="ospm_model_select",
        label_visibility="visible",
    )

    # ── Generate Forecast Button ────────────────────────────────────────────
    if st.button("⚡ Generate Forecast", key="ospm_generate_btn"):
        st.session_state["ospm_generated"]      = True
        st.session_state["ospm_gen_city"]       = st.session_state.get("ospm_city", CITIES[0])
        st.session_state["ospm_gen_model"]      = st.session_state.get("ospm_model_select", list(OSPM_MODELS.keys())[0])

    current_m = st.session_state.get("ospm_model_select", list(OSPM_MODELS.keys())[0])

    # ── Information Block (clean, card-like) ────────────────────────────────
    info_html = (
        '<hr class="ospm-side-divider"/>'
        '<div class="ospm-side-section">INFORMATION</div>'
        '<div class="ospm-info-block">'
        '<div><span class="label">Model:</span>'
        f'<span class="value">{OSPM_MODELS.get(current_m, current_m)}</span></div>'
        '<div style="clear:both;"></div>'
        '<div><span class="label">City:</span>'
        f'<span class="value">{city}</span></div>'
        '<div style="clear:both;"></div>'
        '<div><span class="label">Source:</span>'
        '<span class="value">NCMRWF</span></div>'
        '<div style="clear:both;"></div>'
        '</div>'
    )
    st.markdown(info_html, unsafe_allow_html=True)

def _render_ospm_content():
    from ui.meteogram_loader import (
        get_ospm_param_df, get_loaded_ospm_params,
    )

    st.markdown(
        f"""
        <div style="background:#ffffff; border:1.5px solid {NCMRWF['title_color']};
                    border-radius:8px; padding:14px 20px; margin-bottom:12px;">
            <div style="font-family:{NCMRWF['font_family']}; font-size:20px;
                        font-weight:800; color:{NCMRWF['title_color']};
                        letter-spacing:1px; font-style:italic;">
                METEOGRAM · OSPM
            </div>
            <div style="font-family:{NCMRWF['font_family']}; font-size:12px;
                        color:#555; margin-top:2px;">
                Meteogram Charts — City Wise &nbsp;·&nbsp; Open Source Pre‑trained Models
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Guard: show placeholder until Generate is clicked
    if not st.session_state.get("ospm_generated", False):
        st.markdown(
            f"""
            <div style="
                display:flex; flex-direction:column; align-items:center;
                justify-content:center; gap:16px;
                background:#fafafa; border:2px dashed #6ee7b7;
                border-radius:14px; padding:60px 40px; margin-top:20px;
                text-align:center;
            ">
                <div style="font-size:48px;">🤖</div>
                <div style="font-size:20px; font-weight:800;
                            color:#059669; letter-spacing:0.4px;">
                    Ready to Generate OSPM Forecast
                </div>
                <div style="font-size:13px; color:#6b7280; max-width:400px; line-height:1.7;">
                    Select a <b>Location</b> and an <b>OSPM Model</b>
                    in the panel on the right, then click
                    <b style="color:#059669;">⚡ Generate Forecast</b>
                    to render the meteogram charts.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Read snapshot saved when Generate was clicked
    city       = st.session_state.get("ospm_gen_city",   CITIES[0])
    model      = st.session_state.get("ospm_gen_model",  list(OSPM_MODELS.keys())[0])
    model_type = "Univariate"        # OSPM only evaluated on univariate

    # Build dataframes for OSPM
    loaded_params = get_loaded_ospm_params(city, model, model_type)

    def _ospm_actual_df():
        base = None
        for param in loaded_params:
            df = get_ospm_param_df(city, model, model_type, param)
            if df is None or "datetime" not in df.columns:
                continue
            keep = ["datetime", f"{param}_actual", "_is_forecast"]
            keep = [c for c in keep if c in df.columns]
            sub = df[keep].drop_duplicates(subset=["datetime"])
            base = sub if base is None else base.merge(sub, on="datetime", how="outer")
        if base is None:
            return None
        return base.sort_values("datetime").reset_index(drop=True)

    def _ospm_model_df():
        base = None
        for param in loaded_params:
            df = get_ospm_param_df(city, model, model_type, param)
            if df is None or "datetime" not in df.columns or param not in df.columns:
                continue
            cols = ["datetime", param]
            if "_is_forecast" in df.columns:
                cols.append("_is_forecast")
            sub = df[cols].drop_duplicates(subset=["datetime"])
            base = sub if base is None else base.merge(sub, on="datetime", how="outer")
        if base is None:
            return None
        return base.sort_values("datetime").reset_index(drop=True)

    actual_df   = _ospm_actual_df()
    ospm_df     = _ospm_model_df()
    classical_df = None

    # Forecast-only + last 10 days + common-start alignment
    actual_df, ospm_df, _ = _forecast_window(actual_df, ospm_df, None, n=_FORECAST_DAYS)

    # Colour key
    import streamlit.components.v1 as components
    ff = NCMRWF["font_family"]
    key_html = f"""
    <!DOCTYPE html><html><head><meta charset='utf-8'>
    <style>
    *{{box-sizing:border-box;margin:0;padding:0;}}
    body{{font-family:{ff};background:transparent;color:#111;}}
    .keywrap{{display:flex;gap:14px;flex-wrap:wrap;align-items:center;
              background:#fafafa;border:1px solid #e2e8f0;border-radius:8px;
              padding:8px 14px;font-size:12px;}}
    .keysw{{display:inline-block;width:18px;height:3px;vertical-align:middle;margin-right:6px;}}
    .keynote{{margin-left:auto;color:#666;}}
    </style></head><body>
    <div class="keywrap">
        <div><span class="keysw" style='background:{NCMRWF["actual"]}'></span><b>Actual</b></div>
        <div><span class="keysw" style='background:{NCMRWF["quantum"]}'></span><b>OSPM · {OSPM_MODELS[model]}</b></div>
        <div class="keynote">Forecast-only · Last {_FORECAST_DAYS} days</div>
    </div></body></html>
    """
    components.html(key_html, height=50, scrolling=False)

    # Header card
    st.markdown(f"""
    <div style="background:#fff; border-left:4px solid #059669; border-radius:8px;
                padding:14px 18px; margin:8px 0 16px 0;">
        <div style="display:flex; gap:20px; align-items:baseline; flex-wrap:wrap;">
            <div style="font-size:22px; font-weight:800;">📍 {city.upper()}</div>
            <div style="font-size:12px; color:#444;">
                {actual_df["datetime"].min().strftime('%d %b') if actual_df is not None else "—"} –
                {actual_df["datetime"].max().strftime('%d %b %Y') if actual_df is not None else "—"}
            </div>
            <div style="font-size:12px; color:#444;">
                🟢 OSPM · {OSPM_MODELS[model]}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Render three panels
    header_label = _ncmrwf_header(city, model_label=f"{OSPM_MODELS[model]} ")

    for param in ["pressure", "temperature", "humidity"]:
        if param not in loaded_params:
            st.info(f"No OSPM forecast data for {PARAMS[param]['label']}. Missing file.")
            continue

        _ncmrwf_panel_open()
        fig = _build_ncmrwf_single_figure(
            param=param,
            header_label=header_label,
            df_actual=actual_df,
            df_quantum=ospm_df,
            df_classical=None,
            actual_color=NCMRWF["actual"],
        )
        st.plotly_chart(fig, use_container_width=True,
                        config={"displayModeBar": True, "displaylogo": False})
        _ncmrwf_panel_close()

    # Metrics table and map
    _render_ospm_metrics_matrix(model_type, city, model)
    _render_map(city, source="ospm")

# ── OSPM Metrics renderer ──────────────────────────────────────────────────────

OSPM_METRICS_DATA = {
    "Univariate": {
        "Delhi": {
            "TIMESFM": {
                "temperature": {
                    "Test":     {"R2": 0.9401, "RMSE": 1.0426, "MAE": 0.8084},
                    "Forecast": {"R2": 0.6406, "RMSE": 1.3133, "MAE": 0.9507},
                },
                "humidity": {
                    "Test":     {"R2": 0.0743, "RMSE": 4.2637, "MAE": 3.188},
                    "Forecast": {"R2": 0.0976, "RMSE": 7.9971, "MAE": 6.1698},
                },
                "pressure": {
                    "Test":     {"R2": 0.8906, "RMSE": 157.9909, "MAE": 122.8394},
                    "Forecast": {"R2": 0.3333, "RMSE": 141.9525, "MAE": 115.5204},
                },
            },
            "CHRONOS": {
                "temperature": {
                    "Test":     {"R2": 0.9464, "RMSE": 0.9711, "MAE": 0.7798},
                    "Forecast": {"R2": 0.6664, "RMSE": 1.2652, "MAE": 1.0098},
                },
                "humidity": {
                    "Test":     {"R2": -0.0301, "RMSE": 4.7341, "MAE": 3.5753},
                    "Forecast": {"R2": 0.1506, "RMSE": 7.759, "MAE": 6.38},
                },
                "pressure": {
                    "Test":     {"R2": 0.9021, "RMSE": 149.5216, "MAE": 118.0166},
                    "Forecast": {"R2": 0.4374, "RMSE": 130.3989, "MAE": 108.6695},
                },
            },
            "TSTRANSFORMER": {
                "temperature": {
                    "Test":     {"R2": None, "RMSE": None, "MAE": None},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
                "humidity": {
                    "Test":     {"R2": None, "RMSE": None, "MAE": None},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
                "pressure": {
                    "Test":     {"R2": None, "RMSE": None, "MAE": None},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
            },
        },
        "Mumbai": {
            "TIMESFM": {
                "temperature": {
                    "Test":     {"R2": 0.795,  "RMSE": 0.6662,  "MAE": 0.536},
                    "Forecast": {"R2": 0.6864, "RMSE": 1.222,   "MAE": 1.0078},
                },
                "humidity": {
                    "Test":     {"R2": 0.6595, "RMSE": 4.0929,  "MAE": 3.1476},
                    "Forecast": {"R2": 0.3026, "RMSE": 7.6471,  "MAE": 6.2735},
                },
                "pressure": {
                    "Test":     {"R2": 0.7603, "RMSE": 123.8367, "MAE": 92.9444},
                    "Forecast": {"R2": 0.4676, "RMSE": 107.0163, "MAE": 82.1776},
                },
            },
            "CHRONOS": {
                "temperature": {
                    "Test":     {"R2": None, "RMSE": None, "MAE": None},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
                "humidity": {
                    "Test":     {"R2": None, "RMSE": None, "MAE": None},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
                "pressure": {
                    "Test":     {"R2": None, "RMSE": None, "MAE": None},
                    "Forecast": {"R2": None, "RMSE": None, "MAE": None},
                },
            },
            "TSTRANSFORMER": {
                "temperature": {
                    "Test":     {"R2": 0.7591, "RMSE": 0.6577, "MAE": 0.5352},
                    "Forecast": {"R2": 0.3812, "RMSE": 1.2841, "MAE": 1.0956},
                },
                "humidity": {
                    "Test":     {"R2": 0.7076, "RMSE": 3.7817,  "MAE": 2.9517},
                    "Forecast": {"R2": 0.1726, "RMSE": 8.3296,  "MAE": 6.7736},
                },
                "pressure": {
                    "Test":     {"R2": 0.8093, "RMSE": 147.4478, "MAE": 111.4824},
                    "Forecast": {"R2": 0.1636, "RMSE": 97.2589,  "MAE": 81.4392},
                },
            },
        },
        "Chennai": {
            "TIMESFM": {
                "temperature": {
                    "Test":     {"R2": 0.6282, "RMSE": 0.5945, "MAE": 0.4663},
                    "Forecast": {"R2": 0.2227, "RMSE": 0.7442, "MAE": 0.6338},
                },
                "humidity": {
                    "Test":     {"R2": 0.5362, "RMSE": 5.1225, "MAE": 3.7537},
                    "Forecast": {"R2": 0.4567, "RMSE": 3.1204, "MAE": 2.3819},
                },
                "pressure": {
                    "Test":     {"R2": 0.7277, "RMSE": 118.1379, "MAE": 98.9478},
                    "Forecast": {"R2": 0.6522, "RMSE": 166.1949, "MAE": 131.4514},
                },
            },
            "CHRONOS": {
                "temperature": {
                    "Test":     {"R2": 0.7291, "RMSE": 0.4832, "MAE": 0.4019},
                    "Forecast": {"R2": 0.2498, "RMSE": 0.7311, "MAE": 0.5761},
                },
                "humidity": {
                    "Test":     {"R2": 0.3667, "RMSE": 4.4185, "MAE": 3.312},
                    "Forecast": {"R2": 0.34, "RMSE": 3.4392, "MAE": 2.67},
                },
                "pressure": {
                    "Test":     {"R2": 0.7413, "RMSE": 115.1583, "MAE": 94.2333},
                    "Forecast": {"R2": 0.5522, "RMSE": 188.5861, "MAE": 145.9324},
                },
            },
            "TSTRANSFORMER": {
                "temperature": {
                    "Test":     {"R2": 0.5965, "RMSE": 0.6179, "MAE": 0.487},
                    "Forecast": {"R2": 0.5667, "RMSE": 0.7703, "MAE": 0.5741},
                },
                "humidity": {
                    "Test":     {"R2": 0.5247, "RMSE": 5.1584, "MAE": 4.0265},
                    "Forecast": {"R2": 0.4696, "RMSE": 3.0831, "MAE": 2.4593},
                },
                "pressure": {
                    "Test":     {"R2": 0.7144, "RMSE": 134.333, "MAE": 108.3893},
                    "Forecast": {"R2": 0.4233, "RMSE": 73.2252, "MAE": 55.7378},
                },
            },
        },
    },
    "Multivariate": {
        "Delhi":   {"TIMESFM": _empty_metrics(), "CHRONOS": _empty_metrics(), "TSTRANSFORMER": _empty_metrics()},
        "Mumbai":  {"TIMESFM": _empty_metrics(), "CHRONOS": _empty_metrics(), "TSTRANSFORMER": _empty_metrics()},
        "Chennai": {"TIMESFM": _empty_metrics(), "CHRONOS": _empty_metrics(), "TSTRANSFORMER": _empty_metrics()},
    },
}


def _render_ospm_metrics_matrix(model_type: str, city: str, model: str):
    import streamlit.components.v1 as components

    st.markdown("---")
    st.markdown(f"### 🤖 OSPM Forecast Metrics — {city}")

    data = OSPM_METRICS_DATA.get(model_type, {}).get(city, {}).get(model, {})

    def _cell(val, metric_key):
        if val is None:
            return "&mdash;", "#f8fafc", "#94a3b8", "400"
        return f"{val:.4f}", "#ffffff", "#1e293b", "400"

    param_list   = ["temperature", "humidity", "pressure"]
    param_labels = {
        "temperature": "&#127777; Temperature",
        "humidity":    "&#128167; Humidity",
        "pressure":    "&#128309; Pressure",
    }
    metric_rows = [
        ("R&sup2; Score", "R2"),
        ("RMSE",          "RMSE"),
        ("MAE",           "MAE"),
    ]

    hdr_style = ("background:linear-gradient(135deg,#065f46,#059669);"
                 "color:#fff;font-weight:700;font-size:13px;"
                 "padding:12px 10px;text-align:center;"
                 "border:1px solid #065f46;letter-spacing:0.3px;")

    param_ths = "".join(
        f'<th style="{hdr_style}">{param_labels[p]}</th>'
        for p in param_list
    )

    tbody = ""
    for idx, (metric_label, metric_key) in enumerate(metric_rows):
        row_bg = "#ffffff" if idx % 2 == 0 else "#f0fdf4"
        tds = (
            f'<td style="padding:13px 20px;font-weight:700;font-size:13px;'
            f'color:#1e293b;border-bottom:1px solid #e2e8f0;'
            f'border-right:1px solid #d1d5db;background:#ffffff;">'
            f'{metric_label}</td>'
        )
        for param in param_list:
            val = data.get(param, {}).get("Forecast", {}).get(metric_key, None)
            txt, bg, fg, fw = _cell(val, metric_key)
            tds += (
                f'<td style="padding:13px 14px;font-size:13px;'
                f'text-align:center;background:{bg};color:{fg};'
                f'font-weight:{fw};border-bottom:1px solid #e2e8f0;'
                f'border-right:1px solid #f1f5f9;">{txt}</td>'
            )
        tbody += f'<tr style="background:{row_bg};">{tds}</tr>'

    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{font-family:Arial,sans-serif;background:transparent;}}
  .wrap{{overflow-x:auto;border-radius:12px;border:1px solid #6ee7b7;
         box-shadow:0 4px 16px rgba(5,150,105,0.10);}}
  table{{width:100%;border-collapse:collapse;}}
</style>
</head><body>
<div class="wrap">
  <table>
    <thead>
      <tr>
        <th style="background:linear-gradient(135deg,#065f46,#059669);
            color:#fff;font-weight:700;font-size:13px;padding:12px 20px;
            text-align:left;border:1px solid #065f46;min-width:160px;">Metric</th>
        {param_ths}
      </tr>
    </thead>
    <tbody>{tbody}</tbody>
  </table>
</body></html>"""

    components.html(full_html, height=200, scrolling=False)


# ── Data tables ───────────────────────────────────────────────────────────────
# Best FORECAST R² per city / parameter — (model_name, forecast_R², test_R²)
_FORECAST_BEST = {
    "Delhi": {
        "temperature": {
            "QML":       ("HQNN",          0.800,  0.350),
            "Classical": ("ANN",           0.560,  0.900),
            "OSPM":      ("CHRONOS",       0.666,  0.946),
        },
        "humidity": {
            "QML":       ("QGRU",          0.445,  0.816),
            "Classical": ("LSTM",          0.360,  0.814),
            "OSPM":      ("CHRONOS",       0.151, -0.030),
        },
        "pressure": {
            "QML":       ("HQNN",          0.670,  0.710),
            "Classical": ("LSTM",          0.375,  0.903),
            "OSPM":      ("CHRONOS",       0.437,  0.902),
        },
    },
    "Mumbai": {
        "temperature": {
            "QML":       ("QGRU",          0.613,  0.857),
            "Classical": ("ANN",           0.610,  0.864),
            "OSPM":      ("TIMESFM",       0.686,  0.795),
        },
        "humidity": {
            "QML":       ("QGRU",          0.242,  0.637),
            "Classical": ("GRU",           0.298,  0.671),
            "OSPM":      ("TIMESFM",       0.303,  0.660),
        },
        "pressure": {
            "QML":       ("QGRU",          0.624,  0.889),
            "Classical": ("ANN",           0.571,  0.806),
            "OSPM":      ("TIMESFM",       0.468,  0.760),
        },
    },
    "Chennai": {
        "temperature": {
            "QML":       ("HQNN",          0.172,  0.755),
            "Classical": ("ANN",           0.298,  0.558),
            "OSPM":      ("TSTRANSFORMER", 0.567,  0.597),
        },
        "humidity": {
            "QML":       ("QLSTM",         0.123,  0.450),
            "Classical": ("ANN",           0.101,  0.460),
            "OSPM":      ("TSTRANSFORMER", 0.470,  0.525),
        },
        "pressure": {
            "QML":       ("QLSTM",         0.628,  0.789),
            "Classical": ("LSTM",          0.683,  0.814),
            "OSPM":      ("TIMESFM",       0.652,  0.728),
        },
    },
}

# Average forecast R² per category (all cities, all models, all params)
_AVG_FORECAST_R2 = {
    "QML":       0.340,
    "Classical": 0.349,
    "OSPM":      0.402,
}

# Global win count across 9 contests (3 cities × 3 params)
_FORECAST_WINS = {"QML": 4, "Classical": 1, "OSPM": 4}


# ── CSS injected once ─────────────────────────────────────────────────────────
_CONCLUSION_CSS = """
<style>
/* ── Hero ── */
.con-hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0c4a2e 100%);
    border-radius: 14px; padding: 24px 28px; margin-bottom: 20px; color: #fff;
}
.con-hero-title { font-size: 22px; font-weight: 800; margin-bottom: 6px; }
.con-hero-sub   { font-size: 13px; opacity: 0.75; line-height: 1.65; }
.con-kpi-row    { display: grid; grid-template-columns: repeat(3,1fr);
                  gap: 12px; margin-top: 16px; }
.con-kpi        { background: rgba(255,255,255,0.10); border-radius: 10px;
                  padding: 12px 16px; text-align: center; }
.con-kpi-label  { font-size: 11px; opacity: 0.65; margin-bottom: 4px; }
.con-kpi-val    { font-size: 14px; font-weight: 700; }

/* ── Section header ── */
.con-sec {
    font-size: 15px; font-weight: 700; color: #1e293b;
    margin: 24px 0 12px; padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0;
}

/* ── H2H bars ── */
.con-h2h-grid   { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; }
.con-h2h-card   { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
                  padding: 16px; }
.con-h2h-title  { font-size: 14px; font-weight: 700; color: #1e293b;
                  margin-bottom: 12px; }
.con-h2h-cat    { margin-bottom: 10px; }
.con-h2h-hdr    { display: flex; justify-content: space-between;
                  font-size: 11px; color: #64748b; margin-bottom: 4px; }
.con-bar-bg     { background: #f1f5f9; border-radius: 4px; height: 7px;
                  overflow: hidden; }
.con-bar-fill   { height: 100%; border-radius: 4px; }
.con-bar-val    { font-size: 13px; font-weight: 700; margin-top: 3px; }
.con-h2h-footer { font-size: 11px; color: #94a3b8; margin-top: 10px;
                  padding-top: 10px; border-top: 1px solid #f1f5f9; }

/* ── Win summary ── */
.con-win-row  { display: grid; grid-template-columns: repeat(3,1fr);
                gap: 12px; margin: 16px 0; }
.con-win-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
                padding: 16px; text-align: center; }
.con-win-label{ font-size: 11px; color: #64748b; margin-bottom: 6px; }
.con-win-num  { font-size: 32px; font-weight: 800; }
.con-win-sub  { font-size: 11px; color: #94a3b8; }

/* ── Insight cards ── */
.con-insight {
    border-radius: 10px; padding: 13px 16px; margin-bottom: 10px;
    border-left: 5px solid;
}
.con-insight-title { font-size: 13px; font-weight: 700; margin-bottom: 5px; }
.con-insight-body  { font-size: 12px; line-height: 1.65; color: #374151; }

/* ── Scorecards ── */
.con-score      { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
                  padding: 16px 20px; margin-bottom: 12px; }
.con-score-top  { display: flex; justify-content: space-between; align-items: center;
                  margin-bottom: 10px; }
.con-score-name { font-size: 15px; font-weight: 700; color: #1e293b; }
.con-score-stat { font-size: 12px; color: #64748b; }
.con-score-bg   { background: #f1f5f9; border-radius: 4px; height: 7px;
                  overflow: hidden; margin-bottom: 14px; }
.con-score-fill { height: 100%; border-radius: 4px; }
.con-score-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
                  font-size: 12px; color: #374151; margin-bottom: 12px; }
.con-verdict    { border-left: 4px solid; padding: 9px 14px;
                  font-size: 12px; font-weight: 600; border-radius: 6px; }

/* ── Badge cards ── */
.con-badge-grid { display: grid; grid-template-columns: repeat(3,1fr);
                  gap: 14px; margin-bottom: 20px; }
.con-badge-card { background: #fff; border: 1.5px solid; border-radius: 12px;
                  padding: 14px 12px; }
.con-badge-title{ font-size: 13px; font-weight: 700; color: #1e293b; }
.con-badge-sub  { font-size: 11px; color: #94a3b8; margin-bottom: 10px; }
.con-badge-row  { display: flex; justify-content: space-between;
                  padding: 3px 6px; border-radius: 5px; font-size: 11px; }
.con-badge-pill { text-align: center; margin-top: 10px; padding: 6px;
                  border-radius: 7px; font-size: 11px; font-weight: 700; }

/* ── Key findings ── */
.con-finding       { background: #fff; border: 1px solid #e2e8f0;
                     border-radius: 10px; padding: 13px 16px; margin-bottom: 10px; }
.con-finding-title { font-size: 13px; font-weight: 700; color: #1e293b;
                     margin-bottom: 5px; }
.con-finding-body  { font-size: 12px; color: #374151; line-height: 1.65; }

/* ── Metrics table ── */
.con-tbl-wrap { overflow-x: auto; border: 1px solid #e2e8f0;
                border-radius: 10px; margin-bottom: 16px; }
.con-tbl-wrap table { border-collapse: collapse; width: 100%;
                      min-width: 680px; font-size: 11px; }
.con-tbl-wrap thead th {
    padding: 8px 10px; font-weight: 600; text-align: center;
    background: #f8fafc; color: #475569;
    border-bottom: 1px solid #e2e8f0;
}
.con-tbl-wrap thead th.tl { text-align: left; }
.con-tbl-wrap tbody td {
    padding: 7px 10px; text-align: center;
    border-bottom: 1px solid #f1f5f9;
}
.con-tbl-wrap tbody td.tl { text-align: left; font-weight: 600; color: #1e293b; }
.con-tbl-wrap tbody tr:hover { background: #fafafa; }
.con-tbl-wrap tbody tr:last-child td { border-bottom: none; }
.con-best { font-weight: 800; }
.con-neg  { color: #dc2626; }
.con-dash { color: #cbd5e1; }
.con-cat-sep { border-left: 2px solid #e2e8f0 !important; }

/* ── Recommendation ── */
.con-rec      { background: linear-gradient(135deg,#0f172a,#1e293b,#0c4a2e);
                border-radius: 14px; padding: 22px 26px; color: #fff; }
.con-rec-title{ font-size: 18px; font-weight: 800; margin-bottom: 8px; }
.con-rec-body { font-size: 13px; color: #94a3b8; line-height: 1.75;
                margin-bottom: 18px; }
.con-rec-row  { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; }
.con-rec-card { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
                border-radius: 10px; padding: 12px; text-align: center; }
.con-rec-lbl  { font-size: 10px; opacity: 0.6; margin-bottom: 6px; }
.con-rec-model{ font-size: 16px; font-weight: 800; margin-bottom: 4px; }
.con-rec-note { font-size: 10px; color: #64748b; }
</style>
"""


# ── Colour helpers ────────────────────────────────────────────────────────────
_C = {
    "QML":       {"fg": "#2563eb", "bg": "#eff6ff", "bd": "#bfdbfe"},
    "Classical": {"fg": "#d97706", "bg": "#fffbeb", "bd": "#fde68a"},
    "OSPM":      {"fg": "#059669", "bg": "#f0fdf4", "bd": "#6ee7b7"},
}
_CAT_LABEL = {
    "QML":       "⚛️ Quantum ML",
    "Classical": "🖥️ Classical ML",
    "OSPM":      "🤖 OSPM ",
}
_PARAM_ICON = {"temperature": "🌡️", "humidity": "💧", "pressure": "🔵"}


def _forecast_winner(param_data: dict) -> tuple:
    """Return (category, (model, forecast_r2, test_r2)) with highest forecast R²."""
    return max(param_data.items(), key=lambda x: x[1][1])


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def _render_conclusion_tab():
    import streamlit as st

    st.markdown(_CONCLUSION_CSS, unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="con-hero">
        <div class="con-hero-title">🏁 Conclusion — Research Summary</div>
        <div class="con-hero-sub">
            Data-driven performance analysis · 3 cities · 3 weather parameters ·
            QML (Quantum) vs Classical ML vs Open-Source Pre-trained Models (OSPM)<br>
            Primary metric: <b>Forecast R²</b> (generalisation on unseen data).
            Test R² is excluded from all tables.
        </div>
        <div class="con-kpi-row">
            <div class="con-kpi">
                <div class="con-kpi-label">Forecast contests (9 total)</div>
                <div class="con-kpi-val" style="color:#93c5fd;">
                    QML 4 &nbsp;·&nbsp; OSPM 4 &nbsp;·&nbsp; Classical 1
                </div>
            </div>
            <div class="con-kpi">
                <div class="con-kpi-label">Best avg forecast R² — OSPM zero-shot</div>
                <div class="con-kpi-val" style="color:#6ee7b7;">0.402</div>
            </div>
            <div class="con-kpi">
                <div class="con-kpi-label">Highest single forecast R²</div>
                <div class="con-kpi-val" style="color:#fde68a;">
                    0.800 — HQNN · Delhi · Temperature
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── City selector ─────────────────────────────────────────────────────────
    city = st.selectbox(
        "📍 Select city",
        CITIES,
        key="conclusion_city_v2",
    )

    # ── All sections rendered inline (no sub-tabs) ────────────────────────────
    _render_h2h(city)
    _render_win_cards(city)
    _render_insight_cards(city)
    _render_category_scorecards()
    _render_best_badges(city)
    _render_key_findings(city)
    _render_metrics_table(city)
    _render_final_conclusion(city)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Forecast R² head-to-head
# ══════════════════════════════════════════════════════════════════════════════

def _render_h2h(city: str):
    import streamlit as st
    import streamlit.components.v1 as components

    st.markdown(
        f'<div class="con-sec">⚔️ Forecast R² Head-to-Head — {city}'
        f'<span style="font-size:12px;font-weight:400;color:#64748b;margin-left:10px;">'
        f'(Higher = better generalisation on unseen data)</span></div>',
        unsafe_allow_html=True,
    )

    city_data = _FORECAST_BEST[city]
    params    = ["temperature", "humidity", "pressure"]

    cards_html = ""
    for param in params:
        pd        = city_data[param]
        win_cat, win_info = _forecast_winner(pd)
        max_val   = max(v[1] for v in pd.values())

        cats_html = ""
        for cat in ["QML", "Classical", "OSPM"]:
            model, fr, _ = pd[cat]
            pct   = max(0, fr / max(max_val, 0.01) * 100) if fr > 0 else 0
            is_w  = cat == win_cat
            opacity = "1" if is_w else "0.65"
            fw      = "700" if is_w else "400"
            neg_tag = (
                f'<span style="font-size:10px;color:#dc2626;margin-left:4px;">(neg)</span>'
                if fr < 0 else ""
            )
            cats_html += f"""
            <div class="con-h2h-cat" style="opacity:{opacity};">
                <div class="con-h2h-hdr">
                    <span style="font-weight:{fw};color:{_C[cat]['fg'] if is_w else '#64748b'};">
                        {'→ ' if is_w else ''}{_CAT_LABEL[cat]}
                    </span>
                    <span style="color:{_C[cat]['fg']};">{model}</span>
                </div>
                <div class="con-bar-bg">
                    <div class="con-bar-fill"
                         style="width:{pct:.1f}%;background:{_C[cat]['fg']};"></div>
                </div>
                <div class="con-bar-val" style="color:{_C[cat]['fg']};">
                    {fr:.3f}{neg_tag}
                </div>
            </div>"""

        cards_html += f"""
        <div class="con-h2h-card">
            <div class="con-h2h-title">
                {_PARAM_ICON[param]} {param.capitalize()}
            </div>
            {cats_html}
            <div class="con-h2h-footer">
                🏆 Winner:
                <span style="background:{_C[win_cat]['bg']};color:{_C[win_cat]['fg']};
                             padding:2px 8px;border-radius:5px;font-weight:700;font-size:11px;">
                    {win_cat} — {win_info[0]} · R²={win_info[1]:.3f}
                </span>
            </div>
        </div>"""

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
    <style>
    *{{box-sizing:border-box;margin:0;padding:0;}}
    html,body{{background:transparent;font-family:'Segoe UI',Arial,sans-serif;overflow:hidden;}}
    .con-h2h-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;}}
    .con-h2h-card{{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:16px;}}
    .con-h2h-title{{font-size:14px;font-weight:700;color:#1e293b;margin-bottom:12px;}}
    .con-h2h-cat{{margin-bottom:10px;opacity:1;}}
    .con-h2h-hdr{{display:flex;justify-content:space-between;font-size:11px;color:#64748b;margin-bottom:4px;}}
    .con-bar-bg{{background:#f1f5f9;border-radius:4px;height:7px;overflow:hidden;}}
    .con-bar-fill{{height:100%;border-radius:4px;}}
    .con-bar-val{{font-size:13px;font-weight:700;margin-top:3px;}}
    .con-h2h-footer{{font-size:11px;color:#94a3b8;margin-top:10px;
                     padding-top:10px;border-top:1px solid #f1f5f9;}}
    </style></head><body>
    <div class="con-h2h-grid">{cards_html}</div>
    </body></html>"""

    components.html(html, height=310, scrolling=False)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Win count cards
# ══════════════════════════════════════════════════════════════════════════════

def _render_win_cards(city: str):
    import streamlit as st

    wins    = {"QML": 0, "Classical": 0, "OSPM": 0}
    cd      = _FORECAST_BEST[city]
    for param in cd:
        win_cat, _ = _forecast_winner(cd[param])
        wins[win_cat] += 1

    top_cat = max(wins, key=wins.get)
    cols    = st.columns(3)

    for col, cat in zip(cols, ["QML", "Classical", "OSPM"]):
        is_top  = cat == top_cat
        border  = f"2px solid {_C[cat]['fg']}" if is_top else "1px solid #e2e8f0"
        with col:
            st.markdown(f"""
            <div style="background:#fff;border:{border};border-radius:12px;
                        padding:16px;text-align:center;margin-bottom:12px;">
                <div style="font-size:11px;color:#64748b;margin-bottom:6px;">
                    {_CAT_LABEL[cat]}
                </div>
                <div style="font-size:32px;font-weight:800;color:{_C[cat]['fg']};">
                    {wins[cat]}
                </div>
                <div style="font-size:11px;color:#94a3b8;">/ 3 parameter contests</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — City insights
# ══════════════════════════════════════════════════════════════════════════════

_INSIGHTS = {
    "Delhi": [
        (
            "HQNN dominates Delhi — highest single R² in the study",
            "#2563eb", "#eff6ff", "#bfdbfe",
            "HQNN achieves forecast R²=0.800 on temperature — the highest result across "
            "all models, all cities, and all parameters. Its hybrid quantum-classical "
            "architecture captures the large-amplitude seasonal swings and temperature "
            "inversions that define Delhi's continental climate.",
        ),
        (
            "CHRONOS competitive without any fine-tuning",
            "#059669", "#f0fdf4", "#6ee7b7",
            "CHRONOS scores forecast R²=0.666 on temperature and 0.437 on pressure with "
            "zero Delhi-specific fine-tuning, confirming that large pre-trained time-series "
            "models encode useful global meteorological priors even for Indian continental climates.",
        ),
        (
            "Humidity is the universal open challenge",
            "#7c3aed", "#f5f3ff", "#ddd6fe",
            "No model exceeds forecast R²=0.445 on Delhi humidity. The abrupt monsoon onset "
            "and rapid post-monsoon drying create regime shifts that overwhelm all model "
            "categories equally — this remains the primary open research challenge.",
        ),
    ],
    "Mumbai": [
        (
            "TIMESFM leads Mumbai — zero-shot outperforms fine-tuned models",
            "#059669", "#f0fdf4", "#6ee7b7",
            "TIMESFM wins on temperature (0.686) and humidity (0.303) for Mumbai without "
            "any fine-tuning. The city's narrow temperature range and consistent sea-breeze "
            "patterns align with coastal patterns in TIMESFM's global pre-training corpus.",
        ),
        (
            "QGRU is the strongest quantum model for coastal climates",
            "#2563eb", "#eff6ff", "#bfdbfe",
            "QGRU records forecast R²=0.613 (temperature) and 0.624 (pressure). Its gated "
            "recurrent memory handles Mumbai's slowly-changing barometric patterns efficiently "
            "with fewer parameters than classical LSTM.",
        ),
        (
            "Humidity ceiling is lowest in Mumbai",
            "#7c3aed", "#f5f3ff", "#ddd6fe",
            "Humidity forecast peaks at 0.303 (TIMESFM). The high baseline humidity (>70% "
            "year-round) with sudden pre-monsoon surges creates variance that all architectures "
            "fail to capture reliably.",
        ),
    ],
    "Chennai": [
        (
            "OSPM excels — wins temperature and humidity",
            "#059669", "#f0fdf4", "#6ee7b7",
            "TSTRANSFORMER achieves forecast R²=0.567 (temperature) and 0.470 (humidity) — "
            "the only city where OSPM wins on two of three parameters. Chennai's tropical "
            "dual-monsoon patterns appear well-represented in the global pre-training corpus.",
        ),
        (
            "Classical LSTM best for pressure — the only classical win in the study",
            "#d97706", "#fffbeb", "#fde68a",
            "LSTM achieves the best pressure forecast R²=0.683 in Chennai — the single "
            "classical win across all 9 head-to-head contests. Sequential LSTM memory aligns "
            "well with slowly-evolving south Indian monsoon pressure systems.",
        ),
        (
            "QML needs more Chennai training data",
            "#dc2626", "#fef2f2", "#fecaca",
            "QML shows the sharpest test-to-forecast gap (HQNN: 0.755 test → 0.172 forecast "
            "on temperature). Quantum variational circuits are more sensitive to sample size — "
            "expanding the Chennai training window is the highest-priority action.",
        ),
    ],
}


def _render_insight_cards(city: str):
    import streamlit as st

    st.markdown(
        f'<div class="con-sec">💡 City Insights — {city}</div>',
        unsafe_allow_html=True,
    )
    for title, color, bg, bd, body in _INSIGHTS[city]:
        st.markdown(f"""
        <div class="con-insight"
             style="border-left-color:{color};background:{bg};">
            <div class="con-insight-title" style="color:{color};">{title}</div>
            <div class="con-insight-body">{body}</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Category scorecards (global, all cities)
# ══════════════════════════════════════════════════════════════════════════════

_SCORECARDS = [
    {
        "cat":      "QML",
        "avg":      0.340,
        "wins":     4,
        "best":     "HQNN Delhi Temperature — 0.800",
        "worst":    "HQNN Chennai Temperature — 0.172",
        "strength": "Test accuracy; parameter efficiency (up to 84% fewer params)",
        "limit":    "Forecast generalisation drops sharply in data-scarce cities",
        "verdict":  "Best when hardware efficiency and parameter compression matter",
    },
    {
        "cat":      "OSPM",
        "avg":      0.402,
        "wins":     4,
        "best":     "TIMESFM Mumbai Temperature — 0.686",
        "worst":    "CHRONOS Delhi Humidity — 0.151",
        "strength": "Best avg forecast R² (0.402) without any fine-tuning",
        "limit":    "Humidity prediction unreliable; sensitive to distribution shift",
        "verdict":  "Best for rapid zero-shot deployment with no training data",
    },
    {
        "cat":      "Classical",
        "avg":      0.349,
        "wins":     1,
        "best":     "LSTM Chennai Pressure — 0.683",
        "worst":    "GRU Delhi Pressure — 0.286",
        "strength": "Stable, interpretable, production-grade behaviour",
        "limit":    "Fewer forecast wins vs QML and OSPM across all contests",
        "verdict":  "Best for interpretability and explainable production pipelines",
    },
]


def _render_category_scorecards():
    import streamlit as st

    st.markdown(
        '<div class="con-sec">'
        '📊 Category Performance Scorecards '
        '<span style="font-size:12px;font-weight:400;color:#64748b;">'
        '— all cities · all parameters</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    for s in _SCORECARDS:
        cat    = s["cat"]
        bar_w  = s["avg"] * 100
        fg     = _C[cat]["fg"]
        bg     = _C[cat]["bg"]

        st.markdown(f"""
        <div class="con-score">
            <div class="con-score-top">
                <div class="con-score-name" style="color:{fg};">{_CAT_LABEL[cat]}</div>
                <div class="con-score-stat">
                    {s['wins']}/9 wins &nbsp;·&nbsp; avg forecast R² = {s['avg']:.3f}
                </div>
            </div>
            <div class="con-score-bg">
                <div class="con-score-fill"
                     style="width:{bar_w:.1f}%;background:{fg};"></div>
            </div>
            <div class="con-score-grid">
                <div><b style="color:#16a34a;">✅ Best:</b> {s['best']}</div>
                <div><b style="color:#dc2626;">⚠️ Weakest:</b> {s['worst']}</div>
                <div><b>💪 Strength:</b> {s['strength']}</div>
                <div><b>🔻 Limitation:</b> {s['limit']}</div>
            </div>
            <div class="con-verdict"
                 style="border-left-color:{fg};color:{fg};background:{bg};">
                🎯 {s['verdict']}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Best model badges per parameter
# ══════════════════════════════════════════════════════════════════════════════

def _render_best_badges(city: str):
    import streamlit as st

    st.markdown(
        f'<div class="con-sec">🥇 Best Forecast Model per Parameter — {city}</div>',
        unsafe_allow_html=True,
    )

    city_data   = _FORECAST_BEST[city]
    params      = ["temperature", "humidity", "pressure"]
    cols        = st.columns(3)

    for col, param in zip(cols, params):
        pd = city_data[param]
        win_cat, (win_model, win_r2, _) = _forecast_winner(pd)
        border_color = _C[win_cat]["fg"]

        rows_html = ""
        for cat in ["QML", "Classical", "OSPM"]:
            m, fr, _ = pd[cat]
            is_w  = cat == win_cat
            fw    = "700" if is_w else "400"
            row_bg = _C[cat]["bg"] if is_w else "transparent"
            rows_html += f"""
            <div class="con-badge-row"
                 style="background:{row_bg};font-weight:{fw};">
                <span style="color:{_C[cat]['fg']};">{cat} ({m})</span>
                <span style="color:{_C[cat]['fg']};">{fr:.3f}</span>
            </div>"""

        with col:
            st.markdown(f"""
            <div class="con-badge-card"
                 style="border-color:{border_color};">
                <div class="con-badge-title">
                    {_PARAM_ICON[param]} {param.capitalize()}
                </div>
                <div class="con-badge-sub">Forecast R²</div>
                {rows_html}
                <div class="con-badge-pill"
                     style="background:{_C[win_cat]['bg']};
                            color:{_C[win_cat]['fg']};">
                    🏆 {win_cat} wins · {win_r2:.3f}
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — Key findings
# ══════════════════════════════════════════════════════════════════════════════

_KEY_FINDINGS = {
    "Delhi": [
        (
            "⚛️ Quantum HQNN is the star of this study",
            "HQNN's forecast R²=0.800 on Delhi temperature is the single best result across "
            "all 27 city-parameter-model contests. The quantum component captures non-linear "
            "temperature inversions that characterise Delhi winters and monsoon transitions.",
        ),
        (
            "🤖 OSPM validates zero-shot meteorological priors",
            "CHRONOS achieves forecast R²=0.666 (temperature) and 0.437 (pressure) with no "
            "Delhi-specific fine-tuning, confirming that large pre-trained models generalise "
            "meaningfully to Indian continental climates.",
        ),
        (
            "💧 Humidity remains the universal open challenge",
            "No model exceeds forecast R²=0.445 on Delhi humidity — abrupt monsoon transitions "
            "create discontinuities that overwhelm all model architectures equally.",
        ),
    ],
    "Mumbai": [
        (
            "🤖 Mumbai is where OSPM should be the primary model",
            "TIMESFM outperforms all fine-tuned models on temperature and humidity in zero-shot "
            "mode. Mumbai's low climate variability makes it uniquely suited for large pre-trained "
            "models trained on global coastal patterns.",
        ),
        (
            "⚛️ QGRU best quantum model for coastal climates",
            "QGRU's gated recurrence handles Mumbai's stable barometric patterns efficiently "
            "with fewer parameters than classical LSTM — achieving forecast R²=0.624 on pressure.",
        ),
        (
            "🔵 Pressure most predictable across all categories",
            "Pressure forecast R² exceeds 0.468 for every model category — the highest "
            "predictability floor of any city-parameter combination in the study.",
        ),
    ],
    "Chennai": [
        (
            "🤖 Chennai presents the hardest forecasting environment",
            "OSPM leads temperature and humidity; Classical LSTM leads pressure. No single "
            "architecture dominates — an ensemble of TSTRANSFORMER + LSTM is the recommended "
            "production approach.",
        ),
        (
            "🖥️ Classical LSTM uniquely suited to Chennai pressure",
            "Slow-moving pressure systems during monsoon and retreating-monsoon phases favour "
            "LSTM's sequential memory over quantum or zero-shot approaches — the only classical "
            "win in the entire study.",
        ),
        (
            "⚠️ QML training data gap is the key bottleneck",
            "HQNN shows 0.755 test R² but only 0.172 forecast R² on temperature. Expanding "
            "the Chennai historical training window is the highest-priority action to unlock "
            "quantum advantage in this dual-monsoon climate.",
        ),
    ],
}


def _render_key_findings(city: str):
    import streamlit as st

    st.markdown(
        f'<div class="con-sec">🔬 Key Research Findings — {city}</div>',
        unsafe_allow_html=True,
    )
    for title, body in _KEY_FINDINGS[city]:
        st.markdown(f"""
        <div class="con-finding">
            <div class="con-finding-title">{title}</div>
            <div class="con-finding-body">{body}</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — Complete forecast metrics table (no Test R², no empty columns)
# ══════════════════════════════════════════════════════════════════════════════

def _render_metrics_table(city: str):
    import streamlit as st
    import streamlit.components.v1 as components

    st.markdown(
        f'<div class="con-sec">'
        f'📋 Complete Forecast Metrics — {city}'
        f'<span style="font-size:12px;font-weight:400;color:#64748b;margin-left:10px;">'
        f'Forecast split only · Best R² per parameter highlighted</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    model_type = st.radio(
        "Model type",
        ["Multivariate", "Univariate"],
        horizontal=True,
        key="conclusion_model_type_v2",
        index=0,
    )

    params     = ["temperature", "humidity", "pressure"]
    metrics    = [("R²", "R2"), ("RMSE", "RMSE"), ("MAE", "MAE")]

    cat_configs = [
        ("⚛️ Quantum ML",         "QML",       ALL_MODELS,       METRICS_DATA),
        ("🖥️ Classical ML",       "Classical", CLASSICAL_MODELS, CLASSICAL_METRICS_DATA),
    ]
    if model_type == "Univariate":
        cat_configs.append(
            ("🤖 OSPM ", "OSPM", OSPM_MODELS, OSPM_METRICS_DATA)
        )
    else:
        st.info(
            "ℹ️ OSPM models were evaluated on **Univariate** data only — "
            "switch to Univariate to view them."
        )

    for cat_label, cat_key, model_dict, metrics_dict in cat_configs:
        # Filter to models with at least one non-None forecast value
        active = {}
        for mk, ml in model_dict.items():
            city_d = (
                metrics_dict.get(model_type, {})
                            .get(city, {})
                            .get(mk, {})
            )
            if any(
                city_d.get(p, {}).get("Forecast", {}).get(mm) is not None
                for p in params
                for _, mm in metrics
            ):
                active[mk] = ml

        if not active:
            st.caption(f"No forecast data for {cat_label} in this configuration.")
            continue

        # Find best R² per param (across ALL categories for fairness)
        best_r2 = {}
        for p in params:
            vals = []
            for mk in active:
                city_d = (
                    metrics_dict.get(model_type, {})
                                .get(city, {})
                                .get(mk, {})
                )
                v = city_d.get(p, {}).get("Forecast", {}).get("R2")
                if v is not None:
                    vals.append(v)
            best_r2[p] = max(vals) if vals else None

        fg = _C.get(cat_key, {"fg": "#374151"})["fg"]
        bg = _C.get(cat_key, {"bg": "#f8fafc"})["bg"]

        # Build HTML table
        col_span  = len(params) * len(metrics)
        hdr_style = (
            f"background:{fg};color:#fff;font-weight:600;"
            "font-size:12px;padding:9px 12px;text-align:center;"
        )

        # Sub-header: param labels
        param_ths = "".join(
            f'<th colspan="{len(metrics)}" '
            f'style="background:{bg};font-weight:600;font-size:11px;'
            f'padding:6px 10px;text-align:center;'
            f'border-left:{"2px solid #e2e8f0" if i>0 else "none"};">'
            f'{_PARAM_ICON[p]} {p.capitalize()}</th>'
            for i, p in enumerate(params)
        )

        # Metric sub-sub-headers
        metric_ths = "".join(
            f'<th style="background:#fafafa;font-size:10px;color:#64748b;'
            f'padding:5px 8px;text-align:center;'
            f'border-left:{"2px solid #e2e8f0" if pi>0 and mi==0 else "1px solid #f1f5f9"};">'
            f'{ml}</th>'
            for pi, p in enumerate(params)
            for mi, (ml, _) in enumerate(metrics)
        )

        tbody = ""
        for row_i, (mk, ml) in enumerate(active.items()):
            city_d = (
                metrics_dict.get(model_type, {})
                            .get(city, {})
                            .get(mk, {})
            )
            row_bg = "#ffffff" if row_i % 2 == 0 else "#fafafa"
            tds = (
                f'<td style="padding:8px 12px;font-weight:600;font-size:12px;'
                f'color:#1e293b;white-space:nowrap;border-right:2px solid #e2e8f0;'
                f'background:#fff;">{ml}</td>'
            )
            for pi, p in enumerate(params):
                for mi, (_, mm) in enumerate(metrics):
                    v   = city_d.get(p, {}).get("Forecast", {}).get(mm)
                    txt = f"{v:.4f}" if v is not None else "—"
                    is_best = (
                        mm == "R2"
                        and v is not None
                        and best_r2.get(p) is not None
                        and abs(v - best_r2[p]) < 0.0001
                    )
                    is_neg  = v is not None and v < 0
                    is_dash = v is None
                    cell_fg = (
                        fg if is_best else
                        "#dc2626" if is_neg else
                        "#cbd5e1" if is_dash else
                        "#1e293b"
                    )
                    cell_fw = "800" if is_best else "400"
                    border_l = (
                        "border-left:2px solid #e2e8f0;"
                        if pi > 0 and mi == 0 else
                        "border-left:1px solid #f1f5f9;"
                    )
                    tds += (
                        f'<td style="padding:8px 10px;font-size:12px;text-align:center;'
                        f'background:{row_bg};color:{cell_fg};font-weight:{cell_fw};'
                        f'border-bottom:1px solid #f1f5f9;{border_l}">'
                        f'{txt}{"↑" if is_best else ""}</td>'
                    )
            tbody += f"<tr>{tds}</tr>"

        n_data_cols = len(active) * len(params) * len(metrics)
        height      = 3 * 30 + len(active) * 38 + 20

        html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
        <style>
        *{{box-sizing:border-box;margin:0;padding:0;}}
        html,body{{background:transparent;font-family:'Segoe UI',Arial,sans-serif;overflow:hidden;}}
        .wrap{{overflow-x:auto;border-radius:10px;border:1px solid #e2e8f0;
               box-shadow:0 2px 8px rgba(0,0,0,0.05);}}
        table{{border-collapse:collapse;width:100%;}}
        th,td{{white-space:nowrap;}}
        </style></head><body>
        <div class="wrap"><table>
          <thead>
            <tr>
              <th style="{hdr_style} text-align:left;border-bottom:1px solid rgba(255,255,255,0.2);">
                {cat_label}
              </th>
              {param_ths}
            </tr>
            <tr>
              <th style="background:#fafafa;font-size:10px;color:#64748b;
                         padding:5px 8px;text-align:left;border-right:2px solid #e2e8f0;
                         border-bottom:1px solid #e2e8f0;">Model</th>
              {metric_ths}
            </tr>
          </thead>
          <tbody>{tbody}</tbody>
        </table></div></body></html>"""

        components.html(html, height=height, scrolling=False)
        st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — Operational recommendation
# ══════════════════════════════════════════════════════════════════════════════

_RECS = {
    "Delhi": {
        "qml":      "HQNN",
        "ospm":     "CHRONOS",
        "classical":"LSTM",
        "hard":     "Humidity",
        "qml_n":    "forecast R²=0.800 on temperature — best in study",
        "ospm_n":   "forecast R²=0.666 on temperature, zero fine-tuning",
        "cls_n":    "stable pressure prediction, forecast R²=0.375",
        "hard_n":   "max R²≤0.445 across all model categories",
        "body": (
            "HQNN is the clear operational choice for Delhi — it achieves the highest single "
            "forecast R² in the entire study (0.800, temperature) and strong pressure "
            "performance (0.670). Pair with CHRONOS as a zero-shot backup when new training "
            "data is unavailable. Humidity forecasting remains an open challenge for all "
            "model categories in Delhi's complex continental climate."
        ),
    },
    "Mumbai": {
        "qml":      "QGRU",
        "ospm":     "TIMESFM",
        "classical":"GRU",
        "hard":     "Humidity",
        "qml_n":    "forecast R²=0.624 pressure · 0.613 temperature",
        "ospm_n":   "forecast R²=0.686 temperature — best for Mumbai",
        "cls_n":    "reliable baseline, forecast R²=0.578 temperature",
        "hard_n":   "max R²≤0.303 across all model categories",
        "body": (
            "Mumbai is the one city where OSPM (TIMESFM) should be the primary model — "
            "it outperforms fine-tuned models on both temperature and humidity in zero-shot "
            "mode. QGRU serves as a strong quantum backup, especially for pressure. "
            "Mumbai's low climate variability makes it uniquely well-suited for large "
            "pre-trained models trained on global coastal patterns."
        ),
    },
    "Chennai": {
        "qml":      "QLSTM",
        "ospm":     "TSTRANSFORMER",
        "classical":"LSTM",
        "hard":     "Temperature",
        "qml_n":    "forecast R²=0.628 on pressure — most reliable QML variable",
        "ospm_n":   "leads temperature (0.567) and humidity (0.470)",
        "cls_n":    "best pressure predictor, forecast R²=0.683",
        "hard_n":   "QML forecast R²=0.172 — training-data-limited",
        "body": (
            "Chennai presents the hardest forecasting environment. TSTRANSFORMER (OSPM) "
            "leads on temperature and humidity, while Classical LSTM edges all models on "
            "pressure. For production use, an ensemble of TSTRANSFORMER + LSTM is "
            "recommended. QML models need expanded Chennai training data before they can "
            "realise their quantum advantage in this dual-monsoon climate."
        ),
    },
}

def _render_final_conclusion(city: str):
    import streamlit as st

    st.markdown(
        f'<div class="con-sec">🎯 Operational Recommendation — {city}</div>',
        unsafe_allow_html=True,
    )

    r = _RECS[city]
    items = [
        ("Primary QML",      r["qml"],       r["qml_n"],  "#93c5fd"),
        ("Best OSPM",        r["ospm"],      r["ospm_n"], "#6ee7b7"),
        ("Classical Baseline", r["classical"], r["cls_n"], "#fde68a"),
        ("Hardest Variable", r["hard"],      r["hard_n"], "#c4b5fd"),
    ]

    cards_html = "".join(f"""
        <div class="con-rec-card">
            <div class="con-rec-lbl">{label}</div>
            <div class="con-rec-model" style="color:{color};">{model}</div>
            <div class="con-rec-note">{note}</div>
        </div>"""
        for label, model, note, color in items
    )

    st.markdown(f"""
    <div class="con-rec">
        <div class="con-rec-title">🎯 {city}</div>
        <div class="con-rec-body">{r['body']}</div>
        <div class="con-rec-row">{cards_html}</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# Kept for backward compatibility (called from other tabs if needed)
# ══════════════════════════════════════════════════════════════════════════════

def _render_performance_summary(city: str):
    """Alias — routes to new implementation."""
    _render_category_scorecards()
    _render_best_badges(city)

def _render_best_model_badges(city: str):
    """Alias — routes to new implementation."""
    _render_best_badges(city)

def _render_complete_metrics(city: str):
    """Alias — routes to new implementation."""
    _render_metrics_table(city)

def _render_full_model_table(city: str, model_type: str = "Multivariate"):
    """Alias — routes to new implementation."""
    _render_metrics_table(city)