# cat > tests/test_document_loader.py <<'EOF'
from pathlib import Path

from src.document_loader import extract_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = PROJECT_ROOT / "input_documents"


def test_txt_loader():
    file_path = INPUT_DIR / "sample.txt"

    text = extract_text(str(file_path))

    assert text.strip()
    assert "Artificial Intelligence" in text


def test_docx_loader():
    file_path = INPUT_DIR / "sample.docx"

    text = extract_text(str(file_path))

    assert text.strip()


def test_pdf_loader():
    file_path = INPUT_DIR / "sample.pdf"

    text = extract_text(str(file_path))

    assert text.strip()