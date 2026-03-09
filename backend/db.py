from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional
import os

# ── Cấu hình kết nối ──────────────────────────────────────
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME   = "talentiq"

_client: Optional[MongoClient] = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    return _client


def get_history_col() -> Collection:
    """Trả về collection cv_history."""
    return get_client()[DB_NAME]["cv_history"]


def ping() -> bool:
    """Kiểm tra kết nối MongoDB."""
    try:
        get_client().admin.command("ping")
        return True
    except Exception:
        return False
