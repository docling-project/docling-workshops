# Docling Lab — Querying DocLang Files with dclq

`dclq` lets you inspect, outline, search, and extract content from `.dclx` files without an LLM.
It is installed in the virtual environment alongside `docling`. All commands take a `.dclx` file
as their last argument.

To produce `.dclx` files, add `--to dclx` to `docling convert-remote` (see [options.md](options.md)).

### Inspect — count structural elements

```bash
dclq inspect output/document.dclx
```

Prints a summary: number of headings, paragraphs, tables, pictures, and furniture items (page
headers and footers that are not part of the content).

---

### Outline — heading tree with XPath addresses

```bash
dclq outline output/document.dclx
```

Prints every heading in reading order with the XPath that addresses it, for example:

```
/heading[1]   Introduction
  /heading[2]   Background
  /heading[2]   Scope
```

Use the XPath in `dclq show` to retrieve that section's content.

---

### Grep — search for text

```bash
dclq grep -i 'search term' output/document.dclx
```

`-i` makes the search case-insensitive. Returns every element whose text contains the pattern,
with its XPath address.

---

### Show — retrieve a section

```bash
dclq show output/document.dclx '/heading[2]' --section --max-chars 800
```

`--section` includes the heading's entire subtree (all paragraphs and tables nested under it), not
just the heading line itself. `--max-chars` limits the output length.

---

### List — filter by element type

```bash
dclq list output/document.dclx --type table_cell --page 1
```

Lists all elements of a given type. Useful types: `heading`, `paragraph`, `table`, `table_cell`,
`picture`, `list_item`.

---

## Typical workflow

```bash
# Convert and export (see options.md for --to dclx)
docling convert-remote --to md --to dclx --output ./output my_file.pdf

# Then inspect and outline
dclq inspect output/my_file.dclx
dclq outline output/my_file.dclx
```
