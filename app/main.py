import os
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.schemas import OutreachRequest
from app.agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run-agent")
def run(req: OutreachRequest):
    try:
        result = run_agent(
            req.company,
            req.icp,
            req.email
        )
        return result
    except Exception as e:
        return {
            "status": "error",
            "log": [f"Agent error: {str(e)}"],
            "final_response": f"An error occurred: {traceback.format_exc()}"
        }

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