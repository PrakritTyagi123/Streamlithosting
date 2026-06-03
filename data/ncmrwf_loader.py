"""
NCMRWF Data Loading Functions - MULTI-FORMAT DATE SUPPORT
"""
import streamlit as st
import pandas as pd
import os


@st.cache_data
def load_ncmrwf_data(filename, pred_col, actual_col):
    """Load NCMRWF CSV data with automatic date format detection"""
    try:
        if not os.path.exists(filename):
            st.error(f"File not found: {filename}")
            return None
        
        df = pd.read_csv(filename)
        
        if df.empty:
            st.error(f"File {filename} is empty")
            return None
        
        # Find date column
        date_col = None
        for col in ['date', 'Date', 'DATE', 'Datetime', 'datetime', 'DATETIME', 'gvdate']:
            if col in df.columns:
                date_col = col
                break
        
        if date_col is None:
            st.error(f"No date column found in {filename}")
            st.info(f"Available columns: {list(df.columns)}")
            return None
        
        if pred_col not in df.columns:
            st.error(f"Prediction column '{pred_col}' not found")
            st.info(f"Available columns: {list(df.columns)}")
            return None
        
        if actual_col not in df.columns:
            st.error(f"Actual column '{actual_col}' not found")
            st.info(f"Available columns: {list(df.columns)}")
            return None
        
        # Show sample of raw data
        print(f"\n{'='*60}")
        print(f"Loading: {os.path.basename(filename)}")
        print(f"Sample raw dates: {df[date_col].head(3).tolist()}")
        print(f"{'='*60}")
        
        # ✅ FIX: Try multiple date formats
        date_formats = [
            '%d-%m-%Y',  # DD-MM-YYYY (e.g., 11-08-2024)
            '%m-%d-%y',  # MM-DD-YY (e.g., 08-11-24)
            '%m-%d-%Y',  # MM-DD-YYYY (e.g., 08-11-2024)
            '%d-%m-%y',  # DD-MM-YY (e.g., 11-08-24)
            '%Y-%m-%d',  # YYYY-MM-DD (ISO format)
        ]
        
        parsed = False
        for fmt in date_formats:
            try:
                df[date_col] = pd.to_datetime(df[date_col], format=fmt)
                print(f"✅ Parsed dates using format: {fmt}")
                parsed = True
                break
            except:
                continue
        
        # If all formats fail, try automatic parsing with dayfirst
        if not parsed:
            try:
                df[date_col] = pd.to_datetime(df[date_col], dayfirst=True)
                print(f"✅ Parsed dates using automatic detection (dayfirst=True)")
                parsed = True
            except:
                pass
        
        # Last resort: try without dayfirst
        if not parsed:
            try:
                df[date_col] = pd.to_datetime(df[date_col])
                print(f"✅ Parsed dates using automatic detection")
                parsed = True
            except Exception as e:
                st.error(f"Could not parse dates in {filename}: {str(e)}")
                st.info(f"Sample date values: {df[date_col].head(3).tolist()}")
                return None
        
        # Debug: Print date range
        print(f"📅 {os.path.basename(filename)} - Date range: {df[date_col].min()} to {df[date_col].max()}")
        print(f"First 3 dates: {df[date_col].head(3).tolist()}")
        
        # Standardize columns
        result_df = pd.DataFrame({
            'Date': df[date_col],
            'T2M': df[actual_col],
            pred_col: df[pred_col]
        })
        
        result_df = result_df.sort_values('Date').reset_index(drop=True)
        
        # Validate date range
        if result_df['Date'].isnull().any():
            st.warning(f"Some dates could not be parsed in {filename}")
            result_df = result_df.dropna(subset=['Date'])
        
        return result_df
        
    except Exception as e:
        st.error(f"Error loading {filename}: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None


def get_ncmrwf_algorithm_data(algorithm_type, algorithm_name, algorithms_dict):
    """Get NCMRWF data for specific algorithm"""
    try:
        if algorithm_name not in algorithms_dict:
            st.error(f"Algorithm '{algorithm_name}' not available")
            return None
        
        algo_config = algorithms_dict[algorithm_name]
        filename = algo_config['file']
        
        if not filename:
            st.error(f"No file mapping for {algorithm_name}")
            return None
        
        pred_col = algo_config.get('pred_col')
        actual_col = algo_config.get('actual_col')
        
        if not pred_col or not actual_col:
            st.error(f"Column names not configured for {algorithm_name}")
            return None
        
        data = load_ncmrwf_data(filename, pred_col, actual_col)
        
        if data is not None:
            st.success(f"✅ Loaded {len(data)} data points from {os.path.basename(filename)}")
            # Show date range in success message
            st.info(f"📅 Date Range: {data['Date'].min().strftime('%Y-%m-%d')} to {data['Date'].max().strftime('%Y-%m-%d')}")
        
        return data
        
    except Exception as e:
        st.error(f"Error loading NCMRWF data: {str(e)}")
        import traceback
        # print(traceback.format_exc())
        return None


# def test_date_formats():
#     """Test function to check which date format works for your data"""
#     test_dates = [
#         "11-08-2024",  # DD-MM-YYYY
#         "08-11-24",    # MM-DD-YY
#     ]
    
#     formats = {
#         '%d-%m-%Y': 'DD-MM-YYYY',
#         '%m-%d-%y': 'MM-DD-YY',
#         '%m-%d-%Y': 'MM-DD-YYYY',
#         '%d-%m-%y': 'DD-MM-YY',
#     }
    
#     # print("\n" + "="*60)
#     # print("DATE FORMAT TESTING")
#     # print("="*60)
    
#     for date_str in test_dates:
#         print(f"\nTesting: '{date_str}'")
#         for fmt, name in formats.items():
#             try:
#                 result = pd.to_datetime(date_str, format=fmt)
#                 # print(f"  ✅ {name:12} ({fmt:10}) → {result.strftime('%Y-%m-%d')}")
#             except:
#                 print(f"  ❌ {name:12} ({fmt:10}) → Failed")
    
#     # print("="*60 + "\n")