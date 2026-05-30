import React, { useState, useRef } from 'react';
import { UploadCloud, CheckCircle2, FileText, Settings, Download, AlertCircle, Sparkles } from 'lucide-react';
import './index.css';

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [jd, setJd] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setError(null);
    }
  };

  const handleGenerate = async () => {
    if (!file || !jd.trim()) {
      setError("Please provide both a resume PDF and a job description.");
      return;
    }

    setIsGenerating(true);
    setError(null);
    setPdfUrl(null);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('jd', jd);
    formData.append('pages', '1');

    try {
      const res = await fetch('/tailored-resume/', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(errText || "Internal Server Error");
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      setPdfUrl(url);
    } catch (err: unknown) {
      console.error(err);
      setError(err instanceof Error ? err.message : "Failed to generate resume. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <>
      <div className="bg-glow"></div>
      <div className="bg-glow-2"></div>

      <div className="app-container">
        <header className="header">
          <div className="header-badge">AI-Powered Tailoring</div>
          <h1>Kairos</h1>
          <p>Upload your resume and a job description. Get a professionally tailored, ATS-optimized PDF in seconds.</p>
        </header>

        <main className="main-grid">
          {/* Left Column: Inputs */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem' }}>
            <div className="card">
              <h2><UploadCloud className="icon" size={28} /> Upload Resume</h2>
              <div
                className="file-drop-area"
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
              >
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  accept="application/pdf"
                />

                <div className="file-icon-wrapper">
                  <FileText className="file-icon" size={32} />
                </div>

                {file ? (
                  <div>
                    <p style={{ color: 'var(--text-main)' }}>Selected File</p>
                    <span className="file-name">{file.name}</span>
                  </div>
                ) : (
                  <div>
                    <p style={{ color: 'var(--text-main)', fontWeight: 500, marginBottom: '0.5rem' }}>
                      Click or drag to upload
                    </p>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
                      PDF format only
                    </p>
                  </div>
                )}
              </div>
            </div>

            <div className="card">
              <h2><FileText className="icon" size={28} /> Target Role</h2>

              <div className="input-group">
                <label>Job Description</label>
                <textarea
                  placeholder="Paste the full job description here to tailor your resume..."
                  value={jd}
                  onChange={(e) => setJd(e.target.value)}
                />
              </div>
            </div>
          </div>

          {/* Right Column: Generation / Output */}
          <div className="card" style={{ display: 'flex', flexDirection: 'column' }}>
            <h2><Sparkles className="icon" size={28} /> Generated Resume</h2>

            {error && (
              <div className="error-msg">
                <AlertCircle size={20} style={{ flexShrink: 0 }} />
                <span>{error}</span>
              </div>
            )}

            <div className="output-area">
              {isGenerating ? (
                <div className="status-content">
                  <div className="spinner"></div>
                  <div style={{ textAlign: 'center' }}>
                    <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', fontFamily: 'Outfit' }}>
                      Tailoring your resume...
                    </h3>
                    <p style={{ color: 'var(--text-muted)', maxWidth: '280px', margin: '0 auto', fontSize: '0.95rem' }}>
                      AI is rewriting and formatting your experience to match the job description.
                    </p>
                  </div>
                </div>
              ) : pdfUrl ? (
                <div className="status-content">
                  <div className="success-icon">
                    <CheckCircle2 size={40} />
                  </div>
                  <div>
                    <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem', fontFamily: 'Outfit' }}>
                      Ready to Apply!
                    </h3>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem' }}>
                      Your tailored resume has been generated.
                    </p>
                  </div>

                  <a
                    href={pdfUrl}
                    download="Tailored_Resume.pdf"
                    className="download-btn"
                  >
                    <Download size={20} /> Download PDF
                  </a>
                </div>
              ) : (
                <div style={{ color: 'var(--text-muted)', maxWidth: '300px' }}>
                  <Settings
                    size={48}
                    style={{ opacity: 0.2, marginBottom: '1rem', display: 'block', margin: '0 auto 1rem' }}
                  />
                  <p>Upload your resume and paste a job description, then click generate.</p>
                </div>
              )}
            </div>

            <div style={{ marginTop: 'auto', paddingTop: '1.5rem' }}>
              <button
                className="btn-primary"
                onClick={handleGenerate}
                disabled={isGenerating || !file || !jd.trim()}
              >
                {isGenerating ? 'Processing...' : (
                  <>
                    <Sparkles size={20} /> Generate Tailored Resume
                  </>
                )}
              </button>
            </div>
          </div>
        </main>
      </div>
    </>
  );
}
