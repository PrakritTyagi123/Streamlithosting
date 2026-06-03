# ui/components.py
"""
Reusable UI components
"""
import streamlit as st
from config.constants import CLASSICAL_ALGORITHMS, QUANTUM_ALGORITHMS, ALGORITHM_SHORT_NAMES
from data.loader import get_available_dates
from data.processor import get_algorithm_data_with_dates
from visualization.charts import (
    create_temperature_prediction_chart, 
    create_training_params_chart,
    get_training_params_data
)
import logging

logging.basicConfig(level=logging.INFO)

def render_configuration_section(tab_prefix="", data_source="temperature"):
    """
    Render the configuration section and return selected values
    tab_prefix: string to make keys unique per tab (e.g., "temp_", "rain_")
    data_source: "temperature" or "rainfall" - determines which CSV to read dates from
    """
    st.markdown("### Configuration")
    
    config_col1, config_col2, config_col3, config_col4, config_col5, config_col6 = st.columns([0.8, 0.8, 0.8, 0.8, 2, 2])
    
    with config_col1:
        # Get dates based on data source
        if data_source == "rainfall":
            from data.loader import get_available_rainfall_dates
            available_dates = get_available_rainfall_dates()
            data_label = "Rainfall"
        else:  # temperature
            sample_file = "files/SVM_forecast.csv"
            available_dates = get_available_dates(sample_file)
            data_label = "Temperature"
        
        if not available_dates:
            st.error(f"No dates available for {data_label} data. Please check your data files.")
            st.stop()
        
        min_date = min(available_dates)
        max_date = max(available_dates)
        
        start_date = st.date_input(
            "Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            key=f"{tab_prefix}start_date_select"
        )
    
    with config_col2:
        # Use same dates as col1
        end_date = st.date_input(
            "End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            key=f"{tab_prefix}end_date_select"
        )
    
    with config_col3:
        time_intervals = ["1 Hour", "3 Hours", "6 Hours", "12 Hours", "24 Hours"]
        time_interval = st.selectbox(
            "Time Interval",
            time_intervals,
            key=f"{tab_prefix}time_interval_select",
            help="Select data sampling frequency"
        )
    
    with config_col4:
        from config.constants import CITIES
        city = st.selectbox(
            "Location", 
            list(CITIES.keys()), 
            key=f"{tab_prefix}location_select"
        )
    
    with config_col5:
        classical_algo = st.selectbox(
            "Classical Algorithm",
            list(CLASSICAL_ALGORITHMS.keys()),
            key=f"{tab_prefix}classical_select",
            index=0
        )
    
    with config_col6:
        quantum_algo = st.selectbox(
            "Quantum Algorithm",
            list(QUANTUM_ALGORITHMS.keys()),
            key=f"{tab_prefix}quantum_select",
            index=0
        )
    
    # Validation
    if start_date > end_date:
        st.error("Start date must be before or equal to end date!")
        st.stop()
    
    days_diff = (end_date - start_date).days + 1
    
    # Show appropriate message based on data source
    if data_source == "rainfall":
        st.info(f"📅 Rainfall data: {days_diff} day(s) from {start_date} to {end_date}")
    else:
        st.info(f"Selected range: {days_diff} day(s) from {start_date} to {end_date}")
    
    if days_diff == 1 and time_interval == "24 Hours":
        st.error("Cannot display single day with 24-hour interval (only 1 data point).")
        st.warning("Choose a time interval less than 24 hours, OR")
        st.warning("Select a date range of at least 2 days")
        st.stop()
    
    return start_date, end_date, time_interval, city, classical_algo, quantum_algo



def render_algorithm_selection():
    """Render algorithm selection dropdowns"""
    # Get values from session state if they exist
    classical_algo = st.session_state.get('classical_select', list(CLASSICAL_ALGORITHMS.keys())[0])
    quantum_algo = st.session_state.get('quantum_select', list(QUANTUM_ALGORITHMS.keys())[0])
    # logging.info(f"SESSION STATE → {st.session_state}")
    return classical_algo, quantum_algo


def render_prediction_column(algo_type, algorithm_name, start_date, end_date, time_interval):
    """Render a single prediction column (classical or quantum)"""
    title = "Classical Algorithm" if algo_type == 'classical' else "Quantum Algorithm"
    color = '#007bff' if algo_type == 'classical' else '#6f42c1'
    button_key = f"{algo_type}_forecast"
    
    st.markdown(f"#### {title}")
    
    if st.button(f"Generate {title.split()[0]}", key=button_key, use_container_width=True):
        default_name = f"Select {title.split()[0]} Algorithm"
        if algorithm_name == default_name:
            st.error(f"Please select a {algo_type} algorithm first!")
        else:
            with st.spinner(f"Loading..."):
                short_name = ALGORITHM_SHORT_NAMES.get(algorithm_name, algorithm_name)
                
                data = get_algorithm_data_with_dates(
                    algo_type, algorithm_name, start_date, end_date, time_interval
                )
                
                if data is not None:
                    pred_col = [col for col in data.columns if col not in ['Datetime', 'T2M']][0]
                    
                    state_key = f'{algo_type}_data'
                    st.session_state[state_key] = {
                        'data': data,
                        'algorithm': short_name,
                        'prediction_column': pred_col,
                        'time_interval': time_interval,
                        'start_date': start_date,
                        'end_date': end_date,
                        'prediction': data[pred_col].iloc[-1],
                        'actual_temp': data['T2M'].iloc[-1],
                        'last_datetime': data['Datetime'].iloc[-1]
                    }
                    st.session_state[f'last_{algo_type}_algo'] = short_name
                else:
                    st.error("Could not load data")
    
    # Display existing prediction if available
    state_key = f'{algo_type}_data'
    if st.session_state.get(state_key):
        pred = st.session_state[state_key]
        data = pred['data']
        stored_algo_name = pred['algorithm']
        
        pred_col = pred.get('prediction_column')
        if pred_col is None:
            pred_col = [col for col in data.columns if col not in ['Datetime', 'T2M']][0]
        
        # Calculate all values BEFORE the HTML string
        difference = pred['prediction'] - pred['actual_temp']  
        diff_color = '#ef4444' if difference < 0 else '#10b981'
        diff_bg = '#fef2f2' if difference < 0 else '#ecfdf5'
        diff_arrow = '↓' if difference < 0 else '↑'
        date_str = pred['last_datetime'].strftime('%d %B %Y, %H:%M')
        pred_temp = f"{pred['prediction']:.1f}"
        actual_temp = f"{pred['actual_temp']:.1f}"
        diff_value = f"{abs(difference):.1f}"
        
        # Enhanced metric card with both predicted and actual
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border: 2px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05); margin-bottom: 1rem;">
            <div style="margin-bottom: 1rem;">
                <p style="color: #000000; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; margin: 0;">
                    {stored_algo_name}
                </p>
                <p style="color: #000000; font-size: 0.75rem; margin: 0.3rem 0 0 0;">
                    📅 {date_str}
                </p>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6;">
                    <p style="color: #3b82f6; font-size: 0.75rem; font-weight: 600; margin: 0; letter-spacing: 0.5px;">
                        PREDICTED
                    </p>
                    <p style="color: #1e40af; font-size: 1.8rem; font-weight: 800; margin: 0.3rem 0 0 0; line-height: 1;">
                        {pred_temp}°C
                    </p>
                </div>
                <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); padding: 1rem; border-radius: 8px; border-left: 4px solid #059669;">
                    <p style="color: #059669; font-size: 0.75rem; font-weight: 600; margin: 0; letter-spacing: 0.5px;">
                        ACTUAL
                    </p>
                    <p style="color: #065f46; font-size: 1.8rem; font-weight: 800; margin: 0.3rem 0 0 0; line-height: 1;">
                        {actual_temp}°C
                    </p>
                </div>
            </div>
            <div style="padding: 0.75rem; background:#f5f5f5 ; border-radius: 8px; border-left: 4px solid #9ca3af;">
                <p style="color:#4b5563 ; font-size: 0.85rem; font-weight: 600; margin: 0; text-align: center;">
                    {diff_arrow} {diff_value}°C <span style="font-weight: 400; opacity: 0.8;"></span>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        fig = create_temperature_prediction_chart(
            data, stored_algo_name, pred_col, color, algo_type
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"Click 'Generate {title.split()[0]}' button")


# def render_training_params_section():
#     """Render training parameters section"""
#     st.markdown("#### Training Parameters")
    
#     algorithms, classical_params, quantum_params, colors, notes = get_training_params_data()
    
#     if not algorithms:
#         st.info("Generate predictions to see training parameters for selected algorithms.")
#         return

#     # ✅ ADD THIS: Check for kernel methods and show info box
#     kernel_methods = []
#     for algo, note in zip(algorithms, notes):
#         if note and 'Kernel-based' in note:
#             # Extract algorithm name (remove "Classical\n" or "Quantum\n" prefix)
#             algo_name = algo.split('\n')[-1].strip('()')
#             kernel_methods.append(algo_name)
    
#     # ✅ ADD THIS: Show info box if kernel methods are present
#     if kernel_methods:
#         st.info(f"""
#         ℹ️ **{', '.join(kernel_methods)}**: Kernel-based methods don't use traditional 
#         trainable parameters. They rely on support vectors and kernel functions instead.
#         """)
#     fig = create_training_params_chart(algorithms, classical_params, quantum_params, colors, notes)
#     if fig:
#         st.plotly_chart(fig, use_container_width=True)
#         # ✅ ADD THIS: Show helpful caption only for non-kernel algorithms
#         param_algos = [a for a, n in zip(algorithms, notes) 
#                       if not (n and 'Kernel-based' in n)]
#         if param_algos:
#             st.caption("💡 Fewer parameters = faster training but potentially less expressiveness")
def render_training_params_section():
    """Render training parameters section"""
    st.markdown("#### Training Parameters")
    
    algorithms, classical_params, quantum_params, colors, notes = get_training_params_data()
    
    if not algorithms:
        st.info("Generate predictions to see training parameters for selected algorithms.")
        return
    
    # ✅ SEPARATE KERNEL METHODS FROM PARAMETER-BASED ALGORITHMS
    kernel_methods = []
    param_based_algos = []
    param_based_classical = []
    param_based_quantum = []
    param_based_colors = []
    param_based_notes = []
    
    for algo, c_param, q_param, color, note in zip(algorithms, classical_params, quantum_params, colors, notes):
        if note and 'Kernel-based' in note:
            # Extract algorithm name (remove "Classical\n" or "Quantum\n" prefix)
            algo_name = algo.split('\n')[-1].strip('()')
            kernel_methods.append(algo_name)
        else:
            # Keep only algorithms with trainable parameters
            param_based_algos.append(algo)
            param_based_classical.append(c_param)
            param_based_quantum.append(q_param)
            param_based_colors.append(color)
            param_based_notes.append(note)
    
    # ✅ SHOW INFO BOX FOR KERNEL METHODS (NO CHART)
    if kernel_methods:
        st.info(f"""
        ℹ️ **{', '.join(kernel_methods)}**: Kernel-based method with **no trainable parameters**.  
        Uses support vectors and kernel functions instead of gradient-based learning.
        """)
    
    # ✅ SHOW CHART ONLY FOR PARAMETER-BASED ALGORITHMS
    if param_based_algos:
        fig = create_training_params_chart(
            param_based_algos, 
            param_based_classical, 
            param_based_quantum, 
            param_based_colors, 
            param_based_notes
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            # st.caption("💡 Fewer parameters = faster training but potentially less expressiveness")
    elif not kernel_methods:
        # Only show this if no algorithms selected at all
        st.info("Generate predictions to see training parameters for selected algorithms.")

# @st.fragment
# def render_temperature_config_and_graph_fragment(classical_algo, quantum_algo, 
#                                                   classical_algo_short, quantum_algo_short):
#     """
#     ✅ FIXED: Config + Graph in ONE fragment for seamless real-time updates
#     Fragment reruns when inputs change WITHOUT triggering full page reload
#     """
#     # st.markdown("---")
#     st.markdown("### 📅 Configuration")
    
#     # Get available dates
#     sample_file = "files/SVM_forecast.csv"
#     available_dates = get_available_dates(sample_file)
    
#     if not available_dates:
#         st.error("No dates available. Please check your data files.")
#         st.stop()
    
#     min_date = min(available_dates)
#     max_date = max(available_dates)
    
#     # Initialize defaults ONCE (prevents widget resets)
#     if 'temp_generation_start_date' not in st.session_state:
#         st.session_state.temp_generation_start_date = max_date - datetime.timedelta(days=6)
#     if 'temp_generation_end_date' not in st.session_state:
#         st.session_state.temp_generation_end_date = max_date
#     if 'temp_generation_interval' not in st.session_state:
#         st.session_state.temp_generation_interval = "1 Hour"
#     if 'temp_generation_city' not in st.session_state:
#         st.session_state.temp_generation_city = "Delhi"
    
#     # 4-column layout for inputs
#     config_col1, config_col2, config_col3, config_col4 = st.columns(4)
    
#     with config_col1:
#         start_date = st.date_input(
#             "Start Date",
#             value=st.session_state.temp_generation_start_date,
#             min_value=min_date,
#             max_value=max_date,
#             key="temp_start_date_input" # 💡 Unique key prevents widget ID conflicts
#         )
    
#     with config_col2:
#         end_date = st.date_input(
#             "End Date",
#             value=st.session_state.temp_generation_end_date,
#             min_value=min_date,
#             max_value=max_date,
#             key="temp_end_date_input" # 💡 Unique key
#         )
    
#     with config_col3:
#         time_intervals = ["1 Hour", "3 Hours", "6 Hours", "12 Hours", "24 Hours"]
#         time_interval = st.selectbox(
#             "Time Interval",
#             time_intervals, 
#             index=time_intervals.index(st.session_state.temp_generation_interval),
#             key="temp_time_interval_input", # 💡 Unique key
#             help="Select data sampling frequency"
#         )
    
#     with config_col4:
#         from config.constants import CITIES
#         city = st.selectbox(
#             "Location", 
#             list(CITIES.keys()),
#             index=list(CITIES.keys()).index(st.session_state.temp_generation_city),
#             key="temp_location_input"
#         )
    
#     # Validation
#     if start_date > end_date:
#         st.error("Start date must be before or equal to end date!")
#         return
    
#     days_diff = (end_date - start_date).days + 1
#     st.info(f"📅 Selected range: {days_diff} day(s) from {start_date} to {end_date}")
    
#     if days_diff == 1 and time_interval == "24 Hours":
#         st.error("Cannot display single day with 24-hour interval.")
#         st.warning("Choose a time interval less than 24 hours, OR select a date range of at least 2 days")
#         return
    
#     # Check if config changed
#     config_changed = (
#         st.session_state.temp_generation_start_date != start_date or
#         st.session_state.temp_generation_end_date != end_date or
#         st.session_state.temp_generation_interval != time_interval or
#         st.session_state.temp_generation_city != city
#     )
#     # âœ… KEY FIX: Load new data SILENTLY without showing loading message
#     if config_changed:
#         from data.processor import get_algorithm_data_with_dates
        
#         # Load classical data with new config (NO spinner, NO info message)
#         classical_data = get_algorithm_data_with_dates(
#             'classical', classical_algo, start_date, end_date, time_interval
#         )
        
#         # Load quantum data with new config
#         quantum_data = get_algorithm_data_with_dates(
#             'quantum', quantum_algo, start_date, end_date, time_interval
#         )
        
#         if classical_data is not None and quantum_data is not None:
#             # Get prediction columns
#             classical_pred_col = [col for col in classical_data.columns if col not in ['Datetime', 'T2M']][0]
#             quantum_pred_col = [col for col in quantum_data.columns if col not in ['Datetime', 'T2M']][0]
            
#             # Update session state with new data
#             st.session_state.classical_data = {
#                 'data': classical_data,
#                 'algorithm': classical_algo_short,
#                 'prediction_column': classical_pred_col,
#                 'time_interval': time_interval,
#                 'start_date': start_date,
#                 'end_date': end_date,
#                 'prediction': classical_data[classical_pred_col].iloc[-1],
#                 'actual_temp': classical_data['T2M'].iloc[-1],
#                 'last_datetime': classical_data['Datetime'].iloc[-1]
#             }
            
#             st.session_state.quantum_data = {
#                 'data': quantum_data,
#                 'algorithm': quantum_algo_short,
#                 'prediction_column': quantum_pred_col,
#                 'time_interval': time_interval,
#                 'start_date': start_date,
#                 'end_date': end_date,
#                 'prediction': quantum_data[quantum_pred_col].iloc[-1],
#                 'actual_temp': quantum_data['T2M'].iloc[-1],
#                 'last_datetime': quantum_data['Datetime'].iloc[-1]
#             }
            
#             # Update stored configuration
#             st.session_state.temp_generation_start_date = start_date
#             st.session_state.temp_generation_end_date = end_date
#             st.session_state.temp_generation_interval = time_interval
#             st.session_state.temp_generation_city = city
            
#             st.success("✅ Configuration updated!")
#         else:
#             st.error("❌ Could not load data with new configuration")
#             return
    
#     # ==================== RENDER THE GRAPH (directly, no placeholder tricks) ====================
#     st.markdown("---")
#     st.markdown("### 📈  Combined Prediction Comparison")

#     if (st.session_state.get('classical_data') and 
#         st.session_state.get('quantum_data')):
        
#         classical_data = st.session_state.classical_data['data']
#         quantum_data = st.session_state.quantum_data['data']
#         classical_pred_col = st.session_state.classical_data['prediction_column']
#         quantum_pred_col = st.session_state.quantum_data['prediction_column']
        
#         from utils.helpers import get_chart_title_with_dates
#         chart_title = (
#             "Classical vs Quantum Comparison - " +
#             get_chart_title_with_dates(
#                 st.session_state.temp_generation_interval,
#                 st.session_state.temp_generation_start_date,
#                 st.session_state.temp_generation_end_date
#             )
#         )
        
#         from visualization.charts import create_combined_prediction_chart
#         fig_combined = create_combined_prediction_chart(
#             classical_data, quantum_data,
#             st.session_state.classical_data["algorithm"],
#             st.session_state.quantum_data["algorithm"],
#             classical_pred_col, quantum_pred_col,
#             chart_title
#         )
        
#         # âœ… Graph updates smoothly - fragment reruns entire content at once
#         st.plotly_chart(fig_combined, use_container_width=True, key=f"temp_graph_{time_interval}_{start_date}_{end_date}")
#     else:
#         st.info("📊 Generate predictions first to view the comparison graph")
@st.fragment
def render_temperature_config_and_graph_fragment(classical_algo, quantum_algo, 
                                                  classical_algo_short, quantum_algo_short):
    """
    ✅ FIXED: Config + Graph in ONE fragment for seamless real-time updates
    Fragment reruns when inputs change WITHOUT triggering full page reload
    
    🔧 FIX: Removed initialization checks that caused double-click issue
    """
    from datetime import timedelta
    
    st.markdown("### 📅 Configuration")
    
    # Get available dates
    sample_file = "files/SVM_forecast.csv"
    available_dates = get_available_dates(sample_file)
    
    if not available_dates:
        st.error("No dates available. Please check your data files.")
        st.stop()
    
    min_date = min(available_dates)
    max_date = max(available_dates)
    
    # ✅ FIX: Initialize defaults ONLY if they don't exist
    # Don't re-check them during fragment reruns
    if 'temp_generation_start_date' not in st.session_state:
        st.session_state.temp_generation_start_date = max_date - timedelta(days=6)
        st.session_state.temp_generation_end_date = max_date
        st.session_state.temp_generation_interval = "1 Hour"
        st.session_state.temp_generation_city = "Delhi"
    
    # 4-column layout for inputs
    config_col1, config_col2, config_col3, config_col4 = st.columns(4)
    
    with config_col1:
        start_date = st.date_input(
            "Start Date",
            value=st.session_state.temp_generation_start_date,
            min_value=min_date,
            max_value=max_date,
            key="temp_start_date_input"
        )
    
    with config_col2:
        end_date = st.date_input(
            "End Date",
            value=st.session_state.temp_generation_end_date,
            min_value=min_date,
            max_value=max_date,
            key="temp_end_date_input"
        )
    
    with config_col3:
        time_intervals = ["1 Hour", "3 Hours", "6 Hours", "12 Hours", "24 Hours"]
        
        # ✅ KEY FIX: Read CURRENT widget value directly, not stored value
        # Use the widget's key to get the latest value
        time_interval = st.selectbox(
            "Time Interval",
            time_intervals, 
            index=time_intervals.index(st.session_state.get("temp_time_interval_input", st.session_state.temp_generation_interval)),
            key="temp_time_interval_input",
            help="Select data sampling frequency"
        )
    
    with config_col4:
        from config.constants import CITIES
        city = st.selectbox(
            "Location", 
            list(CITIES.keys()),
            index=list(CITIES.keys()).index(st.session_state.temp_generation_city),
            key="temp_location_input"
        )
    
    # Validation
    if start_date > end_date:
        st.error("Start date must be before or equal to end date!")
        return
    
    days_diff = (end_date - start_date).days + 1
    st.info(f"📅 Selected range: {days_diff} day(s) from {start_date} to {end_date}")
    
    if days_diff == 1 and time_interval == "24 Hours":
        st.error("Cannot display single day with 24-hour interval.")
        st.warning("Choose a time interval less than 24 hours, OR select a date range of at least 2 days")
        return
    
    # ✅ FIX: Check if config changed using CURRENT widget values
    config_changed = (
        st.session_state.temp_generation_start_date != start_date or
        st.session_state.temp_generation_end_date != end_date or
        st.session_state.temp_generation_interval != time_interval or
        st.session_state.temp_generation_city != city
    )
    
    # Load new data SILENTLY when config changes
    if config_changed:
        from data.processor import get_algorithm_data_with_dates
        
        # Load classical data with new config
        classical_data = get_algorithm_data_with_dates(
            'classical', classical_algo, start_date, end_date, time_interval
        )
        
        # Load quantum data with new config
        quantum_data = get_algorithm_data_with_dates(
            'quantum', quantum_algo, start_date, end_date, time_interval
        )
        
        if classical_data is not None and quantum_data is not None:
            # Get prediction columns
            classical_pred_col = [col for col in classical_data.columns if col not in ['Datetime', 'T2M']][0]
            quantum_pred_col = [col for col in quantum_data.columns if col not in ['Datetime', 'T2M']][0]
            
            # Update session state with new data
            st.session_state.classical_data = {
                'data': classical_data,
                'algorithm': classical_algo_short,
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
                'prediction_column': quantum_pred_col,
                'time_interval': time_interval,
                'start_date': start_date,
                'end_date': end_date,
                'prediction': quantum_data[quantum_pred_col].iloc[-1],
                'actual_temp': quantum_data['T2M'].iloc[-1],
                'last_datetime': quantum_data['Datetime'].iloc[-1]
            }
            
            # ✅ FIX: Update stored configuration AFTER successful data load
            st.session_state.temp_generation_start_date = start_date
            st.session_state.temp_generation_end_date = end_date
            st.session_state.temp_generation_interval = time_interval
            st.session_state.temp_generation_city = city
            
            st.success("✅ Configuration updated!")
        else:
            st.error("❌ Could not load data with new configuration")
            return
    
    # ==================== RENDER THE GRAPH ====================
    st.markdown("---")
    st.markdown("### 📈 Combined Prediction Comparison")

    if (st.session_state.get('classical_data') and 
        st.session_state.get('quantum_data')):
        
        classical_data = st.session_state.classical_data['data']
        quantum_data = st.session_state.quantum_data['data']
        classical_pred_col = st.session_state.classical_data['prediction_column']
        quantum_pred_col = st.session_state.quantum_data['prediction_column']
        
        from utils.helpers import get_chart_title_with_dates
        chart_title = (
            "Classical vs Quantum Comparison - " +
            get_chart_title_with_dates(
                time_interval,  # ✅ Use current time_interval
                start_date,     # ✅ Use current start_date
                end_date        # ✅ Use current end_date
            )
        )
        
        from visualization.charts import create_combined_prediction_chart
        fig_combined = create_combined_prediction_chart(
            classical_data, quantum_data,
            st.session_state.classical_data["algorithm"],
            st.session_state.quantum_data["algorithm"],
            classical_pred_col, quantum_pred_col,
            chart_title
        )
        
        # ✅ Graph updates smoothly
        st.plotly_chart(fig_combined, use_container_width=True, 
                       key=f"temp_graph_{time_interval}_{start_date}_{end_date}")
    else:
        st.info("📊 Generate predictions first to view the comparison graph")
    
    
   