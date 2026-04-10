from typing import Dict, Callable, Any
import json

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, dict] = {}

    def register(self, name: str, description: str, parameters: dict, func: Callable):
        self.tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters,
            "func": func
        }

    def get_tool(self, name: str) -> dict:
        return self.tools.get(name)

    def get_all_tools(self) -> list:
        return [
            {
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t["description"],
                    "parameters": t["parameters"]
                }
            } for t in self.tools.values()
        ]

tool_registry = ToolRegistry()