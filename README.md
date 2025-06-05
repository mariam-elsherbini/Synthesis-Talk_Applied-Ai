# SynthesisTalk 🤖💬

An AI-powered research assistant that combines document analysis, web search, and intelligent conversation to help users explore complex topics through an intuitive interface.

## 🎯 Project Overview

SynthesisTalk is a comprehensive research platform built for the CSAI 422 - Applied Generative AI course at New Giza University. It demonstrates how modern Large Language Models can be integrated with custom tools to create powerful research workflows.

### Key Features

- **📄 Document Analysis**: Upload and analyze PDF documents with AI-powered summarization
- **🔍 Web Search Integration**: Search the web and get AI-synthesized results
- **💭 Intelligent Chat**: Multi-turn conversations with context awareness
- **📝 Note-Taking System**: Organize and save research insights
- **🧠 Advanced Reasoning**: Chain-of-thought and ReAct reasoning patterns
- **📊 Export Capabilities**: Export findings to PDF format

## 🏗️ Architecture

### Three-Tier Architecture

1. **Frontend** - React.js with Vite + TailwindCSS
2. **Backend** - FastAPI with tool orchestration
3. **LLM Integration** - Unified module supporting multiple providers (NGU, Groq)

```
project-root/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── llm_router.py          # LLM provider routing
│   ├── document_tools.py      # PDF processing & summarization
│   ├── web_tools.py           # Web search functionality
│   ├── notes_tools.py         # Note management
│   ├── explanation_tools.py   # Concept explanations
│   ├── reasoning.py           # Chain-of-thought reasoning
│   ├── export_tools.py        # PDF export functionality
│   ├── utils.py               # Utility functions
│   └── .env                   # Environment configuration
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main application component
│   │   ├── main.jsx          # React entry point
│   │   └── index.css         # Tailwind styles
│   ├── package.json
│   └── vite.config.js
└── requirements.txt
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- macOS Silicon (optimized for, but works on other platforms)

### Installation

1. **Clone and Setup Environment**

```bash
mkdir synthesistalk && cd synthesistalk
python3 -m venv venv311
source venv311/bin/activate  # On Windows: venv311\Scripts\activate
```

2. **Install Backend Dependencies**

```bash
mkdir backend && cd backend
pip install -r requirements.txt
```

3. **Configure Environment Variables**
   Create `backend/.env`:

```ini
NGU_API_KEY="your-ngu-api-key"
NGU_BASE_URL="https://ngullama.femtoid.com/v1"
NGU_MODEL="qwen2.5-coder:7b"

GROQ_API_KEY="your_groq_key_here"
GROQ_BASE_URL="https://api.groq.com/openai/v1"
GROQ_MODEL="llama-3.3-70b-versatile"

MODEL_SERVER="NGU"  # or "GROQ"
SERPAPI_KEY=""      # Optional for web search
```

4. **Setup Frontend**

```bash
cd ../frontend
npm install
```

### Running the Application

1. **Start Backend Server**

```bash
cd backend
uvicorn main:app --reload --port 8000
```

2. **Start Frontend Development Server**

```bash
cd frontend
npm run dev
```

3. **Access Application**
   Open http://localhost:5173 in your browser

## 🛠️ Core Components

### Backend API Endpoints

- `POST /chat` - Main chat interface
- `POST /upload` - Document upload and analysis
- `POST /websearch` - Web search functionality
- `POST /notes` - Save research notes
- `GET /notes` - Retrieve saved notes
- `GET /explain` - Get concept explanations
- `POST /reason` - Chain-of-thought reasoning
- `POST /export` - Export to PDF

### Frontend Features

- **Responsive Design**: Built with TailwindCSS for modern UI/UX
- **Real-time Chat**: Instant messaging with AI assistant
- **File Upload**: Drag-and-drop PDF analysis
- **Multi-tool Integration**: Seamless access to all research tools
- **State Management**: Efficient React state handling

## 🧠 LLM Integration

### Multi-Provider Support

- **NGU (NguLlama)**: Local/custom LLM deployment
- **Groq**: High-performance inference
- **OpenAI-compatible APIs**: Easy extension to other providers

### Advanced Reasoning

- **Chain-of-Thought**: Step-by-step problem solving
- **ReAct Pattern**: Reasoning and acting in iterative loops
- **Context Management**: Maintains conversation history

## 📚 Research Tools

### 1. Document Analysis Tool

- Extracts text from PDF files using PyMuPDF
- Generates structured summaries with markdown formatting
- Creates detailed analysis with multiple sections
- Handles large documents with content chunking

### 2. Web Search Tool

- Integrates with SerpAPI for real-time search
- Provides mock results for testing without API key
- Synthesizes search results into coherent responses
- Supports error handling and fallbacks

### 3. Note-Taking System

- In-memory note storage with topic organization
- RESTful API for note management
- Integration with chat for automatic note generation
- Export capabilities for research documentation

### 4. Explanation Tool

- Multi-level explanations (basic, intermediate, advanced)
- Context-aware concept clarification
- Educational content generation
- Adaptive complexity based on user needs

## 🔧 Development

### Code Structure

**Backend (Python/FastAPI)**

- Modular design with separation of concerns
- Tool-based architecture for easy extension
- Robust error handling and logging
- CORS-enabled for frontend integration

**Frontend (React/JavaScript)**

- Component-based architecture
- Hooks for state management
- Axios for API communication
- TailwindCSS for styling

### Key Dependencies

**Backend:**

```
fastapi>=0.68.0
uvicorn>=0.15.0
python-multipart>=0.0.5
pydantic>=1.8.0
python-dotenv>=0.19.0
openai>=1.0.0
requests>=2.26.0
PyMuPDF>=1.20.0
reportlab>=3.6.0
```

**Frontend:**

```
react>=18.2.0
react-dom>=18.2.0
axios>=1.5.0
vite>=5.2.0
tailwindcss>=3.3.2
```

## 🧪 Testing

### Backend Testing

```bash
cd backend
# Start the server
uvicorn main:app --reload

# Test endpoints
curl -X GET "http://localhost:8000/"
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"messages": [{"role": "user", "content": "Hello"}]}'
```

### Frontend Testing

```bash
cd frontend
npm run dev
# Open http://localhost:5173 and test UI components
```

## 🚀 Deployment

### Local Deployment

The application is configured for local development but can be deployed to cloud platforms.

### Recommended Production Setup

1. **Containerization**: Use Docker for consistent deployment
2. **Cloud Hosting**: Deploy on AWS, GCP, or Azure
3. **Database**: Replace in-memory storage with PostgreSQL/MongoDB
4. **Load Balancing**: Use Nginx for production traffic
5. **SSL/HTTPS**: Implement secure connections

## 🤝 Contributing

### Development Team

- **Mohamed Ayman** (202201208)
- **Hana Ayman** (202101348)
- **Mariam ElSherbini** (202202568)

### Contributing Guidelines

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is developed for educational purposes as part of the CSAI 422 course at New Giza University.

## 🔮 Future Enhancements

### Performance Optimizations

- Tool parallelization for faster response times
- Caching mechanisms for frequently accessed data
- Database integration for persistent storage

### User Experience

- Multi-topic research threads
- Dark mode support
- Advanced file management
- Collaborative features

### Technical Improvements

- Vector database integration for semantic search
- Fine-tuned models for domain-specific tasks
- Advanced export formats (Word, LaTeX)
- Real-time collaboration features

## 📞 Support

For questions or issues related to this project, please refer to the course materials or contact the development team.

---

**SynthesisTalk** - Empowering research through AI-driven synthesis and conversation.
