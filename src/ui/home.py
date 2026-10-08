import streamlit as st
from src.utils.audio import SUPPORTED_AUDIO_EXTENSIONS

def render_home():
    st.markdown("<h1>AI-Powered Meeting Assistant</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p class="subtitle">
        Upload a meeting recording to automatically generate a highly accurate transcript, 
        correct domain-specific terminology, and extract structured meeting minutes, decisions, and action items.
        </p>
    """, unsafe_allow_html=True)
    
    # Feature Row
    c1, c2, c3, c4, c5 = st.columns(5)
    features = [
        ("🎙️", "Accurate<br>Transcription"),
        ("📄", "Domain-Aware<br>Refinement"),
        ("☷", "Structured<br>Meeting Notes"),
        ("✓", "Decisions &<br>Action Items"),
        ("⬇️", "Export to Multiple<br>Formats")
    ]
    for col, (icon, text) in zip([c1, c2, c3, c4, c5], features):
        col.markdown(f"""
            <div class="feature-box">
                <div class="feature-icon">{icon}</div>
                <div style="font-size: 13px; font-weight: 500;">{text}</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
        # Upload Card
    st.markdown("### ☁️ Upload Meeting Audio")
    st.markdown("<p style='color: #94A3B8; font-size: 14px;'><strong>Note:</strong> Due to API constraints, files must be <strong>under 25 MB</strong>. For video files (.mp4), convert them to .mp3 to drastically reduce file size.</p>", unsafe_allow_html=True)
    
    allowed_extensions = [ext.strip('.') for ext in SUPPORTED_AUDIO_EXTENSIONS]
    
    uploaded_file = st.file_uploader(
        "Drag and drop your audio file here, or click to browse",
        type=allowed_extensions,
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        file_mb = uploaded_file.size / (1024 * 1024)
        st.session_state.uploaded_file = uploaded_file
        
        if file_mb > 25:
            st.error(f"⚠️ File is too large ({file_mb:.1f} MB). Please upload a file under 25 MB.")
        else:
            st.success(f"File loaded: {uploaded_file.name} ({file_mb:.1f} MB)")
            
            if st.button("🚀 Process Meeting Audio", type="primary", use_container_width=True):
                st.session_state.current_page = "Processing"
                st.session_state.start_processing = True
                st.rerun()