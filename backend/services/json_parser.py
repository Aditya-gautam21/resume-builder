import os 
from dotenv import load_dotenv

from backend.utils.local_llm import load_local_llm
from backend.utils.prompts import Prompts
from backend.utils.json_helper import safe_parse_json

load_dotenv()

# Step2 -> takes txt data from load_data() and extracts json data from resume

def parse_json(resume_data):
    llm = load_local_llm()

    prompt = Prompts.resume_extraction_prompt(resume_data)

    response = llm.create_chat_completion(
        messages=[
            {
                'role':'system',
                'content': 'You extract structured JSON from resumes. Return ONLY valid JSON.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        temperature=0
    )

    llm_response = (response['choices'][0]['message']['content'])
    json_response = safe_parse_json(llm_response)

    return json_response