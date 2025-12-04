# Agentic AI with Docling

## LM Studio + Docling MCP

In this lab we will use Docling inside the [LM Studio](https://lmstudio.ai/) app (for other runtime apps the instructions are similar).

Start Docling MCP:

```bash
DOCLING_MCP_KEEP_IMAGES=1 uvx --from docling-mcp docling-mcp-server --transport streamable-http conversion generation
```

_Note: make sure to run the command from a folder *without* the `.env` file._


Edit `mcp.json` file:

```
{
  "mcpServers": {
    "docling": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Can use e.g. `openai/gpt-oss-20b`.

### Interact with documents

Prompts:
- Summarize https://arxiv.org/pdf/2408.09869
- Show me page 1

### Create documents

Prompt:

```
Create a new Docling document with the title \"Open-Source Agentic AI\", a paragraph, and a list of the main applications. Show the result in valid markdown.
```
