from app.ai.providers.factory import ProviderFactory
from app.ai.parsers.pdf_parser import extract_text
from app.ai.parsers.text_cleaner import clean_text
from app.ai.prompts.resume_parser import get_resume_parser_prompt
from app.ai.schemas.resume import ResumeSchema


async def process_resume(pdf_path: str):
    """
    Process a resume PDF and return the parsed ResumeSchema.
    """

    print("=" * 60)
    print("📄 Starting Resume Processing...")
    print("=" * 60)

    # Step 1: Extract text from PDF
    print(f"📍 Processing file: {pdf_path}")
    print("📑 Extracting text from PDF...")
    raw_text = extract_text(pdf_path)

    # Step 2: Clean extracted text
    print("🧹 Cleaning extracted text...")
    cleaned_text = clean_text(raw_text)

    print("\n" + "=" * 80)
    print("EXTRACTED TEXT SENT TO GEMINI")
    print("=" * 80)
    print(cleaned_text[:3000])
    print("=" * 80 + "\n")

    # Step 3: Build AI Prompt
    print("📝 Building Resume Parser Prompt...")
    prompt = get_resume_parser_prompt(cleaned_text)

    # Step 4: Initialize Gemini Provider
    print("🤖 Initializing Gemini Provider...")
    provider = ProviderFactory.get_provider("gemini")

    # Step 5: Send Prompt to Gemini
    print("🚀 Sending resume to Gemini...")

    resume = await provider.generate(
        prompt=prompt,
        response_model=ResumeSchema,
    )

    print("✅ Resume Parsed Successfully!")
    print("=" * 60)
    print(resume)
    print("=" * 60)

    return resume