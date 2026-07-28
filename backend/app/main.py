from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.call_handler import router as call_router
from app.whatsapp_handler import router as whatsapp_router
from app.email_sender import router as email_router
import json
import os

app = FastAPI(title="Kiyara AI Agent", version="1.0")

# CORS for Render frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://kiyara-frontend.onrender.com",
        "http://localhost:3000"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(call_router, prefix="/calls", tags=["Calls"])
app.include_router(whatsapp_router, prefix="/whatsapp", tags=["WhatsApp"])
app.include_router(email_router, prefix="/email", tags=["Email"])

@app.get("/")
async def root():
    return {
        "message": "Kiyara is online!",
        "version": "1.0",
        "environment": os.getenv("RENDER", "development")
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(json.dumps({"type": "echo", "text": data}))
    except Exception:
        pass