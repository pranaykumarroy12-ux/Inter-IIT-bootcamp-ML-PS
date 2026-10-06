import streamlit as st
from google import genai
from src.utils.config import get_gemini_api_key, DEFAULT_DOCUMENTATION_MODEL

def render_chat():
    st.markdown("<h1>💬 Chat with the Meeting</h1>", unsafe_allow_html=True)
    st.markdown("""
        <p class="subtitle">
        Ask questions about the meeting and get instant answers based strictly on the transcript.
        </p>
    """, unsafe_allow_html=True)
    
    if "pipeline_results" not in st.session_state or st.session_state.pipeline_results is None:
        st.warning("No meeting data available. Please process an audio file first.")
        return
        
    transcript = st.session_state.pipeline_results["refined_transcript"]
    
    # Initialize chat history tied to the current session
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hi! I have read the transcript of your meeting. What would you like to know?"}
        ]
        
    # Clear chat button
    col1, col2 = st.columns([8, 1])
    with col2:
        if st.button("🗑️ Clear"):
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "Hi! I have read the transcript of your meeting. What would you like to know?"}
            ]
            st.rerun()

    st.divider()

    # Create a container for chat messages
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
    # Chat Input
    if prompt := st.chat_input("E.g., Did they agree on a final budget?"):
        # Append user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # Display user message instantly
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # Generate and display AI response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing meeting record..."):
                    try:
                        client = genai.Client(api_key=get_gemini_api_key())
                        
                        system_context = (
                            "You are an AI Meeting Assistant. You are answering questions based ONLY on the following meeting transcript. "
                            "If the answer is not in the transcript, politely say 'I cannot find the answer to this in the meeting record.' "
                            "Do not hallucinate or make up information outside of this transcript.\n\n"
                            f"MEETING TRANSCRIPT:\n{transcript}\n\n"
                        )
                        
                        # Build the prompt history
                        history_str = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.chat_messages])
                        full_prompt = f"{system_context}\n\nChat History:\n{history_str}\n\nAssistant:"
                        
                        response = client.models.generate_content(
                            model=DEFAULT_DOCUMENTATION_MODEL,
                            contents=full_prompt
                        )
                        
                        ai_text = response.text
                        st.markdown(ai_text)
                        
                        # Save assistant response
                        st.session_state.chat_messages.append({"role": "assistant", "content": ai_text})
                        
                    except Exception as e:
                        st.error(f"Error communicating with AI: {str(e)}")
