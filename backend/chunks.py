from data_loader import load_data
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks():
    data = load_data()

    splitter = RecursiveCharacterTextSplitter(chunk_size=120, chunk_overlap=30)
    chunks = splitter.create_documents([data])
    return chunks