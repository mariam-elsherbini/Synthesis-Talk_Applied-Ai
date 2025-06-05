from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from llm_router import chat
from document_tools import extract_text_from_pdf, summarize_text
from web_tools import search_web
from notes_tools import add_note, list_notes
from explanation_tools import explain_concept
from reasoning import chain_of_thought
from export_tools import export_to_pdf
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_endpoint(payload: dict):
    response = chat(payload["messages"])
    return response

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    with open(f"uploaded_{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    text = extract_text_from_pdf(f"uploaded_{file.filename}")
    summary = summarize_text(text, chat)
    return {"summary": summary}

@app.get("/search")
async def web_search(query: str):
    return search_web(query)

@app.post("/note")
async def save_note(payload: dict):
    return add_note(payload["topic"], payload["content"])

@app.get("/notes")
async def get_notes():
    return list_notes()

@app.get("/explain")
async def explain(query: str):
    return {"explanation": explain_concept(query)}

@app.post("/reason")
async def reasoning(payload: dict):
    result = chain_of_thought(payload["prompt"])
    return {"result": result}

@app.post("/export")
async def export(payload: dict):
    return export_to_pdf(payload["filename"], payload["content"])