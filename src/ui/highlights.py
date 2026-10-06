import streamlit as st
from src.utils.diff_viewer import generate_html_diff

def render_highlights():
    st.markdown("<h1>✦ AI Correction Highlights</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p class="subtitle">
        This view shows exactly what domain-specific jargon the AI corrected in Stage 2.
        </p>
    """, unsafe_allow_html=True)
    
    if "pipeline_results" not in st.session_state or st.session_state.pipeline_results is None:
        st.warning("No results available. Please process an audio file first.")
        return
        
    results = st.session_state.pipeline_results
    
    # Legend
    st.markdown("""
        <div style="display: flex; gap: 20px; margin-bottom: 20px;">
            <div style="background-color: #d4edda; color: #155724; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 14px;">
                🟢 Added/Corrected by AI
            </div>
            <div style="background-color: #f8d7da; color: #721c24; text-decoration: line-through; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 14px; opacity: 0.8;">
                🔴 Removed (Whisper error)
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    diff_html = generate_html_diff(results["raw_transcript"], results["refined_transcript"])
    st.markdown(diff_html, unsafe_allow_html=True)
