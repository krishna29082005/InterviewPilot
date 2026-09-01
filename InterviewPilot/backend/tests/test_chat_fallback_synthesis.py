"""
Test cases for multi-context fallback synthesis.

Tests cover:
1. Gap/weakness detection and synthesis
2. Strength detection and synthesis
3. Preparation recommendations
4. Reason-based questions
5. Generic multi-context summary
6. Single-context fallback preservation
7. Missing data graceful handling
"""

import pytest
from app.ai.schemas.resume import ResumeSchema, TechnicalSkills
from app.ai.services.chat import (
    _fallback_reply,
    _synthesize_multi_context_fallback,
)


# ==========================================================
# Test Data Fixtures
# ==========================================================


@pytest.fixture
def sample_resume():
    """Create a minimal resume for testing."""
    return ResumeSchema(
        name="John Doe",
        email="john@example.com",
        phone="+1234567890",
        professional_summary="Experienced backend developer",
        location="San Francisco, CA",
        technical_skills=TechnicalSkills(
            programming_languages=["Python", "Go", "JavaScript"],
            frameworks=["FastAPI", "Django", "React"],
            libraries=["NumPy", "Pandas"],
            databases=["PostgreSQL", "MongoDB"],
            cloud=["AWS", "GCP"],
            tools=["Docker", "Kubernetes"],
            technologies=[],
            ai_ml=[],
            gen_ai=[],
        ),
        experience=[],
        education=[],
        projects=[],
        certifications=[],
        soft_skills=[],
    )


@pytest.fixture
def sample_ats_analysis():
    """Create a sample ATS analysis result."""
    return {
        "ats_score": 65,
        "analysis": {
            "weaknesses": ["Missing action verbs", "Poor keyword density"],
            "missing_keywords": ["leadership", "agile", "cross-functional"],
        },
    }


@pytest.fixture
def sample_job_match():
    """Create a sample Job Match result."""
    return {
        "analysis": {
            "match_score": 72,
            "missing_skills": ["System Design", "Kubernetes", "gRPC"],
            "matching_skills": ["Python", "FastAPI", "PostgreSQL"],
        },
    }


@pytest.fixture
def sample_interview():
    """Create a sample interview evaluation."""
    return {
        "role": "Backend Engineer",
        "status": "completed",
        "evaluation": {
            "overall_score": 78,
            "technical_score": 82,
            "communication_score": 75,
            "areas_for_improvement": ["System design depth", "Whiteboard explanation"],
        },
    }


# ==========================================================
# Gap/Weakness Tests
# ==========================================================


def test_gap_question_with_all_contexts(
    sample_resume,
    sample_ats_analysis,
    sample_job_match,
    sample_interview,
):
    """Test that gap questions synthesize across all contexts."""
    message = "What are my biggest career gaps?"

    response = _synthesize_multi_context_fallback(
        message=message,
        resume=sample_resume,
        ats_analysis=sample_ats_analysis,
        job_match=sample_job_match,
        interview=sample_interview,
    )

    # Should mention gaps from multiple sources
    assert "areas for improvement" in response.lower()
    or "gaps" in response.lower()

    # Should be a single response, not concatenated
    assert "\n\n" not in response or response.count("\n\n") <= 1

    # Should mention synthesis
    assert "multiple" in response.lower() or "your" in response.lower()


def test_gap_question_ats_only(sample_ats_analysis):
    """Test gap questions with only ATS data."""
    message = "What are my biggest weaknesses?"

    response = _synthesize_multi_context_fallback(
        message=message,
        ats_analysis=sample_ats_analysis,
    )

    # Should extract ATS weaknesses
    assert "Missing action verbs" in response or "Poor keyword density" in response
    assert isinstance(response, str)
    assert len(response) > 0


def test_gap_question_job_match_only(sample_job_match):
    """Test gap questions with only Job Match data."""
    message = "What skills am I missing?"

    response = _synthesize_multi_context_fallback(
        message=message,
        job_match=sample_job_match,
    )

    # Should extract missing skills
    assert (
        "System Design" in response
        or "Kubernetes" in response
        or "missing" in response.lower()
    )
    assert isinstance(response, str)
    assert len(response) > 0


def test_gap_question_no_data():
    """Test gap question when no data is available."""
    message = "What are my career gaps?"

    response = _synthesize_multi_context_fallback(
        message=message,
    )

    # Should provide helpful guidance
    assert "don't have enough data" in response or "not available" in response
    assert isinstance(response, str)


# ==========================================================
# Strength Tests
# ==========================================================


def test_strength_question_with_resume(sample_resume):
    """Test strength questions use resume as primary source."""
    message = "What are my strongest skills?"

    response = _synthesize_multi_context_fallback(
        message=message,
        resume=sample_resume,
    )

    # Should list skills from resume
    assert "Python" in response or "FastAPI" in response or "skills" in response.lower()
    assert "strongest" in response.lower()
    assert isinstance(response, str)


def test_strength_question_resume_plus_job_match(
    sample_resume,
    sample_job_match,
):
    """Test strength questions combine resume and job match."""
    message = "What skills do I have that match the job?"

    response = _synthesize_multi_context_fallback(
        message=message,
        resume=sample_resume,
        job_match=sample_job_match,
    )

    # Should mention skills and alignment
    assert "skill" in response.lower()
    assert (
        "align" in response.lower()
        or "match" in response.lower()
        or "Python" in response
    )
    assert isinstance(response, str)


def test_strength_question_no_resume():
    """Test strength question without resume."""
    message = "What are my strongest skills?"

    response = _synthesize_multi_context_fallback(
        message=message,
    )

    # Should prompt to upload resume
    assert "resume" in response.lower() or "upload" in response.lower()
    assert isinstance(response, str)


# ==========================================================
# Preparation Tests
# ==========================================================


def test_preparation_question_with_all_contexts(
    sample_ats_analysis,
    sample_job_match,
    sample_interview,
):
    """Test preparation questions synthesize priorities."""
    message = "How can I prepare better for interviews?"

    response = _synthesize_multi_context_fallback(
        message=message,
        ats_analysis=sample_ats_analysis,
        job_match=sample_job_match,
        interview=sample_interview,
    )

    # Should provide priorities
    assert (
        "priori" in response.lower()
        or "focus" in response.lower()
        or "improve" in response.lower()
    )
    assert isinstance(response, str)
    assert len(response) > 0


def test_reason_question_why_not_getting_interviews(
    sample_ats_analysis,
    sample_job_match,
):
    """Test 'why' questions are handled as preparation."""
    message = "Why am I not getting backend interviews?"

    response = _synthesize_multi_context_fallback(
        message=message,
        ats_analysis=sample_ats_analysis,
        job_match=sample_job_match,
    )

    # Should provide actionable recommendations
    assert (
        "focus" in response.lower()
        or "priori" in response.lower()
        or "improve" in response.lower()
    )
    assert isinstance(response, str)


# ==========================================================
# Single-Context Preservation Tests
# ==========================================================


def test_single_context_resume_fallback(sample_resume):
    """Test that single-context resume questions still work."""
    message = "What skills are on my resume?"
    contexts = ["resume"]

    response = _fallback_reply(
        message=message,
        contexts=contexts,
        resume=sample_resume,
    )

    # Should use resume fallback
    assert "skill" in response.lower()
    assert isinstance(response, str)
    assert len(response) > 0


def test_single_context_ats_fallback(sample_ats_analysis):
    """Test that single-context ATS questions still work."""
    message = "What is my ATS score?"
    contexts = ["ats_analysis"]

    response = _fallback_reply(
        message=message,
        contexts=contexts,
        ats_analysis=sample_ats_analysis,
    )

    # Should use ATS fallback
    assert "65" in response or "score" in response.lower()
    assert isinstance(response, str)


def test_single_context_job_match_fallback(sample_job_match):
    """Test that single-context job match questions still work."""
    message = "What are the missing skills?"
    contexts = ["job_match"]

    response = _fallback_reply(
        message=message,
        contexts=contexts,
        job_match=sample_job_match,
    )

    # Should use job match fallback
    assert (
        "System Design" in response
        or "missing" in response.lower()
        or "skill" in response.lower()
    )
    assert isinstance(response, str)


def test_single_context_interview_fallback(sample_interview):
    """Test that single-context interview questions still work."""
    message = "How did I perform in my interview?"
    contexts = ["interview"]

    response = _fallback_reply(
        message=message,
        contexts=contexts,
        interview=sample_interview,
    )

    # Should use interview fallback
    assert "78" in response or "score" in response.lower()
    assert isinstance(response, str)


# ==========================================================
# Multi-Context Fallback Tests
# ==========================================================


def test_multi_context_fallback_uses_synthesis(
    sample_resume,
    sample_ats_analysis,
    sample_job_match,
):
    """Test that multi-context fallback uses synthesis, not concatenation."""
    message = "What should I improve?"
    contexts = ["resume", "ats_analysis", "job_match"]

    response = _fallback_reply(
        message=message,
        contexts=contexts,
        resume=sample_resume,
        ats_analysis=sample_ats_analysis,
        job_match=sample_job_match,
    )

    # Should be a single coherent response
    assert isinstance(response, str)
    assert len(response) > 0

    # Should NOT be multiple concatenated fallback responses
    # (no separate "Your ATS score is..." followed by "Your Job Match...")
    assert response.count("Your latest") <= 1 or "synthesis" in response.lower()


def test_multi_context_generic_summary(
    sample_resume,
    sample_ats_analysis,
    sample_job_match,
    sample_interview,
):
    """Test generic multi-context summary when no specific question intent."""
    message = "Tell me about my candidate profile"
    contexts = ["resume", "ats_analysis", "job_match", "interview"]

    response = _synthesize_multi_context_fallback(
        message=message,
        resume=sample_resume,
        ats_analysis=sample_ats_analysis,
        job_match=sample_job_match,
        interview=sample_interview,
    )

    # Should provide overview
    assert "InterviewPilot data" in response
    assert isinstance(response, str)
    assert len(response) > 0


# ==========================================================
# Graceful Degradation Tests
# ==========================================================


def test_partial_data_availability(sample_ats_analysis, sample_interview):
    """Test synthesis with partial data (e.g., only ATS + interview)."""
    message = "What are my career gaps?"

    response = _synthesize_multi_context_fallback(
        message=message,
        ats_analysis=sample_ats_analysis,
        interview=sample_interview,
    )

    # Should work with available data only
    assert isinstance(response, str)
    assert len(response) > 0
    assert (
        "improvement" in response.lower()
        or "gap" in response.lower()
        or "weak" in response.lower()
    )


def test_all_none_inputs():
    """Test synthesis when all data is None."""
    message = "What are my gaps?"

    response = _synthesize_multi_context_fallback(
        message=message,
        resume=None,
        ats_analysis=None,
        job_match=None,
        interview=None,
    )

    # Should provide helpful guidance
    assert isinstance(response, str)
    assert "don't have" in response or "not available" in response


# ==========================================================
# Edge Case Tests
# ==========================================================


def test_gap_question_variant_phrasings():
    """Test various phrasings of gap questions."""
    phrasings = [
        "What are my career gaps?",
        "What weaknesses do I have?",
        "What should I improve?",
        "Where am I lacking?",
        "What needs improvement?",
    ]

    for message in phrasings:
        response = _synthesize_multi_context_fallback(
            message=message,
            ats_analysis={"analysis": {"weaknesses": ["Test weakness"]}},
        )

        assert isinstance(response, str)
        assert len(response) > 0


def test_response_never_concatenates_with_newlines(
    sample_ats_analysis,
    sample_job_match,
):
    """Ensure responses are never two separate paragraphs concatenated."""
    message = "What are my gaps?"

    response = _synthesize_multi_context_fallback(
        message=message,
        ats_analysis=sample_ats_analysis,
        job_match=sample_job_match,
    )

    # Should be ONE coherent response, not two responses joined
    # (old bug was: "Your ATS score... \n\n Your Job Match...")
    lines = response.split("\n")
    
    # Either single paragraph or multiple lines of one thought
    # NOT "X. Your ATS... \n\n Based on Job Match..."
    if len(lines) > 2:
        # If multi-line, should be coherent sentences, not independent thoughts
        assert not (
            "Your ATS" in response and "Your latest" in response
        ), "Should not concatenate independent fallback responses"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
