from llm_router import chat

def chain_of_thought(prompt):
    messages = [
        {"role": "system", "content": "Use chain-of-thought reasoning to solve problems step-by-step."},
        {"role": "user", "content": prompt}
    ]
    return chat(messages).choices[0].message.content