import os
import fitz  # PyMuPDF
import pandas as pd
from langchain.tools import tool

@tool
def read_pdf(file_path: str) -> str:
    """
    Read and return text from a PDF file.

    Args:
        file_path (str): Relative or absolute path to the PDF file.
    Returns:
        str: All extracted text or error message.
    """
    try:
        if not os.path.exists(file_path):
            file_path = os.path.join("data", file_path)

        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        doc = fitz.open(file_path)
        text = "".join(page.get_text() for page in doc)
        doc.close()
        return text.strip() or "No text found in PDF."
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


@tool
def read_excel(file_path: str) -> str:
    """
    Read and return content of an Excel (.xlsx) file as plain text.

    Args:
        file_path (str): Relative or absolute path to the Excel file.
    Returns:
        str: Tabular data or error message.
    """
    try:
        if not os.path.exists(file_path):
            file_path = os.path.join("data", file_path)

        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        df = pd.read_excel(file_path)
        return df.to_string(index=False)
    except Exception as e:
        return f"Error reading Excel: {str(e)}"


@tool
def count_employees_from_pdf_text(pdf_text: str) -> str:
    """
    Count the number of non-empty lines in PDF text as a proxy for employees.

    Args:
        pdf_text (str): Text extracted from the PDF.
    Returns:
        str: Count of entries.
    """
    try:
        lines = [line.strip() for line in pdf_text.splitlines() if line.strip()]
        return f"Found {len(lines)} employees."
    except Exception as e:
        return f"Error counting employees: {str(e)}"


class DocumentReaderTool:
    def __init__(self):
        self._document_reader_tool_list = [
            read_pdf,
            read_excel,
            count_employees_from_pdf_text
        ]

    def get_combined_text(self) -> str:
        """
        Combine and return all document text found in the /data directory.
        """
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

    @property
    def document_reader_tool_list(self):
        return self._document_reader_tool_list
