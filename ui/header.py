import streamlit as st
from pathlib import Path
import base64

def image_to_base64(image_path):
    """Convert image to base64 string"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def render_header():
    """Render the app header with blue background and logos"""
    try:
        # Adjust the path to your logo directory
        logo_path = Path(__file__).parent.parent / "assests" / "fonts"

        # Load and encode logos
        cdac_base64 = image_to_base64(logo_path / "cdac.png")
        ncmrwf_base64 = image_to_base64(logo_path / "NCMRWF_logo.jpeg")
        meity_base64 = image_to_base64(logo_path / "meity_logo.jpeg")
        imd_base64 = image_to_base64(logo_path / "India_Meteorological_Department_(logo).png")

        # Inject CSS and HTML
        st.markdown("""
        <style>
            /* Hide Streamlit default header */
            header[data-testid="stHeader"],
            [data-testid="stToolbar"],
            .stApp > header {
                display: none !important;
                height: 0 !important;
                padding: 0 !important;
                margin: 0 !important;
            }

            /* Remove ALL spacing from main container */
            .main .block-container {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            /* 👇 ADD THESE NEW LINES */
            .element-container:first-of-type {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }

            .stMarkdown:first-child {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }

            div[data-testid="stVerticalBlock"] > div:first-child {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            
            /* Remove spacing from all main sections */
            section.main > div {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }

            /* Blue header styling */
            .blue-header-wrapper {
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #2563eb 100%);
                padding: 10px 20px;
                border-radius: 0 0 24px 24px;
                box-shadow: 0 8px 25px rgba(30, 64, 175, 0.3);
                width: 100%;
                max-width: none;s
                margin: 0 !important;
                margin-top: -35px !important;  
                margin-bottom: 0px !important;  /* ✅ NO bottom margin */
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                position: relative;              /* ✅ ADD THIS */
                top: 0;  
            }

            .logo-group {
                display: flex;
                gap: 10px;
            }

            .logo-group img {
                height: 100px;
                background: white;
                padding: 8px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }

            .header-title {
                flex: 1;
                text-align: center;
                color: white;
                font-size: 2rem;
                font-weight: bold;
                margin: 0 20px;
            }
            
            .logo-cdac {
                height: 120px;
            }

            .logo-ncmrwf {
                height: 120px;
            }

            .logo-imd {
                height: 120px;
            }
            
            .logo-meity {
                height: 110px;
                width: 250px;
                max-height: 100px;
                max-width: 100px;
                object-fit: contain;
                padding: 0;
                margin: 0;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="blue-header-wrapper">
            <div class="logo-group">
                <img class="logo-cdac" src="data:image/png;base64,{cdac_base64}" alt="CDAC">
                <img class="logo-ncmrwf" src="data:image/jpeg;base64,{ncmrwf_base64}" alt="NCMRWF">
            </div>
            <div class="header-title">🌤️ Weather Prediction and Modeling</div>
            <div class="logo-group">
                <img class="logo-meity"  src="data:image/jpeg;base64,{meity_base64}" alt="MeitY">
                <img  class="logo-imd" src="data:image/png;base64,{imd_base64}" alt="IMD">
            </div>
        </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError as e:
        st.error(f"❌ Missing file: {e.filename}")
        render_fallback_header()
    except Exception as e:
        st.warning(f"Error loading logos: {str(e)}")
        render_fallback_header()

def render_fallback_header():
    """Fallback header without logos"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem; 
                background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); 
                border-radius: 0 0 12px 12px; margin-bottom: 1rem; 
                box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);">
        <h1 style="color: #ffffff; font-weight: 900; margin: 0;">Weather Prediction & Modeling</h1>
        <p style="color: #ffffff; margin-top: 10px;">Renewable Weather Prediction System</p>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render a development-mode footer"""
    st.markdown("""
    <div style="text-align: center; margin-top: 1rem; padding: 2rem; 
                background: #f9fafb; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05); 
                border-top: 4px solid #3b82f6; font-size: 0.95rem; color: #374151;">
        <p style="margin-top: 1rem;">
            Owned & maintained by: Centre for Development of Advanced Computing (C-DAC)
        </p>
    </div>
    """, unsafe_allow_html=True)