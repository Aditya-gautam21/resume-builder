from fastapi import UploadFile, HTTPException, APIRouter, File, Form
from fastapi.responses import Response

from backend.services.data_loader import extract_text_from_pdf
from backend.services.json_parser import parse_json
from backend.services.resume_generation import generate_resume
from backend.services.pdf_renderer import render_resume_pdf

router = APIRouter()


@router.post("/parse-resume/")
async def parse_uploaded_resume(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        resume_text = extract_text_from_pdf(contents, file.filename)
        resume_json = parse_json(resume_text)
        return {"status": "ok", "json": resume_json}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/job-description/")
async def upload_jd(jd: str = Form(...)):
    try:
        return {"status": "ok", "jd": jd}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)


@router.post("/tailored-resume/")
async def tailor_resume(
    resume: UploadFile = File(...),
    jd: str = Form(...),
    pages: int = Form(default=1),
    template_name: str = Form(default="classic"),
):
    try:
        contents = await resume.read()
        resume_txt = extract_text_from_pdf(contents, resume.filename)
        resume_json = parse_json(resume_txt)

        tailored = generate_resume(resume_data=resume_json, job_description=jd, pages=pages)
        pdf_bytes = render_resume_pdf(tailored["tailored_resume"], template_name=template_name)

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=tailored_resume.pdf"},
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=e)