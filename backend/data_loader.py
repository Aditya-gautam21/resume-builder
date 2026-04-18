import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

loader = PyPDFLoader(
    file_path=os.getenv('FILE_PATH')
)