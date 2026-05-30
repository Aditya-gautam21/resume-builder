import subprocess
import tempfile
import os
import shutil


def render_latex(tex_content: str) -> bytes:
    tectonic = shutil.which("tectonic")
    if tectonic is None:
        raise RuntimeError(
            "tectonic not found. Install it: "
            "https://tectonic-typesetting.github.io/en-US/install.html"
        )

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "resume.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(tex_content)

        result = subprocess.run(
            [tectonic, tex_path],
            cwd=tmpdir,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Tectonic compilation failed:\n{result.stderr}")

        pdf_path = os.path.join(tmpdir, "resume.pdf")
        with open(pdf_path, "rb") as f:
            return f.read()
