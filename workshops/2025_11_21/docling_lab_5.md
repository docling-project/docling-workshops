# Agentic AI with Docling

## Langflow

Start Langflow:

```bash
uvx langflow run
```

LLM:
- `granite-4.0-h-small`
- temperature: 0
- seed: 42

Test file: demo_data/afr2023_71.pdf

Questions:
- What is the document about?
- What is the total loss allowance for trade receivables?

## LM Studio + Docling MCP

Start Docling MCP:

```bash
DOCLING_MCP_KEEP_IMAGES=1 uvx --from docling-mcp docling-mcp-server --transport streamable-http conversion generation
```

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

Questions:
- Summarize https://arxiv.org/pdf/2408.09869
- Show me page 1
