import streamlit as st

def render_sidebar():
    st.sidebar.markdown("### 🎙️ AI Meeting Assistant")
    st.sidebar.divider()
    
    pages = [
        ("🏠", "Home"),
        ("⚙️", "Processing"),
        ("📄", "Meeting Record"),
        ("📑", "Transcripts"),
        ("✦", "AI Highlights"),
        ("⬇️", "Downloads")
    ]
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
        
    for icon, label in pages:
        is_active = st.session_state.current_page == label
        button_type = "primary" if is_active else "secondary"
        if st.sidebar.button(f"{icon} {label}", key=f"nav_{label}", use_container_width=True, type=button_type):
            st.session_state.current_page = label
            st.rerun()
            
    st.sidebar.divider()
    
    # Render audio player in sidebar if there is results
    if "uploaded_file" in st.session_state and st.session_state.uploaded_file is not None:
        st.sidebar.markdown("**🔊 Meeting Audio**")
        st.sidebar.audio(st.session_state.uploaded_file)
        
    if "pipeline_results" in st.session_state and st.session_state.pipeline_results is not None:
        results = st.session_state.pipeline_results
        if "metrics" in results:
            st.sidebar.divider()
            st.sidebar.markdown("**📊 Performance Metrics**")
            m = results["metrics"]
            
            st.sidebar.metric("Word Count", m["word_count"])
            st.sidebar.metric("Total Time", f"{m['total']:.1f}s")
