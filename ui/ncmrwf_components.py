# ui/ncmrwfffw_components.py
"""
UI Components for NCMRWFFFW Data Source
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config.constants import (
    NCMRWF_CLASSICAL_ALGORITHMS,
    NCMRWF_QUANTUM_ALGORITHMS,
    NCMRWF_ALGORITHM_SHORT_NAMES,
    NCMRWF_REGRESSION_METRICS,
    NCMRWF_UNIVARIATE_CLASSICAL_ALGORITHMS,
    NCMRWF_UNIVARIATE_QUANTUM_ALGORITHMS,
    NCMRWF_UNIVARIATE_ALGORITHM_SHORT_NAMES,
    NCMRWF_UNIVARIATE_REGRESSION_METRICS,
    IDEAL_VALUES
)
from data.ncmrwf_loader import get_ncmrwf_algorithm_data


def create_ncmrwf_combined_chart(classical_data, quantum_data, 
                                     classical_name, quantum_name,
                                     classical_pred_col, quantum_pred_col):
    """Create combined chart for NCMRWFFFW data"""
    fig = go.Figure()
    
    # Actual temperature - Blue
    fig.add_trace(go.Scatter(
        x=classical_data['Date'],
        y=classical_data['T2M'],
        mode='lines+markers',
        name='Actual Temperature',
        line=dict(color='#0000FF', width=3),
        marker=dict(size=5, color='#0000FF'),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Actual: %{y:.2f}°k<extra></extra>'
    ))
    
    # Classical prediction - RED
    fig.add_trace(go.Scatter(
        x=classical_data['Date'],
        y=classical_data[classical_pred_col],
        mode='lines+markers',
        name=f'Classical ({classical_name})',
        line=dict(color='#FF0000', width=3),
        marker=dict(size=5, color='#FF0000'),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Classical: %{y:.2f}°k<extra></extra>'
    ))
    
    # Quantum prediction - Turquoise, dotted
    fig.add_trace(go.Scatter(
        x=quantum_data['Date'],
        y=quantum_data[quantum_pred_col],
        mode='lines+markers',
        name=f'Quantum ({quantum_name})',
        line=dict(color='#30D5C8', width=3),
        marker=dict(size=5, color='#30D5C8'),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Quantum: %{y:.2f}°k<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="<b>NCMRWF: Classical vs Quantum Temperature Prediction</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=18, color='#2c3e50')
        ),
        xaxis_title="Date",
        yaxis_title="Temperature (°k)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        margin=dict(l=60, r=40, t=80, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(
            tickmode='linear',   # 🔹 ensures equal spacing
            tick0=280,           # 🔹 starting value (optional but recommended)
            dtick=2,
            tickfont=dict(color='#000000', size=15),
            title=dict(font=dict(color='#000000', size=16)),
            gridcolor='rgba(0,0,0,0.05)'
        ),
        xaxis=dict(
            tickfont=dict(color='#000000', size=15),
            title=dict(font=dict(color='#000000', size=16)),
            showgrid=True,
            gridcolor='rgba(0,0,0,0.05)'
        ),
        hovermode='x unified'
    )
    
    return fig

def render_ncmrwf_section():
    """Main section for NCMRWF data source"""

    # ==================== UNIVARIATE / MULTIVARIATE TOGGLE ====================
    st.markdown("### 📂 Select Analysis Type")

    current_type = st.session_state.get('ncmrwf_analysis_type', 'Univariate')
    analysis_type = st.radio(
        "Choose analysis type:",
        options=["Univariate", "Multivariate"],
        index=0 if current_type == 'Univariate' else 1,
        horizontal=True,
        key="ncmrwf_analysis_type_radio"
    )

    # Reset predictions if analysis type changed
    if st.session_state.get('ncmrwf_analysis_type') != analysis_type:
        st.session_state.ncmrwf_analysis_type = analysis_type
        st.session_state.ncmr_predictions_generated = False
        st.session_state.ncmr_classical_data = None
        st.session_state.ncmr_quantum_data = None
        st.rerun()

    st.session_state.ncmrwf_analysis_type = analysis_type

    # ==================== DEFINE ALGORITHM SETS BASED ON TYPE ====================
    if analysis_type == "Univariate":
        st.info("📊 **Univariate Mode:** Single-feature time series — Classical: GRU & LSTM | Quantum: QGRU & QLSTM")
        active_classical_algos = NCMRWF_UNIVARIATE_CLASSICAL_ALGORITHMS
        active_quantum_algos = NCMRWF_UNIVARIATE_QUANTUM_ALGORITHMS
        active_short_names = NCMRWF_UNIVARIATE_ALGORITHM_SHORT_NAMES
    else:  # Multivariate
        st.info("📊 **Multivariate Mode:** Multi-feature prediction using all available input variables.")
        active_classical_algos = NCMRWF_CLASSICAL_ALGORITHMS
        active_quantum_algos = NCMRWF_QUANTUM_ALGORITHMS
        active_short_names = NCMRWF_ALGORITHM_SHORT_NAMES

    # ==================== ALGORITHM SELECTION ====================
    st.markdown("### ⚙️ Select Algorithms")

    col_algo1, col_algo2 = st.columns(2)

    with col_algo1:
        st.markdown("**🖥️ Classical Algorithm**")
        classical_options = list(active_classical_algos.keys())

        def update_ncmrwf_classical():
            st.session_state.ncmrwf_selected_classical = st.session_state.ncmr_classical_algo_select

        if st.session_state.get('ncmrwf_selected_classical') not in classical_options:
            st.session_state.ncmrwf_selected_classical = classical_options[0] if classical_options else ""

        try:
            default_classical_idx = classical_options.index(st.session_state.ncmrwf_selected_classical)
        except (ValueError, KeyError):
            default_classical_idx = 0

        classical_algo = st.selectbox(
            "Select algorithm",
            classical_options,
            index=default_classical_idx,
            key="ncmr_classical_algo_select",
            on_change=update_ncmrwf_classical
        )

    with col_algo2:
        st.markdown("**⚛️ Quantum Algorithm**")
        quantum_options = list(active_quantum_algos.keys())

        def update_ncmrwf_quantum():
            st.session_state.ncmrwf_selected_quantum = st.session_state.ncmr_quantum_algo_select

        if st.session_state.get('ncmrwf_selected_quantum') not in quantum_options:
            st.session_state.ncmrwf_selected_quantum = quantum_options[0] if quantum_options else ""

        try:
            default_quantum_idx = quantum_options.index(st.session_state.ncmrwf_selected_quantum)
        except (ValueError, KeyError):
            default_quantum_idx = 0

        quantum_algo = st.selectbox(
            "Select algorithm",
            quantum_options,
            index=default_quantum_idx,
            key="ncmr_quantum_algo_select",
            on_change=update_ncmrwf_quantum
        )

    # Get short names
    classical_algo_short = active_short_names.get(classical_algo, classical_algo)
    quantum_algo_short = active_short_names.get(quantum_algo, quantum_algo)

    # Check if both selected (no placeholder selected)
    both_selected = (
        classical_algo != "Select Classical Algorithm" and
        quantum_algo != "Select Quantum Algorithm" and
        classical_algo != "" and
        quantum_algo != ""
    )

    if both_selected:
        st.info(f"📌 Selected: **{classical_algo_short}** (Classical) vs **{quantum_algo_short}** (Quantum)")
        
        if st.button("🎯 GENERATE NCMRWF PREDICTIONS", key="gen_ncmr_temp", type="primary"):
            with st.spinner(f"Loading predictions for {classical_algo_short} and {quantum_algo_short}..."):
                
                # Debug: Show what we're loading
                st.caption(f"📂 Loading Classical: {classical_algo} -> {active_classical_algos[classical_algo]['file']}")
                st.caption(f"📂 Loading Quantum: {quantum_algo} -> {active_quantum_algos[quantum_algo]['file']}")
                
                classical_data = get_ncmrwf_algorithm_data(
                    'classical', classical_algo, active_classical_algos
                )
                quantum_data = get_ncmrwf_algorithm_data(
                    'quantum', quantum_algo, active_quantum_algos
                )
                
                # Debug: Show loaded data info
                if classical_data is not None:
                    st.caption(f"✅ Classical data loaded: {len(classical_data)} rows")
                    st.caption(f"   Columns: {list(classical_data.columns)}")
                if quantum_data is not None:
                    st.caption(f"✅ Quantum data loaded: {len(quantum_data)} rows")
                    st.caption(f"   Columns: {list(quantum_data.columns)}")
                
                if classical_data is not None and quantum_data is not None:
                    classical_pred_col = active_classical_algos[classical_algo]['pred_col']
                    quantum_pred_col = active_quantum_algos[quantum_algo]['pred_col']
                    
                    st.session_state.ncmr_classical_data = {
                        'data': classical_data,
                        'algorithm': classical_algo_short,
                        'metrics_key': classical_algo_short,
                        'prediction_column': classical_pred_col
                    }
                    st.session_state.ncmr_quantum_data = {
                        'data': quantum_data,
                        'algorithm': quantum_algo_short,
                        'metrics_key': quantum_algo_short,
                        'prediction_column': quantum_pred_col
                    }
                    st.session_state.ncmr_predictions_generated = True
                    st.success("✅ NCMRWF Predictions loaded successfully!")
                    st.rerun()
                else:
                    st.error("❌ Could not load prediction data")
    else:
        missing = []
        if not classical_algo or classical_algo == "Select Classical Algorithm":
            missing.append("Classical Algorithm")
        if not quantum_algo or quantum_algo == "Select Quantum Algorithm":
            missing.append("Quantum Algorithm")
        if missing:
            st.warning(f"⚠️ Please select: {' and '.join(missing)}")

    # ==================== DISPLAY RESULTS ====================
    if st.session_state.get('ncmr_predictions_generated', False):
        st.markdown("---")

        mode_label = st.session_state.get('ncmrwf_analysis_type', 'Multivariate')
        st.markdown(f"### 📈 Combined Prediction Comparison — *{mode_label}*")

        classical_data = st.session_state.ncmr_classical_data['data']
        quantum_data = st.session_state.ncmr_quantum_data['data']
        classical_pred_col = st.session_state.ncmr_classical_data['prediction_column']
        quantum_pred_col = st.session_state.ncmr_quantum_data['prediction_column']
        classical_name = st.session_state.ncmr_classical_data['algorithm']
        quantum_name = st.session_state.ncmr_quantum_data['algorithm']

        fig_combined = create_ncmrwf_combined_chart(
            classical_data, quantum_data,
            classical_name, quantum_name,
            classical_pred_col, quantum_pred_col
        )
        st.plotly_chart(fig_combined, use_container_width=True)

        st.markdown("---")
        st.markdown("#### Algorithm Performance Metrics Comparison: Classical vs Quantum")
        render_ncmrwf_metrics_table(classical_name, quantum_name)

        st.info("""
        📊 **About NCMRWF Dataset:**
        - **Source**: NCMRWF (National Center for Medium Range Weather Forecasting)
        - **Temporal Resolution**: Daily predictions
        - **Total Records**: {} data points
        - **Date Range**: {} to {}
        - **Analysis Type**: {}
        """.format(
            len(classical_data),
            classical_data['Date'].min().strftime('%Y-%m-%d'),
            classical_data['Date'].max().strftime('%Y-%m-%d'),
            mode_label
        ))

        if st.session_state.get('ncmr_predictions_generated', False):
            render_ncmrwf_training_and_quantum_sections()
# def render_ncmrwf_section():
#     """Main section for NCMRWF data source"""

#     # ==================== UNIVARIATE / MULTIVARIATE TOGGLE ====================
#     st.markdown("### 📂 Select Analysis Type")

#     current_type = st.session_state.get('ncmrwf_analysis_type', 'Univariate')
#     analysis_type = st.radio(
#         "Choose analysis type:",
#         options=["Univariate", "Multivariate"],
#         index=0 if current_type == 'Univariate' else 1,
#         horizontal=True,
#         key="ncmrwf_analysis_type_radio"
#     )

#     # Reset predictions if analysis type changed
#     if st.session_state.get('ncmrwf_analysis_type') != analysis_type:
#         st.session_state.ncmrwf_analysis_type = analysis_type
#         st.session_state.ncmr_predictions_generated = False
#         st.session_state.ncmr_classical_data = None
#         st.session_state.ncmr_quantum_data = None
#         st.rerun()

#     st.session_state.ncmrwf_analysis_type = analysis_type

#     # ==================== DEFINE ALGORITHM SETS BASED ON TYPE ====================
#     if analysis_type == "Univariate":
#             st.info("📊 **Univariate Mode:** Single-feature time series — Classical: GRU & LSTM | Quantum: QGRU & QLSTM")
#             active_classical_algos = NCMRWF_UNIVARIATE_CLASSICAL_ALGORITHMS
#             active_quantum_algos = NCMRWF_UNIVARIATE_QUANTUM_ALGORITHMS
#             active_short_names = NCMRWF_UNIVARIATE_ALGORITHM_SHORT_NAMES

#     else:  # Multivariate
#         st.info("📊 **Multivariate Mode:** Multi-feature prediction using all available input variables.")
#         active_classical_algos = NCMRWF_CLASSICAL_ALGORITHMS
#         active_quantum_algos = NCMRWF_QUANTUM_ALGORITHMS
#         active_short_names = NCMRWF_ALGORITHM_SHORT_NAMES

#     # ==================== ALGORITHM SELECTION ====================
#     st.markdown("### ⚙️ Select Algorithms")

#     col_algo1, col_algo2 = st.columns(2)

#     with col_algo1:
#         st.markdown("**🖥️ Classical Algorithm**")

#         classical_options = list(active_classical_algos.keys())

#         def update_ncmrwf_classical():
#             st.session_state.ncmrwf_selected_classical = st.session_state.ncmr_classical_algo_select

#         # Reset if stored selection not valid for current mode
#         if st.session_state.get('ncmrwf_selected_classical') not in classical_options:
#             st.session_state.ncmrwf_selected_classical = classical_options[0] if classical_options else ""

#         try:
#             default_classical_idx = classical_options.index(st.session_state.ncmrwf_selected_classical)
#         except (ValueError, KeyError):
#             default_classical_idx = 0

#         classical_algo = st.selectbox(
#             "Select algorithm",
#             classical_options,
#             index=default_classical_idx,
#             key="ncmr_classical_algo_select",
#             on_change=update_ncmrwf_classical
#         )

#     with col_algo2:
#         st.markdown("**⚛️ Quantum Algorithm**")

#         quantum_options = list(active_quantum_algos.keys())

#         def update_ncmrwf_quantum():
#             st.session_state.ncmrwf_selected_quantum = st.session_state.ncmr_quantum_algo_select

#         # Reset if stored selection not valid for current mode
#         if st.session_state.get('ncmrwf_selected_quantum') not in quantum_options:
#             st.session_state.ncmrwf_selected_quantum = quantum_options[0] if quantum_options else ""

#         try:
#             default_quantum_idx = quantum_options.index(st.session_state.ncmrwf_selected_quantum)
#         except (ValueError, KeyError):
#             default_quantum_idx = 0

#         quantum_algo = st.selectbox(
#             "Select algorithm",
#             quantum_options,
#             index=default_quantum_idx,
#             key="ncmr_quantum_algo_select",
#             on_change=update_ncmrwf_quantum
#         )

#     # Get short names
#     # Get short names — uses correct dict based on mode
#     classical_algo_short = active_short_names.get(classical_algo, classical_algo)
#     quantum_algo_short = active_short_names.get(quantum_algo, quantum_algo)

#     # Check if both selected (no placeholder selected)
    
#     # both_selected = (
#     #     classical_algo != "Select Classical Algorithm" and
#     #     quantum_algo != "Select Quantum Algorithm" and
#     #     classical_algo != "" and
#     #     quantum_algo != ""
#     # )

#     # if both_selected:
#     # st.info(f"📌 Selected: **{classical_algo_short}** (Classical) vs **{quantum_algo_short}** (Quantum)")

#     # if st.button("🎯 GENERATE NCMRWF PREDICTIONS", key="gen_ncmr_temp", type="primary"):
#     #     with st.spinner(f"Loading predictions for {classical_algo_short} and {quantum_algo_short}..."):
            
#     #         # ✅ Debug: Show what we're loading
#     #         st.caption(f"📂 Loading Classical: {classical_algo} -> {active_classical_algos[classical_algo]['file']}")
#     #         st.caption(f"📂 Loading Quantum: {quantum_algo} -> {active_quantum_algos[quantum_algo]['file']}")

#     #         classical_data = get_ncmrwf_algorithm_data(
#     #             'classical', classical_algo, active_classical_algos
#     #         )
#     #         quantum_data = get_ncmrwf_algorithm_data(
#     #             'quantum', quantum_algo, active_quantum_algos
#     #         )
            
#             # ✅ Debug: Show loaded data info
#             if classical_data is not None:
#                 st.caption(f"✅ Classical data loaded: {len(classical_data)} rows")
#                 st.caption(f"   Columns: {list(classical_data.columns)}")
#             if quantum_data is not None:
#                 st.caption(f"✅ Quantum data loaded: {len(quantum_data)} rows")
#                 st.caption(f"   Columns: {list(quantum_data.columns)}")

#                 if classical_data is not None and quantum_data is not None:
#                     classical_pred_col = active_classical_algos[classical_algo]['pred_col']
#                     quantum_pred_col = active_quantum_algos[quantum_algo]['pred_col']

#                     st.session_state.ncmr_classical_data = {
#                         'data': classical_data,
#                         'algorithm': classical_algo_short,
#                         'metrics_key': classical_algo_short,
#                         'prediction_column': classical_pred_col
#                     }
#                     st.session_state.ncmr_quantum_data = {
#                         'data': quantum_data,
#                         'algorithm': quantum_algo_short,
#                         'metrics_key': quantum_algo_short,
#                         'prediction_column': quantum_pred_col
#                     }
#                     st.session_state.ncmr_predictions_generated = True
#                     st.success("✅ NCMRWF Predictions loaded successfully!")
#                     st.rerun()
#                 else:
#                     st.error("❌ Could not load prediction data")
#     else:
#         missing = []
#         if not classical_algo or classical_algo == "Select Classical Algorithm":
#             missing.append("Classical Algorithm")
#         if not quantum_algo or quantum_algo == "Select Quantum Algorithm":
#             missing.append("Quantum Algorithm")
#         if missing:
#             st.warning(f"⚠️ Please select: {' and '.join(missing)}")

#     # ==================== DISPLAY RESULTS ====================
#     if st.session_state.get('ncmr_predictions_generated', False):
#         st.markdown("---")

#         mode_label = st.session_state.get('ncmrwf_analysis_type', 'Multivariate')
#         st.markdown(f"### 📈 Combined Prediction Comparison — *{mode_label}*")

#         classical_data = st.session_state.ncmr_classical_data['data']
#         quantum_data = st.session_state.ncmr_quantum_data['data']
#         classical_pred_col = st.session_state.ncmr_classical_data['prediction_column']
#         quantum_pred_col = st.session_state.ncmr_quantum_data['prediction_column']
#         classical_name = st.session_state.ncmr_classical_data['algorithm']
#         quantum_name = st.session_state.ncmr_quantum_data['algorithm']

#         fig_combined = create_ncmrwf_combined_chart(
#             classical_data, quantum_data,
#             classical_name, quantum_name,
#             classical_pred_col, quantum_pred_col
#         )
#         st.plotly_chart(fig_combined, use_container_width=True)

#         st.markdown("---")
#         st.markdown("#### Algorithm Performance Metrics Comparison: Classical vs Quantum")
#         render_ncmrwf_metrics_table(classical_name, quantum_name)

#         st.info("""
#         📊 **About NCMRWF Dataset:**
#         - **Source**: NCMRWF (National Center for Medium Range Weather Forecasting)
#         - **Temporal Resolution**: Daily predictions
#         - **Total Records**: {} data points
#         - **Date Range**: {} to {}
#         - **Analysis Type**: {}
#         """.format(
#             len(classical_data),
#             classical_data['Date'].min().strftime('%Y-%m-%d'),
#             classical_data['Date'].max().strftime('%Y-%m-%d'),
#             mode_label
#         ))

#         if st.session_state.get('ncmr_predictions_generated', False):
#             render_ncmrwf_training_and_quantum_sections()

def render_ncmrwf_metrics_table(classical_algo, quantum_algo):
    """Display metrics table for NCMRWF algorithms"""

    # ✅ Pick correct metrics dict based on current analysis mode
    analysis_type = st.session_state.get('ncmrwf_analysis_type', 'Multivariate')
    
    if analysis_type == "Univariate":
        metrics_source = NCMRWF_UNIVARIATE_REGRESSION_METRICS
    else:
        metrics_source = NCMRWF_REGRESSION_METRICS

    metric_names = [
        "Mean Squared Error (MSE)",
        "Root Mean Squared Error (RMSE)",
        "Mean Absolute Error (MAE)",
        "Mean Absolute Percentage Error (MAPE)",
        "R² Score"
    ]

    classical_values = [""] * len(metric_names)
    quantum_values = [""] * len(metric_names)

    # Get classical metrics
    classical_found = False
    if classical_algo in metrics_source:
        classical_metrics = metrics_source[classical_algo]
        for i, metric in enumerate(metric_names):
            if metric in classical_metrics:
                classical_values[i] = f"{classical_metrics[metric]:.4f}"
        classical_found = True
    else:
        st.warning(f"⚠️ Metrics not found for classical algorithm: '{classical_algo}'")

    # Get quantum metrics
    quantum_found = False
    if quantum_algo in metrics_source:
        quantum_metrics = metrics_source[quantum_algo]
        for i, metric in enumerate(metric_names):
            if metric in quantum_metrics:
                quantum_values[i] = f"{quantum_metrics[metric]:.4f}"
        quantum_found = True
    else:
        st.warning(f"⚠️ Metrics not found for quantum algorithm: '{quantum_algo}'")

    # Only proceed if at least one algorithm has metrics
    if not classical_found and not quantum_found:
        st.error("❌ No metrics found for either algorithm.")
        return

    # Ideal values
    ideal_values = [IDEAL_VALUES[metric] for metric in metric_names]

    # Create DataFrame (ONCE)
    df = pd.DataFrame({
        'Metric': metric_names,
        f'Classical ({classical_algo})': classical_values,
        f'Quantum ({quantum_algo})': quantum_values,
        'Ideal Value': ideal_values
    })

    # Display table (ONCE)
    from visualization.tables import create_metrics_table_html
    table_html = create_metrics_table_html(
        f'Classical ({classical_algo})',
        f'Quantum ({quantum_algo})',
        df
    )
    st.markdown(table_html, unsafe_allow_html=True)

    # Show comparison only if both metrics exist
    if classical_found and quantum_found:
        c_r2 = metrics_source[classical_algo]['R² Score']
        q_r2 = metrics_source[quantum_algo]['R² Score']

        if q_r2 > c_r2:
            improvement = ((q_r2 - c_r2) / c_r2) * 100
            st.success(f"✅ Quantum shows **{improvement:.2f}% improvement** in R² Score over Classical!")
        elif c_r2 > q_r2:
            difference = ((c_r2 - q_r2) / q_r2) * 100
            st.info(f"ℹ️ Classical shows **{difference:.2f}% better** R² Score")
        else:
            st.info("📊 Both algorithms have identical R² Score")
# def render_ncmrwf_metrics_table(classical_algo, quantum_algo):
#     """Display metrics table for NCMRWF algorithms"""

#     # ✅ Pick correct metrics dict based on current analysis mode
#     analysis_type = st.session_state.get('ncmrwf_analysis_type', 'Multivariate')
#     metrics_source = (
#         NCMRWF_UNIVARIATE_REGRESSION_METRICS
#         if analysis_type == "Univariate"
#         else NCMRWF_REGRESSION_METRICS
#     )

#     metric_names = [
#         "Mean Squared Error (MSE)",
#         "Root Mean Squared Error (RMSE)",
#         "Mean Absolute Error (MAE)",
#         "Mean Absolute Percentage Error (MAPE)",
#         "R² Score"
#     ]

#     classical_values = [""] * len(metric_names)
#     quantum_values = [""] * len(metric_names)

#     # Get classical metrics
#     if classical_algo in metrics_source:
#         classical_metrics = metrics_source[classical_algo]
#         for i, metric in enumerate(metric_names):
#             if metric in classical_metrics:
#                 classical_values[i] = f"{classical_metrics[metric]:.4f}"
#     else:
#         st.warning(f"⚠️ Metrics not found for classical algorithm: '{classical_algo}'")
#         st.info(f"Available keys: {list(metrics_source.keys())}")

#     # Get quantum metrics
#     if quantum_algo in metrics_source:
#         quantum_metrics = metrics_source[quantum_algo]
#         for i, metric in enumerate(metric_names):
#             if metric in quantum_metrics:
#                 quantum_values[i] = f"{quantum_metrics[metric]:.4f}"
#     else:
#         st.warning(f"⚠️ Metrics not found for quantum algorithm: '{quantum_algo}'")
#         st.info(f"Available keys: {list(metrics_source.keys())}")

#     # Ideal values
#     ideal_values = [IDEAL_VALUES[metric] for metric in metric_names]

#     # Create DataFrame
#     df = pd.DataFrame({
#         'Metric': metric_names,
#         f'Classical ({classical_algo})': classical_values,
#         f'Quantum ({quantum_algo})': quantum_values,
#         'Ideal Value': ideal_values
#     })

#     from visualization.tables import create_metrics_table_html
#     table_html = create_metrics_table_html(
#         f'Classical ({classical_algo})',
#         f'Quantum ({quantum_algo})',
#         df
#     )
#     st.markdown(table_html, unsafe_allow_html=True)

#     # Show comparison only if both metrics exist
#     if classical_algo in metrics_source and quantum_algo in metrics_source:
#         c_r2 = metrics_source[classical_algo]['R² Score']
#         q_r2 = metrics_source[quantum_algo]['R² Score']

#         if q_r2 > c_r2:
#             improvement = ((q_r2 - c_r2) / c_r2) * 100
#             st.success(f"✅ Quantum shows **{improvement:.2f}% improvement** in R² Score over Classical!")
#         elif c_r2 > q_r2:
#             difference = ((c_r2 - q_r2) / q_r2) * 100
#             st.info(f"ℹ️ Classical shows **{difference:.2f}% better** R² Score")
#         else:
#             st.info("📊 Both algorithms have identical R² Score")
#         for i, metric in enumerate(metric_names):
#             if metric in classical_metrics:
#                 value = classical_metrics[metric]
#                 # classical_values[i] = f"{value:.4f}"
#                 # if metric == "Mean Absolute Percentage Error (MAPE)":
#                 #     classical_values[i] = f"{value:.4f} ({value*100:.2f}%)"
#                 # else:
#                 classical_values[i] = f"{value:.4f}"
#     else:
#         # Show which key was tried for debugging
#         st.warning(f"⚠️ Metrics not found for classical algorithm: '{classical_algo}'")
#         st.info(f"Available metrics keys: {list(NCMRWF_REGRESSION_METRICS.keys())}")
    
#     # ✅ FIX: Get quantum metrics using SHORT NAMES
#     if quantum_algo in NCMRWF_REGRESSION_METRICS:
#         quantum_metrics = NCMRWF_REGRESSION_METRICS[quantum_algo]
#         for i, metric in enumerate(metric_names):
#             if metric in quantum_metrics:
#                 value = quantum_metrics[metric]
#                 # quantum_values[i] = f"{value:.4f}"
#                 # if metric == "Mean Absolute Percentage Error (MAPE)":
#                 #     quantum_values[i] = f"{value:.4f} ({value*100:.2f}%)"
#                 # else:
#                 quantum_values[i] = f"{value:.4f}"
#     else:
#         st.warning(f"⚠️ Metrics not found for quantum algorithm: '{quantum_algo}'")
#         st.info(f"Available metrics keys: {list(NCMRWF_REGRESSION_METRICS.keys())}")
    
#     # Ideal values
#     ideal_values = [IDEAL_VALUES[metric] for metric in metric_names]
    
#     # Create DataFrame
#     df = pd.DataFrame({
#         'Metric': metric_names,
#         f'Classical ({classical_algo})': classical_values,
#         f'Quantum ({quantum_algo})': quantum_values,
#         'Ideal Value': ideal_values
#     })
    
#     # ✅ Display with HTML styling
#     from visualization.tables import create_metrics_table_html
#     table_html = create_metrics_table_html(
#         f'Classical ({classical_algo})',
#         f'Quantum ({quantum_algo})',
#         df
#     )
#     st.markdown(table_html, unsafe_allow_html=True)
    
#     # ✅ Show comparison ONLY if both metrics exist
#     if classical_algo in NCMRWF_REGRESSION_METRICS and quantum_algo in NCMRWF_REGRESSION_METRICS:
#         c_r2 = NCMRWF_REGRESSION_METRICS[classical_algo]['R² Score']
#         q_r2 = NCMRWF_REGRESSION_METRICS[quantum_algo]['R² Score']
        
#         if q_r2 > c_r2:
#             improvement = ((q_r2 - c_r2) / c_r2) * 100
#             # st.success(f"✅ Quantum algorithm shows **{improvement:.2f}% improvement** in R² Score!")
#         elif c_r2 > q_r2:
#             difference = ((c_r2 - q_r2) / q_r2) * 100
#             # st.info(f"ℹ️ Classical algorithm shows **{difference:.2f}% better** R² Score")
#         else:
#             # st.info("📊 Both algorithms have identical R² Score")
#             pass
#     else:
#         st.info("ℹ️ Generate predictions for both algorithms to see comparison")


#Now adding the new one 
# def render_ncmrwf_training_and_quantum_sections():
#     """
#     Render Training Parameters and Quantum Resources sections for NCMRWF
#     """
#     from config.constants import NCMRWF_ALGORITHM_PARAMS, NCMRWF_QUANTUM_RESOURCE_DATA
#     from visualization.charts import create_ncmrwf_training_params_chart, create_ncmrwf_quantum_resource_charts
    
#     st.markdown("---")
    
#     # ==================== TRAINING PARAMETERS ====================
#     col_train, col_quantum = st.columns(2)
    
#     with col_train:
#         st.markdown("#### Training Parameters")
        
#         # Get selected algorithms
#         classical_algo = st.session_state.get('ncmr_classical_data', {}).get('algorithm', None)
#         quantum_algo = st.session_state.get('ncmr_quantum_data', {}).get('algorithm', None)
        
#         if classical_algo and quantum_algo:
#             # Create chart
#             fig_params = create_ncmrwf_training_params_chart(
#                 classical_algo, quantum_algo, NCMRWF_ALGORITHM_PARAMS
#             )
#             # ✅ FIX: Only display if chart was created successfully
#             if fig_params is not None:
#                 st.plotly_chart(fig_params, use_container_width=True)
#             else:
#                 st.warning(f"⚠️ Could not create training parameters chart for {classical_algo} and {quantum_algo}")
#                 st.info(f"Available algorithm keys in NCMRWF_ALGORITHM_PARAMS: {list(NCMRWF_ALGORITHM_PARAMS.keys())}")
#             # st.plotly_chart(fig_params, use_container_width=True)
#         else:
#             st.info("Generate predictions to view training parameters comparison")
        
#         with st.expander("Training Parameters Information", expanded=False):
#             st.markdown("""
#             **Training Parameters Overview:**
            
#             - **GRU**: 1,649 trainable parameters
#             - **LSTM**: 2,129 trainable parameters
#             - **QGRU**: 677 quantum parameters (~59% reduction)
#             - **QLSTM**: 877 quantum parameters (~59% reduction)
            
#             **Key Insight**: Both quantum models achieve approximately 60% parameter compression 
#             while maintaining competitive performance with their classical counterparts.
#             """)
    
#     # ==================== QUANTUM RESOURCES ====================
#     with col_quantum:
#         st.markdown("#### Quantum Resource Estimates")
        
#         if quantum_algo and quantum_algo in ['QGRU', 'QLSTM','QNN_IS','Hybrid QNN_IS','Hybrid QNN_SE']:
#             # Create combined resource chart for the selected algorithm
#             from visualization.charts import create_ncmrwf_combined_resource_chart
#             fig_resources = create_ncmrwf_combined_resource_chart(quantum_algo)
#             st.plotly_chart(fig_resources, use_container_width=True)
#         else:
#             st.info("Generate quantum predictions to view resource estimates")
        
#         with st.expander("Quantum Resource Information", expanded=False):
#             st.markdown("""
#             **Quantum Circuit Complexity:**
            
#             **QGRU:**
#             - Single-Qubit Gates: 84
#             - Multi-Qubit Gates: 24
#             - Circuit Depth: 15
            
#             **QLSTM:**
#             - Single-Qubit Gates: 64
#             - Multi-Qubit Gates: 16
#             - Circuit Depth: 8
#             **QNN_IS**
#             - Single-Qubit Gates: 
#             - Multi-Qubit Gates: 
#             - Circuit Depth: 
            
#             **Key Insight**: QLSTM has lower circuit complexity than QGRU, making it more 
#             suitable for near-term quantum hardware deployment.
#             """)
# 
def render_ncmrwf_training_and_quantum_sections():
    """
    Render Training Parameters and Quantum Resources sections for NCMRWF.
    Training params differ between Univariate and Multivariate modes.
    Quantum Resource Estimates are always shown as-is.
    """
    from config.constants import (
        NCMRWF_ALGORITHM_PARAMS,
        NCMRWF_UNIVARIATE_ALGORITHM_PARAMS,
        NCMRWF_QUANTUM_RESOURCE_DATA
    )
    from visualization.charts import (
        create_ncmrwf_training_params_chart,
        create_ncmrwf_quantum_resource_charts,
        create_ncmrwf_combined_resource_chart
    )

    st.markdown("---")

    col_train, col_quantum = st.columns(2)

    # ── pick the right params dict based on current analysis mode ──
    analysis_type = st.session_state.get('ncmrwf_analysis_type', 'Multivariate')
    active_params = (
        NCMRWF_UNIVARIATE_ALGORITHM_PARAMS
        if analysis_type == "Univariate"
        else NCMRWF_ALGORITHM_PARAMS
    )

    # ==================== TRAINING PARAMETERS ====================
    with col_train:
        st.markdown("#### Training Parameters")

        classical_algo = st.session_state.get('ncmr_classical_data', {}).get('metrics_key', None)
        quantum_algo   = st.session_state.get('ncmr_quantum_data',  {}).get('metrics_key', None)

        if classical_algo and quantum_algo:
            fig_params = create_ncmrwf_training_params_chart(
                classical_algo, quantum_algo, active_params
            )
            if fig_params is not None:
                st.plotly_chart(fig_params, use_container_width=True)
            else:
                st.error(
                    f"❌ Could not create chart for {classical_algo} and "
                    f"{quantum_algo} in {analysis_type} mode.\n"
                    f"Available keys: {list(active_params.keys())}"
                )
        else:
            st.info("Generate predictions to view training parameters comparison")

        # expander text adapts to mode
        if analysis_type == "Univariate":
            expander_text = """
**Univariate Training Parameters Overview:**

- **GRU**: 1,649 trainable parameters  
- **LSTM**: 2,129 trainable parameters  
- **QGRU**: 677 quantum parameters (~59% reduction)  
- **QLSTM**: 877 quantum parameters (~59% reduction)  

**Key Insight**: Quantum models achieve ~60% parameter compression
while maintaining competitive univariate prediction performance.
"""
        else:
            expander_text = """
**Multivariate Training Parameters Overview:**

- **GRU**: 1,649 trainable parameters  
- **LSTM**: 2,129 trainable parameters  
- **QGRU**: 677 quantum parameters (~59% reduction)  
- **QLSTM**: 877 quantum parameters (~59% reduction)  

**Key Insight**: Both quantum models achieve approximately 60% parameter compression
while maintaining competitive performance with their classical counterparts.
"""

        with st.expander("Training Parameters Information", expanded=False):
            st.markdown(expander_text)

    # ==================== QUANTUM RESOURCES (unchanged) ====================
    with col_quantum:
        st.markdown("#### Quantum Resource Estimates")

        quantum_algo = st.session_state.get('ncmr_quantum_data', {}).get('metrics_key', None)

        if quantum_algo and quantum_algo in ['QGRU', 'QLSTM', 'QNN_IS_2.0', 'Hybrid QNN_SE']:
            fig_resources = create_ncmrwf_combined_resource_chart(quantum_algo)
            if fig_resources is not None:
                st.plotly_chart(fig_resources, use_container_width=True)
            else:
                st.error(f"❌ Could not create resource chart for {quantum_algo}")
        else:
            st.info("Generate quantum predictions to view resource estimates")

        with st.expander("Quantum Resource Information", expanded=False):
            st.markdown("""
**Quantum Circuit Complexity:**

**QGRU:**
- Single-Qubit Gates: 84
- Multi-Qubit Gates: 24
- Circuit Depth: 15

**QLSTM:**
- Single-Qubit Gates: 64
- Multi-Qubit Gates: 16
- Circuit Depth: 8

**QNN_IS:**
- Single-Qubit Gates: 70
- Multi-Qubit Gates: 30
- Circuit Depth: 4

**Key Insight**: QLSTM has lower circuit complexity than QGRU, making it more
suitable for near-term quantum hardware deployment.
""")