#!/usr/bin/env python3
import asyncio
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .utils.config import Config
from .tools.notes_tools import NotesTools
from .tools.logseq_tools import LogseqTools
from .models.ollama_client import OllamaClient
from .models.remote_client import RemoteClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotesLogseqServer:
    def __init__(self, config_path: str = "config.json"):
        self.config = Config(config_path)
        self.notes = NotesTools(self.config.get_notes_path())
        self.logseq = LogseqTools(self.config.get_logseq_path())
        
        self.ollama_client = None
        self.remote_client = None
        
        self._init_model_clients()
        
        self.server = Server("notes-logseq-mcp")
        self._register_handlers()
    
    def _init_model_clients(self):
        try:
            ollama_config = self.config.get_model_config('local')
            self.ollama_client = OllamaClient(
                base_url=ollama_config['base_url'],
                model=ollama_config['model']
            )
            logger.info("Ollama client initialized")
        except Exception as e:
            logger.warning(f"Could not initialize Ollama client: {e}")
        
        try:
            remote_config = self.config.get_model_config('remote')
            if remote_config['api_key'] != 'YOUR_API_KEY':
                self.remote_client = RemoteClient(
                    api_key=remote_config['api_key'],
                    model=remote_config['model']
                )
                logger.info("Remote client initialized")
        except Exception as e:
            logger.warning(f"Could not initialize Remote client: {e}")
    
    def _register_handlers(self):
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="search_notes",
                    description="Search for text in markdown notes. Returns matching files with context.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query to find in notes"
                            },
                            "case_sensitive": {
                                "type": "boolean",
                                "description": "Whether search should be case sensitive",
                                "default": False
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 20
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="get_note_content",
                    description="Get the full content of a specific note file by its relative path.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path to the note file (e.g., 'folder/note.md')"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="list_recent_notes",
                    description="List the most recently modified notes in notes.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {
                                "type": "integer",
                                "description": "Number of recent notes to return",
                                "default": 10
                            }
                        }
                    }
                ),
                Tool(
                    name="create_logseq_page",
                    description="Create or update a page in Logseq with the given title and content.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Title of the Logseq page"
                            },
                            "content": {
                                "type": "string",
                                "description": "Markdown content for the page"
                            },
                            "overwrite": {
                                "type": "boolean",
                                "description": "Whether to overwrite existing content (default: append)",
                                "default": False
                            }
                        },
                        "required": ["title", "content"]
                    }
                ),
                Tool(
                    name="create_logseq_journal",
                    description="Create or append to a journal entry in Logseq.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Content to add to the journal"
                            },
                            "date": {
                                "type": "string",
                                "description": "Date in YYYY_MM_DD format (default: today)"
                            }
                        },
                        "required": ["content"]
                    }
                ),
                Tool(
                    name="summarize_content",
                    description="Summarize text content using a local or remote AI model.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Content to summarize"
                            },
                            "model_provider": {
                                "type": "string",
                                "description": "Model provider to use: 'local' (Ollama) or 'remote'",
                                "enum": ["local", "remote"],
                                "default": "local"
                            },
                            "max_length": {
                                "type": "integer",
                                "description": "Maximum length of summary in words"
                            }
                        },
                        "required": ["content"]
                    }
                ),
                Tool(
                    name="extract_information",
                    description="Extract specific information from content using AI.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "Content to extract information from"
                            },
                            "query": {
                                "type": "string",
                                "description": "What information to extract"
                            },
                            "model_provider": {
                                "type": "string",
                                "description": "Model provider to use: 'local' (Ollama) or 'remote'",
                                "enum": ["local", "remote"],
                                "default": "local"
                            }
                        },
                        "required": ["content", "query"]
                    }
                ),
                Tool(
                    name="get_logseq_page_context",
                    description="Get context about an existing Logseq page including its structure, properties, and content. Use this before updating a page to understand its current format.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Title of the Logseq page to analyze"
                            }
                        },
                        "required": ["title"]
                    }
                ),
                Tool(
                    name="list_logseq_templates",
                    description="List all available templates in Logseq. Use this to find appropriate templates for new pages.",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="create_smart_logseq_page",
                    description="Intelligently create or update a Logseq page. Automatically formats content as outline, uses templates for new pages, and preserves structure when updating existing pages. This is the recommended way to create Logseq pages.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Title of the Logseq page"
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to add (will be automatically formatted as Logseq outline)"
                            },
                            "template_name": {
                                "type": "string",
                                "description": "Optional template name to use for new pages (e.g., 'project', 'meeting')"
                            },
                            "preserve_structure": {
                                "type": "boolean",
                                "description": "If updating existing page, preserve its structure and properties",
                                "default": True
                            },
                            "overwrite": {
                                "type": "boolean",
                                "description": "If True, replace entire page content",
                                "default": False
                            }
                        },
                        "required": ["title", "content"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            try:
                if name == "search_notes":
                    results = self.notes.search_notes(
                        query=arguments["query"],
                        case_sensitive=arguments.get("case_sensitive", False),
                        max_results=arguments.get("max_results", 20)
                    )
                    return [TextContent(type="text", text=str(results))]
                
                elif name == "get_note_content":
                    result = self.notes.get_note_content(arguments["path"])
                    return [TextContent(type="text", text=result["content"])]
                
                elif name == "list_recent_notes":
                    results = self.notes.list_recent_notes(
                        limit=arguments.get("limit", 10)
                    )
                    return [TextContent(type="text", text=str(results))]
                
                elif name == "create_logseq_page":
                    result = self.logseq.create_page(
                        title=arguments["title"],
                        content=arguments["content"],
                        overwrite=arguments.get("overwrite", False)
                    )
                    return [TextContent(type="text", text=f"Page created: {result['path']}")]
                
                elif name == "create_logseq_journal":
                    result = self.logseq.create_journal_entry(
                        content=arguments["content"],
                        date=arguments.get("date")
                    )
                    return [TextContent(type="text", text=f"Journal entry created: {result['path']}")]
                
                elif name == "summarize_content":
                    provider = arguments.get("model_provider", "local")
                    client = self._get_model_client(provider)
                    
                    summary = await client.summarize(
                        content=arguments["content"],
                        max_length=arguments.get("max_length")
                    )
                    return [TextContent(type="text", text=summary)]
                
                elif name == "extract_information":
                    provider = arguments.get("model_provider", "local")
                    client = self._get_model_client(provider)
                    
                    info = await client.extract_info(
                        content=arguments["content"],
                        query=arguments["query"]
                    )
                    return [TextContent(type="text", text=info)]
                
                elif name == "get_logseq_page_context":
                    context = self.logseq.get_page_context(arguments["title"])
                    if context is None:
                        return [TextContent(type="text", text=f"Page '{arguments['title']}' does not exist.")]
                    
                    import json
                    return [TextContent(type="text", text=json.dumps(context, indent=2))]
                
                elif name == "list_logseq_templates":
                    templates = self.logseq.list_available_templates()
                    if not templates:
                        return [TextContent(type="text", text="No templates found in Logseq.")]
                    
                    template_list = "\n".join([f"- {t}" for t in templates])
                    return [TextContent(type="text", text=f"Available templates:\n{template_list}")]
                
                elif name == "create_smart_logseq_page":
                    result = self.logseq.create_page_with_context(
                        title=arguments["title"],
                        content=arguments["content"],
                        template_name=arguments.get("template_name"),
                        preserve_structure=arguments.get("preserve_structure", True),
                        overwrite=arguments.get("overwrite", False)
                    )
                    
                    status = "updated" if result["was_existing"] else "created"
                    template_info = f" using template '{result['used_template']}'" if result.get("used_template") else ""
                    return [TextContent(type="text", text=f"Page {status}: {result['path']}{template_info}")]
                
                else:
                    raise ValueError(f"Unknown tool: {name}")
            
            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    def _get_model_client(self, provider: str):
        if provider == "local":
            if not self.ollama_client:
                raise ValueError("Ollama client not initialized. Check your config.")
            return self.ollama_client
        elif provider == "remote":
            if not self.remote_client:
                raise ValueError("Remote client not initialized. Check your API key in config.")
            return self.remote_client
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    async def run(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    
    server = NotesLogseqServer(config_path)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
