import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
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
MODEL_OUTPUT_DIR = "models"
MODEL_FILE = os.path.join(MODEL_OUTPUT_DIR, "cv_classifier.pkl")
LABEL_ENCODER_FILE = os.path.join(MODEL_OUTPUT_DIR, "label_encoder.pkl")

os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)


def load_data(path: str) -> pd.DataFrame:
    """Tải dữ liệu từ file CSV."""
    print(f"[INFO] Đang tải dữ liệu từ: {path}")
    df = pd.read_csv(path)
    print(f"[INFO] Tổng số mẫu: {len(df)}")
    return df


def preprocess(df: pd.DataFrame):
    """Tiền xử lý dữ liệu và tách features/labels."""
    # Kết hợp các trường text thành một chuỗi đặc trưng
    df["text_features"] = (
        df["skills"].fillna("") + " " +
        df["industry"].fillna("") + " " +
        df["job_title"].fillna("") + " " +
        df["education"].fillna("")
    )

    X = df["text_features"]
    y = df["label"]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    return X, y_encoded, le


def build_pipeline() -> Pipeline:
    """Xây dựng pipeline huấn luyện (TF-IDF + RandomForest)."""
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000)),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42)),
    ])
    return pipeline


def train():
    """Hàm chính để huấn luyện mô hình."""
    # 1. Tải dữ liệu
    df = load_data(DATASET_PATH)

    # 2. Tiền xử lý
    X, y, label_encoder = preprocess(df)

    # 3. Chia tập train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"[INFO] Train: {len(X_train)} mẫu | Test: {len(X_test)} mẫu")

    # 4. Xây dựng & huấn luyện pipeline
    pipeline = build_pipeline()
    print("[INFO] Đang huấn luyện mô hình...")
    pipeline.fit(X_train, y_train)

    # 5. Đánh giá
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n[RESULT] Độ chính xác: {acc * 100:.2f}%")
    print("\n[RESULT] Báo cáo chi tiết:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

    # 6. Lưu mô hình
    joblib.dump(pipeline, MODEL_FILE)
    joblib.dump(label_encoder, LABEL_ENCODER_FILE)
    print(f"\n[INFO] Mô hình đã được lưu tại: {MODEL_FILE}")
    print(f"[INFO] Label encoder đã được lưu tại: {LABEL_ENCODER_FILE}")


if __name__ == "__main__":
    train()
