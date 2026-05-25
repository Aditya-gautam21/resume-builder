class Prompts:
    def resume_extraction_prompt(resume_data):
        prompt = f"""
        You are a strict JSON generator.

        Extract structured JSON from the resume below.

        Rules:
        - Return ONLY valid JSON. No explanation, no extra text.
        - Use empty string "" for missing values, empty list [] for missing arrays.
        - Use EXACT field names shown in the schema below.

        Schema (follow field names exactly):
        {{
          "contact": {{
            "name": "Full name",
            "email": "email address",
            "phone": "phone number",
            "linkedin": "linkedin url"
          }},
          "work_experience": [
            {{
              "role": "Job title",
              "company": "Company name",
              "duration": "Date range e.g. Jun 2024 - Aug 2025",
              "bullets": ["achievement bullet 1", "achievement bullet 2"]
            }}
          ],
          "projects": [
            {{
              "name": "Project name",
              "technologies": ["tech1", "tech2"],
              "bullets": ["achievement bullet 1", "achievement bullet 2"]
            }}
          ],
          "skills": {{
            "languages": ["Python", "Java"],
            "frameworks": ["PyTorch", "TensorFlow"],
            "tools": ["Docker", "Git"],
            "other": []
          }},
          "education": [
            {{
              "degree": "Degree name",
              "school": "Institution name",
              "year": "Graduation year"
            }}
          ]
        }}

        Resume:
        {resume_data}
        """
        return prompt

    def json_chunking(parsed_json):
        prompt = f"""You are a data processing system.

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
        """
        return prompt

    def resume_generation(resume_json, job_description, pages=1):
        prompt = f"""You are an expert resume writer who helps candidates tailor their resumes to specific job descriptions.

You are given:
1. A candidate's resume structured as JSON (contact, work experience, projects, skills, education)
2. A target job description
3. A page limit of {pages} page(s)

Your task: Rewrite and restructure the resume to maximize the candidate's fit for THIS specific job. Fit everything within {pages} page(s) — cut content if needed to meet the page limit.

Rules:

QUANTIFICATION:
- Every bullet point must include at least one metric (%, $, time-saved, team-size, user-count, etc.)
- If the original resume lacks numbers, infer reasonable estimates based on the role's seniority and context
- Examples: "improved deployment speed" → "reduced deployment time by 60%, from 2 hours to 45 minutes"

KEYWORD MATCHING:
- Identify key terms, tools, and phrases in the job description
- Naturally incorporate these into the resume where the candidate genuinely has related experience
- Do NOT fabricate skills the candidate doesn't have. If a JD keyword doesn't match any real experience, skip it.

RESTRUCTURING:
- Reorder work experiences and projects so the most JD-relevant ones appear first
- Rewrite summary (if present) to mirror the language of the job description
- Group skills by relevance to the JD, not alphabetically

OUTPUT FORMAT:
Return ONLY valid JSON. No markdown, no explanation.

STRICT CONSTRAINTS:
- EVERY "bullet" MUST be a single plain text string. Do NOT output objects or nested lists as bullets.
- DO NOT generate single words or URLs longer than 35 characters. If a URL is long, shorten it or omit the protocol.
- DO NOT generate bullets longer than 150 characters.

{{
  "tailored_resume": {{
    "contact": {{
      "name": "...",
      "email": "...",
      "phone": "...",
      "linkedin": "..."
    }},
    "summary": "A 2-3 line professional summary written specifically for this JD",
    "work_experience": [
      {{
        "role": "...",
        "company": "...",
        "duration": "...",
        "bullets": [
          "Quantified achievement aligned with JD requirement...",
          "Another quantified achievement..."
        ]
      }}
    ],
    "projects": [
      {{
        "name": "...",
        "technologies": ["..."],
        "bullets": ["...", "..."]
      }}
    ],
    "skills": {{
      "languages": ["..."],
      "frameworks": ["..."],
      "tools": ["..."],
      "other": ["..."]
    }},
    "education": [
      {{
        "degree": "...",
        "school": "...",
        "year": "..."
      }}
    ],
    "keyword_map": [
      {{
        "jd_keyword": "keyword from JD",
        "matched_to": "specific experience or skill the candidate has that maps to this keyword"
      }}
    ]
  }}
}}

Candidate Resume JSON:
{resume_json}

Job Description:
{job_description}
"""
        return prompt
