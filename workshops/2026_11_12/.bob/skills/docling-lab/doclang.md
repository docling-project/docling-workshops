# Docling Lab — Building and Saving a DoclingDocument

This reference covers authoring a `DoclingDocument` in Python and saving it as a DocLang archive
(`.dclx`). It is about **creating and editing document structure**, not converting source files
(see [convert.md](convert.md)) and not extracting fields from converted text
(see [extraction.md](extraction.md)).

`DoclingDocument` is the in-memory document model from `docling_core`. You build it by adding
structural elements — title, headings, text blocks, tables — and then serialise it to DocLang.

---

## Imports

```python
from docling_core.types.doc import (
    DocItemLabel,
    DoclingDocument,
    TableCell,
    TableData,
)
```

---

## Create a document

```python
doc = DoclingDocument(name="my_document")
```

`name` becomes the document's identifier; it does not need a file extension.

---

## Add structural elements

Elements are appended in the order they are added, which becomes the reading order.

```python
doc.add_title(text="My Document Title")
doc.add_heading(text="Section One", level=1)
doc.add_heading(text="Subsection", level=2)
doc.add_text(label=DocItemLabel.TEXT, text="A paragraph of body text.")
```

For a caption that belongs to a table, add it first and pass it when adding the table:

```python
caption = doc.add_text(label=DocItemLabel.CAPTION, text="Table caption text")
```

---

## Add a table

Build the cells explicitly, then pass them inside a `TableData` object.

```python
def make_cell(text: str, row: int, col: int, header: bool = False) -> TableCell:
    return TableCell(
        text=text,
        start_row_offset_idx=row,
        end_row_offset_idx=row + 1,
        start_col_offset_idx=col,
        end_col_offset_idx=col + 1,
        column_header=header,
    )

# Header row + data rows
cells = [
    make_cell("Field", 0, 0, header=True),
    make_cell("Value", 0, 1, header=True),
    make_cell("entity_name", 1, 0),
    make_cell("Vantara Bank", 1, 1),
    make_cell("reporting_period", 2, 0),
    make_cell("Q3 2026", 2, 1),
]

doc.add_table(
    data=TableData(num_rows=3, num_cols=2, table_cells=cells),
    caption=caption,   # omit if there is no caption
)
```

`num_rows` includes the header row. `num_cols` must match the number of distinct column indices
used in the cells.

---

## Populate a table from a dict

When filling a two-column Field / Value table from a dictionary:

```python
data = {"entity_name": "Vantara Bank", "reporting_period": "Q3 2026"}

cells = [make_cell("Field", 0, 0, header=True), make_cell("Value", 0, 1, header=True)]
for row, (key, value) in enumerate(data.items(), start=1):
    cells += [make_cell(key, row, 0), make_cell(str(value) if value is not None else "", row, 1)]

doc.add_table(
    data=TableData(num_rows=len(data) + 1, num_cols=2, table_cells=cells),
)
```

---

## Preview as Markdown

```python
print(doc.export_to_markdown())
```

Useful for a quick sanity check before saving.

---

## Save as DocLang archive (.dclx)

```python
from pathlib import Path

doc.save_as_doclang_archive(Path("output/my_document.dclx"))
```

The `.dclx` file can be opened in the DocLang Viewer at doclang.ai/viewer.
