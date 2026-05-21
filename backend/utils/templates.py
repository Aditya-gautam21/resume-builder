TEMPLATES = {
    "classic": {
        "name": "Classic Harvard",
        "description": "Traditional reverse-chronological. Safest choice for conservative industries.",
        "sections": [
            "contact",
            "summary",
            "work_experience",
            "education",
            "skills",
            "certifications",
        ],
        "font": {
            "family": "Helvetica",
            "body_size": 11,
            "heading_size": 14,
            "name_size": 20,
            "section_gap": 4,        # mm between sections
            "line_height": 5.5,      # mm per line
        },
        "margins": {"top": 18, "bottom": 18, "left": 20, "right": 20},  # mm (~0.7 inch)
        "color": (0, 0, 0),
        "accent_color": (50, 50, 50),
        "bullet": "•",  # •
        "max_bullets_per_role": 5,
    },

    "modern-tech": {
        "name": "Modern Tech",
        "description": "Skills-forward layout. Best for tech roles where tooling matters first.",
        "sections": [
            "contact",
            "summary",
            "skills",
            "work_experience",
            "projects",
            "education",
        ],
        "font": {
            "family": "Helvetica",
            "body_size": 11,
            "heading_size": 14,
            "name_size": 22,
            "section_gap": 4,
            "line_height": 5.5,
        },
        "margins": {"top": 18, "bottom": 18, "left": 20, "right": 20},
        "color": (30, 30, 30),
        "accent_color": (0, 70, 140),  # navy blue headings
        "bullet": "•",
        "max_bullets_per_role": 4,
    },

    "minimal": {
        "name": "Minimal Clean",
        "description": "Maximum space efficiency. Best for 1-page resumes with dense content.",
        "sections": [
            "contact",
            "summary",
            "work_experience",
            "skills",
            "education",
        ],
        "font": {
            "family": "Helvetica",
            "body_size": 10.5,
            "heading_size": 13,
            "name_size": 18,
            "section_gap": 3,
            "line_height": 5,
        },
        "margins": {"top": 15, "bottom": 15, "left": 18, "right": 18},  # tighter
        "color": (0, 0, 0),
        "accent_color": (0, 0, 0),
        "bullet": "-",
        "max_bullets_per_role": 3,
    },

    "executive": {
        "name": "Executive",
        "description": "Summary-heavy with spaced layout. Best for senior/management roles, 2 pages.",
        "sections": [
            "contact",
            "summary",
            "work_experience",
            "education",
            "skills",
            "certifications",
        ],
        "font": {
            "family": "Helvetica",
            "body_size": 11.5,
            "heading_size": 14.5,
            "name_size": 22,
            "section_gap": 5,
            "line_height": 6,
        },
        "margins": {"top": 20, "bottom": 20, "left": 22, "right": 22},
        "color": (20, 20, 20),
        "accent_color": (60, 60, 60),
        "bullet": "•",
        "max_bullets_per_role": 6,
    },
}

# Hard constraints applied by the PDF renderer regardless of template:
ATS_RULES = {
    "no_tables": True,
    "no_images": True,
    "no_columns": True,         # single column only (skills list is the exception)
    "no_headers_footers": True,  # contact info must be in body, not page header
    "standard_heading_names": True,  # never rename "Work Experience" to "My Journey" etc.
    "consistent_date_format": True,  # "June 2024" everywhere, never mix formats
    "acronym_expansion": True,       # "CRM (Customer Relationship Management)"
}
