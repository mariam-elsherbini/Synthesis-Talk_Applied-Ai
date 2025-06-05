notes_db = []

def add_note(topic, content):
    notes_db.append({"topic": topic, "content": content})
    return {"message": "Note saved."}

def list_notes():
    return notes_db