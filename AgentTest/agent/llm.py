import os
import json
import requests
from dotenv import load_dotenv
from tools.registry import tool_registry

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY", "mock_key")
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

    def chat(self, messages: list, stream: bool = False):
        tools = tool_registry.get_all_tools()
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "stream": stream
        }
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload, headers=headers, timeout=30
            )
            return response.json()
        except Exception:
            return self.mock_response(messages)

    def mock_response(self, messages: list):
        last_msg = messages[-1]["content"]
        if "天气" in last_msg:
            return {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "tool_calls": [{
                            "id": "mock_1",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": json.dumps({"city": "北京"})
                            }
                        }]
                    }
                }]
            }
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": f"已收到：{last_msg}"
                }
            }]
        }

llm_client = LLMClient()