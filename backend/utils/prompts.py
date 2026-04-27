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


        3. Do NOT lose information
        4. Do NOT merge unrelated sections
        5. Do NOT hallucinate
        6. Extract all relevant data and put into respective fields provided down below. if something does not fit in any field create a new field within the same design and fill it.
        7. Output MUST be JSON list of objects(understand the data and fill the fields given in output as is):
        [
        {{
            "metadata": {{
            "type": "...",
            "name": "...",
            "extra_fields": "..."
            }},
            "content": "...clean natural language text..."
        }}
        ]

        do this for all the data present, for all the fields.

        Input:
        {parsed_json}
        '''
        
        return prompt
    
   