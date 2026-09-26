# cat > tests/test_validator.py <<'EOF'
import pytest

from src.validator import (
    validate_qna_list,
    validate_multilingual_qna,
)


def test_validate_qna_list():
    qna = [
        {
            "question": "What is AI?",
            "answer": "AI is a branch of computer science."
        }
    ]

    result = validate_qna_list(qna, "English")

    assert len(result) == 1
    assert result[0]["question"] == "What is AI?"


def test_empty_question_fails():
    qna = [
        {
            "question": "",
            "answer": "Some answer."
        }
    ]

    with pytest.raises(ValueError):
        validate_qna_list(qna, "English")


def test_multilingual_count_mismatch_fails():
    english = [
        {"question": "Q1", "answer": "A1"},
        {"question": "Q2", "answer": "A2"},
    ]

    hindi = [
        {"question": "Q1", "answer": "A1"},
    ]

    marathi = [
        {"question": "Q1", "answer": "A1"},
        {"question": "Q2", "answer": "A2"},
    ]

    with pytest.raises(ValueError):
        validate_multilingual_qna(
            english,
            hindi,
            marathi
        )