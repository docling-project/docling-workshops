# Docling Lab — Information Extraction from Converted Documents

This reference describes how to extract structured fields from converted documents and use them
to fill a JSON form.

Docling for IBM watsonx does **not** yet support schema-based extraction as a service feature.
The approach is to convert the source documents to Markdown and use Bob's own reasoning to read
those Markdown files and populate the form fields.

---

<Steps>

<Step>
**Convert the source documents to Markdown.**

If the documents have not been converted yet, convert them now (see [convert.md](convert.md)).
Use `--to md --output ./output` so each document produces a `.md` file in `output/`.
</Step>

<Step>
**Read the form schema.**

Open the JSON form file the user specified. Its keys are the fields to fill; their current values
show which are empty. Treat the key names as the field identifiers — do not rename or reorder them.
</Step>

<Step>
**Read the converted Markdown files.**

Read each `.md` file in `output/` that corresponds to a source document. The Markdown faithfully
reflects the document's structure: headings are headings, table cells are table cells, lists are
lists. Rely on that structure when locating values — a number in a table row is more trustworthy
than the same number appearing in running text.
</Step>

<Step>
**Extract each field from the Markdown.**

For every field in the form, search the Markdown files for the most specific, authoritative
occurrence of that value. Apply these rules:

- Use only values stated in the documents. Do not infer or invent.
- For fields that appear in more than one document: if the values agree, use the shared value;
  if they differ, record both and flag the discrepancy.
- For list fields, extract each item as a short phrase. Use an empty list `[]` if nothing is found.
- For date fields, normalise to YYYY-MM-DD format.
- For numeric fields, return a plain number without units or formatting.
- Set any field not found in the documents to `null`.
</Step>

<Step>
**Return the filled form as JSON.**

Output a JSON object whose keys exactly match those in the form file, with the extracted values
filled in. Do not add, remove, or rename any keys.
</Step>

</Steps>
