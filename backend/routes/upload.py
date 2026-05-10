from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter
from pypdf import PdfReader
from pathlib import Path
import io

router = APIRouter()

@router.get("/upload-pdf/")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith('pdf'):
        raise HTTPException(status_code=400, detail="Only PDFs are accepted!")
    
    contents = await file.read()
    reader = PdfReader(io.BytesIO(contents))

    text = "\n".join(page.extract_text() or "" for page in reader)

    return text