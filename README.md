# SynthesisTalk - LLM Integration Component

This is the LLM Integration component for the SynthesisTalk project, a collaborative research assistant that demonstrates conversational agency, tool usage, and advanced reasoning techniques.

## 🎯 Project Overview

SynthesisTalk is an intelligent research assistant that helps users explore complex topics through interactive conversation. This LLM integration component provides:

- **Conversational Agency**: Multi-turn conversations with context maintenance
- **Tool Integration**: Document analysis, web search, note-taking, and explanation tools
- **Advanced Reasoning**: Chain of Thought and ReAct reasoning techniques
- **Flexible Architecture**: Support for multiple LLM providers (NGU, GROQ, OpenAI-compatible APIs)

## 🏗️ Architecture

```
SynthesisTalk LLM Integration
├── llm_client.py          # Core LLM integration with tools and reasoning
├── main.py               # FastAPI backend server
├── test_llm.py           # Comprehensive test suite
├── requirements.txt      # Python dependencies
└── setup.sh             # Setup script
```

### Core Components

1. **SynthesisTalkLLM**: Main LLM integration class
2. **ToolManager**: Manages and executes various research tools
3. **ConversationManager**: Handles conversation history and context
4. **ReasoningEngine**: Implements Chain of Thought and ReAct reasoning
5. **FastAPI Backend**: RESTful API for frontend integration

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Make setup script executable and run it
chmod +x setup.sh
./setup.sh

# Or manual setup:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Your `.env` file should contain:

```env
MODEL_SERVER=NGU
NGU_API_KEY=ngu-y8PCtqZW9R
NGU_BASE_URL=https://ngullama.femtoid.com/v1
NGU_MODEL=qwen2.5-coder:7b
```

### 3. Test the Integration

```bash
# Activate virtual environment
source venv/bin/activate

# Run comprehensive tests
python test_llm.py
```

### 4. Start the Server

```bash
# Start FastAPI server
python main.py

# Or with uvicorn for development
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`

## 🔧 Usage Examples

### Basic LLM Interaction

```python
from llm_client import ask_llm

# Simple question
response = ask_llm("What is artificial intelligence?")
print(response)

# With reasoning
response = ask_llm(
    "What are the challenges of AI in healthcare?",
    reasoning_type="chain_of_thought"
)
```

### Advanced Features

```python
from llm_client import SynthesisTalkLLM

# Initialize LLM
llm = SynthesisTalkLLM()

# Multi-turn conversation with tools
response1 = llm.chat("I want to research renewable energy")
response2 = llm.chat("Can you analyze this document about solar panels?", use_tools=True)
response3 = llm.chat("What are the latest developments?", reasoning_type="react")

# Document analysis
result = llm.analyze_document("research_paper.pdf", "key_points")

# Get conversation history
history = llm.conversation_manager.messages
```

### API Usage

```bash
# Chat endpoint
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, I want to research AI in education",
    "use_tools": true,
    "reasoning_type": "chain_of_thought",
    "session_id": "research_session_1"
  }'

# Upload document
curl -X POST "http://localhost:8000/upload-document" \
  -F "file=@document.pdf" \
  -F "session_id=research_session_1"

# Save note
curl -X POST "http://localhost:8000/save-note" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Key Insight",
    "content": "AI can personalize learning experiences",
    "tags": ["AI", "education", "personalization"]
  }'
```

## 🛠️ Available Tools

### 1. Document Analysis Tool

- **Purpose**: Extract and analyze content from PDFs and text files
- **Capabilities**: Summary, key points extraction, detailed analysis
- **Usage**: Automatically triggered when documents are uploaded

### 2. Web Search Tool

- **Purpose**: Search for additional information on topics
- **Capabilities**: Returns relevant search results with snippets
- **Usage**: Activated when current knowledge needs supplementation

### 3. Note-Taking Tool

- **Purpose**: Save and organize important research findings
- **Capabilities**: Structured notes with tags and timestamps
- **Usage**: Automatically saves insights or manually triggered

### 4. Explanation Tool

- **Purpose**: Provide detailed explanations of concepts
- **Capabilities**: Multi-level explanations (basic, intermediate, advanced)
- **Usage**: Triggered when clarification is needed

## 🧠 Reasoning Techniques

### Chain of Thought (CoT)

Breaks down complex problems into step-by-step reasoning:

```python
response = llm.chat(
    "How can AI improve healthcare outcomes?",
    reasoning_type="chain_of_thought"
)
```

### ReAct (Reasoning + Acting)

Combines reasoning with tool usage in iterative cycles:

```python
response = llm.chat(
    "Research the latest developments in quantum computing",
    reasoning_type="react"
)
```

## 📡 API Endpoints

| Endpoint                             | Method | Description                           |
| ------------------------------------ | ------ | ------------------------------------- |
| `/chat`                              | POST   | Main chat interface with tool support |
| `/upload-document`                   | POST   | Upload and analyze documents          |
| `/save-note`                         | POST   | Save research notes                   |
| `/notes`                             | GET    | Retrieve all saved notes              |
| `/search`                            | POST   | Perform web search                    |
| `/conversation-history/{session_id}` | GET    | Get conversation history              |
| `/tools`                             | GET    | List available tools                  |
| `/health`                            | GET    | Health check endpoint                 |

## 🔍 Testing

The project includes comprehensive tests:

```bash
# Run all tests
python test_llm.py

# Tests include:
# ✅ Environment configuration
# ✅ Basic LLM functionality
# ✅ Advanced reasoning techniques
# ✅ Tool integration
# ✅ Document analysis
# ✅ Conversation flow
# ✅ API compatibility
```

## 🎛️ Configuration Options

### LLM Provider Configuration

Switch between providers by changing `MODEL_SERVER` in `.env`:

```env
# NGU (Current)
MODEL_SERVER=NGU
NGU_API_KEY=your_key
NGU_BASE_URL=https://ngullama.femtoid.com/v1
NGU_MODEL=qwen2.5-coder:7b

# GROQ Alternative
MODEL_SERVER=GROQ
GROQ_API_KEY=your_key
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=llama-3.1-70b-versatile
```

### Conversation Settings

```python
# Adjust conversation history length
conversation_manager = ConversationManager(max_history=50)

# Enable/disable specific tools
llm.tool_manager.tools.pop('web_search')  # Disable web search
```

## 📊 Performance Considerations

- **Context Management**: Automatic conversation trimming to prevent token overflow
- **Tool Caching**: Results cached to avoid redundant API calls
- **Error Handling**: Comprehensive error handling with fallback mechanisms
- **Session Management**: Isolated conversations per session

## 🔒 Security Notes

- API keys are loaded from environment variables
- File uploads are validated and sandboxed
- Input sanitization prevents injection attacks
- Session isolation ensures data privacy

## 🚧 Development Notes

### Adding New Tools

```python
def my_custom_tool(param1: str, param2: int) -> ToolResult:
    # Tool implementation
    return ToolResult(success=True, data="result")

# Register the tool
llm.tool_manager.register_tool(
    name="my_tool",
    func=my_custom_tool,
    description="Description of what the tool does",
    parameters={
        "type": "object",
        "properties": {
            "param1": {"type": "string"},
            "param2": {"type": "integer"}
        },
        "required": ["param1", "param2"]
    }
)
```

### Custom Reasoning Techniques

```python
class CustomReasoningEngine(ReasoningEngine):
    @staticmethod
    def my_reasoning_prompt(question: str) -> str:
        return f"Custom reasoning approach for: {question}"
```

## 📝 Project Requirements Fulfillment

This implementation satisfies all LLM Integration requirements:

- ✅ **LLM API Integration**: NGU/GROQ API integration with OpenAI-compatible interface
- ✅ **Tool Management**: Four different tool types implemented
- ✅ **Reasoning Techniques**: Chain of Thought and ReAct implemented
- ✅ **Workflow Orchestration**: Seamless tool and reasoning coordination
- ✅ **Self-Correction**: Error handling and retry mechanisms
- ✅ **Conversation Context**: Multi-turn conversation with context maintenance

## 🤝 Team Integration

This LLM component integrates with:

- **Frontend**: RESTful API with comprehensive endpoints
- **Backend**: FastAPI server with proper error handling
- **Database**: JSON-based storage (easily upgradeable to proper DB)

## 📈 Future Enhancements

- [ ] Add vector database for document embeddings
- [ ] Implement real web search API integration
- [ ] Add streaming responses for real-time chat
- [ ] Implement conversation summarization
- [ ] Add multi-modal support (images, audio)
- [ ] Implement advanced caching strategies

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure `.env` file is properly configured
2. **Import Errors**: Activate virtual environment with `source venv/bin/activate`
3. **Tool Failures**: Check file permissions and network connectivity
4. **Memory Issues**: Reduce conversation history length
