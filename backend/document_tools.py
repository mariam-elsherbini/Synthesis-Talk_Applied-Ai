import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = "\n".join([page.get_text() for page in doc])
    doc.close()
    return text

def summarize_text(text, chat):
    messages = [
        {"role": "system", "content": """You are an expert at creating well-structured, readable summaries. 
        Create summaries with clear organization and proper markdown formatting:
        
        FORMATTING REQUIREMENTS:
        - Use ## for main headings and ### for subheadings
        - Create bullet points using - or * for key concepts
        - Use **bold** for important terms and concepts
        - Add line breaks between sections for readability
        - Structure content with clear hierarchy
        - Keep bullet points concise (1-2 lines each)
        - Group related concepts under appropriate headings
        - Use numbered lists (1., 2., 3.) for sequential information
        
        STRUCTURE:
        1. Start with a brief overview
        2. Organize content into logical sections with headings
        3. Use bullet points for key concepts within each section
        4. End with important takeaways or conclusions"""},
        
        {"role": "user", "content": f"""Please create a well-formatted, structured summary of the following document. 
        Use clear markdown formatting with headings, bullet points, and proper spacing to make it highly readable and organized:

        {text[:4000]}"""}  # Limit text length to avoid token limits
    ]
    return chat(messages).choices[0].message.content

def create_detailed_analysis(text, chat):
    """Create a more detailed analysis with multiple sections"""
    messages = [
        {"role": "system", "content": """You are a research analyst. Create a comprehensive, well-formatted analysis with these sections:
        
        ## Executive Summary
        Brief overview with key points in bullet format
        
        ## Key Themes & Topics  
        - Main themes as bullet points
        - Sub-themes indented
        
        ## Important Findings
        - Critical discoveries or insights
        - Supporting evidence
        
        ## Practical Applications
        - Real-world uses
        - Implementation considerations
        
        ## Conclusions
        - Final thoughts
        - Recommendations
        
        Use proper markdown formatting with headers, bullet points, bold text, and clear structure."""},
        {"role": "user", "content": f"Analyze this document and create a detailed, well-formatted report:\n\n{text[:4000]}"}
    ]
    return chat(messages).choices[0].message.content

def create_bullet_summary(text, chat):
    """Create a bullet-point focused summary"""
    messages = [
        {"role": "system", "content": """Create a summary that is primarily organized as bullet points:
        
        ## Document Summary
        
        ### Main Topics:
        - Topic 1
        - Topic 2
        - Topic 3
        
        ### Key Concepts:
        - **Concept 1**: Brief explanation
        - **Concept 2**: Brief explanation
        - **Concept 3**: Brief explanation
        
        ### Important Details:
        - Detail 1
        - Detail 2
        - Detail 3
        
        ### Takeaways:
        - Key takeaway 1
        - Key takeaway 2
        - Key takeaway 3
        
        Focus on clarity and organization through bullet points."""},
        {"role": "user", "content": f"Create a bullet-point summary of this document:\n\n{text[:4000]}"}
    ]
    return chat(messages).choices[0].message.content