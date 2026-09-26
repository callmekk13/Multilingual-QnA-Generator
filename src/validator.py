
def validate_qna_list(
    qna_pairs: list[dict],
    language: str = "English"
) -> list[dict]:
    """
    Validate and clean a Q&A list.
    """

    if not isinstance(qna_pairs, list):
        raise ValueError(
            f"{language} Q&A must be a list."
        )

    validated = []

    for index, pair in enumerate(
        qna_pairs,
        start=1
    ):

        if not isinstance(pair, dict):
            raise ValueError(
                f"{language} Q&A #{index} is not a dictionary."
            )

        question = pair.get("question")
        answer = pair.get("answer")

        if question is None or answer is None:
            raise ValueError(
                f"{language} Q&A #{index} "
                "is missing question or answer."
            )

        question = str(question).strip()
        answer = str(answer).strip()

        if not question:
            raise ValueError(
                f"{language} Q&A #{index} "
                "has an empty question."
            )

        if not answer:
            raise ValueError(
                f"{language} Q&A #{index} "
                "has an empty answer."
            )

        validated.append({
            "question": question,
            "answer": answer
        })

    return validated


def validate_multilingual_qna(
    english_qna: list[dict],
    hindi_qna: list[dict],
    marathi_qna: list[dict]
) -> dict:
    """
    Validate all three language Q&A lists.
    """

    english_qna = validate_qna_list(
        english_qna,
        "English"
    )

    hindi_qna = validate_qna_list(
        hindi_qna,
        "Hindi"
    )

    marathi_qna = validate_qna_list(
        marathi_qna,
        "Marathi"
    )

    # All languages must contain the same
    # number of Q&A pairs.
    if not (
        len(english_qna)
        == len(hindi_qna)
        == len(marathi_qna)
    ):
        raise ValueError(
            "Q&A count mismatch:\n"
            f"English: {len(english_qna)}\n"
            f"Hindi: {len(hindi_qna)}\n"
            f"Marathi: {len(marathi_qna)}"
        )

    return {
        "English": english_qna,
        "Hindi": hindi_qna,
        "Marathi": marathi_qna
    }
