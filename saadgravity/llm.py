import json
import re
from typing import List, Dict, Any, Tuple
import httpx
from openai import OpenAI
from .tools import TOOL_DEFINITIONS


class LLMClient:
    def __init__(
        self,
        api_base: str,
        api_key: str,
        model: str,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ):
        self.api_base = api_base.rstrip("/")
        self.api_key = api_key or "ollama"
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._init_client()

    def _init_client(self):
        # We configure httpx client with generous timeouts
        http_client = httpx.Client(timeout=180.0)
        self.client = OpenAI(
            base_url=self.api_base, api_key=self.api_key, http_client=http_client
        )

    def check_connection(self) -> Tuple[bool, str]:
        """Test connection to the API endpoint and list models if possible."""
        try:
            models = self.client.models.list()
            model_names = [m.id for m in models.data]
            return (
                True,
                f"Connected to {self.api_base}. Available models: {', '.join(model_names[:5])}",
            )
        except Exception as e:
            return False, f"Connection failed to {self.api_base}: {str(e)}"

    def chat_completion(
        self, messages: List[Dict[str, Any]], use_tools: bool = True
    ) -> Dict[str, Any]:
        """Send chat messages and get response with tool calls or text."""
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        if use_tools:
            kwargs["tools"] = TOOL_DEFINITIONS
            kwargs["tool_choice"] = "auto"

        try:
            response = self.client.chat.completions.create(**kwargs)
            choice = response.choices[0]
            message = choice.message

            tool_calls = []
            if getattr(message, "tool_calls", None):
                for tc in message.tool_calls:
                    try:
                        args = json.loads(tc.function.arguments)
                    except Exception:
                        args = {"raw": tc.function.arguments}
                    tool_calls.append(
                        {"id": tc.id, "name": tc.function.name, "arguments": args}
                    )

            # Check if there is fallback text tool_call inside content
            content = message.content or ""
            if not tool_calls and content:
                extracted = self._extract_text_tool_calls(content)
                if extracted:
                    tool_calls.extend(extracted)

            return {
                "role": "assistant",
                "content": content,
                "tool_calls": tool_calls,
                "raw_message": message,
            }
        except Exception as e:
            # If native tools failed (e.g. model doesn't support tools parameter), retry without tools parameter
            if use_tools:
                return self.chat_completion(messages, use_tools=False)
            raise e

    def _extract_text_tool_calls(self, text: str) -> List[Dict[str, Any]]:
        """Fallback extractor for models that write tool calls inside code blocks."""
        calls = []
        # Pattern 1: ```tool_call ... ```
        matches = re.findall(
            r"```(?:tool_call|json)\s*(\{.*?\})\s*```", text, re.DOTALL
        )
        for m in matches:
            try:
                data = json.loads(m.strip())
                if "name" in data and "arguments" in data:
                    calls.append(
                        {
                            "id": f"call_{len(calls)}",
                            "name": data["name"],
                            "arguments": data["arguments"],
                        }
                    )
            except Exception:
                continue
        return calls
