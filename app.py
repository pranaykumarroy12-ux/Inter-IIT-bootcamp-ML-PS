import streamlit as st
import sys
from pathlib import Path
import tempfile
import json
import os

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.pipeline.workflow import MeetingPipeline
from src.utils.audio import SUPPORTED_AUDIO_EXTENSIONS

# ==========================================
# Page Configuration & UI Setup
# ==========================================
st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ AI-Powered Meeting Assistant")
st.markdown("""
Upload a meeting recording to automatically generate a highly accurate transcript, correct domain-specific terminology, and extract structured meeting minutes, decisions, and action items.
""")

# ==========================================
# File Upload & Initialization
# ==========================================
# Strip the leading dots for Streamlit's uploader
allowed_extensions = [ext.strip('.') for ext in SUPPORTED_AUDIO_EXTENSIONS]

uploaded_file = st.file_uploader(
    "Upload Meeting Audio", 
    type=allowed_extensions,
    help="Supported formats: mp3, wav, m4a, mpeg, flac, aac, ogg"
)

if "pipeline_results" not in st.session_state:
    st.session_state.pipeline_results = None

# ==========================================
# Processing Pipeline
# ==========================================
if uploaded_file is not None:
    if st.button("🚀 Process Meeting Audio", type="primary"):
        st.session_state.pipeline_results = None  # Reset previous results
        
        # Save the uploaded file to a temporary location
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_audio_path = tmp_file.name

            pipeline = MeetingPipeline()
            
            # Use columns to show progress steps
            progress_container = st.container()
            with progress_container:
                st.write("### Processing Status")
                
                # Stage 1
                with st.spinner("⏳ Stage 1: Transcribing audio to text (This may take a few minutes on CPU)..."):
                    raw_transcript = pipeline.run_transcription(temp_audio_path)
                st.success("✅ Stage 1: Transcription Complete!")
                
                # Stage 2
                with st.spinner("⏳ Stage 2: Refining transcript for domain accuracy via Gemini..."):
                    refined_transcript = pipeline.run_refinement(raw_transcript)
                st.success("✅ Stage 2: Refinement Complete!")
                
                # Stage 3
                with st.spinner("⏳ Stage 3: Extracting minutes, decisions, and actionable tasks..."):
                    documentation = pipeline.run_documentation(refined_transcript)
                st.success("✅ Stage 3: Meeting Documentation Complete!")
            
            # Save results to session state
            st.session_state.pipeline_results = {
                "raw_transcript": raw_transcript,
                "refined_transcript": refined_transcript,
                "documentation": documentation
            }
            
        except Exception as e:
            st.error(f"❌ An error occurred during processing: {str(e)}")
        finally:
            # Clean up the temporary file
            if 'temp_audio_path' in locals() and os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)

# ==========================================
# Results Display & Downloads
# ==========================================
if st.session_state.pipeline_results is not None:
    results = st.session_state.pipeline_results
    
    st.divider()
    st.header("📊 Processing Results")
    
    # Create Tabs for organized viewing
    tab1, tab2, tab3 = st.tabs(["📋 Meeting Record (Minutes & Tasks)", "📝 Transcripts (Raw vs Refined)", "💾 Downloads"])
    
    # --- TAB 1: Meeting Record ---
    with tab1:
        st.markdown(results["documentation"]["markdown"])
        
        with st.expander("View Raw JSON Structure"):
            st.json(results["documentation"]["json_record"])

    # --- TAB 2: Transcripts ---
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Raw Transcript (Stage 1)")
            st.info("Original output from Speech-to-Text model.")
            st.text_area("Raw Text", results["raw_transcript"], height=400, disabled=True)
            
        with col2:
            st.subheader("Refined Transcript (Stage 2)")
            st.success("Domain terms corrected, intent preserved.")
            st.text_area("Refined Text", results["refined_transcript"], height=400, disabled=True)

    # --- TAB 3: Downloads ---
    with tab3:
        st.subheader("Download Generated Assets")
        st.markdown("Select the format you wish to download for your records.")
        
        col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)
        
        with col_dl1:
            st.download_button(
                label="📥 Download Raw Transcript (.txt)",
                data=results["raw_transcript"],
                file_name="raw_transcript.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col_dl2:
            st.download_button(
                label="📥 Download Refined Transcript (.txt)",
                data=results["refined_transcript"],
                file_name="refined_transcript.txt",
                mime="text/plain",
                use_container_width=True
            )
            
        with col_dl3:
            # Generate the professional PDF from the JSON structured record
            from src.utils.pdf_export import generate_meeting_pdf
            pdf_bytes = generate_meeting_pdf(results["documentation"]["json_record"])
            
            st.download_button(
                label="📥 Download Meeting Record (.pdf)",
                data=pdf_bytes,
                file_name="meeting_record.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
        with col_dl4:
            json_str = json.dumps(results["documentation"]["json_record"], indent=4)
            st.download_button(
                label="📥 Download Structured Record (.json)",
                data=json_str,
                file_name="meeting_record.json",
                mime="application/json",
                use_container_width=True
            )
