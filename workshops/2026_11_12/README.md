# Hands-On with Docling for IBM watsonx
## Convert, Extract, and Build Your Own Document-Powered App

> **OpenTech Connect 2026 · Hands-on Workshop · 90 minutes**
>
> 📄 The printable [lab guide (PDF)](OpenTech-Connect-2026-Lab-Guide.pdf) for this session.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Workshop Architecture](#2-workshop-architecture)
3. [Part 1 — Get Ready with Docling for IBM watsonx](#3-part-1--get-ready-with-docling-for-ibm-watsonx) *(20 min)*
4. [Part 2 — Choose Your Track](#4-part-2--choose-your-track) *(50 min)*
   - [Where both tracks are going: the form](#where-both-tracks-are-going-the-form)
   - [Track A — Document Intelligence with IBM Bob](#track-a--document-intelligence-with-ibm-bob)
   - [Track B — Document Intelligence with Python](#track-b--document-intelligence-with-python)
5. [Compare the Two Routes](#5-compare-the-two-routes) *(5 min)*
6. [Continue Learning](#6-continue-learning)

---

## 1. Introduction

### The scenario

You are a compliance analyst at **Vantara Bank**, a mid-sized bank operating across multiple regulatory jurisdictions. Every quarter you receive a bundle of regulatory submissions, audit reports, and product disclosure sheets — all arriving as PDFs, Word documents, and EPUBs — and must populate a standardised **Compliance Assessment Form** with the key obligations, risk indicators, and financial metrics they contain.

Today you will use **Docling for IBM watsonx** to automate that pipeline: from raw documents to a filled-in, audit-ready assessment — without standing up a single GPU.

### About this workshop

This workshop introduces **Docling for IBM watsonx**, the enterprise managed-service edition of the open-source [Docling](https://github.com/docling-project/docling) document AI toolkit. You will:

- Use the **Workbench** (no-code UI) to convert, inspect, and export compliance documents
- Export documents to **DocLang**, the open ISO standard for documents, and explore them in the **DocLang Viewer**
- Choose a hands-on track — **IBM Bob** (AI assistant, no coding) or a **Python notebook** (developer) — that takes you all the way to the filled Compliance Assessment Form
- Compare the two routes to the same eight fields

### Workshop timing

| Part | Activity | Time |
|------|----------|------|
| Part 1 | Get Ready with Docling for IBM watsonx | 20 min |
| Part 2 | Your track (Bob *or* Python), ending with the filled form | 50 min |
| Compare | Two routes to the same eight fields | 5 min |
| **Total** | | **75 min** |

> The remaining 15 minutes of the 90-minute session are reserved for setup, Q&A, and the optional extension steps.

### Prerequisites & Access

- An **IBMid** — sign in or register for free at IBM.
- A **Docling for IBM watsonx** trial account — request free access at **<https://www.ibm.com/products/docling>**
- **IBM Bob** — download and request free trial access at **<https://bob.ibm.com/download>**
- **watsonx.ai** *(Track B)* — request free trial access at **<https://www.ibm.com/products/watsonx-ai>**

---

## 2. Workshop Architecture

### How Docling for IBM watsonx works

Docling for IBM watsonx exposes the Docling document AI stack as a **fully managed REST API**. You send a document (PDF, DOCX, EPUB, image, …); the service runs layout analysis, OCR, table structure detection, and enrichment on IBM Cloud; and returns a structured **DoclingDocument** you can export to Markdown, HTML, JSON, or DocLang.

No local GPU or model download is required: Docling converts on the managed service, and in Track B **watsonx.ai** serves the embedding model and the language model.

| Component | Role in this workshop |
|-----------|----------------------|
| **Docling for IBM watsonx** | Managed conversion service — no local GPU or model needed |
| **Workbench** | No-code drag-and-drop UI for conversion and export |
| **DocLang Viewer** | Online viewer for DocLang-format documents (<https://doclang.ai/viewer/>) |
| **IBM Bob** (Track A) | AI assistant connected to Docling via the **docling-lab skill** in `.bob/skills/` |
| **IBM Bob as an IDE** (Track B) | Runs the notebook: editor, Explorer and terminal |
| **Docling Service Client** (Track B) | The Docling [Python SDK](https://developer.dcls.saas.ibm.com/examples/basic/#python-sdk-usage) for calling Docling as a service |
| **watsonx.ai** (Track B) | Embeddings and LLM for RAG, extraction, the summary, and the editing agent |

### Workshop documents

The `docs/` folder contains all the documents for this workshop:

| File | Format | Key fields it contains |
|------|--------|----------------------|
| `vantara_risk_disclosure.pdf` | PDF (4 pages) | Entity name, reporting period, reference number, total risk exposure, risk category table, capital ratios, **logo**, **3 data charts** |
| `q3_audit_summary.docx` | DOCX (6 sections) | Material findings, sign-off date, confirms risk exposure and reference number |
| `regulatory_guidelines_2026.epub` | EPUB (7 chapters) | Key regulatory obligations, AML requirements, reporting deadlines |
| `compliance_assessment_form.json` | JSON | Empty form template — filled at the end of both tracks |
| `docling_lab.ipynb` | IPYNB | Notebook for Track B |

---

## 3. Part 1 — Get Ready with Docling for IBM watsonx
### *(20 minutes — everyone)*

### 3.1 Set up the environment

Clone the repository and run the bootstrap script from within the workshop directory:

```bash
git clone https://github.com/docling-project/docling-workshops.git
cd docling-workshops/workshops/2026_11_12
./bootstrap.sh
```

It verifies prerequisites, installs `uv` (if needed), creates the Python 3.12 virtual environment with `docling-client` and `dclq`, and creates `.env` from `.env.example`.

### 3.2 Sign Up for a Free Trial

1. Go to **<https://www.ibm.com/products/docling>** and request the free trial.
2. Sign in with your IBMid (or create a new one).
3. Follow the prompts to start the trial. Once active, click *Access your trial now* to land on the **Docling for IBM watsonx** dashboard.

---

### 3.3 Explore the Workbench

The **Workbench** converts documents with drag-and-drop — no code needed.

1. In the Workbench, click **Upload a document** and select `vantara_risk_disclosure.pdf` from the `docs/` folder.
2. When conversion completes, inspect the result in the **Tasks** section:
   - The **left column** displays the document structure as a tree of nodes — sections, paragraphs, tables, and figures. Note that text extracted from images appears as dedicated nodes, and headers/footers appear on a shaded background.
   - The **right column** renders the document as it appears in the original file. Click on any element to highlight the corresponding node.
   - Click any table node to inspect reconstructed cells and column headers.
3. Repeat with `q3_audit_summary.docx` or any URL of your choice.
4. Try a conversion with custom options: click **Create task** → **Single** → select `vantara_risk_disclosure.pdf`:
   - **Output formats:** check **DCLX** to produce a DocLang archive.
   - **Text:** uncheck **Enable OCR** (born-digital PDF).
   - **Images:** check **Picture classification** to label each image by type.
5. Click **Actions** → **Download** to save the conversion output archive (`.dclx`).

---

### 3.4 Inspect the DocLang File — the ISO Standard

**DocLang** is an open XML-based ISO standard for structured documents (**<https://doclang.ai>**).

1. Open **<https://doclang.ai/viewer/>** in your browser.
2. Drag and drop the downloaded `.dclx` file.
3. In the **Layers** drop-down, uncheck **Furniture** to filter out headers and footers from view.

---

### 3.5 Get an API Key

1. In your browser, return to the **Docling for IBM watsonx** dashboard.
2. Go to the **API examples** section to find your **Service URL**.
3. Click **Get API key** → **Generate an API key**, name your key, and copy it.

---

### 3.6 Set your Connection Details in `.env`

1. Open `.env` in your editor.
2. Replace `DOCLING_SERVICE_URL` and `DOCLING_SERVICE_API_KEY` with your actual credentials:

```bash
DOCLING_SERVICE_URL=https://<your-service-url>
DOCLING_SERVICE_API_KEY=<your-api-key>

# watsonx.ai credentials (Track B)
WX_API_KEY=<your-watsonx-api-key>
WX_PROJECT_ID=<your-watsonx-project-id>
WX_URL=https://us-south.ml.cloud.ibm.com
```

> [!TIP]
> Run `python scripts/test_connection.py` to check that `docling-client` is installed in your `.venv`, your `.env` credentials are valid, and an end-to-end conversion against the Docling service succeeds.

---

## 4. Part 2 — Choose Your Track
### *(50 minutes — pick Track A or Track B)*

Both tracks use the same service, documents, and credentials, ending with the filled **Compliance Assessment Form**.

| | Track A — IBM Bob | Track B — Python notebook |
|---|---|---|
| **Best for** | anyone; no coding required | developers, data engineers |
| **You drive it from** | conversation with Bob's AI assistant | notebook cells (`docs/docling_lab.ipynb`) |
| **You finish with** | form as JSON, summary, Markdown table | Pydantic object, HTML report, DocLang file |
| **Needs** | IBM Bob (<https://bob.ibm.com/download>) | watsonx.ai (<https://www.ibm.com/products/watsonx-ai>) |

### Where both tracks are going: the form

The **Compliance Assessment Form** (`docs/compliance_assessment_form.json`) defines eight fields:

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

| Field | Lives in |
|-------|----------|
| `entity_name`, `reporting_period`, `total_risk_exposure_usd`, `highest_risk_category`, `regulator_reference_number` | `vantara_risk_disclosure.pdf` |
| `material_findings` (list), `sign_off_date` | `q3_audit_summary.docx` |
| `key_obligations` (list) | `regulatory_guidelines_2026.epub` |

---

### Track A — Document Intelligence with IBM Bob

#### A.1 Check the Connection

Activate your environment and verify connectivity (this verifies that `docling-client` is installed, `.env` settings are configured correctly, and a live document conversion test succeeds):

```bash
source .venv/bin/activate
python scripts/test_connection.py
```

#### A.2 Launch IBM Bob and Load the Lab Skill

1. Open **IBM Bob** and log in with your IBMid.
2. The skill in `.bob/skills/docling-lab/` is automatically detected. On first prompt, click **Approve skill tools for task**.

#### A.3 Convert, Explore, and Extract

Try these prompts in Bob:

```
Convert docs/vantara_risk_disclosure.pdf and return the document key.
```
```
Show me the heading outline of the document.
```
```
From docs/vantara_risk_disclosure.pdf, extract these fields as JSON:
entity_name, reporting_period, total_risk_exposure_usd, highest_risk_category, regulator_reference_number.
```

#### A.4 Fill the Form from All Three Documents

```
Convert all three documents in the docs/ folder and extract the fields for compliance_assessment_form.json as structured JSON.
```

#### A.5 Write the Summary and Export

```
Based on the extracted data, write a 3-sentence compliance executive summary
covering total risk exposure, highest risk category, and key obligations.
Then create a new DoclingDocument with the filled form as a structured table
and export it to Markdown.
```

---

### Track B — Document Intelligence with Python

#### B.1 Open the Notebook

1. In IBM Bob or your IDE, open `docs/docling_lab.ipynb`.
2. Select the Python kernel pointing to `.venv`.
3. Run the setup cells to load credentials from `.env`.

#### B.2 Work Through the Notebook

| Section | What you do |
|---------|------------|
| 1 | Connect to the managed service (`DoclingServiceClient`) |
| 2 | Convert PDF, DOCX, and EPUB with `client.convert_all()` |
| 3 | Inspect document structure (sections, tables, figures) |
| 4 | Export to DocLang (`output/*.dclx`) and query with `dclq` |
| 5 | Chunk documents with `HybridChunker` |
| 6 | Build RAG pipeline with watsonx.ai embeddings and LLM |
| 7 | Extract eight fields into a Pydantic `ComplianceForm` schema |
| 8 | Generate executive summary and HTML report (`output/compliance_assessment_form_filled.html`) |
| 9 | *(optional)* Fill form with `DoclingEditingAgent` |

---

## 5. Compare the Two Routes
### *(5 minutes — everyone)*

| Dimension | Track A — IBM Bob | Track B — Python notebook |
|---|---|---|
| **Where the form is defined** | In conversational prompt | In Pydantic model with types |
| **Inspection & Trace** | Chat tool execution trace | Cell inputs, schema, and outputs |
| **Reproducibility** | Exploratory / prompt-driven | Deterministic script execution |
| **Best for** | Rapid ad-hoc analysis | Automated recurring quarterly pipelines |

---

## 6. Continue Learning

- **Docling Open Source:** <https://github.com/docling-project/docling>
- **Docling for IBM watsonx:** <https://www.ibm.com/products/docling>
- **IBM Bob Assistant:** <https://bob.ibm.com/download>
- **IBM watsonx.ai:** <https://www.ibm.com/products/watsonx-ai>
- **DocLang Viewer:** <https://doclang.ai/viewer/>
- **Docling MCP Server:** <https://github.com/docling-project/docling-mcp>
