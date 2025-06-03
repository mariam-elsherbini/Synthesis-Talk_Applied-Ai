from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import shutil
import json
import logging
from datetime import datetime

# Import your LLM integration
from llm_client import SynthesisTalkLLM

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SynthesisTalk API",
    description="Backend API for SynthesisTalk - Collaborative Research Assistant",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global LLM instance (in production, use dependency injection)
llm_instance = None

def get_llm():
    """Get or create LLM instance"""
    global llm_instance
    if llm_instance is None:
        llm_instance = SynthesisTalkLLM()
    return llm_instance

# Pydantic models for request/response validation
class ChatRequest(BaseModel):
    message: str
    use_tools: bool = True
    reasoning_type: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    tool_results: List[Dict[str, Any]] = []
    reasoning_type: Optional[str] = None
    context: Dict[str, Any] = {}
    session_id: Optional[str] = None

class DocumentAnalysisRequest(BaseModel):
    analysis_type: str = "summary"

class DocumentAnalysisResponse(BaseModel):
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class NoteRequest(BaseModel):
    title: str
    content: str
    tags: List[str] = []

class NoteResponse(BaseModel):
    success: bool
    note: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Session management (simple in-memory storage)
sessions = {}

def get_session_llm(session_id: str) -> SynthesisTalkLLM:
    """Get or create LLM instance for a specific session"""
    if session_id not in sessions:
        sessions[session_id] = SynthesisTalkLLM()
    return sessions[session_id]

# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "SynthesisTalk API is running", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        llm = get_llm()
        return {
            "status": "healthy",
            "model_server": llm.model_server,
            "model": llm.model,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        # Get LLM instance for session
        if request.session_id:
            llm = get_session_llm(request.session_id)
        else:
            llm = get_llm()
        
        # Process chat request
        result = llm.chat(
            user_message=request.message,
            use_tools=request.use_tools,
            reasoning_type=request.reasoning_type
        )
        
        return ChatResponse(
            response=result["response"],
            tool_results=result.get("tool_results", []),
            reasoning_type=result.get("reasoning_type"),
            context=result.get("context", {}),
            session_id=request.session_id
        )
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    session_id: Optional[str] = Form(None)
):
    """Upload and process a document"""
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.txt']
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save uploaded file
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get LLM instance
        if session_id:
            llm = get_session_llm(session_id)
        else:
            llm = get_llm()
        
        # Analyze the document
        analysis_result = llm.analyze_document(file_path, "summary")
        
        return {
            "filename": file.filename,
            "file_path": file_path,
            "analysis": analysis_result,
            "session_id": session_id
        }
        
    except Exception as e:
        logger.error(f"Document upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-document/{filename}", response_model=DocumentAnalysisResponse)
async def analyze_document(
    filename: str,
    request: DocumentAnalysisRequest,
    session_id: Optional[str] = None
):
    """Analyze an uploaded document with specified analysis type"""
    try:
        file_path = os.path.join("uploads", filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {filename}")
        
        # Get LLM instance
        if session_id:
            llm = get_session_llm(session_id)
        else:
            llm = get_llm()
        
        # Perform analysis
        result = llm.analyze_document(file_path, request.analysis_type)
        
        return DocumentAnalysisResponse(**result)
        
    except Exception as e:
        logger.error(f"Document analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save-note", response_model=NoteResponse)
async def save_note(request: NoteRequest):
    """Save a research note"""
    try:
        llm = get_llm()
        result = llm.tool_manager.execute_tool("save_note", {
            "title": request.title,
            "content": request.content,
            "tags": request.tags
        })
        
        return NoteResponse(
            success=result.success,
            note=result.data if result.success else None,
            error=result.error
        )
        
    except Exception as e:
        logger.error(f"Note saving error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes")
async def get_notes():
    """Get all saved research notes"""
    try:
        llm = get_llm()
        notes = llm.export_research_notes()
        return {"notes": notes}
        
    except Exception as e:
        logger.error(f"Notes retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversation-history/{session_id}")
async def get_conversation_history(session_id: str):
    """Get conversation history for a session"""
    try:
        if session_id not in sessions:
            return {"messages": [], "context": {}}
        
        llm = sessions[session_id]
        return {
            "messages": llm.conversation_manager.messages,
            "context": llm.conversation_manager.context
        }
        
    except Exception as e:
        logger.error(f"Conversation history error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/conversation-history/{session_id}")
async def clear_conversation_history(session_id: str):
    """Clear conversation history for a session"""
    try:
        if session_id in sessions:
            sessions[session_id].clear_conversation()
        
        return {"message": f"Conversation history cleared for session {session_id}"}
        
    except Exception as e:
        logger.error(f"Clear conversation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools")
async def get_available_tools():
    """Get list of available tools"""
    try:
        llm = get_llm()
        tools = llm.tool_manager.get_tool_definitions()
        return {"tools": tools}
        
    except Exception as e:
        logger.error(f"Tools retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def web_search(query: str, num_results: int = 5, session_id: Optional[str] = None):
    """Perform web search"""
    try:
        # Get LLM instance
        if session_id:
            llm = get_session_llm(session_id)
        else:
            llm = get_llm()
        
        # Execute search tool
        result = llm.tool_manager.execute_tool("web_search", {
            "query": query,
            "num_results": num_results
        })
        
        return {
            "success": result.success,
            "results": result.data if result.success else [],
            "error": result.error,
            "metadata": result.metadata
        }
        
    except Exception as e:
        logger.error(f"Web search error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions")
async def get_active_sessions():
    """Get list of active sessions"""
    return {
        "sessions": list(sessions.keys()),
        "count": len(sessions)
    }

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a specific session"""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": f"Session {session_id} deleted"}
    else:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

@app.get("/files")
async def list_uploaded_files():
    """List all uploaded files"""
    try:
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            return {"files": []}
        
        files = []
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                stat = os.stat(file_path)
                files.append({
                    "filename": filename,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        
        return {"files": files}
        
    except Exception as e:
        logger.error(f"File listing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/files/{filename}")
async def delete_file(filename: str):
    """Delete an uploaded file"""
    try:
        file_path = os.path.join("uploads", filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"message": f"File {filename} deleted"}
        else:
            raise HTTPException(status_code=404, detail=f"File {filename} not found")
            
    except Exception as e:
        logger.error(f"File deletion error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return HTTPException(status_code=500, detail="Internal server error")

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("SynthesisTalk API starting up...")
    
    # Create necessary directories
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("exports", exist_ok=True)
    
    # Initialize LLM to check configuration
    try:
        llm = get_llm()
        logger.info(f"LLM initialized with model: {llm.model}")
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {str(e)}")
        raise e

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("SynthesisTalk API shutting down...")
    
    # Clear sessions
    global sessions
    sessions.clear()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)