"""
VideoDB client utilities for video upload, indexing, and management
"""
import videodb
import tempfile
import os
from typing import Optional, List, Dict
import streamlit as st
from config import VIDEODB_API_KEY, DEFAULT_COLLECTION_NAME


class VideoDBClient:
    def __init__(self):
        self.connection = None
        self.collection = None

    def initialize_connection(self) -> bool:
        """Initialize connection to VideoDB"""
        try:
            if not VIDEODB_API_KEY:
                st.error("❌ VideoDB API key not found. Please set VIDEODB_API_KEY environment variable.")
                return False

            self.connection = videodb.connect(api_key=VIDEODB_API_KEY)

            # Fix: Create collection with name and description
            try:
                collections = self.connection.get_collections()
                if collections:
                    self.collection = collections[0]
                else:
                    self.collection = self.connection.create_collection(
                        name=DEFAULT_COLLECTION_NAME,
                        description="Collection for educational videos"
                    )
            except Exception as e:
                st.warning(f"⚠️ Could not access collections: {str(e)}")
                self.collection = self.connection.create_collection(
                    name=DEFAULT_COLLECTION_NAME,
                    description="Collection for educational videos"
                )

            return True

        except Exception as e:
            st.error(f"❌ Failed to connect to VideoDB: {str(e)}")
            return False

    def upload_video_from_url(self, url: str):
        """Upload video from URL"""
        try:
            if not self.connection:
                st.error("❌ VideoDB connection not established")
                return None

            with st.spinner("🔄 Uploading and indexing video from URL..."):
                video = self.collection.upload(url=url)
                st.success(f"✅ Video uploaded successfully! ID: {video.id}")
                return video

        except Exception as e:
            st.error(f"❌ Failed to upload video from URL: {str(e)}")
            return None

    def upload_video_from_file(self, uploaded_file):
        """Upload video from local file"""
        try:
            if not self.connection:
                st.error("❌ VideoDB connection not established")
                return None

            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            with st.spinner("🔄 Uploading and indexing video from file..."):
                video = self.collection.upload(file_path=tmp_path)
                st.success(f"✅ Video uploaded successfully! ID: {video.id}")
                os.unlink(tmp_path)
                return video

        except Exception as e:
            st.error(f"❌ Failed to upload video file: {str(e)}")
            return None

    def index_video(self, video) -> bool:
        """Index video for transcript and scenes"""
        try:
            with st.spinner("🔍 Indexing video..."):
                try:
                    video.index_spoken_words()
                    st.info("✅ Indexed spoken words")
                except Exception as e:
                    st.warning(f"⚠️ Could not index spoken words: {str(e)}")

                try:
                    video.index_scenes()
                    st.info("✅ Indexed scenes")
                except Exception as e:
                    st.warning(f"⚠️ Could not index scenes: {str(e)}")

            return True
        except Exception as e:
            st.error(f"❌ Failed to index video: {str(e)}")
            return False

    def get_video_transcript(self, video) -> tuple[str, List[Dict]]:
        """Get video transcript"""
        try:
            transcript = video.get_transcript()
            full_text = ""
            segments = []

            for segment in transcript:
                text = segment.get("text", "")
                start = segment.get("start", 0)
                end = segment.get("end", 0)
                full_text += f"{text} "
                segments.append({"text": text, "start": start, "end": end})

            return full_text.strip(), segments
        except Exception as e:
            st.warning(f"Could not get transcript: {e}")
            return "", []
