from fastapi import FastAPI
from app.schemas import OutreachRequest
from app.agent import run_agent

app = FastAPI()

@app.get("/")
def home():
    return {"message":"FireReach Agent Running"}

@app.post("/run-agent")
def run(req: OutreachRequest):

    result = run_agent(
        req.company,
        req.icp,
        req.email
    )

    return result