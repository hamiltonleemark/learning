from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
#from langchain.agents import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.callbacks import BaseCallbackHandler

from langchain_core.callbacks import BaseCallbackHandler
from datetime import datetime
import uuid
import json
import auditlogger


class FileLoggerCallback(BaseCallbackHandler):
    def __init__(self, filename="trace.log", session_id=None):
        self.filename = filename
        self.session_id = session_id or str(uuid.uuid4())

    def _timestamp(self):
        return datetime.utcnow().isoformat() + "Z"

    def _write(self, payload: dict):
        payload["timestamp"] = self._timestamp()
        payload["session_id"] = self.session_id

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")

    # Logs user input
    def on_chat_model_start(self, serialized, messages, **kwargs):
        if messages and len(messages) > 0:
            last_message = messages[-1]
            self._write({
                "type": "human",
                "content": last_message.content
            })

    # Logs AI output
    def on_llm_end(self, response, **kwargs):
        try:
            text = response.generations[0][0].text
        except Exception:
            text = str(response)

        self._write({
            "type": "ai",
            "content": text
        })


def write_email(to: str, subject: str, content: str) -> str:
    """ Node that writes an email based on the request.

    It uses the write_email tool to generate the email content.
    The request is passed as an argument to the tool, and the generated email
    is stored in the state.
    """

    return f"Email sent to {to} with subject '{subject}' and content: {content}"


def test_write_email_react():

    load_dotenv("../../.env", override=True)
    llm = init_chat_model("openai:gpt-4.1", temperature=0,
                          callbacks=[auditlogger.ProductionAuditLogger()])

    agent = create_react_agent(
        model=llm,
        tools=[write_email],
        prompt="Respond to the user's request using the tools provided.",
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Draft a response to my boss confirming that I want to attend Interrupt! My name is Mark. My boss's name is Sarah."}]}
    )

    for item in result["messages"]:
        item.pretty_print()
