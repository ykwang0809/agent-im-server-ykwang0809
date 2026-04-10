from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
import json
from db.database import get_db
from agent.engine import agent_engine

router = APIRouter()
active_connections = {}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str, db: Session = Depends(get_db)):
    await websocket.accept()

    if conversation_id not in active_connections:
        active_connections[conversation_id] = []
    active_connections[conversation_id].append(websocket)

    async def send_event(event):
        for conn in active_connections[conversation_id]:
            await conn.send_text(json.dumps(event))

    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            if msg.get("action") == "run_agent":
                await agent_engine.run(conversation_id, db, send_event)
    except WebSocketDisconnect:
        active_connections[conversation_id].remove(websocket)
        if not active_connections[conversation_id]:
            del active_connections[conversation_id]