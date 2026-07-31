# Hands-On with Docling for IBM watsonx
## Convert, Extract, and Build Your Own Document-Powered App

> **IBM TechXchange 2026 · Hands-on Lab · 90 minutes**

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Lab Architecture](#2-lab-architecture)
3. [Part 1 — Get Ready with Docling for IBM watsonx](#3-part-1--get-ready-with-docling-for-ibm-watsonx) *(20 min)*
4. [Part 2 — Choose Your Track](#4-part-2--choose-your-track) *(35 min)*
   - [Track A — Document Intelligence with IBM Bob](#track-a--document-intelligence-with-ibm-bob)
   - [Track B — Document Intelligence with Python](#track-b--document-intelligence-with-python)
5. [Use Case — Fill the Compliance Assessment Form](#5-use-case--fill-the-compliance-assessment-form) *(20 min)*
6. [Continue Learning](#6-continue-learning)

---

## 1. Introduction

### The scenario

You are a compliance analyst at **Meridian Financial Group**, a mid-sized bank operating across multiple regulatory jurisdictions. Every quarter you receive a bundle of regulatory submissions, audit reports, and product disclosure sheets — all arriving as PDFs, Word documents, and EPUBs — and must populate a standardised **Compliance Assessment Form** with the key obligations, risk indicators, and financial metrics they contain.

Today you will use **Docling for IBM watsonx** to automate that pipeline: from raw documents to a filled-in, audit-ready assessment — without standing up a single GPU.

### About this lab

This lab introduces **Docling for IBM watsonx**, the enterprise managed-service edition of the open-source [Docling](https://github.com/docling-project/docling) document AI toolkit. You will:

- Use the **Workbench** (no-code UI) to convert, inspect, and export compliance documents
- Export documents to the **DocLang** open ISO standard and explore them in the **DocLang Viewer**
- Choose a hands-on track: **IBM Bob** (AI-assistant, no coding) or **Python notebook** (developer)
- Extract structured data from multiple documents and auto-populate a Compliance Assessment Form

### Lab timing

| Part | Activity | Time |
|------|----------|------|
| Part 1 | Get Ready with Docling for IBM watsonx | 20 min |
| Part 2 | Choose Your Track (Bob *or* Python) | 35 min |
| Use Case | Fill the Compliance Assessment Form | 20 min |
| **Total** | | **75 min** |

> The remaining 15 minutes of the 90-minute session are reserved for setup, Q&A, and the optional extension steps.

### Prerequisites

- A laptop with a modern browser
- **Track A (IBM Bob):** IBM Bob access — provided by your instructor
- **Track B (Python):** Python 3.10+ and [`uv`](https://docs.astral.sh/uv/) — see setup steps in Section 4
- A **Docling for IBM watsonx** trial account — you will create this in Part 1

---

## 2. Lab Architecture

### How Docling for IBM watsonx works

<!-- TODO: add architecture diagram showing: browser/SDK → Docling for IBM watsonx API (IBM Cloud) → DoclingDocument → export formats / downstream tools -->

Docling for IBM watsonx exposes the Docling document AI stack as a **fully managed REST API**. You send a document (PDF, DOCX, EPUB, image, …); the service runs layout analysis, OCR, table structure detection, and enrichment on IBM Cloud; and returns a structured **DoclingDocument** you can export to Markdown, HTML, JSON, or DocLang.

| Component | Role in this lab |
|-----------|-----------------|
| **Docling for IBM watsonx** | Managed conversion service — no local GPU or model needed |
| **Workbench** | No-code drag-and-drop UI for conversion and export |
| **DocLang Viewer** | Online viewer for DocLang-format documents |
| **IBM Bob** (Track A) | AI assistant connected to Docling via **Docling Skills** (packaged in the `docling` library) and/or the **Docling MCP server** |
| **Python SDK** (Track B) | `DoclingServiceClient` — same call shape as the local `DocumentConverter` |
| **watsonx.ai** (Track B) | LLM for RAG generation and compliance summarization |

### Lab documents

The `data/` folder contains the Q3 compliance bundle for Meridian Financial Group:

| File | Format | Key fields it contains |
|------|--------|----------------------|
| `meridian_risk_disclosure.pdf` | PDF (5 pages) | Entity name, reporting period, reference number, total risk exposure, risk category table, capital ratios |
| `q3_audit_summary.docx` | DOCX (6 sections) | Material findings, sign-off date, confirms risk exposure and reference number |
| `regulatory_guidelines_2025.epub` | EPUB (7 chapters) | Key regulatory obligations, AML requirements, reporting deadlines |
| `compliance_assessment_form.json` | JSON | Empty form template — to be populated during the lab |

---

## 3. Part 1 — Get Ready with Docling for IBM watsonx
### *(20 minutes — everyone)*

### 3.1 Sign Up for a Free Trial

1. Go to the free-trial registration page:
   **<https://www.ibm.com/account/reg/us-en/signup?formid=urx-54322>**
2. Sign in with your IBM ID (or create one — it is free).
3. Once provisioned, you land on the **Docling for IBM watsonx** dashboard.

> **Tip:** Your instructor has a shared service URL and API key on the whiteboard if you encounter provisioning delays.

<!-- TODO: add screenshot of dashboard landing page -->

---

### 3.2 Explore the Workbench

The **Workbench** converts documents with drag-and-drop — no code needed.

<!-- TODO: add screenshot of the Workbench UI with callouts -->

1. In the Workbench, click **Upload** and drag `meridian_risk_disclosure.pdf` from the `data/` folder onto the upload area.
2. When conversion completes, browse the **document preview**:
   - Expand the **document tree** — note sections, tables, and figures as separate nodes
   - Click any table to inspect how individual cells and column headers were reconstructed
3. Repeat with `q3_audit_summary.docx` — observe that DOCX produces the same DoclingDocument structure.
4. Try one conversion option: toggle **Table structure** off, re-convert, and compare quality.

---

### 3.3 Export to DocLang — the ISO Standard

**DocLang** (`.dclx`) is an open XML-based ISO standard for structured documents. Unlike Markdown, it preserves heading hierarchy, table cell relationships, list nesting, and figure captions — each element addressable by XPath.

1. Select `meridian_risk_disclosure.pdf` in the Workbench and click **Export → DocLang**.
2. Download the `.dclx` file. Keep it — you will use it in the next step.

---

### 3.4 Inspect the DocLang File in the Viewer

1. Open **<https://doclang.ai/viewer/>** and drag your `.dclx` file onto it.
2. In the tree panel (left), find the first table. Note its **XPath** (e.g. `/heading[4]/table[1]`).
3. Verify that column headers and individual cells are separate nodes — this is what enables precise extraction later.

<!-- TODO: add screenshot of the DocLang Viewer with tree panel callout -->

---

### 3.5 Get an API Key

You need this to connect Part 2 tools to the managed service.

<!-- TODO: add screenshot of the API key creation screen with callouts -->

1. In the dashboard, go to **Settings → API Keys → Create API key**.
2. Copy both the **Service URL** and the **API key** from the confirmation screen.
3. Keep them handy — you will paste them into your tool configuration in Part 2.

> ⚠️ Never commit your API key to a git repository. The `.env` file in this lab is in `.gitignore`.

---

## 4. Part 2 — Choose Your Track
### *(35 minutes — pick Track A or Track B)*

**Track A — IBM Bob:** no code, conversational, requires Bob access. Bob connects to Docling via **Skills** (installed from the `docling` package) and/or the **Docling MCP server**.
**Track B — Python notebook:** requires Python 3.10+ and `uv`.

Rejoin at [Section 5 (Use Case)](#5-use-case--fill-the-compliance-assessment-form) when your 35 minutes are up.

---

### Track A — Document Intelligence with IBM Bob

#### A.1 Create a Workspace and Install the Docling Skill

1. Open IBM Bob and create a new workspace named `docling-compliance-lab`.
2. In a terminal, make the Docling skill available:
   ```bash
   pip install docling
   ```
3. Find the skill path and activate `SKILL.md` in Bob:
   ```bash
   python -c "
   import importlib.util, pathlib
   print(pathlib.Path(importlib.util.find_spec('docling').origin).parent / '.agents/skills/docling')
   "
   ```

**TODO: TOO COMPLEX, FOLLOW INSTRUCTIONS in https://internal.bob.ibm.com/docs/ide/features/skills**

> The skill teaches Bob about conversion, extraction, chunking, and the service client. See [agent skills docs](https://docling-project.github.io/docling/usage/agent_skills/).

---

#### A.2 Connect to the Managed Service and Start the MCP Server

Install the lightweight service-client (no local ML models):

```bash
pip install "docling-slim[service-client]"
```

Create `.env` from the template (copy `env.example` to `.env`) and fill in your credentials.

Start the Docling MCP server in **remote mode**:

```bash
DOCLING_MCP_CONVERSION_MODE=remote \
DOCLING_MCP_SERVICE_URL=https://<your-service-url> \
DOCLING_MCP_SERVICE_API_KEY=<your-api-key> \
uvx --from docling-mcp docling-mcp-server \
  --transport streamable-http conversion generation manipulation
```

Register the server in Bob's MCP configuration:

```json
{
  "mcpServers": {
    "docling": { "url": "http://localhost:8000/mcp" }
  }
}
```

---

#### A.3 Convert, Explore, and Extract

Try these prompts in Bob:

```
Convert data/meridian_risk_disclosure.pdf and return the document key.
```
```
Show me the heading outline of the document.
```
```
What are the main risk categories described in this document?
```
```
From data/meridian_risk_disclosure.pdf, extract these fields as JSON:
entity_name, reporting_period, total_risk_exposure_usd,
highest_risk_category, regulator_reference_number.
```

> When done, proceed to [Section 5 (Use Case)](#5-use-case--fill-the-compliance-assessment-form).

---

### Track B — Document Intelligence with Python

#### B.1 Environment Setup

```bash
uv venv && source .venv/bin/activate
uv pip install notebook ipywidgets ipykernel
cp env.example .env    # then edit .env with your credentials
jupyter notebook docling_lab.ipynb
```

Install the service-client package (no local ML models needed):

```bash
uv pip install "docling-slim[service-client,feat-chunking]"
```

---

#### B.2 Work Through the Notebook

Open `docling_lab.ipynb` and run sections **1 through 7** in order:

| Section | What you do |
|---------|------------|
| 1 | Connect to the managed service (`DoclingServiceClient`) |
| 2 | Convert PDF, DOCX, and EPUB with `client.convert_all()` |
| 3 | Inspect the document structure (sections, tables, figures) |
| 4 | Export to DocLang and query with `dclq` shell commands |
| 5 | Chunk a document with `client.chunk(ChunkerKind.HYBRID)` |
| 6 | RAG pipeline: `DoclingLoader` → Milvus → watsonx.ai LLM |
| 7 | Extract typed fields with `DocumentExtractor` + Pydantic |

Key `dclq` commands you will run in Section 4:

```bash
dclq inspect  meridian_risk_disclosure.dclx   # inventory
dclq outline  meridian_risk_disclosure.dclx   # heading tree + XPaths
dclq grep -i  'risk exposure' meridian_risk_disclosure.dclx
dclq show     meridian_risk_disclosure.dclx '/heading[2]' --section
```

> When done with Section 7, proceed to [Section 5 (Use Case)](#5-use-case--fill-the-compliance-assessment-form).

---

## 5. Use Case — Fill the Compliance Assessment Form
### *(20 minutes — everyone)*

The **Compliance Assessment Form** (`data/compliance_assessment_form.json`) defines these fields — spread across the three documents:

```json
{
  "entity_name": null,
  "reporting_period": null,
  "total_risk_exposure_usd": null,
  "highest_risk_category": null,
  "regulator_reference_number": null,
  "key_obligations": [],
  "material_findings": [],
  "sign_off_date": null
}
```

### Step 1 — Convert All Three Documents *(2 min)*

**Track A (Bob):**
```
Convert all three documents in the data/ folder and return their document keys.
```

**Track B (notebook — Section 2):** already done. Skip to Step 2.

---

### Step 2 — Get a Document Outline *(3 min)*

**Track A (Bob):**
```
Show me the heading outline of q3_audit_summary.docx.
```

**Track B — `dclq`:**
```bash
dclq outline q3_audit_summary.dclx
```

---

### Step 3 — Extract Compliance Metrics *(5 min)*

**Track A (Bob):**
```
From all three compliance documents, extract the following fields and return JSON:
entity_name, reporting_period, total_risk_exposure_usd, highest_risk_category,
regulator_reference_number, key_obligations (list), material_findings (list), sign_off_date.
```

**Track B (notebook — Section 7):** the `ComplianceForm` Pydantic model and multi-document merge loop are already in the notebook. Run the extraction cells.

---

### Step 4 — Generate a Summary and Fill the Form *(10 min)*

**Track A (Bob):**
```
Based on the extracted data, write a 3-sentence compliance executive summary
covering total risk exposure, the highest risk category, and the critical obligations.
Then create a new DoclingDocument with the filled form as a structured table
and export it to Markdown.
```

**Track B (notebook — Section 8):** Run the "Putting It All Together" cells — they assemble the extracted fields, call the watsonx.ai LLM for the narrative summary, and render an HTML compliance report.

---

### ✅ What you achieved

By the end of this use case you have processed three documents in three different formats, extracted eight structured fields without manual copy-paste, generated an executive summary, and produced an audit-ready HTML report — all powered by Docling for IBM watsonx.

---

### Extension steps (if time permits)

**Track A — Auto-fill the Word document (requires Bob DOCX tool):**
```
Using the extracted values, update data/compliance_assessment_form.docx
and save the result as data/compliance_assessment_form_filled.docx.
```

**Track B — Edit the form with Docling Agent (Section 9 in the notebook):**
The notebook includes commented-out code for `DoclingEditingAgent` that can apply natural-language edits to a DoclingDocument template.
> ℹ️ `docling-agent` is not yet on PyPI — install from source:  
> `pip install git+https://github.com/docling-project/docling-agent`

---

## 6. Continue Learning

The lab materials remain available after the event:
**<https://github.com/docling-project/docling-workshops>** → folder `workshops/2026_10_26/`

The Docling for IBM watsonx **free trial** stays active — continue at:
**<https://www.ibm.com/products/docling>**

### Resources

| Resource | URL |
|----------|-----|
| Docling for IBM watsonx | <https://www.ibm.com/products/docling> |
| Free trial sign-up | <https://www.ibm.com/account/reg/us-en/signup?formid=urx-54322> |
| Docling documentation | <https://docling-project.github.io/docling/> |
| Managed service docs | <https://docling-project.github.io/docling/usage/api_server/managed/> |
| Agent skills docs | <https://docling-project.github.io/docling/usage/agent_skills/> |
| Docling MCP | <https://github.com/docling-project/docling-mcp> |
| Docling Agent | <https://github.com/docling-project/docling-agent> |
| DocLang Viewer | <https://doclang.ai/viewer/> |
| `dclq` CLI | <https://github.com/docling-project/docling-core/tree/main/packages/dclq> |
| Docling GitHub | <https://github.com/docling-project/docling> |
| Docling Discord | <https://docling.ai/discord> |

### Quick reference — service client

```python
from docling.service_client import DoclingServiceClient, ChunkerKind

client = DoclingServiceClient(url=..., api_key=...)

result = client.convert(source="report.pdf")          # single document
print(result.document.export_to_markdown())

for r in client.convert_all(source=["a.pdf", "b.docx"], max_concurrency=4):
    print(r.input.file.name, r.status)                # many documents

response = client.chunk(source="report.pdf", chunker=ChunkerKind.HYBRID)
```

### Quick reference — `dclq`

```bash
dclq inspect  doc.dclx                            # structural inventory
dclq outline  doc.dclx                            # heading tree + XPaths
dclq grep -i  'PATTERN' doc.dclx                  # search semantic units
dclq show     doc.dclx '/heading[N]' --section    # retrieve a section
dclq list     doc.dclx --type table_cell --page 1 # list units by type
```

### Quick reference — Docling MCP (remote mode)

```bash
DOCLING_MCP_CONVERSION_MODE=remote \
DOCLING_MCP_SERVICE_URL=https://<url> \
DOCLING_MCP_SERVICE_API_KEY=<key> \
uvx --from docling-mcp docling-mcp-server \
  --transport streamable-http conversion generation manipulation
```

### Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `DOCLING_SERVICE_URL not set` | `.env` not loaded | Run `cp env.example .env` and fill in your credentials |
| Conversion returns empty Markdown | Scanned PDF, no text layer | Enable **OCR** in the Workbench options |
| `dclq` command not found | Package not installed | `pip install dclq` |
| Notebook kernel crash on import | Missing dependency | Re-run the install cell, then **Kernel → Restart** |
| MCP server not responding | Server not started | Re-run the `uvx --from docling-mcp ...` command; check port 8000 is free |
| watsonx.ai returns 401 | Expired API key | Regenerate the key at cloud.ibm.com and update `.env` |
