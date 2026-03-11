from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def tool_research_analyst(signals, icp):

    prompt = f"""
You are a GTM research analyst.

Signals:
{signals}

ICP:
{icp}

Write a 2 paragraph account brief explaining:

1) what the company is doing
2) their pain points
3) why they need the ICP solution
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content