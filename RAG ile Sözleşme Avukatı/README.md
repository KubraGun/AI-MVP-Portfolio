# Contract Lawyer with RAG

A Python application that helps you ask questions about contract documents and get answers using AI.

## What It Does

This project has two main parts:

1.  **Database Builder** (`build_vector_db.py`):
    *   Takes a PDF contract file and extracts the text.
    *   Splits the text into smaller, manageable pieces.
    *   Processes these pieces to create numerical representations (embeddings).
    *   Saves these representations to a local database for fast searching.

2.  **Question Assistant** (`ask_question.py`):
    *   Lets you ask questions in plain English about the contract.
    *   Finds the most relevant parts of the contract related to your question.
    *   Uses an AI model (GPT-3.5) to generate a clear answer based on those relevant parts.

## How to Set Up

1.  **Install Python Libraries:**
    You need to install the required packages. Run this command in your terminal:
    ```
    pip install openai python-dotenv sentence-transformers faiss-cpu numpy PyMuPDF
    ```

2.  **Get an OpenAI API Key:**
    *   You need an API key from OpenAI to use the AI model.
    *   Create a file named `.env` in the project folder.
    *   Inside this file, write: `OPENAI_API_KEY=your_actual_api_key_here`

3.  **Prepare Your Contract:**
    *   Place your contract PDF file in a folder named `data`.
    *   Update the file path in `build_vector_db.py` (the `pdf_file_path` variable) to point to your PDF.

## How to Use

**Step 1: Build the Database**
Run the `build_vector_db.py` script first. This will process your contract and create the searchable database.
```
python build_vector_db.py
```

**Step 2: Ask Questions**
Run the `ask_question.py` script. A prompt will appear in the terminal where you can type your questions.
```
python ask_question.py
```
Type your question about the contract and press Enter. The assistant will provide an answer. To stop the program, type `exit`, `quit`, or `q`.

## How It Works (Simple Explanation)

The system does not read the entire contract from scratch every time. Instead, it first converts the contract into a format that a computer can search very quickly. When you ask a question, it finds the pieces of the contract that are most likely to contain the answer. It then sends only those pieces, along with your question, to an AI model, which writes a final answer for you.

## Important Notes

*   The system is designed to work with PDF contract files.
*   The quality of the answers depends on the quality and clarity of the original contract text.
*   This is a local setup for demonstration and personal use.

---