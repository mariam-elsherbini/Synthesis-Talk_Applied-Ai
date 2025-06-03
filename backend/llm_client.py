import os
from dotenv import load_dotenv
from openai import OpenAI

# Load env vars
load_dotenv()

model_server = os.getenv('MODEL_SERVER', 'GROQ').upper()

if model_server == "GROQ":
    API_KEY = os.getenv('GROQ_API_KEY')
    BASE_URL = os.getenv('GROQ_BASE_URL')
    LLM_MODEL = os.getenv('GROQ_MODEL')
elif model_server == "NGU":
    API_KEY = os.getenv('NGU_API_KEY')
    BASE_URL = os.getenv('NGU_BASE_URL')
    LLM_MODEL = os.getenv('NGU_MODEL')
else:
    raise ValueError(f"Unsupported MODEL_SERVER: {model_server}")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

def ask_llm(user_message):
    messages = [
        {"role": "system", "content": "You are a helpful research assistant."},
        {"role": "user", "content": user_message}
    ]
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages
    )
    return response.choices[0].message.content
