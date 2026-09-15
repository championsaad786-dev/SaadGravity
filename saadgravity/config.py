import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".saadgravity"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "api_base": "http://localhost:11434/v1",
    "api_key": "ollama",
    "model": "qwen2.5-coder:1.5b",
    "temperature": 0.2,
    "max_tokens": 4096,
    "auto_execute": True,
    "theme": "dark",
}


def load_config() -> dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            cfg = DEFAULT_CONFIG.copy()
            cfg.update(data)
            return cfg
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(cfg: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


def update_config_key(key: str, value):
    cfg = load_config()
    cfg[key] = value
    save_config(cfg)
    return cfg
