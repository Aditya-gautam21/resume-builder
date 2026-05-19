import os 
from dotenv import load_dotenv

from backend.utils.local_llm import load_local_llm
from backend.utils.prompts import Prompts

load_dotenv()

# Step2 -> takes txt data from load_data() and extracts json data from resume

def json_parser(resume_data):
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

    return (response['choices'][0]['message']['content'])