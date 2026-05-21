import json
from typing import Dict, Any

from backend.utils.local_llm import load_local_llm
from backend.utils.prompts import Prompts
from backend.utils.json_helper import safe_parse_json


def generate_resume(resume_data: Dict[str, Any], job_description: str, pages: int = 1):
    llm = load_local_llm()

    resume_json_str = json.dumps(resume_data, indent=2)
    prompt = Prompts.resume_generation(
        resume_json=resume_json_str, job_description=job_description, pages=pages
    )
    response = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are an expert resume tailor. Return ONLY valid JSON, no markdown, no explanation.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    llm_response = response["choices"][0]["message"]["content"]
    return safe_parse_json(llm_response)