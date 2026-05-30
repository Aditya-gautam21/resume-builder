# Kairos

AI-powered resume tailoring. Upload your resume and a job description — get back a professionally formatted, ATS-optimized PDF.

## How it works

1. Upload a PDF resume
2. Paste a job description
3. DeepSeek rewrites your resume — matching JD keywords, strengthening bullet points, and reordering experience by relevance
4. The tailored content is rendered into a clean LaTeX PDF via tectonic
5. Download the PDF, ready to submit

## Architecture

```
Upload PDF  →  extract text  →  parse JSON (DeepSeek)  →  tailor (DeepSeek)  →  LaTeX  →  tectonic  →  PDF
```

```
backend/
├── main.py                   # FastAPI app — serves API + frontend
├── routes/
│   └── generator.py          # /parse-resume, /job-description, /tailored-resume
├── services/
│   ├── data_loader.py        # PDF text extraction via pypdf
│   ├── json_parser.py        # Resume text → structured JSON (DeepSeek)
│   ├── resume_generation.py  # JSON → tailored LaTeX (DeepSeek)
│   ├── latex_renderer.py     # LaTeX → PDF via tectonic subprocess
│   ├── pdf_renderer.py       # Fallback PDF renderer (fpdf2, unused by default)
│   ├── json_chunker.py       # JSON → LangChain Document chunks (RAG, unused)
│   └── embeddings.py         # FAISS vector store (RAG, unused)
├── utils/
│   ├── llm.py                # LLM clients (DeepSeek, OpenAI, llama.cpp)
│   ├── prompts.py            # LLM prompt templates
│   └── json_helper.py        # Safe JSON parsing
└── templates/                # (unused — rendered via LaTeX now)

frontend/
└── src/
    ├── App.tsx               # React app — upload, JD input, download
    └── index.css             # Styles
```

## Quick start (Docker)

```bash
# Pull the image
docker pull adigaur121/kairos:latest

# Run
docker run -d \
  --name kairos \
  --restart always \
  -p 80:8000 \
  -e DEEPSEEK_API_KEY="sk-..." \
  adigaur121/kairos:latest
```

Open `http://localhost` in your browser.

## Local development

### Backend

```bash
cd backend

# Install deps (full set for local dev)
pip install -r requirements.txt

# Or slim set (production, DeepSeek-only)
pip install -r requirements-prod.txt

# Install tectonic
curl -fsSL "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.16.9/tectonic-0.16.9-$(uname -m)-unknown-linux-gnu.tar.gz" -o /tmp/tectonic.tar.gz
tar xzf /tmp/tectonic.tar.gz -C ~/.local/bin/ tectonic
chmod +x ~/.local/bin/tectonic

# Create .env with your API key
echo 'DEEPSEEK_API_KEY=sk-...' > .env

# Run
uvicorn backend.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies API calls to `localhost:8000` automatically.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | **Yes** | DeepSeek API key for resume parsing and tailoring |
| `OPENAI_API_KEY` | No | OpenAI API key (unused in default flow) |
| `LOCAL_MODEL_PATH` | No | Path to GGUF model for local llama.cpp inference (unused in default flow) |
| `SUPABASE_URL` | No | Supabase URL (unused stub) |
| `SUPABASE_KEY` | No | Supabase key (unused stub) |

## API

### `POST /tailored-resume/`

Upload resume + job description, get a tailored PDF back.

```bash
curl -X POST http://localhost:8000/tailored-resume/ \
  -F "resume=@resume.pdf" \
  -F "jd=Job description text here" \
  -F "pages=1" \
  -o tailored_resume.pdf
```

### `POST /parse-resume/`

Upload a PDF resume, get structured JSON + tailored LaTeX back (for debugging).

```bash
curl -X POST http://localhost:8000/parse-resume/ \
  -F "file=@resume.pdf" \
  -F "jd=Job description text here" \
  -F "pages=1"
```

## Docker build (for contributors)

```bash
# Build for ARM64 (Oracle VM, Raspberry Pi)
docker buildx build --platform linux/arm64 -t your-username/kairos:latest --push .

# Build for x86_64
docker buildx build --platform linux/amd64 -t your-username/kairos:latest --push .
```

The Dockerfile uses a 3-stage build:
1. `node:22-alpine` — builds the React frontend
2. `debian:bookworm-slim` — downloads the tectonic binary
3. `python:3.12-slim` — runtime with FastAPI + frontend static files
