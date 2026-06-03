"""
Home page content component - Clean theme matching screenshot
Contains all the informational content for the home tab
"""
import streamlit as st

def render_quantum_ml_intro():
    """Render the Quantum Machine Learning introduction section"""
    st.markdown("""
    <div style="background:#3b82f6 ;
                padding: 15px;
                border-radius: 8px;
                margin-top: 5px;
                margin-bottom: 20px;
                ">
        <h2 style="color: white; text-align: center; margin: 0 0 16px 0; font-size: 1.5rem; font-weight: 600;">
            🌦️ Quantum Machine Learning for Weather Prediction
        </h2>
        <p style="color: white; font-size: 17px; line-height: 1.7; text-align: center; margin-bottom: 16px;">
            A New Era of Forecasting
        </p>
    </div>
    <div style="background: #f8fafc;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 24px;
                border-left: 4px solid #3b82f6;">
        <p style="color: #000000; font-size: 16px; line-height: 1.8; margin: 0;">
            Weather prediction is entering a new phase. Beyond traditional physics‑based models and classical AI, 
            Quantum Machine Learning (QML) is emerging as a powerful approach. By harnessing quantum 
            principles such as superposition and entanglement, QML models can represent 
            complex patterns in climate data more efficiently. While still experimental, these models show promise for 
            achieving quantum advantage on real hardware as devices mature towards the NISQ era and Fault tolerance.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_quantum_models_section():
    """Render the quantum models overview section"""
    st.markdown("""
    <div style="background: #3b82f6;
                padding: 16px;
                border-radius: 8px;
                margin-bottom: 24px;">
        <h2 style="color: white; margin: 0; font-size: 1.5rem; text-align: center; font-weight: 600;">
            ⚛️ Quantum Models at a Glance
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create 2 columns for compact layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Quantum Neural Networks
        st.markdown("""
        <div style="background: #f8fafc;
                    padding: 18px;
                    border-radius: 8px;
                    margin-bottom: 16px;
                    border-left: 4px solid #3b82f6;
                    height: 300px;
                    display: flex;
                    flex-direction: column;">
            <h3 style="color: #1e293b; margin: 0 0 12px 0; font-size: 22px; font-weight: 600;">⚛️ Quantum Neural Networks (QNN)</h3>
            <p style="color: #000000; font-size: 17px; line-height: 1.6; margin-bottom: 12px;">
                Quantum versions of neural networks using entangling layers to capture intricate data relationships.
            </p>
            <div style="background: #f0f9ff; padding: 12px; border-radius: 6px;">
                <p style="color: #000000; margin: 0 0 8px 0; font-weight: 600; font-size: 16px;">💪 Strength:</p>
                <p style="color: #000000; margin: 0 0 12px 0; font-size: 16px;">Flexible and expressive, adaptable to both regression and classification</p>
                <p style="color: #000000; margin: 0 0 8px 0; font-weight: 600; font-size: 16px;">🔬 Variants:</p>
                <p style="color: #000000; margin: 0; font-size: 16px;"><strong>Ising Layers:</strong> Balance expressivity with manageable depth<br>
                <strong>Strong Entangling:</strong> Create richer correlations</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # QLSTM
        st.markdown("""
        <div style="background: #f8fafc;
                    padding: 18px;
                    border-radius: 8px;
                    margin-bottom: 16px;
                    border-left: 4px solid #3b82f6;
                    height: 300px;
                    display: flex;
                    flex-direction: column;">
            <h3 style="color: #1e293b; margin: 0 0 12px 0; font-size: 22px; font-weight: 600;">⚛️ Quantum LSTM (QLSTM)</h3>
            <p style="color: #000000; font-size: 17px; line-height: 1.6; margin-bottom: 12px;">
                Quantum‑enhanced LSTMs integrating quantum circuits into memory cells.
            </p>
            <div style="background: #f0f9ff; padding: 12px; border-radius: 6px;">
                <p style="color: #000000; margin: 0 0 8px 0; font-weight: 600; font-size: 16px;">💪 Strength:</p>
                <p style="color: #000000; margin: 0 0 12px 0; font-size: 16px;">Capture long‑term temporal dependencies</p>
                <p style="color: #000000; margin: 0 0 8px 0; font-weight: 600; font-size: 16px;">✨ Advantage:</p>
                <p style="color: #000000; margin: 0; font-size: 16px;">Comparable to classical LSTMs with fewer parameters</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # QSVM
        st.markdown("""
        <div style="background: #f8fafc;
                    padding: 18px;
                    border-radius: 8px;
                    border-left: 4px solid #3b82f6;
                    height: 300px;
                    display: flex;
                    flex-direction: column;">
            <h3 style="color: #1e293b; margin: 0 0 12px 0; font-size: 22px; font-weight: 600;">⚛️ Quantum SVM (QSVM)</h3>
            <p style="color: #000000; font-size: 17px; line-height: 1.6; margin-bottom: 12px;">
                Quantum extensions of SVMs embedding data into high‑dimensional quantum spaces.
            </p>
            <div style="background: #f0f9ff; padding: 12px; border-radius: 6px;">
                <p style="color: #000000; margin: 0 0 8px 0; font-weight: 600; font-size: 16px;">💪 Strength:</p>
                <p style="color: #000000; margin: 0 0 12px 0; font-size: 16px;">Non-Gradient and Quantum Kernel based core</p>
                <p style="color: #000000; margin: 0 0 8px 0; font-weight: 600; font-size: 16px;">✨ Advantage:</p>
                <p style="color: #000000; margin: 0; font-size: 16px;">Quantum kernels enable richer decision boundaries</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # QGRU
        st.markdown("""
        <div style="background: #f8fafc;
                    padding: 18px;
                    border-radius: 8px;
                    margin-bottom: 16px;
                    border-left: 4px solid #3b82f6;
                    height: 300px;
                    display: flex;
                    flex-direction: column;">
            <h3 style="color: #1e293b; margin: 0 0 12px 0; font-size: 22px; font-weight: 600;">⚛️ Quantum GRU (QGRU)</h3>
            <p style="color: #000000; font-size: 17px; line-height: 1.6; margin-bottom: 12px;">
                Quantum adaptations of GRUs designed for sequential data.
            </p>
            <div style="background: #f0f9ff; padding: 12px; border-radius: 6px;">
                <p style="color: #000000; margin: 0 0 8px 0; font-weight: 600; font-size: 16px;">💪 Strength:</p>
                <p style="color: #000000; margin: 0 0 12px 0; font-size: 16px;">Efficient at modeling short‑term dependencies in time series</p>
                <p style="color: #000000; margin: 0 0 8px 0; font-weight: 600; font-size: 16px;">✨ Advantage:</p>
                <p style="color: #000000; margin: 0; font-size: 16px;">Comparative accuracy with fewer trainable parameters</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # VQC
        st.markdown("""
        <div style="background: #f8fafc;
                    padding: 18px;
                    border-radius: 8px;
                    margin-bottom: 16px;
                    border-left: 4px solid #3b82f6;
                    height: 300px;
                    display: flex;
                    flex-direction: column;">
            <h3 style="color: #1e293b; margin: 0 0 12px 0; font-size: 22px; font-weight: 600;">⚛️ Variational Quantum Circuits (VQC)</h3>
            <p style="color: #000000; font-size: 17px; line-height: 1.6; margin-bottom: 12px;">
                Hybrid models where quantum circuits are optimized by classical algorithms.
            </p>
            <div style="background: #f0f9ff; padding: 12px; border-radius: 6px;">
                <p style="color: #000000; margin: 0 0 8px 0; font-weight: 600; font-size: 16px;">💪 Strength:</p>
                <p style="color: #000000; margin: 0 0 12px 0; font-size: 16px;">Modular and versatile for regression tasks</p>
                <p style="color: #000000; margin: 0 0 8px 0; font-weight: 600; font-size: 16px;">✨ Advantage:</p>
                <p style="color: #000000; margin: 0; font-size: 16px;">Leverage quantum parallelism for flexible learning</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Hybrid QNN
        st.markdown("""
        <div style="background: #f8fafc;
                    padding: 18px;
                    border-radius: 8px;
                    border-left: 4px solid #3b82f6;
                    height: 300px;
                    display: flex;
                    flex-direction: column;">
            <h3 style="color: #1e293b; margin: 0 0 12px 0; font-size: 22px; font-weight: 600;">⚛️ Hybrid QNN</h3>
            <p style="color: #000000; font-size: 17px; line-height: 1.6; margin-bottom: 12px;">
                Hybrid models combining classical and quantum layers for optimal performance.
            </p>
            <div style="background:  #f0f9ff; padding: 12px; border-radius: 6px;">
                <p style="color: #000000; margin: 0 0 8px 0; font-weight: 600; font-size: 16px;">💪 Strength:</p>
                <p style="color: #000000; margin: 0 0 12px 0; font-size: 16px;">Combines classical scalability with quantum learning power</p>
                <p style="color: #000000; margin: 0 0 8px 0; font-weight: 600; font-size: 16px;">✨ Advantage:</p>
                <p style="color: #000000; margin: 0; font-size: 16px;">Efficient parameter usage with better generalization</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_key_differences():
    """Render key differences and comparisons"""
    st.markdown("""
    <div style="background: #3b82f6;
                padding: 16px;
                border-radius: 8px;
                margin: 32px 0 24px 0;">
        <h2 style="color: white; margin: 0; font-size: 1.5rem; text-align: center; font-weight: 600;">
            🔍 Key Differences Within Quantum Models
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #f8fafc;
                    padding: 18px;
                    border-radius: 8px;
                    border-left: 4px solid #3b82f6;">
            <h4 style="color:#1e293b ; margin: 0 0 12px 0; text-align: center; font-size:18px; font-weight: 600;">⚛️ QNN vs. QSVM</h4>
            <p style="color:#000000 ; font-size: 16px; margin: 0; line-height: 1.6;">
                <strong>QNN:</strong> Flexible and adaptive<br>
                <strong>QSVM:</strong> Structured and kernel‑driven
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f8fafc;
                    padding: 18px;
                    border-radius: 8px;
                    border-left: 4px solid #3b82f6;">
            <h4 style="color: #1e293b; margin: 0 0 12px 0; text-align: center; font-size: 18px; font-weight: 600;">⚛️ QGRU vs. QLSTM</h4>
            <p style="color: #000000; font-size: 16px; margin: 0; line-height: 1.6;">
                <strong>QGRU:</strong> Excel at short‑term memory<br>
                <strong>QLSTM:</strong> Handle long‑term dependencies
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #f8fafc;
                    padding: 18px;
                    border-radius: 8px;
                    border-left: 4px solid #3b82f6;">
            <h4 style="color: #1e293b; margin: 0 0 12px 0; text-align: center; font-size: 18px; font-weight: 600;">⚛️ VQC</h4>
            <p style="color: #000000; font-size: 16px; margin: 0; line-height: 1.6;">
                Modular building blocks bridging classical and quantum approaches
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_quantum_vs_classical():
    """Render quantum vs classical comparison"""
    st.markdown("""
    <div style="background: #3b82f6;
                padding: 16px;
                border-radius: 8px;
                margin: 32px 0 24px 0;">
        <h2 style="color: white; margin: 0; font-size: 1.5rem; text-align: center; font-weight: 600;">
            ⚖️ Quantum vs. Classical Approaches
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    comparison_data = [
        {
            "title": "🎯 Representation Power",
            "content": "Quantum models can represent richer feature spaces, potentially uncovering patterns that classical models miss."
        },
        {
            "title": "⚡ Efficiency",
            "content": "Classical models remain stable and fast. Quantum models demonstrate parameter efficiency and may achieve quantum advantage as NISQ-Era Quantum hardware is made available."
        },
        {
            "title": "📈 Maturity",
            "content": "Classical AI is production‑ready. Quantum ML is early-stage, but hardware accessibility may close the gap."
        }
    ]
    
    for item in comparison_data:
        st.markdown(f"""
        <div style="background: #f8fafc;
                    padding: 18px;
                    border-radius: 8px;
                    margin-bottom: 16px;
                    border-left: 4px solid #3b82f6;">
            <h3 style="color: #1e293b; margin: 0 0 8px 0; font-size: 20px; font-weight: 600;">{item['title']}</h3>
            <p style="color: #000000; font-size: 16px; line-height: 1.6; margin: 0;">
                {item['content']}
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_hybrid_future():
    """Render the hybrid future section"""
    st.markdown("""
    <div style="background:#3b82f6 ;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
                margin-bottom: 20px;
                ">
        <h2 style="color: white; text-align: center; margin: 0 0 16px 0; font-size: 24px;; font-weight: 600;">
            🚀 The Hybrid Future
        </h2>
        <p style="color: white; font-size: 17px; line-height: 1.7; text-align: center; margin-bottom: 16px;">
            The most promising path lies in hybrid quantum‑classical systems:
        </p>
    </div>
    <div style="background: #f8fafc; padding: 16px; border-radius: 8px; border-left: 4px solid #3b82f6;">
            <p style="color: #000000; font-size: 16px; line-height: 1.8; margin: 0;">
                🖥️ <strong>Classical components</strong> ensure stability and scalability<br>
                ⚛️ <strong>Quantum circuits</strong> add depth and richer representations<br>
                🤝 <strong>Together</strong>, they create next‑generation forecasting as hardware improves
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_full_home_content():
    """Render all home page content sections"""
    render_quantum_ml_intro()
    render_quantum_models_section()
    render_key_differences()
    render_quantum_vs_classical()
    render_hybrid_future()