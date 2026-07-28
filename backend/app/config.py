from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # VideoSDK
    VIDEOSDK_API_KEY: str
    VIDEOSDK_SECRET: str
    VIDEOSDK_BASE_URL: str = "https://api.videosdk.live/v2"

    # AI Models
    OPENAI_API_KEY: str
    DEEPSEEK_API_KEY: str
    GEMINI_API_KEY: str

    # Twilio (WhatsApp)
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_WHATSAPP_FROM: str = "whatsapp:+14155238886"

    # Google Cloud (STT/TTS)
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None

    # Email (Resend)
    RESEND_API_KEY: str
    ADMIN_EMAIL: str

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./kiyara.db"
    RENDER: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()