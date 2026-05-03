from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter
import shutil
from pathlib import Path

from backend.services.data_loader import load_data
from backend.services.parser import json_parser
from backend.services.json_loader import chunker
from backend.services.embeddings import create_vector_store, load_vector_store

router = APIRouter()

@app.post('/upload-pdf/')

def upload_resume():
    file_path = 