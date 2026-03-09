import joblib
import os
from utils.pdf_reader import read_pdf
from utils.ocr_reader import read_pdf_ocr

# =====================================================================
# CẤU HÌNH
# =====================================================================
MODEL_FILE = os.path.join("models", "cv_classifier.pkl")
LABEL_ENCODER_FILE = os.path.join("models", "label_encoder.pkl")


def load_model():
    """Tải mô hình và label encoder đã huấn luyện."""
    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(
            f"Mô hình không tìm thấy tại '{MODEL_FILE}'. "
            "Vui lòng chạy train_model.py trước."
        )
    pipeline = joblib.load(MODEL_FILE)
    label_encoder = joblib.load(LABEL_ENCODER_FILE)
    return pipeline, label_encoder


def extract_text_from_cv(file_path: str, use_ocr: bool = False) -> str:
    """
    Trích xuất văn bản từ file CV (PDF hoặc ảnh).

    Args:
        file_path (str): Đường dẫn đến file CV.
        use_ocr (bool): Sử dụng OCR nếu PDF dạng scan.

    Returns:
        str: Văn bản trích xuất.
    """
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        if use_ocr:
            text = read_pdf_ocr(file_path)
        else:
            text = read_pdf(file_path)
    elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
        from utils.ocr_reader import read_image_ocr
        text = read_image_ocr(file_path)
    else:
        raise ValueError(f"Định dạng file không được hỗ trợ: {ext}")

    return text


def predict_cv(file_path: str, use_ocr: bool = False) -> dict:
    """
    Dự đoán kết quả phân loại CV.

    Args:
        file_path (str): Đường dẫn đến file CV.
        use_ocr (bool): Sử dụng OCR nếu cần.

    Returns:
        dict: Kết quả dự đoán bao gồm nhãn và xác suất.
    """
    # 1. Tải mô hình
    pipeline, label_encoder = load_model()

    # 2. Trích xuất văn bản
    print(f"[INFO] Đang xử lý file: {file_path}")
    text = extract_text_from_cv(file_path, use_ocr=use_ocr)

    if not text.strip():
        return {"error": "Không thể trích xuất nội dung từ file CV."}

    # 3. Dự đoán
    prediction_encoded = pipeline.predict([text])[0]
    probabilities = pipeline.predict_proba([text])[0]
    label = label_encoder.inverse_transform([prediction_encoded])[0]

    # 4. Tạo kết quả
    classes = label_encoder.classes_
    prob_dict = {cls: round(float(prob), 4) for cls, prob in zip(classes, probabilities)}

    result = {
        "file": file_path,
        "prediction": label,
        "confidence": round(float(max(probabilities)), 4),
        "probabilities": prob_dict,
    }

    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Cách dùng: python predict.py <đường_dẫn_file_cv> [--ocr]")
        sys.exit(1)

    cv_path = sys.argv[1]
    use_ocr_flag = "--ocr" in sys.argv

    result = predict_cv(cv_path, use_ocr=use_ocr_flag)
    print("\n===== KẾT QUẢ DỰ ĐOÁN =====")
    for key, value in result.items():
        print(f"  {key}: {value}")
