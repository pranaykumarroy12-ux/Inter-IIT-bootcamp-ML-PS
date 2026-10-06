import streamlit as st
import datetime

def render_meeting_record():
    st.markdown("<h1>📄 Meeting Summary & Minutes</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p class="subtitle">
        Comprehensive meeting record with key discussion points, decisions, and action items.
        </p>
    """, unsafe_allow_html=True)
    
    if "pipeline_results" not in st.session_state or st.session_state.pipeline_results is None:
        st.warning("No results available. Please process an audio file first.")
        return
        
    results = st.session_state.pipeline_results
    doc = results["documentation"]["json_record"]
    m = results["metrics"]
    
    # We create two columns: Left for the content, Right for the Metadata card
    c_main, c_meta = st.columns([2, 1])
    
    with c_meta:
        st.markdown("<div class='css-1r6slb0'>", unsafe_allow_html=True)
        st.markdown("#### ℹ️ Meeting Details")
        st.divider()
        st.markdown(f"**Date:** {datetime.datetime.now().strftime('%b %d, %Y')}")
        st.markdown(f"**Word Count:** {m['word_count']} words")
        st.markdown(f"**Generated:** {datetime.datetime.now().strftime('%I:%M %p')}")
        file_name = st.session_state.uploaded_file.name if "uploaded_file" in st.session_state and st.session_state.uploaded_file else "Audio File"
        st.markdown(f"**Source:** `{file_name}`")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c_main:
        # Display the formatted content
        # We can either just render the markdown, or manually layout the JSON for a structured look
        
        # Summary & Minutes
        st.markdown("### 📋 Executive Summary")
        st.markdown(doc.get("summary_and_minutes", "No summary available."))
        st.divider()
        
        # Key Decisions
        st.markdown("### 🎯 Key Decisions")
        decisions = doc.get("key_decisions", [])
        if not decisions:
            st.info("No key decisions were recorded.")
        else:
            for i, dec in enumerate(decisions):
                st.markdown(f"- {dec}")
        
        st.divider()
        
        # Action Items
        st.markdown("### ⚡ Action Items")
        tasks = doc.get("action_items", [])
        if not tasks:
            st.info("No action items were assigned.")
        else:
            for t in tasks:
                owner = t.get("owner", "Unspecified")
                deadline = t.get("deadline", "Unspecified")
                
                # Render as a nice card
                st.markdown(f"""
                <div class="task-card">
                    <strong>{t.get('task_description', 'Unnamed Task')}</strong><br><br>
                    <span class="badge">👤 Owner: {owner}</span> &nbsp; 
                    <span class="badge">📅 Deadline: {deadline}</span>
                </div>
                """, unsafe_allow_html=True)
