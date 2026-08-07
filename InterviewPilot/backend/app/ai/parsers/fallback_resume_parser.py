"""Deterministic fallback resume parser that returns ResumeSchema."""

from __future__ import annotations

import re
from typing import Iterable

from app.ai.parsers.pdf_parser import extract_text
from app.ai.parsers.text_cleaner import clean_text
from app.ai.schemas.resume import (
    Education,
    Experience,
    PersonalInfo,
    Project,
    ResumeSchema,
    TechnicalSkills,
)


SECTION_KEYS = {
    "education": ("education", "academic background"),
    "experience": ("experience", "work experience", "professional experience", "employment history"),
    "projects": ("projects", "project experience"),
    "certifications": ("certifications", "certificates"),
    "achievements": ("achievements", "awards"),
    "languages": ("languages", "language"),
    "skills": ("skills", "technical skills"),
}


def _unique(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        value = item.strip()
        if not value:
            continue
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(value)
    return out


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _looks_like_heading(line: str) -> bool:
    cleaned = _normalize(line)
    return bool(cleaned) and len(cleaned.split()) <= 6 and re.match(r"^[A-Z][A-Za-z0-9&.,()\-\/ ]{2,80}$", cleaned) is not None


def _extract_name(lines: list[str]) -> str | None:
    for line in lines[:12]:
        candidate = _normalize(line)
        if not candidate or "@" in candidate or re.search(r"\d", candidate):
            continue
        if len(candidate) < 3 or len(candidate) > 60:
            continue
        lowered = candidate.lower()
        if any(term in lowered for term in ("resume", "curriculum vitae", "cv", "profile")):
            continue
        if len(candidate.split()) <= 5:
            return candidate
    return None


def _extract_email(text: str) -> str | None:
    match = re.search(r"([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", text)
    return match.group(1) if match else None


def _extract_phone(text: str) -> str | None:
    match = re.search(r"(\+?\d[\d\s().-]{7,}\d)", text)
    return _normalize(match.group(1)) if match else None


def _extract_links(text: str) -> dict[str, str | None]:
    def normalize_url(value: str) -> str:
        value = value.strip().rstrip(").,;]")
        if value.startswith("http://") or value.startswith("https://"):
            return value
        return f"https://{value}"

    patterns = {
        "linkedin": [
            r"(?:https?://)?(?:www\.)?linkedin\.com/[^\s)]+",
        ],
        "github": [
            r"(?:https?://)?(?:www\.)?github\.com/[^\s)]+",
        ],
        "leetcode": [
            r"(?:https?://)?(?:www\.)?leetcode\.com/[^\s)]+",
        ],
        "portfolio": [
            r"(?:https?://)?(?:www\.)?[A-Za-z0-9.-]+\.[A-Za-z]{2,}[^\s)]*",
        ],
    }

    out = {key: None for key in patterns}
    for key, regexes in patterns.items():
        for pattern in regexes:
            match = re.search(pattern, text, re.I)
            if match:
                out[key] = normalize_url(match.group(0))
                break

    return out


def _extract_location(lines: list[str], text: str) -> str | None:
    for line in lines[:20]:
        lowered = line.lower()
        if any(marker in lowered for marker in ("location:", "based in", "resides in")):
            cleaned = _normalize(re.sub(r"(?i)location[:\-]?\s*", "", line))
            if cleaned and len(cleaned) <= 80:
                return cleaned
    match = re.search(r"\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*,\s*[A-Z]{2,})\b", text)
    return match.group(1) if match else None


def _extract_sections(lines: list[str]) -> dict[str, list[str]]:
    sections = {key: [] for key in SECTION_KEYS}
    current: str | None = None

    for raw_line in lines:
        line = _normalize(raw_line)
        if not line:
            continue

        lowered = line.lower()
        matched = None
        for section, keys in SECTION_KEYS.items():
            if any(
                lowered == key
                or lowered.startswith(key + " ")
                or (len(line.split()) <= 6 and key in lowered and _looks_like_heading(line))
                for key in keys
            ):
                matched = section
                break

        if matched:
            current = matched
            continue

        if current:
            sections[current].append(line)

    return sections


def _split_blocks(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []

    for line in lines:
        if not line.strip():
            if current:
                blocks.append(current)
                current = []
            continue

        if _looks_like_heading(line) and current:
            blocks.append(current)
            current = []

        current.append(_normalize(line))

    if current:
        blocks.append(current)

    return blocks


def _extract_skills(text: str) -> TechnicalSkills:
    alias_groups = {
        "programming_languages": ["Python", "C\\+\\+", "C", "Java", "JavaScript", "TypeScript", "SQL"],
        "frameworks": ["React", "Next\\.?js", "NextJS", "Node\\.?js", "Django", "Flask", "FastAPI", "Tailwind(?: CSS)?", "Spring"],
        "libraries": ["NumPy", "Pandas", "Matplotlib", "Seaborn", "scikit[- ]learn", "sklearn", "PyTorch", "Torch", "TensorFlow", "Tensor Flow", "OpenCV"],
        "databases": ["MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis"],
        "cloud": ["AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes"],
        "tools": ["Git", "GitHub", "VS Code", "Jupyter", "Anaconda", "Linux", "Postman", "Colab", "Kaggle"],
        "technologies": ["HTML", "CSS", "REST", "API", "CI/CD", "Agile", "OOP"],
        "ai_ml": ["Machine Learning", "Deep Learning", "NLP", "LLM", "Computer Vision", "Reinforcement Learning"],
        "gen_ai": ["Gemini", "OpenAI", "LangChain", "RAG", "Prompt Engineering"],
    }

    def find_matches(patterns: list[str]) -> list[str]:
        matches: list[str] = []
        for pattern in patterns:
            if re.search(rf"\b{pattern}\b", text, re.I):
                matches.append(re.sub(r"\\", "", pattern))
        return _unique(matches)

    return TechnicalSkills(
        programming_languages=find_matches(alias_groups["programming_languages"]),
        frameworks=find_matches(alias_groups["frameworks"]),
        libraries=find_matches(alias_groups["libraries"]),
        databases=find_matches(alias_groups["databases"]),
        cloud=find_matches(alias_groups["cloud"]),
        tools=find_matches(alias_groups["tools"]),
        technologies=find_matches(alias_groups["technologies"]),
        ai_ml=find_matches(alias_groups["ai_ml"]),
        gen_ai=find_matches(alias_groups["gen_ai"]),
    )


def _extract_bullets(lines: list[str]) -> list[str]:
    bullets: list[str] = []
    for line in lines:
        cleaned = _normalize(line)
        if re.match(r"^[-*•]\s+", cleaned):
            bullets.append(re.sub(r"^[-*•]\s+", "", cleaned))
        elif re.match(r"^\d+[\).]\s+", cleaned):
            bullets.append(re.sub(r"^\d+[\).]\s+", "", cleaned))
    return _unique(bullets)


def _extract_education(section_lines: list[str]) -> list[Education]:
    if not section_lines:
        return []

    blocks = _split_blocks(section_lines)
    education: list[Education] = []

    for block in blocks[:6]:
        joined = " ".join(block)
        institution = block[0] if block else None
        degree = None
        field_of_study = None
        cgpa = None
        start_date = None
        end_date = None

        for line in block:
            lowered = line.lower()
            if re.search(r"(cgpa|gpa|score|percentage|%)", lowered):
                match = re.search(r"(\d+(?:\.\d+)?)\s*(/10|/4|%|cgpa|gpa)?", line, re.I)
                if match:
                    cgpa = _normalize(match.group(0))
            years = re.findall(r"\b(19\d{2}|20\d{2})\b", line)
            if years:
                start_date = start_date or years[0]
                end_date = years[-1]
            if any(token in lowered for token in ("b.tech", "btech", "m.tech", "mtech", "b.e", "m.e", "b.sc", "m.sc", "mba", "phd", "10th", "12th", "diploma")):
                degree = line
            elif any(token in lowered for token in ("engineering", "science", "computer", "artificial intelligence", "data science", "electronics", "mechanical", "civil", "business")):
                field_of_study = line

        if institution and (degree or field_of_study or cgpa or start_date or end_date):
            education.append(
                Education(
                    institution=institution,
                    degree=degree or "",
                    field_of_study=field_of_study,
                    start_date=start_date,
                    end_date=end_date,
                    cgpa=cgpa,
                )
            )
        elif institution and len(block) > 1:
            education.append(Education(institution=institution, degree="", field_of_study=None, start_date=None, end_date=None, cgpa=None))

    return education


def _extract_experience(section_lines: list[str]) -> list[Experience]:
    if not section_lines:
        return []

    blocks = _split_blocks(section_lines)
    experience: list[Experience] = []

    for block in blocks[:10]:
        header = block[0] if block else ""
        body = block[1:]
        bullets = _extract_bullets(body)

        company = None
        title = None
        if " at " in header.lower():
            match = re.match(r"(.+?)\s+at\s+(.+)", header, re.I)
            if match:
                title = match.group(1).strip()
                company = match.group(2).strip()
        elif "|" in header:
            parts = [part.strip() for part in header.split("|") if part.strip()]
            if len(parts) >= 2:
                title, company = parts[0], parts[1]
        else:
            company = header if header and not _looks_like_heading(header) else None

        dates = re.findall(r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}|\b\d{4}\b|Present|Current)", " ".join(block), re.I)
        start_date = dates[0] if dates else None
        end_date = dates[-1] if len(dates) > 1 else None

        if company and title:
            experience.append(
                Experience(
                    company=company,
                    title=title,
                    start_date=start_date,
                    end_date=end_date,
                    location=None,
                    description=bullets,
                )
            )

    return experience


def _extract_projects(section_lines: list[str]) -> list[Project]:
    if not section_lines:
        return []

    blocks = _split_blocks(section_lines)
    projects: list[Project] = []

    for block in blocks[:10]:
        title = block[0] if block else None
        if not title:
            continue

        body = block[1:]
        bullets = _extract_bullets(body)
        body_text = " ".join(body)
        description = _normalize(body_text) if body_text and not bullets else (bullets[0] if bullets else None)

        tech_candidates = re.findall(r"\b(C\+\+|C#|C|Python|Java|JavaScript|TypeScript|SQL|React|Next\.?js|Node\.?js|PyTorch|TensorFlow|sklearn|scikit[- ]learn|Gemini|LangChain|RAG|GAN|VAE|ChromaDB|Hugging Face)\b", body_text, re.I)
        technologies = _unique([_normalize(item) for item in tech_candidates])

        if description or bullets or technologies:
            projects.append(
                Project(
                    title=title,
                    technologies=technologies,
                    description=description,
                    bullet_points=bullets[:4],
                )
            )

    return projects


def _extract_certifications(section_lines: list[str]) -> list[str]:
    return _unique(_extract_bullets(section_lines) or section_lines[:10])


def _extract_achievements(section_lines: list[str]) -> list[str]:
    return _unique(_extract_bullets(section_lines) or section_lines[:10])


def _extract_languages(section_lines: list[str]) -> list[str]:
    return _unique(_extract_bullets(section_lines) or section_lines[:10])


def _build_summary(education: list[Education], experience: list[Experience], projects: list[Project], skills: TechnicalSkills) -> str:
    parts = ["Resume parsed successfully."]
    parts.append(f"Detected {len(projects)} projects.")
    if skills.programming_languages:
        parts.append("Detected programming languages: " + ", ".join(skills.programming_languages[:6]) + ".")
    parts.append(f"Detected {len(education)} education entr{'y' if len(education) == 1 else 'ies'}.")
    if experience:
        parts.append(f"Detected {len(experience)} experience entr{'y' if len(experience) == 1 else 'ies'}.")
    return " ".join(parts)


def parse_resume_fallback(pdf_path: str) -> ResumeSchema:
    raw_text = extract_text(pdf_path)
    cleaned_text = clean_text(raw_text)
    lines = [line.strip() for line in cleaned_text.splitlines() if line.strip()]
    sections = _extract_sections(lines)

    personal_info = PersonalInfo(
        full_name=_extract_name(lines),
        email=_extract_email(cleaned_text),
        phone=_extract_phone(cleaned_text),
        location=_extract_location(lines, cleaned_text),
        **_extract_links(cleaned_text),
    )

    skills = _extract_skills(cleaned_text + "\n" + "\n".join(sections["skills"]))
    education = _extract_education(sections["education"])
    experience = _extract_experience(sections["experience"])
    projects = _extract_projects(sections["projects"])
    certifications = _extract_certifications(sections["certifications"])
    achievements = _extract_achievements(sections["achievements"])
    languages = _extract_languages(sections["languages"])
    summary = _build_summary(education, experience, projects, skills)

    return ResumeSchema(
        personal_info=personal_info,
        summary=summary,
        education=education,
        experience=experience,
        projects=projects,
        technical_skills=skills,
        soft_skills=[],
        certifications=certifications,
        achievements=achievements,
        languages=languages,
    )
