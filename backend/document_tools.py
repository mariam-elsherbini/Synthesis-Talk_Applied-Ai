import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = "\n".join([page.get_text() for page in doc])
    return text

def summarize_text(text, chat):
    messages = [
        {"role": "system", "content": "You summarize research documents."},
        {"role": "user", "content": f"Summarize the following:\n{text}"}
    ]
    return chat(messages).choices[0].message.content