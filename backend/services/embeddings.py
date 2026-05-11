import os
from pathlib import Path 
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from backend.services.json_chunker import chunker

INDEX_PATH = Path('/home/adityagautam/Desktop/Projects/resume-builder/backend/data/vectorstores')

#Step4 -> creating vectorstore from the data reciened through json chunker

def create_vector_store():
    chunks = chunker()

    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local('INDEX_PATH')

    return vector_store

def load_vector_store():
    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

    if not os.path.exists(INDEX_PATH):
        create_vector_store()

    else:
        vector_store = FAISS.load_local(
            folder_path=INDEX_PATH,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )

    return vector_store