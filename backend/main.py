from fastapi import FastAPI
from pydantic import BaseModel
from llm_client import ask_llm

app = FastAPI()

class UserMessage(BaseModel):
    message: str

@app.post("/ask")
async def ask(user_msg: UserMessage):
    response = ask_llm(user_msg.message)
    return {"response": response}
