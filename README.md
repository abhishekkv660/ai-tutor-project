# 🎓 AI Tutor - Conversational Learning Assistant

A full-stack conversational AI tutor powered by RAG (Retrieval-Augmented Generation) technology, featuring speech recognition, text-to-speech, and an animated mascot interface.

## ✨ Features

- 🤖 **RAG-powered Backend**: LangChain + Chroma Vector DB + Google Gemini 2.5 Flash
- 🗣️ **Speech-to-Text**: FREE Web Speech API integration
- 🔊 **Text-to-Speech**: FREE browser-based synthesis
- 🎨 **Animated Mascot**: Emotion-based character with dynamic animations
- 💬 **Multi-turn Conversations**: Context-aware chat with memory
- 📚 **Knowledge Base**: Customizable document repository
- 🚀 **REST API**: FastAPI with automatic documentation
- 🐳 **Docker Ready**: Easy deployment with Docker Compose
- ☁️ **Cloud Deployable**: AWS EC2 compatible

## 🏗️ Architecture

Frontend (HTML/JS) → Backend (FastAPI) → Gemini 2.5 Flash
↓
Vector DB (Chroma)
↓
HuggingFace Embeddings

text

## 📁 Project Structure

ai-tutor/
├── backend/
│ ├── app.py # Main FastAPI application
│ ├── rag_service.py # RAG pipeline
│ ├── stt_service.py # Speech-to-Text
│ ├── tts_service.py # Text-to-Speech
│ ├── models.py # Pydantic models
│ ├── config.py # Configuration
│ ├── utils.py # Utilities
│ ├── requirements.txt # Dependencies
│ ├── Dockerfile # Backend Docker config
│ └── data/ # Training documents
├── frontend/
│ ├── index.html # Single-page application
│ ├── Dockerfile # Frontend Docker config
│ └── nginx.conf # Nginx configuration
├── docker-compose.yml # Multi-container setup
├── .gitignore
└── README.md

text

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google Gemini API Key ([Get one free](https://makersuite.google.com/app/apikey))

### 1. Clone Repository

git clone https://github.com/abhishekkv660/ai-tutor-project.git
cd ai-tutor-project

text

### 2. Backend Setup

cd backend

Create virtual environment
python -m venv venv
venv\Scripts\activate # Windows

source venv/bin/activate # Linux/Mac
Install dependencies
pip install -r requirements.txt

Create .env file
echo GOOGLE_API_KEY=your_api_key_here > .env

Run backend
python app.py

text

Backend will run at: `http://localhost:8000`

### 3. Frontend Setup

Simply open `frontend/index.html` in your browser, or use Docker:

cd frontend

Open index.html in Chrome/Edge
text

## 🐳 Docker Deployment

### Local Deployment

Create .env file in root
echo GOOGLE_API_KEY=your_api_key_here > .env

Build and start
docker-compose up --build

Access:
Frontend: http://localhost
Backend: http://localhost:8000
text

### AWS EC2 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed AWS EC2 setup guide.

## 📚 API Documentation

Once backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `GET /health` - Health check
- `POST /query` - Single query (no conversation history)
- `POST /chat` - Multi-turn conversation
- `POST /transcribe` - Speech-to-text
- `POST /speak` - Text-to-speech

## 🧪 Testing

cd backend
python test_backend.py

text

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI
- **LLM**: Google Gemini 2.5 Flash
- **Embeddings**: HuggingFace (sentence-transformers)
- **Vector DB**: ChromaDB
- **RAG**: LangChain
- **STT**: SpeechRecognition (Google Web Speech API)
- **TTS**: pyttsx3 (offline)

### Frontend
- **HTML5/CSS3/JavaScript**
- **Web Speech API** (STT)
- **Web Speech Synthesis API** (TTS)
- **Nginx** (production)

### DevOps
- **Docker & Docker Compose**
- **AWS EC2** deployment ready

## 📖 Usage

1. **Open frontend** in browser
2. **Click microphone button** 🎤
3. **Speak your question** (e.g., "What is Python?")
4. **Watch mascot listen** → think → respond → speak!

## 🎨 Mascot Emotions

The mascot shows different emotions based on response:
- 😊 **Happy** - Positive feedback, correct answers
- 🤔 **Thinking** - Analyzing, considering
- 🎓 **Explaining** - Teaching, clarifying concepts
- 😕 **Confused** - Uncertain, needs clarification
- 😐 **Neutral** - Standard responses

## 📝 Customization

### Add Training Documents

Add `.txt` files to `backend/data/`:

echo "Your educational content here" > backend/data/my_topic.txt

Delete vector DB to rebuild
rm -rf backend/chroma_db

Restart backend
python backend/app.py

text

### Configure Settings

Edit `backend/config.py` or `.env`:

GEMINI_MODEL=gemini-2.5-flash
STT_LANGUAGE=en-US
TTS_LANGUAGE=en

text

## 🔒 Security

- ⚠️ **Never commit `.env` file** (contains API key)
- ⚠️ **Use environment variables** for sensitive data
- ✅ **CORS configured** for security
- ✅ **Input validation** with Pydantic

## 🐛 Troubleshooting

### Backend Issues

Check if port 8000 is in use
netstat -ano | findstr :8000

View logs
python app.py # Watch console output

text

### Frontend Issues

Check browser console (F12)
Ensure backend is running at http://localhost:8000
Verify CORS is enabled
text

### Docker Issues

View logs
docker-compose logs backend
docker-compose logs frontend

Rebuild
docker-compose down
docker-compose up --build

text

## 📄 License

MIT License - feel free to use for learning and development

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 👨‍💻 Author

Your Name - [@yourhandle](https://github.com/yourusername)

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com)
- Powered by [Google Gemini](https://ai.google.dev)
- Embeddings by [HuggingFace](https://huggingface.co)
- Vector DB by [Chroma](https://www.trychroma.com)

## 📧 Contact

For questions or support, open an issue or reach out at: your.email@example.com

---

**⭐ Star this repo if you find it helpful!**