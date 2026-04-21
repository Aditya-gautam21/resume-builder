class Prompts:  
    def resume_extraction_prompt(resume_data):
        prompt = f"""
        You are a strict JSON generator.

        Extract structured JSON from the resume below.

        Rules:
        - Return ONLY valid JSON
        - No explanation, no extra text

        Schema:
        {{
        "work_experience": [],
        "projects": [],
        "skills": []
        }}

        Resume:
        {resume_data}
        """

        return prompt