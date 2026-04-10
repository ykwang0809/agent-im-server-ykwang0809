from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.database import get_db, Conversation, Message
from utils.id_generator import generate_uuid
from agent.engine import agent_engine
from typing import Optional

router = APIRouter()


class ConversationCreate(BaseModel):
    title: str


class MessageSend(BaseModel):
    content: str


@router.post("/conversations")
def create_conversation(data: ConversationCreate, db: Session = Depends(get_db)):
    conv_id = generate_uuid()
    conv = Conversation(id=conv_id, title=data.title)
    db.add(conv)
    db.commit()
    return {"id": conv_id, "title": data.title}


@router.get("/conversations")
def list_conversations(db: Session = Depends(get_db)):
    convs = db.query(Conversation).order_by(Conversation.created_at.desc()).all()
    return [{"id": c.id, "title": c.title, "created_at": c.created_at} for c in convs]


@router.get("/conversations/{conv_id}/messages")
def get_messages(conv_id: str, cursor: Optional[int] = 0, limit: int = 20, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(
        Message.conversation_id == conv_id,
        Message.id > cursor
    ).order_by(Message.id).limit(limit).all()
    return [{
        "id": m.id,
        "sender_type": m.sender_type,
        "content": m.content,
        "created_at": m.created_at
    } for m in messages]


@router.post("/conversations/{conv_id}/messages")
async def send_message(conv_id: str, data: MessageSend, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conv_id).first()
    if not conv:
        raise HTTPException(404, "会话不存在")

    user_msg = Message(conversation_id=conv_id, sender_type="user", content=data.content)
    db.add(user_msg)
    db.commit()

    return {"status": "ok", "message_id": user_msg.id}