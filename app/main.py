from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, summary, chatbot

app = FastAPI(title="AI-Powered Finance Chatbot (Backend Only)")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
         "http://localhost:8501",   # Streamlit default
         "http://127.0.0.1:8501",   # Streamlit alt
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(summary.router, prefix="/summary", tags=["Summary"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Finance Chatbot API running 🚀"}
