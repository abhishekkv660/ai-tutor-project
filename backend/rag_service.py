# rag_service.py
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings  # FREE OFFLINE
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
import os
import logging
from typing import Dict, Tuple
from config import settings

logger = logging.getLogger(__name__)

class RAGService:
    """RAG Service using Gemini LLM and FREE HuggingFace Embeddings"""
    
    def __init__(self):
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.chat_memories: Dict[str, ConversationBufferMemory] = {}
        self._initialize()
    
    def _initialize(self):
        """Initialize RAG components"""
        try:
            logger.info("🚀 Initializing RAG service...")
            
            # Initialize Gemini LLM (for text generation only)
            self.llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                temperature=settings.GEMINI_TEMPERATURE,
                max_output_tokens=settings.GEMINI_MAX_TOKENS,
                google_api_key=settings.GOOGLE_API_KEY
            )
            logger.info(f"✅ Gemini LLM: {settings.GEMINI_MODEL}")
            
            # Initialize FREE HuggingFace Embeddings (OFFLINE)
            logger.info("📥 Loading FREE HuggingFace embeddings (first time may take a minute)...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},  # Use CPU (no GPU needed)
                encode_kwargs={'normalize_embeddings': True}
            )
            logger.info("✅ FREE HuggingFace Embeddings initialized (OFFLINE)")
            
            # Load vector store
            self._load_vector_store()
            logger.info("✅ RAG service ready!")
        
        except Exception as e:
            logger.error(f"❌ RAG initialization failed: {e}")
            raise
    
    def _load_vector_store(self):
        """Load or create vector store"""
        persist_dir = settings.VECTOR_DB_PATH
        
        if os.path.exists(persist_dir):
            logger.info("📂 Loading existing vector store...")
            self.vectorstore = Chroma(
                persist_directory=persist_dir,
                embedding_function=self.embeddings
            )
        else:
            logger.info("🆕 Creating new vector store...")
            self._create_vector_store()
    
    def _create_vector_store(self):
        """Create vector store from documents"""
        data_dir = settings.DATA_DIR
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logger.info(f"📁 Created data directory: {data_dir}")
            self._create_sample_documents(data_dir)
        
        try:
            # Load documents
            loader = DirectoryLoader(
                data_dir,
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'}
            )
            documents = loader.load()
            
            if not documents:
                raise ValueError("No documents found in data directory")
            
            logger.info(f"📚 Loaded {len(documents)} documents")
            
            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP
            )
            splits = text_splitter.split_documents(documents)
            logger.info(f"✂️ Split into {len(splits)} chunks")
            
            # Create vector store (this will use FREE local embeddings now!)
            logger.info("🔄 Creating embeddings (this may take a minute)...")
            self.vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory=settings.VECTOR_DB_PATH
            )
            logger.info("✅ Vector store created and persisted")
        
        except Exception as e:
            logger.error(f"❌ Error creating vector store: {e}")
            raise
    
    def _create_sample_documents(self, data_dir: str):
        """Create sample training documents"""
        samples = {
            "python_basics.txt": """
Python Programming Basics

Python is a high-level, interpreted programming language known for its simplicity and readability.
It was created by Guido van Rossum and first released in 1991.

Key Features:
- Easy to learn and use
- Interpreted language
- Dynamically typed
- Object-oriented
- Extensive standard library

Python is widely used in:
- Web development (Django, Flask)
- Data science and analysis
- Machine learning and AI
- Automation and scripting
- Scientific computing
            """,
            
            "machine_learning.txt": """
Machine Learning Fundamentals

Machine Learning is a subset of artificial intelligence that enables systems to learn from data.

Types of Machine Learning:
1. Supervised Learning: Uses labeled training data
2. Unsupervised Learning: Uses unlabeled data
3. Reinforcement Learning: Learns through interaction

Common ML Algorithms:
- Linear Regression
- Decision Trees
- Random Forests
- Neural Networks
            """,
            
            "data_structures.txt": """
Data Structures and Algorithms

Data structures are ways of organizing and storing data efficiently.

Common Data Structures:
1. Arrays: Fixed-size collection
2. Linked Lists: Dynamic size
3. Stacks: LIFO (Last In First Out)
4. Queues: FIFO (First In First Out)
5. Trees: Hierarchical structure
6. Graphs: Nodes and edges
            """
        }
        
        for filename, content in samples.items():
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content.strip())
        
        logger.info(f"✅ Created {len(samples)} sample documents")
    
    def query(self, question: str) -> Tuple[str, list]:
        """Answer a single query"""
        try:
            retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": settings.RETRIEVAL_K}
            )
            docs = retriever.get_relevant_documents(question)
            context = "\n\n".join([doc.page_content for doc in docs])
            
            prompt = f"""You are a friendly AI tutor. Answer clearly and concisely.

Context: {context}

Question: {question}

Answer:"""
            
            response = self.llm.invoke(prompt)
            return response.content, docs
        
        except Exception as e:
            logger.error(f"Query error: {e}")
            raise
    
    def chat(self, question: str, session_id: str = "default") -> Tuple[str, list]:
        """Multi-turn conversation"""
        try:
            if session_id not in self.chat_memories:
                self.chat_memories[session_id] = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True,
                    output_key="answer"
                )
            
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(
                    search_kwargs={"k": settings.RETRIEVAL_K}
                ),
                memory=self.chat_memories[session_id],
                return_source_documents=True
            )
            
            result = qa_chain({"question": question})
            return result["answer"], result.get("source_documents", [])
        
        except Exception as e:
            logger.error(f"Chat error: {e}")
            raise

rag_service = RAGService()
