import os
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import faiss 

from backend.services.parser import json_parser

chunks = json_parser()

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
vector_store = FAISS.from_documents(chunks, embeddings)

print(vector_store.index_to_docstore_id)