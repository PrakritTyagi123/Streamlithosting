import streamlit as st
from pathlib import Path
from PIL import Image
import io
import base64


def resize_image_to_standard(img_path, target_height=280):
    """Resize image to standard height while maintaining aspect ratio"""
    try:
        img = Image.open(img_path)
        # Calculate new width to maintain aspect ratio
        aspect_ratio = img.width / img.height
        new_width = int(target_height * aspect_ratio)
        # Resize image
        img_resized = img.resize((new_width, target_height), Image.Resampling.LANCZOS)
        return img_resized
    except Exception as e:
        st.error(f"Error resizing image: {e}")
        return None

def image_to_base64(img):
    """Convert PIL Image to base64 for HTML embedding"""
    buffered = io.BytesIO()
    # Force RGB mode for consistent output
    if img.mode in ('RGBA','LA','P'):
        img = img.convert('RGB')
    img.save(buffered, format="JPEG",quality = 85,optimize=True )
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def render_final_home_content():
    """Render the new enhanced home page"""
    BASE_DIR = Path(__file__).parent.parent
    ASSETS_DIR = BASE_DIR / "assests"

    # Verify the path exists
    if not ASSETS_DIR.exists():
        st.error(f"❌ Assets directory not found at: {ASSETS_DIR}")
        st.info("Please check your folder structure")
        return

    # -------------------------------------------------
    # CUSTOM CSS - COMPLETELY FIXED
    # -------------------------------------------------
    st.markdown("""
    <style>
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 1rem;
    }
    
    /* Animations */
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-120px); }
        to { opacity: 1; transform: translateX(0); }
    }

    .animated {
        animation: slideIn 0.8s cubic-bezier(0.16,1,0.3,1) forwards;
    }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 0.6rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .hero h1 {
        font-size: 2rem !important;
        font-weight: 700;
        margin: 0 0 0.2rem 0;
    }
    
    .hero p {
        font-size: 1.05rem !important;
        margin: 0;
        opacity: 0.95;
    }

    /* Content card */
    .content-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.8rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .content-card h2 {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0 0 0.8rem 0;
    }
    
    .content-card p {
        font-size: 1.05rem;
        color: #000000;
        line-height: 1.6;
        margin-bottom: 0.8rem;
    }

    /* Stats cards */
    .stat-card {
        background: white;
        padding: 0.9rem 0.6rem;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card:hover {
        transform: translateY(-6px);
        border-color: #4c7fe0;
        box-shadow: 0 6px 16px rgba(76, 127, 224, 0.15);
    }
    
    .stat-emoji {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
        transition: transform 0.3s;
    }
    
    .stat-card:hover .stat-emoji {
        transform: scale(1.08);
    }
    
    .stat-title {
        color: #0f172a;
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .stat-text {
        color: #64748b;
        font-size: 0.8rem;
        margin-bottom: 0.3rem;
    }
    
    .stat-hover-content {
        max-height: 0;
        opacity: 0;
        overflow: hidden;
        transition: max-height 0.4s ease, opacity 0.4s ease;
        color: #475569;
        font-size: 0.9rem;
        line-height: 1.4;
        padding: 0 0.4rem;
    }
    
    .stat-card:hover .stat-hover-content {
        max-height: 150px;
        opacity: 1;
        margin-top: 0.6rem;
    }

    /* Section header */
    .section-header {
        background: linear-gradient(90deg, #4c7fe0 0%, #5b8def 100%);
        padding: 0.7rem 1.2rem;
        border-radius: 0.6rem;
        text-align: center;
        margin: 1rem 0 0.8rem 0;
        color: white;
        box-shadow: 0 3px 10px rgba(76, 127, 224, 0.3);
    }
    
    .section-header h2 {
        font-size: 1.7rem !important;
        font-weight: 700;
        margin: 0 0 0.2rem 0;
    }
    
    .section-header p {
        font-size: 1.05rem !important;
        margin: 0;
        opacity: 0.95;
    }

    /* Section title */
    .section-title {
        margin: 1.5rem 0 0.8rem 0;
        font-size: 1.3rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #0f172a;
    }

    /* Advantage box */
    .advantage-box {
        background: #eff6ff;
        padding: 0.7rem 0.9rem;
        border-radius: 6px;
        border-left: 3px solid #4c7fe0;
        margin-top: 0.8rem;
    }
    
    .advantage-box strong {
        color: #1e40af;
        font-size: 0.9rem;
    }

    /* Info box */
    .info-box {
        background: #eff6ff;
        padding: 0.8rem;
        border-radius: 6px;
        border-left: 3px solid #4c7fe0;
        margin: 0.8rem 0;
    }
    
    /* ✅ CRITICAL FIX: Equal height columns */
    div[data-testid="column"] {
        height: 100%;
    }
    
    /* ✅ Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        background-color: #f8fafc !important;
        border-radius: 6px !important;
    }
    
    details[open] summary {
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    /* ===== ALGORITHM CARD FIXES ===== */
    .algo-card {
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
        background: white;
        margin-bottom: 1.5rem;
        height: 100%;
    }
    
    .algo-header {
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        color: white;
        padding: 1rem;
    }
    
    .algo-header-title {
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
    
    .algo-header-desc {
        font-size: 1.05rem;
        opacity: 0.95;
    }
    
    /* CRITICAL: Fixed height image container with responsive scaling */
    .algo-img-wrapper {
        width: 100%;
        height: 280px;
        background: #f8fafc;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        position: relative;
    }
    
    .algo-img-wrapper img {
        max-width: 100%;
        max-height: 100%;
        width: auto;
        height: auto;
        object-fit: contain;
        display: block;
    }
    
    /* Responsive scaling for zoom */
    @media (min-width: 1px) {
        .algo-img-wrapper {
            height: min(280px, 30vw);
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------
    # HERO SECTION
    # -------------------------------------------------
    st.markdown("""
    <div class="hero animated">
        <h1>⚛️ Quantum Models Explorer</h1>
        <p>Explore quantum machine learning architectures for weather intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------
    # CONTENT + IMAGE
    # -------------------------------------------------
    col_text, col_img = st.columns([2.5, 1])

    with col_text:
        st.markdown("""
        <div class="content-card animated">
            <h2>⚛️ Quantum Weather Intelligence</h2>
            <p style="margin-bottom: 0.8rem;">
                Weather prediction is entering a new phase. Beyond traditional physics-based models and classical AI, 
                <strong>Quantum Machine Learning (QML)</strong> is emerging as a powerful approach for advanced forecasting.
            </p>
            <p style="margin-bottom: 0.8rem;">
                By harnessing quantum principles such as <strong>superposition</strong> and <strong>entanglement</strong>, 
                QML models can represent complex patterns in climate data more efficiently than classical approaches.
            </p>
            <p style="margin-bottom: 1rem;">
                While still experimental, these models show promise for achieving quantum advantage on real hardware 
                as devices mature towards the NISQ era and fault tolerance.
            </p>
            <div class="advantage-box">
                <strong>🔬 Quantum Advantage:</strong> 
                Exponentially richer feature spaces enable modeling of intricate, non-linear climate relationships that classical models cannot capture efficiently.
            </div>
            <div class="advantage-box" style="margin-top: 0.6rem; border-left-color: #10b981;">
                <strong>⚡ Key Benefits:</strong> 
                Fewer parameters, faster convergence, and the ability to process high-dimensional weather data with quantum parallelism.
            </div>
        </div>
        """, unsafe_allow_html=True)

        

    with col_img:
        # Use same base64 technique as algorithm images for proper resizing
        img_path = ASSETS_DIR / "quantum_weather_img.jpeg"
        if img_path.exists():
            try:
                 # Open and resize image
                img = Image.open(img_path)
                
                # Calculate dimensions for consistent display
                # Target width ~500px to fill the column properly
                target_width = 500
                aspect_ratio = img.height / img.width
                target_height = int(target_width * aspect_ratio)
                
                # Resize with high quality
                img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffered = io.BytesIO()
                if img_resized.mode in ('RGBA', 'LA', 'P'):
                    img_resized = img_resized.convert('RGB')
                img_resized.save(buffered, format="JPEG", quality=90, optimize=True)
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                # Embed with responsive HTML
                st.markdown(f"""
                    <div class="animated" style="
                        width: 100%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    ">
                        <img src="data:image/jpeg;base64,{img_base64}" 
                             alt="Quantum Weather Intelligence" 
                             style="
                                 width: 100%;
                                 height: auto;
                                 max-width: 100%;
                                 display: block;
                                 border-radius: 0.8rem;
                                 box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                             ">
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading image: {e}")
        else:
            st.warning(f"Image not found: {img_path.name}")

    # -------------------------------------------------
    # WHY QUANTUM ML SECTION
    # -------------------------------------------------
    st.markdown("""
        <div class="section-header">
            <h2>🚀 Why Quantum Machine Learning?</h2>
            <p>Unlocking unprecedented computational advantages</p>
        </div>
    """, unsafe_allow_html=True)

    # Stats cards
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

    with stats_col1:
        st.markdown("""
            <div class="stat-card">
                <div class="stat-emoji">🎯</div>
                <div class="stat-title">Higher Accuracy</div>
                <p class="stat-text">Complex pattern recognition</p>
                <div class="stat-hover-content">
                    Quantum algorithms can capture intricate correlations in weather data that classical models miss, 
                    leading to more precise forecasts especially for complex phenomena like extreme weather events.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with stats_col2:
        st.markdown("""
            <div class="stat-card">
                <div class="stat-emoji">⚡</div>
                <div class="stat-title">Fewer Parameters</div>
                <p class="stat-text">Efficient quantum learning</p>
                <div class="stat-hover-content">
                    Quantum models achieve comparable or better performance with exponentially fewer parameters than 
                    classical neural networks, making them more efficient and easier to train.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with stats_col3:
        st.markdown("""
            <div class="stat-card">
                <div class="stat-emoji">🔬</div>
                <div class="stat-title">Quantum Advantage</div>
                <p class="stat-text">NISQ-era ready systems</p>
                <div class="stat-hover-content">
                    Designed for current noisy intermediate-scale quantum (NISQ) devices, these algorithms are 
                    practical today and will scale as quantum hardware improves.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with stats_col4:
        st.markdown("""
            <div class="stat-card">
                <div class="stat-emoji">🤝</div>
                <div class="stat-title">Hybrid Power</div>
                <p class="stat-text">Classical + Quantum fusion</p>
                <div class="stat-hover-content">
                    Combines the best of both worlds—classical preprocessing and postprocessing with quantum 
                    computational cores for optimal real-world performance.
                </div>
            </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------
    # ALGORITHM DATA
    # -------------------------------------------------
    algorithms = [
        {
            'icon': '🧠',
            'title': 'Quantum Neural Networks (QNN)',
            'short_desc': 'Quantum versions of neural networks using entangling layers to capture intricate data relationships.',
            # 'color': 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)',
            'image': 'QNN_image_1.jpeg',
            'strength': 'Flexible and expressive, adaptable to both regression and classification tasks with deep quantum feature extraction.',
            'advantage': 'Rich feature representations through quantum entanglement enable modeling of complex, non-linear climate relationships.',
            'variants': [
                '**Ising Layers:** Balance expressivity with manageable circuit depth',
                '**Circuit Depth:** Typically 3-5 layers optimized for weather applications',
                '**Measurement:** Pauli-Z expectations for reliable output extraction'
            ],
            'applications': 'Temperature forecasting, precipitation prediction, extreme weather classification, and climate anomaly detection.'
        },
        {
            'icon': '🔄',
            'title': 'Quantum GRU (QGRU)',
            'short_desc': 'Quantum adaptations of GRUs designed for sequential weather data processing.',
            # 'color': 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)',
            'image': 'QGRU_image_1.jpeg',
            'strength': 'Efficient at modeling short-term dependencies in time series with reduced computational overhead.',
            'advantage': 'Comparative accuracy with significantly fewer trainable parameters than classical GRUs.',
            'variants': [
                '**Update Gates:** Quantum circuits control information flow between timesteps',
                '**Reset Gates:** Manage memory retention in quantum states effectively',
                '**Temporal Encoding:** Maps sequential weather data to quantum feature spaces'
            ],
            'applications': 'Short-term weather forecasting, hourly temperature trends, rapid weather changes, and nowcasting applications.'
        },
        {
            'icon': '🔗',
            'title': 'Quantum LSTM',
            'short_desc': 'Quantum-enhanced LSTMs integrating quantum circuits into memory cells for long-term patterns.',
            # 'color': 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)',
            'image': 'QLSTM_image_1.jpeg',
            'strength': 'Capture long-term temporal dependencies in climate data with quantum memory advantages.',
            'advantage': 'Comparable performance to classical LSTMs with dramatically reduced parameter count.',
            'variants': [
                '**Forget Gate:** Quantum circuits intelligently decide what information to discard',
                '**Input Gate:** Controls integration of new weather observations',
                '**Output Gate:** Manages quantum state exposure to final predictions'
            ],
            'applications': 'Seasonal forecasting, monthly climate predictions, long-range weather patterns, and El Niño/La Niña prediction.'
        },
        {
            'icon': '🎯',
            'title': 'Quantum SVM',
            'short_desc': 'Quantum SVMs embedding data into exponentially high-dimensional quantum feature spaces.',
            # 'color': 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)',
            'image': 'QSVM_img_1.jpeg',
            'strength': 'Excellent for classification tasks with clear decision boundaries in quantum feature space.',
            'advantage': 'Quantum kernel provides access to exponentially large feature spaces for pattern separation.',
            'variants': [
                '**Quantum Kernel:** Maps weather data to quantum Hilbert space',
                '**Feature Maps:** ZZFeatureMap and custom angle encodings for data embedding',
                '**Kernel Estimation:** Inner products computed efficiently via quantum circuits'
            ],
            'applications': 'Binary classification (rain/no rain), weather pattern categorization, storm detection, and anomaly identification.'
        },
        {
            'icon': '⚡',
            'title': 'Variational Quantum Circuits (VQC)',
            'short_desc': 'Hybrid quantum-classical models where parameterized circuits are optimized classically.',
            # 'color': 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)',
            'image': 'VQC_image_1.jpeg',
            'strength': 'Highly customizable architecture that can be tailored to specific weather prediction problems.',
            'advantage': 'Can exploit problem-specific structure efficiently with hardware-aware circuit designs.',
            'variants': [
                '**Ansatz Design:** Hardware-efficient or problem-inspired quantum circuit layouts',
                '**Optimization:** Gradient-based (parameter shift) or gradient-free methods',
                '**Entanglement:** CNOT chains and custom connectivity for qubit correlation'
            ],
            'applications': 'Custom weather models, multi-output regression, ensemble predictions, and domain-specific forecasting.'
        },
        {
            'icon': '🤝',
            'title': 'Hybrid QNN',
            'short_desc': 'Best of both worlds: classical preprocessing and postprocessing with quantum core.',
            # 'color': 'linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%)',
            'image': 'HQNN_image_1.jpeg',
            'strength': 'Leverages classical machine learning strengths while adding quantum computational advantages.',
            'advantage': 'More practical for near-term quantum devices (NISQ era) with realistic noise tolerance.',
            'variants': [
                '**Classical Preprocessing:** Feature engineering, normalization, and data augmentation',
                '**Quantum Core:** Variational circuits for complex pattern extraction',
                '**Classical Postprocessing:** Output refinement, calibration, and ensemble combination'
            ],
            'applications': 'Ensemble weather models, multi-modal data fusion, operational forecasting systems, and production deployments.'
        }
    ]

    # -------------------------------------------------
    # ALGORITHM SECTION - PROPERLY STRUCTURED
    # -------------------------------------------------
    st.markdown("""
        <h2 class="section-title">
            <span style="color: #ec4899;">🎯</span> Quantum Algorithms Collection
        </h2>
    """, unsafe_allow_html=True)

    # Process algorithms in rows of 3
    for i in range(0, len(algorithms), 2):
        cols = st.columns(2)
        
        for j in range(2):
            if i + j < len(algorithms):
                algo = algorithms[i + j]
                
                with cols[j]:
                    # Card container
                    st.markdown('<div class="algo-card">', unsafe_allow_html=True)
                   
                    # Header
                    st.markdown(f"""
                        <div class="algo-header">
                            <div class="algo-header-title">{algo['icon']} {algo['title']}</div>
                            <div class="algo-header-desc">{algo['short_desc']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    # Image using HTML with base64 encoding for FULL control
                    img_path = ASSETS_DIR / algo['image']
                    if img_path.exists():
                        # Resize image to standard height
                        img_resized = resize_image_to_standard(img_path, target_height=280)
                        if img_resized:
                            img_base64 = image_to_base64(img_resized)
                            st.markdown(f"""
                                <div class="algo-img-wrapper">
                                    <img src="{img_base64}" alt="{algo['title']}">
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                                <div class="algo-img-wrapper">
                                    <span style="color: #94a3b8;">Error loading image</span>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="algo-img-wrapper">
                                <span style="color: #94a3b8;">🖼️ Image not found: {algo['image']}</span>
                            </div>
                        """, unsafe_allow_html=True)

                    # Expander
                    with st.expander("🔍 View Details", expanded=False):
                        st.markdown("#### 💪 Strength")
                        st.info(algo['strength'])

                        st.markdown("#### ✨ Advantage")
                        st.success(algo['advantage'])

                        st.markdown("#### 🔧 Key Variants")
                        for variant in algo['variants']:
                            st.markdown(f"• {variant}")

                        st.markdown("#### 🎯 Applications")
                        st.markdown(f'<div class="info-box"><strong>{algo["applications"]}</strong></div>', unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)
                        