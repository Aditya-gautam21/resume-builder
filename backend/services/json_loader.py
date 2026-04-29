import json
from pathlib import Path
from langchain_core.documents import Document
from backend.services.parser import json_parser


def chunker():
    #json_data = json_parser()
    json_path = Path('/home/adityagautam/Desktop/Projects/resume-builder/backend/services/data.json')

    with open(json_path, 'r') as f:
        json_data = json.load(f)

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