import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

model_server = os.getenv("MODEL_SERVER", "GROQ").upper()

if model_server == "GROQ":
    API_KEY = os.getenv("GROQ_API_KEY")
    BASE_URL = os.getenv("GROQ_BASE_URL")
    LLM_MODEL = os.getenv("GROQ_MODEL")
elif model_server == "NGU":
    API_KEY = os.getenv("NGU_API_KEY")
    BASE_URL = os.getenv("NGU_BASE_URL")
    LLM_MODEL = os.getenv("NGU_MODEL")
else:
    raise ValueError("Unsupported MODEL_SERVER")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def chat(messages):
    return client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages
    )