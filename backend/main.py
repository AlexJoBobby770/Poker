# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import session_router, recommend_router

app = FastAPI(
    title="Poker AI Assistant API",
    description="Backend API engine managing Monte Carlo hand equity simulation and opponent profiling.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount application sub-routers under the /api path namespace
app.include_router(session_router.router, prefix="/api")
app.include_router(recommend_router.router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Poker AI Assistant API is fully operational",
        "active_engine": "Monte Carlo Simulator v1"
    }