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
    
    def json_chunking(parsed_json):
        prompt = f'''You are a data processing system.

        Convert the given resume JSON into a list of semantic chunks for a RAG system.

        Rules:
        1. Each chunk must represent ONE logical unit:
        - one work experience
        - one project
        - one skill category

        2. Preserve hierarchy:
        - include role, company, duration together
        - include project name + technologies + description together

        3. Output MUST be JSON list of objects:
        [
        {
            "content": "...clean natural language text...",
            "metadata": {
            "type": "...",
            "name": "...",
            "extra_fields": "..."
            }
        }
        ]

        4. Do NOT lose information
        5. Do NOT merge unrelated sections
        6. Do NOT hallucinate

        Input:
        {parsed_json}
        '''
        
        return prompt