from fastapi import APIRouter, Request, Form
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from app.ai_orchestrator import AIOrchestrator
from app.database import save_message_log
from app.email_sender import send_report
from app.config import settings

router = APIRouter()
orchestrator = AIOrchestrator()
twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

@router.post("/webhook")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...)
):
    reply = await orchestrator.generate(Body, context={"channel": "whatsapp"})

    twilio_client.messages.create(
        from_=settings.TWILIO_WHATSAPP_FROM,
        body=reply,
        to=From
    )

    await save_message_log(From, Body, "incoming")
    await save_message_log(From, reply, "outgoing")
    await send_report({"type": "whatsapp", "from": From, "in": Body, "out": reply})

    return "", 200

@router.post("/send")
async def send_whatsapp(to: str, body: str):
    msg = twilio_client.messages.create(
        from_=settings.TWILIO_WHATSAPP_FROM,
        body=body,
        to=f"whatsapp:{to}"
    )
    return {"sid": msg.sid}