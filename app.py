import os
import sys
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai

PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

load_dotenv()

from src.pipeline import run_pipeline


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Multilingual Q&A Generator",
    page_icon="📚",
    layout="wide"
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("📚 Multilingual Q&A Generator")

st.markdown(
    """
Upload an English **PDF, DOCX, or TXT** document and generate
context-aware Question & Answer pairs in:

- 🇬🇧 English
- 🇮🇳 Hindi
- 🇮🇳 Marathi
"""
)

st.divider()


# ---------------------------------------------------------
# API configuration
# ---------------------------------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error(
        "GEMINI_API_KEY is not configured. "
        "Please add it to your .env file."
    )
    st.stop()

client = genai.Client(api_key=api_key)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    questions_per_chunk = st.slider(
        "Questions per chunk",
        min_value=1,
        max_value=5,
        value=3
    )

    max_chars = st.slider(
        "Maximum chunk size",
        min_value=1000,
        max_value=5000,
        value=3000,
        step=500
    )

    st.divider()

    st.info(
        "The system extracts information from the uploaded "
        "document and generates multilingual Q&A pairs."
    )


# ---------------------------------------------------------
# File upload
# ---------------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload your document",
    type=["pdf", "docx", "txt"],
    help="Supported formats: PDF, DOCX and TXT"
)


# ---------------------------------------------------------
# Generate
# ---------------------------------------------------------

if uploaded_file:

    st.success(
        f"Uploaded: **{uploaded_file.name}**"
    )

    generate = st.button(
        "🚀 Generate Q&A",
        type="primary",
        use_container_width=True
    )

    if generate:

        suffix = Path(
            uploaded_file.name
        ).suffix.lower()

        input_path = None

        try:

            # ---------------------------------------------
            # Save uploaded file temporarily
            # ---------------------------------------------

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getbuffer()
                )

                input_path = temp_file.name


            # ---------------------------------------------
            # Output path
            # ---------------------------------------------

            output_dir = PROJECT_DIR / "outputs"

            output_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            output_path = (
                output_dir / "QnA.xlsx"
            )


            # ---------------------------------------------
            # Run pipeline
            # ---------------------------------------------

            with st.status(
                "Processing document...",
                expanded=True
            ) as status:

                st.write("📄 Extracting document text...")
                st.write("🧹 Cleaning and chunking text...")
                st.write("🤖 Generating English Q&A...")
                st.write("🌐 Translating into Hindi and Marathi...")
                st.write("✅ Validating generated Q&A...")
                st.write("📊 Creating Excel workbook...")

                result = run_pipeline(
                    client=client,
                    input_file=input_path,
                    output_file=str(output_path),
                    questions_per_chunk=questions_per_chunk,
                    max_chars=max_chars,
                    translate=True
                )

                status.update(
                    label="Q&A generation completed!",
                    state="complete",
                    expanded=False
                )


            # ---------------------------------------------
            # Extract results
            # ---------------------------------------------

            english_qna = result["english"]
            hindi_qna = result["hindi"]
            marathi_qna = result["marathi"]


            st.success(
                f"Generated {len(english_qna)} Q&A pairs successfully."
            )


            # ---------------------------------------------
            # Language tabs
            # ---------------------------------------------

            tab_english, tab_hindi, tab_marathi = st.tabs(
                [
                    "🇬🇧 English",
                    "🇮🇳 Hindi",
                    "🇮🇳 Marathi"
                ]
            )


            with tab_english:

                english_df = pd.DataFrame(
                    english_qna
                )

                english_df.columns = [
                    "Question",
                    "Answer"
                ]

                st.dataframe(
                    english_df,
                    use_container_width=True,
                    hide_index=True
                )


            with tab_hindi:

                hindi_df = pd.DataFrame(
                    hindi_qna
                )

                hindi_df.columns = [
                    "Question",
                    "Answer"
                ]

                st.dataframe(
                    hindi_df,
                    use_container_width=True,
                    hide_index=True
                )


            with tab_marathi:

                marathi_df = pd.DataFrame(
                    marathi_qna
                )

                marathi_df.columns = [
                    "Question",
                    "Answer"
                ]

                st.dataframe(
                    marathi_df,
                    use_container_width=True,
                    hide_index=True
                )


            # ---------------------------------------------
            # Download
            # ---------------------------------------------

            st.divider()

            st.subheader("📥 Download Results")

            with open(
                output_path,
                "rb"
            ) as excel_file:

                st.download_button(
                    label="Download QnA.xlsx",
                    data=excel_file,
                    file_name="QnA.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-"
                        "officedocument.spreadsheetml.sheet"
                    ),
                    use_container_width=True
                )


        except Exception as error:

            st.error(
                "An error occurred while generating the Q&A."
            )

            st.exception(error)


        finally:

            if input_path and os.path.exists(input_path):

                os.remove(input_path)
