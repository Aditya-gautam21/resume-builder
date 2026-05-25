import json
from pathlib import Path
from langchain_core.documents import Document
from backend.services.json_parser import parse_json

#Step3 -> takes the raw json data and convert it into chunks with different fields to feed into the embedder

def chunker():
    json_data = parse_json()
    
    docs = []

    for item in json_data:
        doc = Document(
            page_content=item["content"],
            metadata={
                'type': item['metadata']['type'],
                'name': item['metadata']['name'],
                'technologies': item['metadata']['extra_fields'].get('technologies', None),
                'skills': item['metadata']['extra_fields'].get('skills', None)
            }
        )
        docs.append(doc)

    return docs