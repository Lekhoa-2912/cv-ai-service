import joblib
import os

# =====================================================================
# CẤU HÌNH
# =====================================================================
MODEL_DIR = "model"
MODEL_FILE = os.path.join(MODEL_DIR, "svm_model.pkl")
LABEL_ENCODER_FILE = os.path.join(MODEL_DIR, "label_encoder.pkl")

_pipeline = None
_label_encoder = None


def load_model():
    """Tải mô hình SVM và label encoder (lazy loading)."""
    global _pipeline, _label_encoder
    if _pipeline is None:
        if not os.path.exists(MODEL_FILE):
            raise FileNotFoundError(
                f"Mô hình chưa được huấn luyện. "
                f"Vui lòng chạy 'python train_model.py' trước."
            )
        _pipeline = joblib.load(MODEL_FILE)
        _label_encoder = joblib.load(LABEL_ENCODER_FILE)
    return _pipeline, _label_encoder


def predict_industry(resume_text: str) -> dict:
    """
    Dự đoán ngành nghề từ nội dung CV.

    Args:
        resume_text (str): Văn bản CV (đã trích xuất từ PDF/ảnh).

    Returns:
        dict: Kết quả gồm ngành được dự đoán, độ tin cậy và xác suất từng ngành.
    """
    if not resume_text or not resume_text.strip():
        raise ValueError("Nội dung CV không được để trống.")

    pipeline, label_encoder = load_model()

    # Dự đoán
    pred_encoded = pipeline.predict([resume_text])[0]
    probabilities = pipeline.predict_proba([resume_text])[0]
    predicted_label = label_encoder.inverse_transform([pred_encoded])[0]

    # Tạo dict xác suất theo từng ngành
    classes = label_encoder.classes_
    prob_dict = {
        cls: round(float(prob), 4)
        for cls, prob in zip(classes, probabilities)
    }

    # Sắp xếp theo xác suất giảm dần
    prob_dict_sorted = dict(
        sorted(prob_dict.items(), key=lambda x: x[1], reverse=True)
    )

    return {
        "predicted_industry": predicted_label,
        "confidence": round(float(max(probabilities)), 4),
        "probabilities": prob_dict_sorted,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Cách dùng: python predict.py \"<nội dung CV>\"")
        sys.exit(1)

    text = sys.argv[1]
    result = predict_industry(text)

    print("\n===== KẾT QUẢ DỰ ĐOÁN =====")
    print(f"  Ngành dự đoán : {result['predicted_industry']}")
    print(f"  Độ tin cậy    : {result['confidence'] * 100:.1f}%")
    print(f"  Xác suất      :")
    for industry, prob in result["probabilities"].items():
        print(f"    {industry}: {prob * 100:.1f}%")
