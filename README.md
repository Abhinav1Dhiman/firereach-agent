# 🔥 FireReach — The Autonomous Outreach Engine

> An AI-powered outreach agent that researches companies using live signals, generates hyper-personalized emails, and sends them — all autonomously.

**Live Demo:** [firereach-agent-ra87.onrender.com](https://firereach-agent-ra87.onrender.com)

---

## ✨ What It Does

FireReach eliminates the manual grind of SDR outreach. Give it a **target company**, your **Ideal Customer Profile (ICP)**, and a **recipient email** — and it will:

1. 🔍 **Harvest Live Signals** — Fetches real-time news about funding rounds, hiring surges, leadership changes, and product launches using DuckDuckGo search.
2. 🧠 **Analyze & Research** — An AI analyst synthesizes the raw signals with your ICP to generate a 2-paragraph Account Brief highlighting pain points and strategic alignment.
3. 📧 **Draft & Send Email** — Generates a hyper-personalized cold email (zero templates, referencing real signals) and automatically dispatches it via Gmail SMTP.

All three steps are orchestrated by an **autonomous agent loop** using Groq's Function Calling API.

---

## 🏗️ Architecture

```
User Input (Company + ICP + Email)
        │
        ▼
┌──────────────────────────┐
│   🤖 FireReach Agent     │  ← Groq LLM with Function Calling
│   (ReAct Loop)           │
└──────────┬───────────────┘
           │
    ┌──────┼──────────────────────┐
    │      │                      │
    ▼      ▼                      ▼
┌────────┐ ┌──────────────┐ ┌───────────────┐
│Signal  │ │ Research     │ │ Outreach      │
│Harvester│ │ Analyst     │ │ Sender        │
│(DuckDuck│ │ (Groq LLM) │ │ (Groq + SMTP) │
│Go Search)│ └──────────────┘ └───────────────┘
└────────┘
```

---

## 🛠️ Tech Stack

| Component       | Technology                        |
|-----------------|-----------------------------------|
| **LLM**         | Groq (Llama 3.3 70B Versatile)    |
| **Backend**     | FastAPI (Python)                   |
| **Frontend**    | React + Vite                       |
| **Signal Tool** | DuckDuckGo Search (deterministic) |
| **Email**       | Gmail SMTP (via `smtplib`)         |
| **Deployment**  | Render                             |

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9+
- Node.js 18+
- A [Groq API Key](https://console.groq.com/)
- A Gmail account with [App Password](https://myaccount.google.com/apppasswords) enabled

### 1. Clone & Setup Backend
```bash
git clone https://github.com/Abhinav1Dhiman/firereach-agent.git
cd firereach-agent

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
EMAIL_USER=your_gmail@gmail.com
EMAIL_PASS=your_gmail_app_password
```

### 3. Run Backend
```bash
uvicorn app.main:app --reload
```

### 4. Run Frontend (for development)
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to use the dashboard.

---

## 🧪 The Rabbitt Challenge

This agent was built to handle the following scenario:

> **User ICP:** "We sell high-end cybersecurity training to Series B startups."
>
> **Task:** "Find companies with recent growth signals and send a personalized outreach email that connects their expansion to our security training."

The agent successfully:
- ✅ Harvests **real, live signals** (no hallucinated data)
- ✅ Generates a **grounded Account Brief** tied to the ICP
- ✅ Drafts a **zero-template email** referencing specific signals
- ✅ **Automatically sends** the email via SMTP

---

## 📁 Project Structure

```
firereach-agent/
├── app/
│   ├── agent.py              # ReAct agent loop with Groq tool calling
│   ├── config.py             # Environment variable loader
│   ├── main.py               # FastAPI server + static file serving
│   ├── schemas.py            # Pydantic request models
│   └── tools/
│       ├── signal_harvester.py    # Live signal fetcher (DuckDuckGo)
│       ├── research_analyst.py    # AI account brief generator
│       └── outreach_sender.py     # Email drafter + Gmail sender
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # React dashboard component
│   │   └── index.css         # Premium dark-mode styles
│   └── dist/                 # Pre-built production bundle
├── DOCS.md                   # Agent documentation (schemas, prompts)
├── render.yaml               # Render deployment config
├── requirements.txt          # Python dependencies
└── .env                      # Environment secrets (not committed)
```

---

## 📖 Documentation

See [DOCS.md](DOCS.md) for:
- **Logic Flow** — How the agent ensures outreach is grounded in harvested signals
- **Tool Schemas** — JSON schemas for all three function calls
- **System Prompt** — The persona and constraint prompt guiding the agent

---

## 👤 Author

**Abhinav Dhiman**
- GitHub: [@Abhinav1Dhiman](https://github.com/Abhinav1Dhiman)

---

## 📝 License

This project is built as part of the Rabbitt AI Agentic Developer Challenge.