# stt_service.py
import speech_recognition as sr
from typing import Optional
import logging
from config import settings

logger = logging.getLogger(__name__)

class STTService:
    """
    FREE Speech-to-Text Service using Google Web Speech API
    - No API key required
    - Uses SpeechRecognition library
    - Internet required but completely free
    """
    
    def __init__(self):
        """Initialize FREE STT service"""
        self.recognizer = sr.Recognizer()
        
        # Configure recognizer settings
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        logger.info("✅ FREE STT Service initialized (Google Web Speech API)")
    
    def transcribe_audio_file(self, audio_file_path: str, language: str = None) -> Optional[str]:
        """
        Transcribe audio file to text using FREE Google Web Speech API
        
        Args:
            audio_file_path: Path to audio file (WAV format recommended)
            language: Language code (e.g., "en-US", "hi-IN")
            
        Returns:
            Transcribed text or None if transcription fails
        """
        language = language or settings.STT_LANGUAGE
        
        try:
            # Read audio file
            with sr.AudioFile(audio_file_path) as source:
                logger.info(f"📂 Reading audio file: {audio_file_path}")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record the audio data
                audio_data = self.recognizer.record(source)
            
            # Transcribe using FREE Google Web Speech API
            logger.info("🔄 Transcribing with FREE Google Web Speech API...")
            text = self.recognizer.recognize_google(audio_data, language=language)
            
            logger.info(f"✅ Transcription successful: {text}")
            return text
        
        except sr.UnknownValueError:
            logger.error("❌ Speech not understood")
            return None
        
        except sr.RequestError as e:
            logger.error(f"❌ STT API request error: {e}")
            raise Exception(f"STT service error: {e}")
        
        except Exception as e:
            logger.error(f"❌ STT error: {e}")
            raise Exception(f"Transcription failed: {e}")
    
    def transcribe_microphone(
        self, 
        language: str = None, 
        timeout: int = 5, 
        phrase_time_limit: int = 10
    ) -> Optional[str]:
        """
        Transcribe from microphone in real-time
        
        Args:
            language: Language code
            timeout: Timeout waiting for speech (seconds)
            phrase_time_limit: Maximum time for phrase (seconds)
            
        Returns:
            Transcribed text or None
        """
        language = language or settings.STT_LANGUAGE
        
        try:
            with sr.Microphone() as source:
                logger.info("🎤 Listening from microphone...")
                print("🎤 Speak now...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            # Transcribe
            logger.info("🔄 Transcribing...")
            text = self.recognizer.recognize_google(audio, language=language)
            
            logger.info(f"✅ Transcribed: {text}")
            return text
        
        except sr.WaitTimeoutError:
            logger.error("⏱️ Listening timed out - no speech detected")
            return None
        
        except sr.UnknownValueError:
            logger.error("❌ Could not understand audio")
            return None
        
        except Exception as e:
            logger.error(f"❌ Microphone transcription error: {e}")
            return None

# Create global STT service instance
stt_service = STTService()
