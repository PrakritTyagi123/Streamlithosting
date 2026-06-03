# ui/noise_components.py - FIXED VERSION
"""
Fixed Noise Analysis Components
✅ Resolves double-click issue with time interval
✅ Now matches the working temperature tab pattern
"""
import streamlit as st
from datetime import timedelta
from config.constants import NOISE_QUANTUM_ALGORITHMS, NOISE_TYPES


def render_temperature_noise_section():
    """Render noise analysis section for temperature predictions"""
    
    st.markdown("### 🔬 Quantum Noise Analysis")
    st.info("Compare quantum algorithms under different noise conditions")
    
    # Algorithm selection
    col1, col2 = st.columns(2)
    
    algo_options = list(NOISE_QUANTUM_ALGORITHMS.keys())
    
    with col1:
        st.markdown("**⚛️ Left Quantum Algorithm**")
        left_algo = st.selectbox(
            "Select left algorithm",
            algo_options,
            key="temp_noise_left_algo"
        )
    
    with col2:
        st.markdown("**⚛️ Right Quantum Algorithm**")
        right_algo = st.selectbox(
            "Select right algorithm",
            algo_options,
            key="temp_noise_right_algo"
        )
    
    # Get short names
    left_algo_short = NOISE_QUANTUM_ALGORITHMS.get(left_algo, {}).get('short_name', '')
    right_algo_short = NOISE_QUANTUM_ALGORITHMS.get(right_algo, {}).get('short_name', '')
    
    # Noise parameter selection
    st.markdown("### ⚙️ Noise Parameters")
    col_noise1, col_noise2 = st.columns(2)
    
    with col_noise1:
        noise_type_left = st.selectbox(
            "Noise Type (Left)",
            NOISE_TYPES,
            key="temp_noise_type_left"
        )
    
    with col_noise2:
        # Only disable same noise type if SAME ALGORITHM is selected
        if left_algo == right_algo and left_algo != "Select Quantum Algorithm":
            right_noise_options = [nt for nt in NOISE_TYPES if nt != noise_type_left]
            if not right_noise_options:
                right_noise_options = NOISE_TYPES
        else:
            right_noise_options = NOISE_TYPES
        
        noise_type_right = st.selectbox(
            "Noise Type (Right)",
            right_noise_options,
            key="temp_noise_type_right"
        )
    
    st.markdown("---")
    
    # Check if both algorithms are selected
    both_selected = (
        left_algo != "Select Quantum Algorithm" and 
        right_algo != "Select Quantum Algorithm"
    )
    
    # Check for invalid same algorithm + same noise type combination
    same_combo_selected = (
        left_algo == right_algo and 
        noise_type_left == noise_type_right and
        left_algo != "Select Quantum Algorithm"
    )
    
    if same_combo_selected:
        st.error("❌ Cannot compare the same algorithm with the same noise type. Please select different noise types.")
        return
    
    if both_selected:
        # Show informative message
        if left_algo == right_algo:
            st.info(f"📌 Comparing **{left_algo_short}** with different noise conditions:\n\n"
                   f"**Left**: {noise_type_left} | **Right**: {noise_type_right}")
        else:
            st.info(f"📌 Comparing different algorithms:\n\n"
                   f"**Left**: {left_algo_short} ({noise_type_left}) | **Right**: {right_algo_short} ({noise_type_right})")
        
        # Generate button
        if st.button("🎯 GENERATE NOISE COMPARISON", key="gen_temp_noise", type="primary"):
            if left_algo == "Select Quantum Algorithm" or right_algo == "Select Quantum Algorithm":
                st.error("❌ Please select valid algorithms for both left and right sides")
                return
            
            from data.loader import get_available_dates
            sample_file = "files/SVM_forecast.csv"
            available_dates = get_available_dates(sample_file)
            
            if not available_dates:
                st.error("No dates available.")
                st.stop()
            
            min_date = min(available_dates)
            max_date = max(available_dates)
            default_end = max_date
            default_start = max_date - timedelta(days=6)
            
            if 'temp_noise_start_date' not in st.session_state:
                st.session_state.temp_noise_start_date = default_start
                st.session_state.temp_noise_end_date = default_end
                st.session_state.temp_noise_interval = "1 Hour"
            
            start_date = st.session_state.temp_noise_start_date
            end_date = st.session_state.temp_noise_end_date
            time_interval = st.session_state.temp_noise_interval
            
            with st.spinner(f"Loading predictions..."):
                from data.noise_loader import get_noise_algorithm_data
                
                left_data = get_noise_algorithm_data(
                    left_algo,
                    noise_type_left, 
                    start_date, 
                    end_date, 
                    time_interval
                )
                
                right_data = get_noise_algorithm_data(
                    right_algo,
                    noise_type_right, 
                    start_date, 
                    end_date, 
                    time_interval
                )
                
                if left_data is not None and right_data is not None:
                    left_pred_col = [col for col in left_data.columns if col not in ['Datetime', 'T2M']][0]
                    right_pred_col = [col for col in right_data.columns if col not in ['Datetime', 'T2M']][0]
                    
                    st.session_state.noise_left_data = {
                        'data': left_data,
                        'algorithm': left_algo_short,
                        'prediction_column': left_pred_col,
                        'noise_type': noise_type_left,
                        'time_interval': time_interval,
                        'start_date': start_date,
                        'end_date': end_date,
                        'prediction': left_data[left_pred_col].iloc[-1],
                        'actual_temp': left_data['T2M'].iloc[-1],
                        'last_datetime': left_data['Datetime'].iloc[-1]
                    }
                    
                    st.session_state.noise_right_data = {
                        'data': right_data,
                        'algorithm': right_algo_short,
                        'prediction_column': right_pred_col,
                        'noise_type': noise_type_right,
                        'time_interval': time_interval,
                        'start_date': start_date,
                        'end_date': end_date,
                        'prediction': right_data[right_pred_col].iloc[-1],
                        'actual_temp': right_data['T2M'].iloc[-1],
                        'last_datetime': right_data['Datetime'].iloc[-1]
                    }
                    
                    st.session_state.temp_noise_generated = True
                    st.success("✅ Noise predictions loaded!")
                    st.rerun()
                else:
                    st.error("❌ Could not load data")
    else:
        missing = []
        if left_algo == "Select Quantum Algorithm":
            missing.append("Left Algorithm")
        if right_algo == "Select Quantum Algorithm":
            missing.append("Right Algorithm")
        
        st.warning(f"⚠️ Please select: {' and '.join(missing)}")
    
    # Show config + graph if generated
    if st.session_state.get('temp_noise_generated', False):
        st.session_state.temp_noise_left_algo_full = left_algo
        st.session_state.temp_noise_right_algo_full = right_algo
        
        render_noise_config_and_graph_fragment(
            left_algo, right_algo,
            left_algo_short, right_algo_short
        )


@st.fragment
def render_noise_config_and_graph_fragment(left_algo, right_algo, 
                                            left_algo_short, right_algo_short):
    """
    ✅ FIXED Fragment - Resolves double-click issue
    Key fix: Read CURRENT widget value instead of stored session state
    """
    st.markdown("---")
    st.markdown("### 📅 Configuration")
    
    from data.loader import get_available_dates
    sample_file = "files/SVM_forecast.csv"
    available_dates = get_available_dates(sample_file)
    
    if not available_dates:
        st.error("No dates available")
        return
    
    min_date = min(available_dates)
    max_date = max(available_dates)
    
    # ✅ Initialize defaults ONLY if they don't exist
    if 'temp_noise_start_date' not in st.session_state:
        st.session_state.temp_noise_start_date = max_date - timedelta(days=6)
        st.session_state.temp_noise_end_date = max_date
        st.session_state.temp_noise_interval = "1 Hour"
    
    config_col1, config_col2, config_col3 = st.columns(3)
    
    with config_col1:
        start_date = st.date_input(
            "Start Date",
            value=st.session_state.temp_noise_start_date,
            min_value=min_date,
            max_value=max_date,
            key="temp_noise_start_input"
        )
    
    with config_col2:
        end_date = st.date_input(
            "End Date",
            value=st.session_state.temp_noise_end_date,
            min_value=min_date,
            max_value=max_date,
            key="temp_noise_end_input"
        )
    
    with config_col3:
        time_intervals = ["1 Hour", "3 Hours", "6 Hours", "12 Hours", "24 Hours"]
        
        # ✅ KEY FIX: Use widget key to get CURRENT value, not stored session state
        # This prevents the one-step delay that required double-clicking
        current_interval = st.session_state.get(
            "temp_noise_interval_input",  # Read from widget's key first
            st.session_state.temp_noise_interval  # Fallback to stored value
        )
        
        time_interval = st.selectbox(
            "Time Interval",
            time_intervals,
            index=time_intervals.index(current_interval),  # ✅ Use current value
            key="temp_noise_interval_input"
        )
    
    if start_date > end_date:
        st.error("Start date must be before or equal to end date!")
        return
    
    days_diff = (end_date - start_date).days + 1
    st.info(f"📅 Selected range: {days_diff} day(s)")
    
    if days_diff == 1 and time_interval == "24 Hours":
        st.error("Cannot display single day with 24-hour interval.")
        return
    
    # ✅ Detect configuration changes using CURRENT widget values
    config_changed = (
        st.session_state.temp_noise_start_date != start_date or
        st.session_state.temp_noise_end_date != end_date or
        st.session_state.temp_noise_interval != time_interval
    )
    
    # Auto-update when config changes (no button needed)
    if config_changed:
        from data.noise_loader import get_noise_algorithm_data
        
        left_algo_full = st.session_state.get('temp_noise_left_algo_full', left_algo)
        right_algo_full = st.session_state.get('temp_noise_right_algo_full', right_algo)
        
        left_noise_type = st.session_state.noise_left_data['noise_type']
        right_noise_type = st.session_state.noise_right_data['noise_type']
        
        left_data = get_noise_algorithm_data(
            left_algo_full,
            left_noise_type, 
            start_date, 
            end_date, 
            time_interval
        )
        
        right_data = get_noise_algorithm_data(
            right_algo_full,
            right_noise_type, 
            start_date, 
            end_date, 
            time_interval
        )
        
        if left_data is not None and right_data is not None:
            left_pred_col = [col for col in left_data.columns if col not in ['Datetime', 'T2M']][0]
            right_pred_col = [col for col in right_data.columns if col not in ['Datetime', 'T2M']][0]
            
            st.session_state.noise_left_data.update({
                'data': left_data,
                'prediction_column': left_pred_col,
                'time_interval': time_interval,
                'start_date': start_date,
                'end_date': end_date,
                'prediction': left_data[left_pred_col].iloc[-1],
                'actual_temp': left_data['T2M'].iloc[-1],
                'last_datetime': left_data['Datetime'].iloc[-1]
            })
            
            st.session_state.noise_right_data.update({
                'data': right_data,
                'prediction_column': right_pred_col,
                'time_interval': time_interval,
                'start_date': start_date,
                'end_date': end_date,
                'prediction': right_data[right_pred_col].iloc[-1],
                'actual_temp': right_data['T2M'].iloc[-1],
                'last_datetime': right_data['Datetime'].iloc[-1]
            })
            
            # ✅ Update stored configuration AFTER successful data load
            st.session_state.temp_noise_start_date = start_date
            st.session_state.temp_noise_end_date = end_date
            st.session_state.temp_noise_interval = time_interval
            
            # st.success("✅ Configuration updated!")
        else:
            st.error("❌ Could not load data")
            return
    
    # Render graph
    st.markdown("---")
    st.markdown("### 📈 Noise Comparison Graph")
    
    if (st.session_state.get('noise_left_data') and 
        st.session_state.get('noise_right_data')):
        
        left_data = st.session_state.noise_left_data['data']
        right_data = st.session_state.noise_right_data['data']
        left_pred_col = st.session_state.noise_left_data['prediction_column']
        right_pred_col = st.session_state.noise_right_data['prediction_column']
        
        from visualization.charts import create_noise_comparison_chart
        from utils.helpers import get_chart_title_with_dates
        
        left_label = f"{left_algo_short} ({st.session_state.noise_left_data['noise_type']})"
        right_label = f"{right_algo_short} ({st.session_state.noise_right_data['noise_type']})"
        
        chart_title = (
            f"Noise Comparison: {left_label} vs {right_label} - " +
            get_chart_title_with_dates(time_interval, start_date, end_date)
        )
        
        fig = create_noise_comparison_chart(
            left_data, right_data,
            left_label,
            right_label,
            left_pred_col, right_pred_col,
            chart_title
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Metrics table
    st.markdown("---")
    st.markdown("### 📊 Performance Metrics Comparison")
    
    from visualization.tables import create_noise_metrics_table_with_state, create_metrics_table_html
    
    metrics_df, left_header, right_header = create_noise_metrics_table_with_state()
    
    table_html = create_metrics_table_html(left_header, right_header, metrics_df)
    st.markdown(table_html, unsafe_allow_html=True)
    # ==================== QUANTUM RESOURCE ESTIMATES ====================
    st.markdown("---")
    st.markdown("### 🔬 Quantum Resource Estimates")
    
    left_algo = st.session_state.noise_left_data['algorithm']
    right_algo = st.session_state.noise_right_data['algorithm']
    
    if left_algo == right_algo:
        # Same algorithm - show single QRE chart (centered)
        st.markdown(f"#### Quantum Resources - {left_algo}")
        st.info(f"Showing quantum resource estimates for **{left_algo}** (same for both noise types)")
        
        from visualization.charts import create_combined_resource_chart_for_algorithm
        fig = create_combined_resource_chart_for_algorithm(left_algo)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Different algorithms - show two QRE charts side-by-side
        col_qre1, col_qre2 = st.columns(2)
        
        with col_qre1:
            st.markdown(f"#### {left_algo}")
            from visualization.charts import create_combined_resource_chart_for_algorithm
            fig_left = create_combined_resource_chart_for_algorithm(left_algo)
            st.plotly_chart(fig_left, use_container_width=True)
        
        with col_qre2:
            st.markdown(f"#### {right_algo}")
            fig_right = create_combined_resource_chart_for_algorithm(right_algo)
            st.plotly_chart(fig_right, use_container_width=True)


# def render_rain_noise_section():
#     """Render noise analysis section for rainfall predictions"""
#     st.info("🚧 Rainfall noise analysis coming soon...")

####### add thsi code for the rain noise
def render_rain_noise_section():
    """Render noise analysis section for rainfall predictions"""
    
    st.markdown("### 🔬 Quantum Noise Analysis for Rainfall")
    st.info("Compare quantum algorithms for rain prediction under different noise conditions")
    
    from config.constants import RAIN_NOISE_QUANTUM_ALGORITHMS, RAIN_NOISE_TYPES
    
    # Algorithm selection
    col1, col2 = st.columns(2)
    
    algo_options = list(RAIN_NOISE_QUANTUM_ALGORITHMS.keys())
    
    with col1:
        st.markdown("**⚛️ Left Quantum Algorithm**")
        left_algo = st.selectbox(
            "Select left algorithm",
            algo_options,
            key="rain_noise_left_algo"
        )
    
    with col2:
        st.markdown("**⚛️ Right Quantum Algorithm**")
        right_algo = st.selectbox(
            "Select right algorithm",
            algo_options,
            key="rain_noise_right_algo"
        )
    
    # Get short names
    left_algo_short = RAIN_NOISE_QUANTUM_ALGORITHMS.get(left_algo, {}).get('short_name', '')
    right_algo_short = RAIN_NOISE_QUANTUM_ALGORITHMS.get(right_algo, {}).get('short_name', '')
    
    # Noise parameter selection
    st.markdown("### ⚙️ Noise Parameters")
    col_noise1, col_noise2 = st.columns(2)
    
    with col_noise1:
        noise_type_left = st.selectbox(
            "Noise Type (Left)",
            RAIN_NOISE_TYPES,
            key="rain_noise_type_left"
        )
    
    with col_noise2:
        # Prevent same noise type if same algorithm selected
        if left_algo == right_algo and left_algo != "Select Quantum Algorithm":
            right_noise_options = [nt for nt in RAIN_NOISE_TYPES if nt != noise_type_left]
            if not right_noise_options:
                right_noise_options = RAIN_NOISE_TYPES
        else:
            right_noise_options = RAIN_NOISE_TYPES
        
        noise_type_right = st.selectbox(
            "Noise Type (Right)",
            right_noise_options,
            key="rain_noise_type_right"
        )
    
    st.markdown("---")
    
    # Check if both algorithms are selected
    both_selected = (
        left_algo != "Select Quantum Algorithm" and 
        right_algo != "Select Quantum Algorithm"
    )
    
    # Check for invalid same combo
    same_combo_selected = (
        left_algo == right_algo and 
        noise_type_left == noise_type_right and
        left_algo != "Select Quantum Algorithm"
    )
    
    if same_combo_selected:
        st.error("❌ Cannot compare the same algorithm with the same noise type. Please select different noise types.")
        return
    
    if both_selected:
        # Show informative message
        if left_algo == right_algo:
            st.info(f"📌 Comparing **{left_algo_short}** with different noise conditions:\n\n"
                   f"**Left**: {noise_type_left} | **Right**: {noise_type_right}")
        else:
            st.info(f"📌 Comparing different algorithms:\n\n"
                   f"**Left**: {left_algo_short} ({noise_type_left}) | **Right**: {right_algo_short} ({noise_type_right})")
        
        # Generate button
        if st.button("🎯 GENERATE RAIN NOISE COMPARISON", key="gen_rain_noise", type="primary"):
            if left_algo == "Select Quantum Algorithm" or right_algo == "Select Quantum Algorithm":
                st.error("❌ Please select valid algorithms for both left and right sides")
                return
            
            with st.spinner(f"Loading rain noise predictions..."):
                from data.rain_noise_loader import get_rain_noise_algorithm_data, get_rain_noise_metrics
                
                # Load both datasets
                left_data = get_rain_noise_algorithm_data(left_algo, noise_type_left)
                right_data = get_rain_noise_algorithm_data(right_algo, noise_type_right)
                
                if left_data is not None and right_data is not None:
                    left_pred_col = [col for col in left_data.columns if col not in ['Datetime', 'Actual']][0]
                    right_pred_col = [col for col in right_data.columns if col not in ['Datetime', 'Actual']][0]
                    
                    # Get metrics
                    left_metrics = get_rain_noise_metrics(left_algo_short, noise_type_left)
                    right_metrics = get_rain_noise_metrics(right_algo_short, noise_type_right)
                    
                    st.session_state.rain_noise_left_data = {
                        'data': left_data,
                        'algorithm': left_algo_short,
                        'prediction_column': left_pred_col,
                        'noise_type': noise_type_left,
                        'metrics': left_metrics
                    }
                    
                    st.session_state.rain_noise_right_data = {
                        'data': right_data,
                        'algorithm': right_algo_short,
                        'prediction_column': right_pred_col,
                        'noise_type': noise_type_right,
                        'metrics': right_metrics
                    }
                    
                    st.session_state.rain_noise_generated = True
                    st.success("✅ Rain noise predictions loaded!")
                    st.rerun()
                else:
                    st.error("❌ Could not load data")
    else:
        missing = []
        if left_algo == "Select Quantum Algorithm":
            missing.append("Left Algorithm")
        if right_algo == "Select Quantum Algorithm":
            missing.append("Right Algorithm")
        
        st.warning(f"⚠️ Please select: {' and '.join(missing)}")
    
    # Show visualization if generated
    if st.session_state.get('rain_noise_generated', False):
        render_rain_noise_visualization_fragment()


@st.fragment
def render_rain_noise_visualization_fragment():
    """
    Render rain noise visualization with tabs (Single Day & Weekly View)
    """
    st.markdown("---")
    st.markdown("### 📊 Rain Noise Comparison")
    
    if not (st.session_state.get('rain_noise_left_data') and 
            st.session_state.get('rain_noise_right_data')):
        st.info("Generate predictions first")
        return
    
    left_data = st.session_state.rain_noise_left_data['data']
    right_data = st.session_state.rain_noise_right_data['data']
    
    left_algo = st.session_state.rain_noise_left_data['algorithm']
    right_algo = st.session_state.rain_noise_right_data['algorithm']
    
    left_noise = st.session_state.rain_noise_left_data['noise_type']
    right_noise = st.session_state.rain_noise_right_data['noise_type']
    
    left_pred_col = st.session_state.rain_noise_left_data['prediction_column']
    right_pred_col = st.session_state.rain_noise_right_data['prediction_column']
    
    # Create tabs
    tab1, tab2 = st.tabs(["📅 Single Day View", "🗓️ Weekly View"])
    
    with tab1:
        st.markdown("### 🎯 Single Day Controls")
        
        # Show legend
        show_rain_noise_legend()
        
        # Render single day view
        render_rain_noise_single_day_fragment(
            left_data, right_data,
            left_pred_col, right_pred_col,
            left_algo, right_algo,
            left_noise, right_noise
        )
    
    with tab2:
        st.markdown("### 🎯 Weekly View Controls")
        
        show_rain_noise_legend()
        
        render_rain_noise_weekly_view(
            left_data, right_data,
            left_pred_col, right_pred_col,
            left_algo, right_algo,
            left_noise, right_noise
        )
    
    # Show confusion matrices and metrics
    st.markdown("---")
    st.markdown("### 📈 Confusion Matrices Comparison")
    
    col_cm1, col_cm2 = st.columns(2)
    
    with col_cm1:
        st.markdown(f"#### ⚛️ {left_algo} ({left_noise})")
        if st.session_state.rain_noise_left_data.get('metrics'):
            from visualization.charts import create_confusion_matrix_chart
            fig_cm = create_confusion_matrix_chart(
                st.session_state.rain_noise_left_data['metrics'],
                f"{left_algo} ({left_noise})"
            )
            st.plotly_chart(fig_cm, use_container_width=True)
        else:
            st.warning("No metrics available for this noise type")
    
    with col_cm2:
        st.markdown(f"#### ⚛️ {right_algo} ({right_noise})")
        if st.session_state.rain_noise_right_data.get('metrics'):
            from visualization.charts import create_confusion_matrix_chart
            fig_cm = create_confusion_matrix_chart(
                st.session_state.rain_noise_right_data['metrics'],
                f"{right_algo} ({right_noise})"
            )
            st.plotly_chart(fig_cm, use_container_width=True)
        else:
            st.warning("No metrics available for this noise type")
    
    # Metrics table
    st.markdown("---")
    st.markdown("### 📊 Performance Metrics Comparison")
    
    from visualization.tables import create_rain_noise_metrics_table_with_state, create_metrics_table_html
    
    metrics_df, left_header, right_header = create_rain_noise_metrics_table_with_state()
    
    table_html = create_metrics_table_html(left_header, right_header, metrics_df)
    st.markdown(table_html, unsafe_allow_html=True)


def show_rain_noise_legend():
    """Static legend for rain noise visualization"""
    st.markdown("### 📖 Legend")
    legend_cols = st.columns([1, 1, 1, 1.2])
    
    with legend_cols[0]:
        st.markdown("""
        <div style='background: #60a5fa; 
                    padding: 8px; border-radius: 8px; text-align: center;height: 90px; 
                    display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 22px;'>☀️</div>
            <div style='color: white; font-weight: 600; margin-top: 2px; font-size: 15px;'>Clear Day</div>
        </div>
        """, unsafe_allow_html=True)
    
    with legend_cols[1]:
        st.markdown("""
        <div style='background: #1e3a8a; 
                    padding: 8px; border-radius: 8px; text-align: center;height: 90px; 
                    display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 22px;'>🌙</div>
            <div style='color: white; font-weight: 600; margin-top: 2px; font-size: 15px;'>Clear Night</div>
        </div>
        """, unsafe_allow_html=True)
    
    with legend_cols[2]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #10b981 0%, #8b5cf6 50%); 
                    padding: 8px; border-radius: 8px; text-align: center;height: 90px; 
                    display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 22px;'>🌧️</div>
            <div style='color: white; font-weight: 600; margin-top: 2px; font-size: 15px;'>Raining</div>
            <div style='color: white; font-size: 11px; margin-top: 3px;'>Green=Actual, Purple=Algorithms</div>
        </div>
        """, unsafe_allow_html=True)
    
    with legend_cols[3]:
        st.markdown("""
        <div style='background: #f0f2f5; 
                    padding: 8px; border-radius: 8px; text-align: center; border: 2px solid #e5e7eb;
                    height: 90px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='color: #374151; font-weight: 700; font-size: 15px;'>
                <strong>A</strong> = Actual
            </div>
            <div style='color: #374151; font-weight: 700; font-size: 15px; margin-top: 4px;'> 
                <strong>L</strong> = Left Algo
            </div>
            <div style='color: #374151; font-weight: 700; font-size: 15px; margin-top: 4px;'> 
                <strong>R</strong> = Right Algo
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")


@st.fragment
def render_rain_noise_single_day_fragment(left_data, right_data,
                                           left_pred_col, right_pred_col,
                                           left_algo, right_algo,
                                           left_noise, right_noise):
    """Render single day view for rain noise comparison"""
    import pandas as pd
    
    # Prepare data
    dfl = left_data.copy()
    dfr = right_data.copy()
    
    dfl['Datetime'] = pd.to_datetime(dfl['Datetime'], errors='coerce')
    dfr['Datetime'] = pd.to_datetime(dfr['Datetime'], errors='coerce')
    
    dfl['Date'] = dfl['Datetime'].dt.date
    dfr['Date'] = dfr['Datetime'].dt.date
    
    min_date = dfl['Date'].min()
    max_date = dfl['Date'].max()
    
    # Date and interval selection
    col1, col2 = st.columns(2)
    
    with col1:
        selected_date = st.date_input(
            "**Select Date**",
            min_value=min_date,
            max_value=max_date,
            value=max_date,
            key="rain_noise_single_day_date"
        )
    
    with col2:
        time_interval = st.selectbox(
            "**Time Interval**",
            options=["1 Hour", "3 Hours", "6 Hours", "12 Hours", "24 Hours"],
            key="rain_noise_time_interval"
        )
    
    # Build and display timeline
    show_rain_noise_single_day_core(
        dfl, dfr, left_pred_col, right_pred_col,
        left_algo, right_algo, left_noise, right_noise,
        selected_date, time_interval
    )


def show_rain_noise_single_day_core(dfl, dfr, left_pred_col, right_pred_col,
                                      left_algo, right_algo, left_noise, right_noise,
                                      selected_date, time_interval):
    """Core rendering for single day rain noise comparison"""
    import pandas as pd
    
    dfl['Hour'] = dfl['Datetime'].dt.hour
    dfr['Hour'] = dfr['Datetime'].dt.hour
    
    # Filter by date
    day_data_l = dfl[dfl['Date'] == selected_date].sort_values('Hour')
    day_data_r = dfr[dfr['Date'] == selected_date].sort_values('Hour')
    
    # Apply interval filter
    interval_hours = {
        "1 Hour": list(range(24)),
        "3 Hours": [0, 3, 6, 9, 12, 15, 18, 21],
        "6 Hours": [0, 6, 12, 18],
        "12 Hours": [0, 12],
        "24 Hours": [12]
    }
    
    hours_to_show = interval_hours.get(time_interval, list(range(24)))
    day_data_l = day_data_l[day_data_l['Hour'].isin(hours_to_show)]
    day_data_r = day_data_r[day_data_r['Hour'].isin(hours_to_show)]
    
    if len(day_data_l) == 0:
        st.warning("No data for selected date")
        return
    
    # Display header
    day_name = pd.to_datetime(selected_date).strftime('%A')
    date_str = pd.to_datetime(selected_date).strftime('%B %d, %Y')
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
        <h2 style='color: white; margin: 0; text-align: center; font-size: 20px;'>
            {day_name}, {date_str}
        </h2>
        <p style='color: white; margin: 5px 0 0 0; text-align: center; font-size: 15px;'>
            Interval: {time_interval} | Total Hours: {len(hours_to_show)}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🕐 24-Hour Timeline")
    
    # Build 3 timelines: Actual, Left Algorithm, Right Algorithm
    models = [
        {'label': 'A', 'name': 'Actual', 'data': day_data_l, 'pred_col': 'Actual', 'color_rain': '#10b981'},
        {'label': 'L', 'name': f'{left_algo} ({left_noise})', 'data': day_data_l, 'pred_col': left_pred_col, 'color_rain': '#8b5cf6'},
        {'label': 'R', 'name': f'{right_algo} ({right_noise})', 'data': day_data_r, 'pred_col': right_pred_col, 'color_rain': '#6366f1'}
    ]
    
    all_timelines_html = ""
    
    for model in models:
        data = model['data']
        pred_col = model['pred_col']
        
        if len(data) == 0:
            all_timelines_html += f"<p style='color: #f59e0b;'>⚠️ No data for {model['name']}</p>"
            continue
        
        header_text = f"<h4 style='margin-top: 20px; color: #1f2937;'>{model['label']} - {model['name']}</h4>"
        
        all_timelines_html += header_text
        all_timelines_html += build_rain_timeline_html(data, pred_col, model, hours_to_show)
        all_timelines_html += "<br>"
    
    st.markdown(all_timelines_html, unsafe_allow_html=True)


def build_rain_timeline_html(data, pred_col, model, hours_to_show):
    """Build HTML for rain timeline"""
    html_content = f"""
    <style>
        .rain-timeline-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }}
        .rain-timeline-table th {{
            background-color: #f9fafb;
            font-weight: bold;
            text-align: center;
            padding: 8px;
            border: 1px solid #e5e7eb;
        }}
        .rain-timeline-table td {{
            text-align: center;
            font-size: 22px;
            padding: 12px;
            border: 1px solid #e5e7eb;
        }}
        .rain-timeline-table td.model-name {{
            background-color: #f9fafb;
            font-weight: 600;
            font-size: 14px;
            text-align: left;
        }}
    </style>
    <table class="rain-timeline-table">
        <thead>
            <tr>
                <th style="width: 150px; text-align: left;">Model</th>
    """
    
    for hour in hours_to_show:
        html_content += f'<th>{hour:02d}:00</th>'
    
    html_content += """
            </tr>
        </thead>
        <tbody>
            <tr>
    """
    
    html_content += f'<td class="model-name">{model["label"]} - {model["name"]}</td>'
    
    for hour in hours_to_show:
        hour_data = data[data['Hour'] == hour]
        
        if len(hour_data) > 0:
            prediction = int(hour_data.iloc[0][pred_col])
            is_night = (hour >= 19 or hour < 6)
            
            if prediction == 1:
                icon = "🌧️"
                bg_color = model["color_rain"]
            elif is_night:
                icon = "🌙"
                bg_color = "#1e3a8a"
            else:
                icon = "☀️"
                bg_color = "#60a5fa"
            
            html_content += f'<td style="background-color: {bg_color}; color: white;">{icon}</td>'
        else:
            html_content += '<td style="background-color: #f3f4f6; color: #9ca3af;">-</td>'
    
    html_content += """
            </tr>
        </tbody>
    </table>
    """
    
    return html_content


def render_rain_noise_weekly_view(left_data, right_data,
                                   left_pred_col, right_pred_col,
                                   left_algo, right_algo,
                                   left_noise, right_noise):
    """Render weekly heatmap view for rain noise comparison"""
    import pandas as pd
    from datetime import timedelta
    
    # Prepare data
    dfl = left_data.copy()
    dfr = right_data.copy()
    
    dfl['Datetime'] = pd.to_datetime(dfl['Datetime'], errors='coerce')
    dfr['Datetime'] = pd.to_datetime(dfr['Datetime'], errors='coerce')
    
    dfl['Date'] = dfl['Datetime'].dt.date
    dfr['Date'] = dfr['Datetime'].dt.date
    dfl['Hour'] = dfl['Datetime'].dt.hour
    dfr['Hour'] = dfr['Datetime'].dt.hour
    
    min_date = dfl['Date'].min()
    max_date = dfl['Date'].max()
    
    # Date range picker
    st.markdown("### 📅 Select Week")
    col_date1, col_date2 = st.columns(2)
    
    if 'rain_noise_weekly_start' not in st.session_state:
        st.session_state.rain_noise_weekly_start = max_date - timedelta(days=6)
        st.session_state.rain_noise_weekly_end = max_date
    
    with col_date1:
        week_start_date = st.date_input(
            "**Start Date**",
            value=st.session_state.rain_noise_weekly_start,
            min_value=min_date,
            max_value=max_date,
            key="rain_noise_weekly_start_date"
        )
    
    with col_date2:
        constrained_max_date = min(max_date, week_start_date + timedelta(days=13))
        week_end_date = st.date_input(
            "**End Date**",
            value=min(st.session_state.rain_noise_weekly_end, constrained_max_date),
            min_value=week_start_date,
            max_value=constrained_max_date,
            key="rain_noise_weekly_end_date"
        )
    
    num_days = (week_end_date - week_start_date).days + 1
    
    # Header
    start_str = week_start_date.strftime('%b %d')
    end_str = week_end_date.strftime('%b %d, %Y')
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px; border-radius: 10px; margin: 15px 0;'>
        <h2 style='color: white; margin: 0; text-align: center; font-size: 20px;'>
            📆 {start_str} - {end_str} ({num_days} days)
        </h2>
        <p style='color: white; margin: 5px 0 0 0; text-align: center; font-size: 15px;'>
            Showing: Actual & Noise Comparison | All 24 Hours
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate date range
    dates = [week_start_date + timedelta(days=i) for i in range(num_days)]
    hours_to_show = list(range(0, 24))
    
    models = [
        {'label': 'A', 'name': 'Actual', 'data': dfl, 'pred_col': 'Actual', 'color_rain': '#10b981'},
        {'label': 'L', 'name': f'{left_algo} ({left_noise})', 'data': dfl, 'pred_col': left_pred_col, 'color_rain': '#8b5cf6'},
        {'label': 'R', 'name': f'{right_algo} ({right_noise})', 'data': dfr, 'pred_col': right_pred_col, 'color_rain': '#6366f1'}
    ]
    
    # Display heatmap for each model
    for model in models:
        st.markdown(f"### {model['label']} - {model['name']}")
        
        model_data = model['data']
        pred_col = model['pred_col']
        
        # Build heatmap data
        heatmap_rows = []
        
        for date in dates:
            day_data = model_data[model_data['Date'] == date].sort_values('Hour')
            day_name = date.strftime('%a %m/%d')
            
            row = {'Day': day_name}
            
            for hour in hours_to_show:
                hour_row = day_data[day_data['Hour'] == hour]
                
                if len(hour_row) > 0:
                    prediction = int(hour_row.iloc[0][pred_col])
                    is_night = (hour >= 19 or hour < 6)
                    
                    if prediction == 1:
                        icon = "🌧️"
                    elif is_night:
                        icon = "🌙"
                    else:
                        icon = "☀️"
                    
                    row[f'{hour:02d}:00'] = icon
                else:
                    row[f'{hour:02d}:00'] = "-"
            
            heatmap_rows.append(row)
        
        # Create DataFrame
        heatmap_df = pd.DataFrame(heatmap_rows)
        
        # Style the dataframe
        def style_cell(val):
            if val == "🌧️":
                return f'background-color: {model["color_rain"]}; color: white; text-align: center; font-size: 20px; padding: 10px;'
            elif val == "🌙":
                return 'background-color: #1e3a8a; color: white; text-align: center; font-size: 20px; padding: 10px;'
            elif val == "☀️":
                return 'background-color:#60a5fa ; color: white; text-align: center; font-size: 20px; padding: 10px;'
            elif val == "-":
                return 'background-color: #f3f4f6; color: #9ca3af; text-align: center; padding: 10px;'
            else:
                return 'background-color: #f9fafb; font-weight: 600; padding: 10px;'
        
        styled_df = heatmap_df.style.map(style_cell, subset=heatmap_df.columns[1:])
        styled_df = styled_df.set_table_styles([
            {'selector': 'thead th', 'props': [('font-weight', 'bold'), ('font-size', '15px'), ('text-align', 'center')]},
            {'selector': 'tbody th', 'props': [('font-weight', 'bold'), ('font-size', '15px')]}
        ])
        styled_df = styled_df.set_properties(**{'text-align': 'left','font-weight': 'bold', 'font-size': '16px'}, subset=['Day'])
        
        st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)