# models.py
from pydantic import BaseModel, Field
from typing import Optional

class QueryRequest(BaseModel):
    """Request model for single query endpoint"""
    question: str = Field(..., min_length=1, description="User's question")

class ChatRequest(BaseModel):
    """Request model for multi-turn chat endpoint"""
    question: str = Field(..., min_length=1, description="User's question")
    session_id: Optional[str] = Field(default="default", description="Session ID")

class Response(BaseModel):
    """Response model with text and emotion"""
    text: str = Field(..., description="AI response")
    emotion: str = Field(..., description="Detected emotion")

class TranscribeResponse(BaseModel):
    """Response model for STT endpoint"""
    text: str = Field(..., description="Transcribed text")

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    llm: str
    model: str
    stt_service: str
    tts_service: str
    version: str
