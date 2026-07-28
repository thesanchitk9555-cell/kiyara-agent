# Kiyara – Autonomous AI Agent for College Operations

Kiyara handles incoming/outgoing voice calls, WhatsApp messaging, and sends email reports using AI (Gemini/OpenAI/DeepSeek).

## Features
- Incoming/outgoing calls with human‑like female voice
- WhatsApp messaging
- Automatic email reports via Resend
- Real‑time dashboard
- Multi‑model AI fallback

## Setup
1. Copy `.env.example` to `.env` and fill all API keys.
2. Place Google service account JSON in `creds/google.json`.
3. Run `docker-compose up --build`.

## Endpoints
- `POST /calls/incoming` – webhook for VideoSDK
- `POST /calls/outgoing` – initiate call
- `POST /whatsapp/webhook` – Twilio webhook
- `POST /whatsapp/send` – send WhatsApp message
- `POST /email/test` – test email

## Tech Stack
- FastAPI (backend)
- React (frontend)
- VideoSDK, Twilio, Resend
- Gemini/OpenAI/DeepSeek