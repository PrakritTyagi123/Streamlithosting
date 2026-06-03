# visualization/maps.py
"""
Map creation functions using Folium with subzone support
Optimized: GeoJSON cached, map cached, session state passed as params
"""
import folium
from folium import plugins
import streamlit as st
import os


@st.cache_resource
def get_india_boundary():
    """Download India boundary GeoJSON once and cache it for the entire session"""
    import requests

    boundary_file = 'india_boundary.geojson'

    if os.path.exists(boundary_file):
        return boundary_file

    try:
        url = 'https://raw.githubusercontent.com/datameet/maps/master/Country/india-composite.geojson'
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        with open(boundary_file, 'w') as f:
            f.write(r.text)
        return boundary_file
    except Exception:
        return None


@st.cache_data
def create_zoom_map(selected_city, cities_data, selected_subzone=None,
                    classical_data=None, quantum_data=None, custom_datetime=None,
                    last_values=None):# for meteogram's "Last Values" feature
    """
    Create map and return it as a cached HTML string.
    Returns HTML string (pickle-serializable) instead of folium.Map object.

    Args:
        selected_city: Name of the selected city
        cities_data: Dictionary of city information
        selected_subzone: Optional subzone string e.g. "Delhi - North Delhi"
        classical_data: Dict from st.session_state.classical_data (passed explicitly for caching)
        quantum_data: Dict from st.session_state.quantum_data (passed explicitly for caching)
        custom_datetime: Optional datetime for custom map point
    """

    # ==================== DETERMINE MAP CENTER ====================
    if selected_subzone and selected_subzone != "None (City Level)":
        if " - " in str(selected_subzone):
            parent_city, subzone_name = str(selected_subzone).split(" - ", 1)
            if parent_city in cities_data and 'subzones' in cities_data[parent_city]:
                if subzone_name in cities_data[parent_city]['subzones']:
                    subzone_info = cities_data[parent_city]['subzones'][subzone_name]
                    center_lat = subzone_info['lat']
                    center_lon = subzone_info['lon']
                    zoom_level = 13
                    selected_city = parent_city
                else:
                    city_info = cities_data[parent_city]
                    center_lat = city_info['lat']
                    center_lon = city_info['lon']
                    zoom_level = 10
            else:
                center_lat, center_lon = 20.5937, 78.9629
                zoom_level = 5
        else:
            center_lat, center_lon = 20.5937, 78.9629
            zoom_level = 5
    elif selected_city in cities_data:
        city_info = cities_data[selected_city]
        center_lat = city_info['lat']
        center_lon = city_info['lon']
        zoom_level = 10
    else:
        center_lat, center_lon = 20.5937, 78.9629
        zoom_level = 5

    # ==================== CREATE BASE MAP ====================
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_level,
        tiles=None,
        control_scale=True
    )

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery',
        name='Satellite View',
        overlay=False,
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='OSM Labels',
        name='Street Labels',
        overlay=True,
        control=True,
        opacity=0.6
    ).add_to(m)

    # ==================== INDIA BOUNDARY (cached) ====================
    boundary_file = get_india_boundary()

    if boundary_file and os.path.exists(boundary_file):
        folium.GeoJson(
            boundary_file,
            name='India Boundary',
            style_function=lambda feature: {
                'fillColor': 'none',
                'color': '#0066cc',
                'weight': 2.5,
                'opacity': 0.85
            }
        ).add_to(m)

    # ==================== PREDICTION DATA ====================
    if selected_city in cities_data:
        selected_info = cities_data[selected_city]

        classical_pred = None
        quantum_pred = None
        actual_temp = None
        pred_date = None

        if classical_data:
            if custom_datetime:
                classical_df = classical_data['data']
                pred_col = classical_data.get('prediction_column')
                matching_row = classical_df[classical_df['Datetime'] == custom_datetime]
                if not matching_row.empty:
                    classical_pred = matching_row[pred_col].values[0]
                    actual_temp = matching_row['T2M'].values[0] if 'T2M' in matching_row.columns else None
                    pred_date = custom_datetime
            else:
                classical_pred = classical_data['prediction']
                actual_temp = classical_data['actual_temp']
                pred_date = classical_data['last_datetime']

        if quantum_data:
            if custom_datetime:
                quantum_df = quantum_data['data']
                pred_col = quantum_data.get('prediction_column')
                matching_row = quantum_df[quantum_df['Datetime'] == custom_datetime]
                if not matching_row.empty:
                    quantum_pred = matching_row[pred_col].values[0]
                    if actual_temp is None:
                        actual_temp = matching_row['T2M'].values[0] if 'T2M' in matching_row.columns else None
                    if pred_date is None:
                        pred_date = custom_datetime
            else:
                quantum_pred = quantum_data['prediction']
                if actual_temp is None:
                    actual_temp = quantum_data['actual_temp']
                if pred_date is None:
                    pred_date = quantum_data['last_datetime']

        # ==================== BUILD CITY POPUP ====================
        popup_html = f"""
        <div style="width: 340px; font-family: 'Segoe UI', Tahoma, sans-serif; padding: 14px;">
            <h3 style="color: #003d82; margin: 0 0 14px 0; border-bottom: 3px solid #0066cc; padding-bottom: 10px; font-size: 18px;">
                📍 {selected_city}
            </h3>
            <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 12px;">
                <p style="margin: 4px 0; font-size: 14px;"><b>Region:</b> {selected_info['region']}</p>
                <p style="margin: 4px 0; font-size: 14px;"><b>Coordinates:</b> {selected_info['lat']:.4f}°N, {selected_info['lon']:.4f}°E</p>
            </div>
        """

        if pred_date:
            popup_html += f"""
            <div style="background: #e3f2fd; padding: 10px; border-radius: 8px; margin-bottom: 12px; text-align: center;">
                <p style="margin: 0; color: #0066cc; font-weight: bold; font-size: 15px;">
                    📅 {pred_date.strftime('%d %B %Y, %H:%M')}
                </p>
            </div>
            """

        if actual_temp is not None:
            popup_html += f"""
            <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #ffc107; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 13px; color: #856404; font-weight: bold; letter-spacing: 0.5px;">🌡️ ACTUAL TEMPERATURE</p>
                <p style="margin: 6px 0 0 0; font-size: 28px; color: #000; font-weight: bold;">{actual_temp:.1f}°C</p>
            </div>
            """

        if classical_pred is not None:
            classical_algo = classical_data['algorithm']
            popup_html += f"""
            <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #0066cc; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 13px; color: #01579b; font-weight: bold; letter-spacing: 0.5px;">🖥️ CLASSICAL ({classical_algo})</p>
                <p style="margin: 6px 0 0 0; font-size: 28px; color: #0066cc; font-weight: bold;">{classical_pred:.1f}°C</p>
            </div>
            """

        if quantum_pred is not None:
            quantum_algo = quantum_data['algorithm']
            popup_html += f"""
            <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #6f42c1; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <p style="margin: 0; font-size: 13px; color: #4a148c; font-weight: bold; letter-spacing: 0.5px;">⚛️ QUANTUM ({quantum_algo})</p>
                <p style="margin: 6px 0 0 0; font-size: 28px; color: #6f42c1; font-weight: bold;">{quantum_pred:.1f}°C</p>
            </div>
            """

        if last_values: ##POP comes here only when "Show Last Values" is checked in Meteogram tab. It shows the latest actual and quantum values for all parameters (not just temperature) in a compact format.
            icons    = {"temperature": "🌡️", "humidity": "💧", "pressure": "🔵"}
            q_colors = {"temperature": "#e74c3c", "humidity": "#27ae60", "pressure": "#8e44ad"}

            lv_rows = ""
            for p, v in last_values.items():
                icon    = icons.get(p, "📊")
                q_color = q_colors.get(p, "#333")
                unit    = v["unit"]

                actual_html = (
                    f'<span style="font-size:14px;font-weight:700;color:#2c3e50;">'
                    f'{v["actual"]:.1f} {unit}</span>'
                    if v["actual"] is not None else
                    '<span style="color:#aaa;font-size:13px;">—</span>'
                )
                quantum_html = (
                    f'<span style="font-size:14px;font-weight:700;color:{q_color};">'
                    f'{v["quantum"]:.1f} {unit}</span>'
                    if v["quantum"] is not None else
                    '<span style="color:#aaa;font-size:13px;">—</span>'
                )

                lv_rows += f"""
                <div style="padding:7px 0;border-bottom:1px solid #f0f0f0;">
                    <div style="font-size:12px;font-weight:700;color:#374151;
                                margin-bottom:4px;">{icon} {v['label']}</div>
                    <div style="display:flex;gap:16px;">
                        <div style="flex:1;background:#f8f9fa;border-radius:6px;
                                    padding:5px 8px;text-align:center;">
                            <div style="font-size:10px;color:#6b7280;
                                        margin-bottom:2px;">⚫ Actual</div>
                            {actual_html}
                        </div>
                        <div style="flex:1;background:#fff5f5;border-radius:6px;
                                    padding:5px 8px;text-align:center;
                                    border:1px solid {q_color}22;">
                            <div style="font-size:10px;color:#6b7280;
                                    margin-bottom:2px;">{v.get('source_label','⚛️ Quantum')}</div>
                            {quantum_html}
                        </div>
                    </div>
                </div>
                """

            popup_html += f"""
            <div style="background:#f8faff;border:1px solid #dbeafe;border-radius:8px;
                        padding:12px 14px;margin-top:6px;">
                <p style="margin:0 0 8px 0;font-size:12px;color:#6b7280;font-weight:600;
                           letter-spacing:0.5px;">📅 LATEST VALUES (LAST DATA POINT)</p>
                {lv_rows}
            </div>
            """

        if not classical_pred and not quantum_pred and not last_values:
            popup_html += """
            <div style="text-align: center; padding: 20px; background: #f5f5f5; border-radius: 8px; border: 2px dashed #ccc;">
                <p style="margin: 0; color: #666; font-style: italic; font-size: 14px;">
                    ⚠️ Generate predictions to see results
                </p>
            </div>
            """

        popup_html += "</div>"

        # Main city marker — only when no subzone selected
        if not selected_subzone or selected_subzone == "None (City Level)":
            folium.Marker(
                [center_lat, center_lon],
                popup=folium.Popup(popup_html, max_width=370),
                tooltip=f"🌡️ {selected_city} - Click for predictions",
                icon=folium.Icon(color='red', icon='thermometer-half', prefix='fa')
            ).add_to(m)

        # ==================== SUBZONE MARKERS ====================
        if 'subzones' in selected_info:
            for subzone_name, subzone_info in selected_info['subzones'].items():
                is_selected = False
                if selected_subzone and selected_subzone != "None (City Level)":
                    if " - " in str(selected_subzone):
                        _, selected_name = str(selected_subzone).split(" - ", 1)
                        if selected_name == subzone_name:
                            is_selected = True

                if is_selected:
                    subzone_popup_html = f"""
                    <div style="width: 340px; font-family: 'Segoe UI', Tahoma, sans-serif; padding: 14px;">
                        <h3 style="color: #003d82; margin: 0 0 14px 0; border-bottom: 3px solid #0066cc; padding-bottom: 10px; font-size: 18px;">
                            📍 {subzone_name}
                        </h3>
                        <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 12px;">
                            <p style="margin: 4px 0; font-size: 14px;"><b>Zone:</b> {subzone_info['region']}</p>
                            <p style="margin: 4px 0; font-size: 14px;"><b>Parent City:</b> {selected_city}</p>
                            <p style="margin: 4px 0; font-size: 14px;"><b>Coordinates:</b> {subzone_info['lat']:.4f}°N, {subzone_info['lon']:.4f}°E</p>
                        </div>
                    """

                    if pred_date:
                        subzone_popup_html += f"""
                        <div style="background: #e3f2fd; padding: 10px; border-radius: 8px; margin-bottom: 12px; text-align: center;">
                            <p style="margin: 0; color: #0066cc; font-weight: bold; font-size: 15px;">
                                📅 {pred_date.strftime('%d %B %Y, %H:%M')}
                            </p>
                        </div>
                        """

                    if actual_temp is not None:
                        subzone_popup_html += f"""
                        <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #ffc107; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <p style="margin: 0; font-size: 13px; color: #856404; font-weight: bold;">🌡️ ACTUAL</p>
                            <p style="margin: 6px 0 0 0; font-size: 28px; color: #000; font-weight: bold;">{actual_temp:.1f}°C</p>
                        </div>
                        """

                    if classical_pred is not None:
                        classical_algo = classical_data['algorithm']
                        subzone_popup_html += f"""
                        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #0066cc; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <p style="margin: 0; font-size: 13px; color: #01579b; font-weight: bold;">🖥️ {classical_algo}</p>
                            <p style="margin: 6px 0 0 0; font-size: 28px; color: #0066cc; font-weight: bold;">{classical_pred:.1f}°C</p>
                        </div>
                        """

                    if quantum_pred is not None:
                        quantum_algo = quantum_data['algorithm']
                        subzone_popup_html += f"""
                        <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #6f42c1; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <p style="margin: 0; font-size: 13px; color: #4a148c; font-weight: bold;">⚛️ {quantum_algo}</p>
                            <p style="margin: 6px 0 0 0; font-size: 28px; color: #6f42c1; font-weight: bold;">{quantum_pred:.1f}°C</p>
                        </div>
                        """

                    subzone_popup_html += "</div>"

                    folium.Marker(
                        [subzone_info['lat'], subzone_info['lon']],
                        popup=folium.Popup(subzone_popup_html, max_width=370),
                        tooltip=f"📍 {subzone_name} (Selected)",
                        icon=folium.Icon(color='red', icon='map-marker', prefix='fa')
                    ).add_to(m)

    # ==================== MAP CONTROLS ====================
    plugins.MiniMap(toggle_display=True, position='bottomleft').add_to(m)

    plugins.Fullscreen(
        position='topright',
        title='View Fullscreen',
        title_cancel='Exit Fullscreen',
        force_separate_button=True
    ).add_to(m)

    folium.LayerControl(position='topright').add_to(m)

    # Return HTML string — pickle-serializable so @st.cache_data works
    return m.get_root().render()