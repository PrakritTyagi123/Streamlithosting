# visualization/tables.py
"""
Table creation functions
"""
import pandas as pd
import streamlit as st
from config.constants import REGRESSION_METRICS, IDEAL_VALUES, RAINFALL_IDEAL_VALUES,CLASSIFICATION_METRICS,NOISE_METRICS
# ✅ NEW (CORRECT)

def create_metrics_table_with_state():
    """Create metrics table that shows structure always but populates values based on generated predictions"""
    metric_names = [
        "Mean Squared Error (MSE)",
        "Root Mean Squared Error (RMSE)", 
        "Mean Absolute Error (MAE)",
        "Mean Absolute Percentage Error (MAPE)",
        "R² Score",
        "Adjusted R²"
    ]
    
    classical_generated = (st.session_state.classical_data and 
                          st.session_state.classical_data['algorithm'] != "Select Classical Algorithm")
    quantum_generated = (st.session_state.quantum_data and 
                        st.session_state.quantum_data['algorithm'] != "Select Quantum Algorithm")
    
    classical_values = ["—"] * len(metric_names)
    quantum_values = ["—"] * len(metric_names)
    ideal_values = ["—"] * len(metric_names)
    
    classical_header = "Classical Algorithm"
    quantum_header = "Quantum Algorithm"
    
    if classical_generated:
        algorithm = st.session_state.classical_data['algorithm']
        classical_header = f"Classical ({algorithm})"

        # ✅ CHANGE 1: Use metrics_key instead of algorithm
        metrics_key = st.session_state.classical_data.get('metrics_key', algorithm)
        # ✅ CHANGE 2: Look up using metrics_key
        if metrics_key in REGRESSION_METRICS:
            classical_data = REGRESSION_METRICS[metrics_key]
            for i, metric in enumerate(metric_names):
                if metric in classical_data:
                    value = classical_data[metric]
                    # if metric == "Mean Absolute Percentage Error (MAPE)":
                    #     classical_values[i] = f"{value:.3f} ({value*100:.1f}%)"
                    # else:
                    classical_values[i] = f"{value:.3f}"
        
        # if algorithm in REGRESSION_METRICS:
        #     classical_data = REGRESSION_METRICS[algorithm]
        #     for i, metric in enumerate(metric_names):
        #         if metric in classical_data:
        #             value = classical_data[metric]
        #             if metric == "Mean Absolute Percentage Error (MAPE)":
        #                 classical_values[i] = f"{value:.3f} ({value*100:.1f}%)"
        #             else:
        #                 classical_values[i] = f"{value:.3f}"
    
    if quantum_generated:
        algorithm = st.session_state.quantum_data['algorithm']
        quantum_header = f"Quantum ({algorithm})"

         # ✅ CHANGE 3: Use metrics_key instead of algorithm
        metrics_key = st.session_state.quantum_data.get('metrics_key', algorithm)
        
        # if algorithm in REGRESSION_METRICS:
        #     quantum_data = REGRESSION_METRICS[algorithm]
        #     for i, metric in enumerate(metric_names):
        #         if metric in quantum_data:
        #             value = quantum_data[metric]
        #             if metric == "Mean Absolute Percentage Error (MAPE)":
        #                 quantum_values[i] = f"{value:.3f} ({value*100:.1f}%)"
        #             else:
        #                 quantum_values[i] = f"{value:.3f}"
        # ✅ CHANGE 4: Look up using metrics_key
        if metrics_key in REGRESSION_METRICS:
            quantum_data = REGRESSION_METRICS[metrics_key]
            for i, metric in enumerate(metric_names):
                if metric in quantum_data:
                    value = quantum_data[metric]
                    # if metric == "Mean Absolute Percentage Error (MAPE)":
                    #     quantum_values[i] = f"{value:.3f} ({value*100:.1f}%)"
                    # else:
                    quantum_values[i] = f"{value:.3f}"
    
    if classical_generated or quantum_generated:
        ideal_values = [IDEAL_VALUES[metric] for metric in metric_names]
    
    df = pd.DataFrame({
        'Metric': metric_names,
        classical_header: classical_values,
        quantum_header: quantum_values,
        'Ideal Value': ideal_values
    })
    
    return df, classical_header, quantum_header

############ for rainfall 
def create_rainfall_metrics_table(classical_metrics, quantum_metrics, classical_algo, quantum_algo):
    """
    Create a comparison table for rainfall classification metrics
    
    Args:
        classical_metrics: Dictionary with classical algorithm metrics
        quantum_metrics: Dictionary with quantum algorithm metrics
        classical_algo: Classical algorithm name
        quantum_algo: Quantum algorithm name
        
    Returns:
        DataFrame with formatted metrics
    """
    
     
    metric_names = [
        'Accuracy',
        'Precision (No Rain)',
        'Recall (No Rain)',
        'F1-Score (No Rain)',
        'Precision (Rain)',
        'Recall (Rain)',
        'F1-Score (Rain)'
    ]
    
    metrics_data = {
        'Metric': metric_names
    }
    # print("DEBUG - metrics_data:", metrics_data)
    
    # Add classical metrics
    if classical_metrics and classical_algo != "Select Classical Algorithm":
        # print("DEBUG classical_algo:", classical_algo)
        # print("DEBUG classical_metrics:", classical_metrics)
        # print("DEBUG metrics_data:", metrics_data)
        metrics_data[f'{classical_algo}'] = [
            f"{classical_metrics.get('Accuracy', 0):.4f}",
            f"{classical_metrics.get('Precision (No Rain)', 0):.4f}",
            f"{classical_metrics.get('Recall (No Rain)', 0):.4f}",
            f"{classical_metrics.get('F1-Score (No Rain)', 0):.4f}",
            f"{classical_metrics.get('Precision (Rain)', 0):.4f}",
            f"{classical_metrics.get('Recall (Rain)', 0):.4f}",
            f"{classical_metrics.get('F1-Score (Rain)', 0):.4f}"
        ]
    else:
        metrics_data[f'{classical_algo}'] = ['N/A'] * 7
    
    # Add quantum metrics
    if quantum_metrics and quantum_algo != "Select Quantum Algorithm":
        metrics_data[quantum_algo] = [
            f"{quantum_metrics.get('Accuracy', 0):.4f}",
            f"{quantum_metrics.get('Precision (No Rain)', 0):.4f}",
            f"{quantum_metrics.get('Recall (No Rain)', 0):.4f}",
            f"{quantum_metrics.get('F1-Score (No Rain)', 0):.4f}",
            f"{quantum_metrics.get('Precision (Rain)', 0):.4f}",
            f"{quantum_metrics.get('Recall (Rain)', 0):.4f}",
            f"{quantum_metrics.get('F1-Score (Rain)', 0):.4f}"
        ]
    else:
        metrics_data[f'{quantum_algo}'] = ['N/A'] * 7
    # ADD IDEAL VALUES COLUMN
    if (classical_metrics and classical_algo != "Select Classical Algorithm") or \
       (quantum_metrics and quantum_algo != "Select Quantum Algorithm"):
        metrics_data['Ideal Value'] = [RAINFALL_IDEAL_VALUES[metric] for metric in metric_names]
    else:
        metrics_data['Ideal Value'] = ['—'] * 7
    
    df = pd.DataFrame(metrics_data)
    return df


def create_rainfall_metrics_table_with_state():
    """
    Create metrics table using session state data for rainfall predictions
    
    Returns:
        DataFrame, classical header, quantum header
    """
    classical_algo = "Select Classical Algorithm"
    quantum_algo = "Select Quantum Algorithm"
    classical_metrics = None
    quantum_metrics = None

    # Get classical data from session state
    if st.session_state.get('classical_rain_data'):
        if st.session_state.classical_rain_data and st.session_state.classical_rain_data.get('algorithm'):
            classical_algo = st.session_state.classical_rain_data['algorithm']
            # ✅ FIX: Use metrics_key if available (for algorithms with different display names)
            metrics_key = st.session_state.classical_rain_data.get('metrics_key', classical_algo)
            classical_metrics = st.session_state.classical_rain_data.get('metrics')
             # Try to get metrics directly first, otherwise look up from CLASSIFICATION_METRICS
            classical_metrics = st.session_state.classical_rain_data.get('metrics')
            if not classical_metrics:
                from config.constants import CLASSIFICATION_METRICS
                if metrics_key in CLASSIFICATION_METRICS:
                    classical_metrics = CLASSIFICATION_METRICS[metrics_key]
    # Get quantum data from session state
    if st.session_state.get('quantum_rain_data'):
        if st.session_state.quantum_rain_data and st.session_state.quantum_rain_data.get('algorithm'):
            quantum_algo = st.session_state.quantum_rain_data['algorithm']
            quantum_metrics = st.session_state.quantum_rain_data.get('metrics')
            
            # ✅ FIX: Use metrics_key if available
            metrics_key = st.session_state.quantum_rain_data.get('metrics_key', quantum_algo)
            
            # Try to get metrics directly first, otherwise look up from CLASSIFICATION_METRICS
            quantum_metrics = st.session_state.quantum_rain_data.get('metrics')
            if not quantum_metrics:
                from config.constants import CLASSIFICATION_METRICS
                if metrics_key in CLASSIFICATION_METRICS:
                    quantum_metrics = CLASSIFICATION_METRICS[metrics_key]
   
    
    df = create_rainfall_metrics_table(
        classical_metrics, 
        quantum_metrics,
        classical_algo,
        quantum_algo
    )
    
    return df, classical_algo, quantum_algo

# def create_conclusion_metrics_table_html(df_all_metrics):
#     """Create HTML table for conclusion tab with all models comparison"""
    
#     # Get column names
#     columns = df_all_metrics.columns.tolist()
    
#     html = f"""
#     <style>
#         .conclusion-metrics-table {{
#             width: 98%;
#             margin: 20px auto;
#             border-collapse: collapse;
#             background: white;
#             border-radius: 12px;
#             overflow: hidden;
#             box-shadow: 0 4px 15px rgba(30, 64, 175, 0.1);
#         }}
#         .conclusion-metrics-table thead th {{
#             background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
#             color: white !important;
#             font-weight: 700 !important;
#             font-size: 0.9rem !important;
#             padding: 0.9rem 0.6rem !important;
#             text-align: center !important;
#             border: none !important;
#             border-right: 1px solid rgba(255,255,255,0.2) !important;
#         }}
#         .conclusion-metrics-table thead th:first-child {{
#             text-align: left !important;
#             padding-left: 1rem !important;
#         }}
#         .conclusion-metrics-table tbody td {{
#             color: #000000 !important;
#             font-weight: 500 !important;
#             font-size: 0.85rem !important;
#             padding: 0.7rem 0.6rem !important;
#             border-bottom: 1px solid #e0f2fe !important;
#             text-align: center !important;
#         }}
#         .conclusion-metrics-table tbody td:first-child {{
#             font-weight: 600 !important;
#             text-align: left !important;
#             background: #f8fafc !important;
#             color: #000000 !important;
#             padding-left: 1rem !important;
#         }}
#         .conclusion-metrics-table tbody td:not(:first-child) {{
#             background: #f0f9ff !important;
#         }}
#         .conclusion-metrics-table tbody tr:hover {{
#             background: #eff6ff !important;
#         }}
#         .conclusion-metrics-table tbody tr:hover td {{
#             color: #000000 !important;
#         }}
#         .conclusion-metrics-table tbody tr:hover td:not(:first-child) {{
#             background: #dbeafe !important;
#         }}
#     </style>
#     <table class="conclusion-metrics-table">
#         <thead>
#             <tr>
#     """
    
#     # Add headers
#     for col in columns:
#         if col == "Metric":
#             html += f"<th>📊 {col}</th>"
#         else:
#             html += f"<th>{col}</th>"
    
#     html += """
#             </tr>
#         </thead>
#         <tbody>
#     """
    
#     # Add data rows
#     for _, row in df_all_metrics.iterrows():
#         html += "<tr>"
#         for val in row:
#             html += f"<td>{val}</td>"
#         html += "</tr>"
    
#     html += """
#         </tbody>
#     </table>
#     """
    
#     return html
# def create_conclusion_metrics_table_html(df_all_metrics):
#     """Create HTML table with color-coded columns for classical/quantum and best performers"""
    
#     columns = df_all_metrics.columns.tolist()
    
#     # Define classical and quantum algorithms
#     classical_algos = ["LSTM", "GRU", "ANN", "Dense ANN", "SVM"]
#     quantum_algos = ["QLSTM", "QGRU", "QNN-SE", "QNN-Ising", "VQC", "QSVM", "Hybrid QNN"]
    
#     html = f"""
#     <style>
#         .conclusion-metrics-table {{
#             width: 98%;
#             margin: 20px auto;
#             border-collapse: collapse;
#             background: white;
#             border-radius: 12px;
#             overflow: hidden;
#             box-shadow: 0 4px 15px rgba(30, 64, 175, 0.1);
#         }}
#         .conclusion-metrics-table thead th {{
#             color: white !important;
#             font-weight: 700 !important;
#             font-size: 0.9rem !important;
#             padding: 0.9rem 0.6rem !important;
#             text-align: center !important;
#             border: none !important;
#             border-right: 1px solid rgba(255,255,255,0.2) !important;
#         }}
#         .conclusion-metrics-table thead th:first-child {{
#             background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
#             text-align: left !important;
#             padding-left: 1rem !important;
#         }}
#         /* Classical algorithm headers - Blue gradient */
#         .classical-header {{
#             background: linear-gradient(135deg, #3b82f6, #60a5fa) !important;
#         }}
#         /* Quantum algorithm headers - Purple gradient */
#         .quantum-header {{
#             background: linear-gradient(135deg, #8b5cf6, #a78bfa) !important;
#         }}
#         .conclusion-metrics-table tbody td {{
#             color: #000000 !important;
#             font-weight: 500 !important;
#             font-size: 0.85rem !important;
#             padding: 0.7rem 0.6rem !important;
#             border-bottom: 1px solid #e0f2fe !important;
#             text-align: center !important;
#         }}
#         .conclusion-metrics-table tbody td:first-child {{
#             font-weight: 600 !important;
#             text-align: left !important;
#             background: #f8fafc !important;
#             color: #000000 !important;
#             padding-left: 1rem !important;
#         }}
#         /* Classical columns - light blue */
#         .classical-col {{
#             background: #dbeafe !important;
#         }}
#         /* Quantum columns - light purple */
#         .quantum-col {{
#             background: #ede9fe !important;
#         }}
        
#         .conclusion-metrics-table tbody tr:hover {{
#             background: #eff6ff !important;
#         }}
#     </style>
#     <table class="conclusion-metrics-table">
#         <thead>
#             <tr>
#                 <th>📊 Metric</th>
#     """
    
#     # Add column headers with appropriate classes
#     for col in columns[1:]:  # Skip "Metric" column
#         if col in classical_algos:
#             html += f'<th class="classical-header">{col}</th>'
#         elif col in quantum_algos:
#             html += f'<th class="quantum-header">{col}</th>'
#         else:
#             html += f'<th>{col}</th>'
    
#     html += """
#             </tr>
#         </thead>
#         <tbody>
#     """
    
#     # Add data rows with best performer highlighting
#     for _, row in df_all_metrics.iterrows():
#         html += "<tr>"
        
#         metric_name = row.iloc[0]
#         html += f"<td>{metric_name}</td>"
        
#         # Get numeric values for comparison (skip first column which is metric name)
#         values = []
#         for val in row.iloc[1:]:
#             if val != "N/A" and val != "—":
#                 # Extract numeric value (remove % if present)
#                 clean_val = val.replace('%', '').strip()
#                 try:
#                     values.append(float(clean_val))
#                 except:
#                     values.append(None)
#             else:
#                 values.append(None)
        
#         # # Determine best value based on metric type
#         # best_idx = None
#         # if values and any(v is not None for v in values):
#         #     valid_values = [v for v in values if v is not None]
#         #     if "MAPE" in metric_name or "MSE" in metric_name or "RMSE" in metric_name or "MAE" in metric_name:
#         #         # Lower is better
#         #         best_value = min(valid_values)
#         #     else:
#         #         # Higher is better (R², Adjusted R², Accuracy, Precision, Recall, F1)
#         #         best_value = max(valid_values)
            
#         #     best_idx = values.index(best_value) if best_value in values else None
        
#         # Add data cells
#         for idx, (col, val) in enumerate(zip(columns[1:], row.iloc[1:])):
#             cell_class = ""
            
#             # Determine column type
#             if col in classical_algos:
#                 cell_class = "classical-col"
#             elif col in quantum_algos:
#                 cell_class = "quantum-col"
            
#             # # Highlight best performer
#             # if idx == best_idx:
#             #     cell_class += " best-performer"
            
#             html += f'<td class="{cell_class}">{val}</td>'
        
#         html += "</tr>"
    
#     html += """
#         </tbody>
#     </table>
#     """
    
#     return html
def create_conclusion_metrics_table_html(df_all_metrics,table_type="temperature"):
    """Create HTML table with color-coded columns for classical/quantum and best performers"""
    
    columns = df_all_metrics.columns.tolist()
    
    # Define classical and quantum algorithms
    classical_algos = ["LSTM", "GRU", "ANN", "Dense ANN", "SVM"]
    quantum_algos = ["QLSTM", "QGRU", "QNN-SE", "QNN-Ising", "VQC", "QSVM", "Hybrid QNN"]
    
    html = f"""
    <style>
    
        .conclusion-metrics-table {{
            width: 98%;
            margin: 20px auto;
            border-collapse: collapse;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(30, 64, 175, 0.1);
        }}
        .conclusion-metrics-table thead th {{
            color: white !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            padding: 0.9rem 0.6rem !important;
            text-align: center !important;
            border: none !important;
            border-right: 1px solid rgba(255,255,255,0.2) !important;
        }}
        .conclusion-metrics-table thead th:first-child {{
            background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
            text-align: left !important;
            padding-left: 1rem !important;
        }}
        /* Classical algorithm headers - Blue gradient */
        .classical-header {{
            background: linear-gradient(135deg, #3b82f6, #60a5fa) !important;
        }}
        /* Quantum algorithm headers - Purple gradient */
        .quantum-header {{
            background: linear-gradient(135deg, #8b5cf6, #a78bfa) !important;
        }}
        .conclusion-metrics-table tbody td {{
            color: #000000 !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;
            padding: 0.7rem 0.6rem !important;
            border-bottom: 1px solid #e0f2fe !important;
            text-align: center !important;
        }}
        .conclusion-metrics-table tbody td:first-child {{
            font-weight: 600 !important;
            text-align: left !important;
            background: #f8fafc !important;
            color: #000000 !important;
            padding-left: 1rem !important;
        }}
        /* Classical columns - light blue */
        .classical-col {{
            background: #dbeafe !important;
        }}
        /* Quantum columns - light purple */
        .quantum-col {{
            background: #ede9fe !important;
        }}
        
        .conclusion-metrics-table tbody tr:hover {{
            background: #eff6ff !important;
        }}
        /* Best Classical Models */
        .best-classical-temp {{
            background: linear-gradient(135deg, #bfdbfe, #93c5fd) !important;
            font-weight: 700 !important;
            color: #1e3a8a !important;
            border: 2px solid #2563eb !important;
            border-bottom: 2px solid #2563eb !important; /* ✅ ADD THIS */
        }}
        /* Best Quantum Models */
        .best-quantum-temp {{
            background: linear-gradient(135deg, #e9d5ff, #d8b4fe) !important;
            font-weight: 700 !important;
            color: #6b21a8 !important;
            border: 2px solid #8b5cf6 !important;
            border-bottom: 2px solid #8b5cf6 !important; /* ✅ ADD THIS */
        }}

        /* For Rainfall - Best Classical */
        .best-classical-rain {{
            background: linear-gradient(135deg, #bfdbfe, #93c5fd) !important;
            font-weight: 700 !important;
            color: #1e3a8a !important;
            border: 2px solid #2563eb !important;
            border-bottom: 2px solid #2563eb !important; /* ✅ ADD THIS */
        }}

        /* For Rainfall - Best Quantum */
        .best-quantum-rain {{
            background: linear-gradient(135deg, #e9d5ff, #d8b4fe) !important;
            font-weight: 700 !important;
            color: #6b21a8 !important;
            border: 2px solid #8b5cf6 !important;
            border-bottom: 2px solid #8b5cf6 !important; /* ✅ ADD THIS */
        }}
        
    </style>
    <table class="conclusion-metrics-table">
        <thead>
            <tr>
                <th>📊 Metric</th>
    """
    
    # Add column headers with appropriate classes
    for col in columns[1:]:  # Skip "Metric" column
        if col in classical_algos:
            html += f'<th class="classical-header">{col}</th>'
        elif col in quantum_algos:
            html += f'<th class="quantum-header">{col}</th>'
        else:
            html += f'<th>{col}</th>'
    
    html += """
            </tr>
        </thead>
        <tbody>
    """
    
    # Add data rows with best performer highlighting  done the changes here 
    for _, row in df_all_metrics.iterrows():
        html += "<tr>"
        
        metric_name = row.iloc[0]
        html += f"<td>{metric_name}</td>"
        
        # ✅ STEP 1: Extract numeric values from classical and quantum models
        classical_values = {}
        quantum_values = {}
        
        for idx, (col, val) in enumerate(zip(columns[1:], row.iloc[1:])):
            if val != "N/A" and val != "—":
                # Extract numeric value (remove % if present)
                # clean_val = val.replace( '').strip()

                try:
                    # ✅ Since we removed % from MAPE, just convert directly
                    numeric_val = float(val)
                    if col in classical_algos:
                        classical_values[col] = numeric_val
                    elif col in quantum_algos:
                        quantum_values[col] = numeric_val
                except:
                    pass
        
        # ✅ STEP 2: Find best classical and best quantum
        best_classical_col = None
        best_quantum_col = None
        
        # Determine if lower is better or higher is better
        lower_is_better_metrics = ["MSE", "RMSE", "MAE", "MAPE"]
        
        if metric_name in lower_is_better_metrics:
            # Lower is better
            if classical_values:
                best_classical_col = min(classical_values, key=classical_values.get)
            if quantum_values:
                best_quantum_col = min(quantum_values, key=quantum_values.get)
        else:
            # Higher is better (R², Adjusted R², Accuracy, Precision, Recall, F1)
            if classical_values:
                best_classical_col = max(classical_values, key=classical_values.get)
            if quantum_values:
                best_quantum_col = max(quantum_values, key=quantum_values.get)
        
        # ✅ STEP 3: Add data cells with highlighting
        for idx, (col, val) in enumerate(zip(columns[1:], row.iloc[1:])):
            cell_class = ""
            
            # Determine base column type
            if col in classical_algos:
                cell_class = "classical-col"
            elif col in quantum_algos:
                cell_class = "quantum-col"
            
            # ✅ Add best performer highlighting
            if col == best_classical_col:
                if table_type == "temperature":
                    cell_class += " best-classical-temp"
                else:  # rainfall
                    cell_class += " best-classical-rain"
            elif col == best_quantum_col:
                if table_type == "temperature":
                    cell_class += " best-quantum-temp"
                else:  # rainfall
                    cell_class += " best-quantum-rain"
            
            html += f'<td class="{cell_class}">{val}</td>'
        
        html += "</tr>"
    
    html += """
        </tbody>
    </table>
    """
    
    return html

def create_rainfall_conclusion_metrics_table(classification_metrics):
    """Create comprehensive comparison table for all rainfall classification models"""
    
    # ✅ Display names (what shows in table)
    display_names = [
        "LSTM", "GRU", "ANN", "Dense ANN", "SVM",
        "QLSTM", "QGRU", "QNN-SE", "QNN-Ising", "VQC", "QSVM", "Hybrid QNN"
    ]
    
    # ✅ Data key mapping (what's in CLASSIFICATION_METRICS)
    data_keys = {
        "LSTM": "LSTM",
        "GRU": "GRU",
        "ANN": "ANN",
        "Dense ANN": "Dense ANN",
        "SVM": "SVM",
        "QLSTM": "QLSTM",
        "QGRU": "QGRU",
        "QNN-SE": "QNN_SE",          # ✅ Key mapping
        "QNN-Ising": "QNN_IS",        # ✅ Key mapping
        "VQC": "VQC",
        "QSVM": "QSVM",
        "Hybrid QNN": "Hybrid_QNN"    # ✅ Key mapping
    }
    
    metric_names = [
        "Accuracy",
        "Precision (No Rain)",
        "Recall (No Rain)",
        "F1-Score (No Rain)",
        "Precision (Rain)",
        "Recall (Rain)",
        "F1-Score (Rain)"
    ]
    
    data = []
    for metric_name in metric_names:
        row = {"Metric": metric_name}
        
        # ✅ Loop through display names
        for display_name in display_names:
            # ✅ Get data key for lookup
            data_key = data_keys[display_name]
            
            if data_key in classification_metrics:
                if metric_name in classification_metrics[data_key]:
                    value = classification_metrics[data_key][metric_name]
                    row[display_name] = f"{value:.4f}"
                else:
                    row[display_name] = "N/A"
            else:
                row[display_name] = "N/A"
        
        data.append(row)
    
    df_all_metrics = pd.DataFrame(data)
    return df_all_metrics

def create_noise_metrics_table_with_state():
    """
    Create metrics table for noise comparison using session state
    Returns: DataFrame, left_header, right_header
    """
    from config.constants import IDEAL_VALUES, NOISE_METRICS  # ✅ CORRECT IMPORT
    
    metric_names = [
        "Mean Squared Error (MSE)",
        "Root Mean Squared Error (RMSE)",
        "Mean Absolute Error (MAE)",
        "Mean Absolute Percentage Error (MAPE)",
        "R² Score",
        "Adjusted R²"
    ]
    
    # Check if data exists in session state
    left_generated = st.session_state.get('noise_left_data') is not None
    right_generated = st.session_state.get('noise_right_data') is not None
    
    # Initialize with placeholder values
    left_values = ["—"] * len(metric_names)
    right_values = ["—"] * len(metric_names)
    ideal_values = ["—"] * len(metric_names)
    
    left_header = "Left Algorithm"
    right_header = "Right Algorithm"
    
    # ✅ LOAD LEFT ALGORITHM METRICS
    if left_generated:
        algorithm = st.session_state.noise_left_data['algorithm']
        noise_type = st.session_state.noise_left_data['noise_type']
        left_header = f"{algorithm} ({noise_type})"
        
        # Get metrics from the nested NOISE_METRICS dictionary
        if noise_type in NOISE_METRICS:
            if algorithm in NOISE_METRICS[noise_type]:
                left_metrics = NOISE_METRICS[noise_type][algorithm]
                
                for i, metric in enumerate(metric_names):
                    if metric in left_metrics:
                        value = left_metrics[metric]
                        # if metric == "Mean Absolute Percentage Error (MAPE)":
                        #     left_values[i] = f"{value:.3f} ({value*100:.1f}%)"
                        # else:
                        left_values[i] = f"{value:.3f}"
    
    # ✅ LOAD RIGHT ALGORITHM METRICS
    if right_generated:
        algorithm = st.session_state.noise_right_data['algorithm']
        noise_type = st.session_state.noise_right_data['noise_type']
        right_header = f"{algorithm} ({noise_type})"
        
        # Get metrics from the nested NOISE_METRICS dictionary
        if noise_type in NOISE_METRICS:
            if algorithm in NOISE_METRICS[noise_type]:
                right_metrics = NOISE_METRICS[noise_type][algorithm]
                
                for i, metric in enumerate(metric_names):
                    if metric in right_metrics:
                        value = right_metrics[metric]
                        # if metric == "Mean Absolute Percentage Error (MAPE)":
                        #     right_values[i] = f"{value:.3f} ({value*100:.1f}%)"
                        # else:
                        right_values[i] = f"{value:.3f}"
    
    # ✅ ADD IDEAL VALUES COLUMN
    if left_generated or right_generated:
        ideal_values = [IDEAL_VALUES[metric] for metric in metric_names]
    
    # Create and return the DataFrame
    df = pd.DataFrame({
        'Metric': metric_names,
        left_header: left_values,
        right_header: right_values,
        'Ideal Value': ideal_values
    })
    
    return df, left_header, right_header

# visualization/tables.py (UPDATE THIS SECTION)

def create_metrics_table_html(left_header, right_header, metrics_df):
    """
    ✅ FIXED - Single reusable HTML template
    Works for temperature, rainfall, and noise metrics
    """
    
    # Build table rows dynamically
    rows_html = ""
    for _, row in metrics_df.iterrows():
        rows_html += "<tr>"
        for val in row:
            rows_html += f"<td>{val}</td>"
        rows_html += "</tr>"
    
    # Single HTML template with dynamic content
    html = f"""
    <style>
        .metrics-table {{
            width: 100%;
            margin: 20px auto;
            border-collapse: collapse;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(30, 64, 175, 0.1);
        }}
        .metrics-table thead th {{
            background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            padding: 1rem !important;
            text-align: center !important;
            border: none !important;
        }}
        .metrics-table tbody td {{
            color: #000000 !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
            padding: 0.8rem 1rem !important;
            border-bottom: 1px solid #e0f2fe !important;
            text-align: center !important;
        }}
        .metrics-table tbody td:first-child {{
            font-weight: 600 !important;
            text-align: left !important;
            background: #f8fafc !important;
        }}
        .metrics-table tbody td:nth-child(2) {{
            background: #f0f9ff !important;
        }}
        .metrics-table tbody td:nth-child(3) {{
            background: #f0f9ff !important;
        }}
        .metrics-table tbody td:nth-child(4) {{
            background: #f0fdf4 !important;
        }}
        .metrics-table tbody tr:hover {{
            background: #eff6ff !important;
        }}
    </style>
    <table class="metrics-table">
        <thead>
            <tr>
                <th>Metric</th>
                <th>{left_header}</th>
                <th>{right_header}</th>
                <th>Ideal Value</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """
    
    return html


# ✅ Remove duplicate functions:
# - create_rainfall_metrics_table_html (DELETE)
# - Any other *_metrics_table_html functions (DELETE)
# 
# Keep ONLY create_metrics_table_html() and use it everywhere
def create_rain_noise_metrics_table_with_state():
    """
    Create metrics table for rain noise comparison using session state
    Returns: DataFrame, left_header, right_header
    """
    from config.constants import RAINFALL_IDEAL_VALUES
    import pandas as pd
    
    metric_names = [
        "Accuracy",
        "Precision (No Rain)",
        "Recall (No Rain)",
        "F1-Score (No Rain)",
        "Precision (Rain)",
        "Recall (Rain)",
        "F1-Score (Rain)"
    ]
    
    # Check if data exists
    left_generated = st.session_state.get('rain_noise_left_data') is not None
    right_generated = st.session_state.get('rain_noise_right_data') is not None
    
    left_values = ["—"] * len(metric_names)
    right_values = ["—"] * len(metric_names)
    ideal_values = ["—"] * len(metric_names)
    
    left_header = "Left Algorithm"
    right_header = "Right Algorithm"
    
    # Load left metrics
    if left_generated:
        algorithm = st.session_state.rain_noise_left_data['algorithm']
        noise_type = st.session_state.rain_noise_left_data['noise_type']
        left_header = f"{algorithm} ({noise_type})"
        
        left_metrics = st.session_state.rain_noise_left_data.get('metrics', {})
        
        for i, metric in enumerate(metric_names):
            if metric in left_metrics:
                value = left_metrics[metric]
                left_values[i] = f"{value:.4f}"
    
    # Load right metrics
    if right_generated:
        algorithm = st.session_state.rain_noise_right_data['algorithm']
        noise_type = st.session_state.rain_noise_right_data['noise_type']
        right_header = f"{algorithm} ({noise_type})"
        
        right_metrics = st.session_state.rain_noise_right_data.get('metrics', {})
        
        for i, metric in enumerate(metric_names):
            if metric in right_metrics:
                value = right_metrics[metric]
                right_values[i] = f"{value:.4f}"
    
    # Add ideal values
    if left_generated or right_generated:
        ideal_values = [RAINFALL_IDEAL_VALUES[metric] for metric in metric_names]
    
    df = pd.DataFrame({
        'Metric': metric_names,
        left_header: left_values,
        right_header: right_values,
        'Ideal Value': ideal_values
    })
    
    return df, left_header, right_header

def create_noise_comparison_table_html(df_noise):
    """
    Create HTML table for noise analysis with special highlighting for 'Without Noise' column
    """
    
    # Get column names
    columns = df_noise.columns.tolist()
    
    html = f"""
    <style>
        .noise-comparison-table {{
            width: 100%;
            margin: 20px auto;
            border-collapse: collapse;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(30, 64, 175, 0.1);
        }}
        .noise-comparison-table thead th {{
            background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 0.85rem !important;
            padding: 0.8rem 0.5rem !important;
            text-align: center !important;
            border: none !important;
            border-right: 1px solid rgba(255,255,255,0.2) !important;
        }}
        .noise-comparison-table thead th:first-child {{
            text-align: left !important;
            padding-left: 1rem !important;
        }}
        /* ✅ GREEN COLOR - "Without Noise" HEADER */
        .noise-comparison-table thead th:nth-child(2) {{
            background: linear-gradient(135deg, #10b981, #059669) !important;
        }}
        .noise-comparison-table tbody td {{
            color: #000000 !important;
            font-weight: 500 !important;
            font-size: 0.8rem !important;
            padding: 0.6rem 0.5rem !important;
            border-bottom: 1px solid #e0f2fe !important;
            text-align: center !important;
        }}
        .noise-comparison-table tbody td:first-child {{
            font-weight: 600 !important;
            text-align: left !important;
            background: #f8fafc !important;
            color: #000000 !important;
            padding-left: 1rem !important;
        }}
        /* ✅ GREEN COLOR - "Without Noise" CELLS */
        .noise-comparison-table tbody td:nth-child(2) {{
            background: linear-gradient(135deg, #d1fae5, #a7f3d0) !important;
            font-weight: 600 !important;
            color: #065f46 !important;
        }}
        /* ✅ YELLOW COLOR - All other error columns */
        .noise-comparison-table tbody td:not(:first-child):not(:nth-child(2)) {{
            background: #fef3c7 !important;
        }}
        .noise-comparison-table tbody tr:hover {{
            background: #eff6ff !important;
        }}
        /* ✅ GREEN HOVER EFFECT */
        .noise-comparison-table tbody tr:hover td:nth-child(2) {{
            background: linear-gradient(135deg, #a7f3d0, #6ee7b7) !important;
        }}
        /* ✅ YELLOW HOVER EFFECT */
        .noise-comparison-table tbody tr:hover td:not(:first-child):not(:nth-child(2)) {{
            background: #fde68a !important;
        }}
    </style>
    <table class="noise-comparison-table">
        <thead>
            <tr>
    """
    
    # Add headers
    for col in columns:
        html += f"<th>{col}</th>"
    
    html += """
            </tr>
        </thead>
        <tbody>
    """
    
    # Add data rows
    for _, row in df_noise.iterrows():
        html += "<tr>"
        for val in row:
            html += f"<td>{val}</td>"
        html += "</tr>"
    
    html += """
        </tbody>
    </table>
    """
    
    return html

def create_ncmrwf_metrics_table_html(df_ncmrwf_metrics):
    """Create HTML table specifically for NCMRWF metrics with proper color coding"""
    
    columns = df_ncmrwf_metrics.columns.tolist()
    
    # ✅ NCMRWF specific algorithms
    classical_algos = ["GRU", "LSTM","ANN"]
    quantum_algos = ["QGRU", "QLSTM",'QNN_IS_2.0',"Hybrid QNN_SE","VQC"]
    
    html = f"""
    <style>
        .ncmrwf-metrics-table {{
            width: 98%;
            margin: 20px auto;
            border-collapse: collapse;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(30, 64, 175, 0.1);
        }}
        .ncmrwf-metrics-table thead th {{
            color: white !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            padding: 0.9rem 0.6rem !important;
            text-align: center !important;
            border: none !important;
            border-right: 1px solid rgba(255,255,255,0.2) !important;
        }}
        .ncmrwf-metrics-table thead th:first-child {{
            background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
            text-align: left !important;
            padding-left: 1rem !important;
        }}
        /* Classical algorithm headers - Blue gradient */
        .ncmrwf-classical-header {{
            background: linear-gradient(135deg, #3b82f6, #60a5fa) !important;
        }}
        /* Quantum algorithm headers - Purple gradient */
        .ncmrwf-quantum-header {{
            background: linear-gradient(135deg, #8b5cf6, #a78bfa) !important;
        }}
        .ncmrwf-metrics-table tbody td {{
            color: #000000 !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;
            padding: 0.7rem 0.6rem !important;
            border-bottom: 1px solid #e0f2fe !important;
            text-align: center !important;
        }}
        .ncmrwf-metrics-table tbody td:first-child {{
            font-weight: 600 !important;
            text-align: left !important;
            background: #f8fafc !important;
            color: #000000 !important;
            padding-left: 1rem !important;
        }}
        /* Classical columns - light blue */
        .ncmrwf-classical-col {{
            background: #dbeafe !important;
        }}
        /* Quantum columns - light purple */
        .ncmrwf-quantum-col {{
            background: #ede9fe !important;
        }}
        
        .ncmrwf-metrics-table tbody tr:hover {{
            background: #eff6ff !important;
        }}
    </style>
    <table class="ncmrwf-metrics-table">
        <thead>
            <tr>
                <th>📊 Metric</th>
    """
    
    # Add column headers with appropriate classes
    for col in columns[1:]:  # Skip "Metric" column
        if col in classical_algos:
            html += f'<th class="ncmrwf-classical-header">{col}</th>'
        elif col in quantum_algos:
            html += f'<th class="ncmrwf-quantum-header">{col}</th>'
        else:
            html += f'<th>{col}</th>'
    
    html += """
            </tr>
        </thead>
        <tbody>
    """
    
    # Add data rows
    for _, row in df_ncmrwf_metrics.iterrows():
        html += "<tr>"
        
        metric_name = row.iloc[0]
        html += f"<td>{metric_name}</td>"
        
        # Add data cells
        for idx, (col, val) in enumerate(zip(columns[1:], row.iloc[1:])):
            cell_class = ""
            
            # Determine column type
            if col in classical_algos:
                cell_class = "ncmrwf-classical-col"
            elif col in quantum_algos:
                cell_class = "ncmrwf-quantum-col"
            
            html += f'<td class="{cell_class}">{val}</td>'
        
        html += "</tr>"
    
    html += """
        </tbody>
    </table>
    """
    
    return html