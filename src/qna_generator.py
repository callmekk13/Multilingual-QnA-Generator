
import json
from google import genai


def generate_qna(
    client,
    text: str,
    num_questions: int = 5
) -> list[dict]:
    """
    Generate document-grounded Q&A pairs from a text chunk.
    """

    prompt = f"""
You are an expert educational question-answer generation system.

Your task is to generate meaningful question-answer pairs ONLY
from the information explicitly present in the provided text.

IMPORTANT RULES:

1. Do not use outside knowledge.
2. Do not invent facts.
3. Every answer must be directly supported by the text.
4. Questions must be meaningful and relevant.
5. Avoid duplicate or nearly identical questions.
6. Answers should be concise but complete.
7. Do not ask questions whose answers are not present in the text.
8. Return exactly {num_questions} questions when the text contains
   enough information. If the text does not contain enough information,
   return fewer questions.
9. Return ONLY valid JSON.
10. Do not include Markdown or code fences.

Required JSON format:

[
    {{
        "question": "Question here",
        "answer": "Answer here"
    }}
]

TEXT:

{text}
"""

    # Use the current Gemini Interactions API
    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    response_text = response.output_text.strip()

    # Remove accidental Markdown code fences
    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    try:
        qna_pairs = json.loads(response_text)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Gemini returned invalid JSON:\n{response_text}"
        ) from error

    if not isinstance(qna_pairs, list):
        raise ValueError("Expected a JSON list of Q&A pairs.")

    validated_pairs = []

    for pair in qna_pairs:

        if not isinstance(pair, dict):
            continue

        question = pair.get("question")
        answer = pair.get("answer")

        if not question or not answer:
            continue

        validated_pairs.append({
            "question": str(question).strip(),
            "answer": str(answer).strip()
        })

    return validated_pairs
