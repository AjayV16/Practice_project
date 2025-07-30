""""" 
Video Learning Assistant - ChatGPT-style Streamlit App 
"""
import streamlit as st
import tempfile
import os
from typing import List, Dict, Any
import time

from config import APP_TITLE, APP_ICON
from utils.videodb_client import VideoDBClient
from utils.openai_service import OpenAIService

def initialize_session_state():
    if 'videodb_client' not in st.session_state:
        st.session_state.videodb_client = VideoDBClient()

    if 'openai_service' not in st.session_state:
        st.session_state.openai_service = OpenAIService()

    if 'uploaded_videos' not in st.session_state:
        st.session_state.uploaded_videos = []

    if 'videodb_connected' not in st.session_state:
        st.session_state.videodb_connected = False

    if 'openai_connected' not in st.session_state:
        st.session_state.openai_connected = False

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'selected_video' not in st.session_state:
        st.session_state.selected_video = None

def initialize_services():
    if not st.session_state.videodb_connected:
        with st.spinner("🔌 Connecting to VideoDB..."):
            st.session_state.videodb_connected = st.session_state.videodb_client.initialize_connection()

    if not st.session_state.openai_connected:
        with st.spinner("🤖 Connecting to OpenAI..."):
            st.session_state.openai_connected = st.session_state.openai_service.initialize_client()

def sidebar_upload_section():
    st.sidebar.header("📁 Upload Video")
    uploaded_file = st.sidebar.file_uploader("Choose a video file", type=['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv'])
    if uploaded_file and st.sidebar.button("Upload File"):
        with st.spinner("⏳ Processing video..."):
            video = st.session_state.videodb_client.upload_video_from_file(uploaded_file)
            if video:
                st.session_state.videodb_client.index_video(video)
                st.session_state.uploaded_videos.append(video)
                st.session_state.selected_video = video
                st.rerun()

    video_url = st.sidebar.text_input("Or paste video URL")
    if video_url and st.sidebar.button("Upload from URL"):
        with st.spinner("⏳ Processing video..."):
            video = st.session_state.videodb_client.upload_video_from_url(video_url)
            if video:
                st.session_state.videodb_client.index_video(video)
                st.session_state.uploaded_videos.append(video)
                st.session_state.selected_video = video
                st.rerun()

    if st.session_state.uploaded_videos:
        selected = st.sidebar.selectbox(
            "🎥 Select video to chat with:",
            st.session_state.uploaded_videos,
            format_func=lambda v: getattr(v, 'title', v.id)
        )
        st.session_state.selected_video = selected

        if st.sidebar.button("🗑️ Delete Selected Video"):
            st.session_state.uploaded_videos = [
                v for v in st.session_state.uploaded_videos if getattr(v, "id", None) != getattr(selected, "id", None)
            ]
            if st.session_state.selected_video and getattr(st.session_state.selected_video, "id", None) == getattr(selected, "id", None):
                st.session_state.selected_video = None
            st.rerun()

def chat_interface():
    if not st.session_state.selected_video:
        st.info("📤 Upload and select a video from the sidebar to start chatting.")
        return
    
    if not st.session_state.chat_history:
        welcome_msg = "👋 Hi! Ask me anything about the selected video."
        st.session_state.chat_history.append({"role": "assistant", "message": welcome_msg})

    for msg in st.session_state.chat_history:
        align = "user" if msg['role'] == "user" else "assistant"
        with st.chat_message(align):
            st.markdown(msg['message'])

    prompt = st.chat_input("Ask something about this video...")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "message": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("🤖 Thinking..."):
            try:
                transcript, _ = st.session_state.videodb_client.get_video_transcript(st.session_state.selected_video)
                general_inputs = [
                    "hi", "hello", "okay", "ok", "thanks", "thank you", "how are you", "yo", "sup", "fine", "cool"
                ]
                if prompt.strip().lower() in general_inputs:
                    answer = "😊 Got it! Feel free to ask me anything about the selected video."
                elif transcript:
                    answer = st.session_state.openai_service.generate_intelligent_summary(transcript, prompt)
                else:
                    answer = "❌ I couldn't fetch the video transcript."

                st.session_state.chat_history.append({"role": "assistant", "message": answer})
                with st.chat_message("assistant"):
                    st.markdown(answer)
            except Exception as e:
                st.error(f"Error generating answer: {e}")

def main():
    st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")
    initialize_session_state()
    initialize_services()

    if not st.session_state.videodb_connected:
        st.error("❌ VideoDB service not available. Please check your API key.")
        st.stop()

    if not st.session_state.openai_connected:
        st.warning("⚠️ OpenAI service not available. Using fallback summarization.")

    sidebar_upload_section()
    st.title(f"{APP_ICON} {APP_TITLE}")

    # 🔁 Reset Chat Button - top right, proportionate
    reset_col = st.columns([11, 1])[1]
    with reset_col:
        if st.button("Reset", help="Reset chat history", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    chat_interface()

if __name__ == "__main__":
    main()
