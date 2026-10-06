import streamlit as st
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import UI components
from src.ui.theme import load_custom_css
from src.ui.sidebar import render_sidebar
from src.ui.home import render_home
from src.ui.processing import render_processing
from src.ui.meeting_record import render_meeting_record
from src.ui.transcripts import render_transcripts
from src.ui.highlights import render_highlights
from src.ui.downloads import render_downloads

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load theme
load_custom_css()

# Render persistent sidebar
render_sidebar()

# ==========================================
# Routing
# ==========================================
page = st.session_state.get("current_page", "Home")

if page == "Home":
    render_home()
elif page == "Processing":
    render_processing()
elif page == "Meeting Record":
    render_meeting_record()
elif page == "Transcripts":
    render_transcripts()
elif page == "AI Highlights":
    render_highlights()
elif page == "Downloads":
    render_downloads()
else:
    render_home()
