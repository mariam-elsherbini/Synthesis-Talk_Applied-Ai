from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_to_pdf(filename, content):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    text = c.beginText(40, height - 40)
    for line in content.split('\n'):
        text.textLine(line)
    c.drawText(text)
    c.save()
    return {"message": f"PDF saved as {filename}"}