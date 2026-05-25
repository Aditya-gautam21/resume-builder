from backend.services.pdf_renderer import render_resume_pdf

dummy_data = {
    "contact": {"name": "Aditya Gautam", "email": "aditya@example.com"},
    "summary": "Experienced ML Engineer.",
    "work_experience": [
        {
            "role": "ML Engineer",
            "company": "Tech Corp",
            "duration": "2020 - Present",
            "bullets": [
                "Developed PyTorch models for NLP tasks.",
                "Optimized LLM inference pipeline. " * 20, # Very long bullet
                "A" * 200 # very long word
            ]
        }
    ]
}

try:
    pdf_bytes = render_resume_pdf(dummy_data, template_name="classic")
    with open("dummy_output.pdf", "wb") as f:
        f.write(pdf_bytes)
    print("Successfully generated dummy_output.pdf")
except Exception as e:
    print(f"Error: {e}")
