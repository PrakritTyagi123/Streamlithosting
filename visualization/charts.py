# visualization/charts.py
"""
Chart creation functions using Plotly
"""
import plotly.graph_objects as go
import numpy as np
import streamlit as st
from config.constants import QUANTUM_RESOURCE_DATA, ALGORITHM_PARAMS
import pandas as pd
from plotly.subplots import make_subplots
import colorsys
from datetime import datetime, timedelta

def create_quantum_resource_charts(height=350):
    """Create three quantum resource comparison charts"""
    
    fig_single = go.Figure()
    fig_single.add_trace(go.Bar(
        x=QUANTUM_RESOURCE_DATA["algorithms"],
        y=QUANTUM_RESOURCE_DATA["single_gate_count"],
        marker=dict(
            color=QUANTUM_RESOURCE_DATA["colors"],
            line=dict(color='#2D1B69', width=1)
        ),
        text=QUANTUM_RESOURCE_DATA["single_gate_count"],
        textposition='auto',
        textfont=dict(color='white', size=12, family='Arial Black'),
        hovertemplate='<b>%{x}</b><br>Single Gates: %{y}<br><extra></extra>'
    ))
    
    fig_single.update_layout(
        title=dict(
            text="<b>Single Gate Count Comparison</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='#2c3e50')
        ),
        xaxis_title="Quantum Algorithms",
        yaxis_title="Number of Single Gates",
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=height,
        margin=dict(l=50, r=20, t=50, b=60),
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(color='#000000', size=15),
            title=dict(font=dict(color='#000000', size=18))
        ),
        yaxis=dict(
            tickfont=dict(color='#000000', size=15),
            title=dict(font=dict(color='#000000', size=18))
        ),
        bargap=0.3
    )
    
    fig_multi = go.Figure()
    fig_multi.add_trace(go.Bar(
        x=QUANTUM_RESOURCE_DATA["algorithms"],
        y=QUANTUM_RESOURCE_DATA["multi_gate_count"],
        marker=dict(
            color=QUANTUM_RESOURCE_DATA["colors"],
            line=dict(color='#2D1B69', width=1)
        ),
        text=QUANTUM_RESOURCE_DATA["multi_gate_count"],
        textposition='auto',
        textfont=dict(color='white', size=12, family='Arial Black'),
        hovertemplate='<b>%{x}</b><br>Multi Gates: %{y}<br><extra></extra>'
    ))
    
    fig_multi.update_layout(
        title=dict(
            text="<b>Multi-Gate Count Comparison</b>",
            x=0.5,
            xanchor='center', 
            font=dict(size=20, color='#2c3e50')
        ),
        xaxis_title="Quantum Algorithms",
        yaxis_title="Number of Multi Gates",
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=height,
        margin=dict(l=50, r=20, t=50, b=60),
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(color='#000000', size=15),
            title=dict(font=dict(color='#000000', size=18))
        ),
        yaxis=dict(
            tickfont=dict(color='#000000', size=15),
            title=dict(font=dict(color='#000000', size=18))
        ),
        bargap=0.3
    )
    
    fig_depth = go.Figure()
    fig_depth.add_trace(go.Bar(
        x=QUANTUM_RESOURCE_DATA["algorithms"],
        y=QUANTUM_RESOURCE_DATA["depth"],
        marker=dict(
            color=QUANTUM_RESOURCE_DATA["colors"],
            line=dict(color='#2D1B69', width=1)
        ),
        text=QUANTUM_RESOURCE_DATA["depth"],
        textposition='auto',
        textfont=dict(color='white', size=12, family='Arial Black'),
        hovertemplate='<b>%{x}</b><br>Circuit Depth: %{y}<br><extra></extra>'
    ))
    
    fig_depth.update_layout(
        title=dict(
            text="<b>Circuit Depth Comparison</b>",
            x=0.5,
            xanchor='center', 
            font=dict(size=20, color='#2c3e50')
        ),
        xaxis_title="Quantum Algorithms",
        yaxis_title="Circuit Depth",
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=height,
        margin=dict(l=50, r=20, t=50, b=60),
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(color='#000000', size=15),
            title=dict(font=dict(color='#000000', size=18))
        ),
        yaxis=dict(
            tickfont=dict(color='#000000', size=15),
            title=dict(font=dict(color='#000000', size=18))
        ),
        bargap=0.3
    )
    
    return fig_single, fig_multi, fig_depth

def create_combined_resource_chart_for_algorithm(algorithm_name):
    """
    Create a combined bar chart showing Single-Qubit, Multi-Qubit, and Circuit Depth
    for a specific quantum algorithm
    """
    # Map algorithm names to indices
    algo_map = {
        'QGRU': 0,
        'QLSTM': 1,
        'QNN_IS': 2,
        'QNN_SE': 3,
        'VQC': 4,
        'QSVM': 5,
        'Hybrid QNN': 6
    }
    
    # Get short name from full name
    short_name = algorithm_name
    for key in algo_map.keys():
        if key in algorithm_name:
            short_name = key
            break
    
    if short_name not in algo_map:
        fig = go.Figure()
        fig.add_annotation(
            text="No quantum resource data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="gray")
        )
        fig.update_layout(height=400, title="Quantum Resource Estimates", showlegend=False)
        return fig
    
    idx = algo_map[short_name]
    
    # Get data
    single_gate = QUANTUM_RESOURCE_DATA['single_gate_count'][idx]
    multi_gate = QUANTUM_RESOURCE_DATA['multi_gate_count'][idx]
    depth = QUANTUM_RESOURCE_DATA['depth'][idx]
    
    # Create chart
    fig = go.Figure()
    
    categories = ['Single-Qubit Gates', 'Multi-Qubit Gates', 'Circuit Depth']
    values = [single_gate, multi_gate, depth]
    colors_list = ['#3B82F6', '#10B981', '#F59E0B']
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        text=values,
        textposition='outside',
        textfont=dict(color='#000000', size=12),  # ← Add this line
        marker=dict(color=colors_list, line=dict(color='rgba(0,0,0,0.3)', width=1)),
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=f'Quantum Resource Estimates - {short_name}', font=dict(size=16, color='#1f2937'), x=0.5, xanchor="center"),
        xaxis=dict(
            title='Resource Type',
            title_font=dict(size=18, color='#000000'),  # Changed from titlefont
            tickfont=dict(size=15, color='#000000')
        ),
        yaxis=dict(
            title='Count',
            title_font=dict(size=18, color='#000000'),  # Changed from titlefont
            tickfont=dict(size=15, color='#000000'),
            gridcolor='rgba(0,0,0,0.1)'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        height=500,
        margin=dict(l=50, r=30, t=60, b=50)
    )
    
    return fig

def create_temperature_prediction_chart(data, algorithm_name, pred_col, color='#1d4ed8', chart_type='classical'):
    """Create temperature prediction chart for a single algorithm"""
    fig = go.Figure()
    
    # Actual temperature line - BLACK (matching combined chart)
    fig.add_trace(go.Scatter(
        x=data['Datetime'],
        y=data['T2M'],
        mode='lines+markers',
        line=dict(color='#0000FF', width=2),  # ← Changed to black
        marker=dict(size=3),
        name='Actual',
        hovertemplate='<b>%{x}</b><br>%{y:.1f}°C<extra></extra>'
    ))
    
    # Predicted temperature line
    # Set colors based on chart type to match combined chart Turquoise color with else red for classical
    if chart_type == 'quantum':
        # Yellow for quantum, dotted line
        line_style = dict(color='#30D5C8', width=2, dash='dot')
    else:
        # Blue for classical, solid line
        line_style = dict(color='#FF0000', width=2)
    
    fig.add_trace(go.Scatter(
        x=data['Datetime'],
        y=data[pred_col],
        mode='lines+markers',
        line=line_style,
        marker=dict(size=4),
        name='Predicted',
        hovertemplate='<b>%{x}</b><br>%{y:.1f}°C<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"{algorithm_name}",
        height=400,
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Datetime",
        yaxis_title="Temperature (°C)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        font=dict(size=10,color='#000000'),
        xaxis=dict(tickfont=dict(size=12,color='#000000'),title=dict(font=dict(color='#000000', size=16))),
        yaxis=dict(tickfont=dict(size=12,color='#000000'),title=dict(font=dict(color='#000000', size=16)))
    )
    
    return fig


def create_combined_prediction_chart(classical_data, quantum_data, classical_name, quantum_name, 
                                     classical_pred_col, quantum_pred_col, chart_title):
    """
    Create combined classical vs quantum comparison chart
    OPTIMIZED for real-time updates with memoization
    """
    # Ensure datetime columns are properly formatted
    classical_data = classical_data.copy()
    quantum_data = quantum_data.copy()
    
    classical_data['Datetime'] = pd.to_datetime(classical_data['Datetime'], errors='coerce')
    quantum_data['Datetime'] = pd.to_datetime(quantum_data['Datetime'], errors='coerce')
    
    fig = go.Figure()
    
    # Actual temperature - Blue
    fig.add_trace(go.Scatter(
        x=classical_data['Datetime'],
        y=classical_data['T2M'],
        mode='lines+markers',
        name='Actual Temperature',
        line=dict(color='#0000FF', width=3),
        marker=dict(size=5, color='#0000FF'),
        hovertemplate='<b>%{x|%Y-%m-%d %H:%M}</b><br>Actual: %{y:.2f}°C<extra></extra>'
    ))
    
    # Classical prediction - RED
    fig.add_trace(go.Scatter(
        x=classical_data['Datetime'],
        y=classical_data[classical_pred_col],
        mode='lines+markers',
        name=f'Classical ({classical_name})',
        line=dict(color='#FF0000', width=3),
        marker=dict(size=5, color='#FF0000'),
        hovertemplate='<b>%{x|%Y-%m-%d %H:%M}</b><br>Classical: %{y:.2f}°C<extra></extra>'
    ))
    
    # Quantum prediction - turquoise, dotted
    fig.add_trace(go.Scatter(
        x=quantum_data['Datetime'],
        y=quantum_data[quantum_pred_col],
        mode='lines+markers',
        name=f'Quantum ({quantum_name})',
        line=dict(color='#30D5C8', width=3, dash='dot'),
        marker=dict(size=5, color='#30D5C8'),
        hovertemplate='<b>%{x|%Y-%m-%d %H:%M}</b><br>Quantum: %{y:.2f}°C<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=f"<b>{chart_title}</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=18, color='#2c3e50')
        ),
        xaxis_title="Datetime",
        yaxis_title="Temperature (°C)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=450,
        margin=dict(l=60, r=40, t=80, b=60),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1
        ),
        yaxis=dict(
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
        hovermode='x unified'  # âœ… Better hover experience
    )
    
    return fig


# Add this helper function for better performance
def render_temperature_metrics_cards(classical_data, quantum_data, classical_pred_col, quantum_pred_col):
    """
    Render metric cards showing latest predictions
    Optimized for real-time updates
    """
    import streamlit as st
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        actual = classical_data['T2M'].iloc[-1]
        st.metric("Current Actual Temperature", f"{actual:.1f}°C", delta=None)
    
    with col2:
        classical_pred = classical_data[classical_pred_col].iloc[-1]
        classical_error = classical_pred - actual
        st.metric("Classical Prediction", f"{classical_pred:.1f}°C", delta=f"{classical_error:+.1f}Â°C")
    
    with col3:
        quantum_pred = quantum_data[quantum_pred_col].iloc[-1]
        quantum_error = quantum_pred - actual
        st.metric("Quantum Prediction", f"{quantum_pred:.1f}°C", delta=f"{quantum_error:+.1f}Â°C")


def get_training_params_data():
    """Get training parameters data for selected algorithms - reads from session state data"""
    algorithms_to_show = []
    classical_params = []
    quantum_params = []
    colors = []
    notes = []
    
    # Check classical data - read algorithm name directly from the data
    if (st.session_state.classical_data and 
        isinstance(st.session_state.classical_data, dict) and
        st.session_state.classical_data.get('algorithm') and
        st.session_state.classical_data['algorithm'] != "Select Classical Algorithm"):
        
        classical_algo = st.session_state.classical_data['algorithm']
        algo_data = ALGORITHM_PARAMS.get(classical_algo, {})
        
        algorithms_to_show.append(f"Classical\n({classical_algo})")
        classical_params.append(algo_data.get('classical', 0))
        quantum_params.append(algo_data.get('quantum', 0))
        colors.append('#1d4ed8')  # Blue for classical
        notes.append(algo_data.get('note', ''))
    
    # Check quantum data - read algorithm name directly from the data
    if (st.session_state.quantum_data and 
        isinstance(st.session_state.quantum_data, dict) and
        st.session_state.quantum_data.get('algorithm') and
        st.session_state.quantum_data['algorithm'] != "Select Quantum Algorithm"):
        
        quantum_algo = st.session_state.quantum_data['algorithm']
        algo_data = ALGORITHM_PARAMS.get(quantum_algo, {})
        
        algorithms_to_show.append(f"Quantum\n({quantum_algo})")
        classical_params.append(algo_data.get('classical', 0))
        quantum_params.append(algo_data.get('quantum', 0))
        colors.append('#fde047')  # Yellow for quantum
        notes.append(algo_data.get('note', ''))
    
    return algorithms_to_show, classical_params, quantum_params, colors, notes

def create_training_params_chart(algorithms, classical_params, quantum_params, colors, notes):
    """Create training parameters comparison chart"""
    if not algorithms:
        return None
    
    has_hybrid = any('Hybrid QNN' in algo for algo in algorithms)
    use_log_scale = has_hybrid and any(param > 1000 for param in classical_params + quantum_params)
    
    # ✅ ADD THIS CHECK
    has_kernel_methods = any(note and 'Kernel-based' in note for note in notes)
    fig = go.Figure()
    
    x_labels = []
    x_positions_classical = []
    x_positions_quantum = []
    
    for i, algo in enumerate(algorithms):
        # if 'Hybrid QNN' in algo:
        #     x_labels.extend([f"{algo}<br>(Classical)", f"{algo}<br>(Quantum)"])
        #     x_positions_classical.append(len(x_labels) - 2)
        #     x_positions_quantum.append(len(x_labels) - 1)
        # else:
        x_labels.append(algo.replace('\n', '<br>'))
        x_positions_classical.append(len(x_labels) - 1)
        x_positions_quantum.append(len(x_labels) - 1)
    
    display_classical = []
    display_quantum = []
    text_classical = []
    text_quantum = []
    
    for classical, quantum in zip(classical_params, quantum_params):
        if use_log_scale:
            if classical > 0:
                display_classical.append(np.log10(classical))
                text_classical.append(f'{classical:,}<br>(log: {np.log10(classical):.1f})')
            else:
                display_classical.append(0)
                text_classical.append('0')
                
            if quantum > 0:
                display_quantum.append(np.log10(quantum))
                text_quantum.append(f'{quantum:,}<br>(log: {np.log10(quantum):.1f})')
            else:
                display_quantum.append(0)
                text_quantum.append('0')
        else:
            display_classical.append(classical)
            display_quantum.append(quantum)
            text_classical.append(f'{classical:,}' if classical > 0 else '0')
            text_quantum.append(f'{quantum:,}' if quantum > 0 else '0')
    
    x_vals_classical = []
    x_vals_quantum = []
    y_vals_classical = []
    y_vals_quantum = []
    base_vals_quantum = [] 
    colors_classical = []
    colors_quantum = []
    text_vals_classical = []
    text_vals_quantum = []
    
    for i, (algo, classical_val, quantum_val, classical_txt, quantum_txt) in enumerate(
    zip(algorithms, display_classical, display_quantum, text_classical, text_quantum)):
    
    # No need to check for kernel methods - they're already filtered out
    
        if 'Hybrid QNN' in algo:
            x_vals_classical.append(x_positions_classical[i])
            y_vals_classical.append(classical_val)
            colors_classical.append('#007bff')
            text_vals_classical.append(classical_txt)
            
            x_vals_quantum.append(x_positions_quantum[i])
            y_vals_quantum.append(quantum_val)
            base_vals_quantum.append(classical_val)
            colors_quantum.append('#9d4edd')
            text_vals_quantum.append(quantum_txt)
        else:
            x_vals_classical.append(x_positions_classical[i])
            y_vals_classical.append(classical_val)
            colors_classical.append('#007bff')
            text_vals_classical.append(classical_txt)
            
            x_vals_quantum.append(x_positions_quantum[i])
            y_vals_quantum.append(quantum_val)
            base_vals_quantum.append(0)
            colors_quantum.append('#6f42c1')
            text_vals_quantum.append(quantum_txt)
    
    if x_vals_classical:
        fig.add_trace(go.Bar(
            name='Classical',
            x=x_vals_classical,
            y=y_vals_classical,
            marker=dict(color=colors_classical, opacity=0.8),
            text=text_vals_classical,
            textposition='inside',
            textfont=dict(color='white', size=10, family='Arial Black'),
            width=0.6
        ))
    
    if x_vals_quantum:
        fig.add_trace(go.Bar(
            name='Quantum',
            x=x_vals_quantum,
            y=y_vals_quantum,
            marker=dict(color=colors_quantum, opacity=0.8),
            text=text_vals_quantum,
            textposition='inside',
            textfont=dict(color='white', size=10, family='Arial Black'),
            width=0.6,
            # base=0
            base=base_vals_quantum
        ))
    
    y_title = "Log₁₀(Parameters)" if use_log_scale else "Number of Parameters"
    title_suffix = " (Log Scale)" if use_log_scale else ""
    
    fig.update_layout(
        title=dict(
            text=f"<b>Training Parameters Overview{title_suffix}</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='#000000')
        ),
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(x_labels))),
            ticktext=x_labels,
            tickangle=0,
            tickfont=dict(size=15, color='#000000'),
            title=dict(font=dict(color='#000000', size=14)),
            side='bottom',  # ← Add this
            anchor='free',  # ← Add this
            position=0 ,
            dtick=1,  # ← Add this
            type='category'  # ← Add this
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(color='#000000', size=15)),
            tickfont=dict(size=18, color='#000000'),
            gridcolor='rgba(0,0,0,0.1)'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500, # ← Change Height
        margin=dict(l=60, r=60, t=80, b=100),# ← Increased bottom margin
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        # barmode='stack',
        barmode='overlay',  # ← Add this line - makes bars side-by-side
        bargap=0.2,  # ← Add this for better spacing
        bargroupgap=0.1,
        xaxis_fixedrange=False 
    )
    return fig



#rain
def show_rain_forecast_with_tabs(classical_data, quantum_data,
                                  classical_pred_col, quantum_pred_col,
                                  classical_algo, quantum_algo):
    """
    FIXED VERSION - No more flicker in Single Day View
    
    KEY FIX: Move date/time pickers INSIDE the fragment to prevent double reruns
    """
    
    # Prepare data for date ranges (lightweight operation, runs once)
    dfc = classical_data.copy()
    # Makes a copy of the classical dataset
    # This avoids modifying the original data accidentally
    # print(dfc)
    dfc['Datetime'] = pd.to_datetime(dfc['Datetime'], errors='coerce')
    # print(dfc['Datetime'])
    dfc['Date'] = dfc['Datetime'].dt.date
    # Now we have a date
    # print(dfc['Date'])
    
    min_date = dfc['Date'].min()
    # print(min_date)
    max_date = dfc['Date'].max()
    # print(max_date)
    
    # Create tabs
    tab1, tab2 = st.tabs(["📅 Single Day View", "🗓️ Weekly View"])
    
    with tab1:
        st.markdown("### 🎯 Single Day Controls")
        
        # Show static legend ONCE (outside fragment)
        show_legend()
        
        # st.markdown("---")
        
        # ✅ FIX: Pass data ranges to fragment, let fragment handle widgets
        render_single_day_forecast_fragment(
            classical_data, quantum_data,
            classical_pred_col, quantum_pred_col,
            classical_algo, quantum_algo,
            min_date, max_date
        )
    
    with tab2:
        st.markdown("### 🎯 Weekly View Controls")
        
        show_weekly_rain_forecast_heatmap(
            classical_data, quantum_data,
            classical_pred_col, quantum_pred_col,
            classical_algo, quantum_algo,
            selected_date=max_date
        )

def show_legend():
    """
    Static legend component - rendered once, outside fragment
    """
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
        <div style='background: linear-gradient(135deg, #3b82f6 0%, #10b981 50%, #8b5cf6 100%); 
                    padding: 8px; border-radius: 8px; text-align: center;height: 90px; 
                    display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 22px;'>🌧️</div>
            <div style='color: white; font-weight: 600; margin-top: 2px; font-size: 15px;'>Raining</div>
            <div style='color: white; font-size: 11px; margin-top: 3px;'>Blue=Classical, Green=Actual, Purple=Quantum</div>
        </div>
        """, unsafe_allow_html=True)
    
    with legend_cols[3]:
        st.markdown("""
        <div style='background: #f0f2f5; 
                    padding: 8px; border-radius: 8px; text-align: center; border: 2px solid #e5e7eb;
                    height: 90px; display: flex; flex-direction: column; justify-content: center;'>
            <div style='color: #374151; font-weight: 700; font-size: 15px;'>
                <strong>C</strong>=Classical 
            </div>
            <div style='color: #374151; font-weight: 700; font-size: 15px; margin-top: 4px;'> 
                <strong>A</strong> = Actual
            </div>
            <div style='color: #374151; font-weight: 700; font-size: 15px; margin-top: 4px;'> 
                <strong>Q</strong> = Quantum
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
@st.fragment
def render_single_day_forecast_fragment(classical_data, quantum_data,
                                         classical_pred_col, quantum_pred_col,
                                         classical_algo, quantum_algo,
                                         min_date, max_date):
    """
    ✅ FIXED Fragment - Handles widgets internally to prevent parent reruns
    """
    
    # Initialize defaults ONCE
    if 'tab1_single_day_date_input' not in st.session_state:
        st.session_state.tab1_single_day_date_input = min_date
    if 'tab1_time_interval_input' not in st.session_state:
        st.session_state.tab1_time_interval_input = "1 Hour"
    
    # ✅ Widgets are NOW inside the fragment
    col1, col2 = st.columns(2)
    
    with col1:
        single_day_date = st.date_input(
            "**Select Date**",
            min_value=min_date,
            max_value=max_date,
            key="tab1_single_day_date_input",
            help="Choose a specific day to view hourly forecast"
        )
        
    with col2:
        time_interval = st.selectbox(
            "**Time Interval**",
            options=["1 Hour", "3 Hours", "6 Hours", "12 Hours", "24 Hours"],
            key="tab1_time_interval_input",
            help="Select time interval for hourly display"
        )
    
    # st.markdown("---")
    
    # Render the actual forecast
    show_single_day_rain_forecast_core(
        classical_data, quantum_data,
        classical_pred_col, quantum_pred_col,
        classical_algo, quantum_algo,
        selected_date=single_day_date,
        time_interval=time_interval
    )

  
def show_single_day_rain_forecast_core(classical_data, quantum_data, 
                                        classical_pred_col, quantum_pred_col,
                                        classical_algo, quantum_algo,
                                        selected_date, time_interval):
    """
    Core function to render single day rain forecast (dynamic content only)
    Added debug output to track rendering
    """
    
    # DEBUG: Show what's being rendered
    # st.caption(f"🔄 Rendering data for: **{selected_date}** at **{time_interval}** interval")
    
    # Prepare data efficiently
    dfc = classical_data.copy()
    dfq = quantum_data.copy()
    
    dfc['Datetime'] = pd.to_datetime(dfc['Datetime'], errors='coerce')
    dfq['Datetime'] = pd.to_datetime(dfq['Datetime'], errors='coerce')
    
    dfc['Date'] = dfc['Datetime'].dt.date
    dfq['Date'] = dfq['Datetime'].dt.date
    dfc['Hour'] = dfc['Datetime'].dt.hour
    dfq['Hour'] = dfq['Datetime'].dt.hour
    
    # Convert selected_date to date object if needed
    if isinstance(selected_date, str):
        selected_date = pd.to_datetime(selected_date).date()
    elif hasattr(selected_date, 'date'):
        selected_date = selected_date.date()
    
    # Filter data for selected date
    day_data_c = dfc[dfc['Date'] == selected_date].sort_values('Hour')
    day_data_q = dfq[dfq['Date'] == selected_date].sort_values('Hour')
    
    # Apply time interval filter
    interval_hours = {
        "1 Hour": list(range(24)),
        "3 Hours": [0, 3, 6, 9, 12, 15, 18, 21],
        "6 Hours": [0, 6, 12, 18],
        "12 Hours": [0, 12],
        "24 Hours": [12]
    }
    
    hours_to_show = interval_hours.get(time_interval, list(range(24)))
    day_data_c = day_data_c[day_data_c['Hour'].isin(hours_to_show)].reset_index(drop=True)
    day_data_q = day_data_q[day_data_q['Hour'].isin(hours_to_show)].reset_index(drop=True)
    
    # DEBUG: Show filtered data info
    # st.caption(f"📊 Data points: Classical={len(day_data_c)}, Quantum={len(day_data_q)} | Hours shown: {len(hours_to_show)}")
    
    if len(day_data_c) == 0:
        st.warning("No data available for the selected date and interval.")
        return
    
    # Build all content in a single container to minimize repaints
    day_name = pd.to_datetime(selected_date).strftime('%A')
    date_str = pd.to_datetime(selected_date).strftime('%B %d, %Y')
    
    # Use a single container with all content rendered at once
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px; 
                border-radius: 10px; 
                margin-bottom: 15px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
        <h2 style='color: white; margin: 0; text-align: center; font-size: 20px;'>
            {day_name}, {date_str}
        </h2>
        <p style='color: white; margin: 5px 0 0 0; text-align: center; font-size: 15px;'>
            Interval: {time_interval} | Total Hours: {len(hours_to_show)}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🕐 24-Hour Timeline")
    
    # Model configurations
    models = [
        {
            'label': 'C', 
            'name': 'Classical', 
            'algo': classical_algo,
            'data': day_data_c,
            'pred_col': classical_pred_col,
            'color_rain': '#3b82f6'
        },
        {
            'label': 'A', 
            'name': 'Actual', 
            'algo': None,
            'data': day_data_c,
            'pred_col': 'Actual',
            'color_rain': '#10b981'
        },
        {
            'label': 'Q', 
            'name': 'Quantum', 
            'algo': quantum_algo,
            'data': day_data_q,
            'pred_col': quantum_pred_col,
            'color_rain': '#8b5cf6'
        }
    ]
    
    # Build all timelines in one go for smoother rendering
    all_timelines_html = ""
    
    for model in models:
        data = model['data']
        pred_col = model['pred_col']
        
        if len(data) == 0:
            all_timelines_html += f"<p style='color: #f59e0b;'>⚠️ No data available for {model['name']}</p>"
            continue
        
        # Build header with algorithm name if applicable
        if model['algo']:
            header_text = f"<h4 style='margin-top: 20px; color: #1f2937;'>{model['label']} - {model['name']} ({model['algo']})</h4>"
        else:
            header_text = f"<h4 style='margin-top: 20px; color: #1f2937;'>{model['label']} - {model['name']}</h4>"
        
        all_timelines_html += header_text
        all_timelines_html += build_timeline_html(data, pred_col, model, hours_to_show)
        all_timelines_html += "<br>"
    
    # Render all timelines at once in a single markdown call
    st.markdown(all_timelines_html, unsafe_allow_html=True)
def build_timeline_html(data, pred_col, model, hours_to_show):
    """
    Builds the timeline HTML for a single model
    Optimized for performance with minimal DOM operations
    """
    html_content = f"""
    <style>
        .timeline-table {{
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
            margin-bottom: 15px;
            animation: fadeIn 0.3s ease-in;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        .timeline-table th {{
            background-color: #f9fafb;
            font-weight: bold;
            font-size: 13px;
            text-align: center;
            padding: 8px;
            border: 1px solid #e5e7eb;
        }}
        .timeline-table th.model-header {{
            width: 120px;
            text-align: left;
            font-size: 14px;
        }}
        .timeline-table td {{
            text-align: center;
            font-size: 22px;
            padding: 12px;
            border: 1px solid #e5e7eb;
        }}
        .timeline-table td.model-name {{
            background-color: #f9fafb;
            font-weight: 600;
            font-size: 14px;
            text-align: left;
        }}
    </style>
    <table class="timeline-table">
        <thead>
            <tr>
                <th class="model-header">Model</th>
    """
    
    # Add hour headers
    for hour in hours_to_show:
        html_content += f'<th>{hour:02d}:00</th>'
    
    html_content += """
            </tr>
        </thead>
        <tbody>
            <tr>
    """
    
    # Add model name cell
    html_content += f'<td class="model-name">{model["label"]} - {model["name"]}</td>'
    
    # Add hour data cells
    for hour in hours_to_show:
        hour_data = data[data['Hour'] == hour]
        
        if len(hour_data) > 0:
            prediction = int(hour_data.iloc[0][pred_col])
            is_night = (hour >= 19 or hour < 6)
            
            # Determine icon and background
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
@st.fragment
def show_weekly_rain_forecast_heatmap(classical_data, quantum_data,
                                       classical_pred_col, quantum_pred_col,
                                       classical_algo, quantum_algo,
                                       selected_date):
    """
    Show weekly rain forecast as a HEATMAP with start and end date pickers
    Shows all 3 models (Classical, Actual, Quantum) together
    """
    # Prepare data
    dfc = classical_data.copy()
    dfq = quantum_data.copy()
    
    dfc['Datetime'] = pd.to_datetime(dfc['Datetime'], errors='coerce')
    dfq['Datetime'] = pd.to_datetime(dfq['Datetime'], errors='coerce')
    
    dfc['Date'] = dfc['Datetime'].dt.date
    dfq['Date'] = dfq['Datetime'].dt.date
    dfc['Hour'] = dfc['Datetime'].dt.hour
    dfq['Hour'] = dfq['Datetime'].dt.hour
    
    # Get available date range
    min_date = dfc['Date'].min()
    max_date = dfc['Date'].max()
    
    if 'weekly_default_initialized' not in st.session_state:
        st.session_state.weekly_default_initialized = True
        st.session_state.weekly_default_end = max_date
        st.session_state.weekly_default_start = max_date - timedelta(days=6)
    
    # Date range picker for weekly view
    st.markdown("### 📅 Select Week")
    col_date1, col_date2 = st.columns(2)

    default_start = st.session_state.weekly_default_start
    default_end = st.session_state.weekly_default_end
    
    with col_date1:
        # Start date picker
        week_start_date = st.date_input(
            "**Start Date**",
            value=default_start,
            min_value=min_date,
            max_value=max_date,
            key="weekly_heatmap_start_date",
            help="Select the start date (maximum 14 days range)"
        )
    
    with col_date2:
        # End date picker with dynamic max constraint
        # Limit end date to 13 days after start date (14 days total including start)
        constrained_max_date = min(max_date, week_start_date + timedelta(days=13))
        week_end_date = st.date_input(
            "**End Date**",
            value=min(default_end, constrained_max_date),
            min_value=week_start_date,
            max_value=constrained_max_date,
            key="weekly_heatmap_end_date",
            help="Select the end date (maximum 14 days from start date)"
        )
    
    
    
    # Calculate number of days
    num_days = (week_end_date - week_start_date).days + 1
    
    # Header with week info
    start_str = week_start_date.strftime('%b %d')
    end_str = week_end_date.strftime('%b %d, %Y')
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px; 
                border-radius: 10px; 
                margin: 15px 0;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
        <h2 style='color: white; margin: 0; text-align: center; font-size: 20px;'>
            📆 {start_str} - {end_str} ({num_days} days)
        </h2>
        <p style='color: white; margin: 5px 0 0 0; text-align: center; font-size: 15px;'>
            Showing: Classical, Actual & Quantum Models | All 24 Hours
        </p>
    </div>
    """, unsafe_allow_html=True)
    # Legend
    st.markdown("---")
    st.markdown("### 📖 Heatmap Legend")
    legend_cols = st.columns(3)
    
    with legend_cols[0]:
        st.markdown("""
        <div style='background:#60a5fa ; 
                    padding: 12px; 
                    border-radius: 8px; 
                    text-align: center;
                    height: 120px; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <div style='font-size: 32px;'>☀️</div>
            <div style='color: white; font-weight: 600; margin-top: 5px; font-size: 13px;'>Clear Day</div>
        </div>
        """, unsafe_allow_html=True)
    
    with legend_cols[1]:
        st.markdown("""
        <div style='background: #1e3a8a; 
                    padding: 12px; 
                    border-radius: 8px; 
                    text-align: center;
                    height: 120px; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <div style='font-size: 32px;'>🌙</div>
            <div style='color: white; font-weight: 600; margin-top: 5px; font-size: 13px;'>Clear Night</div>
        </div>
        """, unsafe_allow_html=True)
    
    with legend_cols[2]:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #3b82f6 0%, #10b981 50%, #8b5cf6 100%); 
                    padding: 12px; 
                    border-radius: 8px; 
                    text-align: center;
                    height: 120px; 
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <div style='font-size: 32px;'>🌧️</div>
            <div style='color: white; font-weight: 600; margin-top: 5px; font-size: 13px;'>Raining</div>
            <div style='color: white; font-size: 13px; margin-top: 3px;'>Blue=Classical, Green=Actual, Purple=Quantum</div>
        </div>
        """, unsafe_allow_html=True)


    
    # Generate date range
    dates = [week_start_date + timedelta(days=i) for i in range(num_days)]
    
    # All hours (no interval selection in this tab)
    hours_to_show = list(range(0, 24))
    
    models = [
        {'name': 'Classical', 'label': 'C', 'algo': classical_algo, 'data': dfc, 'pred_col': classical_pred_col, 'color_rain': '#3b82f6'},
        {'name': 'Actual', 'label': 'A', 'algo': None, 'data': dfc, 'pred_col': 'Actual', 'color_rain': '#10b981'},
        {'name': 'Quantum', 'label': 'Q', 'algo': quantum_algo, 'data': dfq, 'pred_col': quantum_pred_col, 'color_rain': '#8b5cf6'}
    ]
    
    # Display heatmap for each model
    for model in models:
        # Build header with algorithm name if applicable
        if model['algo']:
            header_text = f"### {model['label']} - {model['name']} Model ({model['algo']})"
        else:
            header_text = f"### {model['label']} - {model['name']} Model"
        
        st.markdown(header_text)

        model_data = model['data']
        pred_col = model['pred_col']
        
        # Create heatmap table using Streamlit's native rendering
        # Build data for display
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
                    
                    # Determine icon
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
        
        # Display as styled dataframe
        styled_df = heatmap_df.style.map(style_cell, subset=heatmap_df.columns[1:])
        styled_df = styled_df.set_table_styles([
            # {'selector': 'th', 'props': [('font-weight', 'bold'), ('font-size', '16px')]}
            {'selector': 'thead th', 'props': [('font-weight', 'bold'), ('font-size', '15px'), ('text-align', 'center')]},
            {'selector': 'tbody th', 'props': [('font-weight', 'bold'), ('font-size', '15px')]}

        ])
        styled_df = styled_df.set_properties(**{'text-align': 'left','font-weight': 'bold', 'font-size': '16px'}, subset=['Day'])
        st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)
        # st.dataframe(styled_df, width='stretch', hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

def create_confusion_matrix_chart(metrics, algorithm_name):
    """
    Create a confusion matrix visualization
    
    Args:
        metrics: Dictionary with classification metrics
        algorithm_name: Name of the algorithm
        
    Returns:
        Plotly figure
    """
    # Extract confusion matrix values
    tn = metrics.get("True Negatives (TN)", 0)
    fp = metrics.get("False Positives (FP)", 0)
    fn = metrics.get("False Negatives (FN)", 0)
    tp = metrics.get("True Positives (TP)", 0)
    
    # Create confusion matrix
    confusion_matrix = [[fn, tp], [tn, fp]]
    
    fig = go.Figure(data=go.Heatmap(
        z=confusion_matrix,
        x=['Predicted No Rain', 'Predicted Rain'],
        y=['Actual Rain', 'Actual No Rain'],
        text=confusion_matrix,
        texttemplate='%{text}',
        textfont={"size": 22, "color": "white"},
        # showscale=True,
        colorscale=[
            [0, '#60a5fa'],      # Medium-light blue (darker than before)
            [0.4, '#3b82f6'],    # Medium blue
            [0.7, '#2563eb'],    # Darker blue
            [1, '#1e40af'] 
        ],
        showscale=False,  # Hide color scale bar
        hovertemplate='%{y}<br>%{x}<br>Count: %{z}<extra></extra>',
        # colorscale='Blues',
    ))
    
    fig.update_layout(
        title={
            'text': f'Confusion Matrix - {algorithm_name}',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#1e40af', 'family': 'Arial, sans-serif'}
        },
        height=300,  # Smaller height
        width=400,   # Smaller width
        xaxis={'side': 'bottom', 
               'tickfont': {'size': 15,'color': '#000000','family': 'Arial', 'weight': 'bold' },
               'title': {'font': {'color': '#000000','size': 16,'family': 'Arial','weight': 'bold'}}
               
               },
        yaxis={'side': 'left', 
              'tickfont': {'size': 15,'color': '#000000','family': 'Arial','weight': 'bold'},
              
              'title': {'font': {'color': '#000000','size': 16,'family': 'Arial','weight': 'bold'}},
        },
        margin=dict(l=80, r=20, t=50, b=60)
    )
    
    return fig

def create_noise_comparison_chart(left_data, right_data, left_name, right_name,
                                   left_pred_col, right_pred_col, chart_title):
    """
    Create noise comparison chart (3 lines: Actual, Left Algorithm, Right Algorithm)
    """
    left_data = left_data.copy()
    right_data = right_data.copy()
    
    left_data['Datetime'] = pd.to_datetime(left_data['Datetime'], errors='coerce')
    right_data['Datetime'] = pd.to_datetime(right_data['Datetime'], errors='coerce')
    
    fig = go.Figure()
    
    # Actual temperature - Blue
    fig.add_trace(go.Scatter(
        x=left_data['Datetime'],
        y=left_data['T2M'],
        mode='lines+markers',
        name='Actual Temperature',
        line=dict(color='#0000FF', width=3),
        marker=dict(size=5, color='#0000FF'),
        hovertemplate='<b>%{x|%Y-%m-%d %H:%M}</b><br>Actual: %{y:.2f}°C<extra></extra>'
    ))
    
    # Left algorithm - RED
    fig.add_trace(go.Scatter(
        x=left_data['Datetime'],
        y=left_data[left_pred_col],
        mode='lines+markers',
        name=f'{left_name}',
        line=dict(color='#FF0000', width=3),
        marker=dict(size=5, color='#FF0000'),
        hovertemplate=f'<b>%{{x|%Y-%m-%d %H:%M}}</b><br>{left_name}: %{{y:.2f}}°C<extra></extra>'
    ))
    
    # Right algorithm - Turquoise (dotted)
    fig.add_trace(go.Scatter(
        x=right_data['Datetime'],
        y=right_data[right_pred_col],
        mode='lines+markers',
        name=f'{right_name}',
        line=dict(color='#30D5C8', width=3, dash='dot'),
        marker=dict(size=5, color='#30D5C8'),
        hovertemplate=f'<b>%{{x|%Y-%m-%d %H:%M}}</b><br>{right_name}: %{{y:.2f}}°C<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=f"<b>{chart_title}</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=18, color='#2c3e50')
        ),
        xaxis_title="Datetime",
        yaxis_title="Temperature (°C)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=450,
        margin=dict(l=60, r=40, t=80, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(
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

# ==================== NCMRWF CHART FUNCTIONS ====================

# def create_ncmrwf_training_params_chart(classical_algo, quantum_algo, params_data):
#     """
#     Create training parameters chart for NCMRWF models
#     Shows side-by-side comparison
#     """
#     from config.constants import NCMRWF_ALGORITHM_PARAMS
    
#     algorithms = [f"Classical\n({classical_algo})", f"Quantum\n({quantum_algo})"]
    
#     classical_params = [
#         NCMRWF_ALGORITHM_PARAMS[classical_algo]['classical'],
#         NCMRWF_ALGORITHM_PARAMS[quantum_algo]['classical']
#     ]
    
#     quantum_params = [
#         NCMRWF_ALGORITHM_PARAMS[classical_algo]['quantum'],
#         NCMRWF_ALGORITHM_PARAMS[quantum_algo]['quantum']
#     ]

#     is_hybrid = quantum_algo in {
#         'QNN_IS_2.0',
#         'Hybrid QNN_SE',
#         'VQC'
#     }

#     fig = go.Figure()
    
#     # Classical parameters bar
#     fig.add_trace(go.Bar(
#         name='Classical Parameters',
#         x=algorithms,
#         y=classical_params,
#         marker=dict(color='#007bff', opacity=0.8),
#         text=[f'{val:,}' for val in classical_params],
#         textposition='inside',
#         textfont=dict(color='white', size=12, family='Arial Black')
#     ))
    
#     # Quantum parameters bar
#     fig.add_trace(go.Bar(
#         name='Quantum Parameters',
#         x=algorithms,
#         y=quantum_params,
#         base=classical_params if is_hybrid else None,
#         marker=dict(color='#6f42c1', opacity=0.8),
#         text=[f'{val:,}' for val in quantum_params],
#         textposition='inside',
#         textfont=dict(color='white', size=12, family='Arial Black')
#     ))
    
#     fig.update_layout(
#         title=dict(
#             text="<b>NCMRWF Training Parameters Comparison</b>",
#             x=0.5,
#             xanchor='center',
#             font=dict(size=18, color='#000000')
#         ),
#         xaxis=dict(
#             tickfont=dict(size=14, color='#000000'),
#             title=dict(font=dict(color='#000000', size=14))
#         ),
#         yaxis=dict(
#             title=dict(text="Number of Parameters", font=dict(color='#000000', size=14)),
#             tickfont=dict(size=12, color='#000000'),
#             gridcolor='rgba(0,0,0,0.1)'
#         ),
#         plot_bgcolor='white',
#         paper_bgcolor='white',
#         height=500,
#         margin=dict(l=60, r=40, t=60, b=80),
#         showlegend=True,
#         legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=1.02,
#             xanchor="center",
#             x=0.5
#         ),
#         # barmode='group',
#         barmode='overlay',
#         bargap=0.2,  # ← Add this for better spacing
#         bargroupgap=0.1,
#         xaxis_fixedrange=False 
#     )
    
#     return fig

# def create_ncmrwf_training_params_chart(classical_algo, quantum_algo, params_data):
#     """
#     Create training parameters chart for NCMRWF models
#     Shows side-by-side comparison with hybrid model stacking
#     """
#     from config.constants import NCMRWF_ALGORITHM_PARAMS
    
#     algorithms = [f"Classical\n({classical_algo})", f"Quantum\n({quantum_algo})"]
    
#     classical_params = [
#         NCMRWF_ALGORITHM_PARAMS[classical_algo]['classical'],
#         NCMRWF_ALGORITHM_PARAMS[quantum_algo]['classical']
#     ]
    
#     quantum_params = [
#         NCMRWF_ALGORITHM_PARAMS[classical_algo]['quantum'],
#         NCMRWF_ALGORITHM_PARAMS[quantum_algo]['quantum']
#     ]

#     # ✅ CHECK if quantum algorithm is hybrid (has both classical + quantum)
#     is_hybrid = (NCMRWF_ALGORITHM_PARAMS[quantum_algo]['classical'] > 0 and 
#                  NCMRWF_ALGORITHM_PARAMS[quantum_algo]['quantum'] > 0)
def create_ncmrwf_training_params_chart(classical_algo, quantum_algo, params_data):
    """
    Create training parameters chart for NCMRWF models.
    Uses passed params_data so it works for both Univariate and Multivariate.
    """
    if classical_algo not in params_data or quantum_algo not in params_data:
        return None

    algorithms = [f"Classical\n({classical_algo})", f"Quantum\n({quantum_algo})"]

    classical_params = [
        params_data[classical_algo]['classical'],
        params_data[quantum_algo]['classical']
    ]
    quantum_params = [
        params_data[classical_algo]['quantum'],
        params_data[quantum_algo]['quantum']
    ]

    is_hybrid = (
        params_data[quantum_algo]['classical'] > 0 and
        params_data[quantum_algo]['quantum'] > 0
    )
    use_log_scale = is_hybrid and any(
        param > 1000 for param in classical_params + quantum_params
    )

    display_classical, display_quantum = [], []
    text_classical, text_quantum = [], []

    for classical, quantum in zip(classical_params, quantum_params):
        if use_log_scale:
            display_classical.append(np.log10(classical) if classical > 0 else 0)
            display_quantum.append(np.log10(quantum) if quantum > 0 else 0)
            text_classical.append(
                f'{classical:,}<br>(log: {np.log10(classical):.1f})' if classical > 0 else '0'
            )
            text_quantum.append(
                f'{quantum:,}<br>(log: {np.log10(quantum):.1f})' if quantum > 0 else '0'
            )
        else:
            display_classical.append(classical)
            display_quantum.append(quantum)
            text_classical.append(f'{classical:,}' if classical > 0 else '0')
            text_quantum.append(f'{quantum:,}' if quantum > 0 else '0')

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Classical Parameters',
        x=algorithms,
        y=display_classical,
        marker=dict(color='#007bff', opacity=0.8),
        text=text_classical,
        textposition='inside',
        textfont=dict(color='white', size=12, family='Arial Black')
    ))

    fig.add_trace(go.Bar(
        name='Quantum Parameters',
        x=algorithms,
        y=display_quantum,
        base=display_classical if is_hybrid else None,
        marker=dict(color='#6f42c1', opacity=0.8),
        text=text_quantum,
        textposition='inside',
        textfont=dict(color='white', size=12, family='Arial Black')
    ))

    y_title = "Log₁₀(Parameters)" if use_log_scale else "Number of Parameters"
    title_suffix = " (Log Scale)" if use_log_scale else ""

    fig.update_layout(
        title=dict(
            text=f"<b>NCMRWF Training Parameters Comparison{title_suffix}</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=18, color='#000000')
        ),
        xaxis=dict(
            tickfont=dict(size=14, color='#000000'),
            title=dict(font=dict(color='#000000', size=14)),
            tickangle=0
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(color='#000000', size=14)),
            tickfont=dict(size=12, color='#000000'),
            gridcolor='rgba(0,0,0,0.1)'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        margin=dict(l=60, r=40, t=60, b=100),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        barmode='overlay',
        bargap=0.2,
        bargroupgap=0.1,
        xaxis_fixedrange=False
    )

    return fig

def create_ncmrwf_combined_resource_chart(algorithm_name):
    """
    Create combined resource chart for NCMRWF quantum algorithm (QGRU or QLSTM)
    """
    from config.constants import NCMRWF_QUANTUM_RESOURCE_DATA
    
    # Get algorithm index
    algo_idx = NCMRWF_QUANTUM_RESOURCE_DATA['algorithms'].index(algorithm_name)
    
    single_gate = NCMRWF_QUANTUM_RESOURCE_DATA['single_gate_count'][algo_idx]
    multi_gate = NCMRWF_QUANTUM_RESOURCE_DATA['multi_gate_count'][algo_idx]
    depth = NCMRWF_QUANTUM_RESOURCE_DATA['depth'][algo_idx]
    
    fig = go.Figure()
    
    categories = ['Single-Qubit Gates', 'Multi-Qubit Gates', 'Circuit Depth']
    values = [single_gate, multi_gate, depth]
    colors_list = ['#3B82F6', '#10B981', '#F59E0B']
    
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        text=values,
        textposition='outside',
        textfont=dict(color='#000000', size=14),
        marker=dict(color=colors_list, line=dict(color='rgba(0,0,0,0.3)', width=1)),
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=f'<b>Quantum Resources - {algorithm_name}</b>',
            font=dict(size=18, color='#1f2937'),
            x=0.5,
            xanchor="center"
        ),
        xaxis=dict(
            title='Resource Type',
            title_font=dict(size=14, color='#000000'),
            tickfont=dict(size=13, color='#000000')
        ),
        yaxis=dict(
            title='Count',
            title_font=dict(size=14, color='#000000'),
            tickfont=dict(size=13, color='#000000'),
            gridcolor='rgba(0,0,0,0.1)'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        height=500,
        margin=dict(l=50, r=30, t=60, b=50)
    )
    
    return fig


def create_ncmrwf_quantum_resource_charts(height=350):
    """
    Create three separate quantum resource comparison charts for NCMRWF
    (Similar to IMD version but only for QGRU and QLSTM)
    """
    from config.constants import NCMRWF_QUANTUM_RESOURCE_DATA
    
    # Single Gate Count Chart
    fig_single = go.Figure()
    fig_single.add_trace(go.Bar(
        x=NCMRWF_QUANTUM_RESOURCE_DATA["algorithms"],
        y=NCMRWF_QUANTUM_RESOURCE_DATA["single_gate_count"],
        marker=dict(
            color=NCMRWF_QUANTUM_RESOURCE_DATA["colors"],
            line=dict(color='#2D1B69', width=1)
        ),
        text=NCMRWF_QUANTUM_RESOURCE_DATA["single_gate_count"],
        textposition='auto',
        textfont=dict(color='white', size=14, family='Arial Black'),
        hovertemplate='<b>%{x}</b><br>Single Gates: %{y}<br><extra></extra>'
    ))
    
    fig_single.update_layout(
        title=dict(
            text="<b>Single Gate Count</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=18, color='#2c3e50')
        ),
        xaxis_title="Algorithm",
        yaxis_title="Count",
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=height,
        margin=dict(l=50, r=20, t=50, b=60),
        xaxis=dict(tickfont=dict(color='#000000', size=14)),
        yaxis=dict(tickfont=dict(color='#000000', size=14))
    )
    
    # Multi Gate Count Chart
    fig_multi = go.Figure()
    fig_multi.add_trace(go.Bar(
        x=NCMRWF_QUANTUM_RESOURCE_DATA["algorithms"],
        y=NCMRWF_QUANTUM_RESOURCE_DATA["multi_gate_count"],
        marker=dict(
            color=NCMRWF_QUANTUM_RESOURCE_DATA["colors"],
            line=dict(color='#2D1B69', width=1)
        ),
        text=NCMRWF_QUANTUM_RESOURCE_DATA["multi_gate_count"],
        textposition='auto',
        textfont=dict(color='white', size=14, family='Arial Black'),
        hovertemplate='<b>%{x}</b><br>Multi Gates: %{y}<br><extra></extra>'
    ))
    
    fig_multi.update_layout(
        title=dict(
            text="<b>Multi-Gate Count</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=18, color='#2c3e50')
        ),
        xaxis_title="Algorithm",
        yaxis_title="Count",
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=height,
        margin=dict(l=50, r=20, t=50, b=60),
        xaxis=dict(tickfont=dict(color='#000000', size=14)),
        yaxis=dict(tickfont=dict(color='#000000', size=14))
    )
    
    # Circuit Depth Chart
    fig_depth = go.Figure()
    fig_depth.add_trace(go.Bar(
        x=NCMRWF_QUANTUM_RESOURCE_DATA["algorithms"],
        y=NCMRWF_QUANTUM_RESOURCE_DATA["depth"],
        marker=dict(
            color=NCMRWF_QUANTUM_RESOURCE_DATA["colors"],
            line=dict(color='#2D1B69', width=1)
        ),
        text=NCMRWF_QUANTUM_RESOURCE_DATA["depth"],
        textposition='auto',
        textfont=dict(color='white', size=14, family='Arial Black'),
        hovertemplate='<b>%{x}</b><br>Circuit Depth: %{y}<br><extra></extra>'
    ))
    
    fig_depth.update_layout(
        title=dict(
            text="<b>Circuit Depth</b>",
            x=0.5,
            xanchor='center',
            font=dict(size=18, color='#2c3e50')
        ),
        xaxis_title="Algorithm",
        yaxis_title="Depth",
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=height,
        margin=dict(l=50, r=20, t=50, b=60),
        xaxis=dict(tickfont=dict(color='#000000', size=14)),
        yaxis=dict(tickfont=dict(color='#000000', size=14))
    )
    
    return fig_single, fig_multi, fig_depth