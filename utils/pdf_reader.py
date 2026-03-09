import pdfplumber
import os


def read_pdf(file_path: str) -> str:
    """
    Đọc nội dung văn bản từ file PDF.

    Args:
        file_path (str): Đường dẫn đến file PDF cần đọc.

    Returns:
        str: Nội dung văn bản trích xuất từ PDF.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File không tồn tại: {file_path}")

    if not file_path.lower().endswith(".pdf"):
        raise ValueError(f"File không phải định dạng PDF: {file_path}")

    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise RuntimeError(f"Lỗi khi đọc file PDF '{file_path}': {e}")

    return text.strip()


def read_pdf_pages(file_path: str) -> list[str]:
    """
    Đọc nội dung từng trang của file PDF.

    Args:
        file_path (str): Đường dẫn đến file PDF.

    Returns:
        list[str]: Danh sách nội dung từng trang.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File không tồn tại: {file_path}")

    pages_text = []
    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                pages_text.append(page_text if page_text else "")
    except Exception as e:
        raise RuntimeError(f"Lỗi khi đọc file PDF '{file_path}': {e}")

    return pages_text
