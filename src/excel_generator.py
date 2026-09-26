
from pathlib import Path
import pandas as pd


def create_excel(
    english_qna: list[dict],
    hindi_qna: list[dict],
    marathi_qna: list[dict],
    output_path: str
) -> str:

    output_file = Path(output_path)

    # Create output directory
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Convert Q&A lists to DataFrames
    english_df = pd.DataFrame(
        english_qna,
        columns=["question", "answer"]
    )

    hindi_df = pd.DataFrame(
        hindi_qna,
        columns=["question", "answer"]
    )

    marathi_df = pd.DataFrame(
        marathi_qna,
        columns=["question", "answer"]
    )

    # Rename columns according to assignment
    english_df.columns = ["Questions", "Answers"]
    hindi_df.columns = ["Questions", "Answers"]
    marathi_df.columns = ["Questions", "Answers"]

    # Create Excel workbook
    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        english_df.to_excel(
            writer,
            sheet_name="English",
            index=False
        )

        hindi_df.to_excel(
            writer,
            sheet_name="Hindi",
            index=False
        )

        marathi_df.to_excel(
            writer,
            sheet_name="Marathi",
            index=False
        )

    return str(output_file)
    
