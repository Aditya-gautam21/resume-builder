import os
from typing import Dict, Any

from backend.utils.local_llm import load_local_llm
from backend.utils.prompts import Prompts


def generate_resume(resume_data: Dict[str, Any], jd: str):
    llm = load_local_llm()

    prompt = Prompts.resume_generation(resume_json=resume_data, job_description=jd)
    response = llm.create_chat_completion(
        messages=[
            {
                'role':'system',
                'content':'You are an expert resume tailor. Return ONLY valid JSON, no markdown, no explanation.'
            },
            {
                'role':'user',
                'content': prompt
            }
        ],
        temperature=0
    )

    return response['choices'][0]['message']['content']