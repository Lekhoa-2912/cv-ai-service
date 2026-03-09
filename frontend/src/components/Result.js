import React from "react";
import "./Result.css";

/* ─── Thông tin ngành nghề ─────────────────────────────── */
const IND = {
    "Công nghệ thông tin": { abbr: "CNTT", color: "#4E7AFF", icon: "bi-cpu-fill" },
    "Quản trị kinh doanh": { abbr: "QTKD", color: "#F4A030", icon: "bi-briefcase-fill" },
    "Marketing": { abbr: "MKT", color: "#E040BA", icon: "bi-megaphone-fill" },
    "Tài chính - Kế toán": { abbr: "TCKТ", color: "#0ED4A0", icon: "bi-bank2" },
    "Nhân sự": { abbr: "NS", color: "#9F6AFF", icon: "bi-people-fill" },
    "Thiết kế": { abbr: "TK", color: "#FF6B35", icon: "bi-palette-fill" },
    "Logistics": { abbr: "LOG", color: "#30C8FF", icon: "bi-truck" },
    "Giáo dục": { abbr: "GD", color: "#FFD166", icon: "bi-mortarboard-fill" },
};

const getMeta = (name) =>
    IND[name] ?? { abbr: "KH", color: "#4E7AFF", icon: "bi-file-person" };

/* ─── Vòng tròn độ tin cậy (SVG Arc) ──────────────────── */
function ArcDial({ value, color }) {
    const R = 34, CX = 42, CY = 42;
    const circ = 2 * Math.PI * R;
    const dash = circ * value;

    return (
        <svg className="arc-svg" viewBox="0 0 84 84">
            {/* Nền vòng */}
            <circle cx={CX} cy={CY} r={R}
                fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="5"
            />
            {/* Vòng điền */}
            <circle cx={CX} cy={CY} r={R}
                fill="none"
                stroke={color}
                strokeWidth="5"
                strokeDasharray={`${dash} ${circ}`}
                strokeLinecap="round"
                transform={`rotate(-90 ${CX} ${CY})`}
                style={{
                    transition: "stroke-dasharray 1.1s cubic-bezier(0.34,1.2,0.64,1)",
                    filter: `drop-shadow(0 0 7px ${color}88)`,
                }}
            />
            {/* Phần trăm */}
            <text x={CX} y={CY - 3}
                textAnchor="middle" dominantBaseline="auto"
                style={{ fill: "#EDF1FF", fontSize: "13px", fontWeight: 800, fontFamily: "Inter, sans-serif" }}
            >
                {Math.round(value * 100)}
            </text>
            <text x={CX} y={CY + 11}
                textAnchor="middle"
                style={{ fill: "rgba(237,241,255,0.32)", fontSize: "7px", fontFamily: "Inter, sans-serif", fontWeight: 600, letterSpacing: "0.06em" }}
            >
                PHÙ HỢP
            </text>
        </svg>
    );
}

/* ─── Component kết quả chính ──────────────────────────── */
export default function Result({ data }) {
    if (!data) return null;

    const { predicted_industry, confidence, probabilities } = data;
    const meta = getMeta(predicted_industry);
    const sorted = Object.entries(probabilities).sort((a, b) => b[1] - a[1]);
    const topVal = sorted[0]?.[1] ?? 1;

    const level =
        confidence >= 0.70 ? { label: "Khớp cao", cls: "lv-strong" } :
            confidence >= 0.45 ? { label: "Khả năng khớp", cls: "lv-likely" } :
                { label: "Tín hiệu yếu", cls: "lv-weak" };

    return (
        <div className="result-root" style={{ "--rc": meta.color }}>

            {/* ── ĐẦU KẾT QUẢ ── */}
            <div className="vd-head">
                <div className="vd-industry-col">
                    <div className="vd-eyebrow">Phân loại ngành nghề</div>
                    <div className="vd-industry-wrap">
                        <div className="vd-industry-icon">
                            <i className={`bi ${meta.icon}`} />
                        </div>
                        <div>
                            <div className="vd-name">{predicted_industry}</div>
                            <div
                                className="vd-abbr-badge"
                                style={{ color: meta.color, borderColor: `${meta.color}40` }}
                            >
                                {meta.abbr}
                            </div>
                        </div>
                    </div>
                    <div className={`vd-level-chip ${level.cls}`}>{level.label}</div>
                </div>

                <div className="vd-dial-col">
                    <ArcDial value={confidence} color={meta.color} />
                </div>
            </div>

            {/* ── ĐƯỜNG PHÂN CÁCH ── */}
            <div className="vd-divider" />

            {/* ── BẢNG XẾP HẠNG ── */}
            <div className="vd-breakdown">
                <div className="bd-header">
                    <span className="bd-title">Tất cả ngành — theo độ phù hợp</span>
                    <span className="bd-count">{sorted.length} ngành</span>
                </div>

                <div className="bd-list">
                    {sorted.map(([name, prob], idx) => {
                        const m = getMeta(name);
                        const pct = (prob * 100).toFixed(1);
                        const rel = topVal > 0 ? prob / topVal : 0;

                        return (
                            <div key={name} className={`bd-row ${idx === 0 ? "bd-top" : ""}`}>
                                <span className="bd-rank">{String(idx + 1).padStart(2, "0")}</span>

                                <span className="bd-icon" style={{ color: m.color }}>
                                    <i className={`bi ${m.icon}`} />
                                </span>

                                <span className="bd-name">{name}</span>

                                <div className="bd-track">
                                    <div
                                        className="bd-fill"
                                        style={{
                                            width: `${rel * 100}%`,
                                            background: idx === 0 ? m.color : "rgba(255,255,255,0.1)",
                                            boxShadow: idx === 0 ? `0 0 8px ${m.color}66` : "none",
                                        }}
                                    />
                                </div>

                                <span
                                    className="bd-pct"
                                    style={{ color: idx === 0 ? m.color : undefined }}
                                >
                                    {pct}%
                                </span>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
