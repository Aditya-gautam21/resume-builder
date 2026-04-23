import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

def load_data():
    loader = PyPDFLoader(
        file_path=os.getenv('FILE_PATH')
    )

    data  = loader.load()

    data_txt = " ".join(chunk.page_content for chunk in data)

    return data_txt