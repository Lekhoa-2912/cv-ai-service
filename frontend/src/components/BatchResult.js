import React from "react";
import "./BatchResult.css";

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

/* ── Dải màu confidence ── */
function ConfBar({ value, color }) {
    const pct = (value * 100).toFixed(0);
    return (
        <div className="br-conf-wrap">
            <div className="br-conf-track">
                <div className="br-conf-fill" style={{ width: `${pct}%`, background: color }} />
            </div>
            <span className="br-conf-val" style={{ color }}>{pct}%</span>
        </div>
    );
}

export default function BatchResult({ batchData }) {
    const { total, success_count, fail_count, data } = batchData;

    return (
        <div className="br-root">

            {/* ── TỔNG KẾT ── */}
            <div className="br-summary">
                <div className="br-stat">
                    <span className="br-stat-val">{total}</span>
                    <span className="br-stat-lbl">Tổng CV</span>
                </div>
                <div className="br-stat success">
                    <span className="br-stat-val">{success_count}</span>
                    <span className="br-stat-lbl">Thành công</span>
                </div>
                {fail_count > 0 && (
                    <div className="br-stat fail">
                        <span className="br-stat-val">{fail_count}</span>
                        <span className="br-stat-lbl">Thất bại</span>
                    </div>
                )}
            </div>

            {/* ── DANH SÁCH KẾT QUẢ ── */}
            <div className="br-list">
                {data.map((item, idx) => {
                    if (!item.success) {
                        return (
                            <div key={idx} className="br-row br-row-fail">
                                <div className="br-row-num">{String(idx + 1).padStart(2, "0")}</div>
                                <div className="br-row-file">
                                    <i className="bi bi-file-earmark-pdf" />
                                    <span>{item.file_name}</span>
                                </div>
                                <div className="br-row-error">
                                    <i className="bi bi-exclamation-triangle-fill" />
                                    {item.error}
                                </div>
                            </div>
                        );
                    }

                    const d = item.data;
                    const color = getColor(d.predicted_industry);
                    const icon = getIcon(d.predicted_industry);

                    return (
                        <div key={idx} className="br-row">
                            <div className="br-row-num">{String(idx + 1).padStart(2, "0")}</div>

                            {/* Tên ứng viên */}
                            <div className="br-row-candidate">
                                <div className="br-avatar" style={{ background: `${color}22`, color }}>
                                    {d.candidate_name?.charAt(0)?.toUpperCase() ?? "?"}
                                </div>
                                <div className="br-candidate-info">
                                    <span className="br-cname">{d.candidate_name}</span>
                                    <span className="br-fname">{item.file_name}</span>
                                </div>
                            </div>

                            {/* Ngành */}
                            <div className="br-row-industry">
                                <span
                                    className="br-industry-chip"
                                    style={{ color, background: `${color}15`, borderColor: `${color}35` }}
                                >
                                    <i className={`bi ${icon}`} />
                                    {d.predicted_industry}
                                </span>
                            </div>

                            {/* Độ tin cậy */}
                            <div className="br-row-conf">
                                <ConfBar value={d.confidence} color={color} />
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
