
import json


def _parse_json_response(response_text: str):
    response_text = response_text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace(
            "```json",
            ""
        )
        response_text = response_text.replace(
            "```",
            ""
        )
        response_text = response_text.strip()

    try:
        return json.loads(response_text)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Gemini returned invalid JSON:\n{response_text}"
        ) from error


def translate_qna_to_languages(
    client,
    qna_pairs: list[dict]
) -> dict:

    input_qna = json.dumps(
        qna_pairs,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
You are a professional multilingual translator.

Translate the provided English Question-Answer pairs into:

1. Hindi
2. Marathi

IMPORTANT RULES:

1. Preserve the exact meaning of every question.
2. Preserve the exact meaning of every answer.
3. Do not add information.
4. Do not remove important information.
5. Do not use outside knowledge.
6. Keep technical terms accurate.
7. Use natural and grammatically correct Hindi.
8. Use natural and grammatically correct Marathi.
9. Keep the same number of Q&A pairs.
10. Keep the same order of Q&A pairs.
11. Every English question must have exactly one
    Hindi and one Marathi translation.
12. Every English answer must have exactly one
    Hindi and one Marathi translation.
13. Return ONLY valid JSON.
14. Do not use Markdown or code fences.

Required output format:

{{
    "Hindi": [
        {{
            "question": "Hindi question",
            "answer": "Hindi answer"
        }}
    ],
    "Marathi": [
        {{
            "question": "Marathi question",
            "answer": "Marathi answer"
        }}
    ]
}}

English Q&A pairs:

{input_qna}
"""

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    result = _parse_json_response(
        response.output_text
    )

    if not isinstance(result, dict):
        raise ValueError(
            "Expected a JSON object."
        )

    if "Hindi" not in result:
        raise ValueError(
            "Hindi translations are missing."
        )

    if "Marathi" not in result:
        raise ValueError(
            "Marathi translations are missing."
        )

    hindi_qna = result["Hindi"]
    marathi_qna = result["Marathi"]

    if len(hindi_qna) != len(qna_pairs):
        raise ValueError(
            f"Hindi count mismatch. "
            f"Expected {len(qna_pairs)}, "
            f"got {len(hindi_qna)}."
        )

    if len(marathi_qna) != len(qna_pairs):
        raise ValueError(
            f"Marathi count mismatch. "
            f"Expected {len(qna_pairs)}, "
            f"got {len(marathi_qna)}."
        )

    def validate_pairs(
        pairs: list[dict],
        language: str
    ) -> list[dict]:

        validated = []

        for pair in pairs:

            if not isinstance(pair, dict):
                raise ValueError(
                    f"Invalid Q&A object in {language}."
                )

            question = pair.get("question")
            answer = pair.get("answer")

            if not question or not answer:
                raise ValueError(
                    f"Missing question or answer "
                    f"in {language} translation."
                )

            validated.append({
                "question": str(question).strip(),
                "answer": str(answer).strip()
            })

        return validated

    return {
        "Hindi": validate_pairs(
            hindi_qna,
            "Hindi"
        ),
        "Marathi": validate_pairs(
            marathi_qna,
            "Marathi"
        )
    }
