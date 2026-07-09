from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.database import Base
from database.connection import engine
from routers import interactions

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-First CRM HCP Module",
    description="Log and manage interactions with Healthcare Professionals using AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(interactions.router)

@app.get("/")
def root():
    return {
        "message": "AI-First CRM HCP Module API",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

def start():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start()
