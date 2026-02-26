import os
from dotenv import load_dotenv
from pypdf import PdfReader

from crewai.tools import tool

load_dotenv()

@tool("read_financial_pdf")
def read_financial_pdf_tool(file_path: str) -> str:
    """
    Read and return cleaned text from a PDF file path.

    Args:
        file_path: Absolute or relative path to a PDF file.

    Returns:
        Extracted text from the PDF (cleaned).
    """
    if not file_path or not isinstance(file_path, str):
        raise ValueError("file_path must be a non-empty string")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    reader = PdfReader(file_path)
    pages_text = []

    for page in reader.pages:
        text = page.extract_text() or ""
        # Clean up repeated whitespace / blank lines
        text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
        if text:
            pages_text.append(text)

    full_text = "\n\n".join(pages_text).strip()

    if not full_text:
        return (
            "WARNING: No extractable text found in this PDF. "
            "It might be a scanned PDF (image-only). Consider OCR support if needed."
        )

    return full_text