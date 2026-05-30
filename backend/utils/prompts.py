import json

class Prompts:
    def resume_extraction_prompt(resume_data: str) -> str:
      prompt = f"""You are a strict JSON extractor specialized in parsing resumes.

        ## TASK
        Extract all information from the resume below into structured JSON.
        Every piece of information in the resume must be captured — do not skip or summarize any section.

        ## OUTPUT RULES
        - Return ONLY valid JSON. No explanation, no markdown, no code fences.
        - Use empty string "" for missing text values.
        - Use empty list [] for missing array values.
        - Use EXACT field names as shown in the schema.
        - Preserve original wording for bullets, do not paraphrase.
        - If a field has multiple possible values (e.g. multiple URLs), capture all of them.

        ## CONTACT EXTRACTION RULES
        - Capture every URL found (LinkedIn, GitHub, portfolio, personal site, etc.) under "links" as a list.
        - Capture city/location if present under "location".
        - If a field is not present, use "".

        ## SKILLS EXTRACTION RULES
        - Infer skill categories from the resume's own groupings if present.
        - If the resume does not categorize skills, group them yourself into: languages, frameworks, tools, cloud, databases, other.
        - Do not invent skills — only extract what is explicitly written.

        ## ACHIEVEMENTS SECTION RULES
        This is a flexible section. It captures any of the following if present in the resume:
        certifications, awards, publications, research, hackathons, competitions, honors, patents, conferences, or volunteer work.
        - Capture each item with as many fields as are available.
        - Use "type" to classify the item: one of "certification", "award", "publication", "hackathon", "competition", "research", "honor", "patent", "conference", "volunteer", "other".
        - If a certificate link/URL is present, capture it under "url".
        - If a date or year is present, capture it under "date".

        ## SCHEMA
        {{
          "contact": {{
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
            "links": [
              {{
                "label": "e.g. LinkedIn / GitHub / Portfolio",
                "url": "full url or handle"
              }}
            ]
          }},
          "summary": "Professional summary or objective paragraph if present, else empty string",
          "work_experience": [
            {{
              "role": "Job title",
              "company": "Company name",
              "location": "City, Country or Remote if mentioned",
              "duration": "e.g. Jun 2024 - Aug 2025",
              "bullets": [
                "Exact bullet point as written in resume"
              ]
            }}
          ],
          "projects": [
            {{
              "name": "Project name",
              "link": "Project URL or code link if present, else empty string",
              "technologies": ["tech1", "tech2"],
              "bullets": [
                "Exact bullet point as written in resume"
              ]
            }}
          ],
          "skills": {{
            "languages": [],
            "frameworks": [],
            "tools": [],
            "cloud": [],
            "databases": [],
            "other": []
          }},
          "education": [
            {{
              "degree": "Full degree name",
              "school": "Institution name",
              "location": "City if mentioned",
              "duration": "e.g. Nov 2022 - Jun 2026 or just graduation year",
              "gpa": "GPA or CGPA if mentioned, else empty string",
              "coursework": ["course1", "course2"]
            }}
          ],
          "achievements": [
            {{
              "type": "certification | award | publication | hackathon | competition | research | honor | patent | conference | volunteer | other",
              "title": "Title or name of the achievement",
              "issuer": "Issuing organization, event name, or publisher if mentioned",
              "date": "Date or year if mentioned, else empty string",
              "url": "Certificate or reference URL if present, else empty string",
              "description": "Any additional detail or context if present, else empty string"
            }}
          ]
        }}

        ## RESUME
        {resume_data}"""
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
          {parsed_json}"""

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
            {job_description}"""
        
        return prompt
    
    def deepseek_prompt(resume_json: dict, job_description: str, num_pages: int):
        page_rules = {
            1: """
        CRITICAL — 1 PAGE HARD LIMIT:
        - The compiled PDF must fit in exactly 1 page. This is non-negotiable.
        - Use these EXACT LaTeX settings:
            \\\\usepackage[margin=0.55in]{{geometry}}
            \\\\setlength{{\\\\itemsep}}{{1pt}}
            \\\\setlength{{\\\\parskip}}{{0pt}}
        - Font size: 10pt in \\\\documentclass[letterpaper,10pt]{{article}}
        - Maximum bullets per role: 3
        - Maximum roles: 2 most recent/relevant only
        - Maximum projects: 2 most relevant only (3 if only 1 role given)
        - Include 3-4 most relevant achievements/certifications
        - Summary: max 2 lines. Skills: single line per category, max 5 items each.
        - Reorder sections by JD relevance.
        """,
            2: """
        PAGE LIMIT — 2 PAGES:
        - Use margin=0.7in, 11pt font
        - Include full work history, all projects, certifications, skills
        - Summary: 3-4 lines
        """,
            3: """
        PAGE LIMIT — 3 PAGES:
        - Use margin=0.85in, 11pt font
        - Include all sections in full detail
        - Add coursework, publications, volunteer work if present
        """,
        }

        prompt = f"""You are an expert resume writer and ATS (Applicant Tracking System) optimization specialist. \
Your task is to rewrite and tailor the candidate's resume to closely match the given job description, \
maximizing ATS score while keeping the content truthful and professionally credible.

---

## INPUTS

### 1. CANDIDATE RESUME DATA (structured JSON)
{resume_json}

### 2. TARGET JOB DESCRIPTION
{job_description}

### 3. PAGE LIMIT
{num_pages} page(s). Follow these rules STRICTLY:
{page_rules}

---

## REWRITING RULES

### Summary
- Write a professional summary tailored to this exact role.
- Lead with most relevant experience and core competency.
- Include 2-3 critical keywords from the JD.

### Work Experience
- Rewrite each bullet using: [Action Verb] + [Task/Responsibility] + [Result/Impact]
- Reorder bullets so JD-relevant ones appear first.
- Strengthen weak bullets using reasonable inference — never invent numbers or companies.
- Keep each bullet to 1-2 lines.

### Projects
- Reorder by JD relevance. Rewrite descriptions to highlight JD-relevant technologies.

### Skills
- Extract skills from the JSON. Add JD skills only if clearly implied by existing experience.
- Do NOT invent skills. Group into logical categories.

### Education
- Keep factually identical. Do not alter institutions, degrees, or dates.

### Achievements
- Retain and prioritize items most relevant to the JD.

---

## HALLUCINATION GUARDRAILS

- NEVER add a company, institution, certification, or technology absent from the resume JSON.
- NEVER invent a job title (industry-standard reframes okay, promotions are not).
- NEVER fabricate metrics not present in the JSON.
- Improve framing and language, never the underlying facts.

---

## LATEX OUTPUT RULES

- Output ONLY valid LaTeX code — no explanations, no markdown, no text outside the document.
- Use this base setup:

\\\\documentclass[letterpaper,11pt]{{article}}
\\\\usepackage[margin=0.7in]{{geometry}}
\\\\usepackage{{enumitem}}
\\\\usepackage{{hyperref}}
\\\\usepackage[T1]{{fontenc}}
\\\\usepackage[utf8]{{inputenc}}
\\\\usepackage{{titlesec}}
\\\\usepackage{{parskip}}

- Section headers: bold, full-width, with a horizontal rule beneath (use \\\\rule after the heading).
- Use itemize with tight spacing for ATS-friendly bullet lists.
- Do NOT use multi-column layouts, tables for layout, text boxes, or graphics.
- Use a clean, standard font. Do not load exotic font packages.
- Hyperlink email and LinkedIn/GitHub URLs using \\\\href{{}}{{}}.
- The LaTeX must compile without errors.

---

## OUTPUT FORMAT

Return ONLY the complete LaTeX document, starting with \\\\documentclass and ending with \\\\end{{document}}.
No explanation, commentary, or text outside the LaTeX."""

        return prompt