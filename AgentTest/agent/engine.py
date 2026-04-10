import json
import time
import asyncio
from typing import List, Dict
from sqlalchemy.orm import Session
from db.database import Message, ToolCallRecord
from agent.llm import llm_client
from tools.registry import tool_registry


class AgentEngine:
    def __init__(self, max_loops: int = 10):
        self.max_loops = max_loops

    async def run(self, conversation_id: str, db: Session, send_event):
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()

        chat_history = [
            {"role": "user" if m.sender_type == "user" else "assistant", "content": m.content}
            for m in messages
        ]

        full_response = ""
        loop_count = 0

        while loop_count < self.max_loops:
            loop_count += 1
            response = llm_client.chat(chat_history)
            choice = response["choices"][0]["message"]

            if "tool_calls" in choice:
                tool_call = choice["tool_calls"][0]
                func = tool_call["function"]
                tool_name = func["name"]
                args = json.loads(func["arguments"])

                # 推送工具调用事件
                await send_event({
                    "event": "tool_call",
                    "data": {"tool": tool_name, "arguments": args}
                })

                # 执行工具
                start = time.time()
                tool = tool_registry.get_tool(tool_name)
                result = tool["func"](**args)
                duration = time.time() - start

                # 记录工具调用
                msg = Message(conversation_id=conversation_id, sender_type="agent", content="")
                db.add(msg)
                db.commit()

                record = ToolCallRecord(
                    conversation_id=conversation_id,
                    message_id=msg.id,
                    tool_name=tool_name,
                    arguments=json.dumps(args),
                    result=result,
                    duration=duration
                )
                db.add(record)
                db.commit()

                await send_event({
                    "event": "tool_result",
                    "data": {"tool": tool_name, "result": result, "duration": duration}
                })

                chat_history.append(choice)
                chat_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": result
                })
            else:
                content = choice.get("content", "")
                full_response = content
                await send_event({
                    "event": "text_delta",
                    "data": {"content": content}
                })
                break

        # 保存最终消息
        agent_msg = Message(
            conversation_id=conversation_id,
            sender_type="agent",
            content=full_response
        )
        db.add(agent_msg)
        db.commit()

        await send_event({"event": "done", "data": {"status": "completed"}})
        return full_response


agent_engine = AgentEngine()