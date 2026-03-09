import React, { useState } from "react";
import "./UploadCV.css";

const MAX_FILES = 20;

export default function UploadCV({ onResult, onLoading }) {
  const [mode, setMode] = useState("file");
  const [files, setFiles] = useState([]);       // multi-file list
  const [text, setText] = useState("");
  const [dragging, setDragging] = useState(false);
  const [error, setError] = useState("");
  const [progress, setProgress] = useState(null);     // "x/y đang xử lý"

  /* ── Thêm files (lọc trùng và chỉ PDF) ── */
  const addFiles = (incoming) => {
    const pdfs = Array.from(incoming).filter(f => f.type === "application/pdf");
    const invalid = Array.from(incoming).length - pdfs.length;
    if (invalid > 0) setError(`${invalid} file không phải PDF đã bị bỏ qua.`);
    else setError("");

    setFiles(prev => {
      const names = new Set(prev.map(f => f.name));
      const news = pdfs.filter(f => !names.has(f.name));
      const merged = [...prev, ...news].slice(0, MAX_FILES);
      if (merged.length === MAX_FILES) setError(`Tối đa ${MAX_FILES} file mỗi lần.`);
      return merged;
    });
  };

  const removeFile = (idx) =>
    setFiles(prev => prev.filter((_, i) => i !== idx));

  /* ── Submit ── */
  const handleSubmit = async () => {
    setError("");
    onLoading(true);
    onResult(null);
    setProgress(null);

    try {
      if (mode === "text") {
        /* ─ Chế độ text: 1 CV ─ */
        if (!text.trim()) { setError("Vui lòng nhập nội dung CV."); onLoading(false); return; }
        const res = await fetch("http://localhost:8000/predict/text", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text }),
        });
        const json = await res.json();
        if (!res.ok || !json.success) throw new Error(json.detail || json.error || "Lỗi server.");
        onResult({ type: "single", data: json.data });

      } else if (files.length === 1) {
        /* ─ 1 file: dùng endpoint đơn ─ */
        const fd = new FormData();
        fd.append("file", files[0]);
        setProgress("1/1 đang xử lý...");
        const res = await fetch("http://localhost:8000/predict/file", { method: "POST", body: fd });
        const json = await res.json();
        if (!res.ok || !json.success) throw new Error(json.detail || json.error || "Lỗi server.");
        onResult({ type: "single", data: json.data });

      } else if (files.length > 1) {
        /* ─ Nhiều file: dùng endpoint batch ─ */
        if (files.length === 0) { setError("Vui lòng chọn ít nhất 1 file PDF."); onLoading(false); return; }
        const fd = new FormData();
        files.forEach(f => fd.append("files", f));
        setProgress(`0/${files.length} đang xử lý...`);
        const res = await fetch("http://localhost:8000/predict/batch", { method: "POST", body: fd });
        const json = await res.json();
        if (!res.ok) throw new Error(json.detail || "Lỗi server.");
        onResult({ type: "batch", data: json });

      } else {
        setError("Vui lòng chọn ít nhất 1 file PDF.");
        onLoading(false);
        return;
      }
    } catch (e) {
      setError(e.message);
    } finally {
      onLoading(false);
      setProgress(null);
    }
  };

  const totalSize = files.reduce((s, f) => s + f.size, 0);

  return (
    <div className="upcv-root">

      {/* ── TABS ── */}
      <div className="upcv-tabs">
        <button className={`upcv-tab ${mode === "file" ? "active" : ""}`} onClick={() => setMode("file")}>
          <i className="bi bi-file-earmark-pdf" /> PDF Upload
        </button>
        <button className={`upcv-tab ${mode === "text" ? "active" : ""}`} onClick={() => setMode("text")}>
          <i className="bi bi-textarea-t" /> Nhập văn bản
        </button>
      </div>

      {/* ── FILE MODE ── */}
      {mode === "file" && (
        <>
          {/* Drop zone */}
          <div
            className={`drop-zone ${dragging ? "dz-over" : ""} ${files.length > 0 ? "dz-filled dz-multi" : ""}`}
            onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
            onDragLeave={() => setDragging(false)}
            onDrop={(e) => { e.preventDefault(); setDragging(false); addFiles(e.dataTransfer.files); }}
            onClick={() => document.getElementById("cv-input").click()}
          >
            <input
              id="cv-input" type="file" accept=".pdf" hidden multiple
              onChange={(e) => addFiles(e.target.files)}
            />

            {files.length === 0 ? (
              <div className="dz-placeholder">
                <div className="dz-ring"><i className="bi bi-cloud-arrow-up-fill" /></div>
                <p className="dz-primary">Kéo thả file PDF vào đây</p>
                <p className="dz-secondary">hoặc <span className="dz-link">click để chọn file</span></p>
                <div className="dz-format-chip">
                  <i className="bi bi-files" /> Nhiều file · Chỉ PDF · Tối đa {MAX_FILES} CV
                </div>
              </div>
            ) : (
              <div className="dz-multi-hint" onClick={e => e.stopPropagation()}>
                <i className="bi bi-plus-circle" />
                <span>Thêm file (click hoặc kéo thả)</span>
              </div>
            )}
          </div>

          {/* Danh sách files đã chọn */}
          {files.length > 0 && (
            <div className="file-list">
              <div className="file-list-hdr">
                <span className="fl-count">
                  <i className="bi bi-files" /> {files.length} file
                  <span> · {(totalSize / 1024).toFixed(0)} KB tổng</span>
                </span>
                <button className="fl-clear-all" onClick={() => setFiles([])}>
                  Xoá tất cả
                </button>
              </div>

              {files.map((f, idx) => (
                <div key={`${f.name}-${idx}`} className="file-row">
                  <div className="file-row-icon"><i className="bi bi-file-earmark-pdf-fill" /></div>
                  <div className="file-row-info">
                    <span className="file-row-name">{f.name}</span>
                    <span className="file-row-size">{(f.size / 1024).toFixed(0)} KB</span>
                  </div>
                  <button className="file-row-del" onClick={() => removeFile(idx)}>
                    <i className="bi bi-x" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      {/* ── TEXT MODE ── */}
      {mode === "text" && (
        <div className="text-wrap">
          <textarea
            className="resume-ta"
            placeholder="Dán nội dung CV vào đây — kỹ năng, kinh nghiệm, học vấn, vị trí ứng tuyển..."
            value={text} onChange={(e) => setText(e.target.value)} rows={10}
          />
          <div className="ta-footer">
            <span className="ta-char">{text.length.toLocaleString("vi-VN")} ký tự</span>
            {text.length > 0 && <button className="ta-clear" onClick={() => setText("")}>Xoá</button>}
          </div>
        </div>
      )}

      {/* ── LỖI ── */}
      {error && (
        <div className="upcv-error">
          <i className="bi bi-exclamation-triangle-fill" /> {error}
        </div>
      )}

      {/* ── PROGRESS ── */}
      {progress && (
        <div className="upcv-progress">
          <div className="progress-spinner" />
          <span>{progress}</span>
        </div>
      )}

      {/* ── NÚT PHÂN TÍCH ── */}
      <button className="analyze-btn" onClick={handleSubmit}>
        <i className="bi bi-cpu-fill" />
        <span>
          {mode === "file" && files.length > 1
            ? `Phân tích ${files.length} CV`
            : "Phân tích CV"}
        </span>
        <i className="bi bi-arrow-right-short ms-auto" style={{ fontSize: "1.1rem" }} />
      </button>
    </div>
  );
}
