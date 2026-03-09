import React, { useState } from "react";
import UploadCV from "./components/UploadCV";
import Result from "./components/Result";
import BatchResult from "./components/BatchResult";
import History from "./components/History";
import "./App.css";

const NAV = [
    { id: "analyze", icon: "bi-cpu", label: "Phân tích" },
    { id: "history", icon: "bi-clock-history", label: "Lịch sử" },
    { id: "pipeline", icon: "bi-kanban", label: "Ứng viên" },
];

const STATS = [
    { val: "8", unit: "ngành", lbl: "Ngành được phân loại" },
    { val: "SVM", unit: "", lbl: "Kiến trúc mô hình" },
    { val: "100%", unit: "", lbl: "Pipeline TF-IDF" },
    { val: "<1s", unit: "", lbl: "Thời gian xử lý" },
];

export default function App() {
    const [activeNav, setActiveNav] = useState("analyze");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [theme, setTheme] = useState(
        () => localStorage.getItem("talentiq-theme") || "dark"
    );

    const toggleTheme = () => {
        const next = theme === "dark" ? "light" : "dark";
        setTheme(next);
        localStorage.setItem("talentiq-theme", next);
    };

    return (
        <div className="app-shell" data-theme={theme}>

            {/* ══ THANH RAIL ══ */}
            <aside className="rail">
                <div className="rail-logo">T</div>

                <nav className="rail-nav">
                    {NAV.map((n) => (
                        <button
                            key={n.id}
                            className={`rail-item ${activeNav === n.id ? "is-active" : ""}`}
                            onClick={() => setActiveNav(n.id)}
                        >
                            <i className={`bi ${n.icon}`} />
                            <span className="rail-tooltip">{n.label}</span>
                        </button>
                    ))}

                    <div className="rail-divider" />

                    <button className="rail-item">
                        <i className="bi bi-gear" />
                        <span className="rail-tooltip">Cài đặt</span>
                    </button>
                </nav>

                <div className="rail-avatar" title="Tài khoản">JD</div>
            </aside>

            {/* ══ NỘI DUNG CHÍNH ══ */}
            <div className="main-body">

                {/* THANH TRÊN */}
                <header className="top-bar">
                    <div className="topbar-left">
                        <span className="brand-name">TalentIQ · Tuyển dụng AI</span>
                        <span className="model-badge">
                            <span className="badge-dot" />
                            SVM · TF-IDF · v3.0
                        </span>
                    </div>
                    <div className="topbar-right">
                        <span className="api-status">
                            <span className="status-pulse" />
                            API hoạt động
                        </span>
                        <span className="topbar-ver">localhost:8000</span>
                        {/* NÚt đổi chế độ */}
                        <button className="theme-toggle" onClick={toggleTheme} title={theme === 'dark' ? 'Chuyển sang sáng' : 'Chuyển sang tối'}>
                            {theme === "dark"
                                ? <i className="bi bi-sun-fill" />
                                : <i className="bi bi-moon-stars-fill" />}
                        </button>
                    </div>
                </header>

                {/* TRANG */}
                <main className="page-content">

                    {/* ── PHÂN TÍCH CV ── */}
                    {activeNav === "analyze" && (
                        <>
                            <div className="page-hdr">
                                <div className="page-hdr-left">
                                    <div className="page-eyebrow">AI · Tuyển dụng</div>
                                    <h1 className="page-headline">Phân tích CV</h1>
                                    <p className="page-desc">
                                        Tải lên hồ sơ — mô hình SVM phân loại ngành nghề trong tích tắc.
                                    </p>
                                </div>
                            </div>

                            {/* DẢI THỐNG KÊ */}
                            <div className="stats-strip">
                                {STATS.map((s) => (
                                    <div key={s.lbl} className="stat-cell">
                                        <div className="stat-val">
                                            {s.val}
                                            {s.unit && <span>{s.unit}</span>}
                                        </div>
                                        <div className="stat-lbl">{s.lbl}</div>
                                    </div>
                                ))}
                            </div>

                            {/* LƯỚI 2 PANEL */}
                            <div className="work-grid">

                                {/* BẢNG ĐẦU VÀO */}
                                <div className="panel">
                                    <div className="panel-hdr">
                                        <div className="panel-hdr-left">
                                            <span className="panel-dot blue" />
                                            <span className="panel-title">Đầu vào</span>
                                        </div>
                                        <span className="panel-badge">PDF · Văn bản</span>
                                    </div>
                                    <UploadCV onResult={setResult} onLoading={setLoading} />
                                </div>

                                {/* BẢNG KẾT QUẢ */}
                                <div className="panel">
                                    <div className="panel-hdr">
                                        <div className="panel-hdr-left">
                                            <span className={`panel-dot ${result ? "green" : "amber"}`} />
                                            <span className="panel-title">Kết quả</span>
                                        </div>
                                        {result && (
                                            <span className="panel-badge" style={{ color: "var(--green)" }}>
                                                ✓ Đã phân loại
                                            </span>
                                        )}
                                    </div>

                                    {loading ? (
                                        <div className="loading-state">
                                            <div className="scan-box">
                                                <div className="scan-beam" />
                                            </div>
                                            <p className="loading-label">
                                                Đang phân tích hồ sơ
                                                <span className="ellipsis" />
                                            </p>
                                        </div>
                                    ) : result?.type === "single" ? (
                                        <Result data={result.data} />
                                    ) : result?.type === "batch" ? (
                                        <BatchResult batchData={result.data} />
                                    ) : (
                                        <div className="empty-state">
                                            <div className="empty-icon">
                                                <i className="bi bi-file-earmark-person" />
                                            </div>
                                            <p className="empty-hd">Chưa có dữ liệu</p>
                                            <p className="empty-bd">
                                                Tải lên PDF hoặc dán nội dung CV
                                                <br />
                                                để nhận kết quả phân loại ngành nghề.
                                            </p>
                                        </div>
                                    )}
                                </div>

                            </div>
                        </>
                    )}

                    {/* ── LỊCH SỬ ── */}
                    {activeNav === "history" && (
                        <>
                            <div className="page-hdr">
                                <div className="page-hdr-left">
                                    <div className="page-eyebrow">MongoDB · Lưu trữ</div>
                                    <h1 className="page-headline">Lịch sử phân tích</h1>
                                    <p className="page-desc">
                                        Toàn bộ CV đã được phân tích — lưu tự động vào MongoDB.
                                    </p>
                                </div>
                            </div>

                            <div className="panel">
                                <div className="panel-hdr">
                                    <div className="panel-hdr-left">
                                        <span className="panel-dot blue" />
                                        <span className="panel-title">Danh sách ứng viên</span>
                                    </div>
                                    <span className="panel-badge">MongoDB</span>
                                </div>
                                <History />
                            </div>
                        </>
                    )}

                    {/* ── ỨNG VIÊN (placeholder) ── */}
                    {activeNav === "pipeline" && (
                        <div className="empty-state" style={{ padding: "80px 24px" }}>
                            <div className="empty-icon">
                                <i className="bi bi-kanban" />
                            </div>
                            <p className="empty-hd">Tính năng đang phát triển</p>
                            <p className="empty-bd">
                                Quản lý pipeline ứng viên sẽ có trong phiên bản tiếp theo.
                            </p>
                        </div>
                    )}

                </main>
            </div>
        </div>
    );
}
