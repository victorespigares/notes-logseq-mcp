# Prompt Examples

Once the MCP server is configured, you can use these prompts in your MCP client (Windsurf, Claude Desktop, Cursor, etc.) to interact with your notes and Logseq notes.

## Basic Search

### Search in notes
```
Search notes for all notes that mention "The Leap"
```

### Search and show content
```
Search for notes about "machine learning" in notes and show me the content of the 3 most relevant ones
```

## Smart Logseq Features

### Template-Based Page Creation
```
List my Logseq templates, then create a smart page called "Project Alpha" 
using the "project" template with content about the new AI initiative
```

**Internal flow:**
1. `list_logseq_templates()`
2. `create_smart_logseq_page(title="Project Alpha", content=..., template_name="project")`

### Context-Aware Page Updates
```
Get the context of my "Resources" page, then add these new learning 
resources while preserving the existing structure
```

**Internal flow:**
1. `get_logseq_page_context(title="Resources")`
2. `create_smart_logseq_page(title="Resources", content=..., preserve_structure=true)`

### Automatic Outline Formatting
```
Create a smart Logseq page called "Meeting Notes" with this summary: 
"Discussed Q1 roadmap. Key decisions made. Action items assigned."
```

**Result:** Content automatically formatted as Logseq bullets with proper hierarchy.

## Complete Workflows

### 1. Search → Summarize → Create Smart Logseq Page
```
Search notes for everything about the book "The Leap", 
summarize the information found and create a smart Logseq page called 
"Summary - The Leap" with the summarized content.
```

**Internal flow:**
1. `search_notes(query="The Leap")`
2. For each result: `get_note_content(path=...)`
3. `summarize_content(content=..., model_provider="local")`
4. `create_smart_logseq_page(title="Summary - The Leap", content=...)`

### 2. Extract Specific Information with Template
```
Search notes for notes about "productivity" and extract all techniques 
or methods mentioned. Then create a smart Logseq page called 
"Productivity Techniques" using the "resource" template with the organized information.
```

**Internal flow:**
1. `search_notes(query="productivity")`
2. `get_note_content(path=...)` for each result
3. `extract_information(content=..., query="productivity techniques and methods")`
4. `create_smart_logseq_page(title="Productivity Techniques", content=..., template_name="resource")`

### 3. Consolidate Recent Notes with Structure Preservation
```
List my 10 most recent Notes, briefly summarize each one 
and add to my existing "Weekly Review" page while preserving its structure.
```

**Internal flow:**
1. `list_recent_notes(limit=10)`
2. For each note: `get_note_content(path=...)`
3. `summarize_content(content=..., model_provider="local")`
4. `get_logseq_page_context(title="Weekly Review")`
5. `create_smart_logseq_page(title="Weekly Review", content=..., preserve_structure=true)`

### 4. Research with Remote Model and Template
```
Search notes for information about "artificial intelligence", 
use Remote API to do a deep analysis of the content 
and create a smart Logseq page using the "analysis" template with insights and connections.
```

**Internal flow:**
1. `search_notes(query="artificial intelligence")`
2. `get_note_content(path=...)` for relevant results
3. `summarize_content(content=..., model_provider="remote")`
4. `create_smart_logseq_page(title="AI Analysis", content=..., template_name="analysis")`

### 5. Template-Based Meeting Notes
```
List templates, then create a meeting page for "Team Sync 2026-01-19" 
using the meeting template with today's discussion points.
```

**Internal flow:**
1. `list_logseq_templates()`
2. `create_smart_logseq_page(title="Team Sync 2026-01-19", content=..., template_name="meeting")`

## Specific Commands

### Search with filters
```
Search notes for "python" (case sensitive) and limit to 5 results
```

### List available templates
```
List all my Logseq templates
```

### Get page context
```
Show me the structure and properties of my "Projects" page
```

### Create smart page with template
```
Create a smart Logseq page called "Q1 Goals" using the "planning" template
```

### Update page preserving structure
```
Add these new ideas to my "Ideas" page while keeping the existing format
```

### Use specific model
```
Summarize this content using local Ollama: [content]
```

```
Summarize this content using Remote API: [content]
```

## Advanced Workflows

### Comparative Analysis with Template
```
Search for notes about "React" and "Vue" in notes, compare the advantages 
and disadvantages mentioned in my notes and create a smart Logseq page 
using the "comparison" template with a comparison table.
```

### Context-Aware Index Generation
```
Get the context of my "Project Index" page, then search all notes 
that contain "project", extract titles and dates, and update the index 
while preserving the existing structure and properties.
```

### Thematic Consolidation with Structure Preservation
```
Search notes for all references to "books read", 
extract titles, authors and my comments, and update my 
"Personal Library" page while maintaining its existing categories and format.
```

### Smart Content Migration
```
1. Get context of my existing "Learning Resources" page
2. Search notes for "machine learning courses"
3. Extract course names and links
4. Add to "Learning Resources" preserving the existing section structure
```

## Usage Tips

1. **Be specific**: The more specific your query, the better results you'll get.

2. **Chain operations**: You can request multiple operations in a single prompt.

3. **Choose the appropriate model**:
   - Use `local` (Ollama) for fast tasks and offline work
   - Use `remote` for deeper analysis using online LLMs (need API key configured in config.json)

4. **Use smart Logseq tools**: Always prefer `create_smart_logseq_page` over basic `create_logseq_page` for:
   - Automatic outline formatting
   - Template usage
   - Structure preservation
   - Property maintenance

5. **Leverage templates**: Create templates for common page types (projects, meetings, reviews) and use them consistently.

6. **Check context before updates**: Use `get_logseq_page_context` to understand existing page structure before making major updates.

7. **Preserve structure by default**: The smart tools automatically preserve existing formatting, properties, and sections.

8. **Let AI format content**: Provide plain text and let the system format it as proper Logseq outlines.

## Path Configuration

Make sure the paths in `config.json` point to your correct directories:

```json
{
  "notes_path": "~/Notes",
  "logseq_path": "~/Documents/Logseq"
}
```

## Troubleshooting

If a command fails:
1. Verify that the paths in `config.json` are correct
2. Make sure Ollama is running if using local model
3. Verify your Remote API (Anthropic, OpenAI, Remote API) key if using that model
4. Check the MCP server logs for more details
