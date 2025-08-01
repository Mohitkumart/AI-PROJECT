import os
import fitz  # PyMuPDF
import pandas as pd

def read_pdf_text(file_path: str) -> str:
    if not os.path.exists(file_path):
        file_path = os.path.join("data", file_path)

    if not os.path.exists(file_path):
        return f"File not found: {file_path}"

    doc = fitz.open(file_path)
    text = "".join(page.get_text() for page in doc)
    doc.close()
    return text.strip() or "No text found in PDF."


def read_excel_text(file_path: str) -> str:
    if not os.path.exists(file_path):
        file_path = os.path.join("data", file_path)

    if not os.path.exists(file_path):
        return f"File not found: {file_path}"

    df = pd.read_excel(file_path)
    return df.to_string(index=False)


def count_employees_from_text(pdf_text: str) -> str:
    lines = [line.strip() for line in pdf_text.splitlines() if line.strip()]
    return f"Found {len(lines)} employees."


def get_combined_text_from_data_folder() -> str:
    combined_text = ""
    data_dir = "data"

    if not os.path.exists(data_dir):
        return "No data folder found."

    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        if filename.endswith(".pdf"):
            try:
                doc = fitz.open(file_path)
                text = "".join(page.get_text() for page in doc)
                doc.close()
                combined_text += f"\n\n--- PDF: {filename} ---\n{text.strip()}"
            except Exception as e:
                combined_text += f"\n\n--- PDF: {filename} ---\nError: {str(e)}"
        elif filename.endswith(".xlsx"):
            try:
                df = pd.read_excel(file_path)
                combined_text += f"\n\n--- Excel: {filename} ---\n{df.to_string(index=False)}"
            except Exception as e:
                combined_text += f"\n\n--- Excel: {filename} ---\nError: {str(e)}"

    return combined_text.strip() or "No documents found in data folder."
