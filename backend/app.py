from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import employee
from api import project, task, time, screenshot  # Uncomment when these files exist

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee.router, prefix="/api/employees", tags=["employees"])
app.include_router(project.router, prefix="/api/projects", tags=["projects"])
app.include_router(task.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(time.router, prefix="/api/time", tags=["time"])
app.include_router(screenshot.router, prefix="/api/screenshots", tags=["screenshots"])

@app.get("/")
def read_root():
    return {"status": "ok"} 