# 🤖 TalentIQ — CV AI Service

> **Hệ thống phân tích & phân loại CV tự động bằng Machine Learning**  
> Dự đoán ngành nghề phù hợp của ứng viên từ nội dung CV (PDF hoặc văn bản thuần).

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react&logoColor=black"/>
  <img src="https://img.shields.io/badge/MongoDB-6.0+-47A248?style=for-the-badge&logo=mongodb&logoColor=white"/>
  <img src="https://img.shields.io/badge/scikit--learn-1.4+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
</p>

---

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Ngôn ngữ lập trình](#-ngôn-ngữ-lập-trình)
- [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
- [Thuật toán AI/ML](#-thuật-toán-aiml)
- [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
- [Cấu trúc thư mục](#-cấu-trúc-thư-mục)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Hướng dẫn cài đặt](#-hướng-dẫn-cài-đặt)
- [Huấn luyện mô hình](#-huấn-luyện-mô-hình)
- [Chạy ứng dụng](#-chạy-ứng-dụng)
- [API Reference](#-api-reference)

---

## 🎯 Giới thiệu

**TalentIQ CV AI Service** là một ứng dụng web **full-stack** giúp phân loại CV ứng viên tự động theo **ngành nghề** sử dụng Machine Learning. Hệ thống có khả năng:

- 📄 Phân tích nội dung CV từ file **PDF** hoặc **văn bản** trực tiếp
- 🏷️ Dự đoán **ngành nghề phù hợp** kèm độ tin cậy (confidence score)
- 📦 Xử lý **hàng loạt** nhiều CV cùng một lúc (batch processing, tối đa 20 file)
- 🗃️ Lưu trữ **lịch sử phân tích** trên MongoDB để tra cứu lại bất cứ lúc nào

---

## ✨ Tính năng

| Tính năng | Mô tả |
|-----------|-------|
| 📄 **Upload PDF** | Tải lên CV dạng PDF, hệ thống tự trích xuất văn bản |
| ✍️ **Phân tích văn bản** | Dán nội dung CV trực tiếp để phân tích ngay |
| 📦 **Batch Processing** | Upload & phân tích nhiều CV cùng lúc (tối đa 20 file) |
| 🏷️ **Phân loại ngành** | Dự đoán ngành nghề với xác suất % từng ngành |
| 👤 **Trích xuất tên** | Tự động nhận diện tên ứng viên từ nội dung CV |
| 📊 **Lịch sử phân tích** | Xem lại tất cả các lần phân tích theo thời gian |
| 🗑️ **Quản lý lịch sử** | Xóa từng bản ghi lịch sử dễ dàng |
| 📡 **Swagger API Docs** | Tài liệu API tự động tại `/docs` |

---

## 💻 Ngôn ngữ lập trình

| Ngôn ngữ | Phiên bản | Dùng ở đâu |
|----------|-----------|-------------|
| **Python** | 3.10+ | Backend API, ML pipeline, xử lý PDF, OCR |
| **JavaScript (ES6+)** | — | Frontend React, logic giao diện, gọi API |
| **CSS3** | — | Thiết kế giao diện (Vanilla CSS + Bootstrap 5) |
| **JSON** | — | Định dạng trao đổi dữ liệu REST API |

---

## 🛠️ Công nghệ sử dụng

### 🐍 Backend — Python

| Thư viện | Phiên bản | Vai trò |
|----------|-----------|---------|
| **FastAPI** | ≥ 0.110.0 | Web framework API RESTful bất đồng bộ (async) |
| **Uvicorn** | ≥ 0.29.0 | ASGI server chạy FastAPI |
| **scikit-learn** | ≥ 1.4.0 | Machine Learning: SVM, TF-IDF, Pipeline |
| **pandas** | ≥ 2.0.0 | Xử lý dữ liệu bảng (đọc CSV dataset) |
| **numpy** | ≥ 1.26.0 | Tính toán số học, xử lý ma trận |
| **joblib** | ≥ 1.3.0 | Lưu/tải mô hình ML (.pkl) |
| **pypdf** | ≥ 4.0.0 | Trích xuất văn bản từ file PDF |
| **pdfplumber** | ≥ 0.10.0 | Đọc PDF chi tiết từng trang |
| **pymongo** | ≥ 4.6.0 | Kết nối và thao tác với MongoDB |
| **pydantic** | ≥ 2.0.0 | Validation dữ liệu và schema |
| **python-multipart** | ≥ 0.0.9 | Hỗ trợ upload file |
| **pytesseract** | ≥ 0.3.10 | OCR — nhận diện chữ từ ảnh/PDF scan |
| **Pillow** | ≥ 10.0.0 | Xử lý ảnh (hỗ trợ OCR) |
| **pdf2image** | ≥ 1.17.0 | Chuyển PDF scan sang ảnh để OCR |

### ⚛️ Frontend — JavaScript / React

| Thư viện | Phiên bản | Vai trò |
|----------|-----------|---------|
| **React** | ^18.3.1 | UI framework component-based |
| **React DOM** | ^18.3.1 | Render React vào trình duyệt |
| **Bootstrap** | ^5.3.8 | CSS framework responsive |
| **Bootstrap Icons** | ^1.13.1 | Bộ icon vector đẹp |
| **Axios** | — | HTTP client gọi REST API backend |
| **react-scripts** | 5.0.1 | Build tool (Create React App) |

### 🗄️ Database

| Công nghệ | Vai trò |
|-----------|---------|
| **MongoDB** | Lưu trữ lịch sử phân tích CV (NoSQL document store) |

---

## 🧠 Thuật toán AI/ML

### 1. 🔢 TF-IDF — Term Frequency Inverse Document Frequency

Chuyển đổi **văn bản CV thành vector số học** để mô hình ML có thể xử lý.

```
TF-IDF(t, d) = TF(t, d) × log(N / DF(t))
```

- **TF:** tần suất xuất hiện của từ `t` trong tài liệu `d`
- **IDF:** log nghịch đảo số tài liệu chứa từ `t` — giảm trọng số từ phổ biến

**Cấu hình trong dự án:**
```python
TfidfVectorizer(
    max_features=10000,  # Giữ 10.000 từ quan trọng nhất
    ngram_range=(1, 2),  # Đơn từ + cặp từ (bigram)
    sublinear_tf=True,   # Dùng log(1+tf) thay vì tf thô
)
```

---

### 2. 🎯 SVM — Support Vector Machine (Thuật toán chính)

Phân loại ngành nghề của CV dựa trên vector TF-IDF.

- Tìm **siêu phẳng (hyperplane)** tối ưu phân tách các lớp ngành nghề
- Tối đa hóa **margin** — khoảng cách giữa các lớp
- **Linear SVM** đặc biệt hiệu quả cho text classification

**Cấu hình trong dự án:**
```python
SVC(
    kernel="linear",   # Kernel tuyến tính — lý tưởng cho văn bản
    C=1.0,             # Regularization — cân bằng fit vs. generalize
    probability=True,  # Bật xác suất (Platt scaling)
    random_state=42,
)
```

> **Tại sao chọn SVM?**  
> SVM là lựa chọn hàng đầu cho text classification vì hoạt động rất tốt với không gian chiều cao (10.000+ features), dữ liệu thưa (sparse TF-IDF vectors), và ít bị overfit hơn các mô hình phức tạp.

---

### 3. ⚙️ Pipeline ML (scikit-learn)

Toàn bộ quy trình được đóng gói trong một **Pipeline** nhất quán:

```
Văn bản CV (raw text)
        │
        ▼
 ┌─────────────────────┐
 │  TF-IDF Vectorizer  │  → ma trận số học (10.000 features)
 └──────────┬──────────┘
            │
            ▼
 ┌─────────────────────┐
 │   SVM Classifier    │  → chỉ số ngành (encoded)
 └──────────┬──────────┘
            │
            ▼
 ┌─────────────────────┐
 │   Label Decoder     │  → tên ngành ("IT", "Finance", ...)
 └──────────┬──────────┘
            │
            ▼
  Ngành dự đoán + Độ tin cậy + Xác suất từng ngành
```

---

### 4. 🏷️ Label Encoding

Chuyển đổi nhãn ngành nghề (chuỗi) ↔ số nguyên để SVM xử lý:

```python
LabelEncoder()
# Ví dụ: "IT" → 2, "Finance" → 1, "Marketing" → 3
```

---

### 5. 🔍 OCR — Optical Character Recognition

Trích xuất văn bản từ CV dạng **scan / ảnh** (PDF scan, JPG, PNG).

**Công nghệ:** Tesseract OCR (Google) qua `pytesseract`

```python
pytesseract.image_to_string(image, lang="vie+eng")  # Tiếng Việt + Anh
```

**Quy trình PDF scan:**
```
PDF scan → pdf2image (DPI=300) → Tesseract OCR → Văn bản thuần
```

---

### 6. 👤 Trích xuất tên ứng viên (Rule-based NLP)

Tự động nhận diện tên ứng viên từ các dòng đầu của CV bằng quy tắc ngôn ngữ:

- Quét **8 dòng đầu** của CV
- Tìm dòng gồm **2–5 từ**, mỗi từ bắt đầu chữ **viết hoa**
- Hỗ trợ đầy đủ **tiếng Việt có dấu** (à, á, ả, ã, ạ, ă, â, đ, ...)

```python
re.match(r"^[A-ZÁÀẢÃẠĂẮẶẰẲẴÂẤẬẦẨẪĐ...]", word)
```

---

### Tổng quan luồng xử lý

```
[Upload PDF / Nhập Text]
         │
         ▼
[Trích xuất văn bản]
 pypdf / pdfplumber / Tesseract OCR
         │
         ▼
[ML Pipeline: TF-IDF → SVM]
   → Ngành dự đoán
   → Độ tin cậy (confidence)
   → Xác suất từng ngành
         │
         ▼
[Trích xuất tên — Rule-based NLP]
         │
         ▼
[Lưu MongoDB — collection: cv_history]
         │
         ▼
[Trả JSON về Frontend]
```

---

## 🏗️ Kiến trúc hệ thống

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTEND (React 18)                        │
│   http://localhost:3000                                       │
│                                                               │
│  ┌────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │  UploadCV  │ │  Result  │ │ History  │ │ BatchResult  │  │
│  └────────────┘ └──────────┘ └──────────┘ └──────────────┘  │
└─────────────────────────┬────────────────────────────────────┘
                          │ HTTP REST API (proxy)
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI + Uvicorn)                  │
│   http://localhost:8000                                       │
│                                                               │
│  ┌──────────────────────┐   ┌──────────────────────────────┐ │
│  │   /predict/file      │   │   /history         GET       │ │
│  │   /predict/text      │   │   /history/{id}    GET       │ │
│  │   /predict/batch     │   │   /history/{id}    DELETE    │ │
│  └──────────┬───────────┘   └──────────────┬───────────────┘ │
│             │                              │                  │
│  ┌──────────▼───────────┐   ┌─────────────▼───────────────┐  │
│  │   ML Engine          │   │   MongoDB (PyMongo)          │  │
│  │   SVM + TF-IDF       │   │   DB: talentiq               │  │
│  │   Pipeline (.pkl)    │   │   Collection: cv_history     │  │
│  └──────────────────────┘   └─────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 Cấu trúc thư mục

```
cv-ai-service/
│
├── 📂 backend/                      # Backend Python/FastAPI
│   ├── main.py                      # FastAPI app — tất cả endpoints
│   ├── predict.py                   # Module dự đoán (load model, infer)
│   ├── train_model.py               # Script huấn luyện mô hình SVM
│   ├── db.py                        # Kết nối MongoDB
│   ├── requirements.txt             # Thư viện Python
│   ├── 📂 dataset/
│   │   └── cv_industry_dataset.csv  # Dataset CSV huấn luyện
│   └── 📂 model/
│       ├── svm_model.pkl            # Mô hình SVM đã huấn luyện
│       └── label_encoder.pkl        # Label encoder
│
├── 📂 frontend/                     # Frontend React
│   ├── package.json
│   └── 📂 src/
│       ├── App.js                   # Component gốc, quản lý state
│       ├── App.css
│       ├── index.js
│       └── 📂 components/
│           ├── UploadCV.js          # Upload & phân tích CV
│           ├── UploadCV.css
│           ├── Result.js            # Hiển thị kết quả phân tích đơn
│           ├── Result.css
│           ├── BatchResult.js       # Kết quả phân tích hàng loạt
│           ├── BatchResult.css
│           ├── History.js           # Danh sách lịch sử phân tích
│           └── History.css
│
├── 📂 utils/                        # Tiện ích dùng chung
│   ├── __init__.py
│   ├── pdf_reader.py                # Đọc PDF bằng pdfplumber
│   └── ocr_reader.py                # OCR ảnh/PDF scan bằng Tesseract
│
├── train_model.py                   # Script huấn luyện (RandomForest, thử nghiệm)
├── predict.py                       # Script predict CLI độc lập
├── main.py                          # Entry point chạy server
├── requirements.txt                 # Requirements tổng
├── create_sample_cv.py              # Tạo CV mẫu để test
└── README.md
```

---

## 💡 Yêu cầu hệ thống

| Công cụ | Phiên bản tối thiểu |
|---------|---------------------|
| Python | 3.10+ |
| Node.js | 18.x+ |
| npm | 9.x+ |
| MongoDB | 6.0+ |
| Tesseract OCR | 5.x *(tuỳ chọn, cho PDF scan)* |

> **Cài Tesseract trên Windows:**  
> Tải tại: https://github.com/UB-Mannheim/tesseract/wiki  
> Thêm language pack tiếng Việt `vie` để hỗ trợ CV tiếng Việt.

---

## 🚀 Hướng dẫn cài đặt

### Bước 1: Clone dự án

```bash
git clone https://github.com/Lekhoa-2912/cv-ai-service.git
cd cv-ai-service
```

### Bước 2: Cài đặt Backend

```bash
# Tạo và kích hoạt môi trường ảo
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# Cài thư viện
pip install -r backend/requirements.txt
```

### Bước 3: Cài đặt Frontend

```bash
cd frontend
npm install
cd ..
```

### Bước 4: Cấu hình MongoDB

Mặc định kết nối `mongodb://localhost:27017`. Để dùng URI tùy chỉnh:

```bash
# Windows PowerShell
$env:MONGO_URI = "mongodb+srv://user:password@cluster.mongodb.net"

# Linux / macOS
export MONGO_URI="mongodb+srv://user:password@cluster.mongodb.net"
```

---

## 🏋️ Huấn luyện mô hình

### Chuẩn bị dataset

File CSV cần có 2 cột:

| Cột | Mô tả |
|-----|-------|
| `resume_text` | Nội dung văn bản CV |
| `industry` | Nhãn ngành nghề |

Đặt tại: `backend/dataset/cv_industry_dataset.csv`

### Chạy huấn luyện

```bash
cd backend
python train_model.py
```

**Output mẫu:**
```
[INFO] Đang tải dữ liệu từ: dataset/cv_industry_dataset.csv
[INFO] Tổng số mẫu: 1200
[INFO] Số nhãn (industries): 8
[INFO] Train: 960 | Test: 240
[INFO] Đang huấn luyện mô hình SVM...

[RESULT] Độ chính xác: 94.58%

[INFO] ✅ Mô hình SVM đã lưu: model/svm_model.pkl
[INFO] ✅ Label encoder đã lưu: model/label_encoder.pkl
```

---

## ▶️ Chạy ứng dụng

### Chạy Backend

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

| URL | Mô tả |
|-----|-------|
| http://localhost:8000 | Backend API |
| http://localhost:8000/docs | Swagger UI — tài liệu API tương tác |

### Chạy Frontend

```bash
cd frontend
npm start
```

| URL | Mô tả |
|-----|-------|
| http://localhost:3000 | Giao diện người dùng |

---

## 📡 API Reference

### Endpoints tổng quan

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/` | Kiểm tra server |
| GET | `/health` | Trạng thái server + model + MongoDB |
| POST | `/predict/file` | Phân tích từ file PDF |
| POST | `/predict/text` | Phân tích từ văn bản thuần |
| POST | `/predict/batch` | Phân tích nhiều PDF cùng lúc (≤ 20) |
| GET | `/history` | Lấy danh sách lịch sử (phân trang) |
| GET | `/history/{id}` | Lấy chi tiết một bản ghi |
| DELETE | `/history/{id}` | Xóa một bản ghi |

### Response mẫu — `POST /predict/file`

```json
{
  "success": true,
  "data": {
    "predicted_industry": "Information Technology",
    "confidence": 0.9231,
    "probabilities": {
      "Information Technology": 0.9231,
      "Finance": 0.0412,
      "Marketing": 0.0357
    },
    "candidate_name": "Nguyễn Văn Minh",
    "history_id": "65f3a1b2c3d4e5f6a7b8c9d0"
  }
}
```

### Response mẫu — `POST /predict/batch`

```json
{
  "success": true,
  "total": 3,
  "success_count": 2,
  "fail_count": 1,
  "data": [
    { "file_name": "cv1.pdf", "success": true,  "data": { "..." } },
    { "file_name": "cv2.pdf", "success": true,  "data": { "..." } },
    { "file_name": "cv3.pdf", "success": false, "error": "Không trích được nội dung" }
  ]
}
```

---

<div align="center">

**Được phát triển với ❤️ bằng Python · React · Machine Learning (SVM)**

</div>