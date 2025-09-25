import streamlit as st
import sys
import os
import time
import asyncio
from typing import Generator

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.bot import SimpleConsulateBot

# Configure the Streamlit page
st.set_page_config(
    page_title="Egyptian Consulate Paris - AI Assistant",
    page_icon="🏛️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Egyptian theme
st.markdown("""
<style>
    /* Force light theme */
    .stApp {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Override any dark mode elements */
    .stApp > header {
        background-color: transparent !important;
    }
    
    /* Ensure sidebar is light */
    .css-1d391kg {
        background-color: #f8f9fa !important;
    }
    
    /* Force light background for all containers */
    .block-container {
        background-color: #ffffff !important;
    }
    
    /* Override any dark theme chat elements */
    .stChatMessage {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Force all input elements to light theme */
    input, textarea, select {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        border: 1px solid #d1d5db !important;
    }
    
    /* Force any text input widgets to be light */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Force any text area widgets to be light */
    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, rgba(0,35,102,0.9) 0%, rgba(255,255,255,0.9) 50%, rgba(206,17,38,0.9) 100%); /* French and Egyptian flag colors with better opacity */
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid #d4af37; /* Gold border - a nod to Egyptian heritage */
    }
    .main-header h1 {
        color: #111827; /* Dark text for better readability */
        margin: 0;
        font-size: 2.5em;
        text-shadow: 1px 1px 1px rgba(255,255,255,0.5);
        font-family: 'Garamond', serif; /* More elegant, French-inspired typography */
        font-weight: bold;
    }
    .main-header h2 {
        color: #1f2937; /* Dark but slightly lighter than h1 */
        margin: 12px 0 0 0;
        font-size: 1.3em;
        font-family: 'Garamond', serif;
    }
    /* Logo styling */
    .main-header img {
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
        transition: transform 0.3s ease;
    }
    .main-header img:hover {
        transform: scale(1.05);
    }
    .main-header p {
        color: #374151; /* Dark enough to read clearly */
        margin: 12px 0 0 0;
        font-style: italic; /* A touch of French elegance */
    }
    /* Chat styling */
    .stChatMessage {
        padding: 1.2rem;
        border-radius: 0.7rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* User message styling - French theme */
    .stChatMessage[data-testid*="user"] {
        background-color: #f5f5f5;
        border-left: 4px solid #002366; /* French blue */
    }
    
    /* Assistant message styling - Egyptian theme */
    .stChatMessage[data-testid*="assistant"] {
        background-color: #f9f7f2; /* Papyrus-like color */
        border-left: 4px solid #CE1126; /* Egyptian red */
    }
    
    /* Sidebar styling */
    .sidebar .stButton button {
        width: 100%;
        margin: 7px 0;
        background-color: #002366; /* French blue */
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .sidebar .stButton button:hover {
        background-color: #CE1126; /* Egyptian red on hover */
        transform: translateY(-2px);
    }
    
    /* Chat input styling - Force light theme */
    div[data-testid="stChatInput"] {
        background-color: #ffffff !important;
    }
    
    div[data-testid="stChatInput"] > div {
        background-color: #ffffff !important;
    }
    
    div[data-testid="stChatInput"] > div > div {
        background-color: #ffffff !important;
    }
    
    div[data-testid="stChatInput"] > div > div > div {
        background-color: #ffffff !important;
    }
    
    div[data-testid="stChatInput"] > div > div > div > div {
        border-radius: 30px;
        border: 2px solid #d4af37 !important; /* Gold border */
        padding: 5px 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        background-color: #ffffff !important; /* Force white background */
        color: #1f2937 !important; /* Force dark text */
    }
    
    /* Force the textarea inside chat input to be light */
    div[data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        border: none !important;
    }
    
    /* Force placeholder text to be visible */
    div[data-testid="stChatInput"] textarea::placeholder {
        color: #6b7280 !important;
        opacity: 0.8 !important;
    }
    
    /* Global font styling */
    body, .stMarkdown, p {
        font-family: 'Garamond', serif;
    }
    
    /* Footer styling */
    .st-emotion-cache-hzygls {
        position: relative !important;
        bottom: 0px !important;
        width: 100% !important;
        min-width: 100% !important;
        background-color: #E6EBF1 !important; /* Light theme footer */
        display: flex !important;
        flex-direction: column !important;
        -webkit-box-align: center !important;
        align-items: center !important;
        border-top: 1px solid #e5e7eb !important; /* Light border */
        padding: 10px 0 !important;
    }
    
    /* Decorative elements - right star only */
    .stApp::after {
        content: "";
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 40px;
        height: 40px;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23d4af37"><path d="M12 2L9.2 8.6 2 9.2 7 14.57 5.18 22 12 18.57 18.82 22 17 14.57 22 9.2 14.8 8.6z"/></svg>');
        background-repeat: no-repeat;
        opacity: 0.5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "bot" not in st.session_state:
        st.session_state.bot = SimpleConsulateBot()

def stream_response_sync(message: str) -> Generator[str, None, None]:
    """Synchronous wrapper for streaming response"""
    try:
        # Create a new event loop for this operation
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def get_response():
            async for chunk in st.session_state.bot.stream_response(message):
                if chunk:
                    yield chunk
        
        try:
            # Run the async generator
            async_gen = get_response()
            while True:
                try:
                    chunk = loop.run_until_complete(async_gen.__anext__())
                    yield chunk
                except StopAsyncIteration:
                    break
        finally:
            loop.close()
            
    except Exception as e:
        yield f"Sorry, I encountered an error: {str(e)}"

def clear_chat_history():
    """Clear the chat history"""
    st.session_state.messages = []
    st.session_state.bot.clear_history()
    st.rerun()

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # No footer CSS needed
    
    # Load and encode the logo
    import base64
    
    def get_logo_base64():
        try:
            with open("logo.svg", "r", encoding="utf-8") as f:
                logo_svg = f.read()
            return base64.b64encode(logo_svg.encode()).decode()
        except:
            return ""
    
    logo_base64 = get_logo_base64()
    
    # Header with French-Egyptian design and logo
    if logo_base64:
        st.markdown(f"""
        <div class="main-header">
            <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 10px;">
                <img src="data:image/svg+xml;base64,{logo_base64}" style="height: 80px; width: auto;" alt="Egyptian Consulate Logo">
                <div>
                    <h1 style="margin: 0; line-height: 1.2;">Consulat d'Égypte à Paris</h1>
                    <h2 style="margin: 5px 0 0 0; font-size: 1em;">القنصلية العامة لجمهورية مصر العربية في باريس</h2>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback if logo can't be loaded
        st.markdown("""
        <div class="main-header">
            <h1>🦅 Consulat d'Égypte à Paris<br><span style="font-size: 0.7em;">القنصلية العامة لجمهورية مصر العربية في باريس</span></h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Main chat interface
    
    # Display chat history with enhanced styling
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🏛️"):
            st.write(message["content"])
    
    # Fixed placeholder text - multilingual
    placeholder_text = "Feel free to ask ..."
    
    # Chat input with fixed placeholder
    if prompt := st.chat_input(placeholder_text):
        # Add user message to session state and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.write(prompt)
        
        # Generate and display bot response with streaming
        with st.chat_message("assistant", avatar="🏛️"):
            try:
                # Use st.write_stream for token-by-token streaming
                full_response = st.write_stream(stream_response_sync(prompt))
            except Exception as e:
                full_response = f"Sorry, I encountered an error: {str(e)}"
                st.write(full_response)
            
        # Add bot response to session state
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    

if __name__ == "__main__":
    main()
