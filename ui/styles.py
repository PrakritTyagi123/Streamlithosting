# ui/styles.py
"""
CSS styling for the Streamlit app - Professional Blue Theme (No Waves)
"""
import streamlit as st


def apply_custom_css():
    """Apply custom CSS styling to the app with Professional Blue theme"""
    st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    /* ==================== REMOVE ALL TOP SPACE ==================== */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
        margin-top: 0rem !important;
    }
    
    section.main > div:first-child {
        padding-top: 0rem !important;
        margin-top: 0 !important;
    }
    
    /* ✅ CRITICAL: Attach tabs directly to header */
    .stTabs {
        margin-top: -10px !important;
        padding-top: 0 !important;
    }

    [data-baseweb="tab-list"] {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    
    header {
        visibility: hidden !important;
        height: 0 !important;
    }
    
    [data-testid="stToolbar"] {
        display: none !important;
    }
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        # background: Pure;
        background:#ffffff;
    }
    
    .stApp {
        background: #ffffff;
        
        
    }
    /* Remove heading anchor links */
    .element-container a[href^="#"] {
        display: none !important;
    }

    h1 a, h2 a, h3 a, h4 a {
        display: none !important;
    }

    /* Remove image fullscreen button */
    button[title="View fullscreen"] {
        display: none !important;
    }

    [data-testid="StyledFullScreenButton"] {
        display: none !important;
    }

    /* Alternative selector for fullscreen button */
    .element-container button[kind="header"] {
        display: none !important;
    }
    /* Remove ALL fullscreen buttons from images */
    button[title="View fullscreen"],
    button[aria-label="View fullscreen"],
    [data-testid="StyledFullScreenButton"],
    .stImage button,
    .element-container button[kind="header"],
    div[data-testid="stImage"] button {
        display: none !important;
        visibility: hidden !important;
    }

    /* Hide fullscreen overlay on hover */
    .stImage:hover button {
        display: none !important;
    }
    /* ADD THESE NEW LINES BELOW */
    /* FORCE hide fullscreen button - most aggressive approach */
    .stImage button[kind="header"] {
        display: none !important;
    }

    button[data-testid="baseButton-header"] {
        display: none !important;
    }

    /* Hide ANY button inside image container */
    [data-testid="stImage"] button,
    [data-testid="stImage"] > div > button,
    [data-testid="stImage"] > div > div > button {
        display: none !important;
        pointer-events: none !important;
    }

    /* Target by position - last child button */
    .stImage > div:last-child button {
        display: none !important;
    }

    /* ==================== CONFIGURATION SECTION ==================== */
    .config-section {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(30, 64, 175, 0.1);
        margin-bottom: 2rem;
    }
    
    /* ==================== INFO BOXES ==================== */
    .info-box {
        background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
        border-left: 5px solid #3b82f6;
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        color: #1e40af;
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(59, 130, 246, 0.15);
    }
    
    .info-box i {
        font-size: 1.5rem;
        color: #3b82f6;
    }
    
    /* ==================== SIDEBAR STYLING ==================== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #eff6ff 0%, #dbeafe 100%);
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent;
    }
    
    section[data-testid="stSidebar"] label {
        color: #1e40af !important;
        font-weight: 600 !important;
    }
    
    /* ==================== INPUT FIELDS ==================== */
    .stSelectbox label,
    .stDateInput label,
    div[data-testid="stDateInput"] label,
    div[data-testid="stSelectbox"] label {
        color: #000000 !important;
        font-weight: 900 !important;  /* Changed from 600 to 700 for extra bold */
        font-size: 1.4rem !important;
        letter-spacing: 0.5px !important;
        text-transform: none !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Make all form labels bold */
    label {
        font-weight: 900 !important;
        font-size: 1.4rem !important;
    }
    
    .stSelectbox > div > div,
    .stDateInput > div > div > input {
        background-color: white !important;
        border: 2px solid #bfdbfe !important;
        border-radius: 10px !important;
        color: #1e40af !important;
        font-weight: 500 !important;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover,
    .stDateInput > div > div > input:hover {
        border-color: #93c5fd !important;
    }
    
    .stSelectbox > div > div:focus,
    .stDateInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* ==================== BUTTONS ==================== */
    .stButton > button {
        width: 100%;
        height: 3.5rem;
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* ==================== METRICS CARDS ==================== */
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e0f2fe;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.1);
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(30, 64, 175, 0.2);
        border-color: #3b82f6;
    }
    
    .stMetric label {
        color: #64748b !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.85rem !important;
        letter-spacing: 0.5px;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #1e40af !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
    }
    
    /* ==================== HEADINGS ==================== */
    h1, h2, h3, h4 {
    font-weight: 700 !important;
    }
    /* Default blue color for headings in main content */
    .main h1, .main h2, .main h3, .main h4 {
        color: #1e40af !important;
    }

    /* Override: Allow white color when explicitly set in inline styles */
    h1[style*="color: white"],
    h2[style*="color: white"],
    h3[style*="color: white"],
    h4[style*="color: white"],
    h1[style*="color:white"],
    h2[style*="color:white"],
    h3[style*="color:white"],
    h4[style*="color:white"] {
        color: white !important;
    }

    
    
    /* ==================== ALERTS ==================== */
    .stAlert {
        background: linear-gradient(135deg, #dbeafe, #eff6ff) !important;
        border-left: 5px solid #3b82f6 !important;
        color: #1e40af !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* ==================== DATA TABLES ==================== */
     /* ==================== DATA TABLES ==================== */
    .stDataFrame {
        background: white !important;
        border-radius: 12px !important;
        border: 2px solid #e0f2fe !important;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.1) !important;
        overflow: hidden;
    }
    
    /* Table Header Styling - MULTIPLE SELECTORS FOR COMPATIBILITY */
    .stDataFrame thead tr th,
    .stDataFrame thead th,
    .stDataFrame th,
    div[data-testid="stDataFrame"] thead tr th,
    div[data-testid="stDataFrame"] th {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 1.2rem 1.5rem !important;
        border: none !important;
        text-align: center !important;
        letter-spacing: 0.5px !important;
    }
    
    /* ALTERNATIVE: Target first row if it's not in thead */
    .stDataFrame tbody tr:first-child td,
    div[data-testid="stDataFrame"] tbody tr:first-child td {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 1.2rem 1.5rem !important;
        text-align: center !important;
    }
    
    /* Table Body - All Cells Larger (skip first row) */
    .stDataFrame tbody tr:not(:first-child) td,
    div[data-testid="stDataFrame"] tbody tr:not(:first-child) td {
        font-size: 1.05rem !important;
        padding: 1rem 1.5rem !important;
        border-bottom: 1px solid #e0f2fe !important;
        text-align: center !important;
    }
    
    /* First Column (Metric Names) - Left Aligned (skip header row) */
    .stDataFrame tbody tr:not(:first-child) td:first-child,
    div[data-testid="stDataFrame"] tbody tr:not(:first-child) td:first-child {
        font-weight: 600 !important;
        color: #1e40af !important;
        text-align: left !important;
        background: #f8fafc !important;
    }
    
    /* Second Column (Classical Algorithm) - BLUE Background (skip header) */
    .stDataFrame tbody tr:not(:first-child) td:nth-child(2),
    div[data-testid="stDataFrame"] tbody tr:not(:first-child) td:nth-child(2) {
        background: linear-gradient(135deg, #bfdbfe 0%, #dbeafe 100%) !important;
        color: #1e40af !important;
        font-weight: 700 !important;
        border-left: 3px solid #3b82f6 !important;
        border-right: 3px solid #3b82f6 !important;
    }
    
    /* Third Column (Quantum Algorithm) - BLUE Background (skip header) */
    .stDataFrame tbody tr:not(:first-child) td:nth-child(3),
    div[data-testid="stDataFrame"] tbody tr:not(:first-child) td:nth-child(3) {
        background: linear-gradient(135deg, #bfdbfe 0%, #dbeafe 100%) !important;
        color: #1e40af !important;
        font-weight: 700 !important;
        border-left: 3px solid #3b82f6 !important;
        border-right: 3px solid #3b82f6 !important;
    }
    
    /* Fourth Column (Ideal Value) (skip header) */
    .stDataFrame tbody tr:not(:first-child) td:nth-child(4),
    div[data-testid="stDataFrame"] tbody tr:not(:first-child) td:nth-child(4) {
        background: #f0fdf4 !important;
        color: #065f46 !important;
        font-weight: 500 !important;
    }
    
    /* Row Hover Effect (skip header row) */
    .stDataFrame tbody tr:not(:first-child):hover,
    div[data-testid="stDataFrame"] tbody tr:not(:first-child):hover {
        background: #f0f9ff !important;
        transform: scale(1.01);
        transition: all 0.2s ease;
    }
    
    .stDataFrame tbody tr:not(:first-child):hover td,
    div[data-testid="stDataFrame"] tbody tr:not(:first-child):hover td {
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Make table wider */
    .stDataFrame,
    div[data-testid="stDataFrame"] {
        width: 100% !important;
    }
    
    .stDataFrame table,
    div[data-testid="stDataFrame"] table {
        width: 100% !important;
        min-width: 100% !important;
    }
    
    
    /* ==================== EXPANDER ==================== */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe) !important;
        border-radius: 10px !important;
        color: #1e40af !important;
        font-weight: 600 !important;
        border: 2px solid #bfdbfe !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #dbeafe, #bfdbfe) !important;
        border-color: #3b82f6 !important;
    }
    
    /* ==================== TABS ==================== */
    /* ==================== FULL-WIDTH BLUE TABS ==================== */
    # ==================== TABS ====================
    # ==================== FULL-WIDTH BLUE TABS (FIXED FOR DYNAMIC WIDTH) ====================

    /* Tab Container - Full Width with proper spacing */
    .stTabs {
        width: 100% !important;
        margin-top: 0px !important;
        overflow: visible !important;
    }

    /* Tab List Container - Allow wrapping or scrolling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px !important;
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
        width: 100% !important;
        display: flex !important;
        flex-wrap: nowrap !important;
        border-bottom: none !important;
        overflow-x: auto !important;
        overflow-y: visible !important;
        padding: 0 !important;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    /* Individual Tab - Dynamic width with minimum size */
    .stTabs [data-baseweb="tab"] {
        flex: 1 1 auto !important; /* ✅ Flexible but with minimum content width */
        min-width: fit-content !important; /* ✅ Prevents text cutting */
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 1.2rem 2rem !important; /* ✅ Reduced padding for better fit */
        margin: 0 !important;
        transition: all 0.3s ease !important;
        text-align: center !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
        white-space: nowrap !important; /* ✅ Prevents text wrapping */
        height: auto !important;
        min-height: 60px !important;
    }

    /* Tab text sizing - ensure consistency */
    .stTabs [data-baseweb="tab"] button {
        font-size: 1.1rem !important;
        white-space: nowrap !important;
    }

    .stTabs button div {
        font-size: 1.1rem !important;
        white-space: nowrap !important;
    }

    .stTabs [data-baseweb="tab"] span {
        font-size: 1.1rem !important;
        white-space: nowrap !important;
    }

    /* Remove border from last tab */
    .stTabs [data-baseweb="tab"]:last-child {
        border-right: none !important;
    }

    /* Tab Hover Effect */
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
    }

    /* Active/Selected Tab - Lighter Blue */
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.25) !important;
        color: white !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.5) !important;
        border-bottom: 4px solid #fbbf24 !important; /* Gold bottom border for active tab */
    }

    /* Tab Panel Content Area */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 2rem !important;
    }

    /* Tab Text/Icon Styling */
    .stTabs button div {
        color: white !important;
    }

    .stTabs [aria-selected="true"] button div {
        color: white !important;
    }

    /* Optional: Add top rounded corners */
    .stTabs [data-baseweb="tab"]:first-child {
        border-radius: 12px 0 0 0 !important;
    }

    .stTabs [data-baseweb="tab"]:last-child {
        border-radius: 0 12px 0 0 !important;
    }

    /* Responsive handling for smaller screens */
    @media (max-width: 1200px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 1rem !important;
            padding: 1rem 1.5rem !important;
        }
        
        .stTabs [data-baseweb="tab"] button,
        .stTabs button div,
        .stTabs [data-baseweb="tab"] span {
            font-size: 1rem !important;
        }
    }

    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: scroll !important;
            -webkit-overflow-scrolling: touch !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 0.9rem !important;
            padding: 0.8rem 1.2rem !important;
            min-height: 50px !important;
        }
        
        .stTabs [data-baseweb="tab"] button,
        .stTabs button div,
        .stTabs [data-baseweb="tab"] span {
            font-size: 0.9rem !important;
        }
    }

    
    
    /* ==================== SCROLLBAR ==================== */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #e0f2fe;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #3b82f6, #2563eb);
        border-radius: 10px;
        border: 2px solid #e0f2fe;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #2563eb, #1e40af);
    }
    
    /* ==================== CHARTS & PLOTS ==================== */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.1);
    }
    
    /* ==================== CARDS ==================== */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.1);
        border: 2px solid #e0f2fe;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(30, 64, 175, 0.2);
        border-color: #3b82f6;
    }
    
    /* ==================== MOBILE RESPONSIVE ==================== */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        .subtitle {
            font-size: 1rem;
        }
        .icon-group i {
            font-size: 2.5rem;
        }
        .header-content {
            padding: 2rem 1.5rem;
        }
        .logo-row {
            flex-direction: column;
            gap: 15px;
        }
    }
    
    /* ==================== HIDE STREAMLIT BRANDING ==================== */
    [data-testid="stToolbar"] {
        display: none;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    header {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
    
    .main .block-container {
        padding-top: 1rem;
        max-width: 1400px;
    }

</style>
""", unsafe_allow_html=True)

def create_section_header(icon, title):
    """Create a styled section header with icon"""
    st.markdown(f"""
    <div class="section-header">
        <h2><i class="fas fa-{icon}"></i>{title}</h2>
    </div>
    """, unsafe_allow_html=True)


def create_info_box(text, icon="info-circle"):
    """Create an info box with icon"""
    st.markdown(f"""
    <div class="info-box">
        <i class="fas fa-{icon}"></i>
        <span>{text}</span>
    </div>
    """, unsafe_allow_html=True)


def create_metric_card(icon, label, value, delta=None):
    """Create a custom metric card with icon"""
    delta_html = ""
    if delta:
        delta_color = "#10b981" if delta > 0 else "#ef4444"
        delta_symbol = "↑" if delta > 0 else "↓"
        delta_html = f'<div style="color: {delta_color}; font-weight: 600; font-size: 0.9rem; margin-top: 0.5rem;">{delta_symbol} {abs(delta)}</div>'
    
    st.markdown(f"""
    <div class="card" style="text-align: center;">
        <i class="fas fa-{icon}" style="font-size: 2.5rem; color: #3b82f6; margin-bottom: 0.8rem;"></i>
        <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; 
                    text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.5px;">{label}</div>
        <div style="color: #1e40af; font-size: 2.2rem; font-weight: 800;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)