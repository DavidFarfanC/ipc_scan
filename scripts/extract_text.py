import os
import fitz  # PyMuPDF
import docx
import pandas as pd

def extract_text_from_pdf(file_path):
    """
    Extrae texto de un archivo PDF.
    """
    text = ""
    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
    except Exception as e:
        print(f"Error al leer {file_path}: {e}")
    return text

def extract_text_from_docx(file_path):
    """
    Extrae texto de un archivo DOCX.
    """
    text = ""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"Error al leer {file_path}: {e}")
    return text

def extract_text_from_xlsx(file_path):
    """
    Extrae texto de un archivo XLSX.
    """
    text = ""
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        text = df.to_string()
    except Exception as e:
        print(f"Error al leer {file_path}: {e}")
    return text

def extract_text(file_path):
    """
    Identifica el tipo de archivo y extrae el texto en consecuencia.
    """
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".xlsx":
        return extract_text_from_xlsx(file_path)
    elif ext == ".txt":
        return open(file_path, "r", encoding="utf-8", errors="ignore").read()
    return None
