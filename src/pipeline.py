
import re

from .document_loader import extract_text
from .text_processor import clean_text, chunk_text
from .qna_generator import generate_qna
from .translator import translate_qna_to_languages
from .excel_generator import create_excel
from .validator import validate_multilingual_qna


def normalize_question(question: str) -> str:
    question = question.lower()

    question = re.sub(
        r"[^a-z0-9\s]",
        "",
        question
    )

    question = re.sub(
        r"\s+",
        " ",
        question
    )

    return question.strip()


def remove_duplicate_qna(
    qna_pairs: list[dict]
) -> list[dict]:

    unique_qna = []
    seen_questions = set()

    for pair in qna_pairs:

        question = pair["question"]

        normalized = normalize_question(
            question
        )

        if normalized in seen_questions:
            continue

        seen_questions.add(normalized)
        unique_qna.append(pair)

    return unique_qna


def generate_qna_from_chunks(
    client,
    chunks: list[str],
    questions_per_chunk: int = 5
) -> list[dict]:

    all_qna = []

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        print(
            f"Processing chunk "
            f"{index}/{len(chunks)}..."
        )

        qna_pairs = generate_qna(
            client=client,
            text=chunk,
            num_questions=questions_per_chunk
        )

        all_qna.extend(qna_pairs)

        print(
            f"Generated "
            f"{len(qna_pairs)} Q&A pairs."
        )

    return all_qna


def run_pipeline(
    client,
    input_file: str,
    output_file: str,
    questions_per_chunk: int = 5,
    max_chars: int = 4000,
    translate: bool = True
):

    print("=" * 60)
    print("MULTILINGUAL Q&A GENERATION PIPELINE")
    print("=" * 60)

    # STEP 1
    print("\n[1/7] Extracting document text...")

    text = extract_text(input_file)

    print(
        f"Extracted {len(text)} characters."
    )

    # STEP 2
    print("\n[2/7] Cleaning text...")

    cleaned_text = clean_text(text)

    print(
        f"Cleaned text length: "
        f"{len(cleaned_text)} characters."
    )

    # STEP 3
    print("\n[3/7] Creating text chunks...")

    chunks = chunk_text(
        cleaned_text,
        max_chars=max_chars
    )

    print(
        f"Created {len(chunks)} chunks."
    )

    if not chunks:
        raise ValueError(
            "No usable text chunks were created."
        )

    # STEP 4
    print("\n[4/7] Generating English Q&A...")

    english_qna = generate_qna_from_chunks(
        client=client,
        chunks=chunks,
        questions_per_chunk=questions_per_chunk
    )

    print(
        f"Total generated Q&A: "
        f"{len(english_qna)}"
    )

    # STEP 5
    print("\n[5/7] Removing duplicate questions...")

    english_qna = remove_duplicate_qna(
        english_qna
    )

    print(
        f"Unique English Q&A: "
        f"{len(english_qna)}"
    )

    if not english_qna:
        raise ValueError(
            "No Q&A pairs were generated."
        )

    # STEP 6
    print(
        "\n[6/7] Translating into "
        "Hindi and Marathi..."
    )

    if not translate:
        raise ValueError(
            "Translation is required for "
            "the final multilingual output."
        )

    translations = translate_qna_to_languages(
        client=client,
        qna_pairs=english_qna
    )

    hindi_qna = translations["Hindi"]
    marathi_qna = translations["Marathi"]

    # VALIDATION
    print(
        "\nValidating all three languages..."
    )

    validated = validate_multilingual_qna(
        english_qna=english_qna,
        hindi_qna=hindi_qna,
        marathi_qna=marathi_qna
    )

    english_qna = validated["English"]
    hindi_qna = validated["Hindi"]
    marathi_qna = validated["Marathi"]

    print("Validation successful!")

    # STEP 7
    print("\n[7/7] Creating Excel file...")

    create_excel(
        english_qna=english_qna,
        hindi_qna=hindi_qna,
        marathi_qna=marathi_qna,
        output_path=output_file
    )

    print(
        f"Excel saved to: {output_file}"
    )

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED")
    print("=" * 60)

    return {
        "english": english_qna,
        "hindi": hindi_qna,
        "marathi": marathi_qna,
        "output_file": output_file
    }
