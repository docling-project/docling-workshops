# Docling Lab — Pipeline Options Reference

All flags below are appended to `docling convert-remote <source>`.
Combine any number of them in a single command.

---

## Output formats (`--to`)

Multiple `--to` flags produce multiple output files from a single conversion.

| Flag | Output |
|---|---|
| `--to md` | Markdown (default if `--to` is omitted) |
| `--to json` | Docling JSON (full document model) |
| `--to html` | Single-page HTML |
| `--to text` | Plain text |
| `--to dclx` | DocLang archive (`.dclx`) — the ISO standard format |
| `--to chunks` | Text chunks ready for RAG ingestion |

**Example — Markdown and DocLang:**

```bash
docling convert-remote --to md --to dclx --output ./output \
    my_file.pdf
```

---

## Input format filter (`--from`)

Restricts which file types are processed when converting a directory.
Has no effect on single-file or URL conversions.

```bash
# Only PDF and DOCX files in the docs/ directory
docling convert-remote --from pdf --from docx docs/
```

---

## Text and OCR

| Flag | Effect |
|---|---|
| `--no-ocr` | Disable OCR — use for born-digital PDFs where text is already embedded |
| `--force-ocr` | Replace all existing text with OCR output (useful for scanned PDFs with bad embedded text) |
| `--ocr-lang <langs>` | Comma-separated OCR language codes, e.g. `en,fr,de` |

**Example — born-digital PDF, no OCR needed:**

```bash
docling convert-remote --no-ocr my_file.pdf
```

---

## Table extraction

| Flag | Effect |
|---|---|
| `--tables` | Extract table structure — cells, headers, spans (default: on) |
| `--no-tables` | Skip table extraction (faster, but tables become plain text) |

---

## Enrichments

Enrichments run additional AI models on the converted content.
Each is off by default; enable only the ones you need.

| Flag | Effect |
|---|---|
| `--enrich-picture-classes` | Classify each image by type (photo, chart, diagram, …) |
| `--enrich-picture-description` | Generate a natural-language description for each image |
| `--enrich-chart-data` | Extract structured data from chart images |
| `--enrich-formula` | Recognise and mark up mathematical formulae |
| `--enrich-code` | Detect and mark up code blocks |

**Example — classify images and extract chart data:**

```bash
docling convert-remote --enrich-picture-classes --enrich-chart-data \
    my_file.pdf
```

---

## Page range

Convert only a subset of pages (1-based, inclusive):

```bash
docling convert-remote --page-range 1-3 my_file.pdf
```

---

## Pipeline selection (`--pipeline`)

| Value | Use case |
|---|---|
| `standard` | Default — layout analysis + table detection (best for most documents) |
| `vlm` | Vision-language model pipeline — slower but better on complex layouts |
| `legacy` | Older pipeline — use only if `standard` produces unexpected results |

```bash
docling convert-remote --pipeline vlm my_file.pdf
```

---

## Combining options — full example

Convert the PDF to Markdown and DocLang, skip OCR, classify images,
extract chart data, and save results to `./output`:

```bash
docling convert-remote \
    --to md --to dclx \
    --no-ocr \
    --enrich-picture-classes \
    --enrich-chart-data \
    --output ./output \
    my_file.pdf
```
