import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional


def execute_run_command(command: str, cwd: Optional[str] = None) -> str:
    """Execute a bash shell command and return stdout/stderr."""
    work_dir = cwd if cwd and os.path.exists(cwd) else os.getcwd()
    try:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=work_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120,
        )
        out = proc.stdout
        err = proc.stderr
        exit_code = proc.returncode

        res = []
        if out:
            res.append(out)
        if err:
            res.append(f"[STDERR]\n{err}")
        if exit_code != 0:
            res.append(f"[Process exited with code {exit_code}]")

        output_str = "\n".join(res).strip()
        return output_str if output_str else "[Command completed with no output]"
    except subprocess.TimeoutExpired:
        return "[Error: Command execution timed out after 120 seconds]"
    except Exception as e:
        return f"[Error executing command: {str(e)}]"


def execute_view_file(
    path: str, start_line: int = 1, end_line: Optional[int] = None
) -> str:
    """View file contents with line numbers."""
    target = Path(path).expanduser().resolve()
    if not target.exists():
        return f"[Error: File not found at {path}]"
    if not target.is_file():
        return f"[Error: {path} is a directory, not a file]"

    try:
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        total_lines = len(lines)
        s_line = max(1, start_line)
        e_line = min(total_lines, end_line) if end_line else total_lines

        selected = lines[s_line - 1 : e_line]
        formatted = [
            f"{i:4d} | {line}" for i, line in enumerate(selected, start=s_line)
        ]
        return (
            f"[File: {target} ({s_line}-{e_line} of {total_lines} lines)]\n"
            + "".join(formatted)
        )
    except Exception as e:
        return f"[Error viewing file: {str(e)}]"


def execute_write_file(path: str, content: str) -> str:
    """Write or overwrite file contents."""
    target = Path(path).expanduser().resolve()
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return f"[Successfully wrote {len(content)} characters to {target}]"
    except Exception as e:
        return f"[Error writing file: {str(e)}]"


def execute_replace_file_content(
    path: str, target_content: str, replacement_content: str
) -> str:
    """Replace exact content block inside a file."""
    target = Path(path).expanduser().resolve()
    if not target.exists() or not target.is_file():
        return f"[Error: File not found at {path}]"

    try:
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()

        if target_content not in content:
            return f"[Error: Target content was not found in {path}]"

        new_content = content.replace(target_content, replacement_content, 1)
        with open(target, "w", encoding="utf-8") as f:
            f.write(new_content)
        return f"[Successfully updated {path}]"
    except Exception as e:
        return f"[Error updating file: {str(e)}]"


def execute_list_dir(path: str = ".") -> str:
    """List directory contents."""
    target = Path(path).expanduser().resolve()
    if not target.exists():
        return f"[Error: Directory not found at {path}]"
    if not target.is_dir():
        return f"[Error: {path} is not a directory]"

    try:
        entries = sorted(os.listdir(target))
        res = [f"Directory contents of {target}:"]
        for e in entries:
            full = target / e
            if full.is_dir():
                res.append(f"  📁 {e}/")
            else:
                sz = full.stat().st_size
                res.append(f"  📄 {e} ({sz} bytes)")
        return "\n".join(res)
    except Exception as e:
        return f"[Error listing directory: {str(e)}]"


# Tool schemas for native LLM function calling
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a bash shell command in the system terminal and inspect output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The exact shell command to execute.",
                    }
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "view_file",
            "description": "View file content with line numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to inspect.",
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "Line number to start reading from (1-indexed).",
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "Line number to end reading at.",
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create a new file or completely overwrite an existing file with content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the target file.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write into the file.",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "replace_file_content",
            "description": "Perform precise search and replace on a section of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file."},
                    "target_content": {
                        "type": "string",
                        "description": "The exact substring to replace.",
                    },
                    "replacement_content": {
                        "type": "string",
                        "description": "The new content to replace it with.",
                    },
                },
                "required": ["path", "target_content", "replacement_content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List files and folders in a specified directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path (default is current directory).",
                    }
                },
                "required": [],
            },
        },
    },
]


def dispatch_tool(name: str, args: Dict[str, Any]) -> str:
    """Dispatch a tool by name and arguments."""
    if name == "run_command":
        return execute_run_command(args.get("command", ""))
    elif name == "view_file":
        return execute_view_file(
            args.get("path", ""),
            start_line=int(args.get("start_line", 1)),
            end_line=int(args.get("end_line")) if args.get("end_line") else None,
        )
    elif name == "write_file":
        return execute_write_file(args.get("path", ""), args.get("content", ""))
    elif name == "replace_file_content":
        return execute_replace_file_content(
            args.get("path", ""),
            args.get("target_content", ""),
            args.get("replacement_content", ""),
        )
    elif name == "list_dir":
        return execute_list_dir(
            args.get("path", "." if not args else args.get("path", "."))
        )
    else:
        return f"[Error: Unknown tool {name}]"
