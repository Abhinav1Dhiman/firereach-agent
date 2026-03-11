# FireReach Autonomous Outreach Agent

## Architecture

User Input
→ Signal Harvester
→ Research Analyst
→ Outreach Sender

## Tools

1. tool_signal_harvester
Captures growth signals for a company.

2. tool_research_analyst
LLM analyzes signals and ICP to generate account insights.

3. tool_outreach_automated_sender
Creates and sends personalized outreach email.

## Tech Stack

FastAPI
Groq Llama3
SMTP Email
Python

## Running

pip install -r requirements.txt

uvicorn main:app --reload