"""
Complete Parameter Comparison Table - Single File Solution
Add this entire file as visualization/parameters_table.py
"""

import pandas as pd
import streamlit as st


def create_parameter_data():
    """
    Create parameter comparison data
    Returns a DataFrame with all parameter comparisons
    """
    parameters_data = {
        "Model Pair": [
            "Gated Recurrent Unit",
            "Long Short-Term Memory",
            "Artificial Neural Network (SE)",
            "Artificial Neural Network (IS)",
            "Dense Artificial Neural Network",
            "Artificial Neural Network (VQC)"
        ],
        "Classical Model": [
            "GRU",
            "LSTM",
            "ANN",
            "ANN",
            "Dense ANN",
            "ANN"
        ],
        "Classical Params": [
            1073,
            460,
            48,
            48,
            17653,
            48
        ],
        "Quantum Model": [
            "QGRU",
            "QLSTM",
            "QNN_SE",
            "QNN_IS",
            "HQNN",
            "VQC"
        ],
        "Quantum Params": [
            164,
            190,
            48,
            21,
            20,
            10
        ]
    }
    
    return pd.DataFrame(parameters_data)


def get_param_color(val):
    """Return color style for parameter value - no color coding"""
    if val == "-" or val == "~17653":
        return "color: #64748b; font-weight: 500;"
    
    try:
        return "color: #1e293b; font-weight: 600;"
    except:
        return ""


def get_status(classical, quantum):
    """Return status badge based on parameter comparison"""
    if classical == "-" or quantum == "-":
        return '<span style="color: #64748b;">—</span>'
    
    try:
        c_val = float(str(classical).replace("~", ""))
        q_val = float(str(quantum).replace("~", ""))
        
        if q_val < c_val * 0.5:
            return '✨ Highly Optimized'
        elif q_val < c_val:
            return '✓ Optimized'
        else:
            return '⚠ Not Optimized'
    except:
        return "—"


def create_parameters_metrics_table_html(df):
    """
    Create an HTML table with the same theme as temperature metrics
    Matches the exact style from the temperature table in your codebase
    """
    
    # Generate rows first
    rows_html = ""
    for idx, row in df.iterrows():
        classical = row['Classical Model']
        classical_params = row['Classical Params']
        quantum = row['Quantum Model']
        quantum_params = row['Quantum Params']
        
        # Calculate reduction percentage
        if classical_params == "-" or quantum_params == "-":
            reduction_html = '<span style="background-color: #e2e8f0; color: #64748b; display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 12px;">Not Applicable</span>'
        else:
            try:
                c_val = float(str(classical_params).replace("~", ""))
                q_val = float(str(quantum_params).replace("~", ""))
                reduction = ((c_val - q_val) / c_val) * 100
                
                if reduction >= 80:
                    badge_style = "background-color: #dcfce7; color: #166534;"
                    reduction_html = f'<span style="{badge_style} display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 12px;">↓ {reduction:.1f}%</span>'
                elif reduction >= 50:
                    badge_style = "background-color: #fef3c7; color: #92400e;"
                    reduction_html = f'<span style="{badge_style} display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 12px;">↓ {reduction:.1f}%</span>'
                elif reduction >= 0:
                    badge_style = "background-color: #fed7aa; color: #7c2d12;"
                    reduction_html = f'<span style="{badge_style} display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 12px;">↓ {reduction:.1f}%</span>'
                else:
                    badge_style = "background-color: #fecaca; color: #7f1d1d;"
                    reduction_html = f'<span style="{badge_style} display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 12px;">↑ {abs(reduction):.1f}%</span>'
            except:
                reduction_html = '<span style="background-color: #e2e8f0; color: #64748b; display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: 600; font-size: 12px;">N/A</span>'
        
        # Get parameter colors
        c_param_color = get_param_color(classical_params)
        q_param_color = get_param_color(quantum_params)
        
        # Get status
        status = get_status(classical_params, quantum_params)
        
        rows_html += f"""<tr>
            <td style="padding: 14px 12px; text-align: center; font-weight: 500; color: #1e293b; font-size: 14px; border: 1px solid #e2e8f0;">{classical}</td>
            <td style="padding: 14px 12px; text-align: center; font-size: 14px; border: 1px solid #e2e8f0; {c_param_color}">{classical_params}</td>
            <td style="padding: 14px 12px; text-align: center; font-weight: 500; color: #1e293b; font-size: 14px; border: 1px solid #e2e8f0; background-color: #f3f0ff;">{quantum}</td>
            <td style="padding: 14px 12px; text-align: center; font-size: 14px; border: 1px solid #e2e8f0; background-color: #f3f0ff; {q_param_color}">{quantum_params}</td>
        </tr>"""
    
    html = f"""
    <table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;">
        <thead>
            <tr style="background-color: #3b82f6; color: white;">
                <th style="padding: 16px 12px; text-align: center; font-weight: 600; font-size: 14px; border: 1px solid #1e40af;">🔷 Classical</th>
                <th style="padding: 16px 12px; text-align: center; font-weight: 600; font-size: 14px; border: 1px solid #1e40af;">Parameters</th>
                <th style="padding: 16px 12px; text-align: center; font-weight: 600; font-size: 14px; border: 1px solid #1e40af;">🔶 Quantum</th>
                <th style="padding: 16px 12px; text-align: center; font-weight: 600; font-size: 14px; border: 1px solid #1e40af;">Parameters</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """
    
    return html


def render_parameters_comparison_section():
    """
    Main function to render parameter comparison section in Streamlit
    Call this function in your conclusion tab
    
    Usage in your conclusion.py:
        from visualization.parameters_table import render_parameters_comparison_section
        render_parameters_comparison_section()
    """
    
    st.markdown("---")
    
    st.markdown("""
    <div style="background: #3b82f6;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 24px;">
        <h3 style="color: white; text-align: center; margin: 0; font-size: 26px; font-weight: 600;">
            ⚙️ Model Parameter Comparison - Classical vs Quantum
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #e0f2fe; 
                padding: 16px; 
                border-radius: 8px; 
                margin-bottom: 20px;">
        <p style="margin: 0; color: #000000; font-weight: 500; text-align: center; font-size: 15px;">
            <strong>
                🔷 Classical Models: Traditional machine learning approaches | 
                🔶 Quantum Models: Quantum-enhanced variants
            </strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create and display the table
    df_params = create_parameter_data()
    table_html = create_parameters_metrics_table_html(df_params)
    
    # Render the table using markdown with unsafe_allow_html
    st.markdown(table_html, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #f8fafc; 
                padding: 18px; 
                border-radius: 8px; 
                margin-top: 20px;
                border-left: 4px solid #3b82f6;">
        <p style="margin: 0; color: #000000; font-size: 15px; line-height: 1.6;">
            <strong>💡 Key Insights – Training Parameter Compression: </strong> 
            A clear advantage observed across the quantum and hybrid models lies in the substantial reduction of trainable parameters when transitioning from classical deep networks to quantum-enhanced architectures. Classical models such as GRU (1073 parameters), LSTM (460 parameters), and especially Dense ANN (17,653 parameters) demonstrate high representational power but incur a significant training cost and increased risk of overfitting. In contrast, quantum models achieve similar functional expressiveness with drastically fewer parameters: QGRU (164 parameters), QLSTM (190 parameters), QNN-SE (48 parameters), QNN-IS (21 parameters), and VQC (10 parameters). This compression—often by an order of magnitude—illustrates the inherent efficiency of variational quantum circuits, where expressive transformations arise from quantum state evolution rather than large weight matrices.
           The Hybrid QNN (HQNN) maintains this benefit by combining a lightweight quantum module with a streamlined classical backbone, achieving competitive performance while dramatically reducing the effective parameter load. Such parameter-efficiency not only accelerates training but also reduces memory footprints, making HQNN particularly well-suited for real-time weather forecasting systems and scalable deployment on resource-constrained NISQ hardware.
        </p>
    </div>
    """, unsafe_allow_html=True)