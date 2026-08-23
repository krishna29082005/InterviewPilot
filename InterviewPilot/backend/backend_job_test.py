import asyncio

from app.ai.services.job_match import extract_job_requirements


job_description = """
We are looking for a Python Backend Engineer.

Requirements:
- Strong Python programming experience
- FastAPI experience
- PostgreSQL
- REST API development
- Docker
- Git

Nice to have:
- AWS
- Kubernetes
- CI/CD
"""


async def main():
    result = await extract_job_requirements(job_description)

    print("\n" + "=" * 60)
    print("JOB REQUIREMENTS")
    print("=" * 60)
    print(result.model_dump_json(indent=2))
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())