import logging

from app.ai.exceptions import AIError
from app.ai.providers.factory import ProviderFactory
from app.ai.prompts.interview_evaluation_prompt import (
    INTERVIEW_EVALUATION_PROMPT,
)
from app.ai.schemas.interview_evaluation import (
    InterviewEvaluation,
)
from app.ai.schemas.mock_interview import (
    InterviewQuestion,
)

logger = logging.getLogger(__name__)


def _build_interview_context(
    role: str,
    questions: list[InterviewQuestion],
    answers: list[str],
) -> str:
    """
    Build the structured interview context that will be
    provided to the evaluator.

    Each question is paired with the candidate's answer
    in the same order.
    """

    parts: list[str] = [
        f"Target Role: {role}",
        "",
        "Interview Responses:",
    ]

    for index, question in enumerate(questions):
        answer = (
            answers[index]
            if index < len(answers)
            else ""
        )

        parts.append(
            f"""
Question {index + 1}
Category: {question.category}
Difficulty: {question.difficulty}

Question:
{question.question}

Candidate Answer:
{answer}
"""
        )

    return "\n".join(parts)


def _score_answer(
    answer: str,
) -> int:
    """
    Very simple deterministic baseline score.

    This is NOT intended to replace AI evaluation.
    It only provides a safe fallback when Gemini is unavailable.
    """

    normalized = answer.strip()

    if not normalized:
        return 0

    word_count = len(
        normalized.split()
    )

    if word_count >= 80:
        return 85

    if word_count >= 50:
        return 75

    if word_count >= 25:
        return 65

    if word_count >= 10:
        return 50

    return 35


def _fallback_evaluation(
    role: str,
    questions: list[InterviewQuestion],
    answers: list[str],
) -> InterviewEvaluation:
    """
    Generate a deterministic interview evaluation when
    Gemini is unavailable.
    """

    if not questions:
        return InterviewEvaluation(
            overall_score=0,
            technical_score=0,
            relevance_score=0,
            communication_score=0,
            problem_solving_score=0,
            strengths=[],
            weaknesses=[
                "No interview questions were available for evaluation.",
            ],
            improvement_suggestions=[
                "Complete an interview before requesting an evaluation.",
            ],
            summary=(
                "The interview could not be evaluated because "
                "no interview responses were available."
            ),
            question_feedback=[],
        )

    answer_scores = [
        _score_answer(answer)
        for answer in answers
    ]

    if answer_scores:
        average_score = round(
            sum(answer_scores)
            / len(answer_scores)
        )
    else:
        average_score = 0

    # Keep all fallback dimensions conservative.
    overall_score = average_score
    technical_score = max(
        0,
        average_score - 5,
    )
    relevance_score = average_score
    communication_score = min(
        100,
        average_score + 5,
    )
    problem_solving_score = average_score

    strengths: list[str] = []
    weaknesses: list[str] = []
    improvements: list[str] = []
    question_feedback: list[str] = []

    non_empty_answers = [
        answer.strip()
        for answer in answers
        if answer.strip()
    ]

    if non_empty_answers:
        strengths.append(
            "The candidate provided responses to the interview questions."
        )

    if average_score >= 70:
        strengths.append(
            "Most answers contain enough detail to demonstrate an initial understanding."
        )
    else:
        weaknesses.append(
            "Several answers are relatively brief and could demonstrate deeper reasoning."
        )

    if average_score < 70:
        improvements.append(
            "Expand technical answers with reasoning, examples, and relevant trade-offs."
        )

    improvements.append(
        "Structure answers clearly by explaining the concept, reasoning, and practical example."
    )

    for index, question in enumerate(questions):
        answer = (
            answers[index]
            if index < len(answers)
            else ""
        )

        score = _score_answer(answer)

        if not answer.strip():
            feedback = (
                f"Question {index + 1}: No answer was provided. "
                "Provide a direct response and explain your reasoning."
            )

        elif score >= 70:
            feedback = (
                f"Question {index + 1}: The answer contains "
                "reasonable detail. Improve it further by adding "
                "specific technical examples or trade-offs."
            )

        else:
            feedback = (
                f"Question {index + 1}: The answer is relatively brief. "
                "Provide more technical detail, reasoning, and examples."
            )

        question_feedback.append(
            feedback
        )

    if not strengths:
        strengths.append(
            "The interview session was successfully completed."
        )

    summary = (
        f"The interview for the {role} role was completed. "
        f"The deterministic fallback evaluator estimates an "
        f"overall performance score of {overall_score}/100 "
        "based primarily on response completeness. "
        "Use the AI evaluator for deeper technical assessment "
        "when the language model is available."
    )

    return InterviewEvaluation(
        overall_score=overall_score,
        technical_score=technical_score,
        relevance_score=relevance_score,
        communication_score=communication_score,
        problem_solving_score=problem_solving_score,
        strengths=strengths,
        weaknesses=weaknesses,
        improvement_suggestions=improvements,
        summary=summary,
        question_feedback=question_feedback,
    )


async def evaluate_interview(
    role: str,
    questions: list[InterviewQuestion],
    answers: list[str],
) -> InterviewEvaluation:
    """
    Evaluate a completed mock interview.

    Gemini is attempted first. If Gemini fails, use the
    deterministic fallback evaluator.
    """

    if len(answers) < len(questions):
        logger.warning(
            "Interview evaluation received %d answers for %d questions.",
            len(answers),
            len(questions),
        )

    interview_context = _build_interview_context(
        role=role,
        questions=questions,
        answers=answers,
    )

    prompt = f"""
{INTERVIEW_EVALUATION_PROMPT}

{interview_context}
"""

    provider = ProviderFactory.get_provider(
        "gemini"
    )

    try:
        evaluation = await provider.generate(
            prompt=prompt,
            response_model=InterviewEvaluation,
        )

        logger.info(
            "Interview evaluation generated successfully."
        )

        return evaluation

    except AIError as exc:
        logger.warning(
            "Gemini interview evaluation failed, "
            "using deterministic fallback: %s",
            exc,
        )

        return _fallback_evaluation(
            role=role,
            questions=questions,
            answers=answers,
        )