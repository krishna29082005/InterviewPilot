"""Resume parsing entry point for the AI parser layer."""

from app.ai.parsers.pdf_parser import extract_text
from app.ai.parsers.text_cleaner import clean_text
from app.ai.prompts.resume_parser import RESUME_PARSER_PROMPT


def parse_resume_text(pdf_path: str) -> dict:
    """Extract and clean resume text and prepare it for parsing."""
    raw_text = extract_text(pdf_path)
    cleaned_text = clean_text(raw_text)

    return {
        "prompt": RESUME_PARSER_PROMPT,
        "text": cleaned_text,
    }
