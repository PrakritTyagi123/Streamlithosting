"""
ui/meteogram_loader.py
======================
CHANGES:
  - QRC removed, VQC added to quantum models
  - CRC removed from classical models
  - OSPM (Open Source Pre-trained Model) loader added at the bottom
  - Pressure unit normalised to hPa:
      files in Pa  (mean > 2000) → divided by 100
      files in hPa (mean ≤ 2000) → kept as-is
"""

import os
import io
import glob
import pandas as pd
import streamlit as st

_THIS_DIR     = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_THIS_DIR)

BASE_FOLDER         = os.path.join(_PROJECT_ROOT, "files", "Meteogram_data")
UNIVARIATE_FOLDER   = os.path.join(BASE_FOLDER, "Univariate_data")
MULTIVARIATE_FOLDER = os.path.join(BASE_FOLDER, "Multivariate_data")

CITIES      = ["Delhi", "Mumbai", "Chennai"]
MODEL_TYPES = ["Univariate", "Multivariate"]

ALL_MODELS = {
    "QLSTM": "Quantum Long Short Term Memory (QLSTM)",
    "QGRU":  "Quantum Gated Recurrent Unit (QGRU)",
    "HQNN":  "Hybrid Quantum Neural Network (HQNN)",
    "VQC":   "Variational Quantum Circuit (VQC)",
    "QSVR":  "Quantum Support Vector Regression (QSVR)",
}

CLASSICAL_MODELS = {
    "LSTM": "Long Short Term Memory (LSTM)",
    "GRU":  "Gated Recurrent Unit (GRU)",
    "ANN":  "Artificial Neural Network (ANN)",
    "SVR":  "Support Vector Regression (SVR)",
}

OSPM_MODELS = {
    "TIMESFM":       "timesfm_2.5_200M-pytorch",
    "CHRONOS":       "Amazon/Chronos-t5-large Model",
    "PATCHTST":      "PatchTST Model",
    "TSTRANSFORMER": "Timeseries Transformer Model",
    "MOMENT":        "AutonLab/MOMENT_1_Large Model",
}

PARAM_PREFIX_MAP = {
    "temp": "temperature",
    "hum":  "humidity",
    "pres": "pressure",
}

COL_ALIASES = {
    "date": "datetime", "time": "datetime", "Date": "datetime",
    "DateTime": "datetime", "Datetime": "datetime", "DATETIME": "datetime",
    "t2m": "temperature", "T2M": "temperature",
    "Temp": "temperature", "TEMPERATURE": "temperature",
    "rh": "humidity", "RH": "humidity", "rel_humidity": "humidity",
    "relative_humidity": "humidity", "HUMIDITY": "humidity",
    "mslp": "pressure", "MSLP": "pressure", "slp": "pressure",
    "SLP": "pressure", "PRESSURE": "pressure",
}

_DATETIME_COLS = {
    "date", "datetime", "time", "Date", "DateTime", "Datetime",
    "DATETIME", "DATE", "TIME", "time_forecast", "Time_Forecast", "TIME_FORECAST",
}
_YTRUE_COLS = {
    "y_true", "Y_true", "Y_True", "actual", "Actual",
    "Actual_forecast", "actual_forecast", "ACTUAL",
}
_YPRED_COLS = {
    "y_pred", "Y_pred", "Y_Pred", "predicted", "Predicted",
    "Forecast", "forecast", "FORECAST", "PREDICTED",
    "prediction", "Prediction", "PREDICTION",
}

_MODEL_ALIASES = {
    "hybrid_qnn_se":     "HQNN",
    "hybrid_qnn_is_2.0": "HQNN",
    "hybrid_qnn":        "HQNN",
    "hqnn":              "HQNN",
    "qlstm":             "QLSTM",
    "qgru":              "QGRU",
    "vqc":               "VQC",
    "qsvr":              "QSVR",
}

_CLASSICAL_MODEL_ALIASES = {
    "lstm": "LSTM",
    "gru":  "GRU",
    "ann":  "ANN",
    "svr":  "SVR",
}

_CLA_PREFIX  = "cla_"
_OSPM_PREFIX = "ospm_"

_OSPM_MODEL_ALIASES = {
    "timesfm_2":              "TIMESFM",
    "timesfm":                "TIMESFM",
    "chronos_t5":             "CHRONOS",
    "chronos":                "CHRONOS",
    "patchtst":               "PATCHTST",
    "timeseries_transformer": "TSTRANSFORMER",
    "tstransformer":          "TSTRANSFORMER",
    "moment_1":               "MOMENT",
    "moment":                 "MOMENT",
}


# ─────────────────────────────────────────────────────────────────────────────
# Shared helpers
# ─────────────────────────────────────────────────────────────────────────────

def _parse_datetime(series: pd.Series) -> pd.Series:
    for fmt in ("%d-%m-%Y", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d",
                "%m-%d-%y", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return pd.to_datetime(series, format=fmt)
        except Exception:
            continue
    return pd.to_datetime(series, dayfirst=True)


def _kelvin_to_celsius(series: pd.Series) -> pd.Series:
    """Convert Kelvin → Celsius when mean > 100, otherwise just round."""
    s = pd.to_numeric(series, errors="coerce")
    return (s - 273.15).round(3) if s.mean() > 100 else s.round(3)


def _pa_to_hpa(series: pd.Series) -> pd.Series:
    """
    Normalise pressure to hPa regardless of source unit.

    Heuristic:
      - Pa  values are typically 80 000 – 110 000  → mean >> 2 000
      - hPa values are typically      800 – 1 100  → mean  <  2 000

    Files already in hPa are passed through unchanged (just rounded).
    Files in Pa are divided by 100 before rounding.
    """
    s = pd.to_numeric(series, errors="coerce")
    return (s / 100).round(2) if s.mean() > 2000 else s.round(2)


def _convert_value(series: pd.Series, param_col: str) -> pd.Series:
    """
    Dispatch to the correct unit-normalisation helper for each parameter.

      temperature → Kelvin-aware Celsius conversion
      pressure    → Pa-aware hPa conversion
      humidity    → numeric coercion + rounding only
    """
    if param_col == "temperature":
        return _kelvin_to_celsius(series)
    elif param_col == "pressure":
        return _pa_to_hpa(series)
    else:
        # humidity (and any future parameter): just coerce + round
        return pd.to_numeric(series, errors="coerce").round(3)


def _detect_city(fname_low):
    for c in CITIES:
        if c.lower() in fname_low:
            return c
    return None


def _detect_model(fname_low):
    for alias in sorted(_MODEL_ALIASES.keys(), key=len, reverse=True):
        if alias in fname_low:
            return _MODEL_ALIASES[alias]
    return None


def _detect_param(fname_low):
    for prefix, col in PARAM_PREFIX_MAP.items():
        if fname_low.startswith(prefix):
            return col
    return None


def _normalise_section(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip() for c in df.columns]
    for col in list(df.columns):
        if col in _DATETIME_COLS:
            df = df.rename(columns={col: "datetime"})
            break
    for col in list(df.columns):
        if col in _YTRUE_COLS and col != "y_true":
            df = df.rename(columns={col: "y_true"})
            break
    for col in list(df.columns):
        if col in _YPRED_COLS and col != "y_pred":
            df = df.rename(columns={col: "y_pred"})
            break
    return df


def _read_csv_smart(filepath: str) -> pd.DataFrame:
    """
    Read CSV that may have a second header mid-file.
    Section 0  -> historical data   (_is_forecast = False)
    Section 1+ -> forecast data     (_is_forecast = True)
    Used for QUANTUM and OSPM files.
    """
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        raw_lines = f.readlines()

    if not raw_lines:
        return pd.DataFrame()

    sections   = []
    cur_header = None
    cur_lines  = []

    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            continue
        first_token = stripped.split(",")[0].strip()
        is_header = False
        try:
            float(first_token)
        except ValueError:
            try:
                pd.to_datetime(first_token, dayfirst=True)
                is_header = False
            except Exception:
                is_header = True

        if is_header:
            if cur_header and cur_lines:
                sections.append((cur_header, cur_lines[:]))
            cur_header = stripped
            cur_lines  = []
        else:
            if cur_header is not None:
                cur_lines.append(line)

    if cur_header and cur_lines:
        sections.append((cur_header, cur_lines[:]))

    if not sections:
        df = pd.read_csv(filepath, sep=None, engine="python")
        df.columns = [c.strip() for c in df.columns]
        df["_is_forecast"] = False
        return df

    dfs = []
    for section_idx, (header, lines) in enumerate(sections):
        try:
            clean_header = header.rstrip(",")
            clean_lines  = [l.rstrip().rstrip(",") + "\n" for l in lines]
            text = clean_header + "\n" + "".join(clean_lines)
            df   = pd.read_csv(io.StringIO(text))
            df   = _normalise_section(df)
            if "datetime" in df.columns:
                df["_is_forecast"] = (section_idx > 0)
                dfs.append(df)
        except Exception:
            continue

    if not dfs:
        df = pd.read_csv(filepath, sep=None, engine="python")
        df.columns = [c.strip() for c in df.columns]
        df["_is_forecast"] = False
        return df

    return pd.concat(dfs, ignore_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# Quantum loader
# ─────────────────────────────────────────────────────────────────────────────

def _load_single_csv(filepath: str):
    fname     = os.path.basename(filepath)
    fname_low = fname.lower().replace(".csv", "")

    city      = _detect_city(fname_low)
    model     = _detect_model(fname_low)
    param_col = _detect_param(fname_low)

    if not city:
        raise ValueError(f"City not recognised: {fname}")
    if not model:
        raise ValueError(f"Model not recognised: {fname}")
    if not param_col:
        raise ValueError(f"Param prefix missing: {fname}")

    df = _read_csv_smart(filepath)

    if df.empty:
        raise ValueError(f"Empty file: {fname}")

    # Use param-aware conversion so pressure is always stored in hPa
    if "y_pred" in df.columns:
        df[param_col] = _convert_value(df["y_pred"], param_col)
        if "y_true" in df.columns:
            df[param_col + "_actual"] = _convert_value(df["y_true"], param_col)
        df.drop(columns=[c for c in ("y_pred", "y_true") if c in df.columns], inplace=True)

    if "datetime" not in df.columns:
        df.rename(columns={k: v for k, v in COL_ALIASES.items() if k in df.columns}, inplace=True)

    if "datetime" not in df.columns:
        raise ValueError(f"No datetime column: {fname}")

    df["datetime"] = _parse_datetime(df["datetime"].astype(str).str.strip())
    df = df.dropna(subset=["datetime", param_col])
    df = df.sort_values("datetime").reset_index(drop=True)

    keep = ["datetime", param_col, param_col + "_actual", "_is_forecast"]
    df   = df[[c for c in keep if c in df.columns]]

    return city, model, param_col, df


# ─────────────────────────────────────────────────────────────────────────────
# Classical loader
# ─────────────────────────────────────────────────────────────────────────────

def _detect_classical_model(fname_low):
    for alias in sorted(_CLASSICAL_MODEL_ALIASES.keys(), key=len, reverse=True):
        if alias in fname_low:
            return _CLASSICAL_MODEL_ALIASES[alias]
    return None


def _detect_classical_param(fname_low):
    stripped = fname_low[len(_CLA_PREFIX):] if fname_low.startswith(_CLA_PREFIX) else fname_low
    for prefix, col in PARAM_PREFIX_MAP.items():
        if stripped.startswith(prefix):
            return col
    return None


def _load_classical_csv(filepath: str):
    fname     = os.path.basename(filepath)
    fname_low = fname.lower().replace(".csv", "")

    if not fname_low.startswith(_CLA_PREFIX):
        raise ValueError(f"Not a classical file (missing 'cla_' prefix): {fname}")

    city      = _detect_city(fname_low)
    model     = _detect_classical_model(fname_low)
    param_col = _detect_classical_param(fname_low)

    if not city:
        raise ValueError(f"City not recognised in classical file: {fname}")
    if not model:
        raise ValueError(f"Classical model not recognised: {fname}")
    if not param_col:
        raise ValueError(f"Param prefix missing in classical file: {fname}")

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        raw_lines = f.readlines()

    sections   = []
    cur_header = None
    cur_lines  = []

    for line in raw_lines:
        stripped = line.strip()
        if not stripped or all(c == ',' for c in stripped):
            continue
        first_token = stripped.split(",")[0].strip()
        is_header = False
        try:
            float(first_token)
        except ValueError:
            try:
                pd.to_datetime(first_token, dayfirst=True)
                is_header = False
            except Exception:
                is_header = True

        if is_header:
            if cur_header and cur_lines:
                sections.append((cur_header, cur_lines[:]))
            cur_header = stripped
            cur_lines  = []
        else:
            if cur_header is not None:
                cur_lines.append(line)

    if cur_header and cur_lines:
        sections.append((cur_header, cur_lines[:]))

    if not sections:
        raise ValueError(f"No parseable sections in classical file: {fname}")

    _DT_NAMES   = {"time", "datetime", "date", "time_forecast",
                   "date_forecast", "time_pred", "date_pred"}
    _PRED_NAMES = {"y_pred", "forecast", "predicted", "prediction",
                   "y_prediction", "pred", "forecasted"}
    _ACT_NAMES  = {"actual", "y_true", "actual_forecast", "true",
                   "observed", "y_actual"}

    dfs = []
    for section_idx, (header, lines) in enumerate(sections):
        try:
            text   = header + "\n" + "".join(lines)
            sec_df = pd.read_csv(io.StringIO(text))
            sec_df.columns = [c.strip() for c in sec_df.columns]
            sec_df = sec_df.dropna(how="all")

            # ── Find datetime column ───────────────────────────────────────
            dt_col = None
            for c in sec_df.columns:
                if c.strip().lower() in _DT_NAMES:
                    dt_col = c
                    break
            if dt_col is None:
                for c in sec_df.columns:
                    try:
                        pd.to_datetime(sec_df[c].dropna().iloc[0])
                        dt_col = c
                        break
                    except Exception:
                        continue
            if dt_col is None:
                continue
            sec_df = sec_df.rename(columns={dt_col: "datetime"})

            # ── Find prediction column ─────────────────────────────────────
            pred_col = None
            for c in sec_df.columns:
                if c.strip().lower() in _PRED_NAMES:
                    pred_col = c
                    break
            if pred_col is None:
                continue

            # ── Find actual column (optional) ──────────────────────────────
            act_col = None
            for c in sec_df.columns:
                if c.strip().lower() in _ACT_NAMES:
                    act_col = c
                    break

            # Use param-aware conversion so pressure is always stored in hPa
            sec_df[param_col]      = _convert_value(sec_df[pred_col], param_col)
            sec_df["_is_forecast"] = (section_idx > 0)

            keep_cols = ["datetime", param_col, "_is_forecast"]
            if act_col is not None:
                actual_key = param_col + "_actual"
                sec_df[actual_key] = _convert_value(sec_df[act_col], param_col)
                keep_cols.append(actual_key)

            sec_df = sec_df[keep_cols].dropna(subset=["datetime", param_col])
            dfs.append(sec_df)
        except Exception:
            continue

    if not dfs:
        raise ValueError(f"No valid data parsed from classical file: {fname}")

    df = pd.concat(dfs, ignore_index=True)
    df["datetime"] = _parse_datetime(df["datetime"].astype(str).str.strip())
    df = df.dropna(subset=["datetime", param_col])
    df = df.sort_values("datetime").reset_index(drop=True)
    actual_key = param_col + "_actual"
    keep_final = ["datetime", param_col, "_is_forecast"]
    if actual_key in df.columns:
        keep_final.append(actual_key)
    df = df[keep_final]

    return city, model, param_col, df


# ─────────────────────────────────────────────────────────────────────────────
# OSPM loader  (Open Source Pre-trained Models)
# ─────────────────────────────────────────────────────────────────────────────

def _detect_ospm_model(fname_low: str):
    """Return canonical OSPM model key from filename, or None."""
    for alias in sorted(_OSPM_MODEL_ALIASES.keys(), key=len, reverse=True):
        if alias in fname_low:
            return _OSPM_MODEL_ALIASES[alias]
    return None


def _detect_ospm_param(fname_low: str):
    """
    OSPM files: ospm_temp_delhi_timesfm.csv
    Strip 'ospm_' prefix, then match param prefix.
    """
    stripped = fname_low[len(_OSPM_PREFIX):] if fname_low.startswith(_OSPM_PREFIX) else fname_low
    for prefix, col in PARAM_PREFIX_MAP.items():
        if stripped.startswith(prefix):
            return col
    return None


def _load_ospm_csv(filepath: str):
    """
    Load a single OSPM CSV file.
    Expected filename: ospm_<param>_<city>_<model_key>.csv
    e.g.  ospm_temp_delhi_timesfm.csv
          ospm_hum_mumbai_chronos.csv
          ospm_pres_chennai_patchtst.csv

    Returns (city, model, param_col, df).
    df columns: datetime, {param_col}, [{param_col}_actual], _is_forecast
    Pressure is always stored in hPa regardless of source unit.
    """
    fname     = os.path.basename(filepath)
    fname_low = fname.lower().replace(".csv", "")

    if not fname_low.startswith(_OSPM_PREFIX):
        raise ValueError(f"Not an OSPM file (missing 'ospm_' prefix): {fname}")

    city      = _detect_city(fname_low)
    model     = _detect_ospm_model(fname_low)
    param_col = _detect_ospm_param(fname_low)

    if not city:
        raise ValueError(f"City not recognised in OSPM file: {fname}")
    if not model:
        raise ValueError(f"OSPM model not recognised: {fname}")
    if not param_col:
        raise ValueError(f"Param prefix missing in OSPM file: {fname}")

    # Re-use the same smart CSV reader (supports multi-section / forecast rows)
    df = _read_csv_smart(filepath)

    if df.empty:
        raise ValueError(f"Empty OSPM file: {fname}")

    # Use param-aware conversion so pressure is always stored in hPa
    if "y_pred" in df.columns:
        df[param_col] = _convert_value(df["y_pred"], param_col)
        if "y_true" in df.columns:
            df[param_col + "_actual"] = _convert_value(df["y_true"], param_col)
        df.drop(columns=[c for c in ("y_pred", "y_true") if c in df.columns], inplace=True)

    if "datetime" not in df.columns:
        df.rename(columns={k: v for k, v in COL_ALIASES.items() if k in df.columns}, inplace=True)

    if "datetime" not in df.columns:
        raise ValueError(f"No datetime column in OSPM file: {fname}")

    df["datetime"] = _parse_datetime(df["datetime"].astype(str).str.strip())
    df = df.dropna(subset=["datetime", param_col])
    df = df.sort_values("datetime").reset_index(drop=True)

    keep = ["datetime", param_col, param_col + "_actual", "_is_forecast"]
    df   = df[[c for c in keep if c in df.columns]]

    return city, model, param_col, df


# ─────────────────────────────────────────────────────────────────────────────
# Folder scanner
# ─────────────────────────────────────────────────────────────────────────────

def _scan_folder(folder: str, model_type: str, store: dict, cla_store: dict,
                 ospm_store: dict, loaded: set, log: list):
    if not os.path.exists(folder):
        log.append(f"⚠️ Folder not found: `{folder}`")
        return

    csv_files = glob.glob(os.path.join(folder, "*.csv"))
    if not csv_files:
        log.append(f"⚠️ No CSV files in: `{folder}`")
        return

    for filepath in sorted(csv_files):
        if filepath in loaded:
            continue
        fname     = os.path.basename(filepath)
        fname_low = fname.lower()

        # ── OSPM file ──────────────────────────────────────────────────────
        if fname_low.startswith(_OSPM_PREFIX):
            try:
                city, model, param_col, df = _load_ospm_csv(filepath)
                n_hist = int((~df["_is_forecast"]).sum()) if "_is_forecast" in df.columns else len(df)
                n_fore = int(df["_is_forecast"].sum())    if "_is_forecast" in df.columns else 0
                (ospm_store
                 .setdefault(model_type, {})
                 .setdefault(city, {})
                 .setdefault(model, {})[param_col]) = df
                loaded.add(filepath)
                log.append(
                    f"✅ [OSPM/{model_type}] `{fname}` → "
                    f"**{city}** / **{model}** / **{param_col}** "
                    f"({n_hist} historical + {n_fore} forecast rows)"
                )
            except Exception as e:
                log.append(f"❌ `{fname}`: {e}")

        # ── Classical file ─────────────────────────────────────────────────
        elif fname_low.startswith(_CLA_PREFIX):
            try:
                city, model, param_col, df = _load_classical_csv(filepath)
                n_hist = int((~df["_is_forecast"]).sum()) if "_is_forecast" in df.columns else len(df)
                n_fore = int(df["_is_forecast"].sum())    if "_is_forecast" in df.columns else 0
                (cla_store
                 .setdefault(model_type, {})
                 .setdefault(city, {})
                 .setdefault(model, {})[param_col]) = df
                loaded.add(filepath)
                log.append(
                    f"✅ [Classical/{model_type}] `{fname}` → "
                    f"**{city}** / **{model}** / **{param_col}** "
                    f"({n_hist} historical + {n_fore} forecast rows)"
                )
            except Exception as e:
                log.append(f"❌ `{fname}`: {e}")

        # ── Quantum file ───────────────────────────────────────────────────
        else:
            try:
                city, model, param_col, df = _load_single_csv(filepath)
                (store
                 .setdefault(model_type, {})
                 .setdefault(city, {})
                 .setdefault(model, {})[param_col]) = df
                loaded.add(filepath)
                n_hist = int((~df["_is_forecast"]).sum()) if "_is_forecast" in df.columns else len(df)
                n_fore = int(df["_is_forecast"].sum())    if "_is_forecast" in df.columns else 0
                log.append(
                    f"✅ [Quantum/{model_type}] `{fname}` → **{city}** / **{model}** / **{param_col}** "
                    f"({n_hist} historical + {n_fore} forecast rows)"
                )
            except Exception as e:
                log.append(f"❌ `{fname}`: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# Public API — Quantum
# ─────────────────────────────────────────────────────────────────────────────

def load_meteogram_data(force_reload: bool = False) -> dict:
    """
    Load all CSV files from both Univariate and Multivariate folders.

    Quantum store:
        store[model_type][city][model][param] = DataFrame

    Classical store:
        cla_store[model_type][city][model][param] = DataFrame

    OSPM store:
        ospm_store[model_type][city][model][param] = DataFrame

    All pressure values are normalised to hPa at load time.
    """
    if (
        not force_reload
        and st.session_state.get("_meteogram_data_loaded", False)
    ):
        return st.session_state.get("_meteogram_store", {})

    store      = {}
    cla_store  = {}
    ospm_store = {}
    loaded     = set()
    log        = []

    _scan_folder(UNIVARIATE_FOLDER,   "Univariate",   store, cla_store, ospm_store, loaded, log)
    _scan_folder(MULTIVARIATE_FOLDER, "Multivariate", store, cla_store, ospm_store, loaded, log)

    st.session_state._meteogram_store        = store
    st.session_state._meteogram_cla_store    = cla_store
    st.session_state._meteogram_ospm_store   = ospm_store
    st.session_state._meteogram_loaded_paths = loaded
    st.session_state._meteogram_load_log     = log
    st.session_state._meteogram_data_loaded  = True

    return store


def get_available_models(city: str, model_type: str) -> list:
    store = st.session_state.get("_meteogram_store", {})
    return list(store.get(model_type, {}).get(city, {}).keys())


def get_param_df(city: str, model: str, model_type: str, param: str):
    store = st.session_state.get("_meteogram_store", {})
    return store.get(model_type, {}).get(city, {}).get(model, {}).get(param, None)


def get_loaded_params(city: str, model: str, model_type: str) -> list:
    store = st.session_state.get("_meteogram_store", {})
    return list(store.get(model_type, {}).get(city, {}).get(model, {}).keys())


# ─────────────────────────────────────────────────────────────────────────────
# Public API — Classical
# ─────────────────────────────────────────────────────────────────────────────

def get_available_classical_models(city: str, model_type: str) -> list:
    cla_store = st.session_state.get("_meteogram_cla_store", {})
    return list(cla_store.get(model_type, {}).get(city, {}).keys())


def get_classical_param_df(city: str, model: str, model_type: str, param: str):
    cla_store = st.session_state.get("_meteogram_cla_store", {})
    return cla_store.get(model_type, {}).get(city, {}).get(model, {}).get(param, None)


def get_loaded_classical_params(city: str, model: str, model_type: str) -> list:
    cla_store = st.session_state.get("_meteogram_cla_store", {})
    return list(cla_store.get(model_type, {}).get(city, {}).get(model, {}).keys())


# ─────────────────────────────────────────────────────────────────────────────
# Public API — OSPM
# ─────────────────────────────────────────────────────────────────────────────

def get_ospm_param_df(city: str, model: str, model_type: str, param: str):
    """Return OSPM DataFrame for given city/model/param, or None."""
    ospm_store = st.session_state.get("_meteogram_ospm_store", {})
    return ospm_store.get(model_type, {}).get(city, {}).get(model, {}).get(param, None)


def get_loaded_ospm_params(city: str, model: str, model_type: str) -> list:
    """Return list of params loaded for an OSPM model."""
    ospm_store = st.session_state.get("_meteogram_ospm_store", {})
    return list(ospm_store.get(model_type, {}).get(city, {}).get(model, {}).keys())


def get_available_ospm_models(city: str, model_type: str) -> list:
    """Return list of OSPM model keys that have at least one param loaded."""
    ospm_store = st.session_state.get("_meteogram_ospm_store", {})
    return list(ospm_store.get(model_type, {}).get(city, {}).keys())


# ─────────────────────────────────────────────────────────────────────────────
# Load log helper
# ─────────────────────────────────────────────────────────────────────────────

def show_load_log():
    log = st.session_state.get("_meteogram_load_log", [])
    if not log:
        return
    with st.expander("📋 Data Load Log", expanded=False):
        for entry in log:
            st.markdown(entry)