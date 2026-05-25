# Resume Builder

Tailor your resume to any job description and export it as a PDF.

## How it works

1. Upload a PDF resume
2. Provide a job description
3. The app uses a local LLM to rewrite your resume — adding quantified metrics, matching JD keywords, and reordering experience by relevance
4. Download the tailored resume as a formatted PDF

## Architecture

```
backend/
├── main.py                  # FastAPI app entry point
├── routes/
│   ├── generator.py         # /parse-resume, /job-description, /tailored-resume
│   └── rag.py               # RAG vector store (WIP)
├── services/
│   ├── data_loader.py       # PDF text extraction via pypdf
│   ├── json_parser.py       # Resume text → structured JSON via LLM
│   ├── resume_generation.py # Tailor resume to JD via LLM
│   ├── pdf_renderer.py      # JSON → formatted PDF via fpdf2
│   ├── json_chunker.py      # JSON → LangChain Document chunks
│   └── embeddings.py        # Chunks → FAISS vector store
├── utils/
│   ├── prompts.py           # LLM prompt templates
│   ├── local_llm.py         # llama.cpp + OpenAI model loaders
│   ├── json_helper.py       # Safe JSON parsing with markdown-stripping
│   └── templates.py         # PDF templates (classic, modern-tech, minimal, executive)
└── data/
    └── vectorstores/        # FAISS index storage
```

## Setup

```bash
# Create conda environment
conda create -n resume-builder python=3.12 -y
conda activate resume-builder

# Install dependencies
pip install -r backend/requirements.txt

# Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your paths and keys
```

### .env configuration

| Variable | Description |
|----------|-------------|
| `LOCAL_MODEL_PATH` | Path to GGUF model for llama.cpp (e.g., Gemma) |
| `OPENAI_API_KEY` | OpenAI API key (for embeddings) |
| `EMBEDDING_MODEL_PATH` | Path to embedding model |
| `SUPABASE_URL` | Supabase project URL (optional) |
| `SUPABASE_KEY` | Supabase publishable key (optional) |

## Running

```bash
uvicorn backend.main:app --reload
```

Then open `http://localhost:8000/docs` for the Swagger UI.

## API

### `POST /parse-resume/`

Upload a PDF resume, get structured JSON back.

```
curl -X POST http://localhost:8000/parse-resume/ \
  -F "file=@resume.pdf"
```

### `POST /job-description/`

Submit a job description.

```
curl -X POST http://localhost:8000/job-description/ \
  -F "jd=Looking for an ML Engineer with PyTorch experience..."
```

### `POST /tailored-resume/`

Upload resume + job description, get a tailored PDF back.

```
curl -X POST http://localhost:8000/tailored-resume/ \
  -F "resume=@resume.pdf" \
  -F "jd=Job description text here" \
  -F "pages=1" \
  -F "template_name=classic" \
  -o tailored_resume.pdf
```

Templates: `classic`, `modern-tech`, `minimal`, `executive`.
