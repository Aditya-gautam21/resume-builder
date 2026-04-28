import os
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from backend.services.json_chunk import json_chunking

chunks = json_chunking()

documents = [
    Document(
        page_content=chunk["content"],
        metadata=chunk["metadata"]
    ) for chunk in chunks
]

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
vector_store = FAISS.from_documents(chunks, embeddings)

print(vector_store.index_to_docstore_id)