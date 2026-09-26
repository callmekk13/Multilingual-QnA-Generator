
from pathlib import Path

import fitz
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    text_parts = []

    with fitz.open(file_path) as pdf:
        for page in pdf:
            text_parts.append(page.get_text())

    return "\n".join(text_parts)


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""
    document = Document(file_path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


def extract_text_from_txt(file_path: str) -> str:
    """Read text from a TXT file."""
    return Path(file_path).read_text(encoding="utf-8")


def extract_text(file_path: str) -> str:
    """
    Extract text from PDF, DOCX, or TXT.

    Parameters
    ----------
    file_path : str
        Path to the input document.

    Returns
    -------
    str
        Extracted document text.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format: {extension}. "
            f"Supported formats: {SUPPORTED_EXTENSIONS}"
        )

    if extension == ".pdf":
        text = extract_text_from_pdf(str(path))

    elif extension == ".docx":
        text = extract_text_from_docx(str(path))

    elif extension == ".txt":
        text = extract_text_from_txt(str(path))

    else:
        raise ValueError(f"Unsupported file format: {extension}")

    if not text.strip():
        raise ValueError("The document contains no extractable text.")

    return text
