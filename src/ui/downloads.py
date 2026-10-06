import streamlit as st
import json

def render_downloads():
    st.markdown("<h1>⬇️ Download Generated Assets</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p class="subtitle">
        Export your meeting record in your preferred format.
        </p>
    """, unsafe_allow_html=True)
    
    if "pipeline_results" not in st.session_state or st.session_state.pipeline_results is None:
        st.warning("No results available. Please process an audio file first.")
        return
        
    results = st.session_state.pipeline_results
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown("""
        <div class="css-1r6slb0" style="margin-bottom: 15px; height: 160px;">
            <h3 style="margin-top: 0; color: #60A5FA !important;">Raw Transcript</h3>
            <span class="badge">.txt</span>
            <p style="font-size: 13px; color: #94A3B8; margin-top: 10px;">Original output from Speech-to-Text model.</p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download",
            data=results["raw_transcript"],
            file_name="raw_transcript.txt",
            mime="text/plain",
            use_container_width=True,
            key="dl_raw"
        )
        
    with c2:
        st.markdown("""
        <div class="css-1r6slb0" style="margin-bottom: 15px; height: 160px;">
            <h3 style="margin-top: 0; color: #34D399 !important;">Refined Transcript</h3>
            <span class="badge">.txt</span>
            <p style="font-size: 13px; color: #94A3B8; margin-top: 10px;">Domain-corrected transcript.</p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="⬇️ Download",
            data=results["refined_transcript"],
            file_name="refined_transcript.txt",
            mime="text/plain",
            use_container_width=True,
            key="dl_ref"
        )
        
    with c3:
        st.markdown("""
        <div class="css-1r6slb0" style="margin-bottom: 15px; height: 160px;">
            <h3 style="margin-top: 0; color: #F87171 !important;">Meeting Record</h3>
            <span class="badge">.pdf</span>
            <p style="font-size: 13px; color: #94A3B8; margin-top: 10px;">Complete meeting minutes with decisions and action items.</p>
        </div>
        """, unsafe_allow_html=True)
        
        from src.utils.pdf_export import generate_meeting_pdf
        try:
            pdf_bytes = generate_meeting_pdf(results["documentation"]["json_record"])
            st.download_button(
                label="⬇️ Download",
                data=pdf_bytes,
                file_name="meeting_record.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="dl_pdf"
            )
        except Exception as e:
            st.error("PDF Generation failed.")
            
    with c4:
        st.markdown("""
        <div class="css-1r6slb0" style="margin-bottom: 15px; height: 160px;">
            <h3 style="margin-top: 0; color: #A78BFA !important;">Structured Record</h3>
            <span class="badge">.json</span>
            <p style="font-size: 13px; color: #94A3B8; margin-top: 10px;">Machine-readable structured data.</p>
        </div>
        """, unsafe_allow_html=True)
        
        json_str = json.dumps(results["documentation"]["json_record"], indent=4)
        st.download_button(
            label="⬇️ Download",
            data=json_str,
            file_name="meeting_record.json",
            mime="application/json",
            use_container_width=True,
            key="dl_json"
        )
