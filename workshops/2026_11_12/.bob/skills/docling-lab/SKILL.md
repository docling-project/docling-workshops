---
name: docling-lab
description: >
  Use when the user wants to convert documents with the Docling for IBM watsonx managed service,
  query DocLang files with dclq, extract structured information from converted documents, or build
  and save a DoclingDocument programmatically. Covers converting a single file, a URL, or a
  directory; choosing output formats; enabling enrichments; inspecting document outlines with dclq;
  filling a JSON form from converted Markdown; and authoring a DoclingDocument with titles,
  headings, text, and tables. Trigger phrases: "convert", "docling convert", "convert to markdown",
  "extract from PDF", "convert with docling", "docling remote", "docling-lab", "dclq", "outline",
  "heading outline", "extract fields", "fill the form", "information extraction",
  "DoclingDocument", "save as doclang", "build a document", "save_as_doclang_archive",
  "dclx from python", "add_table", "add_heading".
---

# Docling Lab — Command-Line Conversion Skill

This skill teaches Bob how to convert documents using the `docling convert-remote` CLI, which
sends conversion requests to the **Docling for IBM watsonx** managed service. No local ML models
or GPU are required — all processing happens on the service.

## Prerequisites

- Virtual environment in the workshop directory is active (`.venv`): `source .venv/bin/activate`
- `.env` file in the workshop directory is populated with `DOCLING_SERVICE_URL` and `DOCLING_SERVICE_API_KEY`
- `docling-client` and `dclq` are installed (`uv pip install docling-client dclq`)

Credentials are loaded automatically from the `.env` file — no need to export them manually.

## When to use each reference

| Task | Reference |
|---|---|
| Convert a file, URL, or directory | [convert.md](convert.md) |
| Customize the pipeline (OCR, enrichments, output formats, page range) | [options.md](options.md) |
| Query converted documents with dclq (inspect, outline, grep, show) | [query.md](query.md) |
| Extract structured fields from converted documents and fill a JSON form | [extraction.md](extraction.md) |
| Build a DoclingDocument in Python (title, heading, text, table) and save as DocLang | [doclang.md](doclang.md) |

Always read the relevant reference before running a command or answering a question.
When the user's request involves any of the above tasks, activate this skill and route to the
appropriate reference file.
