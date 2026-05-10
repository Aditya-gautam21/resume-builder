from fastapi import APIRouter

from backend.services.parser import json_parser
from backend.services.json_loader import chunker
from backend.services.embeddings import create_vector_store, load_vector_store
from routes.upload import upload_resume

router = APIRouter()

@router.post("/rag")
async def vectorstore_creation():
    pdf_data = upload_resume()

    