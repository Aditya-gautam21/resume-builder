from fastapi import File, UploadFile, HTTPException, APIRouter, Form
from pypdf import PdfReader
from pathlib import Path
import io

from backend.services.data_loader import extract_text_from_pdf
from backend.services.json_data_extractor import json_parser
from backend.services.resume_generation import generate_resume

router = APIRouter()

@router.post("/parse-resume/")
async def parse_uploaded_resume(file: UploadFile = File(...)):
    try: 
        contents = await file.read()
        resume_text = extract_text_from_pdf(contents, file.filename)
        resume_json = json_parser(resume_text)
        return {'status': 'ok', 'json': resume_json}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/job-description/")
async def upload_jd(jd: str = Form(...)):
    try:
        return {'status':'ok','jd':jd}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)
    
@router.post("/tailored-resume/")
async def tailor_resume(resume: UploadFile = File(...), jd:str = Form(...)):
    try:
        contents = await resume.read()
        resume_txt = extract_text_from_pdf(contents)
        resume_json = json_parser(resume_txt)

        tailored = generate_resume(resume_data=resume_json, job_description=jd)

        return {'status':'ok', 'final_resume':tailored}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)