from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import tempfile
from predict import predict_cv

# =====================================================================
# KHỞI TẠO ỨNG DỤNG
# =====================================================================
app = FastAPI(
    title="CV AI Service",
    description="API phân loại và phân tích CV bằng Machine Learning",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================================
# ENDPOINTS
# =====================================================================

@app.get("/", tags=["Health"])
def root():
    """Kiểm tra trạng thái API."""
    return {"message": "CV AI Service đang hoạt động!", "status": "ok"}


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/predict", tags=["Prediction"])
async def predict(
    file: UploadFile = File(...),
    use_ocr: bool = False,
):
    """
    Phân loại CV từ file PDF hoặc ảnh.

    - **file**: File CV (PDF, PNG, JPG, ...)
    - **use_ocr**: Sử dụng OCR để xử lý PDF dạng scan (mặc định: False)
    """
    allowed_extensions = {".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tiff"}
    ext = os.path.splitext(file.filename)[-1].lower()

    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Định dạng file không hỗ trợ: {ext}. Chấp nhận: {allowed_extensions}",
        )

    # Lưu file tạm thời
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        result = predict_cv(tmp_path, use_ocr=use_ocr)
        return {"success": True, "data": result}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.post("/predict-text", tags=["Prediction"])
def predict_from_text(text: str):
    """
    Phân loại CV từ văn bản thuần túy.

    - **text**: Nội dung CV dạng text
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Văn bản CV không được để trống.")

    try:
        from predict import load_model
        pipeline, label_encoder = load_model()

        prediction_encoded = pipeline.predict([text])[0]
        probabilities = pipeline.predict_proba([text])[0]
        label = label_encoder.inverse_transform([prediction_encoded])[0]
        classes = label_encoder.classes_
        prob_dict = {cls: round(float(prob), 4) for cls, prob in zip(classes, probabilities)}

        return {
            "success": True,
            "data": {
                "prediction": label,
                "confidence": round(float(max(probabilities)), 4),
                "probabilities": prob_dict,
            },
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý: {str(e)}")


# =====================================================================
# CHẠY SERVER
# =====================================================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
