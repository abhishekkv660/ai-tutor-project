# tts_service.py
import pyttsx3
import os
import tempfile
import logging
from typing import Optional, List
from config import settings

logger = logging.getLogger(__name__)

class TTSService:
    """
    FREE Offline Text-to-Speech Service using pyttsx3
    - Completely offline (no internet required)
    - No API keys needed
    - Works on Windows, Mac, Linux
    - Supports multiple voices
    """
    
    def __init__(self):
        """Initialize FREE offline TTS service"""
        try:
            # Initialize pyttsx3 engine
            self.engine = pyttsx3.init()
            
            # Configure voice properties
            self.engine.setProperty('rate', settings.TTS_SPEED)
            self.engine.setProperty('volume', settings.TTS_VOLUME)
            
            # Get available voices
            self.voices = self.engine.getProperty('voices')
            
            # Log initialization
            logger.info(f"✅ FREE Offline TTS initialized (pyttsx3)")
            logger.info(f"📢 Available voices: {len(self.voices)}")
            
            for idx, voice in enumerate(self.voices):
                logger.info(f"  Voice {idx}: {voice.name}")
            
            # Set default voice (female voice typically at index 1)
            if len(self.voices) > 1:
                self.engine.setProperty('voice', self.voices[1].id)
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize TTS: {e}")
            raise
    
    def get_available_voices(self) -> List[dict]:
        """
        Get list of available voices
        
        Returns:
            List of voice dictionaries
        """
        return [
            {
                'id': voice.id,
                'name': voice.name,
                'languages': voice.languages
            }
            for voice in self.voices
        ]
    
    def set_voice(self, voice_index: int = 0):
        """
        Set voice by index
        
        Args:
            voice_index: Index of voice (0, 1, 2, ...)
        """
        if 0 <= voice_index < len(self.voices):
            self.engine.setProperty('voice', self.voices[voice_index].id)
            logger.info(f"✅ Voice changed to: {self.voices[voice_index].name}")
        else:
            logger.warning(f"❌ Invalid voice index: {voice_index}")
    
    def text_to_speech(self, text: str, output_path: Optional[str] = None) -> str:
        """
        Convert text to speech and save to file
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file (optional)
            
        Returns:
            Path to generated audio file
        """
        try:
            # Generate default output path if not provided
            if not output_path:
                output_path = os.path.join(tempfile.gettempdir(), "tts_output.wav")
            
            # Ensure WAV format (pyttsx3 default)
            if not output_path.endswith('.wav'):
                output_path = output_path.replace('.mp3', '.wav')
            
            logger.info(f"🔊 Generating speech (offline): {text[:50]}...")
            
            # Save to file
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            logger.info(f"✅ Audio saved to: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"❌ TTS error: {e}")
            raise Exception(f"Text-to-speech conversion failed: {e}")
    
    def speak_realtime(self, text: str):
        """
        Speak text immediately (real-time playback)
        
        Args:
            text: Text to speak
        """
        try:
            logger.info(f"🔊 Speaking: {text[:50]}...")
            self.engine.say(text)
            self.engine.runAndWait()
            logger.info("✅ Speech completed")
        except Exception as e:
            logger.error(f"❌ Real-time speech error: {e}")
    
    def set_rate(self, rate: int):
        """Set speech rate (words per minute)"""
        self.engine.setProperty('rate', rate)
        logger.info(f"Speech rate set to: {rate} WPM")
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        self.engine.setProperty('volume', volume)
        logger.info(f"Volume set to: {volume}")

# Create global TTS service instance
tts_service = TTSService()
