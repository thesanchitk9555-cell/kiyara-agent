from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from app.config import settings
import os

# Render uses ephemeral storage, so use /tmp for SQLite
db_path = "/tmp/kiyara.db" if os.getenv("RENDER") else "./kiyara.db"
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class CallLog(Base):
    __tablename__ = "call_logs"
    id = Column(Integer, primary_key=True)
    from_number = Column(String(20))
    user_text = Column(Text)
    ai_reply = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class MessageLog(Base):
    __tablename__ = "message_logs"
    id = Column(Integer, primary_key=True)
    to_number = Column(String(20))
    body = Column(Text)
    direction = Column(String(10))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

async def save_call_log(from_number, user_text, ai_reply):
    db = SessionLocal()
    db.add(CallLog(from_number=from_number, user_text=user_text, ai_reply=ai_reply))
    db.commit()
    db.close()

async def save_message_log(to_number, body, direction):
    db = SessionLocal()
    db.add(MessageLog(to_number=to_number, body=body, direction=direction))
    db.commit()
    db.close()