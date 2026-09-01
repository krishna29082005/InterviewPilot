import logging

from app.ai.exceptions import AIError
from app.ai.providers.factory import ProviderFactory
from app.ai.prompts.chat_context_prompt import (
    CHAT_CONTEXT_PROMPT,
)
from app.ai.prompts.chat_prompt import CHAT_PROMPT
from app.ai.schemas.chat import (
    ChatContext,
    ChatContextSelection,
    ChatMessageResponse,
)
from app.ai.schemas.resume import ResumeSchema


logger = logging.getLogger(__name__)


# ==========================================================
# High-Confidence Context Patterns
# ==========================================================
#
# These phrases are explicit enough that we do not need
# scoring or another LLM call.
#

HIGH_CONFIDENCE_PATTERNS: dict[
    ChatContext,
    list[str],
] = {
    "resume": [
        "skills on my resume",
        "skills in my resume",
        "skills from my resume",
        "strongest skills on my resume",
        "strongest skills in my resume",
        "what is on my resume",
        "what's on my resume",
        "my resume",
        "my cv",
        "projects on my resume",
        "projects in my resume",
        "experience on my resume",
        "experience in my resume",
        "education on my resume",
        "education in my resume",
        "certifications on my resume",
        "certifications in my resume",
        "improve my resume",
        "improve my cv",
        "resume feedback",
        "cv feedback",
    ],

    "ats_analysis": [
        "ats score",
        "my ats",
        "my ats score",
        "ats analysis",
        "ats result",
        "ats performance",
        "ats compatibility",
        "applicant tracking",
        "ats keywords",
        "missing ats keywords",
        "ats formatting",
        "resume ats score",
        "why is my ats score",
        "why is my ats low",
        "improve my ats score",
        "improve my ats",
    ],

    "job_match": [
        "job match",
        "job-match",
        "job description",
        "match score",
        "missing skills for this job",
        "missing skills for the job",
        "required skills for this job",
        "required skills for the job",
        "skills for this role",
        "skills needed for this role",
        "why don't i match this job",
        "why do i not match this job",
        "why is my job match low",
        "why is my match score low",
        "role fit",
        "job fit",
    ],

    "interview": [
        "mock interview",
        "interview score",
        "interview evaluation",
        "interview performance",
        "interview feedback",
        "how did i perform in my interview",
        "how was my interview",
        "my interview",
        "my interview answers",
        "my interview questions",
        "how can i improve my interview",
        "how can i improve in interviews",
        "technical interview",
    ],
}


# ==========================================================
# Secondary Context Patterns
# ==========================================================
#
# These are weaker signals and are used only when there is
# no explicit high-confidence match.
#

SECONDARY_CONTEXT_PATTERNS: dict[
    ChatContext,
    list[str],
] = {
    "resume": [
        "resume",
        "cv",
        "project",
        "projects",
        "experience",
        "education",
        "certification",
        "certifications",
        "skill",
        "skills",
    ],

    "ats_analysis": [
        "ats",
        "applicant tracking system",
        "keyword",
        "keywords",
        "formatting",
    ],

    "job_match": [
        "job",
        "role",
        "matching skills",
        "matching keywords",
        "missing skills",
        "required skills",
    ],

    "interview": [
        "interview",
        "answer",
        "answers",
        "question",
        "questions",
        "performance",
    ],
}


# ==========================================================
# Text Normalization
# ==========================================================

def _normalize_message(
    message: str,
) -> str:
    """
    Normalize whitespace and casing so phrase matching
    is predictable.
    """

    return " ".join(
        message.lower().strip().split()
    )


# ==========================================================
# Explicit Context Detection
# ==========================================================

def _get_high_confidence_context(
    message: str,
) -> list[ChatContext] | None:
    """
    Detect explicit intent phrases.

    If a high-confidence phrase is found, return its context
    immediately. This prevents clear questions from being
    routed through weaker scoring.
    """

    text = _normalize_message(
        message
    )

    matches: list[ChatContext] = []

    for context, patterns in (
        HIGH_CONFIDENCE_PATTERNS.items()
    ):
        for pattern in patterns:
            if pattern in text:
                matches.append(context)
                break

    # No explicit match.
    if not matches:
        return None

    # If multiple explicit contexts appear, keep all of them.
    #
    # Example:
    # "Why is my resume ATS score low?"
    #
    # -> resume + ats_analysis
    #
    # This is useful because both contexts may genuinely
    # contribute to the final answer.

    unique_matches: list[ChatContext] = []

    for context in matches:
        if context not in unique_matches:
            unique_matches.append(
                context
            )

    logger.info(
        "High-confidence chat contexts: %s",
        unique_matches,
    )

    return unique_matches


# ==========================================================
# Secondary Context Scoring
# ==========================================================

def _score_secondary_contexts(
    message: str,
) -> dict[ChatContext, int]:
    """
    Score weaker context signals.

    Longer phrases receive more weight than single words.
    """

    text = _normalize_message(
        message
    )

    scores: dict[ChatContext, int] = {
        "resume": 0,
        "ats_analysis": 0,
        "job_match": 0,
        "interview": 0,
    }

    for context, patterns in (
        SECONDARY_CONTEXT_PATTERNS.items()
    ):
        for pattern in patterns:
            if pattern in text:
                scores[context] += (
                    1 + len(pattern.split())
                )

    return scores


# ==========================================================
# Secondary Context Detection
# ==========================================================

def _get_secondary_contexts(
    message: str,
) -> list[ChatContext] | None:
    """
    Return a secondary deterministic context only when
    there is a clear winner.
    """

    scores = _score_secondary_contexts(
        message
    )

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    best_context, best_score = ranked[0]
    second_score = ranked[1][1]

    logger.info(
        "Secondary chat routing scores: %s",
        scores,
    )

    if best_score == 0:
        return None

    # Require a useful signal.
    if best_score < 3:
        return None

    # Require a clear lead.
    if (
        best_score - second_score
        < 2
    ):
        return None

    logger.info(
        "Secondary chat context selected: %s",
        best_context,
    )

    return [best_context]


# ==========================================================
# Gemini Context Router
# ==========================================================

async def _route_with_gemini(
    message: str,
) -> list[ChatContext]:
    """
    Ask Gemini to classify genuinely ambiguous questions.
    """

    prompt = f"""
{CHAT_CONTEXT_PROMPT}

User Question:

{message}
"""

    provider = ProviderFactory.get_provider(
        "gemini"
    )

    result = await provider.generate(
        prompt=prompt,
        response_model=ChatContextSelection,
    )

    return result.contexts


# ==========================================================
# Hybrid Context Router
# ==========================================================

async def select_contexts(
    message: str,
    available_contexts: list[ChatContext],
) -> list[ChatContext]:
    """
    Hybrid context routing:

    1. Explicit deterministic intent.
    2. Secondary deterministic scoring.
    3. Gemini for ambiguity.
    4. All available contexts if Gemini fails.
    """

    logger.info(
        "CHAT ROUTING MESSAGE: %s",
        message,
    )

    logger.info(
        "CHAT AVAILABLE CONTEXTS: %s",
        available_contexts,
    )

    # ------------------------------------------------------
    # 1. High-confidence deterministic routing
    # ------------------------------------------------------

    high_confidence_contexts = (
        _get_high_confidence_context(
            message
        )
    )

    if high_confidence_contexts:
        selected = [
            context
            for context in high_confidence_contexts
            if context in available_contexts
        ]

        if selected:
            logger.info(
                "CHAT ROUTING RESULT: high-confidence %s",
                selected,
            )

            return selected

    # ------------------------------------------------------
    # 2. Secondary deterministic routing
    # ------------------------------------------------------

    secondary_contexts = (
        _get_secondary_contexts(
            message
        )
    )

    if secondary_contexts:
        selected = [
            context
            for context in secondary_contexts
            if context in available_contexts
        ]

        if selected:
            logger.info(
                "CHAT ROUTING RESULT: secondary %s",
                selected,
            )

            return selected

    # ------------------------------------------------------
    # 3. Gemini routing for ambiguity
    # ------------------------------------------------------

    try:
        gemini_contexts = (
            await _route_with_gemini(
                message
            )
        )

        selected = [
            context
            for context in gemini_contexts
            if context in available_contexts
        ]

        if selected:
            logger.info(
                "CHAT ROUTING RESULT: Gemini %s",
                selected,
            )

            return selected

    except AIError as exc:
        logger.warning(
            "Gemini context routing failed: %s",
            exc,
        )

    # ------------------------------------------------------
    # 4. Gemini unavailable fallback
    # ------------------------------------------------------

    logger.info(
        "CHAT ROUTING RESULT: available-context fallback %s",
        available_contexts,
    )

    return available_contexts


# ==========================================================
# Context Formatting
# ==========================================================

def _safe_resume_context(
    resume: ResumeSchema | None,
) -> str:
    if resume is None:
        return (
            "Resume information is not available."
        )

    return resume.model_dump_json(
        indent=2
    )


def _build_context(
    contexts: list[ChatContext],
    resume: ResumeSchema | None = None,
    ats_analysis: dict | None = None,
    job_match: dict | None = None,
    interview: dict | None = None,
) -> str:
    """
    Include only contexts selected by the router.
    """

    sections: list[str] = []

    if "resume" in contexts:
        sections.append(
            "=== RESUME ===\n"
            + _safe_resume_context(
                resume
            )
        )

    if "ats_analysis" in contexts:
        sections.append(
            "=== ATS ANALYSIS ===\n"
            + (
                str(ats_analysis)
                if ats_analysis is not None
                else "ATS analysis is not available."
            )
        )

    if "job_match" in contexts:
        sections.append(
            "=== JOB MATCH ===\n"
            + (
                str(job_match)
                if job_match is not None
                else "Job match information is not available."
            )
        )

    if "interview" in contexts:
        sections.append(
            "=== INTERVIEW ===\n"
            + (
                str(interview)
                if interview is not None
                else "Interview information is not available."
            )
        )

    return "\n\n".join(
        sections
    )


# ==========================================================
# Resume Fallback
# ==========================================================

def _resume_fallback(
    message: str,
    resume: ResumeSchema | None,
) -> str:
    """
    Answer common resume questions from stored resume data.
    """

    if resume is None:
        return (
            "I don't have a parsed resume available yet. "
            "Please upload your resume first."
        )

    text = message.lower()

    skills: list[str] = []

    technical_skills = resume.technical_skills

    skills.extend(
        technical_skills.programming_languages
    )

    skills.extend(
        technical_skills.frameworks
    )

    skills.extend(
        technical_skills.libraries
    )

    skills.extend(
        technical_skills.databases
    )

    skills.extend(
        technical_skills.cloud
    )

    skills.extend(
        technical_skills.tools
    )

    skills.extend(
        technical_skills.technologies
    )

    skills.extend(
        technical_skills.ai_ml
    )

    skills.extend(
        technical_skills.gen_ai
    )

    unique_skills: list[str] = []
    seen: set[str] = set()

    for skill in skills:
        normalized = skill.strip().lower()

        if not normalized:
            continue

        if normalized in seen:
            continue

        seen.add(normalized)

        unique_skills.append(
            skill.strip()
        )

    if (
        "skill" in text
        or "skills" in text
    ):
        if unique_skills:
            return (
                "Based on your stored resume, your main "
                "technical skills include: "
                + ", ".join(unique_skills)
                + "."
            )

        return (
            "Your stored resume does not contain any "
            "technical skills that I can summarize."
        )

    if (
        "project" in text
        or "projects" in text
    ):
        if resume.projects:
            project_names = [
                project.title
                for project in resume.projects
            ]

            return (
                "Your resume currently contains these "
                "projects: "
                + ", ".join(project_names)
                + "."
            )

        return (
            "I don't see any projects in your stored resume."
        )

    if "experience" in text:
        if resume.experience:
            experience_titles = [
                experience.title
                for experience in resume.experience
            ]

            return (
                "Your resume contains experience entries "
                "including: "
                + ", ".join(experience_titles)
                + "."
            )

        return (
            "I don't see any experience entries in your "
            "stored resume."
        )

    if "education" in text:
        if resume.education:
            return (
                f"Your stored resume contains "
                f"{len(resume.education)} education entries."
            )

        return (
            "I don't see any education entries in your "
            "stored resume."
        )

    return (
        "I can use your stored resume data, but the AI "
        "assistant is currently unavailable. Try asking "
        "about your skills, projects, experience, or education."
    )


# ==========================================================
# Job Match Fallback
# ==========================================================

def _job_match_fallback(
    message: str,
    job_match: dict | None,
) -> str:
    """
    Answer common Job Match questions from saved analysis.
    """

    if job_match is None:
        return (
            "I don't have a saved Job Match analysis yet. "
            "Run Job Match analysis against a job description first."
        )

    analysis = job_match.get(
        "analysis",
        {},
    )

    text = message.lower()

    missing_skills = analysis.get(
        "missing_skills",
        [],
    )

    matching_skills = analysis.get(
        "matching_skills",
        [],
    )

    missing_keywords = analysis.get(
        "missing_keywords",
        [],
    )

    match_score = analysis.get(
        "match_score"
    )

    if "missing skill" in text:
        if missing_skills:
            return (
                "According to your latest Job Match analysis, "
                "the missing required skills are: "
                + ", ".join(missing_skills)
                + "."
            )

        return (
            "Your latest Job Match analysis did not identify "
            "any missing required skills."
        )

    if (
        "match score" in text
        or "job match" in text
        or "match" in text
    ):
        if match_score is not None:
            return (
                f"Your latest Job Match score is "
                f"{match_score}%. "
                "It is based on required skills and "
                "job-description keyword alignment."
            )

    if matching_skills:
        response = (
            "Your latest Job Match analysis shows these "
            "matching skills: "
            + ", ".join(matching_skills)
            + "."
        )

        if missing_keywords:
            response += (
                " It also identified missing job-specific "
                "keywords such as: "
                + ", ".join(missing_keywords)
                + "."
            )

        return response

    return (
        "Your latest Job Match analysis is available, "
        "but I need a more specific question to summarize it."
    )


# ==========================================================
# Interview Fallback
# ==========================================================

def _interview_fallback(
    message: str,
    interview: dict | None,
) -> str:
    """
    Answer common interview questions from the current
    interview session/evaluation.
    """

    if interview is None:
        return (
            "I don't have an interview session available yet. "
            "Complete a mock interview first."
        )

    evaluation = interview.get(
        "evaluation"
    )

    if evaluation:
        overall = evaluation.get(
            "overall_score"
        )

        technical = evaluation.get(
            "technical_score"
        )

        communication = evaluation.get(
            "communication_score"
        )

        if (
            overall is not None
            and technical is not None
            and communication is not None
        ):
            return (
                f"Your latest interview evaluation has an "
                f"overall score of {overall}/100, a "
                f"technical score of {technical}/100, and "
                f"a communication score of "
                f"{communication}/100."
            )

    role = interview.get(
        "role",
        "your selected role",
    )

    status = interview.get(
        "status",
        "unknown",
    )

    return (
        f"You currently have a {status} mock interview "
        f"for the {role} role. Complete the interview "
        "to receive a detailed evaluation."
    )


# ==========================================================
# ATS Fallback
# ==========================================================

def _ats_fallback(
    ats_analysis: dict | None,
) -> str:
    """
    Answer common ATS questions from saved ATS data.
    """

    if ats_analysis is None:
        return (
            "Your ATS analysis is not currently available. "
            "Run the ATS analysis first."
        )

    score = ats_analysis.get(
        "ats_score"
    )

    if score is not None:
        weaknesses = ats_analysis.get(
            "weaknesses",
            [],
        )

        missing_keywords = ats_analysis.get(
            "missing_keywords",
            [],
        )

        response = (
            f"Your ATS score is {score}/100."
        )

        if weaknesses:
            response += (
                " Main weaknesses include: "
                + ", ".join(
                    weaknesses[:3]
                )
                + "."
            )

        if missing_keywords:
            response += (
                " Missing keywords include: "
                + ", ".join(
                    missing_keywords[:5]
                )
                + "."
            )

        return response

    return (
        "Your ATS analysis is available, but the "
        "fallback assistant cannot summarize it further "
        "without the AI service."
    )


# ==========================================================
# Multi-Context Synthesis
# ==========================================================

def _synthesize_multi_context_fallback(
    message: str,
    resume: ResumeSchema | None = None,
    ats_analysis: dict | None = None,
    job_match: dict | None = None,
    interview: dict | None = None,
) -> str:
    """
    Synthesize multiple contexts into a single coherent response.

    This handles broad/multi-context questions like:
    - "What are my biggest career gaps?"
    - "What should I improve next?"
    - "How can I prepare better for interviews?"
    - "Why am I not getting interviews?"

    Rather than concatenating independent fallback responses,
    this function intelligently combines data from all selected
    contexts into one synthesized answer.
    """

    text = message.lower()

    # Detect question intent patterns
    is_gap_question = any(
        phrase in text
        for phrase in [
            "gap",
            "gaps",
            "weakness",
            "weaknesses",
            "weak",
            "improve",
            "need to",
            "should i improve",
            "missing",
            "lack",
            "lacking",
        ]
    )

    is_strength_question = any(
        phrase in text
        for phrase in [
            "strength",
            "strengths",
            "strong",
            "good",
            "best",
            "strong suit",
            "excel",
            "standout",
        ]
    )

    is_preparation_question = any(
        phrase in text
        for phrase in [
            "prepare",
            "preparation",
            "prepare for",
            "get ready",
            "ready for",
            "how to prepare",
            "how should i",
        ]
    )

    is_reason_question = any(
        phrase in text
        for phrase in [
            "why",
            "why am i",
            "why is",
            "reason",
            "not getting",
        ]
    )

    # --- Gap/Weakness Synthesis ---
    if is_gap_question:
        gaps: list[tuple[str, str]] = []  # (gap_text, source)

        # ATS weaknesses
        if ats_analysis is not None:
            analysis = ats_analysis.get("analysis", {})
            weaknesses = analysis.get("weaknesses", [])
            for weakness in weaknesses[:2]:
                gaps.append((weakness, "ats"))

        # Missing skills from Job Match
        if job_match is not None:
            analysis = job_match.get("analysis", {})
            missing_skills = analysis.get("missing_skills", [])
            for skill in missing_skills[:2]:
                gaps.append((skill, "job_match"))

        # Interview areas for improvement
        if interview is not None:
            evaluation = interview.get("evaluation", {})
            areas = evaluation.get("areas_for_improvement", [])
            for area in areas[:2]:
                gaps.append((area, "interview"))

        if gaps:
            unique_gaps = []
            seen: set[str] = set()
            for gap_text, source in gaps:
                gap_lower = gap_text.lower()
                if gap_lower not in seen:
                    seen.add(gap_lower)
                    unique_gaps.append(gap_text)

            response = (
                "Based on your current InterviewPilot data, "
                "your main areas for improvement are: "
                + ", ".join(unique_gaps)
                + "."
            )

            # Add contextual synthesis
            sources = set(source for _, source in gaps)
            if len(sources) > 1:
                response += (
                    " Multiple analyses point to these gaps, "
                    "so improving them will boost your candidacy across "
                    "resume quality, job fit, and interview performance."
                )
            elif "ats" in sources and "job_match" in sources:
                response += (
                    " These gaps directly impact both your ATS score "
                    "and job match alignment."
                )
            elif "job_match" in sources:
                response += (
                    " These are specific to the roles you are targeting. "
                    "Developing these skills will significantly improve your match."
                )

            return response

        return (
            "I don't have enough data from your available "
            "analyses to identify specific gaps. Try running "
            "ATS analysis or Job Match analysis for more details."
        )

    # --- Strength Synthesis ---
    if is_strength_question:
        strengths: list[str] = []

        # Resume skills (most reliable source)
        if resume is not None:
            technical_skills = resume.technical_skills
            all_skills: list[str] = []
            all_skills.extend(technical_skills.programming_languages or [])
            all_skills.extend(technical_skills.frameworks or [])
            all_skills.extend(technical_skills.libraries or [])
            all_skills.extend(technical_skills.databases or [])
            all_skills.extend(technical_skills.cloud or [])

            # Get unique skills
            seen: set[str] = set()
            for skill in all_skills[:10]:
                skill_normalized = skill.strip().lower()
                if skill_normalized and skill_normalized not in seen:
                    seen.add(skill_normalized)
                    strengths.append(skill.strip())

        # Matching skills from Job Match (confirm alignment)
        if job_match is not None and not strengths:
            analysis = job_match.get("analysis", {})
            matching = analysis.get("matching_skills", [])
            strengths.extend(matching[:5])

        if strengths:
            response = (
                "Based on your resume and analysis data, "
                "your strongest technical skills are: "
                + ", ".join(strengths[:6])
                + "."
            )

            if job_match is not None:
                response += (
                    " These skills align well with your target roles."
                )

            return response

        return (
            "I don't have detailed skill data available. "
            "Upload and analyze your resume to see "
            "a detailed skill breakdown."
        )

    # --- Preparation Synthesis ---
    if is_preparation_question or is_reason_question:
        recommendations: list[str] = []

        # Priority 1: Job Match gaps (most specific)
        if job_match is not None:
            analysis = job_match.get("analysis", {})
            missing_skills = analysis.get("missing_skills", [])
            if missing_skills:
                recommendations.append(
                    f"Build skills in {', '.join(missing_skills[:2])}"
                )

        # Priority 2: ATS optimization
        if ats_analysis is not None:
            score = ats_analysis.get("ats_score", 0)
            analysis = ats_analysis.get("analysis", {})
            if score < 70:
                weaknesses = analysis.get("weaknesses", [])
                if weaknesses:
                    recommendations.append(
                        f"Optimize your resume for better ATS compatibility "
                        f"(currently {score}/100)"
                    )

        # Priority 3: Interview technique
        if interview is not None:
            evaluation = interview.get("evaluation", {})
            if evaluation:
                areas = evaluation.get("areas_for_improvement", [])
                if areas:
                    recommendations.append(
                        f"Practice interview technique, especially: {areas[0]}"
                    )

        if recommendations:
            return (
                "To improve your candidacy, focus on these priorities: "
                + "; ".join(recommendations)
                + "."
            )

        return (
            "Complete ATS analysis, Job Match analysis, or a mock "
            "interview to get personalized improvement recommendations."
        )

    # --- Generic Multi-Context Summary ---
    response_parts: list[str] = []

    if resume is not None:
        response_parts.append(
            "your resume has relevant skills and experience"
        )

    if ats_analysis is not None:
        score = ats_analysis.get("ats_score")
        if score is not None:
            response_parts.append(f"your ATS score is {score}/100")

    if job_match is not None:
        match_score = job_match.get("analysis", {}).get("match_score")
        if match_score is not None:
            response_parts.append(
                f"your job match score is {match_score}%"
            )

    if interview is not None:
        evaluation = interview.get("evaluation", {})
        if evaluation:
            overall = evaluation.get("overall_score")
            if overall is not None:
                response_parts.append(
                    f"your interview evaluation is {overall}/100"
                )

    if response_parts:
        return (
            "Based on your InterviewPilot data: "
            + ", ".join(response_parts)
            + ". Ask me about a specific aspect for more details."
        )

    return (
        "The InterviewPilot AI assistant is temporarily "
        "unavailable. Try asking about specific aspects of "
        "your resume, ATS score, job match, or interviews."
    )


# ==========================================================
# Data-Driven Fallback
# ==========================================================

def _fallback_reply(
    message: str,
    contexts: list[ChatContext],
    resume: ResumeSchema | None = None,
    ats_analysis: dict | None = None,
    job_match: dict | None = None,
    interview: dict | None = None,
) -> str:
    """
    Provide useful deterministic responses when Gemini
    is unavailable.

    For single-context questions, use specialized fallbacks.
    For multi-context questions, synthesize a coherent response.
    """

    # Single-context fallbacks (preserve existing behavior)
    if len(contexts) == 1:
        if contexts[0] == "resume":
            return _resume_fallback(
                message=message,
                resume=resume,
            )

        if contexts[0] == "ats_analysis":
            return _ats_fallback(
                ats_analysis=ats_analysis,
            )

        if contexts[0] == "job_match":
            return _job_match_fallback(
                message=message,
                job_match=job_match,
            )

        if contexts[0] == "interview":
            return _interview_fallback(
                message=message,
                interview=interview,
            )

    # Multi-context: synthesize a coherent response
    return _synthesize_multi_context_fallback(
        message=message,
        resume=resume,
        ats_analysis=ats_analysis,
        job_match=job_match,
        interview=interview,
    )


# ==========================================================
# Final Chat Generation
# ==========================================================

async def chat_with_candidate(
    message: str,
    resume: ResumeSchema | None = None,
    ats_analysis: dict | None = None,
    job_match: dict | None = None,
    interview: dict | None = None,
) -> ChatMessageResponse:
    """
    Generate a context-aware chatbot response.

    Context routing happens before final answer generation.
    """

    available_contexts: list[ChatContext] = []

    if resume is not None:
        available_contexts.append(
            "resume"
        )

    if ats_analysis is not None:
        available_contexts.append(
            "ats_analysis"
        )

    if job_match is not None:
        available_contexts.append(
            "job_match"
        )

    if interview is not None:
        available_contexts.append(
            "interview"
        )

    if not available_contexts:
        available_contexts = [
            "resume"
        ]

    contexts = await select_contexts(
        message=message,
        available_contexts=available_contexts,
    )

    logger.info(
        "CHAT FINAL CONTEXTS: %s",
        contexts,
    )

    context = _build_context(
        contexts=contexts,
        resume=resume,
        ats_analysis=ats_analysis,
        job_match=job_match,
        interview=interview,
    )

    prompt = f"""
{CHAT_PROMPT}

Relevant InterviewPilot Context:

{context}

User Question:

{message}
"""

    provider = ProviderFactory.get_provider(
        "gemini"
    )

    try:
        reply = await provider.generate(
            prompt=prompt,
        )

        return ChatMessageResponse(
            reply=reply,
            context_used=contexts,
        )

    except AIError as exc:
        logger.warning(
            "Gemini chatbot generation failed, "
            "using data-driven fallback: %s",
            exc,
        )

        return ChatMessageResponse(
            reply=_fallback_reply(
                message=message,
                contexts=contexts,
                resume=resume,
                ats_analysis=ats_analysis,
                job_match=job_match,
                interview=interview,
            ),
            context_used=contexts,
        )