import asyncio
import os
from fastapi import APIRouter, Request, BackgroundTasks
from app.ai_orchestrator import AIOrchestrator
from app.database import save_call_log
from app.email_sender import send_report

# Google Cloud clients - lazy load to handle missing credentials
stt_client = None
tts_client = None

try:
    from google.cloud import speech_v1
    from google.cloud import texttospeech
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        stt_client = speech_v1.SpeechClient()
        tts_client = texttospeech.TextToSpeechClient()
except Exception as e:
    print(f"⚠️ Google Cloud not configured: {e}")

router = APIRouter()
orchestrator = AIOrchestrator()

@router.post("/incoming")
async def incoming_call_webhook(request: Request, bg: BackgroundTasks):
    data = await request.json()
    call_id = data.get("callId")
    from_number = data.get("from")
    session_id = data.get("sessionId")
    bg.add_task(handle_call_flow, call_id, from_number, session_id)
    return {"status": "accepted"}

@router.post("/outgoing")
async def make_outgoing_call(to: str, message: str = None):
    # In production, use VideoSDK SIP API
    return {"status": "dialing", "to": to}

async def handle_call_flow(call_id: str, from_number: str, session_id: str):
    print(f"🔊 Kiyara handling call from {from_number}")

    # Simulate audio (replace with real stream from VideoSDK)
    user_text = "नमस्ते, मुझे कॉलेज के बारे में जानकारी चाहिए।"

    print(f"👤 User said: {user_text}")

    # AI reply
    ai_reply = await orchestrator.generate(user_text, context={"caller": from_number})
    print(f"🤖 Kiyara replies: {ai_reply}")

    # If Google Cloud is configured, generate TTS
    audio_out = None
    if tts_client:
        try:
            synthesis_input = texttospeech.SynthesisInput(text=ai_reply)
            voice = texttospeech.VoiceSelectionParams(
                language_code="hi-IN",
                name="hi-IN-Standard-A",
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MULAW
            )
            tts_response = tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            audio_out = tts_response.audio_content
            print(f"🎵 TTS generated: {len(audio_out)} bytes")
        except Exception as e:
            print(f"❌ TTS error: {e}")

    # Save log and email report
    await save_call_log(from_number, user_text, ai_reply)
    await send_report({"type": "call", "from": from_number, "transcript": user_text, "reply": ai_reply})

    print("✅ Call handled")