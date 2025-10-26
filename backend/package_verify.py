# verify_conda.py
import sys
print("="*60)
print("🐍 Python & Conda Environment Check")
print("="*60)
print(f"Python: {sys.version}")
print(f"Location: {sys.executable}")
print()

packages = {
    'fastapi': 'FastAPI',
    'langchain': 'LangChain',
    'langchain_google_genai': 'LangChain Google GenAI',
    'langchain_core': 'LangChain Core',
    'chromadb': 'ChromaDB',
    'speech_recognition': 'SpeechRecognition',
    'pyttsx3': 'pyttsx3',
    'pyaudio': 'PyAudio',
    'pydantic': 'Pydantic'
}

print("📦 Package Status:")
print("-"*60)
for module, name in packages.items():
    try:
        mod = __import__(module)
        version = getattr(mod, '__version__', 'installed')
        print(f"✅ {name:30} {version}")
    except ImportError:
        print(f"❌ {name:30} NOT INSTALLED")

print("="*60)
print("\n🎯 Ready to run AI Tutor Backend!")
