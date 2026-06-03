import streamlit as st

def show_splash_screen():
    """Display the enhanced landing page for a few seconds"""
    
    # CSS to make fullscreen and remove scrollbars
    st.markdown("""
    <style>
        /* Remove all padding and margins */
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        .main {
            padding: 0 !important;
            overflow: hidden !important;
        }
        
        /* Hide scrollbars */
        body, html {
            overflow: hidden !important;
            margin: 0;
            padding: 0;
            height: 100vh;
        }
    </style>
    """, unsafe_allow_html=True)
    
    landing_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            html, body {
                height: 100vh;
                width: 100vw;
                overflow: hidden;
            }

            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #1e40af 100%);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                color: white;
                position: relative;
            }

            .grid-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: 
                    linear-gradient(rgba(59, 130, 246, 0.1) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(59, 130, 246, 0.1) 1px, transparent 1px);
                background-size: 50px 50px;
                animation: gridMove 20s linear infinite;
                pointer-events: none;
                z-index: 1;
            }

            @keyframes gridMove {
                0% { transform: translate(0, 0); }
                100% { transform: translate(50px, 50px); }
            }

            .container {
                text-align: center;
                max-width: min(1200px, 90vw);
                width: 90vw;
                max-height: 90vh;
                z-index: 10;
                position: relative;
                display: flex;
                flex-direction: column;
                justify-content: center;
                padding: 2vh 3vw;
                gap: 2vh;
            }

            .particles {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 2;
            }

            .particle {
                position: absolute;
                background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 70%);
                border-radius: 50%;
                animation: particleFloat 15s infinite linear;
            }

            .particle:nth-child(1) { left: 10%; animation-delay: 0s; width: 4px; height: 4px; }
            .particle:nth-child(2) { left: 20%; animation-delay: 2s; width: 8px; height: 8px; }
            .particle:nth-child(3) { left: 30%; animation-delay: 4s; width: 5px; height: 5px; }
            .particle:nth-child(4) { left: 40%; animation-delay: 6s; width: 7px; height: 7px; }
            .particle:nth-child(5) { left: 50%; animation-delay: 8s; width: 6px; height: 6px; }
            .particle:nth-child(6) { left: 60%; animation-delay: 10s; width: 4px; height: 4px; }
            .particle:nth-child(7) { left: 70%; animation-delay: 12s; width: 8px; height: 8px; }
            .particle:nth-child(8) { left: 80%; animation-delay: 14s; width: 5px; height: 5px; }

            .hero {
                margin-bottom: 1.5vh;
            }

            .weather-icon {
                font-size: clamp(2.5rem, 7vh, 5rem);
                margin-bottom: 1vh;
                animation: float 3s ease-in-out infinite;
                filter: drop-shadow(0 10px 30px rgba(0,0,0,0.3));
                display: inline-block;
            }

            .main-title {
                font-size: clamp(1.8rem, 5.5vh, 4rem);
                font-weight: 900;
                margin-bottom: 0.8vh;
                background: linear-gradient(135deg, #fff 0%, #bfdbfe 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: -2px;
                line-height: 1.1;
            }

            .subtitle {
                font-size: clamp(0.85rem, 2vh, 1.3rem);
                opacity: 0.9;
                margin-bottom: 0.5vh;
                font-weight: 300;
            }

            .tagline {
                font-size: clamp(0.75rem, 1.4vh, 0.95rem);
                opacity: 0.7;
                margin-bottom: 1.5vh;
                font-style: italic;
            }

            .features {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 2vw;
                margin-bottom: 2vh;
                max-width: 900px;
                margin-left: auto;
                margin-right: auto;
            }

            .feature-card {
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(10px);
                padding: clamp(12px, 2vh, 20px) clamp(10px, 1.5vw, 16px);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.15);
                transition: all 0.3s ease;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }

            .feature-card:hover {
                transform: translateY(-5px);
                background: rgba(255, 255, 255, 0.12);
                box-shadow: 0 12px 48px rgba(0, 0, 0, 0.2);
            }

            .feature-icon {
                font-size: clamp(1.5rem, 3.5vh, 2.5rem);
                margin-bottom: 0.5vh;
            }

            .feature-title {
                font-size: clamp(0.85rem, 1.8vh, 1.2rem);
                font-weight: 600;
                margin-bottom: 0.3vh;
            }

            .feature-desc {
                font-size: clamp(0.7rem, 1.4vh, 0.95rem);
                opacity: 0.8;
                line-height: 1.4;
            }

            .cta-section {
                background: rgba(255, 255, 255, 0.12);
                backdrop-filter: blur(20px);
                border-radius: 28px;
                padding: clamp(16px, 3vh, 30px) clamp(20px, 3vw, 40px);
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .cta-title {
                font-size: clamp(1.1rem, 2.8vh, 2rem);
                font-weight: 700;
                margin-bottom: 1vh;
                color: white;
            }

            .cta-description {
                font-size: clamp(0.8rem, 1.7vh, 1.1rem);
                opacity: 0.9;
                margin-bottom: 1.8vh;
                line-height: 1.5;
            }

            .button-placeholder {
                height: clamp(50px, 8vh, 70px);
                margin-bottom: 0.8vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: rgba(255, 255, 255, 0.8);
                font-size: clamp(0.9rem, 1.8vh, 1.2rem);
                font-weight: 500;
                animation: fadeInOut 2s ease-in-out infinite;
            }

            @keyframes fadeInOut {
                0%, 100% { opacity: 0.5; }
                50% { opacity: 1; }
            }

            .cdac-text {
                margin-top: 1vh;
                font-size: clamp(0.7rem, 1.4vh, 0.95rem);
                opacity: 0.6;
                font-weight: 300;
            }

            .quantum-badge {
                position: fixed;
                top: 2vh;
                right: 2vw;
                background: rgba(168, 85, 247, 0.2);
                border: 1px solid rgba(168, 85, 247, 0.4);
                padding: 0.5vh 1.5vw;
                border-radius: 50px;
                font-size: clamp(0.65rem, 1.3vh, 0.85rem);
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                animation: pulse 2s ease-in-out infinite;
                z-index: 100;
            }

            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); }
                50% { transform: translateY(-20px) rotate(5deg); }
            }

            @keyframes particleFloat {
                0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
            }

            @keyframes pulse {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.8; transform: scale(1.05); }
            }

            @media (max-width: 1024px) {
                .features {
                    grid-template-columns: repeat(3, 1fr);
                }
            }

            @media (max-width: 768px) {
                .features {
                    grid-template-columns: repeat(1, 1fr);
                    gap: 2vh;
                    max-width: 400px;
                }
                .quantum-badge {
                    font-size: clamp(0.6rem, 1.1vh, 0.75rem);
                    padding: 0.4vh 1.2vw;
                }
            }

            @media (max-height: 700px) {
                .hero {
                    margin-bottom: 1vh;
                }
                .features {
                    margin-bottom: 1vh;
                }
            }
        </style>
    </head>
    <body>
        <div class="grid-overlay"></div>
        
        <div class="particles">
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
        </div>

        <div class="quantum-badge">🔬 Powered by Quantum Machine Learning</div>

        <div class="container">
            <div class="hero">
                <div class="weather-icon">⛅</div>
                <h1 class="main-title">Weather Prediction</h1>
                <p class="subtitle">QML & AI - Powered Climate Intelligence Platform</p>
                <p class="tagline">Harnessing quantum computing for next-generation meteorology</p>
            </div>

            <div class="features">
                <div class="feature-card">
                    <div class="feature-icon">🌡️</div>
                    <div class="feature-title">Temperature Forecasting</div>
                    <div class="feature-desc">Advanced quantum algorithms for precise predictions</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🌧️</div>
                    <div class="feature-title">Precipitation Tracking</div>
                    <div class="feature-desc">Quantum-enhanced rainfall predictions</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <div class="feature-title">Model Comparison</div>
                    <div class="feature-desc">Compare quantum vs classical ML</div>
                </div>
            </div>

            <div class="cta-section">
                <h2 class="cta-title">Ready to Explore Quantum Weather Forecasting?</h2>
                <p class="cta-description">Compare quantum and classical models, analyze predictions, and witness the future of meteorology powered by cutting-edge AI</p>
                <div class="button-placeholder">Loading Dashboard...</div>
                <p class="cdac-text">CDAC - Centre for Development of Advanced Computing</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Display the HTML (non-interactive background)
    st.components.v1.html(landing_html, height=1000, scrolling=False)