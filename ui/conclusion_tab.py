# ui/conclusion_tab.py
"""
Updated Conclusion Tab Component with NCMRWF Support
"""
import streamlit as st
import pandas as pd
# from visualization.tables import create_conclusion_metrics_table_html,create_noise_comparison_table_html  # ✅ ADD THIS
from visualization.charts import create_quantum_resource_charts
from config.constants import CLASSIFICATION_METRICS, REGRESSION_METRICS, NCMRWF_REGRESSION_METRICS,NOISE_METRICS, IDEAL_VALUES
from visualization.parameters_table import render_parameters_comparison_section
# from visualization.tables import create_conclusion_metrics_table_html, create_noise_comparison_table_html
from visualization.tables import (
    create_conclusion_metrics_table_html, 
    create_noise_comparison_table_html,
    create_ncmrwf_metrics_table_html  # ✅ ADD THIS
)
def inject_custom_css():
    """Inject custom CSS for animations and styling"""
    st.markdown("""
    <style>
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        .scroll-animate {
            animation: fadeInUp 0.8s ease forwards;
            opacity: 0;
        }
        .animate-fade {
            animation: fadeInUp 0.8s ease forwards;
            opacity: 0;
        }
        
        .animate-slide-left {
            animation: slideInLeft 0.8s ease forwards;
            opacity: 0;
        }
        
        .animate-slide-right {
            animation: slideInRight 0.8s ease forwards;
            opacity: 0;
        }
        
        .animate-delay-1 { animation-delay: 0.1s; }
        .animate-delay-2 { animation-delay: 0.3s; }
        .animate-delay-3 { animation-delay: 0.5s; }
        .animate-delay-4 { animation-delay: 0.7s; }
        .animate-delay-5 { animation-delay: 0.9s; }
        .animate-delay-6 { animation-delay: 1.1s; }
        
        .simple-card {
            background: white;
            padding: 24px;
            border-radius: 8px;
            border: 2px solid #e5e7eb;
            margin-bottom: 16px;
            transition: all 0.3s ease;
        }
        
        .simple-card:hover {
            border-color: #3b82f6;
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15);
            transform: translateY(-4px);
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            background: #f8fafc;
            padding: 8px;
            border-radius: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 60px;
            background: transparent;
            border-radius: 8px;
            color: #64748b;
            font-weight: 500;
            font-size: 16px;
            padding: 0 24px;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: #e0f2fe;
            color: #3b82f6;
        }
        
        .stTabs [aria-selected="true"] {
            background: white;
            color: #3b82f6;
            border-bottom: 3px solid #3b82f6;
        }
    </style>
    """, unsafe_allow_html=True)


def render_animated_header():
    """Render animated main header"""
    st.markdown("""
    <div class="animate-fade" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                padding: 32px;
                border-radius: 12px;
                margin-bottom: 32px;
                box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);">
        <h1 style="color: white; text-align: center; margin: 0; font-size: 32px; font-weight: 700;
                   text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            📊 Comprehensive Analysis & Results
        </h1>
        <p style="color: #e0f2fe; text-align: center; margin: 12px 0 0 0; font-size: 16px;">
            Quantum Machine Learning Performance Evaluation
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_performance_summary_tab():
    """Render Performance Summary tab"""
    
    st.markdown("""
    <div class="animate-fade animate-delay-1" style="background: #3b82f6;
                padding: 18px;
                border-radius: 10px;
                margin-bottom: 24px;">
        <h2 style="color: white; margin: 0; font-size: 24px; font-weight: 600;">
            🏆 Top Performers
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    performers = [
        "QLSTM achieves comparable performance to LSTM with ~58% compression in training parameters and R² of 91%-92%",
        "QGRU performs comparably to GRU, achieving ~84% reduction in training parameters with R² of 89%-91%",
        "QNN-SE demonstrates improvement over ANN, especially in relative error minimization",
        "QNN-Ising outperforms ANN, though not as strongly as QNN-SE",
        "VQC is slightly comparable to ANN in R² and MAPE, showing marginal improvement",
        "QSVM achieves similar performance metrics as SVM - both perform comparably",
        "Hybrid QNN is resource-efficient with miniscule quantum layer, delivering best classification results"
    ]
    
    titles = ["QLSTM vs LSTM", "QGRU vs GRU", "QNN-SE vs ANN", "QNN-Ising vs ANN", "VQC vs ANN", "QSVM vs SVM", "Hybrid QNN vs Dense ANN"]

    cols = st.columns(2)
    for idx in range(6):
        delay = (idx % 4) + 2
        direction = "animate-slide-left" if idx % 2 == 0 else "animate-slide-right"
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="{direction} animate-delay-{delay} simple-card">
                <h3 style="color: #1e293b; margin: 0 0 12px 0; font-size: 18px; font-weight: 600;">
                    ✨ {titles[idx]}
                </h3>
                <p style="color: #000000; margin: 0; font-size: 16px; line-height: 1.6;">
                    {performers[idx]}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="animate-fade animate-delay-6 simple-card">
        <h3 style="color: #1e293b; margin: 0 0 12px 0; font-size: 18px; font-weight: 600;">
            ✨ {titles[6]}
        </h3>
        <p style="color: #374151; margin: 0; font-size: 16px; line-height: 1.6;">
            {performers[6]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="animate-fade animate-delay-1" style="background: #3b82f6;
                padding: 18px;
                border-radius: 10px;
                margin: 32px 0 24px 0;">
        <h2 style="color: white; margin: 0; font-size: 24px; font-weight: 600;">
            ⚖️ Trade-offs
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    tradeoffs = [
        ("QLSTM/QGRU", "Heavier but achieve the best quantum performance in Temperature Data"),
        ("HQNN/QNNs", "Lightweight achieve the best quantum performance in Rainfall Data"),
        ("QSVM/VQC", "Resource-efficient, but perform comparable to QNNs")
    ]
    
    cols = st.columns(3)
    for idx, (title, desc) in enumerate(tradeoffs):
        with cols[idx]:
            st.markdown(f"""
            <div class="animate-fade animate-delay-{idx + 2} simple-card">
                <h3 style="color: #000000; margin: 0 0 12px 0; font-size: 20px; font-weight: 600;">
                    ⚡ {title}
                </h3>
                <p style="color: #000000; margin: 0; font-size: 16px; line-height: 1.5;">
                    {desc}
                </p>
            </div>
            """, unsafe_allow_html=True)

def _render_training_params_section(classical_params, quantum_params,
                                    classical_label, quantum_label,
                                    section_title="Training Parameters"):
    import plotly.graph_objects as go

    fig_classical = go.Figure(go.Bar(
        x=list(classical_params.keys()),
        y=list(classical_params.values()),
        marker_color='#3B82F6',
        text=list(classical_params.values()),
        textposition='inside',
        textfont=dict(size=13, color='white'),
    ))
    fig_classical.update_layout(
        title=dict(text=f"<b>{classical_label}</b>", x=0.5, xanchor='center',
                   font=dict(size=15, color='#2c3e50')),
        yaxis_title="Number of Parameters",
        xaxis_title="Classical Models",
        plot_bgcolor='white', paper_bgcolor='white', height=420,
        bargap=0.6,
        bargroupgap=0.2,
        margin=dict(l=50, r=30, t=60, b=80),
        yaxis=dict(gridcolor='rgba(0,0,0,0.06)', tickfont=dict(size=12)),
        xaxis=dict(tickfont=dict(size=12)),
    )
    fig_classical.update_traces(marker_line_color='#1e40af', marker_line_width=1.2)

    fig_quantum = go.Figure(go.Bar(
        x=list(quantum_params.keys()),
        y=list(quantum_params.values()),
        marker_color='#8B5CF6',
        text=list(quantum_params.values()),
        textposition='inside',
        textfont=dict(size=13, color='white'),
    ))
    fig_quantum.update_layout(
        title=dict(text=f"<b>{quantum_label}</b>", x=0.5, xanchor='center',
                   font=dict(size=15, color='#2c3e50')),
        yaxis_title="Number of Parameters",
        xaxis_title="Quantum Models",
        plot_bgcolor='white', paper_bgcolor='white', height=420,
        bargap=0.6,
        bargroupgap=0.2,
        margin=dict(l=50, r=30, t=60, b=80),
        yaxis=dict(gridcolor='rgba(0,0,0,0.06)', tickfont=dict(size=12)),
        xaxis=dict(tickfont=dict(size=12)),
    )
    fig_quantum.update_traces(marker_line_color='#5b21b6', marker_line_width=1.2)

    st.markdown(f"""
    <div class="animate-fade" style="background: #3b82f6;
                padding: 16px; border-radius: 10px; margin: 32px 0 20px 0;">
        <h2 style="color: white; margin: 0; font-size: 22px; font-weight: 600;">
            📐 {section_title}
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_classical, use_container_width=True)
    with col2:
        st.plotly_chart(fig_quantum, use_container_width=True)
def render_quantum_resources_tab():
    """Render Quantum Resources tab"""
    
    st.markdown("""
    <div class="animate-fade animate-delay-1" style="background: #3b82f6;
                padding: 18px;
                border-radius: 10px;
                margin-bottom: 24px;">
        <h2 style="color: white; margin: 0; font-size: 24px; font-weight: 600;">
            🔬 Quantum Resource Estimates Of All Quantum Algorithms
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    fig_single, fig_multi, fig_depth = create_quantum_resource_charts(height=500)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="animate-fade animate-delay-1">', unsafe_allow_html=True)
        st.plotly_chart(fig_single, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="animate-fade animate-delay-2">', unsafe_allow_html=True)
        st.plotly_chart(fig_multi, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="animate-fade animate-delay-3">', unsafe_allow_html=True)
        st.plotly_chart(fig_depth, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
        # ---- Training Parameter Charts ----
    from config.constants import ALGORITHM_PARAMS

    classical_params = {k: v['classical'] for k, v in ALGORITHM_PARAMS.items()
                        if v['type'] == 'classical' and v.get('classical', 0) > 0}
    quantum_params   = {k: v.get('quantum', 0) + v.get('classical', 0)
                        for k, v in ALGORITHM_PARAMS.items()
                        if v['type'] in ('quantum', 'hybrid')
                        and (v.get('quantum', 0) + v.get('classical', 0)) > 0}

    _render_training_params_section(
        classical_params=classical_params,
        quantum_params=quantum_params,
        classical_label="Classical Models — Training Parameters (IMD)",
        quantum_label="Quantum / Hybrid Models — Training Parameters (IMD)",
        section_title="IMD Training Parameters Comparison"
    )

def create_ncmrwf_metrics_table():
    """Create NCMRWF metrics comparison table"""
    all_models = ["GRU", "LSTM",'ANN', "QGRU", "QLSTM",'QNN_IS_2.0',"Hybrid QNN_SE",'VQC']   # changing here
    metric_names = ["MSE", "RMSE", "MAE", "MAPE", "R² Score"]

    data = []
    for metric_name in metric_names:
        row = {"Metric": metric_name}
        for model in all_models:
            if model in NCMRWF_REGRESSION_METRICS:
                if metric_name == "MAPE":
                    # value = NCMRWF_REGRESSION_METRICS[model]["Mean Absolute Percentage Error (MAPE)"] * 100
                    value = NCMRWF_REGRESSION_METRICS[model]["Mean Absolute Percentage Error (MAPE)"] 

                    row[model] = f"{value:.4f}"
                elif metric_name == "MSE":
                    value = NCMRWF_REGRESSION_METRICS[model]["Mean Squared Error (MSE)"]
                    row[model] = f"{value:.4f}"
                elif metric_name == "RMSE":
                    value = NCMRWF_REGRESSION_METRICS[model]["Root Mean Squared Error (RMSE)"]
                    row[model] = f"{value:.4f}"
                elif metric_name == "MAE":
                    value = NCMRWF_REGRESSION_METRICS[model]["Mean Absolute Error (MAE)"]
                    row[model] = f"{value:.4f}"
                elif metric_name == "R² Score":
                    value = NCMRWF_REGRESSION_METRICS[model]["R² Score"]
                    row[model] = f"{value:.4f}"
            else:
                row[model] = "N/A"
        data.append(row)

    return pd.DataFrame(data)

def create_noise_table_by_algorithm(algorithm):
    """
    Create a single table for a specific algorithm showing all noise types
    Rows = Metrics, Columns = Without Noise + All Error Types
    """
    from config.constants import NOISE_METRICS, REGRESSION_METRICS
    
    # All error types
    error_types = [
        "Gate Rotation Error",
        "Amplitude Damping Error",
        "Initialization Error",
        "Thermal Relaxation Error",
        "Depolarizing Error",
        "Dephasing Error",
        "Readout Error"
    ]
    
    # All metrics to display
    metric_names = [
        "Mean Squared Error (MSE)",
        "Root Mean Squared Error (RMSE)",
        "Mean Absolute Error (MAE)",
        "Mean Absolute Percentage Error (MAPE)",
        "R² Score",
        "Adjusted R²"
    ]
    
    # Short metric names for display
    metric_display_names = {
        "Mean Squared Error (MSE)": "MSE",
        "Root Mean Squared Error (RMSE)": "RMSE",
        "Mean Absolute Error (MAE)": "MAE",
        "Mean Absolute Percentage Error (MAPE)": "MAPE",
        "R² Score": "R² Score",
        "Adjusted R²": "Adjusted R²"
    }
    
    data = []
    for metric_name in metric_names:
        row = {"📊 Metric": metric_display_names[metric_name]}
        
        # Add "Without Noise" column (from REGRESSION_METRICS)
        if algorithm in REGRESSION_METRICS:
            if metric_name in REGRESSION_METRICS[algorithm]:
                value = REGRESSION_METRICS[algorithm][metric_name]
                # if "MAPE" in metric_name:
                #     row["✨ Without Noise"] = f"{value:.2f}%"
                # else:
                row["✨ Without Noise"] = f"{value:.4f}"
            else:
                row["✨ Without Noise"] = "—"
        else:
            row["✨ Without Noise"] = "—"
        
        # Add each error type column
        for error_type in error_types:
            if error_type in NOISE_METRICS and algorithm in NOISE_METRICS[error_type]:
                if metric_name in NOISE_METRICS[error_type][algorithm]:
                    value = NOISE_METRICS[error_type][algorithm][metric_name]
                    # if "MAPE" in metric_name:
                    #     row[error_type] = f"{value:.2f}%"
                    # else:
                    #     row[error_type] = f"{value:.4f}"
                    row[error_type] = f"{value:.4f}"
                else:
                    row[error_type] = "—"
            else:
                row[error_type] = "—"
        
        data.append(row)
    
    return pd.DataFrame(data)

# added new function
def render_noise_analysis_tab():
    """
    Render Noise Analysis tab with dropdown to select algorithm
    """
    st.markdown("""
    <div class="animate-fade animate-delay-1" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 24px;">
        <h2 style="color: white; text-align: center; margin: 0; font-size: 26px; font-weight: 600;">
            🔬 Comprehensive Quantum Noise Analysis
        </h2>
        <p style="color: #e0d4ff; text-align: center; margin: 8px 0 0 0; font-size: 15px;">
            Temperature Prediction - Impact of Quantum Hardware Errors
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # All quantum algorithms
    # all_algorithms = ["QLSTM", "QGRU", "QSVM", "QNN_IS", "QNN_SE", "VQC", "Hybrid_QNN"]

    # Display names (full descriptive forms)
    algorithm_display_names = [
        "Quantum Long Short-Term Memory (QLSTM)",
        "Quantum Gated Recurrent Unit (QGRU)",
        "Quantum Support Vector Machine (QSVM)",
        "Quantum Neural Network - Ising (QNN-Ising)",
        "Quantum Neural Network - Strongly Entangling (QNN-SE)",
        "Variational Quantum Classifier (VQC)",
        "Hybrid Quantum Neural Network (Hybrid QNN)"
    ]
    # Mapping from display names to data keys
    algorithm_data_keys = {
        "Quantum Long Short-Term Memory (QLSTM)": "QLSTM",
        "Quantum Gated Recurrent Unit (QGRU)": "QGRU",
        "Quantum Support Vector Machine (QSVM)": "QSVM",
        "Quantum Neural Network - Ising (QNN-Ising)": "QNN_IS",
        "Quantum Neural Network - Strongly Entangling (QNN-SE)": "QNN_SE",
        "Variational Quantum Classifier (VQC)": "VQC",
        "Hybrid Quantum Neural Network (Hybrid QNN)": "Hybrid_QNN"
    }
    
    # Algorithm selector
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_algorithm_display = st.selectbox(
            "🎯 **Select Quantum Algorithm to Analyze:**",
            # all_algorithms,
            algorithm_display_names, 
            key="noise_algorithm_selector",
            help="View performance across all noise types for the selected algorithm"
        )
        # Convert display name to data key
        selected_algorithm = algorithm_data_keys[selected_algorithm_display]
    
    st.markdown("---")
    
    # Create and display table for selected algorithm
    st.markdown(f"""
    <div class="scroll-animate animate-delay-2" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                padding: 18px;
                border-radius: 10px;
                margin: 24px 0 16px 0;">
        <h3 style="color: white; margin: 0; font-size: 22px; font-weight: 600; text-align: center;">
            ⚛️ {selected_algorithm_display} - Performance Across All Noise Types
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    df_noise = create_noise_table_by_algorithm(selected_algorithm)
    
    if df_noise.empty:
        st.warning(f"⚠️ No data available for {selected_algorithm}")
    else:
        # Display table with special styling
        table_html = create_noise_comparison_table_html(df_noise)
        st.markdown(f'<div class="scroll-animate animate-delay-3">{table_html}</div>', unsafe_allow_html=True)
    
    # Key Insights section
    st.markdown("""
    <div class="scroll-animate" style="background: #3b82f6;
                padding: 18px;
                border-radius: 10px;
                margin: 32px 0 24px 0;">
        <h3 style="color: white; margin: 0; font-size: 20px; font-weight: 600;">
            📊 Noise Analysis Guide
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="simple-card">
            <h4 style="color: #ef4444; margin: 0 0 12px 0; font-size: 18px; font-weight: 600;">
                ⚠️ Error Types Tested
            </h4>
            <p style="color: #374151; margin: 0; font-size: 15px; line-height: 1.7;">
                <strong>Gate Rotation:</strong> Imperfect gate implementations<br>
                <strong>Amplitude Damping:</strong> Energy loss in qubits<br>
                <strong>Thermal Relaxation:</strong> Temperature-induced decoherence<br>
                <strong>Depolarizing:</strong> Random Pauli errors<br>
                <strong>Dephasing:</strong> Phase information loss<br>
                <strong>Initialization:</strong> Imperfect qubit preparation<br>
                <strong>Readout:</strong> Measurement errors
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="simple-card">
            <h4 style="color: #3b82f6; margin: 0 0 12px 0; font-size: 18px; font-weight: 600;">
                📋 Table Legend
            </h4>
            <p style="color: #374151; margin: 0; font-size: 15px; line-height: 1.7;">
                <strong>✨ Without Noise:</strong> Baseline ideal performance<br>
                <strong>"—"</strong> = Data not yet available<br>
                <strong>MSE/RMSE/MAE:</strong> Lower is better<br>
                <strong>MAPE:</strong> Lower percentage is better<br>
                <strong>R² Score:</strong> Closer to 1.0 is better<br>
                <strong>Adjusted R²:</strong> Accounts for model complexity
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("""
    💡 **Interpretation Guide:**
    - **Compare "Without Noise"** (green column) vs error columns to see degradation
    - **Smaller performance gaps** indicate better noise resilience
    - **R² Score > 0.85** under noise suggests good NISQ-era deployability
    - **Fewer "—" marks** indicate more comprehensive testing
    """)



def render_complete_metrics_tab(regression_metrics):
    """Render Complete Metrics tab with NCMRWF support"""
    
    # IMD Temperature Metrics
    st.markdown("""
    <div class="scroll-animate" style="background: #3b82f6;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 24px;">
        <h2 style="color: white; text-align: center; margin: 0; font-size: 26px; font-weight: 600;">
            📊 IMD Temperature Prediction - Complete Performance Metrics
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Display names (what user sees)
    display_names = [
        "LSTM", "GRU", "ANN", "Dense ANN", "SVM",
        "QLSTM", "QGRU", "QNN-SE", "QNN-Ising", "VQC", "QSVM", "Hybrid QNN"
    ]
    
    # Data keys (what we lookup in REGRESSION_METRICS)
    data_keys = {
        "LSTM": "LSTM",
        "GRU": "GRU",
        "ANN": "ANN",
        "Dense ANN": "Dense ANN",
        "SVM": "SVM",
        "QLSTM": "QLSTM",
        "QGRU": "QGRU",
        "QNN-SE": "QNN_SE",
        "QNN-Ising": "QNN_IS",
        "VQC": "VQC",
        "QSVM": "QSVM",
        "Hybrid QNN": "Hybrid_QNN"
    }
    
    metric_names = ["MSE", "RMSE", "MAE", "MAPE", "R² Score", "Adjusted R²"]

    data = []
    for metric_name in metric_names:
        row = {"Metric": metric_name}
        
        for display_name in display_names:
            data_key = data_keys[display_name]
            
            if data_key in regression_metrics:
                if metric_name == "MAPE":
                    # value = regression_metrics[data_key]["Mean Absolute Percentage Error (MAPE)"] * 100
                    value = regression_metrics[data_key]["Mean Absolute Percentage Error (MAPE)"] 
                    row[display_name] = f"{value:.2f}"
                elif metric_name == "MSE":
                    value = regression_metrics[data_key]["Mean Squared Error (MSE)"]
                    row[display_name] = f"{value:.4f}"
                elif metric_name == "RMSE":
                    value = regression_metrics[data_key]["Root Mean Squared Error (RMSE)"]
                    row[display_name] = f"{value:.4f}"
                elif metric_name == "MAE":
                    value = regression_metrics[data_key]["Mean Absolute Error (MAE)"]
                    row[display_name] = f"{value:.4f}"
                elif metric_name == "R² Score":
                    value = regression_metrics[data_key]["R² Score"]
                    row[display_name] = f"{value:.4f}"
                elif metric_name == "Adjusted R²":
                    value = regression_metrics[data_key]["Adjusted R²"]
                    row[display_name] = f"{value:.4f}"
            else:
                row[display_name] = "N/A"
        
        data.append(row)

    df_imd_metrics = pd.DataFrame(data)

    st.markdown("""
    <div class="scroll-animate animate-delay-1" style="background: #e0f2fe; 
                padding: 16px; 
                border-radius: 8px; 
                margin-bottom: 20px;">
        <p style="margin: 0; color: #000000; font-weight: 500; text-align: center; font-size: 15px;">
            <strong>
                🔷 Classical Models: LSTM, GRU, ANN, Dense ANN, SVM | 
                🔶 Quantum Models: QLSTM, QGRU, QNN-SE, QNN-Ising, VQC, QSVM, Hybrid QNN
            </strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    table_html = create_conclusion_metrics_table_html(df_imd_metrics, table_type="temperature")
    st.markdown(table_html, unsafe_allow_html=True)

    # Rainfall Metrics
    st.markdown("""
    <div class="scroll-animate" style="background: #3b82f6;
                padding: 20px;
                border-radius: 10px;
                margin: 32px 0 24px 0;">
        <h2 style="color: white; text-align: center; margin: 0; font-size: 26px; font-weight: 600;">
            📊 Complete Performance Metrics - Rainfall Classification
        </h2>
    </div>
    """, unsafe_allow_html=True)

    from visualization.tables import create_rainfall_conclusion_metrics_table
    df_rainfall = create_rainfall_conclusion_metrics_table(CLASSIFICATION_METRICS)
    
    table_html = create_conclusion_metrics_table_html(df_rainfall, table_type="rainfall")
    st.markdown(table_html, unsafe_allow_html=True)

    # Parameter Comparison
    st.markdown('<div class="scroll-animate animate-delay-2">', unsafe_allow_html=True)
    render_parameters_comparison_section()
    st.markdown('</div>', unsafe_allow_html=True)
   


def render_conclusion_tab_content():
    """Render Conclusion tab content"""
    
    st.markdown("""
    <div class="scroll-animate" 
         style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                padding: 32px;
                border-radius: 12px;
                margin-bottom: 32px;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);">
        <h2 style="color: white; margin: 0 0 16px 0; font-size: 28px; font-weight: 700; text-align: center;">
            🎓 Final Conclusion
        </h2>
        <p style="color: #e0f2fe; text-align: center; font-size: 16px; margin: 0;">
            Comprehensive Analysis of Classical vs Quantum Machine Learning Models
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="scroll-animate animate-delay-1 simple-card">
        <h3 style="color: #1e293b; margin: 0 0 16px 0; font-size: 20px; font-weight: 600;">
            📋 Overview
        </h3>
        <p style="color: #000000; margin: 0; font-size: 16px; line-height: 1.8; text-align: justify;">
            The comparative analysis of classical, quantum, and hybrid quantum-classical models demonstrates 
            a clear hierarchy in predictive accuracy, computational efficiency, and hardware feasibility for 
            NISQ-era deployment.
        </p>
    </div>
    """, unsafe_allow_html=True)

    findings = [
        {
            "title": "Classical Deep Networks Performance",
            "content": "Classical deep networks such as LSTM, Dense ANN, and GRU continue to show strong baseline performance in both regression and rainfall-classification tasks. However, their advantage comes with a substantial parameter footprint—ranging from hundreds (LSTM 460, GRU 1,073) to tens of thousands of trainable weights (Dense ANN 17,653).",
            "icon": "🏛️"
        },
        {
            "title": "Pure Quantum Models",
            "content": "The family of pure quantum neural models (QGRU, QLSTM, QNN-SE, QNN-IS, VQC, QSVM) achieves significant model-size compression, with parameter counts reduced by up to an order of magnitude. However, these models also exhibit performance trade-offs, typically falling short of classical LSTM/ANN in both regression and classification metrics.",
            "icon": "⚛️"
        },
        {
            "title": "Hybrid Classical-Quantum Neural Network (HQNN)",
            "content": "Among all evaluated models, the Hybrid Classical Quantum Neural Network (HQNN) distinctly emerges as the most balanced and practically deployable architecture. It consistently outperforms all quantum-only algorithms in both regression and classification accuracy, while remaining competitive with strong classical baselines.",
            "icon": "🔄"
        },
        {
            "title": "Circuit Efficiency",
            "content": "The circuit-profiling results further reinforce HQNN's suitability for real-hardware implementation. Its single-qubit gate count, multi-qubit gate count, and circuit depth remain among the lowest within the quantum category. This low-overhead quantum footprint directly translates into improved robustness against decoherence and faster execution.",
            "icon": "⚡"
        }
    ]

    for idx, finding in enumerate(findings):
        st.markdown(f"""
        <div class="scroll-animate animate-delay-{idx + 2} simple-card">
            <h3 style="color: #000000; margin: 0 0 12px 0; font-size: 20px; font-weight: 600;">
                {finding['icon']} {finding['title']}
            </h3>
            <p style="color: #000000; margin: 0; font-size: 16px; line-height: 1.7; text-align: justify;">
                {finding['content']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="scroll-animate" 
         style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                padding: 32px;
                border-radius: 12px;
                margin-top: 32px;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);">
        <h3 style="color: white; margin: 0 0 16px 0; font-size: 24px; font-weight: 700;">
            🎯 Overall Conclusion
        </h3>
        <p style="color: #e0f2fe; margin: 0; font-size: 16px; line-height: 1.8; text-align: justify;">
            While purely quantum models demonstrate the feasibility and compression advantage of QML, 
            their performance gap indicates that hybridization remains the most effective route forward. 
            The HQNN successfully combines the representational strength of classical deep learning with 
            the expressiveness of quantum feature transformations, achieving superior accuracy, minimal 
            quantum resource requirements, and excellent NISQ-era implementability. This positions the 
            hybrid architecture as the most promising candidate for near-term quantum-enhanced weather 
            forecasting systems.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_conclusion_tab(regression_metrics):
    """Main function to render the complete conclusion tab with IMD/NCMRWF dropdown"""
    inject_custom_css()
    
    # ==================== HEADER WITH DROPDOWN ====================
    col_title, col_spacer, col_dropdown = st.columns([3, 0.5, 1.5])
    
    with col_title:
        st.markdown(
            '<h3 style="color: #1f2937; margin: 0; padding: 10px 0;">📊 Comprehensive Analysis & Results</h3>', unsafe_allow_html=True)
    
    with col_spacer:
        st.write("")
    
    with col_dropdown:
        st.markdown("<div style='margin-top: 10px;'>", unsafe_allow_html=True)
        data_source = st.selectbox(
            "**📂 Data Source:**",
            options=["IMD", "NCMRWF"],
            key="conclusion_data_source",
            help="Select dataset for analysis"
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ==================== CONDITIONAL TAB RENDERING ====================
    if data_source == "IMD":
        tab1, tab2, tab3 = st.tabs([
            "🏆 Performance Summary",
            "🔬 Quantum Resources",
            "🔬 Noise Analysis",
        ])
        
        with tab1:
            render_performance_summary_tab()
            st.markdown("---")
            render_complete_metrics_tab(regression_metrics)
            st.markdown("---")
            render_conclusion_tab_content()
        
        with tab2:
            render_quantum_resources_tab()
        
        with tab3:
            render_noise_analysis_tab()
    
    else:  # NCMRWF
        tab1, tab2 = st.tabs([
            "🏆 Performance Summary",
            "🔬 Quantum Resources",
        ])
        
        with tab1:
            render_ncmrwf_performance_summary_tab()
            st.markdown("---")
            render_ncmrwf_complete_metrics_tab()
            st.markdown("---")
            render_ncmrwf_conclusion_tab_content()
        
        with tab2:
            render_ncmrwf_quantum_resources_tab()
# ==================== NCMRWF-SPECIFIC TAB FUNCTIONS ====================

def render_ncmrwf_performance_summary_tab():
    """Render NCMRWF Performance Summary tab"""
    
    st.markdown("""
    <div class="animate-fade animate-delay-1" style="background: #3b82f6;
                padding: 18px;
                border-radius: 10px;
                margin-bottom: 24px;">
        <h2 style="color: white; margin: 0; font-size: 24px; font-weight: 600;">
            🏆 NCMRWF Top Performers
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    performers = [
        ("QGRU vs GRU", "QGRU achieves **94.7% R² score** with only **677 quantum parameters** compared to GRU's 1,649 classical parameters — achieving **59% parameter compression** while **outperforming** the classical model", "🥇"),
        ("QLSTM vs LSTM", "QLSTM achieves **94.6% R² score** with **877 quantum parameters** compared to LSTM's 2,129 classical parameters — achieving **59% parameter compression** with comparable performance", "🥈"),
        ("Quantum Efficiency", "Both quantum models demonstrate **superior parameter efficiency** and **competitive accuracy**, validating the effectiveness of quantum approaches for weather forecasting", "⚡"),
        ("Circuit Complexity", "**QLSTM** has the lowest circuit depth (8) and fewest multi-qubit gates (16), making it the most **NISQ-friendly** model for near-term quantum hardware", "🔬")
    ]
    
    cols = st.columns(2)
    for idx, (title, desc, icon) in enumerate(performers):
        delay = (idx % 2) + 2
        direction = "animate-slide-left" if idx % 2 == 0 else "animate-slide-right"
        
        # ✅ Highlight QGRU (best performer)
        border_color = "#10b981" if "QGRU" in title and idx == 0 else "#e5e7eb"
        bg_color = "#f0fdf4" if "QGRU" in title and idx == 0 else "white"
        
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="{direction} animate-delay-{delay} simple-card" 
                 style="border: 2px solid {border_color}; background: {bg_color};">
                <h3 style="color: #1e293b; margin: 0 0 12px 0; font-size: 18px; font-weight: 600;">
                    {icon} {title}
                </h3>
                <p style="color: #000000; margin: 0; font-size: 16px; line-height: 1.6;">
                    {desc}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="animate-fade animate-delay-3" style="background:#3b82f6 ;
                padding: 18px;
                border-radius: 10px;
                margin: 32px 0 24px 0;">
        <h2 style="color: white; margin: 0; font-size: 24px; font-weight: 600;">
            📊 Key Insights
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="simple-card" style="border: 2px solid #10b981; background: #f0fdf4;">
        <h4 style="color: #047857; margin: 0 0 12px 0; font-size: 18px; font-weight: 600;">
            🎯 Winner: QGRU
        </h4>
        <p style="color: #000000; margin: 0; font-size: 16px; line-height: 1.7;">
            <strong>QGRU emerges as the best overall NCMRWF model:</strong><br>
            ✅ Highest R² Score (94.7%)<br>
            ✅ 59% parameter reduction vs classical GRU<br>
            ✅ Superior accuracy with quantum efficiency<br>
            ✅ Practical for NISQ-era deployment
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_ncmrwf_quantum_resources_tab():
    """Render NCMRWF Quantum Resources tab"""
    
    st.markdown("""
    <div class="animate-fade animate-delay-1" style="background:#3b82f6 ;
                padding: 18px;
                border-radius: 10px;
                margin-bottom: 24px;">
        <h2 style="color: white; margin: 0; font-size: 24px; font-weight: 600;">
            🔬 NCMRWF Quantum Resource Estimates
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    from visualization.charts import create_ncmrwf_quantum_resource_charts
    fig_single, fig_multi, fig_depth = create_ncmrwf_quantum_resource_charts(height=400)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.plotly_chart(fig_single, width='stretch')
    
    with col2:
        st.plotly_chart(fig_multi, width='stretch')
    
    with col3:
        st.plotly_chart(fig_depth, width='stretch')
    
    st.success("""
    **🌟 QLSTM is the most hardware-efficient model** with the lowest circuit depth (8) and 
    minimal multi-qubit gates (16), making it ideal for near-term quantum devices.
    """)
    # ---- Training Parameter Charts (mode-aware) ----
    from config.constants import NCMRWF_ALGORITHM_PARAMS, NCMRWF_UNIVARIATE_ALGORITHM_PARAMS

    analysis_mode = st.radio(
        "**📂 Select Analysis Mode for Training Parameters:**",
        options=["Multivariate", "Univariate"],
        horizontal=True,
        key="ncmrwf_qr_analysis_mode"
    )

    if analysis_mode == "Multivariate":
        active_params = NCMRWF_ALGORITHM_PARAMS
        c_label = "Classical Models — Training Parameters (NCMRWF Multivariate)"
        q_label = "Quantum / Hybrid Models — Training Parameters (NCMRWF Multivariate)"
        title   = "NCMRWF Multivariate Training Parameters Comparison"
    else:
        active_params = NCMRWF_UNIVARIATE_ALGORITHM_PARAMS
        c_label = "Classical Models — Training Parameters (NCMRWF Univariate)"
        q_label = "Quantum Models — Training Parameters (NCMRWF Univariate)"
        title   = "NCMRWF Univariate Training Parameters Comparison"

    classical_params = {k: v['classical'] for k, v in active_params.items()
                        if v['type'] == 'classical' and v.get('classical', 0) > 0}
    quantum_params   = {k: v.get('quantum', 0) + v.get('classical', 0)
                        for k, v in active_params.items()
                        if v['type'] in ('quantum', 'hybrid')
                        and (v.get('quantum', 0) + v.get('classical', 0)) > 0}

    _render_training_params_section(classical_params, quantum_params, c_label, q_label, title)

def render_ncmrwf_complete_metrics_tab():
    """Render NCMRWF Complete Metrics tab"""
    
    st.markdown("""
    <div class="scroll-animate" style="background: #3b82f6;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 24px;">
        <h2 style="color: white; text-align: center; margin: 0; font-size: 26px; font-weight: 600;">
            📊 NCMRWF Temperature Prediction - Complete Performance Metrics
        </h2>
    </div>
    """, unsafe_allow_html=True)

    df_ncmrwf_metrics = create_ncmrwf_metrics_table()

    st.markdown("""
    <div class="scroll-animate animate-delay-1" style="background: #d1fae5; 
                padding: 16px; 
                border-radius: 8px; 
                margin-bottom: 20px;">
        <p style="margin: 0; color: #000000; font-weight: 500; text-align: center; font-size: 15px;">
            <strong>
                🔷 Classical Models: GRU, LSTM, ANN | 
                🔶 Quantum Models: QGRU, QLSTM, Hybrid QNN_IS, Hybrid QNN_SE
            </strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ✅ USE NCMRWF-SPECIFIC TABLE FUNCTION
    table_html = create_ncmrwf_metrics_table_html(df_ncmrwf_metrics)
    st.markdown(table_html, unsafe_allow_html=True)
    
    # ✅ Highlight best performers
    st.markdown("### 🏆 Performance Highlights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="simple-card" style="border: 2px solid #10b981; background: #f0fdf4;">
            <h4 style="color: #047857; margin: 0 0 8px 0;">🥇 Best R² Score: QGRU</h4>
            <p style="color: #000000; margin: 0; font-size: 15px;">
                <strong>94.72%</strong> — Highest accuracy among all models
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="simple-card" style="border: 2px solid #3b82f6;">
            <h4 style="color: #1e40af; margin: 0 0 8px 0;">🥈 Best Efficiency: QLSTM</h4>
            <p style="color: #000000; margin: 0; font-size: 15px;">
                <strong>94.59% R²</strong> with lowest circuit depth
            </p>
        </div>
        """, unsafe_allow_html=True)
def render_ncmrwf_conclusion_tab_content():
    """Render NCMRWF Conclusion content"""
    
    st.markdown("""
    <div class="scroll-animate" 
         style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                padding: 32px;
                border-radius: 12px;
                margin-bottom: 32px;
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">
        <h2 style="color: white; margin: 0 0 16px 0; font-size: 28px; font-weight: 700; text-align: center;">
            🎓 NCMRWF Final Conclusion
        </h2>
        <p style="color: #d1fae5; text-align: center; font-size: 16px; margin: 0;">
            Quantum Models Outperform Classical Baselines
        </p>
    </div>
    """, unsafe_allow_html=True)

    findings = [
        {
            "title": "QGRU: Best Overall Performance",
            "content": "QGRU achieves the highest R² score of **94.72%**, surpassing its classical counterpart (GRU: 93.22%) while using only **677 quantum parameters** compared to GRU's **1,649 classical parameters**. This represents a **59% parameter compression** with **improved accuracy**, demonstrating quantum advantage in weather forecasting.",
            "icon": "🥇"
        },
        {
            "title": "QLSTM: Most Hardware-Efficient",
            "content": "QLSTM delivers excellent performance (R²: **94.59%**) with the lowest circuit complexity: only **8 circuit depth**, **16 multi-qubit gates**, and **64 single-qubit gates**. This minimal quantum footprint makes QLSTM the most **NISQ-deployable** model for near-term quantum hardware.",
            "icon": "🔬"
        },
        {
            "title": "Quantum Parameter Efficiency",
            "content": "Both QGRU and QLSTM achieve approximately **59% parameter reduction** compared to their classical counterparts. QGRU uses **677 parameters** vs GRU's **1,649**, and QLSTM uses **877 parameters** vs LSTM's **2,129**. This dramatic compression demonstrates quantum computing's ability to learn complex patterns with fewer trainable weights.",
            "icon": "⚡"
        },
        {
            "title": "Practical Quantum Advantage",
            "content": "The NCMRWF results provide clear evidence of **practical quantum advantage**: quantum models achieve better or comparable accuracy with significantly fewer parameters and acceptable circuit complexity. This validates quantum machine learning as a viable approach for real-world weather forecasting applications.",
            "icon": "🎯"
        }
    ]
    # ✅ NOW the for loop is OUTSIDE the list definition
    for idx, finding in enumerate(findings):
        border_color = "#10b981" if idx == 0 else "#e5e7eb"
        bg_color = "#f0fdf4" if idx == 0 else "white"
        
        st.markdown(f"""
        <div class="scroll-animate animate-delay-{idx + 2} simple-card" 
             style="border: 2px solid {border_color}; background: {bg_color};">
            <h3 style="color: #000000; margin: 0 0 12px 0; font-size: 20px; font-weight: 600;">
                {finding['icon']} {finding['title']}
            </h3>
            <p style="color: #000000; margin: 0; font-size: 16px; line-height: 1.7; text-align: justify;">
                {finding['content']}
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="scroll-animate" 
         style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                padding: 32px;
                border-radius: 12px;
                margin-top: 32px;
                box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">
        <h3 style="color: white; margin: 0 0 16px 0; font-size: 24px; font-weight: 700;">
            🎯 NCMRWF Overall Conclusion
        </h3>
        <p style="color: #d1fae5; margin: 0; font-size: 16px; line-height: 1.8; text-align: justify;">
            The NCMRWF dataset validation confirms that <strong>quantum recurrent neural networks (QGRU, QLSTM) 
            deliver superior performance compared to classical models</strong> while maintaining practical 
            hardware requirements for NISQ-era devices. <strong>QGRU emerges as the best overall model</strong> 
            with highest accuracy and reasonable circuit complexity, while <strong>QLSTM offers the most 
            hardware-efficient solution</strong> for deployment on current quantum processors. These results 
            establish quantum machine learning as a <strong>viable and advantageous approach</strong> for 
            operational weather forecasting systems.
        </p>
    </div>
    """, unsafe_allow_html=True)

            