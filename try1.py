# ==================== TAB 2: TEMPERATURE PREDICTION ====================
with tab2:
    # ==================== OPTION 1: INLINE WITH TITLE (RECOMMENDED) ====================
    col_title, col_spacer, col_datasource = st.columns([2, 1, 2])

    with col_title:
        st.markdown('<h3>📊 Temperature Predictions Dashboard</h3>', unsafe_allow_html=True)

    with col_spacer:
        st.write("")  # Empty spacer
    
    with col_datasource:
        st.markdown("<div style='margin-top: 10px;'>", unsafe_allow_html=True)
        data_source = st.selectbox(
            "**📂 Data Source:**",
            options=["IMD", "NCMRWF"],
            key="temp_data_source",
            help="Select dataset for temperature predictions"
        )
    
    st.markdown("---")
    
    # ==================== 📸 SCREENSHOT HELPER (TEMPORARY - DELETE AFTER TAKING PHOTOS) ====================
    st.markdown("### 📸 All Dropdown Options for Screenshots")
    st.info("⚠️ This section is for documentation only. Delete this entire section after taking screenshots!")
    
    # IMD Section
    st.markdown("#### 📂 Data Source: **IMD**")
    col_imd1, col_imd2 = st.columns(2)
    
    with col_imd1:
        st.markdown("**🖥️ Classical Algorithm**")
        st.markdown('<div style="border: 2px solid #2563eb; border-radius: 8px; padding: 12px; background: white;">', unsafe_allow_html=True)
        for algo in CLASSICAL_ALGORITHMS.keys():
            st.markdown(f'<div style="padding: 8px; border-bottom: 1px solid #e5e7eb;">{algo}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_imd2:
        st.markdown("**⚛️ Quantum Algorithm**")
        st.markdown('<div style="border: 2px solid #2563eb; border-radius: 8px; padding: 12px; background: white;">', unsafe_allow_html=True)
        for algo in QUANTUM_ALGORITHMS.keys():
            st.markdown(f'<div style="padding: 8px; border-bottom: 1px solid #e5e7eb;">{algo}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # NCMRWF Section
    st.markdown("#### 📂 Data Source: **NCMRWF**")
    col_ncmr1, col_ncmr2 = st.columns(2)
    
    with col_ncmr1:
        st.markdown("**🖥️ Classical Algorithm**")
        st.markdown('<div style="border: 2px solid #2563eb; border-radius: 8px; padding: 12px; background: white;">', unsafe_allow_html=True)
        for algo in NCMRWF_CLASSICAL_ALGORITHMS.keys():
            st.markdown(f'<div style="padding: 8px; border-bottom: 1px solid #e5e7eb;">{algo}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_ncmr2:
        st.markdown("**⚛️ Quantum Algorithm**")
        st.markdown('<div style="border: 2px solid #2563eb; border-radius: 8px; padding: 12px; background: white;">', unsafe_allow_html=True)
        for algo in NCMRWF_QUANTUM_ALGORITHMS.keys():
            st.markdown(f'<div style="padding: 8px; border-bottom: 1px solid #e5e7eb;">{algo}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.error("🚨 REMOVE THIS ENTIRE SCREENSHOT SECTION AFTER TAKING YOUR PICTURES! 🚨")
    st.markdown("---")
    # ==================== END SCREENSHOT HELPER ====================
    
    # ✅ INITIALIZE ALGORITHM STORAGE FOR EACH DATA SOURCE
    if 'imd_selected_classical' not in st.session_state:
        st.session_state.imd_selected_classical = "Select Classical Algorithm"
    # ... rest of your code continues ...