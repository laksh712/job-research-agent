import os
from typing import TypedDict, Annotated
import operator
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

from tools import tools

load_dotenv()

# State persists across every loop iteration
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# LLM — Groq with Llama 3.3-70B, free
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)
llm_with_tools = llm.bind_tools(tools)

SYSTEM_PROMPT = """You are a job research agent helping a software engineer prepare for interviews.

When given a company name, you MUST use your tools in this order:
1. search_tech_stack — find their technologies
2. search_engineering_culture — find their engineering culture and blog
3. search_interview_patterns — find what topics come up in interviews
4. search_recent_news — find recent company news
5. search_open_roles — find current openings

After all searches, generate a structured report in markdown with these sections:
# Company Research Brief: [Company Name]

## Tech Stack
[languages, frameworks, databases, cloud, tools]

## Engineering Culture
[team size, how they work, values, what they care about]

## Interview Preparation
### Topics to focus on
[DSA topics, system design areas]
### Likely questions
[3-4 specific questions they commonly ask]

## Recent News & Context
[what's happening at the company — use this in your interview]

## Open Roles
[current openings relevant to a backend/full-stack engineer]

## Your Talking Points
[2-3 ways to connect YOUR projects to what this company does — be specific]

Always be specific. Never give generic advice."""

def agent_node(state: AgentState):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

def should_continue(state: AgentState):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END

# Build the graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")

app = graph.compile()

def run_agent(company_name: str) -> str:
    """Run the agent and return the final markdown report."""
    result = app.invoke({
        "messages": [
            HumanMessage(content=f"Research this company for my interview: {company_name}")
        ]
    })
    # Last message is the final LLM response with the report
    return result["messages"][-1].content