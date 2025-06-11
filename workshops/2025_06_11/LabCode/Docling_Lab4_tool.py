# This is the code included in the container image
# ghrc.io/docling-project/lab-demo-docling-llamstack-mcp


from functools import lru_cache
from pathlib import Path

from docling.chunking import DocMeta, HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
)
from docling.document_converter import DocumentConverter, FormatOption, PdfFormatOption
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from llama_stack_client import LlamaStackClient
from mcp.server.fastmcp import FastMCP
from pydantic_settings import BaseSettings, SettingsConfigDict
from transformers import AutoTokenizer

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DOCLING_MCP_",
        env_file=".env",
        extra="allow",
    )

    llama_stack_url: str = "http://localhost:8321"
    vdb_embedding: str = "all-MiniLM-L6-v2"

settings = Settings()
mcp = FastMCP("Docling Documents Ingest")

@lru_cache
def get_converter() -> DocumentConverter:
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False  # Skip OCR for faster processing (enable for scanned docs)

    format_options: dict[InputFormat, FormatOption] = {
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
    }

    return DocumentConverter(format_options=format_options)


@lru_cache
def get_llama_stack_client():
    client = LlamaStackClient(
        base_url=settings.llama_stack_url,
    )
    return client


@mcp.tool()
def ingest_document_to_vectordb(source: str, vector_db_id: str):
    """
    Ingest source documents into the vector database for using them in RAG applications.

    :param source: The http source document to ingest
    :param vector_db_id: The llama stack vector_db_id
    # :returns: Filename of the file which has been ingested
    """

    print(f"{source=}")
    print(f"{vector_db_id=}")

    if source.startswith("file://"):
        source = Path(source.replace("file://", ""))
    converter = get_converter()
    result = converter.convert(source)
    doc = result.document
    print(f"{result.status=}")

    tokenizer = HuggingFaceTokenizer(
        tokenizer=AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=f"sentence-transformers/{settings.vdb_embedding}"
        )
    )
    chunker = HybridChunker(tokenizer=tokenizer)

    chunk_iter = chunker.chunk(dl_doc=doc)

    ls_chunks = []
    for i, chunk in enumerate(chunk_iter):
        meta = DocMeta.model_validate(chunk.meta)

        enriched_text = chunker.contextualize(chunk=chunk)

        token_count = tokenizer.count_tokens(enriched_text)
        chunk_dict = {
            "content": enriched_text,
            "mime_type": "text/plain",
            "metadata": {
                "document_id": f"{doc.origin.binary_hash}",
                "token_count": token_count,
                "doc_items": [item.self_ref for item in meta.doc_items],
            },
        }
        ls_chunks.append(chunk_dict)

    client = get_llama_stack_client()
    client.vector_io.insert(
        vector_db_id=vector_db_id,
        chunks=ls_chunks,
    )

    return result.input.file.name


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="sse")
