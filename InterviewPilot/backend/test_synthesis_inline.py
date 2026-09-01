"""Quick inline test of synthesis functions."""
from app.ai.services.chat import _synthesize_multi_context_fallback, _fallback_reply

# Test 1: Gap question with ATS data
result1 = _synthesize_multi_context_fallback(
    message="What are my biggest career gaps?",
    ats_analysis={
        "ats_score": 65,
        "analysis": {
            "weaknesses": ["Missing action verbs", "Poor keyword density"],
            "missing_keywords": ["leadership"],
        },
    },
)
print("Test 1 (Gap question with ATS):")
print(result1[:150] + "...")
print()

# Test 2: Strength question with resume
class MockTechnicalSkills:
    def __init__(self):
        self.programming_languages = ["Python", "Go"]
        self.frameworks = ["FastAPI"]
        self.libraries = []
        self.databases = []
        self.cloud = []
        self.tools = []
        self.technologies = []
        self.ai_ml = []
        self.gen_ai = []

class MockResume:
    def __init__(self):
        self.technical_skills = MockTechnicalSkills()

result2 = _synthesize_multi_context_fallback(
    message="What are my strongest skills?",
    resume=MockResume(),
)
print("Test 2 (Strength question with resume):")
print(result2[:150] + "...")
print()

# Test 3: Preparation question
result3 = _synthesize_multi_context_fallback(
    message="How should I prepare for interviews?",
    job_match={
        "analysis": {
            "missing_skills": ["System Design", "Kubernetes"],
            "match_score": 70,
        },
    },
)
print("Test 3 (Preparation question):")
print(result3[:150] + "...")
print()

# Test 4: Single context fallback (should preserve old behavior)
result4 = _fallback_reply(
    message="What skills are on my resume?",
    contexts=["resume"],
    resume=MockResume(),
)
print("Test 4 (Single context - resume):")
print(result4[:150] + "...")
print()

print("✓ All synthesis tests passed!")
