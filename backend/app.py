# app.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import tempfile
import logging

# Import services and models
from rag_service import rag_service
from stt_service import stt_service
from tts_service import tts_service
from models import QueryRequest, ChatRequest, Response, TranscribeResponse, HealthResponse
from utils import detect_emotion
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="AI Tutor RAG API",
    description="Conversational AI Tutor with RAG, STT, and TTS",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🎓 AI Tutor RAG API",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "query": "POST /query",
            "chat": "POST /chat",
            "transcribe": "POST /transcribe",
            "speak": "POST /speak"
        },
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        llm="Google Gemini",
        model=settings.GEMINI_MODEL,
        stt_service=settings.STT_SERVICE,
        tts_service=settings.TTS_SERVICE,
        version="1.0.0"
    )

# Query endpoint (single query without conversation history)
@app.post("/query", response_model=Response)
async def query_endpoint(request: QueryRequest):
    """
    Answer a single query without conversation history
    
    Args:
        request: QueryRequest with question
        
    Returns:
        Response with answer text and detected emotion
    """
    try:
        logger.info(f"📝 Query received: {request.question}")
        
        # Get answer from RAG service
        answer, source_docs = rag_service.query(request.question)
        
        # Detect emotion from answer
        emotion = detect_emotion(answer)
        
        logger.info(f"✅ Query answered with emotion: {emotion}")
        return Response(text=answer, emotion=emotion)
    
    except Exception as e:
        logger.error(f"❌ Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Chat endpoint (multi-turn conversation with history)
@app.post("/chat", response_model=Response)
async def chat_endpoint(request: ChatRequest):
    """
    Answer query with conversation history (multi-turn conversation)
    
    Args:
        request: ChatRequest with question and session_id
        
    Returns:
        Response with answer text and detected emotion
    """
    try:
        logger.info(f"💬 Chat [{request.session_id}]: {request.question}")
        
        # Get answer from RAG service with conversation history
        answer, source_docs = rag_service.chat(request.question, request.session_id)
        
        # Detect emotion from answer
        emotion = detect_emotion(answer)
        
        logger.info(f"✅ Chat answered with emotion: {emotion}")
        return Response(text=answer, emotion=emotion)
    
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# STT endpoint (Speech-to-Text)
@app.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(audio: UploadFile = File(...)):
    """
    Transcribe uploaded audio file to text
    
    Args:
        audio: Audio file (WAV format recommended)
        
    Returns:
        TranscribeResponse with transcribed text
    """
    try:
        logger.info(f"🎤 Transcription request: {audio.filename}")
        
        # Save uploaded file temporarily
        temp_path = os.path.join(tempfile.gettempdir(), f"temp_{audio.filename}")
        with open(temp_path, "wb") as f:
            content = await audio.read()
            f.write(content)
        
        # Transcribe using STT service
        text = stt_service.transcribe_audio_file(temp_path)
        
        # Cleanup temp file
        os.remove(temp_path)
        
        if text:
            logger.info(f"✅ Transcription successful: {text}")
            return TranscribeResponse(text=text)
        else:
            raise HTTPException(status_code=400, detail="Could not transcribe audio")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# TTS endpoint (Text-to-Speech)
@app.post("/speak")
async def text_to_speech(text: str):
    """
    Convert text to speech and return audio file
    
    Args:
        text: Text to convert to speech
        
    Returns:
        Audio file (WAV format)
    """
    try:
        logger.info(f"🔊 TTS request: {text[:50]}...")
        
        # Generate speech using TTS service
        audio_path = tts_service.text_to_speech(text)
        
        if audio_path and os.path.exists(audio_path):
            logger.info(f"✅ TTS successful: {audio_path}")
            return FileResponse(
                audio_path,
                media_type="audio/wav",
                filename="speech.wav"
            )
        else:
            raise HTTPException(status_code=500, detail="TTS generation failed")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ TTS error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the application
if __name__ == "__main__":
    import uvicorn
    
    logger.info("="*60)
    logger.info("🚀 Starting AI Tutor Backend Server")
    logger.info(f"📍 Host: {settings.HOST}:{settings.PORT}")
    logger.info(f"🤖 LLM: {settings.GEMINI_MODEL}")
    logger.info(f"🎤 STT: {settings.STT_SERVICE}")
    logger.info(f"🔊 TTS: {settings.TTS_SERVICE}")
    logger.info("="*60)
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info"
    )
