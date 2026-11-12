# Docling Lab — Converting Documents

All commands use `docling convert-remote`. Credentials are read automatically from the `.env`
file in the working directory.

---

## IMPORTANT — always pass `--from <format>`

Due to a known bug in `docling-client`, calling `docling convert-remote` **without** `--from`
makes the service reject the upload (`HTTP 422 Unprocessable Entity`, "Task submission failed",
"Document ... failed to convert"). The workaround is to **always specify the valid input
format(s) explicitly with `--from`**, even for a single file or URL.

```bash
# DO NOT — fails with 422
docling convert-remote docs/vantara_risk_disclosure.pdf

# DO — works
docling convert-remote --from pdf docs/vantara_risk_disclosure.pdf
```

Pick `--from` to match the input file type (repeat the flag for mixed inputs):

| File extension | `--from` value |
|---|---|
| `.pdf` | `pdf` |
| `.docx` | `docx` |
| `.epub` | `epub` |
| `.pptx` | `pptx` |
| `.html` | `html` |
| `.md` | `md` |
| `.xlsx` | `xlsx` |
| images (`.png`, `.jpg`, …) | `image` |

Run `docling convert-remote --help` for the full list of valid `--from` values.

If a conversion fails with a 422 / "failed to convert" message, first check that `--from` is set
and matches the file type before investigating anything else.

**Example — PDF to Markdown and DocLang (`.dclx`):**

```bash
docling convert-remote --from pdf --to md --to dclx --output ./output \
    docs/vantara_risk_disclosure.pdf
```

---

## Convert a single local file

```bash
docling convert-remote --from pdf my_file.pdf
```

Output is written to the current directory as `my_file.md` (Markdown by default).
To write to a specific folder:

```bash
docling convert-remote --from pdf --output ./output my_file.pdf
```

---

## Convert a file from a URL

```bash
docling convert-remote --from pdf https://arxiv.org/pdf/2408.09869
```

---

## Convert multiple files at once

Pass multiple paths or URLs as separate arguments:

```bash
docling convert-remote --from pdf --from docx --from epub my_file.pdf \
                       api_reference.docx \
                       annual_report.epub
```

---

## Convert all documents in a directory

```bash
docling convert-remote --from pdf --from docx --from epub docs/
```

Without `--from`, `--from` defaults to all formats, which triggers the bug described above — so
list every format you want converted. The command walks the directory tree and converts files
matching those formats. To restrict to fewer formats (e.g. only PDFs and DOCX files):

```bash
docling convert-remote --from pdf --from docx docs/
```

---

## Check conversion output

After conversion, the output files appear in the directory specified by `--output` (default: `.`).
Each source document produces one output file per requested format, named after the source file.

Example — after converting `my_file.pdf` to Markdown and JSON:

```
./my_file.md
./my_file.json
```

---

## Exit codes

| Code | Meaning |
|---|---|
| `0` | All documents converted successfully |
| `1` | Runtime or connection failure (service unreachable, conversion error) |
| `2` | Configuration error (no service URL resolved from flag, env, or `.env`) |
