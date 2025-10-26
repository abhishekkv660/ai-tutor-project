# config.py
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Gemini Model Configuration
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 1024
    
    # Embedding Model
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"  # FREE local model
    
    # Vector Database
    VECTOR_DB_PATH: str = "./chroma_db"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    RETRIEVAL_K: int = 3
    
    # Data Directory
    DATA_DIR: str = "./data"
    
    # STT Configuration (FREE)
    STT_SERVICE: str = os.getenv("STT_SERVICE", "google_free")
    STT_LANGUAGE: str = "en-US"
    
    # TTS Configuration (FREE OFFLINE)
    TTS_SERVICE: str = os.getenv("TTS_SERVICE", "pyttsx3")
    TTS_LANGUAGE: str = "en"
    TTS_SPEED: int = 150
    TTS_VOLUME: float = 0.9
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Validate API key
if not settings.GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY is required in .env file")
