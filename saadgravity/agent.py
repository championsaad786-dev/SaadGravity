import json
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from .llm import LLMClient
from .prompt import SYSTEM_PROMPT
from .tools import dispatch_tool
from .config import load_config

console = Console()


class AutonomousAgent:
    def __init__(self, config: Optional[dict] = None):
        self.config = config or load_config()
        self.client = LLMClient(
            api_base=self.config["api_base"],
            api_key=self.config["api_key"],
            model=self.config["model"],
            temperature=self.config.get("temperature", 0.2),
            max_tokens=self.config.get("max_tokens", 4096),
        )
        self.messages: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self.auto_execute = self.config.get("auto_execute", True)
        self.max_steps = 25

    def reset_conversation(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def set_model(self, model_name: str):
        self.config["model"] = model_name
        self.client.model = model_name

    def set_api_base(self, api_base: str):
        self.config["api_base"] = api_base
        self.client.api_base = api_base.rstrip("/")
        self.client._init_client()

    def step(self, user_input: str):
        """Execute autonomous ReAct loop for the user request."""
        self.messages.append({"role": "user", "content": user_input})

        current_step = 0
        while current_step < self.max_steps:
            current_step += 1
            console.print(
                f"\n[bold magenta]⚡ Step {current_step} / {self.max_steps}[/bold magenta]"
            )

            try:
                response = self.client.chat_completion(self.messages)
            except Exception as e:
                console.print(
                    Panel(
                        f"[bold red]LLM Generation Error:[/bold red] {str(e)}",
                        border_style="red",
                    )
                )
                break

            content = response.get("content", "")
            tool_calls = response.get("tool_calls", [])

            # Print assistant thoughts / text if present
            if content and content.strip():
                clean_content = content
                # Remove raw tool blocks if they leaked into content
                clean_content = clean_content.replace("```tool_call", "").replace(
                    "```json", ""
                )
                console.print(
                    Panel(
                        clean_content.strip(),
                        title="[bold cyan]🧠 SaadGravity[/bold cyan]",
                        border_style="cyan",
                    )
                )

            # If no tools requested, we are done
            if not tool_calls:
                # Add assistant response to history
                self.messages.append({"role": "assistant", "content": content})
                console.print(
                    "[dim green]✓ Task finished or awaiting your input.[/dim green]"
                )
                break

            # Handle native or fallback tool calls
            assistant_msg = {"role": "assistant", "content": content}
            raw_msg = response.get("raw_message")
            if getattr(raw_msg, "tool_calls", None):
                assistant_msg["tool_calls"] = raw_msg.tool_calls
            self.messages.append(assistant_msg)

            for tc in tool_calls:
                call_id = tc.get("id", "call_0")
                tool_name = tc.get("name", "")
                tool_args = tc.get("arguments", {})

                # Render tool call box
                args_preview = json.dumps(tool_args, indent=2)
                console.print(
                    Panel(
                        Syntax(
                            args_preview, "json", theme="monokai", line_numbers=False
                        ),
                        title=f"[bold yellow]🛠️ Tool Invocation: {tool_name}[/bold yellow]",
                        border_style="yellow",
                    )
                )

                # Autonomous or confirmed execution
                if not self.auto_execute:
                    from rich.prompt import Confirm

                    proceed = Confirm.ask(
                        f"Execute [bold]{tool_name}[/bold]?", default=True
                    )
                    if not proceed:
                        result = "[Execution aborted by user]"
                        self.messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": call_id,
                                "name": tool_name,
                                "content": result,
                            }
                        )
                        continue

                # Execute tool
                tool_output = dispatch_tool(tool_name, tool_args)

                # Show preview of output
                output_preview = (
                    tool_output
                    if len(tool_output) <= 800
                    else tool_output[:800]
                    + f"\n... [truncated {len(tool_output)-800} chars]"
                )
                console.print(
                    Panel(
                        output_preview,
                        title=f"[dim green]📤 Result ({tool_name})[/dim green]",
                        border_style="green",
                    )
                )

                # Append tool result to history
                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call_id,
                        "name": tool_name,
                        "content": tool_output,
                    }
                )

        if current_step >= self.max_steps:
            console.print(
                "[bold red]⚠ Reached maximum autonomous step limit (25).[/bold red]"
            )
