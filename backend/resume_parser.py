# backend/resume_parser.py
import PyPDF2
from docx import Document
import io

def parse_resume(file_stream, file_type):
    text = ""
    if file_type == 'pdf':
        reader = PyPDF2.PdfReader(file_stream)
        for page in reader.pages:
            text += page.extract_text() or "" # Handle empty page text
    elif file_type == 'docx':
        document = Document(file_stream)
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"
    return text.strip() # Remove leading/trailing whitespace