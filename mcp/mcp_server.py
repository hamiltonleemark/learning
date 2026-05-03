# mcp_server.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict, Callable

app = FastAPI()

# -------------------------
# Tool Registry
# -------------------------
TOOLS: Dict[str, Callable] = {}

def tool(name: str):
    def decorator(func: Callable):
        TOOLS[name] = func
        return func
    return decorator

# -------------------------
# Example Tools
# -------------------------
@tool("ping")
def ping():
    return {"status": "ok"}

@tool("add")
def add(a: int, b: int):
    return {"result": a + b}

@tool("echo")
def echo(message: str):
    return {"echo": message}

# -------------------------
# MCP Request Model
# -------------------------
class MCPRequest(BaseModel):
    method: str
    params: Dict[str, Any] = {}

# -------------------------
# MCP Endpoint
# -------------------------
@app.post("/mcp")
def handle_mcp(req: MCPRequest):
    if req.method == "tools/list":
        return {
            "tools": [
                {
                    "name": name,
                    "description": func.__doc__ or "",
                }
                for name, func in TOOLS.items()
            ]
        }

    elif req.method == "tools/call":
        tool_name = req.params.get("name")
        args = req.params.get("arguments", {})

        if tool_name not in TOOLS:
            return {"error": f"Tool '{tool_name}' not found"}

        try:
            result = TOOLS[tool_name](**args)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}

    return {"error": f"Unknown method {req.method}"}
