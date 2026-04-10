from fastapi import FastAPI
import uvicorn
from api import conversation, websocket
from db.database import init_db
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Agent IM Server", version="1.0")

# 初始化数据库
init_db()

# 注册路由
app.include_router(conversation.router)
app.include_router(websocket.router)

@app.get("/")
def root():
    return {"message": "Agent IM Server running"}

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=True)
