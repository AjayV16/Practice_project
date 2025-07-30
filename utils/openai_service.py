"""
OpenAI service for generating intelligent summaries and answers
"""
import json
import os
from typing import Optional
from openai import OpenAI
import streamlit as st
from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS, TEMPERATURE


class OpenAIService:
    def __init__(self):
        self.client = None
        
    def initialize_client(self) -> bool:
        """Initialize OpenAI client"""
        try:
            if not OPENAI_API_KEY:
                st.error("❌ OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
                st.info("💡 Get your API key from https://platform.openai.com/api-keys")
                return False
            
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            return True
            
        except Exception as e:
            st.error(f"❌ Failed to initialize OpenAI client: {str(e)}")
            return False
    
    def generate_intelligent_summary(self, transcript: str, question: str) -> str:
        """Generate an intelligent summary that answers the question"""
        if not self.client:
            return self._fallback_summary(transcript, question)
        
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational assistant that provides clear, concise answers from video transcripts. "
                                   "Your task is to answer the user's question based on the video content provided. "
                                   "Keep your response focused, educational, and easy to understand. "
                                   "If the transcript doesn't contain information to answer the question, say so."
                    },
                    {
                        "role": "user",
                        "content": f"Question: {question}\n\n"
                                   f"Video transcript: {transcript}\n\n"
                                   f"Based on the video transcript, provide a **very short answer**, ideally in **2 lines or fewer**. Keep it crisp and clear."

                    }
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.warning(f"OpenAI service unavailable: {str(e)}")
            return self._fallback_summary(transcript, question)
    
    def _fallback_summary(self, transcript: str, question: str) -> str:
        """Fallback summary when OpenAI is not available"""
        if not transcript:
            return "No transcript content available."
        
        # Clean transcript
        cleaned = self._clean_transcript(transcript)
        
        # Split into sentences
        sentences = [s.strip() for s in cleaned.split(". ") if len(s.strip()) > 10]
        
        # Find relevant sentences
        question_lower = question.lower()
        question_words = [word.strip('.,!?').lower() for word in question.split() if len(word) > 3]
        
        scored_sentences = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            score = 0
            
            # Score based on question words
            for word in question_words:
                if word in sentence_lower:
                    score += 2
            
            # Bonus for educational indicators
            indicators = ['because', 'the reason', 'helps', 'allows', 'enables', 'controls', 'responsible']
            for indicator in indicators:
                if indicator in sentence_lower:
                    score += 3
            
            if score > 0:
                scored_sentences.append((sentence, score))
        
        # Sort and select top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        if scored_sentences:
            top_sentences = [sent[0] for sent in scored_sentences[:3]]
            return f"Based on the video: {' '.join(top_sentences)}"
        else:
            return f"The video content: {' '.join(sentences[:2])}"
    
    def _clean_transcript(self, transcript: str) -> str:
        """Clean transcript text"""
        # Remove excessive dashes and clean up formatting
        cleaned = transcript.replace(" - ", " ")
        cleaned = " ".join(cleaned.split())  # Remove extra whitespace
        return cleaned
    
    def analyze_video_topic(self, transcript: str) -> str:
        """Analyze what the video is about"""
        if not self.client:
            return "Educational content"
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "Analyze the video transcript and provide a brief topic summary in 1-2 sentences."
                    },
                    {
                        "role": "user",
                        "content": f"Video transcript: {transcript[:500]}..."
                    }
                ],
                max_tokens=50,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return "Educational content"