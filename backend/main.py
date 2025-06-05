from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_router import chat
from document_tools import extract_text_from_pdf, summarize_text, create_detailed_analysis, create_bullet_summary
from web_tools import search_web
from notes_tools import add_note, list_notes
from explanation_tools import explain_concept
from reasoning import chain_of_thought
from export_tools import export_to_pdf
import shutil
import os
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request bodies
class ChatRequest(BaseModel):
    messages: list

class WebSearchRequest(BaseModel):
    query: str

class NoteRequest(BaseModel):
    note: str

class ReasoningRequest(BaseModel):
    prompt: str

class ExportRequest(BaseModel):
    filename: str
    content: str

@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    response = chat(payload.messages)
    return {"response": response.choices[0].message.content}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...), 
    summary_type: str = Form("standard")
):
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/uploaded_{file.filename}"
    
    try:
        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract text from PDF
        text = extract_text_from_pdf(file_path)
        
        # Generate summary based on type
        if summary_type == "bullet":
            summary = create_bullet_summary(text, chat)
        elif summary_type == "detailed":
            summary = create_detailed_analysis(text, chat)
        else:  # standard
            summary = summarize_text(text, chat)
        
        # Clean up the uploaded file
        os.remove(file_path)
        
        return {"summary": summary, "summary_type": summary_type}
        
    except Exception as e:
        # Clean up file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
        return {"error": f"Failed to process file: {str(e)}"}

@app.post("/websearch")
async def web_search_endpoint(payload: WebSearchRequest):
    try:
        results = search_web(payload.query)
        # Create a simple response from search results
        response = f"Found {len(results)} results for '{payload.query}':\n\n"
        for i, result in enumerate(results, 1):
            response += f"**{i}. {result.get('title', 'No title')}**\n"
            response += f"{result.get('snippet', 'No description')}\n"
            if result.get('link'):
                response += f"[Read more]({result.get('link')})\n\n"
            else:
                response += "\n"
        return {"response": response}
    except Exception as e:
        return {"response": f"Search failed: {str(e)}"}

@app.post("/notes")
async def save_note(payload: NoteRequest):
    result = add_note("general", payload.note)
    return result

@app.get("/notes")
async def get_notes():
    return {"notes": list_notes()}

@app.get("/explain")
async def explain(query: str):
    return {"explanation": explain_concept(query)}

@app.post("/reason")
async def reasoning(payload: ReasoningRequest):
    result = chain_of_thought(payload.prompt)
    return {"result": result}

@app.post("/export")
async def export(payload: ExportRequest):
    return export_to_pdf(payload.filename, payload.content)

@app.get("/")
async def root():
    return {"message": "SynthesiTalk API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running properly"}