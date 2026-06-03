# data/processor.py
"""
Data processing and algorithm-specific operations
"""
import streamlit as st
from data.loader import load_forecast_data, filter_data_by_date_and_interval
from config.constants import CLASSICAL_ALGORITHMS, QUANTUM_ALGORITHMS


def get_algorithm_data_with_dates(algorithm_type, algorithm_name, start_date, end_date, time_interval):
    """Get data for specific algorithm with date range and interval filtering"""
    try:
        if algorithm_type == 'classical':
            filename = CLASSICAL_ALGORITHMS[algorithm_name]['file']
        else:
            filename = QUANTUM_ALGORITHMS[algorithm_name]['file']
        
        data = load_forecast_data(filename)
        if data is None:
            return None
        
        available_cols = list(data.columns)
        prediction_col = None
        
        for col in available_cols:
            if col not in ['Datetime', 'T2M']:
                prediction_col = col
                break
        
        if prediction_col is None:
            st.error(f"Could not find prediction column in {filename}")
            return None
        
        result_data = data[['Datetime', 'T2M', prediction_col]].copy()
        
        filtered_data = filter_data_by_date_and_interval(
            result_data, start_date, end_date, time_interval
        )
        
        if len(filtered_data) == 0:
            st.warning(f"No data found for the selected date range and interval")
            return None
        
        return filtered_data
        
    except Exception as e:
        st.error(f"Error getting algorithm data: {str(e)}")
        return None