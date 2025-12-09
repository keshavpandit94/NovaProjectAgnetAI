import os
from fastapi import FastAPI
from app.api.v1.chat_router import router as chat_router
from app.api.v1.auth_router import router as auth_router 
from app.api.v1.history_router import router as history_router 
from app.database.connection import connect_db, close_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Gemini Multimodal Agent Backend",
    description="FastAPI application using Gemini and MongoDB for history and auth.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allows all headers (including Content-Type)
)

# --- Startup and Shutdown Events ---
@app.on_event("startup")
def startup_event():
    connect_db()

@app.on_event("shutdown")
def shutdown_event():
    close_db()
    
# --- Include Routers ---
app.include_router(chat_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1") 
app.include_router(history_router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Gemini Multimodal Agent Backend is running."}

# To Run locally: uvicorn main:app --reload --port 8001
# For Render/production: uvicorn main:app --host 0.0.0.0 --port $PORT (uses PORT env var)