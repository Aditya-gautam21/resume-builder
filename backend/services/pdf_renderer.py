from fpdf import FPDF
from backend.utils.templates import TEMPLATES


def _safe(text):
    """Replace Unicode chars that built-in PDF fonts (Latin-1) can't render."""
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        "—": "-",  # em dash
        "–": "-",  # en dash
        "‘": "'",  # left single quote
        "’": "'",  # right single quote
        "“": '"',  # left double quote
        "”": '"',  # right double quote
        "…": "...",  # ellipsis
        "•": "-",  # bullet
        " ": " ",  # non-breaking space
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _section_heading(pdf, label, font):
    pdf.set_font(font["family"], "B", font["heading_size"])
    pdf.cell(0, font["heading_size"] + 2, _safe(label.upper()), ln=True)
    pdf.ln(2)


def _render_contact(pdf, data, font, color):
    pdf.set_font(font["family"], "B", font["name_size"])
    pdf.set_text_color(*color)
    pdf.cell(0, font["name_size"] + 2, _safe(data.get("name", "")), ln=True)

    pdf.set_font(font["family"], "", font["body_size"])
    parts = [_safe(v) for k, v in data.items() if k != "name" and v]
    if parts:
        pdf.cell(0, font["line_height"], " | ".join(parts), ln=True)


def _render_summary(pdf, text, font, color):
    pdf.set_font(font["family"], "", font["body_size"])
    pdf.set_text_color(*color)
    pdf.multi_cell(0, font["line_height"], _safe(text))


def _render_work_experience(pdf, entries, font, color, bullet_char, max_bullets):
    for i, job in enumerate(entries):
        pdf.set_font(font["family"], "B", font["body_size"])
        pdf.set_text_color(*color)
        header = f"{job.get('role', '')} - {job.get('company', '')}"
        if job.get("duration"):
            header += f"  ({job['duration']})"
        pdf.cell(0, font["line_height"], _safe(header), ln=True)

        pdf.set_font(font["family"], "", font["body_size"])
        bullets = job.get("bullets", [])[:max_bullets]
        for bullet in bullets:
            pdf.multi_cell(0, font["line_height"], _safe(f"  {bullet_char} {bullet}"))

        if i < len(entries) - 1:
            pdf.ln(font["line_height"] * 0.5)


def _render_bulleted_section(pdf, entries, font, color, bullet_char):
    for i, entry in enumerate(entries):
        pdf.set_font(font["family"], "B", font["body_size"])
        pdf.set_text_color(*color)
        name = _safe(entry.get("name", ""))
        techs = entry.get("technologies", [])
        header = name
        if techs:
            header += f"  |  {', '.join(_safe(t) for t in techs)}"
        pdf.cell(0, font["line_height"], _safe(header), ln=True)

        pdf.set_font(font["family"], "", font["body_size"])
        for bullet in entry.get("bullets", []):
            pdf.multi_cell(0, font["line_height"], _safe(f"  {bullet_char} {bullet}"))

        if i < len(entries) - 1:
            pdf.ln(font["line_height"] * 0.5)


def _render_skills(pdf, skills, font, color):
    lines = []
    for category, items in skills.items():
        if items:
            label = _safe(category.replace("_", " ").title())
            vals = ", ".join(_safe(i) for i in items)
            lines.append(f"{label}: {vals}")

    pdf.set_font(font["family"], "", font["body_size"])
    pdf.set_text_color(*color)
    for line in lines:
        pdf.cell(0, font["line_height"], _safe(line), ln=True)


def _render_education(pdf, entries, font, color):
    pdf.set_font(font["family"], "", font["body_size"])
    pdf.set_text_color(*color)
    for entry in entries:
        line = f"{entry.get('degree', '')} - {entry.get('school', '')}"
        if entry.get("year"):
            line += f"  ({entry['year']})"
        pdf.cell(0, font["line_height"], _safe(line), ln=True)


def _render_certifications(pdf, entries, font, color):
    pdf.set_font(font["family"], "", font["body_size"])
    pdf.set_text_color(*color)
    for cert in entries:
        name = cert if isinstance(cert, str) else cert.get("name", "")
        pdf.cell(0, font["line_height"], _safe(name), ln=True)


_SECTION_RENDERERS = {
    "contact":         _render_contact,
    "summary":         _render_summary,
    "work_experience": _render_work_experience,
    "projects":        _render_bulleted_section,
    "skills":          _render_skills,
    "education":       _render_education,
    "certifications":  _render_certifications,
}


def render_resume_pdf(resume_data, template_name="classic"):
    if template_name not in TEMPLATES:
        raise ValueError(f"Unknown template '{template_name}'. Choices: {list(TEMPLATES.keys())}")

    template = TEMPLATES[template_name]
    font = template["font"]
    margins = template["margins"]

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(True, margins["bottom"])
    pdf.set_margins(margins["left"], margins["top"], margins["right"])
    pdf.add_page()

    for section_name in template["sections"]:
        data = resume_data.get(section_name)
        if not data:
            continue

        renderer = _SECTION_RENDERERS.get(section_name)
        if renderer is None:
            continue

        _section_heading(pdf, section_name.replace("_", " "), font)

        if section_name == "contact":
            renderer(pdf, data, font, template["color"])
        elif section_name == "work_experience":
            renderer(pdf, data, font, template["color"], template["bullet"], template["max_bullets_per_role"])
        elif section_name == "projects":
            renderer(pdf, data, font, template["color"], template["bullet"])
        else:
            renderer(pdf, data, font, template["color"])

        pdf.ln(font["section_gap"])

    return pdf.output()
