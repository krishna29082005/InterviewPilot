import re

from app.ai.schemas.job_requirements import JobRequirements


SKILL_CATALOG = [
    # Languages
    "Python",
    "C++",
    "Java",
    "JavaScript",
    "TypeScript",
    "Go",
    "Rust",
    "SQL",

    # Frameworks
    "FastAPI",
    "Django",
    "Flask",
    "React",
    "Next.js",
    "Node.js",

    # Databases
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "Redis",
    "SQLite",

    # Cloud / DevOps
    "AWS",
    "Azure",
    "GCP",
    "Docker",
    "Kubernetes",
    "CI/CD",

    # AI / ML
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "PyTorch",
    "TensorFlow",
    "Hugging Face",
    "LangChain",
    "RAG",

    # Backend / engineering
    "REST API",
    "REST APIs",
    "GraphQL",
    "Git",
    "Linux",
]


def _contains_skill(text: str, skill: str) -> bool:
    return re.search(
        rf"\b{re.escape(skill)}\b",
        text,
        re.IGNORECASE,
    ) is not None


def extract_job_requirements_fallback(
    job_description: str,
) -> JobRequirements:

    text = job_description.lower()

    required_skills: list[str] = []
    preferred_skills: list[str] = []
    keywords: list[str] = []

    # Find skills mentioned in the JD
    detected_skills = [
        skill
        for skill in SKILL_CATALOG
        if _contains_skill(text, skill)
    ]

    # Very simple classification:
    # If a skill appears near "preferred", "nice to have",
    # or "bonus", classify it as preferred.
    preferred_section = re.search(
        r"(preferred|nice to have|nice-to-have|bonus|optional)"
        r"(.*)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    preferred_text = (
        preferred_section.group(2)
        if preferred_section
        else ""
    )

    for skill in detected_skills:
        if skill.lower() in preferred_text:
            preferred_skills.append(skill)
        else:
            required_skills.append(skill)

    # Basic role-related keywords
    keyword_candidates = [
        "backend",
        "frontend",
        "full stack",
        "software engineer",
        "machine learning",
        "data science",
        "data engineering",
        "api development",
        "backend development",
        "deployment",
        "cloud",
        "microservices",
    ]

    for keyword in keyword_candidates:
        if keyword in text:
            keywords.append(keyword)

    return JobRequirements(
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        keywords=keywords,
    )