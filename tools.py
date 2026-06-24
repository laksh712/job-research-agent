import os
from langchain_core.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search_tech_stack(company: str) -> str:
    """Search what technologies, languages, and frameworks the company uses."""
    results = tavily.search(
        query=f"{company} tech stack engineering technologies backend frontend",
        max_results=3
    )
    return "\n\n".join([r["content"] for r in results["results"]])

@tool
def search_engineering_culture(company: str) -> str:
    """Search engineering blog, culture, team size, and how they work."""
    results = tavily.search(
        query=f"{company} engineering blog culture interview process engineering team",
        max_results=3
    )
    return "\n\n".join([r["content"] for r in results["results"]])

@tool
def search_interview_patterns(company: str) -> str:
    """Search what topics come up in interviews at this company."""
    results = tavily.search(
        query=f"{company} software engineer interview questions DSA system design experience",
        max_results=3
    )
    return "\n\n".join([r["content"] for r in results["results"]])

@tool
def search_recent_news(company: str) -> str:
    """Search recent product launches, funding, and company news."""
    results = tavily.search(
        query=f"{company} 2024 2025 2026 product launch funding news engineering",
        max_results=3
    )
    return "\n\n".join([r["content"] for r in results["results"]])

@tool
def search_open_roles(company: str) -> str:
    """Search current open engineering roles at the company."""
    results = tavily.search(
        query=f"{company} software engineer backend jobs hiring 2026",
        max_results=2
    )
    return "\n\n".join([r["content"] for r in results["results"]])

tools = [
    search_tech_stack,
    search_engineering_culture,
    search_interview_patterns,
    search_recent_news,
    search_open_roles
]