import streamlit as st

def show_splash_screen():
    """Display landing page with fixed floating button - returns True when user wants to enter"""
    
    # CSS to make fullscreen
    st.markdown("""
    <style>
        /* Remove all padding and margins */
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        .main {
            padding: 0 !important;
        }
        
        /* Hide Streamlit's default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # The complete React landing page with FIXED FLOATING BUTTON
    landing_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body, html {
                margin: 0;
                padding: 0;
                height: 100vh;
                overflow-y: auto;
                overflow-x: hidden;
            }
            #root {
                min-height: 100vh;
            }
        </style>
    </head>
    <body>
        <div id="root"></div>
        
        <script type="text/babel">
            const { useState } = React;

            function WeatherLanding() {
                const [isHovered, setIsHovered] = useState(false);

                const handleEnter = () => {
                    // Send message to Streamlit parent
                    window.parent.postMessage({
                        type: 'streamlit:setComponentValue',
                        value: true
                    }, '*');
                };

                return (
                    <div className="relative min-h-screen overflow-x-hidden bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800">
                        {/* Animated Grid */}
                        <div className="absolute inset-0 opacity-30 pointer-events-none">
                            <div className="absolute inset-0 animate-[gridMove_20s_linear_infinite]"
                                style={{
                                    backgroundImage: 'linear-gradient(rgba(59, 130, 246, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(59, 130, 246, 0.1) 1px, transparent 1px)',
                                    backgroundSize: '50px 50px'
                                }}
                            />
                        </div>

                        {/* Particles */}
                        <div className="absolute inset-0 pointer-events-none overflow-hidden">
                            {[...Array(8)].map((_, i) => (
                                <div
                                    key={i}
                                    className="absolute rounded-full bg-white opacity-80 animate-[particleFloat_15s_linear_infinite]"
                                    style={{
                                        left: `${(i + 1) * 10}%`,
                                        width: `${4 + (i % 3) * 2}px`,
                                        height: `${4 + (i % 3) * 2}px`,
                                        animationDelay: `${i * 2}s`,
                                        filter: 'blur(1px)'
                                    }}
                                />
                            ))}
                        </div>

                        {/* Badge */}
                        <div className="fixed top-4 right-4 bg-purple-500/20 border border-purple-500/40 px-4 sm:px-6 py-2 rounded-full text-xs font-semibold uppercase tracking-wider animate-pulse z-40 text-white">
                            🔬 Powered by Quantum ML
                        </div>

                        {/* FIXED FLOATING BUTTON - ALWAYS VISIBLE IN BOTTOM RIGHT */}
                        <button
                            onClick={handleEnter}
                            onMouseEnter={() => setIsHovered(true)}
                            onMouseLeave={() => setIsHovered(false)}
                            className="fixed bottom-8 right-8 z-50 group"
                            style={{
                                width: isHovered ? '200px' : '70px',
                                height: '70px',
                                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
                            }}
                        >
                            <div className="relative w-full h-full">
                                {/* Glowing background effect */}
                                <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full blur-xl opacity-60 group-hover:opacity-100 transition-opacity duration-300"></div>
                                
                                {/* Main button */}
                                <div className="relative w-full h-full bg-gradient-to-r from-blue-500 to-blue-600 rounded-full shadow-2xl flex items-center justify-center overflow-hidden group-hover:from-blue-600 group-hover:to-purple-600 transition-all duration-300">
                                    {/* Arrow icon (always visible) */}
                                    <div 
                                        className="absolute flex items-center justify-center text-white text-2xl font-bold"
                                        style={{
                                            left: isHovered ? '15px' : '50%',
                                            transform: isHovered ? 'translateX(0)' : 'translateX(-50%)',
                                            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
                                        }}
                                    >
                                        →
                                    </div>
                                    
                                    {/* Text (appears on hover) */}
                                    <div 
                                        className="absolute text-white font-semibold text-sm whitespace-nowrap"
                                        style={{
                                            right: '15px',
                                            opacity: isHovered ? 1 : 0,
                                            transition: 'opacity 0.3s ease-in-out'
                                        }}
                                    >
                                        Enter App
                                    </div>
                                </div>
                                
                                {/* Ripple effect on click */}
                                <div className="absolute inset-0 rounded-full bg-white opacity-0 group-active:opacity-30 group-active:animate-ping transition-opacity"></div>
                            </div>
                        </button>

                        {/* Main Content */}
                        <div className="relative z-10 min-h-screen flex items-center justify-center p-4 sm:p-8 pb-32">
                            <div className="text-center max-w-6xl w-full space-y-6 sm:space-y-8 text-white">
                                
                                {/* Hero */}
                                <div className="space-y-3 sm:space-y-4 animate-[float_3s_ease-in-out_infinite]">
                                    <div className="text-5xl sm:text-7xl mb-3 sm:mb-4 filter drop-shadow-2xl">⛅</div>
                                    <h1 className="text-4xl sm:text-6xl md:text-7xl font-black bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent tracking-tight">
                                        Weather Prediction
                                    </h1>
                                    <p className="text-lg sm:text-xl md:text-2xl opacity-90 font-light px-4">
                                        QML & AI - Powered Climate Intelligence Platform
                                    </p>
                                    <p className="text-xs sm:text-sm md:text-base opacity-70 italic px-4">
                                        Harnessing quantum computing for next-generation meteorology
                                    </p>
                                </div>

                                {/* Features */}
                                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-6 max-w-4xl mx-auto py-4 sm:py-8 px-4">
                                    <div className="bg-white/10 backdrop-blur-lg p-4 sm:p-6 rounded-3xl border border-white/20 hover:bg-white/15 hover:transform hover:-translate-y-2 transition-all duration-300 shadow-2xl">
                                        <div className="text-4xl sm:text-5xl mb-3 sm:mb-4">🌡️</div>
                                        <h3 className="text-base sm:text-xl font-semibold mb-2">Temperature Forecasting</h3>
                                        <p className="text-xs sm:text-sm opacity-80">Advanced quantum algorithms for precise predictions</p>
                                    </div>
                                    
                                    <div className="bg-white/10 backdrop-blur-lg p-4 sm:p-6 rounded-3xl border border-white/20 hover:bg-white/15 hover:transform hover:-translate-y-2 transition-all duration-300 shadow-2xl">
                                        <div className="text-4xl sm:text-5xl mb-3 sm:mb-4">🌧️</div>
                                        <h3 className="text-base sm:text-xl font-semibold mb-2">Precipitation Tracking</h3>
                                        <p className="text-xs sm:text-sm opacity-80">Quantum-enhanced rainfall predictions</p>
                                    </div>
                                    
                                    <div className="bg-white/10 backdrop-blur-lg p-4 sm:p-6 rounded-3xl border border-white/20 hover:bg-white/15 hover:transform hover:-translate-y-2 transition-all duration-300 shadow-2xl">
                                        <div className="text-4xl sm:text-5xl mb-3 sm:mb-4">📊</div>
                                        <h3 className="text-base sm:text-xl font-semibold mb-2">Model Comparison</h3>
                                        <p className="text-xs sm:text-sm opacity-80">Compare quantum vs classical ML</p>
                                    </div>
                                </div>

                                {/* Info Box */}
                                <div className="bg-white/15 backdrop-blur-2xl rounded-3xl p-6 sm:p-10 border border-white/25 shadow-2xl max-w-4xl mx-auto">
                                    <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-3 sm:mb-4">
                                        Ready to Explore Quantum Weather Forecasting?
                                    </h2>
                                    <p className="text-sm sm:text-base md:text-lg opacity-90 mb-6 sm:mb-8 leading-relaxed px-4">
                                        Compare quantum and classical models, analyze predictions, and witness the future of meteorology powered by cutting-edge AI
                                    </p>
                                    
                                    <p className="text-xs sm:text-sm opacity-60 font-light">
                                        CDAC - Centre for Development of Advanced Computing
                                    </p>
                                    
                                    {/* Instruction for button */}
                                    <div className="mt-6 flex items-center justify-center gap-2 text-blue-200 text-sm animate-bounce">
                                        <span>Click the button</span>
                                        <span className="text-xl">→</span>
                                        <span>in the bottom right corner</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <style>{`
                            @keyframes gridMove {
                                0% { transform: translate(0, 0); }
                                100% { transform: translate(50px, 50px); }
                            }
                            
                            @keyframes particleFloat {
                                0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
                                10% { opacity: 1; }
                                90% { opacity: 1; }
                                100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
                            }
                            
                            @keyframes float {
                                0%, 100% { transform: translateY(0px) rotate(0deg); }
                                50% { transform: translateY(-20px) rotate(3deg); }
                            }
                        `}</style>
                    </div>
                );
            }

            ReactDOM.render(<WeatherLanding />, document.getElementById('root'));
        </script>
    </body>
    </html>
    """
    
    # Initialize session state
    if 'enter_app' not in st.session_state:
        st.session_state.enter_app = False
    
    # Display the React component and get result
    result = st.components.v1.html(landing_html, height=900, scrolling=True)
    
    # Check if button was clicked
    if result == True:
        st.session_state.enter_app = True
        st.rerun()
    
    return st.session_state.enter_app


# Example usage in your main app
if __name__ == "__main__":
    st.set_page_config(page_title="Weather Prediction", layout="wide", initial_sidebar_state="collapsed")
    
    # Show splash screen until user clicks enter
    if not show_splash_screen():
        st.stop()
    
    # Your main app starts here
    st.title("🌦️ Weather Prediction Dashboard")
    st.write("Welcome! You clicked the button on the landing page.")
    st.write("Your main weather prediction app would go here...")
    
    # Reset button to go back to landing page
    if st.button("← Back to Landing Page"):
        st.session_state.enter_app = False
        st.rerun()
