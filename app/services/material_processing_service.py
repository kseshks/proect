from pathlib import Path

from bs4 import BeautifulSoup
import requests
from pypdf import PdfReader

ALLOWED_EXTENSIONS = {".txt", ".pdf"}
MAX_FILE_SIZE_MB = 10


def validate_file(filename: str) -> None:
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Недопустимый тип файла")

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    parts = []

    for page in reader.pages:
        text = page.extract_text() or ""
        parts.append(text)

    return "\n".join(parts).strip()

def extract_text_from_file(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()

    if ext == ".txt":
        return extract_text_from_txt(file_path)

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)

    raise ValueError("Формат файла не поддерживается")

def extract_text_from_url(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(strip=True)
    return text