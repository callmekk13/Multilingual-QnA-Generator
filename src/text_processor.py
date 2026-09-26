
import re


def clean_text(text: str) -> str:
    """
    Clean extracted document text while preserving its meaning.
    """

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces at the beginning/end of lines
    lines = [line.strip() for line in text.split("\n")]

    # Remove empty lines at the beginning/end
    text = "\n".join(lines).strip()

    return text


def chunk_text(
    text: str,
    max_chars: int = 4000
) -> list[str]:
    """
    Split text into meaningful chunks without cutting sentences or words.
    """

    text = clean_text(text)

    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(start + max_chars, text_length)

        if end < text_length:

            # Prefer paragraph boundary
            paragraph_break = text.rfind("\n\n", start, end)

            if paragraph_break > start:
                end = paragraph_break

            else:
                # Prefer sentence boundary
                sentence_breaks = [
                    text.rfind(". ", start, end),
                    text.rfind("? ", start, end),
                    text.rfind("! ", start, end)
                ]

                best_break = max(sentence_breaks)

                if best_break > start:
                    end = best_break + 1

                else:
                    # Fall back to word boundary
                    space_break = text.rfind(" ", start, end)

                    if space_break > start:
                        end = space_break

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end

        # Skip whitespace before the next chunk
        while start < text_length and text[start].isspace():
            start += 1

    return chunks
