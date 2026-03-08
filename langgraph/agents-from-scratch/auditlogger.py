import json
import uuid
import threading
import queue
from datetime import datetime
from langchain_core.callbacks import BaseCallbackHandler
import auditlogger


class ProductionAuditLogger(BaseCallbackHandler):
    def __init__(self, filename="audit.log", session_id=None):
        self.filename = filename
        self.session_id = session_id or str(uuid.uuid4())
        self.log_queue = queue.Queue()
        self._stop_event = threading.Event()

        # Start background writer thread
        self.worker = threading.Thread(target=self._writer, daemon=True)
        self.worker.start()

    # ---------- Internal Utilities ----------

    def _timestamp(self):
        return datetime.utcnow().isoformat() + "Z"

    def _enqueue(self, payload: dict):
        payload["timestamp"] = self._timestamp()
        payload["session_id"] = self.session_id
        self.log_queue.put(payload)

    def _writer(self):
        with open(self.filename, "a", encoding="utf-8") as f:
            while not self._stop_event.is_set() or not self.log_queue.empty():
                try:
                    record = self.log_queue.get(timeout=0.5)
                    f.write(json.dumps(record) + "\n")
                    f.flush()
                except queue.Empty:
                    continue

    def shutdown(self):
        self._stop_event.set()
        self.worker.join()

    # ---------- Callback Hooks ----------

    def on_chat_model_start(self, serialized, messages, **kwargs):
        if messages:
            self._enqueue({
                "type": "human",
                "content": messages[-1].content
            })

    def on_llm_end(self, response, **kwargs):
        try:
            text = response.generations[0][0].text
        except Exception:
            text = str(response)

        self._enqueue({
            "type": "ai",
            "content": text
        })

    def on_tool_start(self, serialized, input_str, **kwargs):
        self._enqueue({
            "type": "tool_start",
            "tool": serialized.get("name"),
            "input": input_str
        })

    def on_tool_end(self, output, **kwargs):
        self._enqueue({
            "type": "tool_end",
            "output": output
        })
