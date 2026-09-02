import logging

from app.ai.exceptions import AIError
from app.ai.parsers.fallback_resume_parser import parse_resume_fallback
from app.ai.parsers.pdf_parser import extract_text
from app.ai.parsers.text_cleaner import clean_text
from app.ai.prompts.resume_parser import get_resume_parser_prompt
from app.ai.providers.factory import ProviderFactory
from app.ai.schemas.resume import ResumeSchema

logger = logging.getLogger(__name__)


async def process_resume(pdf_path: str) -> ResumeSchema:
    """
    Process a resume PDF and return the parsed ResumeSchema.
    """

    logger.info("Starting resume processing: %s", pdf_path)

    # Step 1: Extract text from PDF
    raw_text = extract_text(pdf_path)
    logger.debug("Resume text extracted successfully.")

    # Step 2: Clean extracted text
    cleaned_text = clean_text(raw_text)
    logger.debug("Resume text cleaned successfully.")

    # Step 3: Build AI prompt
    prompt = get_resume_parser_prompt(cleaned_text)

    # Step 4: Initialize AI provider
    provider = ProviderFactory.get_provider("gemini")

    # Step 5: Send prompt to Gemini
    try:
        resume = await provider.generate(
            prompt=prompt,
            response_model=ResumeSchema,
        )
    except AIError:
        logger.warning(
            "Gemini resume parsing failed; using fallback parser."
        )
        resume = parse_resume_fallback(pdf_path)

    logger.info("Resume processing completed successfully.")

    return resume