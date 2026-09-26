# Multilingual Q&A Generator

An AI-powered system that accepts an English PDF, DOCX, or TXT document and automatically generates context-aware Question & Answer pairs in:

* English
* Hindi
* Marathi

The generated Q&A pairs are exported into a single Excel workbook with separate worksheets for each language.

## Features

* Supports PDF, DOCX, and TXT input files
* Automatic text extraction
* Text cleaning and chunking
* Context-aware Q&A generation using Google Gemini
* English Q&A generation
* Hindi translation
* Marathi translation
* Duplicate question removal
* Q&A validation
* Excel output generation
* Streamlit web interface
* Downloadable `QnA.xlsx` output

## Project Architecture

```text
Multilingual-QnA-Generator/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── src/
│   ├── document_loader.py
│   ├── text_processor.py
│   ├── qna_generator.py
│   ├── translator.py
│   ├── validator.py
│   ├── excel_generator.py
│   └── pipeline.py
│
├── input_documents/
│   ├── sample.txt
│   ├── sample.docx
│   └── sample.pdf
│
├── outputs/
├── tests/
└── demo/
```

## How It Works

The system follows this pipeline:

```text
Input Document
      ↓
Document Text Extraction
      ↓
Text Cleaning
      ↓
Text Chunking
      ↓
English Q&A Generation
      ↓
Duplicate Removal
      ↓
Hindi + Marathi Translation
      ↓
Validation
      ↓
Excel Generation
      ↓
QnA.xlsx
```

## Technologies Used

* Python
* Google Gemini API
* Google GenAI Python SDK
* Streamlit
* PyMuPDF
* python-docx
* Pandas
* OpenPyXL
* python-dotenv

## Input Formats

The application supports:

```text
.pdf
.docx
.txt
```

The input document should contain English text.

## Output

The application generates:

```text
QnA.xlsx
```

The Excel workbook contains three worksheets:

```text
English
Hindi
Marathi
```

Each worksheet contains:

```text
Questions | Answers
```

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Multilingual-QnA-Generator
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file:

```text
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit the `.env` file to GitHub.

A template is provided in:

```text
.env.example
```

## Run the Application

Start Streamlit:

```bash
streamlit run app.py
```

The application will open in your browser.

Upload a PDF, DOCX, or TXT file and click:

```text
Generate Q&A
```

The generated results can be viewed in the English, Hindi, and Marathi tabs and downloaded as an Excel file.

## Example

### Input

```text
Artificial Intelligence (AI) is a branch of computer science
that focuses on creating systems capable of performing tasks
that normally require human intelligence.
```

### Generated English Q&A

```text
Question:
What is Artificial Intelligence?

Answer:
Artificial Intelligence is a branch of computer science that
focuses on creating systems capable of performing tasks that
normally require human intelligence.
```

The same Q&A is translated into Hindi and Marathi and added to their respective Excel worksheets.

## Validation

The system validates:

* Q&A structure
* Missing questions
* Missing answers
* Empty questions
* Empty answers
* Language-wise Q&A counts
* Duplicate questions

This helps ensure that the final Excel workbook contains structured and consistent data.

## Security

API credentials are stored in the local `.env` file.

The `.gitignore` file prevents `.env` and generated Excel files from being committed to the repository.

Never upload your actual API key to GitHub.

## Future Improvements

Possible future improvements include:

* Support for larger documents
* Better semantic chunking
* Question difficulty levels
* Question categories
* Automatic answer-quality scoring
* More Indian languages
* PDF/DOCX preview
* Q&A filtering
* Advanced multilingual validation
* Cloud deployment
* Authentication and user management

## Assignment Deliverables

This project provides:

* Python source code
* PDF/DOCX/TXT document processing
* English Q&A generation
* Hindi translation
* Marathi translation
* Excel output
* Streamlit interface
* Project documentation
* Demo-ready workflow

## Author

**Kartikey Kolhe**

B.Tech Computer Science & Engineering (Data Science)

---

### Note

This project uses Google Gemini for Q&A generation and multilingual translation. API usage may be subject to the limits of the selected Gemini API tier.
