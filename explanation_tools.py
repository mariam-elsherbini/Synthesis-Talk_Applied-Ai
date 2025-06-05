from llm_router import chat

def explain_concept(concept):
    messages = [
        {"role": "system", "content": "You are an expert educator."},
        {"role": "user", "content": f"Explain the concept: {concept}"}
    ]
    return chat(messages).choices[0].message.content