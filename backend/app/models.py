from pydantic import BaseModel
from typing import Optional

class IncomingCallPayload(BaseModel):
    callId: str
    from_: str
    to: str
    sessionId: Optional[str] = None

class OutgoingCallRequest(BaseModel):
    to_number: str
    message: Optional[str] = None

class WhatsAppWebhookPayload(BaseModel):
    From: str
    Body: str
    ProfileName: Optional[str] = None

class EmailReportPayload(BaseModel):
    type: str
    data: dict