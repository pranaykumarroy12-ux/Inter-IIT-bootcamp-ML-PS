import streamlit as st
import time
import os
import tempfile
from src.pipeline.workflow import MeetingPipeline

def render_processing():
    st.markdown("<h1>⚙️ Processing Meeting Audio</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p class="subtitle">
        Your audio is being processed through multiple AI stages. This may take a few minutes.
        </p>
    """, unsafe_allow_html=True)
    
    if "uploaded_file" not in st.session_state or st.session_state.uploaded_file is None:
        st.warning("Please upload a file first on the Home screen.")
        if st.button("← Go to Home"):
            st.session_state.current_page = "Home"
            st.rerun()
        return

    file = st.session_state.uploaded_file
    st.info(f"🎵 **{file.name}**  •  {(file.size / (1024*1024)):.1f} MB")
    
    # We will use st.status containers for the visual timeline
    if st.session_state.get("start_processing", False):
        st.session_state.start_processing = False
        st.session_state.pipeline_results = None
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(file.read())
                temp_audio_path = tmp_file.name

            pipeline = MeetingPipeline()
            total_start = time.time()
            
            # Stage 1
            t0 = time.time()
            with st.status("Stage 1: Speech-to-Text (Transcription)", expanded=True) as status1:
                st.write("Converting audio to raw transcript using Groq Whisper API...")
                raw_transcript = pipeline.run_transcription(temp_audio_path)
                stage1_time = time.time() - t0
                if not raw_transcript or not raw_transcript.strip():
                    status1.update(label="Stage 1 Failed", state="error", expanded=True)
                    st.warning("⚠️ No speech was detected in this audio file.")
                    if 'temp_audio_path' in locals() and os.path.exists(temp_audio_path):
                        os.remove(temp_audio_path)
                    st.stop()
                status1.update(label=f"✓ Stage 1: Speech-to-Text (Completed in {stage1_time:.1f}s)", state="complete", expanded=False)
            
            # Stage 2
            t0 = time.time()
            with st.status("Stage 2: Domain-Aware Refinement", expanded=True) as status2:
                st.write("Correcting terminology, preserving intent and meaning...")
                refined_transcript = pipeline.run_refinement(raw_transcript)
                stage2_time = time.time() - t0
                status2.update(label=f"✓ Stage 2: Domain-Aware Refinement (Completed in {stage2_time:.1f}s)", state="complete", expanded=False)
                
            # Stage 3
            t0 = time.time()
            with st.status("Stage 3: Meeting Documentation", expanded=True) as status3:
                st.write("Generating structured minutes, decisions and action items...")
                documentation = pipeline.run_documentation(refined_transcript)
                stage3_time = time.time() - t0
                status3.update(label=f"✓ Stage 3: Meeting Documentation (Completed in {stage3_time:.1f}s)", state="complete", expanded=False)
                
            total_time = time.time() - total_start
            
            st.session_state.pipeline_results = {
                "raw_transcript": raw_transcript,
                "refined_transcript": refined_transcript,
                "documentation": documentation,
                "metrics": {
                    "stage1": stage1_time,
                    "stage2": stage2_time,
                    "stage3": stage3_time,
                    "total": total_time,
                    "word_count": len(raw_transcript.split())
                }
            }
            
            st.success("✅ **Processing Complete!** Your meeting record is ready.")
            if st.button("View Results →", type="primary"):
                st.session_state.current_page = "Meeting Record"
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ An error occurred during processing: {str(e)}")
        finally:
            if 'temp_audio_path' in locals() and os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
    
    elif st.session_state.get("pipeline_results") is not None:
        m = st.session_state.pipeline_results["metrics"]
        st.success(f"✓ Stage 1 Completed in {m['stage1']:.1f}s")
        st.success(f"✓ Stage 2 Completed in {m['stage2']:.1f}s")
        st.success(f"✓ Stage 3 Completed in {m['stage3']:.1f}s")
        st.info("Processing was already completed for this file.")
        if st.button("View Results →", type="primary"):
            st.session_state.current_page = "Meeting Record"
            st.rerun()
    else:
        st.info("Click 'Process Meeting Audio' on the Home screen to start.")
