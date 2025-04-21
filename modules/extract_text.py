import fitz
import docx
import os
import requests


def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_doc(file_path):
    try:
        import textract
        return textract.process(file_path).decode("utf-8")
    except ImportError:
        raise ImportError("To handle .doc files, please install textract: pip install textract")
    except Exception as e:
        raise ValueError(f"Failed to extract text from .doc file: {str(e)}")

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def get_text(file_path, original_filename=None):
    filename = original_filename or file_path
    extension = os.path.splitext(filename)[-1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)
    elif extension == ".docx":
        return extract_text_from_docx(file_path)
    elif extension == ".doc":
        return extract_text_from_doc(file_path)
    elif extension == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")



def get_stackoverflow_link(topic, api_key):
 

    query = f"{topic} site:stackoverflow.com"
    url = f"https://serpapi.com/search.json?q={query}&api_key={api_key}"

    response = requests.get(url)
    results = response.json().get("organic_results", [])

    for res in results:
        link = res.get("link")
        if "stackoverflow.com" in link:
            return {
                "title": res.get("title"),
                "link": link
            }

    return None  # No Stack Overflow link found
