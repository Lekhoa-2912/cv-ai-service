import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from typing import List, Optional

import pypdf
from bson import ObjectId
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db import get_history_col, ping
from predict import predict_industry

# ══════════════════════════════════════════════════════════
# KHỞI TẠO FASTAPI
# ══════════════════════════════════════════════════════════
app = FastAPI(
    title="TalentIQ CV API",
    description="API phân tích CV + lưu lịch sử bằng MongoDB",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ══════════════════════════════════════════════════════════
# SCHEMAS
# ══════════════════════════════════════════════════════════
class TextRequest(BaseModel):
    text: str
    candidate_name: Optional[str] = None   # tên ứng viên (tuỳ chọn)


class PredictResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None


# ══════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════
ALLOWED_EXT = {".pdf"}


def extract_text_from_pdf(path: str) -> str:
    text = ""
    reader = pypdf.PdfReader(path)
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text.strip()


def extract_name_from_text(text: str) -> str:
    """
    Trích tên ứng viên từ văn bản CV.
    Ưu tiên: 2–4 từ viết hoa liền nhau ở các dòng đầu.
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for line in lines[:8]:          # chỉ tìm trong 8 dòng đầu
        words = line.split()
        # Tên thường 2-5 từ, mỗi từ bắt đầu bằng chữ hoa hoặc ALL CAPS
        if 2 <= len(words) <= 5 and all(
            re.match(r"^[A-ZÁÀẢÃẠĂẮẶẰẲẴÂẤẬẦẨẪĐÉÈẺẼẸÊẾỆỀỂỄÍÌỈĨỊÓÒỎÕỌÔỐỘỒỔỖƠỚỢỜỞỠÚÙỦŨỤƯỨỰỪỬỮÝỲỶỸỴ"
                     r"A-Z]", w, re.IGNORECASE) for w in words
        ):
            return " ".join(w.title() for w in words)
    return "Không xác định"


def _doc_to_dict(doc: dict) -> dict:
    """Chuyển MongoDB doc sang dict JSON-serializable."""
    doc["id"] = str(doc.pop("_id"))
    if isinstance(doc.get("analyzed_at"), datetime):
        doc["analyzed_at"] = doc["analyzed_at"].isoformat()
    return doc


def save_history(
    candidate_name: str,
    file_name: str,
    result: dict,
) -> str:
    """Lưu kết quả phân tích vào MongoDB. Trả về id."""
    col = get_history_col()
    doc = {
        "candidate_name":     candidate_name,
        "file_name":          file_name,
        "predicted_industry": result["predicted_industry"],
        "confidence":         result["confidence"],
        "probabilities":      result["probabilities"],
        "analyzed_at":        datetime.now(tz=timezone.utc),
    }
    inserted = col.insert_one(doc)
    return str(inserted.inserted_id)


# ══════════════════════════════════════════════════════════
# ENDPOINTS — HEALTH
# ══════════════════════════════════════════════════════════
@app.get("/", tags=["Hệ thống"])
def root():
    return {"message": "TalentIQ CV API v3.0 đang hoạt động!", "status": "ok"}


@app.get("/health", tags=["Hệ thống"])
def health_check():
    mongo_ok = ping()
    return {
        "status":  "healthy",
        "model":   "SVM + TF-IDF",
        "mongodb": "connected" if mongo_ok else "disconnected",
    }


# ══════════════════════════════════════════════════════════
# ENDPOINTS — PREDICT
# ══════════════════════════════════════════════════════════
@app.post("/predict/file", response_model=PredictResponse, tags=["Phân tích"])
async def predict_from_file(file: UploadFile = File(...)):
    """Phân loại ngành từ file PDF. Tự động trích tên ứng viên & lưu lịch sử."""
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(400, detail=f"Chỉ chấp nhận file PDF (nhận được: '{ext}').")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        text = extract_text_from_pdf(tmp_path)
        if not text:
            return PredictResponse(
                success=False,
                error="Không thể trích nội dung từ PDF (có thể là file scan).",
            )

        result          = predict_industry(text)
        candidate_name  = extract_name_from_text(text)

        # Lưu lịch sử
        history_id = save_history(candidate_name, file.filename, result)
        result["history_id"]     = history_id
        result["candidate_name"] = candidate_name

        return PredictResponse(success=True, data=result)

    except FileNotFoundError as e:
        raise HTTPException(503, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Lỗi xử lý: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.post("/predict/batch", tags=["Phân tích"])
async def predict_batch(files: List[UploadFile] = File(...)):
    """
    Phân loại ngành từ NHIỀU file PDF cùng lúc.
    Trả về danh sách kết quả, mỗi file một bản ghi.
    Tất cả đều được lưu vào MongoDB lịch sử.
    """
    if len(files) > 20:
        raise HTTPException(400, detail="Tối đa 20 file mỗi lần upload.")

    results = []

    for file in files:
        ext = os.path.splitext(file.filename)[-1].lower()
        item = {
            "file_name": file.filename,
            "success":   False,
            "error":     None,
            "data":      None,
        }

        if ext not in ALLOWED_EXT:
            item["error"] = f"Không phải file PDF."
            results.append(item)
            continue

        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = tmp.name

            text = extract_text_from_pdf(tmp_path)
            if not text:
                item["error"] = "Không trích được nội dung (PDF scan?)."
                results.append(item)
                continue

            result         = predict_industry(text)
            candidate_name = extract_name_from_text(text)
            history_id     = save_history(candidate_name, file.filename, result)

            result["history_id"]     = history_id
            result["candidate_name"] = candidate_name
            result["file_name"]      = file.filename

            item["success"] = True
            item["data"]    = result

        except Exception as e:
            item["error"] = str(e)
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

        results.append(item)

    success_count = sum(1 for r in results if r["success"])
    return {
        "success":       True,
        "total":         len(results),
        "success_count": success_count,
        "fail_count":    len(results) - success_count,
        "data":          results,
    }


@app.post("/predict/text", response_model=PredictResponse, tags=["Phân tích"])
def predict_from_text(body: TextRequest):
    """Phân loại ngành từ văn bản CV thuần túy. Lưu lịch sử MongoDB."""
    try:
        result = predict_industry(body.text)

        # Tên: ưu tiên do user nhập, sau đó tự trích từ text
        candidate_name = (
            body.candidate_name.strip()
            if body.candidate_name and body.candidate_name.strip()
            else extract_name_from_text(body.text)
        )

        history_id = save_history(candidate_name, "text-input", result)
        result["history_id"]     = history_id
        result["candidate_name"] = candidate_name

        return PredictResponse(success=True, data=result)

    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(503, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Lỗi xử lý: {e}")


# ══════════════════════════════════════════════════════════
# ENDPOINTS — HISTORY
# ══════════════════════════════════════════════════════════
@app.get("/history", tags=["Lịch sử"])
def get_history(
    limit: int = Query(default=50, ge=1, le=200),
    skip:  int = Query(default=0,  ge=0),
):
    """Lấy danh sách lịch sử phân tích CV (mới nhất trước)."""
    try:
        col  = get_history_col()
        docs = list(
            col.find({}, {"probabilities": 0})   # bỏ probabilities cho gọn
               .sort("analyzed_at", -1)
               .skip(skip)
               .limit(limit)
        )
        return {
            "success": True,
            "total":   col.count_documents({}),
            "data":    [_doc_to_dict(d) for d in docs],
        }
    except Exception as e:
        raise HTTPException(500, detail=f"Lỗi lấy lịch sử: {e}")


@app.get("/history/{history_id}", tags=["Lịch sử"])
def get_history_detail(history_id: str):
    """Lấy chi tiết một lần phân tích (bao gồm probabilities)."""
    try:
        col = get_history_col()
        doc = col.find_one({"_id": ObjectId(history_id)})
        if not doc:
            raise HTTPException(404, detail="Không tìm thấy bản ghi.")
        return {"success": True, "data": _doc_to_dict(doc)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=f"Lỗi: {e}")


@app.delete("/history/{history_id}", tags=["Lịch sử"])
def delete_history(history_id: str):
    """Xoá một bản ghi lịch sử."""
    try:
        col    = get_history_col()
        result = col.delete_one({"_id": ObjectId(history_id)})
        if result.deleted_count == 0:
            raise HTTPException(404, detail="Không tìm thấy bản ghi.")
        return {"success": True, "message": "Đã xoá thành công."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=f"Lỗi: {e}")


# ══════════════════════════════════════════════════════════
# CHẠY SERVER
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
