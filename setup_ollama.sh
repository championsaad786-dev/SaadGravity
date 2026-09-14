#!/usr/bin/env bash
# ==============================================================================
#  SaadGravity - Local LLM & Ollama Setup Helper
# ==============================================================================

set -e

echo -e "\033[1;36m"
echo "  ███████╗ █████╗  █████╗ ██████╗  ██████╗ ██████╗  █████╗ ██╗   ██╗██╗████████╗██╗   ██╗"
echo "  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔══██╗██╔══██╗██║   ██║██║╚══██╔══╝╚██╗ ██╔╝"
echo "  ███████╗███████║███████║██║  ██║██║  ███╗██████╔╝███████║██║   ██║██║   ██║    ╚████╔╝ "
echo "  ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██╔══██╗██╔══██║╚██╗ ██╔╝██║   ██║     ╚██╔╝  "
echo "  ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║   ██║      ██║   "
echo "  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝   ╚═╝      ╚═╝   "
echo -e "\033[0m"
echo -e "\033[1;33m[+] Checking for Ollama installation...\033[0m"

if ! command -v ollama &> /dev/null; then
    echo -e "\033[1;33m[!] Ollama not found. Installing Ollama...\033[0m"
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo -e "\033[1;32m[✓] Ollama is already installed!\033[0m"
fi

# Ensure service is active or run in background
if ! pgrep -x "ollama" > /dev/null; then
    echo -e "\033[1;33m[!] Starting Ollama service in background...\033[0m"
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
fi

echo -e "\033[1;32m[✓] Ollama is running at http://localhost:11434\033[0m"

echo ""
echo -e "\033[1;36mSelect which model to pull for SaadGravity (Optimized for 4GB RAM CPU):\033[0m"
echo "1) qwen2.5-coder:1.5b  (Recommended: Fast & Excellent Coding)"
echo "2) llama3.2:1b         (Ultra-lightweight & responsive)"
echo "3) dolphin-phi         (Uncensored 2.7B reasoning model)"
echo "4) deepseek-coder:1.3b (Coding specialist)"
echo "5) Custom Model Name"
echo "6) Skip (Configure external remote endpoint like OpenRouter / vLLM)"
echo ""
read -p "Enter choice [1-6] (Default 1): " choice
choice=${choice:-1}

case $choice in
    1)
        MODEL="qwen2.5-coder:1.5b"
        ;;
    2)
        MODEL="llama3.2:1b"
        ;;
    3)
        MODEL="dolphin-phi"
        ;;
    4)
        MODEL="deepseek-coder:1.3b"
        ;;
    5)
        read -p "Enter model name (e.g. dolphin-llama3, mistral, etc.): " MODEL
        ;;
    6)
        echo -e "\033[1;32m[✓] Skipping model download. You can connect SaadGravity to any API endpoint using:\033[0m"
        echo "    saadgravity -b https://openrouter.ai/api/v1 -k YOUR_KEY -m MODEL_NAME"
        exit 0
        ;;
    *)
        MODEL="qwen2.5-coder:1.5b"
        ;;
esac

echo -e "\033[1;33m[+] Pulling $MODEL via Ollama (this may take a few moments depending on speed)...\033[0m"
ollama pull "$MODEL"

echo -e "\033[1;32m[✓] Successfully pulled $MODEL!\033[0m"

# Update config
python3 -c "
from saadgravity.config import update_config_key
update_config_key('model', '$MODEL')
update_config_key('api_base', 'http://localhost:11434/v1')
update_config_key('api_key', 'ollama')
print('Configuration updated!')
"

echo ""
echo -e "\033[1;32m[🎉] All done! You can now launch your autonomous agent by running:\033[0m"
echo -e "    \033[1;37msaadgravity\033[0m"
