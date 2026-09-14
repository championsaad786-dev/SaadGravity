import sys
import os
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style

from .agent import AutonomousAgent
from .config import load_config, save_config, update_config_key, CONFIG_DIR

console = Console()

BANNER = r"""[bold cyan]
   ███████╗ █████╗  █████╗ ██████╗  ██████╗ ██████╗  █████╗ ██╗   ██╗██╗████████╗██╗   ██╗
   ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔══██╗██╔══██╗██║   ██║██║╚══██╔══╝╚██╗ ██╔╝
   ███████╗███████║███████║██║  ██║██║  ███╗██████╔╝███████║██║   ██║██║   ██║    ╚████╔╝ 
   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██╔══██╗██╔══██║╚██╗ ██╔╝██║   ██║     ╚██╔╝  
   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║   ██║      ██║   
   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝   ╚═╝      ╚═╝   
[/bold cyan]
[bold white]        ⚡ Autonomous Terminal AI Coding Agent & System Orchestrator ⚡[/bold white]
[dim cyan]       Built for Uncensored Local & Remote LLMs | Full Bash & Code Automation[/dim cyan]
"""

def print_banner(cfg: dict):
    console.print(BANNER)
    
    status_table = Table(box=box.ROUNDED, expand=True)
    status_table.add_column("⚡ Agent Status", style="bold green")
    status_table.add_column("🧠 Model", style="bold yellow")
    status_table.add_column("🌐 Backend Endpoint", style="bold cyan")
    status_table.add_column("🤖 Autonomous Mode", style="bold magenta")

    auto_str = "ON (Auto-execute)" if cfg.get("auto_execute", True) else "OFF (Ask confirmation)"
    status_table.add_row("ONLINE", cfg.get("model", "N/A"), cfg.get("api_base", "N/A"), auto_str)
    console.print(status_table)
    console.print("[dim]Type [bold white]/help[/bold white] for commands, [bold white]/model <name>[/bold white] to change model, [bold white]/exit[/bold white] to quit.\n[/dim]")

def print_help():
    table = Table(title="[bold cyan]SaadGravity Command Reference[/bold cyan]", box=box.ROUNDED)
    table.add_column("Command", style="bold yellow", width=25)
    table.add_column("Description", style="white")

    table.add_row("/model <name>", "Switch current LLM model (e.g. /model qwen2.5-coder:1.5b)")
    table.add_row("/backend <url>", "Change API endpoint (e.g. /backend http://localhost:11434/v1)")
    table.add_row("/key <apikey>", "Set custom API key for remote providers (OpenRouter, Groq, etc.)")
    table.add_row("/auto <on|off>", "Toggle autonomous tool execution without confirmation")
    table.add_row("/status", "Check backend connection and available models")
    table.add_row("/clear", "Clear conversation memory and start fresh")
    table.add_row("/tools", "List built-in autonomous agent tools")
    table.add_row("/exit or /quit", "Exit SaadGravity")
    console.print(table)

def print_tools():
    table = Table(title="[bold cyan]Built-in Autonomous Tools[/bold cyan]", box=box.ROUNDED)
    table.add_column("Tool", style="bold green", width=22)
    table.add_column("Capability", style="white")

    table.add_row("run_command", "Execute bash shell commands in Kali Linux with live outputs")
    table.add_row("view_file", "Inspect file contents with line numbering & range support")
    table.add_row("write_file", "Create new code files or overwrite existing files")
    table.add_row("replace_file_content", "Perform surgical search-and-replace on codebase")
    table.add_row("list_dir", "Browse folders and project directory hierarchies")
    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="SaadGravity - Autonomous Terminal AI Coding Agent")
    parser.add_argument("prompt", nargs="*", help="Optional initial instruction to run directly")
    parser.add_argument("-m", "--model", help="Specify model name to use")
    parser.add_argument("-b", "--backend", help="Specify API Base URL (e.g. http://localhost:11434/v1)")
    parser.add_argument("-k", "--key", help="Specify API Key")
    parser.add_argument("--confirm", action="store_true", help="Ask confirmation before executing every tool")
    args = parser.parse_args()

    cfg = load_config()
    if args.model:
        cfg["model"] = args.model
    if args.backend:
        cfg["api_base"] = args.backend
    if args.key:
        cfg["api_key"] = args.key
    if args.confirm:
        cfg["auto_execute"] = False
    save_config(cfg)

    agent = AutonomousAgent(cfg)

    # If single-shot prompt passed via CLI
    if args.prompt:
        user_prompt = " ".join(args.prompt)
        print_banner(cfg)
        console.print(f"[bold cyan]Input:[/bold cyan] {user_prompt}\n")
        agent.step(user_prompt)
        sys.exit(0)

    # Interactive TUI mode
    print_banner(cfg)

    history_file = CONFIG_DIR / "history.txt"
    session = PromptSession(history=FileHistory(str(history_file)))

    pt_style = Style.from_dict({
        'prompt': '#00ffff bold',
    })

    while True:
        try:
            user_input = session.prompt(
                [('class:prompt', 'SaadGravity ❯ ')],
                style=pt_style,
                auto_suggest=AutoSuggestFromHistory()
            ).strip()

            if not user_input:
                continue

            # Handle Slash Commands
            if user_input.startswith("/"):
                parts = user_input.split(maxsplit=1)
                cmd = parts[0].lower()
                arg = parts[1].strip() if len(parts) > 1 else ""

                if cmd in ["/exit", "/quit"]:
                    console.print("[bold red]Exiting SaadGravity. Happy coding! 🚀[/bold red]")
                    break
                elif cmd == "/help":
                    print_help()
                elif cmd == "/tools":
                    print_tools()
                elif cmd == "/clear":
                    agent.reset_conversation()
                    console.print("[bold green]✓ Conversation context cleared.[/bold green]")
                elif cmd == "/status":
                    ok, msg = agent.client.check_connection()
                    style = "green" if ok else "red"
                    console.print(f"[{style}]{msg}[/{style}]")
                elif cmd == "/model":
                    if not arg:
                        console.print(f"[yellow]Current model:[/yellow] {cfg.get('model')}")
                    else:
                        cfg = update_config_key("model", arg)
                        agent.set_model(arg)
                        console.print(f"[bold green]✓ Model switched to:[/bold green] {arg}")
                elif cmd == "/backend":
                    if not arg:
                        console.print(f"[yellow]Current backend:[/yellow] {cfg.get('api_base')}")
                    else:
                        cfg = update_config_key("api_base", arg)
                        agent.set_api_base(arg)
                        console.print(f"[bold green]✓ Backend updated to:[/bold green] {arg}")
                elif cmd == "/key":
                    cfg = update_config_key("api_key", arg)
                    agent.client.api_key = arg
                    agent.client._init_client()
                    console.print("[bold green]✓ API Key updated.[/bold green]")
                elif cmd == "/auto":
                    val = arg.lower() in ["on", "true", "1", "yes"]
                    cfg = update_config_key("auto_execute", val)
                    agent.auto_execute = val
                    state = "ENABLED (Auto-execute)" if val else "DISABLED (Manual confirm)"
                    console.print(f"[bold green]✓ Autonomous execution {state}[/bold green]")
                else:
                    console.print(f"[red]Unknown command:[/red] {cmd}. Type /help for options.")
                continue

            # Process User Request through Autonomous ReAct loop
            agent.step(user_input)

        except KeyboardInterrupt:
            console.print("\n[yellow]Use /exit to quit.[/yellow]")
        except EOFError:
            break
        except Exception as e:
            console.print(f"[bold red]Unexpected Error:[/bold red] {str(e)}")

if __name__ == "__main__":
    main()
