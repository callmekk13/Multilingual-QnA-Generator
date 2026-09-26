# cat > tests/test_text_processor.py <<'EOF'
from src.text_processor import clean_text, chunk_text


def test_clean_text():
    text = "Hello   world.\n\n\nThis is a test."
    result = clean_text(text)

    assert result == "Hello world.\n\nThis is a test."


def test_chunk_text():
    text = (
        "Artificial Intelligence is a branch of computer science. "
        "Machine learning is a subset of artificial intelligence."
    )

    chunks = chunk_text(text, max_chars=50)

    assert len(chunks) >= 1
    assert all(chunk.strip() for chunk in chunks)