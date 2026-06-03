# data/rain_noise_loader.py
"""
Rain noise data loading functions
"""
import streamlit as st
import pandas as pd
import os
from config.constants import RAIN_NOISE_QUANTUM_ALGORITHMS, RAIN_NOISE_CLASSIFICATION_METRICS


@st.cache_data
def load_rain_noise_forecast_data(filename):
    """Load rain noise forecast CSV data"""
    try:
        if not os.path.exists(filename):
            st.error(f"File not found: {filename}")
            return None
        
        df = pd.read_csv(filename)
        
        if df.empty:
            st.error(f"File {filename} is empty")
            return None
        # ✅ FIX: Check for lowercase column names
        # Your files have: datetime, RF_binary, QGRU_pred/QNN-IS_pred/QNN-SE_pred
        if 'datetime' in df.columns:
            df.rename(columns={'datetime': 'Datetime'}, inplace=True)
        
        if 'RF_binary' in df.columns:
            df.rename(columns={'RF_binary': 'Actual'}, inplace=True)
        # Expected columns: Datetime, Actual, [Algorithm prediction column]
        required_cols = ['Datetime', 'Actual']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns in {filename}: {missing_cols}")
            st.info(f"Available columns: {df.columns.tolist()}")
            return None
        
          # Parse datetime
        datetime_formats = [
            '%Y-%m-%d %H:%M:%S',  # ✅ Your format: 2025-08-01 00:00:00
            '%d-%m-%Y %H:%M:%S',
            '%d-%m-%Y %H:%M',
            '%Y-%m-%d %H:%M',
            '%d/%m/%Y %H:%M:%S',
            '%d/%m/%Y %H:%M'
        ]
        
        datetime_parsed = False
        for fmt in datetime_formats:
            try:
                df['Datetime'] = pd.to_datetime(df['Datetime'], format=fmt)
                datetime_parsed = True
                break
            except ValueError:
                continue
        
        if not datetime_parsed:
            try:
                df['Datetime'] = pd.to_datetime(df['Datetime'])
            except Exception as e:
                st.error(f"Could not parse datetime: {str(e)}")
                return None
        
        return df
        
    except Exception as e:
        st.error(f"Error loading {filename}: {str(e)}")
        return None


def get_rain_noise_file_path(algorithm_name, noise_type):
    """
    Get file path for rain noise data
    """
    if algorithm_name not in RAIN_NOISE_QUANTUM_ALGORITHMS:
        return None
    
    algo_config = RAIN_NOISE_QUANTUM_ALGORITHMS[algorithm_name]
    
    # If "Without Noise" selected, return the base model file
    if noise_type == "Without Noise":
        return algo_config.get("without_noise_file")

    # ✅ FIX: Use the mapping to get correct folder name
    from config.constants import RAIN_NOISE_TYPE_TO_FOLDER
    
    # # Otherwise, construct path to error folder
    # error_folder_name = noise_type.replace(" ", "")
    # file_path = algo_config.get("noise_folder", "").format(error_type=error_folder_name)
    
    # return file_path
    # ✅ FIX: Use the mapping to get correct folder name
    
    
    error_folder_name = RAIN_NOISE_TYPE_TO_FOLDER.get(noise_type, noise_type.replace(" ", ""))
    file_path = algo_config.get("noise_folder", "").format(error_type=error_folder_name)
    
    return file_path


def get_rain_noise_algorithm_data(algorithm_name, noise_type, selected_date=None):
    """
    Load rain noise data for a specific algorithm and noise type
    
    Args:
        algorithm_name: Full algorithm name
        noise_type: Type of noise
        selected_date: Optional date to filter by
    
    Returns:
        DataFrame with rain prediction data
    """
    try:
        if algorithm_name not in RAIN_NOISE_QUANTUM_ALGORITHMS:
            st.error(f"Algorithm '{algorithm_name}' not available")
            return None
        
        # Get the correct file path
        filename = get_rain_noise_file_path(algorithm_name, noise_type)
        
        if not filename:
            st.error(f"No file mapping for {algorithm_name} with {noise_type}")
            return None
        
        # Load data
        data = load_rain_noise_forecast_data(filename)
        if data is None:
            return None
        
        # Find prediction column (not Datetime or Actual)
        prediction_col = None
        for col in data.columns:
            if col not in ['Datetime', 'Actual']:
                prediction_col = col
                break
        
        if prediction_col is None:
            st.error(f"Could not find prediction column in {filename}")
            return None
        
        # Keep only necessary columns
        result_data = data[['Datetime', 'Actual', prediction_col]].copy()
        
        # Filter by date if provided
        if selected_date:
            result_data['Date'] = result_data['Datetime'].dt.date
            result_data = result_data[result_data['Date'] == selected_date]
            result_data = result_data.drop('Date', axis=1)
        
        if len(result_data) == 0:
            st.warning(f"No data for selected criteria")
            return None
        
        return result_data
        
    except Exception as e:
        st.error(f"Error loading rain noise data: {str(e)}")
        return None


def get_rain_noise_metrics(algorithm_short_name, noise_type):
    """
    Get classification metrics for rain noise
    """
    return RAIN_NOISE_CLASSIFICATION_METRICS.get(noise_type, {}).get(algorithm_short_name, {})