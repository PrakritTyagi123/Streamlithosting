# data/loader.py
"""
Data loading and processing functions
"""
import streamlit as st
import pandas as pd
import os
from pathlib import Path


@st.cache_data
def load_forecast_data(filename):
    """Load forecast CSV data with comprehensive error handling"""
    try:
        if not os.path.exists(filename):
            st.error(f"File not found: {filename}")
            return None
        
        df = pd.read_csv(filename)
        
        if df.empty:
            st.error(f"File {filename} is empty")
            return None
        
        required_cols = ['Datetime', 'T2M']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns in {filename}: {missing_cols}")
            return None
            
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
                datetime_parsed = True
            except Exception as e:
                st.error(f"Could not parse datetime column in {filename}: {str(e)}")
                return None
        
        return df
        
    except Exception as e:
        st.error(f"Error loading {filename}: {str(e)}")
        return None


@st.cache_data
def get_available_dates(filename):
    """Extract available dates from CSV file"""
    try:
        if not os.path.exists(filename):
            return []
        
        df = pd.read_csv(filename)
        
        datetime_formats = [
            '%d-%m-%Y %H:%M:%S',
            '%d-%m-%Y %H:%M',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M'
        ]
        
        for fmt in datetime_formats:
            try:
                df['Datetime'] = pd.to_datetime(df['Datetime'], format=fmt)
                break
            except:
                continue
        
        if df['Datetime'].dtype == 'object':
            df['Datetime'] = pd.to_datetime(df['Datetime'], dayfirst=True)
        
        df['Date'] = df['Datetime'].dt.date
        available_dates = sorted(df['Date'].unique())
        
        return available_dates
    except Exception as e:
        st.error(f"Error reading dates from {filename}: {str(e)}")
        return []


def filter_data_by_date_and_interval(data, start_date, end_date, time_interval):
    """Filter data based on date range and time interval"""
    df = data.copy()
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    
    df['Date'] = df['Datetime'].dt.date
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].copy()
    df = df.sort_values('Datetime').reset_index(drop=True)
    
    if len(df) == 0:
        return df
    
    df['Hour'] = df['Datetime'].dt.hour
    
    interval_hours = {
        "1 Hour": list(range(24)),
        "3 Hours": [1, 4, 7, 10, 13, 16, 19, 22],
        "6 Hours": [1, 7, 13, 19],
        "12 Hours": [1, 13],
        "24 Hours": [1]
    }
    
    hours_to_keep = interval_hours.get(time_interval, list(range(24)))
    
    filtered_df = df[df['Hour'].isin(hours_to_keep)].copy()
    filtered_df = filtered_df.drop(['Date', 'Hour'], axis=1)
    
    days_count = (end_date - start_date).days + 1
    
    # st.info(f"Showing {len(filtered_df)} data points across {days_count} day(s) "
    #         f"with {time_interval} intervals ({len(hours_to_keep)} points/day)")
    
    return filtered_df
 

#############################  RAINFALL FUNCTIONS  #############################

def load_rainfall_predictions(algorithm_name, data_folder="files/rainfall_data"):
    """
    Load rainfall predictions for a specific algorithm with robust encoding handling
    
    Args:
        algorithm_name: Name of the algorithm (ANN, SVM, QNNIS, QSVM, etc.)
        data_folder: Folder containing the CSV files
        
    Returns:
        DataFrame with datetime, actual values, and predictions
    """
    from config.constants import RAINFALL_FILE_MAPPING
    
    if algorithm_name not in RAINFALL_FILE_MAPPING:
        st.error(f"Algorithm '{algorithm_name}' not found in RAINFALL_FILE_MAPPING")
        return None
    
    file_info = RAINFALL_FILE_MAPPING[algorithm_name]
    file_path = Path(data_folder) / file_info["predictions"]
    
    if not file_path.exists():
        st.error(f"File not found: {file_path}")
        return None
    
    # ✅ Try multiple encodings
    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'iso-8859-1', 'cp1252']
    df = None
    
    for encoding in encodings_to_try:
        try:
            df = pd.read_csv(file_path, encoding=encoding, encoding_errors='replace')
            # print(f"Loaded {file_path} with encoding {encoding}")
            break  # Success, exit loop
        except Exception as e:
            continue  # Try next encoding
    
    if df is None:
        st.error(f"Could not read file {file_path} with any encoding")
        return None
    
    try:
        # ✅ Clean column names (remove any hidden characters)
        df.columns = [str(col).strip() for col in df.columns]
        # print(df.columns)
        # Rename columns for consistency
        # Expected: datetime, RF_binary, [model]_pred
        if len(df.columns) >= 3:
            df.columns = ['Datetime', 'Actual', f'{algorithm_name}_Prediction']
            # print(df.columns)
        else:
            st.error(f"Unexpected number of columns in {file_path}: {len(df.columns)}")
            return None
        
        # ✅ Convert datetime with multiple format attempts
        datetime_formats = [
            '%Y-%m-%d %H:%M:%S',
            '%d-%m-%Y %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%d-%m-%Y %H:%M',
            '%Y/%m/%d %H:%M:%S',
            '%d/%m/%Y %H:%M:%S',
        ]
        
        datetime_parsed = False
        for fmt in datetime_formats:
            try:
                df['Datetime'] = pd.to_datetime(df['Datetime'], format=fmt, errors='coerce')
                datetime_parsed = True
                # print(df)
                break
            except:
                continue
        
        if not datetime_parsed:
            # Final attempt with automatic parsing
            df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
        
        # ✅ Remove rows with invalid datetimes
        df = df.dropna(subset=['Datetime'])
        # print(df)
        if df.empty:
            st.error(f"No valid data after datetime parsing in {file_path}")
            return None
        
        # ✅ Convert to binary with error handling
        try:
            df['Actual'] = pd.to_numeric(df['Actual'], errors='coerce').fillna(0).astype(int)
            df[f'{algorithm_name}_Prediction'] = pd.to_numeric(
                df[f'{algorithm_name}_Prediction'], 
                errors='coerce'
            ).fillna(0).astype(int)
        except Exception as e:
            st.error(f"Error converting values to binary in {file_path}: {str(e)}")
            return None
        
        # ✅ Ensure values are only 0 or 1
        df['Actual'] = df['Actual'].clip(0, 1)
        df[f'{algorithm_name}_Prediction'] = df[f'{algorithm_name}_Prediction'].clip(0, 1)
        
        # ✅ Final cleanup - remove any remaining NaN
        df = df.dropna()
        
        # ✅ Sort by datetime
        df = df.sort_values('Datetime').reset_index(drop=True)
        # print(df)
        return df
        
    except Exception as e:
        st.error(f"Error processing {file_path}: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None


def load_rainfall_metrics(algorithm_name, data_folder="rainfall_data"):
    """
    Load rainfall metrics for a specific algorithm
    
    Args:
        algorithm_name: Name of the algorithm
        data_folder: Folder containing the CSV files (not used currently)
        
    Returns:
        Dictionary with metrics
    """
    from config.constants import CLASSIFICATION_METRICS
    
    if algorithm_name in CLASSIFICATION_METRICS:
        # ✅ Return a copy to avoid modifying the original
        metrics = CLASSIFICATION_METRICS[algorithm_name].copy()
        # print(metrics)
        # ✅ Ensure all values are clean Python types
        cleaned_metrics = {}
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                # Convert to float if it has decimal, otherwise int
                cleaned_metrics[key] = float(value) if isinstance(value, float) else int(value)
                # print(cleaned_metrics[key])
            else:
                cleaned_metrics[key] = value
        
        return cleaned_metrics
        # print(cleaned_metrics)
    
    st.warning(f"No metrics found for algorithm: {algorithm_name}")
    return {}


def get_rainfall_data_for_display(algorithm_name):
    """
    Get formatted data for displaying rainfall predictions
    
    Args:
        algorithm_name: Name of the algorithm
        
    Returns:
        Dictionary with data and metadata, or None if loading fails
    """
    try:
        # ✅ Clean algorithm name
        algorithm_name = str(algorithm_name).strip()
        
        df = load_rainfall_predictions(algorithm_name)
        # print(df)
        if df is None or df.empty:
            st.error(f"Could not load data for {algorithm_name}")
            return None
        
        metrics = load_rainfall_metrics(algorithm_name)
        
        # ✅ Return clean dictionary
        return {
            'data': df,
            'algorithm': algorithm_name,
            'prediction_column': f'{algorithm_name}_Prediction',
            'metrics': metrics if metrics else {},
            'type': 'classification'
        }
        # result = {
        #     'data': df,
        #     'algorithm': algorithm_name,
        #     'prediction_column': f'{algorithm_name}_Prediction',
        #     'metrics': metrics if metrics else {},
        #     'type': 'classification'
        # }
        # print(result)
    except Exception as e:
        st.error(f"Error in get_rainfall_data_for_display for {algorithm_name}: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None
    

def get_available_rainfall_dates(data_folder="files/rainfall_data"):
    """
    Extract available dates from rainfall CSV files
    Returns list of unique dates across all rainfall prediction files
    """
    from config.constants import RAINFALL_FILE_MAPPING
    from pathlib import Path
    
    all_dates = set()
    
    try:
        # Check one of the rainfall files to get dates
        # Using ANN as reference since all files should have same date range
        file_info = RAINFALL_FILE_MAPPING.get("ANN")
        if file_info:
            file_path = Path(data_folder) / file_info["predictions"]
            
            if file_path.exists():
                # ✅ Try multiple encodings
                df = None
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        df = pd.read_csv(file_path, encoding=encoding)
                        break
                    except:
                        continue
                
                if df is None:
                    st.error(f"Could not read {file_path}")
                    return []
                
                # Try multiple datetime formats
                datetime_formats = [
                    '%Y-%m-%d %H:%M:%S',
                    '%d-%m-%Y %H:%M:%S',
                    '%Y-%m-%d %H:%M',
                    '%d-%m-%Y %H:%M',
                    '%Y/%m/%d %H:%M:%S',
                    '%d/%m/%Y %H:%M:%S',
                    '%Y/%m/%d %H:%M',
                    '%d/%m/%Y %H:%M'
                ]
                
                datetime_parsed = False
                for fmt in datetime_formats:
                    try:
                        df['datetime'] = pd.to_datetime(df.iloc[:, 0], format=fmt, errors='coerce')
                        datetime_parsed = True
                        break
                    except:
                        continue
                
                if not datetime_parsed:
                    df['datetime'] = pd.to_datetime(df.iloc[:, 0], dayfirst=True, errors='coerce')
                
                # ✅ Remove invalid dates
                df = df.dropna(subset=['datetime'])
                
                # Extract unique dates
                df['date'] = df['datetime'].dt.date
                all_dates = set(df['date'].unique())
        
        return sorted(list(all_dates))
        
    except Exception as e:
        st.error(f"Error reading rainfall dates: {str(e)}")
        return []


@st.cache_data
def get_rainfall_date_range(data_folder="files/rainfall_data"):
    """Get min/max dates from rainfall data without loading full predictions"""
    from config.constants import RAINFALL_FILE_MAPPING
    from pathlib import Path
    
    # logger.debug("get_rainfall_date_range called")
    
    try:
        file_info = RAINFALL_FILE_MAPPING.get("LSTM")
        if not file_info:
            # logger.debug("LSTM not in RAINFALL_FILE_MAPPING, using defaults")
            return datetime(2025, 8, 1).date(), datetime(2025, 8, 31).date()
        
        file_path = Path(data_folder) / file_info["predictions"]
        if not file_path.exists():
            # logger.warning(f"Rainfall file not found: {file_path}, using defaults")
            return datetime(2025, 8, 1).date(), datetime(2025, 8, 31).date()
        
        # ✅ Read only the datetime column (first column) to minimize memory
        df = pd.read_csv(file_path, usecols=[0], encoding='utf-8', encoding_errors='replace')
        
        if df.empty:
            # logger.warning("Rainfall file is empty, using defaults")
            return datetime(2025, 8, 1).date(), datetime(2025, 8, 31).date()
        
        # Get first and last values
        first_val = df.iloc[0, 0]
        last_val = df.iloc[-1, 0]
        
        # Try multiple datetime formats
        datetime_formats = [
            '%Y-%m-%d %H:%M:%S',
            '%d-%m-%Y %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%d-%m-%Y %H:%M',
            '%Y/%m/%d %H:%M:%S',
            '%d/%m/%Y %H:%M:%S',
        ]
        
        first_date = None
        last_date = None
        
        # Try parsing first date
        for fmt in datetime_formats:
            try:
                first_date = pd.to_datetime(first_val, format=fmt, errors='coerce')
                if pd.notna(first_date):
                    break
            except:
                continue
        
        if first_date is None or pd.isna(first_date):
            first_date = pd.to_datetime(first_val, errors='coerce')
        
        # Try parsing last date
        for fmt in datetime_formats:
            try:
                last_date = pd.to_datetime(last_val, format=fmt, errors='coerce')
                if pd.notna(last_date):
                    break
            except:
                continue
        
        if last_date is None or pd.isna(last_date):
            last_date = pd.to_datetime(last_val, errors='coerce')
        
        # Return dates if valid
        if pd.notna(first_date) and pd.notna(last_date):
            min_date = first_date.date()
            max_date = last_date.date()
            # logger.debug(f"Date range extracted: {min_date} to {max_date}")
            return min_date, max_date
        else:
            # logger.warning("Could not parse dates from file, using defaults")
            return datetime(2025, 8, 1).date(), datetime(2025, 8, 31).date()
            
    except Exception as e:
        # logger.exception(f"Error getting date range: {e}")
        return datetime(2025, 8, 1).date(), datetime(2025, 8, 31).date()