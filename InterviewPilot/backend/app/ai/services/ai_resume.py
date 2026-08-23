import logging

from app.ai.exceptions import AIError
from app.ai.parsers.fallback_resume_parser import parse_resume_fallback
from app.ai.parsers.pdf_parser import extract_text
from app.ai.parsers.text_cleaner import clean_text
from app.ai.prompts.resume_parser import get_resume_parser_prompt
from app.ai.providers.factory import ProviderFactory
from app.ai.schemas.resume import ResumeSchema

logger = logging.getLogger(__name__)


async def process_resume(pdf_path: str):#this function dosent perform anything it just calls the other functions to perform the task of 
    #parsing the resume and returning the parsed ResumeSchema. it is basically a wrapper function that orchestrates the different steps involved in processing a resume PDF.
    """
    Process a resume PDF and return the parsed ResumeSchema.
    """

    print("=" * 60)
    print("ðŸ“„ Starting Resume Processing...")
    print("=" * 60)

    # Step 1: Extract text from PDF
    print(f"ðŸ“ Processing file: {pdf_path}")
    print("ðŸ“‘ Extracting text from PDF...")
    raw_text = extract_text(pdf_path)

    # Step 2: Clean extracted text
    print("ðŸ§¹ Cleaning extracted text...")
    cleaned_text = clean_text(raw_text)

    print("\n" + "=" * 80)
    print("EXTRACTED TEXT SENT TO GEMINI")
    print("=" * 80)
    print(cleaned_text[:3000])
    print("=" * 80 + "\n")

    # Step 3: Build AI Prompt
    print("ðŸ“ Building Resume Parser Prompt...")
    prompt = get_resume_parser_prompt(cleaned_text)

    # Step 4: Initialize Gemini Provider
    print("ðŸ¤– Initializing Gemini Provider...")
    provider = ProviderFactory.get_provider("gemini")

    # Step 5: Send Prompt to Gemini
    print("ðŸš€ Sending resume to Gemini...")

    try:
        resume = await provider.generate(
            prompt=prompt,
            response_model=ResumeSchema,
        )
    except AIError:
        logger.warning("Gemini parsing failed, using fallback parser.")
        print("⚠️ Gemini parsing failed, using fallback parser.")
        resume = parse_resume_fallback(pdf_path)

    print("âœ… Resume Parsed Successfully!")
    print("=" * 60)
    print(resume)
    print("=" * 60)

    return resume
