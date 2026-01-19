# Smart Logseq Integration Guide

This guide explains the intelligent Logseq features that go beyond simple copy-paste.

## Overview

The smart Logseq integration understands:
- **Page structure** - Analyzes existing pages to preserve their format
- **Templates** - Automatically applies templates for new pages
- **Properties** - Reads and preserves Logseq properties (key:: value)
- **Outline formatting** - Converts content to proper Logseq bullet format
- **Context awareness** - Knows when to append vs. create new sections

## Key Features

### 1. Automatic Outline Formatting

Instead of pasting raw text, content is automatically formatted as Logseq outlines:

**Input:**
```
This is a summary
Key point one
Key point two
```

**Output:**
```
- This is a summary
- Key point one
- Key point two
```

### 2. Template Detection and Usage

The system can find and use your Logseq templates:

```
List available Logseq templates
```

Then create pages using them:

```
Create a smart Logseq page called "Project Alpha" using the "project" template 
with content: "New AI initiative focusing on automation"
```

**Result:** Page created with all template properties, sections, and structure intact.

### 3. Structure Preservation

When updating existing pages, the system preserves:
- Existing properties (tags, dates, status, etc.)
- Section hierarchy
- Indentation style (tabs vs spaces)
- Existing formatting patterns

**Example:**

Existing page "Weekly Review" has:
```
status:: active
week:: 2026-W03

## Goals
- Complete project proposal

## Notes
- Met with team
```

When you add new content, it preserves this structure:
```
Add to my Weekly Review page: "Finished the design mockups"
```

**Result:**
```
status:: active
week:: 2026-W03

## Goals
- Complete project proposal

## Notes
- Met with team
- Finished the design mockups
```

### 4. Context Analysis

Before updating a page, you can analyze its structure:

```
Get the context of my "Resources" page
```

**Returns:**
- Properties found
- Section structure
- Outline hierarchy
- Formatting patterns (todos, tags, links)
- Indentation style

This helps the AI understand how to format new content appropriately.

## Practical Workflows

### Workflow 1: Smart Project Page Creation

```
1. List available Logseq templates
2. Search notes for "customer feedback Q1"
3. Summarize the findings
4. Create a smart Logseq page "Q1 Customer Insights" using the "analysis" 
   template with the summary
```

**What happens:**
- Finds your "analysis" template
- Uses its properties (type::, date::, status::)
- Follows its section structure
- Formats summary as proper outline
- Result: Professional, consistent page

### Workflow 2: Context-Aware Page Updates

```
1. Get the context of my "Learning Resources" page
2. Search notes for "machine learning courses"
3. Extract course names and links
4. Create a smart Logseq page "Learning Resources" with the new courses, 
   preserving structure
```

**What happens:**
- Analyzes existing page structure
- Sees it has sections like "## Courses", "## Books"
- Adds new content under appropriate section
- Maintains existing formatting style
- Preserves all properties

### Workflow 3: Template-Based Meeting Notes

```
1. List templates to find "meeting" template
2. Create a smart Logseq page "Team Sync 2026-01-19" using "meeting" template
3. Add content: "Discussed Q1 roadmap. Action items: Review designs by Friday"
```

**What happens:**
- Uses meeting template with properties (attendees::, date::, etc.)
- Formats action items as checkboxes if template uses them
- Follows template's section structure
- Result: Consistent meeting notes format

### Workflow 4: Intelligent Content Migration

```
1. Search notes for "productivity tips"
2. Get context of existing "Productivity" Logseq page
3. Extract all tips from notes
4. Create smart Logseq page "Productivity" with extracted tips, 
   preserving existing structure
```

**What happens:**
- Reads existing page to understand its organization
- Formats new tips to match existing style
- Appends without duplicating sections
- Maintains property metadata

## Advanced Features

### Property Preservation

The system automatically detects and preserves Logseq properties:

```
type:: resource
status:: active
tags:: [[AI]], [[Learning]]
```

When updating, these properties remain at the top of the page.

### Section-Aware Appending

If a page has sections (## Headers), new content is intelligently placed:
- Analyzes which section the content belongs to
- Appends to appropriate section
- Creates new section if needed

### Indentation Style Detection

Automatically matches your Logseq's indentation:
- Detects tabs vs. spaces
- Maintains consistent hierarchy
- Preserves nested bullet structure

### Template Structure

Templates can include:
- **Properties**: Metadata fields
- **Sections**: Organized headers
- **Placeholders**: Areas for content
- **Queries**: Logseq query blocks

All are preserved when using the template.

## Tool Reference

### `create_smart_logseq_page`

**Recommended for all page creation/updates**

Parameters:
- `title` (required): Page title
- `content` (required): Content to add
- `template_name` (optional): Template to use for new pages
- `preserve_structure` (default: true): Keep existing structure when updating
- `overwrite` (default: false): Replace entire page

### `get_logseq_page_context`

**Use before updating to understand page structure**

Parameters:
- `title` (required): Page to analyze

Returns:
- Properties found
- Outline structure
- Sections
- Formatting patterns
- Content preview

### `list_logseq_templates`

**Discover available templates**

No parameters required.

Returns list of all templates in your Logseq.

## Best Practices

### 1. Always Use Smart Tools for Logseq

❌ **Don't:** Use basic `create_logseq_page` for important content
✅ **Do:** Use `create_smart_logseq_page` for intelligent formatting

### 2. Check Context Before Major Updates

❌ **Don't:** Blindly append to pages
✅ **Do:** Use `get_logseq_page_context` first to understand structure

### 3. Leverage Templates

❌ **Don't:** Manually format every new page
✅ **Do:** Create templates for common page types (projects, meetings, reviews)

### 4. Let AI Format Content

❌ **Don't:** Pre-format content with bullets
✅ **Do:** Provide plain text and let the system format as Logseq outline

### 5. Use Preserve Structure

❌ **Don't:** Set `preserve_structure: false` unless you want to lose formatting
✅ **Do:** Keep default `preserve_structure: true` for updates

## Example Prompts

### Discovery
```
"List my Logseq templates"
"Show me the structure of my 'Weekly Review' page"
"What properties does my 'Projects' page have?"
```

### Creation
```
"Create a smart Logseq page 'Q1 Goals' using the 'planning' template"
"Search notes for 'book recommendations' and create a smart page with them"
"Make a new meeting page for today using the meeting template"
```

### Updates
```
"Add today's learnings to my 'Daily Notes' page, preserving structure"
"Update my 'Resources' page with new links, keeping the existing format"
"Append this summary to 'Project Alpha' without changing the properties"
```

### Analysis + Action
```
"Analyze my 'Reading List' page, then add these 3 books in the same format"
"Check the structure of 'Team OKRs', then add Q2 objectives matching the style"
"Get context of 'Ideas' page and add new ideas under the right category"
```

## Troubleshooting

**Template not found:**
- Run `list_logseq_templates` to see available templates
- Check template naming (case-sensitive)
- Ensure templates are in `pages/` or `templates/` folder

**Structure not preserved:**
- Verify `preserve_structure: true` is set
- Check if page exists before updating
- Use `get_logseq_page_context` to debug

**Content not formatted as outline:**
- This is automatic - no action needed
- Headers (##) are preserved as-is
- Plain text becomes bullets (-)

**Properties lost:**
- Properties are always preserved at top of page
- Check if original page had properties
- Use `get_logseq_page_context` to verify

## Summary

The smart Logseq integration transforms the MCP server from a simple copy-paste tool into an intelligent assistant that:

✅ Understands your Logseq structure
✅ Uses your templates automatically  
✅ Preserves your formatting preferences
✅ Formats content as proper outlines
✅ Maintains metadata and properties

**Result:** Professional, consistent Logseq pages that match your existing workflow.
