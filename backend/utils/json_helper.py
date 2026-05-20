import re, json

def safe_parse_json(raw: str) -> dict:
    raw = raw.strip()
    # Strip ```json ... ``` if present
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*\n", "", raw)
        raw = re.sub(r"\n```\s*$", "", raw)
    return json.loads(raw)