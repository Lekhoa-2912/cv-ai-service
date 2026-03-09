import pytesseract
from PIL import Image
import pdf2image
import os


# Cấu hình đường dẫn Tesseract (chỉnh sửa nếu cần)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def read_image_ocr(image_path: str, lang: str = "vie+eng") -> str:
    """
    Trích xuất văn bản từ file ảnh bằng OCR (Tesseract).

    Args:
        image_path (str): Đường dẫn đến file ảnh.
        lang (str): Ngôn ngữ nhận dạng OCR (mặc định: 'vie+eng').

    Returns:
        str: Văn bản trích xuất được từ ảnh.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File ảnh không tồn tại: {image_path}")

    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Lỗi khi OCR ảnh '{image_path}': {e}")


def read_pdf_ocr(pdf_path: str, lang: str = "vie+eng", dpi: int = 300) -> str:
    """
    Trích xuất văn bản từ file PDF bằng OCR (dành cho PDF dạng scan/ảnh).

    Args:
        pdf_path (str): Đường dẫn đến file PDF.
        lang (str): Ngôn ngữ nhận dạng OCR (mặc định: 'vie+eng').
        dpi (int): Độ phân giải khi chuyển đổi PDF sang ảnh (mặc định: 300).

    Returns:
        str: Văn bản trích xuất được từ PDF.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File PDF không tồn tại: {pdf_path}")

    try:
        images = pdf2image.convert_from_path(pdf_path, dpi=dpi)
        full_text = ""
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang=lang)
            full_text += f"\n--- Trang {i + 1} ---\n{text}"
        return full_text.strip()
    except Exception as e:
        raise RuntimeError(f"Lỗi khi OCR file PDF '{pdf_path}': {e}")


def read_image_ocr_from_bytes(image_bytes: bytes, lang: str = "vie+eng") -> str:
    """
    Trích xuất văn bản từ dữ liệu ảnh dạng bytes.

    Args:
        image_bytes (bytes): Dữ liệu ảnh dạng bytes.
        lang (str): Ngôn ngữ nhận dạng OCR.

    Returns:
        str: Văn bản trích xuất được.
    """
    import io
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Lỗi khi OCR ảnh từ bytes: {e}")
