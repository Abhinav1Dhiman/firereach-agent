# FireReach Autonomous Outreach Engine - Documentation

## 1. Logic Flow
FireReach employs a ReAct (Reasoning and Acting) architectural loop powered by the Groq `llama-3.3-70b-versatile` model. 

1. **Initialization:** The user inputs the Target Company, Ideal Customer Profile (ICP), and Target Email via the premium React dashboard.
2. **Signal Capture (Deterministic):** The agent initiates the sequence by calling `tool_signal_harvester`. This tool bypasses LLM hallucination by performing a live DuckDuckGo search querying for specific, high-value intent triggers such as "(funding OR hiring OR leadership OR acquisition OR new product OR growth)".
3. **Contextual Research:** Once the live signals are harvested, the agent explicitly calls `tool_research_analyst`. This tool synthesizes the raw JSON signals and the user's ICP to generate a highly contextual, 2-paragraph Account Brief. It connects the company's real-time events to the value proposition of the ICP.
4. **Automated Execution:** Satisfied with the research brief, the agent finally calls `tool_outreach_automated_sender`. This tool transforms the brief into a hyper-personalized, template-free cold email (guaranteed under 120 words and referencing the live signals) and automatically dispatches it using SMTP SSL.
5. **Completion:** The agent summarizes its actions and streams the completion back to the frontend.

## 2. Tool Schemas
The agent uses strict Function Calling (JSON tracking) for execution. The schemas provided to the Groq model are:

### `tool_signal_harvester`
```json
{
  "name": "tool_signal_harvester",
  "description": "Deterministic tool that fetches recent news and live buyer signals (funding, hiring, leadership) for a target company.",
  "parameters": {
    "type": "object",
    "properties": {
      "company": { "type": "string", "description": "The name of the target company to research" }
    },
    "required": ["company"]
  }
}
```

### `tool_research_analyst`
```json
{
  "name": "tool_research_analyst",
  "description": "AI tool that takes the harvested signals and the user's ICP to generate a 2-paragraph Account Brief.",
  "parameters": {
    "type": "object",
    "properties": {
      "signals": { "type": "string", "description": "The raw signals collected by the harvester" },
      "icp": { "type": "string", "description": "The Ideal Customer Profile (ICP)" }
    },
    "required": ["signals", "icp"]
  }
}
```

### `tool_outreach_automated_sender`
```json
{
  "name": "tool_outreach_automated_sender",
  "description": "AI-driven tool that transforms the research brief into a hyper-personalized email and dispatches it.",
  "parameters": {
    "type": "object",
    "properties": {
      "brief": { "type": "string", "description": "The 2-paragraph account brief summarizing the company's pain points" },
      "email": { "type": "string", "description": "The target email address to send the completed email to" }
    },
    "required": ["brief", "email"]
  }
}
```

## 3. System Prompt
The underlying persona and constraints applied to FireReach:

> "You are FireReach, an autonomous outreach engine.
> You must execute a strict sequence to generate and send outreach:
> 1. Call tool_signal_harvester to gather live signals on the target company '[COMPANY_NAME]'.
> 2. Call tool_research_analyst with the harvested signals and ICP '[ICP_DESCRIPTION]' to generate a brief.
> 3. Call tool_outreach_automated_sender with the generated brief and target email '[TARGET_EMAIL]'.
> You must NOT guess any signals. You MUST wait for the tool output before proceeding to the next step.
> Once the automated sender tool is called, summarize your work to the user and end."

## 4. Deployment Instructions
The application is structured for a decoupled deployment strategy:

### Backend (Render/Railway/Heroku)
1. Link your GitHub repository to Render and deploy as a **Web Service**.
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set Environment Variables: `GROQ_API_KEY`, `EMAIL_USER`, `EMAIL_PASS`.

### Frontend (Vercel/Netlify)
1. Link your GitHub repository to Vercel and set the Root Directory to `frontend`.
2. Vercel will automatically detect Vite. 
3. *Important:* Update the `fetch()` call in `frontend/src/App.jsx` to point to your new deployed Render backend URL instead of `/run-agent` before pushing to production (or setup a rewrite in `vercel.json`).
