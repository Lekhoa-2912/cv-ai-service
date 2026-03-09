import React, { useEffect, useState, useCallback } from "react";
import "./History.css";

const IND_COLOR = {
    "Công nghệ thông tin": "#4E7AFF",
    "Quản trị kinh doanh": "#F4A030",
    "Marketing": "#E040BA",
    "Tài chính - Kế toán": "#0ED4A0",
    "Nhân sự": "#9F6AFF",
    "Thiết kế": "#FF6B35",
    "Logistics": "#30C8FF",
    "Giáo dục": "#FFD166",
};

const IND_ICON = {
    "Công nghệ thông tin": "bi-cpu-fill",
    "Quản trị kinh doanh": "bi-briefcase-fill",
    "Marketing": "bi-megaphone-fill",
    "Tài chính - Kế toán": "bi-bank2",
    "Nhân sự": "bi-people-fill",
    "Thiết kế": "bi-palette-fill",
    "Logistics": "bi-truck",
    "Giáo dục": "bi-mortarboard-fill",
};

const getColor = (ind) => IND_COLOR[ind] ?? "#4E7AFF";
const getIcon = (ind) => IND_ICON[ind] ?? "bi-file-person";

function formatDate(iso) {
    const d = new Date(iso);
    return d.toLocaleString("vi-VN", {
        day: "2-digit", month: "2-digit", year: "numeric",
        hour: "2-digit", minute: "2-digit",
    });
}

function ConfBar({ value, color }) {
    const pct = (value * 100).toFixed(0);
    return (
        <div className="conf-wrap">
            <div className="conf-track">
                <div className="conf-fill" style={{ width: `${pct}%`, background: color }} />
            </div>
            <span className="conf-val" style={{ color }}>{pct}%</span>
        </div>
    );
}

export default function History() {
    const [records, setRecords] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [total, setTotal] = useState(0);
    const [deleting, setDeleting] = useState(null);

    const fetchHistory = useCallback(async () => {
        setLoading(true);
        setError("");
        try {
            const res = await fetch("http://localhost:8000/history?limit=100");
            const json = await res.json();
            if (!res.ok) throw new Error(json.detail || "Không thể tải lịch sử.");
            setRecords(json.data);
            setTotal(json.total);
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => { fetchHistory(); }, [fetchHistory]);

    const handleDelete = async (id) => {
        setDeleting(id);
        try {
            const res = await fetch(`http://localhost:8000/history/${id}`, { method: "DELETE" });
            if (!res.ok) throw new Error("Xoá thất bại.");
            setRecords((prev) => prev.filter((r) => r.id !== id));
            setTotal((t) => t - 1);
        } catch (e) {
            alert(e.message);
        } finally {
            setDeleting(null);
        }
    };

    /* ── LOADING ── */
    if (loading) return (
        <div className="hist-center">
            <div className="hist-spinner" />
            <p className="hist-msg">Đang tải lịch sử...</p>
        </div>
    );

    /* ── ERROR ── */
    if (error) return (
        <div className="hist-center">
            <div className="hist-error-icon"><i className="bi bi-exclamation-circle" /></div>
            <p className="hist-msg error">{error}</p>
            <button className="hist-retry-btn" onClick={fetchHistory}>Thử lại</button>
        </div>
    );

    /* ── EMPTY ── */
    if (records.length === 0) return (
        <div className="hist-center">
            <div className="hist-empty-icon"><i className="bi bi-clock-history" /></div>
            <p className="hist-msg">Chưa có lịch sử phân tích.</p>
            <p className="hist-sub">Phân tích một CV để bắt đầu ghi lại lịch sử.</p>
        </div>
    );

    return (
        <div className="hist-root">

            {/* ── HEADER ── */}
            <div className="hist-hdr">
                <div className="hist-hdr-left">
                    <span className="hist-total-badge">{total}</span>
                    <span className="hist-title">lượt phân tích đã lưu</span>
                </div>
                <button className="hist-refresh-btn" onClick={fetchHistory} title="Làm mới">
                    <i className="bi bi-arrow-clockwise" />
                </button>
            </div>

            {/* ── TABLE ── */}
            <div className="hist-table-wrap">
                <table className="hist-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Ứng viên</th>
                            <th>Ngành nghề</th>
                            <th>Độ phù hợp</th>
                            <th>File</th>
                            <th>Thời gian</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {records.map((r, idx) => {
                            const color = getColor(r.predicted_industry);
                            const icon = getIcon(r.predicted_industry);
                            return (
                                <tr key={r.id} className="hist-row">
                                    <td className="td-idx">{idx + 1}</td>

                                    <td className="td-name">
                                        <div className="name-avatar" style={{ background: `${color}22`, color }}>
                                            {r.candidate_name?.charAt(0)?.toUpperCase() ?? "?"}
                                        </div>
                                        <span className="name-text">{r.candidate_name}</span>
                                    </td>

                                    <td className="td-industry">
                                        <span className="industry-chip" style={{ color, borderColor: `${color}40`, background: `${color}12` }}>
                                            <i className={`bi ${icon}`} />
                                            {r.predicted_industry}
                                        </span>
                                    </td>

                                    <td className="td-conf">
                                        <ConfBar value={r.confidence} color={color} />
                                    </td>

                                    <td className="td-file">
                                        <span className="file-chip">
                                            <i className={`bi ${r.file_name === "text-input" ? "bi-textarea-t" : "bi-file-earmark-pdf"}`} />
                                            {r.file_name === "text-input" ? "Nhập text" : r.file_name}
                                        </span>
                                    </td>

                                    <td className="td-date">{formatDate(r.analyzed_at)}</td>

                                    <td className="td-action">
                                        <button
                                            className="del-btn"
                                            onClick={() => handleDelete(r.id)}
                                            disabled={deleting === r.id}
                                            title="Xoá"
                                        >
                                            {deleting === r.id
                                                ? <i className="bi bi-hourglass-split" />
                                                : <i className="bi bi-trash3" />}
                                        </button>
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
