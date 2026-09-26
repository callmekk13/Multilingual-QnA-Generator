# cat > tests/test_pipeline.py <<'EOF'
from src.pipeline import remove_duplicate_qna


def test_remove_duplicate_qna():
    qna = [
        {
            "question": "What is AI?",
            "answer": "Artificial Intelligence."
        },
        {
            "question": "What is AI?",
            "answer": "Artificial Intelligence."
        },
        {
            "question": "What is Machine Learning?",
            "answer": "A subset of AI."
        },
    ]

    result = remove_duplicate_qna(qna)

    assert len(result) == 2