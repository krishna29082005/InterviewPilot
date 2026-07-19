def get_resume_parser_prompt(resume_text: str) -> str:
    return f"""
You are an expert ATS resume parser.

Your task is ONLY to extract structured information from the resume.

IMPORTANT RULES

- Return ONLY valid JSON.
- Never return markdown.
- Never wrap the JSON in ``` blocks.
- Never explain anything.
- Never invent information.
- If a field does not exist, use null for strings and [] for arrays.
- Keep descriptions short.
- Maximum 2 bullet points.
- Preserve spelling exactly.
- Preserve URLs exactly.
- Preserve dates exactly.
- Ensure the JSON is COMPLETE before stopping.

Return EXACTLY this schema:

{{
  "personal_info": {{
    "full_name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "github": "",
    "leetcode": "",
    "portfolio": ""
  }},

  "education": [
    {{
      "institution": "",
      "degree": "",
      "score": "",
      "dates": ""
    }}
  ],

  "experience": [
    {{
      "company": "",
      "title": "",
      "start_date": "",
      "end_date": "",
      "location": "",
      "description": []
    }}
  ],

  "projects": [
    {{
      "title": "",
      "technologies": [],
      "description": "",
      "bullet_points": []
    }}
  ],

  "technical_skills": {{
    "programming_languages": [],
    "frameworks": [],
    "libraries": [],
    "databases": [],
    "cloud": [],
    "tools": [],
    "technologies": [],
    "ai_ml": [],
    "gen_ai": []
  }}
}}

Resume

-----------------------
{resume_text}
-----------------------
"""