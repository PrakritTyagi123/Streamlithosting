# visualization/plotly_maps.py
"""
Improved Plotly Mapbox with auto-update and embedded info panel
"""
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import pandas as pd


def create_plotly_weather_map(selected_city, cities_data, selected_subzone=None, selected_datetime=None):
    """
    Create interactive Plotly Mapbox with embedded info panel
    
    Args:
        selected_city: City name (e.g., "Delhi")
        cities_data: Dictionary with city information
        selected_subzone: Optional subzone selection (e.g., "Delhi - Safdarjung")
        selected_datetime: Optional datetime for predictions
    
    Returns:
        Plotly Figure object
    """
    
    # Determine center and zoom based on selection
    if selected_subzone and selected_subzone != "None (City Level)":
        if " - " in str(selected_subzone):
            parent_city, subzone_name = str(selected_subzone).split(" - ", 1)
            if parent_city in cities_data and 'subzones' in cities_data[parent_city]:
                if subzone_name in cities_data[parent_city]['subzones']:
                    subzone_info = cities_data[parent_city]['subzones'][subzone_name]
                    center_lat = subzone_info['lat']
                    center_lon = subzone_info['lon']
                    zoom_level = 12
                    location_name = subzone_name
                    location_region = subzone_info['region']
                    parent_name = parent_city
                else:
                    city_info = cities_data[parent_city]
                    center_lat = city_info['lat']
                    center_lon = city_info['lon']
                    zoom_level = 9
                    location_name = parent_city
                    location_region = city_info['region']
                    parent_name = None
            else:
                center_lat, center_lon = 20.5937, 78.9629
                zoom_level = 4
                location_name = "India"
                location_region = "Overview"
                parent_name = None
        else:
            center_lat, center_lon = 20.5937, 78.9629
            zoom_level = 4
            location_name = "India"
            location_region = "Overview"
            parent_name = None
    elif selected_city in cities_data:
        city_info = cities_data[selected_city]
        center_lat = city_info['lat']
        center_lon = city_info['lon']
        zoom_level = 9
        location_name = selected_city
        location_region = city_info['region']
        parent_name = None
    else:
        center_lat, center_lon = 20.5937, 78.9629
        zoom_level = 4
        location_name = "India"
        location_region = "Overview"
        parent_name = None
    
    # Get prediction data from session state
    classical_pred = None
    quantum_pred = None
    actual_temp = None
    pred_datetime = None
    classical_algo = None
    quantum_algo = None
    
    # Use custom datetime if provided
    if selected_datetime:
        custom_datetime = selected_datetime
    else:
        custom_datetime = st.session_state.get('custom_map_datetime', None)
    
    # Extract classical predictions
    if st.session_state.get('classical_data'):
        classical_df = st.session_state.classical_data['data']
        pred_col = st.session_state.classical_data.get('prediction_column')
        
        if custom_datetime:
            matching_row = classical_df[classical_df['Datetime'] == custom_datetime]
            if not matching_row.empty:
                classical_pred = matching_row[pred_col].values[0]
                actual_temp = matching_row['T2M'].values[0] if 'T2M' in matching_row.columns else None
                pred_datetime = custom_datetime
        else:
            classical_pred = st.session_state.classical_data['prediction']
            actual_temp = st.session_state.classical_data['actual_temp']
            pred_datetime = st.session_state.classical_data['last_datetime']
        
        classical_algo = st.session_state.classical_data['algorithm']
    
    # Extract quantum predictions
    if st.session_state.get('quantum_data'):
        quantum_df = st.session_state.quantum_data['data']
        pred_col = st.session_state.quantum_data.get('prediction_column')
        
        if custom_datetime:
            matching_row = quantum_df[quantum_df['Datetime'] == custom_datetime]
            if not matching_row.empty:
                quantum_pred = matching_row[pred_col].values[0]
                if actual_temp is None:
                    actual_temp = matching_row['T2M'].values[0] if 'T2M' in matching_row.columns else None
                if pred_datetime is None:
                    pred_datetime = custom_datetime
        else:
            quantum_pred = st.session_state.quantum_data['prediction']
            if actual_temp is None:
                actual_temp = st.session_state.quantum_data['actual_temp']
            if pred_datetime is None:
                pred_datetime = st.session_state.quantum_data['last_datetime']
        
        quantum_algo = st.session_state.quantum_data['algorithm']
    
    # Create the figure
    fig = go.Figure()
    
    # Add marker for location
    marker_text = f"{location_name}"
    if parent_name:
        marker_text += f" ({parent_name})"
    
    fig.add_trace(go.Scattermapbox(
        lat=[center_lat],
        lon=[center_lon],
        mode='markers',
        marker=dict(
            size=15,
            color='red',
            symbol='marker'
        ),
        text=marker_text,
        hoverinfo='text',
        showlegend=False
    ))
    
    # Build info panel HTML (RIGHT SIDE OF MAP)
    info_html = f"""
    <div style="
        position: absolute;
        top: 20px;
        right: 20px;
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        min-width: 280px;
        max-width: 320px;
        font-family: 'Segoe UI', Arial, sans-serif;
        z-index: 1000;
    ">
        <h3 style="margin: 0 0 15px 0; color: #003d82; border-bottom: 3px solid #0066cc; padding-bottom: 8px; font-size: 18px;">
            📍 {location_name}
        </h3>
        
        <div style="margin-bottom: 15px; padding: 10px; background: #f8f9fa; border-radius: 8px;">
            <p style="margin: 4px 0; font-size: 13px; color: #333;"><b>Region:</b> {location_region}</p>
            <p style="margin: 4px 0; font-size: 13px; color: #333;"><b>Coordinates:</b> {center_lat:.4f}°N, {center_lon:.4f}°E</p>
        </div>
    """
    
    if pred_datetime:
        formatted_datetime = pred_datetime.strftime('%d %b %Y, %H:%M')
        info_html += f"""
        <div style="background: #e3f2fd; padding: 10px; border-radius: 8px; margin-bottom: 15px; text-align: center;">
            <p style="margin: 0; color: #0066cc; font-weight: bold; font-size: 14px;">
                📅 {formatted_datetime}
            </p>
        </div>
        """
    
    if actual_temp is not None:
        info_html += f"""
        <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #ffc107;">
            <p style="margin: 0; font-size: 12px; color: #856404; font-weight: bold; letter-spacing: 0.5px;">🌡️ ACTUAL</p>
            <p style="margin: 6px 0 0 0; font-size: 24px; color: #000; font-weight: bold;">{actual_temp:.1f}°C</p>
        </div>
        """
    
    if classical_pred is not None and classical_algo:
        info_html += f"""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #0066cc;">
            <p style="margin: 0; font-size: 12px; color: #01579b; font-weight: bold; letter-spacing: 0.5px;">🖥️ {classical_algo}</p>
            <p style="margin: 6px 0 0 0; font-size: 24px; color: #0066cc; font-weight: bold;">{classical_pred:.1f}°C</p>
        </div>
        """
    
    if quantum_pred is not None and quantum_algo:
        info_html += f"""
        <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #6f42c1;">
            <p style="margin: 0; font-size: 12px; color: #4a148c; font-weight: bold; letter-spacing: 0.5px;">⚛️ {quantum_algo}</p>
            <p style="margin: 6px 0 0 0; font-size: 24px; color: #6f42c1; font-weight: bold;">{quantum_pred:.1f}°C</p>
        </div>
        """
    
    if not classical_pred and not quantum_pred:
        info_html += """
        <div style="text-align: center; padding: 20px; background: #f5f5f5; border-radius: 8px; border: 2px dashed #ccc;">
            <p style="margin: 0; color: #666; font-style: italic; font-size: 13px;">
                ⚠️ Generate predictions to see results
            </p>
        </div>
        """
    
    info_html += "</div>"
    
    # Configure map layout - Using OpenStreetMap (no token needed)
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom_level
        ),
        showlegend=False,
        hovermode='closest',
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        annotations=[
            dict(
                text=info_html,
                showarrow=False,
                xref="paper",
                yref="paper",
                x=1,
                y=1,
                xanchor='right',
                yanchor='top',
                align='left',
                bgcolor='rgba(0,0,0,0)',
                bordercolor='rgba(0,0,0,0)'
            )
        ]
    )
    
    return fig


@st.fragment
def render_map_controls_fragment(map_type="temperature"):
    """
    Fragment for date/time controls - only this part reruns on change
    """
    # Determine which session state keys to use
    if map_type == "temperature":
        city_key = 'temp_generation_city'
        subzone_key = 'temp_subzone_selector'
        data_key_classical = 'classical_data'
        data_key_quantum = 'quantum_data'
        date_key = 'temp_selected_map_date'
        time_key = 'temp_selected_map_time'
        custom_datetime_key = 'temp_custom_map_datetime'
    else:  # rain
        city_key = 'rain_generation_city'
        subzone_key = 'rain_subzone_selector'
        data_key_classical = 'classical_rain_data'
        data_key_quantum = 'quantum_rain_data'
        date_key = 'rain_selected_map_date'
        time_key = 'rain_selected_map_time'
        custom_datetime_key = 'rain_custom_map_datetime'
    
    # Get data source
    data_source = (st.session_state.get(data_key_classical) or 
                   st.session_state.get(data_key_quantum))
    
    if not data_source:
        return None, None
    
    # Extract dataframe
    if 'data' in data_source:
        df = data_source['data']
    else:
        df = data_source
    
    min_date = df['Datetime'].min().date()
    max_date = df['Datetime'].max().date()
    
    # Initialize defaults
    if date_key not in st.session_state:
        st.session_state[date_key] = max_date
    if time_key not in st.session_state:
        st.session_state[time_key] = df['Datetime'].max().time()
    
    # Styled date/time controls
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px; border-radius: 10px; margin-bottom: 10px;">
        <h4 style="color: white; margin: 0 0 10px 0;">🗓️ Select Date & Time</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        selected_date = st.date_input(
            "📅 Date",
            value=st.session_state[date_key],
            min_value=min_date,
            max_value=max_date,
            key=f"{map_type}_map_date_widget"
        )
    
    with col2:
        # Get available times for selected date
        available_times = df[
            df['Datetime'].dt.date == selected_date
        ]['Datetime'].dt.time.unique()
        
        if len(available_times) > 0:
            available_times_sorted = sorted(available_times)
            
            # Find current time index
            default_time_index = len(available_times_sorted) - 1
            if st.session_state[time_key] in available_times_sorted:
                default_time_index = available_times_sorted.index(st.session_state[time_key])
            
            selected_time = st.selectbox(
                "⏰ Time",
                options=available_times_sorted,
                index=default_time_index,
                key=f"{map_type}_map_time_widget"
            )
        else:
            st.warning("No data for selected date")
            selected_time = None
    
    # Auto-update session state when selection changes
    if selected_time:
        from datetime import datetime
        new_datetime = datetime.combine(selected_date, selected_time)
        
        # Only update if changed
        if (st.session_state.get(date_key) != selected_date or 
            st.session_state.get(time_key) != selected_time):
            st.session_state[date_key] = selected_date
            st.session_state[time_key] = selected_time
            st.session_state[custom_datetime_key] = new_datetime
            st.session_state['custom_map_datetime'] = new_datetime
        
        current_datetime = new_datetime
        st.info(f"📍 Showing: {current_datetime.strftime('%d-%m-%Y %H:%M')}")
    else:
        current_datetime = None
        st.info("📍 Showing: Latest prediction")
    
    return current_datetime, selected_date


def render_map_with_controls(map_type="temperature"):
    """
    Main function to render map with auto-updating controls
    """
    from config.constants import CITIES
    
    # Get city and subzone
    if map_type == "temperature":
        city_key = 'temp_generation_city'
        subzone_key = 'temp_subzone_selector'
        data_key_classical = 'classical_data'
        data_key_quantum = 'quantum_data'
    else:
        city_key = 'rain_generation_city'
        subzone_key = 'rain_subzone_selector'
        data_key_classical = 'classical_rain_data'
        data_key_quantum = 'quantum_rain_data'
    
    city = st.session_state.get(city_key, 'Delhi')
    selected_subzone = st.session_state.get(subzone_key, None)
    
    # Check if predictions exist
    has_data = (st.session_state.get(data_key_classical) or 
                st.session_state.get(data_key_quantum))
    
    if not has_data:
        st.info("🎯 Generate predictions first to enable interactive map")
        fig = create_plotly_weather_map(city, CITIES, selected_subzone)
        st.plotly_chart(fig, use_container_width=True, key=f"{map_type}_basic_map")
        return
    
    # Render controls (fragment - only this reruns)
    current_datetime, selected_date = render_map_controls_fragment(map_type)
    
    # Create and display map
    fig = create_plotly_weather_map(city, CITIES, selected_subzone, current_datetime)
    st.plotly_chart(fig, use_container_width=True, key=f"{map_type}_main_map")