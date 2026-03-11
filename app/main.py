import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.schemas import OutreachRequest
from app.agent import run_agent

app = FastAPI()

@app.post("/run-agent")
def run(req: OutreachRequest):
    result = run_agent(
        req.company,
        req.icp,
        req.email
    )
    return result

# Serve the React frontend if the dist folder exists
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

if os.path.exists(frontend_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def catch_all(full_path: str):
        file_path = os.path.join(frontend_path, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_path, "index.html"))
else:
    @app.get("/")
    def home():
        return {"message": "FireReach Agent API Running (Frontend not built)"}