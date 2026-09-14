# ⚡ SaadGravity

<div align="center">

```
   ███████╗ █████╗  █████╗ ██████╗  ██████╗ ██████╗  █████╗ ██╗   ██╗██╗████████╗██╗   ██╗
   ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔══██╗██╔══██╗██║   ██║██║╚══██╔══╝╚██╗ ██╔╝
   ███████╗███████║███████║██║  ██║██║  ███╗██████╔╝███████║██║   ██║██║   ██║    ╚████╔╝ 
   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██╔══██╗██╔══██║╚██╗ ██╔╝██║   ██║     ╚██╔╝  
   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║   ██║      ██║   
   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝   ╚═╝      ╚═╝   
```

### 🤖 Autonomous Terminal AI Coding Agent & System Orchestrator 🤖
#### *The Open-Source Antigravity CLI for Local & Uncensored LLMs*

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Kali Linux](https://img.shields.io/badge/Kali-Linux-557C94?style=for-the-badge&logo=kalilinux)](https://kali.org)
[![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=for-the-badge&logo=ollama)](https://ollama.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**SaadGravity** brings the full autonomous power of Google's **Gemini Antigravity IDE / Claude Code / Aider** straight to your Kali Linux terminal — with zero censorship restrictions and full support for **local models** (Ollama, LM Studio, vLLM) or remote providers (OpenRouter, DeepSeek, Groq).

[Features](#-features) • [Quickstart](#-quickstart) • [Autonomous-Tools](#-built-in-tools) • [Slash-Commands](#-slash-commands)

</div>

---

## 🚀 Why SaadGravity?

Traditional AI CLI tools are either locked behind heavy cloud subscriptions or restricted by strict guardrails. **SaadGravity** gives you **complete autonomous control**:

- 🛠️ **Autonomous ReAct Engine:** Multi-step autonomous agent loop that executes commands, views files, patches code, tests for errors, and self-corrects until the mission is accomplished.
- 🔓 **Uncensored & Local Model Ready:** Directly interfaces with Ollama, LM Studio, LocalAI, vLLM, or OpenRouter. Run Dolphin, Hermes, Qwen, Mistral, Llama, or custom fine-tunes without restrictions.
- 🎨 **Antigravity-Inspired Terminal TUI:** Real-time reasoning streams, tool execution boxes, syntax-highlighted code diffs, and interactive command prompts powered by `rich` and `prompt_toolkit`.
- ⚡ **Lightweight & Fast:** Engineered to run smoothly even on resource-constrained systems (4GB RAM) with optimized 1B–3B coding models.

---

## 🛠️ Built-in Autonomous Tools

The agent comes pre-equipped with an execution sandbox directly inside your terminal:

| Tool | Capability |
|------|------------|
| 💻 `run_command` | Executes any bash shell command with live stdout/stderr capture |
| 👁️ `view_file` | Reads file contents with line numbering and line range slicing |
| ✍️ `write_file` | Creates new code files or overwrites existing ones |
| 🔧 `replace_file_content` | Performs precise search-and-replace edits on project files |
| 📁 `list_dir` | Explores directories and project hierarchies |

---

## 📦 Quickstart

### 1. Installation
```bash
git clone https://github.com/championsaad786-dev/SaadGravity.git
cd SaadGravity
pip3 install -r requirements.txt
pip3 install -e .
```

### 2. Setup Local LLM (Ollama)
Run the automated setup helper to install Ollama and pull an optimized coding or uncensored model:
```bash
./setup_ollama.sh
```

### 3. Launch SaadGravity
Launch the interactive agent interface from anywhere:
```bash
saadgravity
```

Or pass a single autonomous instruction directly:
```bash
saadgravity "Scan the current directory, find all python scripts, and add docstrings to every function"
```

---

## 🌐 Connecting to Remote / External Endpoints

You can connect SaadGravity to any OpenAI-compatible API (e.g. OpenRouter, Groq, DeepSeek, or vLLM):

```bash
# Example: Using OpenRouter with an uncensored model
saadgravity -b https://openrouter.ai/api/v1 -k YOUR_OPENROUTER_KEY -m cognitivecomputations/dolphin-2.9.2-qwen2-72b

# Example: Using local LM Studio
saadgravity -b http://localhost:1234/v1 -m local-model
```

---

## ⚡ Slash Commands

Inside the interactive terminal prompt, you can use built-in control commands:

| Command | Action |
|---------|--------|
| `/model <name>` | Dynamically switch models on the fly |
| `/backend <url>` | Change the active API endpoint base URL |
| `/key <apikey>` | Set or update your provider API key |
| `/auto on\|off` | Toggle autonomous execution (auto-run tools vs. ask confirmation) |
| `/status` | Test API connection and inspect active model settings |
| `/clear` | Wipe conversation context and start fresh |
| `/tools` | Display full list of registered agent tools |
| `/help` | Show interactive command reference |
| `/exit` | Exit the CLI session |

---

## 👤 Author

**Saad** - Aspiring Developer 🚀 | Cybersecurity & AI Systems Enthusiast  
GitHub: [@championsaad786-dev](https://github.com/championsaad786-dev)

## 📄 License
MIT License - see [LICENSE](LICENSE) for details.
