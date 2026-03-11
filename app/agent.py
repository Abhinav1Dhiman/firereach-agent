import json
from groq import Groq
from app.config import GROQ_API_KEY
from app.tools.signal_harvester import tool_signal_harvester
from app.tools.research_analyst import tool_research_analyst
from app.tools.outreach_sender import tool_outreach_automated_sender

client = Groq(api_key=GROQ_API_KEY)

tools = [
    {
        "type": "function",
        "function": {
            "name": "tool_signal_harvester",
            "description": "Deterministic tool that fetches recent news and live buyer signals (funding, hiring, leadership) for a target company.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {"type": "string", "description": "The name of the target company to research"}
                },
                "required": ["company"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_research_analyst",
            "description": "AI tool that takes the harvested signals and the user's ICP to generate a 2-paragraph Account Brief.",
            "parameters": {
                "type": "object",
                "properties": {
                    "signals": {"type": "string", "description": "The raw signals collected by the harvester"},
                    "icp": {"type": "string", "description": "The Ideal Customer Profile (ICP)"}
                },
                "required": ["signals", "icp"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "tool_outreach_automated_sender",
            "description": "AI-driven tool that transforms the research brief into a hyper-personalized email and dispatches it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "brief": {"type": "string", "description": "The 2-paragraph account brief summarizing the target company's pain points"},
                    "email": {"type": "string", "description": "The target email address to send the completed email to"}
                },
                "required": ["brief", "email"]
            }
        }
    }
]

def run_agent(company: str, icp: str, email: str):
    system_prompt = f"""
    You are FireReach, an autonomous outreach engine.
    You must execute a strict sequence to generate and send outreach:
    1. Call tool_signal_harvester to gather live signals on the target company '{company}'.
    2. Call tool_research_analyst with the harvested signals and ICP '{icp}' to generate a brief.
    3. Call tool_outreach_automated_sender with the generated brief and target email '{email}'.
    You must NOT guess any signals. You MUST wait for the tool output before proceeding to the next step.
    Once the automated sender tool is called, summarize your work to the user and end.
    """

    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": "Begin the sequence."}]
    log = []
    
    for step in range(6):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        msg = response.choices[0].message
        
        messages.append({
            "role": "assistant",
            "content": msg.content,
            "tool_calls": getattr(msg, "tool_calls", None)
        })
        
        if getattr(msg, "tool_calls", None):
            for tool_call in msg.tool_calls:
                func_name = tool_call.function.name
                try:
                    args = json.loads(tool_call.function.arguments)
                except:
                    args = {}
                
                log.append(f"Agent called {func_name}")
                
                try:
                    if func_name == "tool_signal_harvester":
                        res = tool_signal_harvester(args.get("company", company))
                    elif func_name == "tool_research_analyst":
                        res = tool_research_analyst(str(args.get("signals", "")), args.get("icp", icp))
                    elif func_name == "tool_outreach_automated_sender":
                        res = tool_outreach_automated_sender(args.get("brief", ""), args.get("email", email))
                    else:
                        res = "Unknown tool"
                except Exception as e:
                    res = f"Error: {e}"
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": str(res)
                })
        else:
            log.append("Agent finished.")
            break
            
    return {
        "status": "success",
        "log": log,
        "final_response": msg.content
    }