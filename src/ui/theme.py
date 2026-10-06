import streamlit as st

def load_custom_css():
    st.markdown("""
        <style>
        /* Base Theme */
        .stApp {
            background-color: #0B1120;
            color: #E2E8F0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Typography adjustments */
        h1, h2, h3, h4, h5, h6 {
            color: #F8FAFC !important;
            font-weight: 600 !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #0F172A;
            border-right: 1px solid #1E293B;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
            width: 100%;
        }
        
        .stButton > button:hover {
            opacity: 0.9;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
            color: white;
        }
        
        /* Secondary Buttons / Nav buttons (can target via specific containers if needed) */
        
        /* Cards */
        .css-1r6slb0, [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
            background-color: #1E293B;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #334155;
        }
        
        /* Metric Cards */
        [data-testid="stMetric"] {
            background-color: #1E293B;
            border: 1px solid #334155;
            padding: 15px;
            border-radius: 10px;
        }
        
        /* File Uploader styling */
        [data-testid="stFileUploadDropzone"] {
            background-color: #1E293B;
            border: 2px dashed #4F46E5;
            border-radius: 12px;
        }
        
        /* Status Indicators */
        .status-success {
            color: #10B981;
            font-weight: 500;
        }
        
        .status-processing {
            color: #3B82F6;
            font-weight: 500;
        }
        
        .status-error {
            color: #EF4444;
            font-weight: 500;
        }
        
        /* Dividers */
        hr {
            border-color: #334155;
        }
        
        /* Subtitle Text */
        .subtitle {
            color: #94A3B8;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        
        /* Feature Row */
        .feature-box {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            height: 100%;
        }
        
        .feature-icon {
            font-size: 24px;
            margin-bottom: 10px;
            color: #4F46E5;
        }
        
        /* Nav button overrides */
        .nav-btn {
            background-color: transparent !important;
            border: none !important;
            color: #94A3B8 !important;
            text-align: left !important;
            justify-content: flex-start !important;
            padding: 10px 15px !important;
            border-radius: 8px !important;
            margin-bottom: 5px !important;
            background: none !important;
        }
        
        .nav-btn:hover {
            background-color: #1E293B !important;
            color: white !important;
            box-shadow: none !important;
        }
        
        .nav-btn-active {
            background: linear-gradient(90deg, rgba(79,70,229,0.2) 0%, rgba(79,70,229,0) 100%) !important;
            border-left: 3px solid #4F46E5 !important;
            color: white !important;
            border-radius: 0 8px 8px 0 !important;
        }
        
        /* Task Cards */
        .task-card {
            background-color: #1E293B;
            border-left: 4px solid #4F46E5;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px 8px 8px 4px;
        }
        
        .badge {
            background-color: #334155;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            color: #E2E8F0;
        }
        </style>
    """, unsafe_allow_html=True)
