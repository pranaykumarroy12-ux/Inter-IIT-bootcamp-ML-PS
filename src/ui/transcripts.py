import streamlit as st

def render_transcripts():
    st.markdown("<h1>📑 Transcripts (Raw vs Refined)</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p class="subtitle">
        Compare the original transcription with the AI-refined version.
        </p>
    """, unsafe_allow_html=True)
    
    if "pipeline_results" not in st.session_state or st.session_state.pipeline_results is None:
        st.warning("No results available. Please process an audio file first.")
        return
        
    results = st.session_state.pipeline_results
    
    view_mode = st.radio("View as:", ["Side by Side", "Unified (Refined Only)"], horizontal=True, label_visibility="collapsed")
    
    if view_mode == "Side by Side":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🟦 Raw Transcript (Stage 1)")
            st.caption("Original output from Speech-to-Text model.")
            st.text_area("Raw Text", results["raw_transcript"], height=500, disabled=True, label_visibility="collapsed")
            
        with col2:
            st.markdown("### 🟩 Refined Transcript (Stage 2)")
            st.caption("Domain terms corrected, intent preserved.")
            st.text_area("Refined Text", results["refined_transcript"], height=500, disabled=True, label_visibility="collapsed")
    else:
        st.markdown("### 🟩 Refined Transcript (Stage 2)")
        st.caption("Domain terms corrected, intent preserved.")
        st.text_area("Refined Text", results["refined_transcript"], height=500, disabled=True, label_visibility="collapsed")
