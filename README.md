# Notes-Logseq MCP Server

MCP server to integrate markdown notes and Logseq with Windsurf IDE using AI.

[![GitHub](https://img.shields.io/badge/GitHub-victorespigares%2Fnotes--logseq--mcp-blue?logo=github)](https://github.com/victorespigares/notes-logseq-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Features

- 🔍 **Search notes** by content with context
- 📝 **Smart Logseq integration** - understands page structure, templates, and properties
- 🤖 **AI processing** with local (Ollama) or remote models (Anthropic, OpenAI, Perplexity)
- 📊 **Summarize** and extract information from notes
- 🎯 **Context-aware** - preserves existing page structure when updating
- 📋 **Template support** - automatically uses templates for new pages

## Installation

### From GitHub

```bash
# Clone the repository
git clone https://github.com/victorespigares/notes-logseq-mcp.git
cd notes-logseq-mcp

# Create virtual environment (Python 3.10+ required)
python3 -m venv venv

# 2. Install dependencies
venv/bin/pip install -r requirements.txt

# 3. Configure
cp config.example.json config.json
# Edit config.json with your paths

# 4. Test
venv/bin/python -m src.server config.json
```

## Configuration

### config.json

```json
{
  "notes_path": "~/Notes",
  "logseq_path": "~/Documents/Logseq",
  "models": {
    "default_provider": "local",
    "ollama": {
      "base_url": "http://localhost:11434",
      "model": "llama3.1"
    },
    "remote": {
      "api_key": "YOUR_API_KEY",
      "model": "claude-3.5-sonnet",
      "provider": "anthropic|openai|perplexity"
    }
  }
}
```

**Find your notes path:**
- FSNotes (macOS): `~/Library/Containers/co.fluder.FSNotes/Data/Library/Application Support/FSNotes`
- nvAlt: `~/Library/Application Support/Notational Data`
- Or any folder with markdown or txt files

**Logseq path:**
- Default: `~/Documents/Logseq` or `~/Logseq`

### Windsurf Integration

Edit `~/Library/Application Support/Windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "notes-logseq": {
      "command": "/ABSOLUTE/PATH/TO/notes-logseq-mcp/venv/bin/python",
      "args": [
        "-m",
        "src.server",
        "/ABSOLUTE/PATH/TO/notes-logseq-mcp/config.json"
      ],
      "env": {
        "PYTHONPATH": "/ABSOLUTE/PATH/TO/notes-logseq-mcp"
      }
    }
  }
}
```

**Important:**
- Use **absolute paths** (replace `/ABSOLUTE/PATH/TO/`)
- Use **venv Python** (`venv/bin/python`), not system Python
- Restart Windsurf after config changes

## Available Tools

### Notes Tools
| Tool | Description |
|------|-------------|
| `search_notes` | Search text in notes with context |
| `get_note_content` | Get full content of a note |
| `list_recent_notes` | List most recent notes |

### Smart Logseq Tools
| Tool | Description |
|------|-------------|
| `create_smart_logseq_page` | **Recommended** - Intelligently create/update pages with auto-formatting, template support, and structure preservation |
| `get_logseq_page_context` | Analyze existing page structure, properties, and format |
| `list_logseq_templates` | List available templates in Logseq |
| `create_logseq_page` | Basic page creation (legacy) |
| `create_logseq_journal` | Create journal entry |

### AI Tools
| Tool | Description |
|------|-------------|
| `summarize_content` | AI summary (local/remote) |
| `extract_information` | Extract specific info with AI |

## Usage Examples

### Basic Search and Create
```
Search notes for "machine learning" and create a summary in Logseq
```

### Smart Page Creation with Template
```
Search for "project alpha" in notes, then create a smart Logseq page 
using the "project" template with the findings
```

### Context-Aware Updates
```
Get the context of my "Weekly Review" page, then add this week's 
summary preserving the existing structure
```

### Template Discovery
```
List available Logseq templates, then create a new meeting page 
using the appropriate template
```

### Advanced Workflow
```
Search for "productivity" in notes, extract all techniques, 
then create a smart Logseq page that follows my existing 
"Resources" page structure
```

## Troubleshooting

**Server timeout:**
- Use `venv/bin/python` in mcp_config.json
- Test manually: `venv/bin/python -m src.server config.json`

**ModuleNotFoundError:**
- Install dependencies: `venv/bin/pip install -r requirements.txt`
- Use Python 3.10+

**Notes not found:**
- Verify `notes_path` in config.json
- Check folder permissions

**Ollama not responding:**
- Start Ollama: `ollama serve`
- Check port 11434

## Tests

```bash
venv/bin/python -m pytest tests/ -v
```

## Documentation

- [Smart Logseq Features Guide](SMART_LOGSEQ.md) - Detailed guide on intelligent Logseq integration
- [Prompt Examples](examples/prompts.md) - Ready-to-use prompts for Windsurf

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Repository

**GitHub:** [victorespigares/notes-logseq-mcp](https://github.com/victorespigares/notes-logseq-mcp)

## License

MIT License - see [LICENSE](LICENSE) file for details
