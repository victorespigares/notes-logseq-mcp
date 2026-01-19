from setuptools import setup, find_packages

setup(
    name="notes-logseq-mcp",
    version="0.1.0",
    description="MCP Server for Notes and Logseq integration",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "mcp>=1.0.0",
        "aiohttp",
        "pydantic",
        "python-dotenv",
        "ollama",
        "openai",
    ],
    entry_points={
        "console_scripts": [
            "notes-logseq-mcp=server:main",
        ],
    },
)
