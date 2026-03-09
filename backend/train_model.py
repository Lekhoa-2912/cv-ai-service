import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# =====================================================================
# CẤU HÌNH
# =====================================================================
DATASET_PATH = os.path.join("dataset", "cv_industry_dataset.csv")
MODEL_DIR = "model"
MODEL_FILE = os.path.join(MODEL_DIR, "svm_model.pkl")
LABEL_ENCODER_FILE = os.path.join(MODEL_DIR, "label_encoder.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)


def load_data(path: str) -> pd.DataFrame:
    """Tải dữ liệu từ file CSV."""
    print(f"[INFO] Đang tải dữ liệu từ: {path}")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy dataset: {path}")
    df = pd.read_csv(path)
    print(f"[INFO] Tổng số mẫu: {len(df)}")
    return df


def preprocess(df: pd.DataFrame):
    """Tiền xử lý dữ liệu."""
    df = df.dropna(subset=["resume_text", "industry"])
    X = df["resume_text"].astype(str)
    y = df["industry"].astype(str)

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    return X, y_encoded, le


def build_pipeline() -> Pipeline:
    """Xây dựng pipeline: TF-IDF + SVM."""
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            sublinear_tf=True,
        )),
        ("svm", SVC(
            kernel="linear",
            C=1.0,
            probability=True,
            random_state=42,
        )),
    ])
    return pipeline


def train():
    """Hàm chính để huấn luyện và lưu mô hình SVM."""
    # 1. Tải dữ liệu
    df = load_data(DATASET_PATH)

    # 2. Tiền xử lý
    X, y, label_encoder = preprocess(df)
    print(f"[INFO] Số nhãn (industries): {len(label_encoder.classes_)}")
    print(f"[INFO] Danh sách ngành: {list(label_encoder.classes_)}")

    # 3. Chia train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"[INFO] Train: {len(X_train)} | Test: {len(X_test)}")

    # 4. Xây dựng và huấn luyện
    pipeline = build_pipeline()
    print("[INFO] Đang huấn luyện mô hình SVM...")
    pipeline.fit(X_train, y_train)

    # 5. Đánh giá
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n[RESULT] Độ chính xác: {acc * 100:.2f}%")
    print("\n[RESULT] Báo cáo chi tiết:")
    print(classification_report(
        y_test, y_pred,
        target_names=label_encoder.classes_
    ))

    # 6. Lưu mô hình
    joblib.dump(pipeline, MODEL_FILE)
    joblib.dump(label_encoder, LABEL_ENCODER_FILE)
    print(f"[INFO] ✅ Mô hình SVM đã lưu: {MODEL_FILE}")
    print(f"[INFO] ✅ Label encoder đã lưu: {LABEL_ENCODER_FILE}")


if __name__ == "__main__":
    train()
