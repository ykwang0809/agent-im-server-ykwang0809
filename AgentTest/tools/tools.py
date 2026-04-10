import json
import time
from .registry import tool_registry

# 1. 获取天气
def get_weather(city: str) -> str:
    return f"{city} 当前天气：晴，25℃，湿度60%"

# 2. 知识搜索
def search_knowledge(query: str) -> str:
    return f"关于「{query}」的搜索结果：这是模拟知识返回"

# 3. 创建任务
def create_task(title: str, assignee: str) -> str:
    return f"任务已创建：{title}，负责人：{assignee}，状态：待处理"

# 注册工具
tool_registry.register(
    name="get_weather",
    description="获取指定城市的天气",
    parameters={
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "城市名称"}
        },
        "required": ["city"]
    },
    func=get_weather
)

tool_registry.register(
    name="search_knowledge",
    description="搜索知识信息",
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"}
        },
        "required": ["query"]
    },
    func=search_knowledge
)

tool_registry.register(
    name="create_task",
    description="创建任务",
    parameters={
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "任务标题"},
            "assignee": {"type": "string", "description": "负责人"}
        },
        "required": ["title", "assignee"]
    },
    func=create_task
)