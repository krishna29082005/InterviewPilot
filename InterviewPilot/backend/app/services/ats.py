import json
from pathlib import Path

from app.ai.schemas.ats_schema import ATSAnalysis


ATS_DIR = (
    Path(__file__).resolve().parents[2]
    / "uploads"
    / "resumes"
)


def get_ats_analysis(
    user_id: int,
) -> dict | None:
    """
    Return the latest saved ATS analysis for the user.
    """

    path = (
        ATS_DIR
        / f"{user_id}_ats_analysis.json"
    )

    if not path.exists():
        return None

    try:
        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    except (OSError, json.JSONDecodeError):
        return None


def save_ats_analysis(
    user_id: int,
    result: ATSAnalysis,
) -> None:
    """
    Save the latest ATS analysis for the user.
    """

    ATS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = (
        ATS_DIR
        / f"{user_id}_ats_analysis.json"
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            result.model_dump(),
            file,
            indent=4,
            ensure_ascii=False,
        )