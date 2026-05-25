import React, { useState, useRef } from 'react';
import { UploadCloud, CheckCircle2, FileText, Settings, Download, Loader2 } from 'lucide-react';

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [jd, setJd] = useState('');
  const [template, setTemplate] = useState('classic');
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
      setError("Please provide both a resume PDF and a Job Description.");
      return;
    }

    setIsGenerating(true);
    setError(null);
    setPdfUrl(null);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('jd', jd);
    formData.append('pages', '1');
    formData.append('template_name', template);

    try {
      // The backend is running on 8000
      const res = await fetch('http://localhost:8000/tailored-resume/', {
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
    } catch (err: any) {
      console.error(err);
      setError(err.message || "Failed to generate resume. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Aether Resume</h1>
        <p>AI-powered tailoring to land your next interview.</p>
      </header>

      <main className="main-grid">
        {/* Left Column: Inputs */}
        <div className="left-panel">
          <div className="card glass-panel" style={{ marginBottom: '2rem' }}>
            <h2><UploadCloud className="icon" /> Upload Resume</h2>
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
              <FileText className="file-icon" />
              {file ? (
                <p>Selected: <strong>{file.name}</strong></p>
              ) : (
                <p>Drag & drop your current resume (PDF), or click to browse</p>
              )}
            </div>
          </div>

          <div className="card glass-panel">
            <h2><FileText className="icon" /> Target Role</h2>
            
            <div className="input-group">
              <label>Job Description</label>
              <textarea 
                rows={6} 
                placeholder="Paste the target job description here..."
                value={jd}
                onChange={(e) => setJd(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label>Template Style</label>
              <select 
                value={template} 
                onChange={(e) => setTemplate(e.target.value)}
                style={{
                  background: 'rgba(0,0,0,0.2)', 
                  border: '1px solid var(--surface-border)',
                  color: 'var(--text-main)',
                  padding: '1rem',
                  borderRadius: 'var(--radius-md)',
                  outline: 'none',
                  fontSize: '1rem'
                }}
              >
                <option value="classic">Classic Harvard</option>
                <option value="modern-tech">Modern Tech</option>
                <option value="minimal">Minimal Clean</option>
                <option value="executive">Executive</option>
              </select>
            </div>
          </div>
        </div>

        {/* Right Column: Generation / Output */}
        <div className="right-panel">
          <div className="card glass-panel" style={{ height: '100%' }}>
            <h2><Settings className="icon" /> Generate</h2>
            
            {error && (
              <div style={{ background: 'rgba(255, 75, 75, 0.1)', color: 'var(--error)', padding: '1rem', borderRadius: '8px', border: '1px solid rgba(255, 75, 75, 0.2)' }}>
                {error}
              </div>
            )}

            <div className="output-area">
              {isGenerating ? (
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem' }}>
                  <Loader2 className="loading-indicator" style={{ width: '48px', height: '48px', color: 'var(--primary)', animation: 'spin 1s linear infinite' }} />
                  <h3>Tailoring your resume...</h3>
                  <p>Our local LLM is restructuring your experience to match the job description. This usually takes 2-5 minutes.</p>
                </div>
              ) : pdfUrl ? (
                <div>
                  <CheckCircle2 className="success-icon" />
                  <h3>Generation Complete!</h3>
                  <p>Your highly tailored resume is ready.</p>
                  
                  <a href={pdfUrl} download="Tailored_Resume.pdf" className="download-link" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', justifyContent: 'center' }}>
                    <Download size={20} /> Download PDF
                  </a>
                </div>
              ) : (
                <div style={{ color: 'var(--text-muted)' }}>
                  <p>Fill in the details on the left and click Generate to create your customized resume.</p>
                </div>
              )}
            </div>

            <div style={{ marginTop: 'auto' }}>
              <button 
                onClick={handleGenerate} 
                disabled={isGenerating || !file || !jd.trim()}
              >
                {isGenerating ? 'Processing...' : 'Generate Tailored Resume'}
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
