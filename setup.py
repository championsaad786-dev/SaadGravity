from setuptools import setup, find_packages

setup(
    name="saadgravity",
    version="1.0.0",
    description="Autonomous Terminal AI Coding Agent & System Orchestrator (Antigravity CLI Style)",
    author="Saad (championsaad786-dev)",
    packages=find_packages(),
    install_requires=[
        "httpx>=0.24.0",
        "openai>=1.0.0",
        "rich>=13.0.0",
        "prompt_toolkit>=3.0.0",
        "pydantic>=2.0.0"
    ],
    entry_points={
        "console_scripts": [
            "saadgravity = saadgravity.cli:main",
        ],
    },
    python_requires=">=3.8",
)
