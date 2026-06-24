# job-research-agent

An AI agent that researches any tech company in 60 seconds and 
generates a structured interview prep brief.

## What it does

Type a company name → the agent autonomously:
- Searches their tech stack and engineering culture
- Finds common interview topics and questions
- Summarises recent company news and product launches
- Identifies open roles
- Generates talking points connecting YOUR experience to their work

Output: downloadable markdown report, ready before your interview.

## Tech Stack

- **Agent framework**: LangGraph (state machine with tool-use loop)
- **LLM**: Llama 3.3-70B via Groq API
- **Web search**: Tavily API
- **UI**: Streamlit
- **Language**: Python

## Architecture

User input → LangGraph agent → 5 parallel tool calls (Tavily search) 
→ LLM synthesises results → Structured markdown report → Download

The agent uses a Think → Act → Observe loop. After each tool call, 
the LLM reads the result and decides what to search next — no 
hardcoded steps.

## Run locally

```bash
git clone https://github.com/YOUR_USERNAME/job-research-agent
cd job-research-agent
pip install -r requirements.txt

# Add your keys to .env
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key

streamlit run app.py
```

## Live demo

[your-app.streamlit.app](https://your-app.streamlit.app)

## What I learned building this

- LangGraph state machine design — typed state, conditional edges
- Tool binding with LLMs — how the model decides which tool to call
- Prompt engineering for structured output
- Agent loop termination — preventing infinite loops