# data/noise_loader.py
"""
Smart noise data loading - handles both "Without Noise" and error files
"""
import streamlit as st
import pandas as pd
import os
from config.constants import NOISE_QUANTUM_ALGORITHMS, NOISE_METRICS, NOISE_TYPE_TO_FOLDER


@st.cache_data
def load_noise_forecast_data(filename):
    """Load noise forecast CSV data"""
    try:
        if not os.path.exists(filename):
            st.error(f"File not found: {filename}")
            return None
        
        df = pd.read_csv(filename)
        
        if df.empty:
            st.error(f"File {filename} is empty")
            return None
        
        # Expected columns: Datetime, T2M, [Algorithm prediction column]
        required_cols = ['Datetime', 'T2M']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns in {filename}: {missing_cols}")
            return None
        
        # Parse datetime
        datetime_formats = [
            '%d-%m-%Y %H:%M:%S',
            '%d-%m-%Y %H:%M',
            '%Y-%m-%d %H:%M:%S',
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
                df['Datetime'] = pd.to_datetime(df['Datetime'], dayfirst=True)
            except Exception as e:
                st.error(f"Could not parse datetime: {str(e)}")
                return None
        
        return df
        
    except Exception as e:
        st.error(f"Error loading {filename}: {str(e)}")
        return None


def get_file_path_for_noise(algorithm_name, noise_type):
    """
    ✅ FIXED - Smart file path resolution with proper mapping
    Handles both "Without Noise" and error-specific files
    """
    if algorithm_name not in NOISE_QUANTUM_ALGORITHMS:
        return None
    
    algo_config = NOISE_QUANTUM_ALGORITHMS[algorithm_name]
    
    # If "Without Noise" selected, return the base model file
    if noise_type == "Without Noise":
        return algo_config.get("without_noise_file")
    
    # ✅ FIX: Use the mapping from config instead of simple replace
    # Convert display name to folder name using the mapping
    folder_name = NOISE_TYPE_TO_FOLDER.get(noise_type)
    
    if not folder_name:
        st.error(f"Unknown noise type: {noise_type}")
        return None
    
    # Construct path using the mapped folder name
    noise_folder_template = algo_config.get("noise_folder", "")
    
    if not noise_folder_template:
        st.error(f"No noise folder template for {algorithm_name}")
        return None
    
    # Replace {error_type} with the correctly formatted folder name
    file_path = noise_folder_template.format(error_type=folder_name)
    
    # Debug output (optional - remove in production)
    # st.write(f"🔍 Debug: noise_type='{noise_type}' → folder_name='{folder_name}'")
    # st.write(f"🔍 Debug: file_path='{file_path}'")
    
    return file_path


def get_noise_algorithm_data(algorithm_name, noise_type, start_date, end_date, time_interval):
    """
    ✅ UPDATED - Now handles "Without Noise" option
    """
    try:
        if algorithm_name not in NOISE_QUANTUM_ALGORITHMS:
            st.error(f"Algorithm '{algorithm_name}' not available")
            return None
        
        # ✅ Get the correct file path
        filename = get_file_path_for_noise(algorithm_name, noise_type)
        
        if not filename:
            st.error(f"No file mapping for {algorithm_name} with {noise_type}")
            return None
        
        # ✅ Add debug info
        # st.info(f"📂 Loading: {filename}")
        
        # Check if file exists before trying to load
        if not os.path.exists(filename):
            st.error(f"❌ File does not exist: {filename}")
            st.info(f"💡 Expected algorithm: {algorithm_name}")
            st.info(f"💡 Expected noise type: {noise_type}")
            return None
        
        # Load data
        data = load_noise_forecast_data(filename)
        if data is None:
            return None
        
        # st.success(f"✅ Successfully loaded data from {filename}")
        
        # Find prediction column
        prediction_col = None
        for col in data.columns:
            if col not in ['Datetime', 'T2M']:
                prediction_col = col
                break
        
        if prediction_col is None:
            st.error(f"Could not find prediction column in {filename}")
            st.info(f"Available columns: {data.columns.tolist()}")
            return None
        
        # Keep only necessary columns
        result_data = data[['Datetime', 'T2M', prediction_col]].copy()
        
        # Filter by date range and interval
        from data.loader import filter_data_by_date_and_interval
        filtered_data = filter_data_by_date_and_interval(
            result_data, start_date, end_date, time_interval
        )
        
        if len(filtered_data) == 0:
            st.warning(f"No data for selected range")
            return None
        
        return filtered_data
        
    except Exception as e:
        st.error(f"Error loading noise data: {str(e)}")
        import traceback
        st.error(f"Stack trace: {traceback.format_exc()}")
        return None


def get_noise_metrics(algorithm_short_name, noise_type):
    """
    ✅ UPDATED - Now handles all error types dynamically
    """
    return NOISE_METRICS.get(noise_type, {}).get(algorithm_short_name, {})