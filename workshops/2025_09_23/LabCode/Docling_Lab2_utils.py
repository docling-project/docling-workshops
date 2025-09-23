import uuid
from typing import Any, Literal, Union

from docling.chunking import DocMeta, HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    PictureDescriptionVlmOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from docling_core.types.doc import DoclingDocument
from docling_core.transforms.chunker.hierarchical_chunker import (
    ChunkingDocSerializer,
    ChunkingSerializerProvider,
)
from docling_core.transforms.serializer.markdown import MarkdownTableSerializer
from llama_stack_client import LlamaStackClient, RAGDocument
from llama_stack_client.types import QueryChunksResponse, QueryResult
from llama_stack_client.types.vector_io_insert_params import Chunk, ChunkChunkMetadata
from pydantic import NonNegativeFloat
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console
from transformers import AutoTokenizer

class Settings(BaseSettings):
    base_url: str

    vdb_provider: str
    vdb_embedding: str
    vdb_embedding_dimension: int
    vdb_embedding_window: int

    inference_model_id: str
    max_tokens: int
    temperature: NonNegativeFloat
    top_p: float
    stream: bool

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def answer_with_rag(
    *,
    client: LlamaStackClient,
    vector_db_id: str,
    sampling_params: dict[str, Any],
    queries: list[str],
    inference_model_id=str,
    stream: bool,
    console: Console,
    mode: Literal["rag_tool", "vector_io"] = "rag_tool",
) -> Union[list[QueryChunksResponse], list[QueryResult]]:
    all_responses = []
    for prompt in queries:
        console.print(f"[cyan]\nUser> {prompt}[/cyan]")

        # RAG retrieval call
        if mode == "rag_tool":
            retr_response = client.tool_runtime.rag_tool.query(
                content=prompt, vector_db_ids=[vector_db_id]
            )
            prompt_context = "".join((c.text for c in retr_response.content))
        elif mode == "vector_io":
            retr_response = client.vector_io.query(
                vector_db_id=vector_db_id,
                query=prompt,
            )
            prompt_context = "\n".join([c.content for c in retr_response.chunks])
        else:
            raise ValueError(f"Unknown mode: {mode}")
        all_responses.append(retr_response)

        # the list of messages to be sent to the model must start with the system prompt
        messages = [{"role": "system", "content": "You are a helpful assistant."}]

        # construct the actual prompt to be executed, incorporating the original query and the retrieved content
        extended_prompt = f"Please answer the given query using the context below.\n\nCONTEXT:\n{prompt_context}\n\nQUERY:\n{prompt}"
        messages.append({"role": "user", "content": extended_prompt})

        # use Llama Stack inference API to directly communicate with the desired model
        response = client.chat.completions.create(
            messages=messages,
            model=inference_model_id,
            stream=stream,
            **sampling_params,
        )

        # print the response
        text = "inference> "
        for chunk in response:
            if (
                hasattr(chunk.choices[0], "delta")
                and chunk.choices[0].delta.content
            ):
                text += chunk.choices[0].delta.content

            elif (
                hasattr(chunk.choices[0], "text") and chunk.choices[0].text.content
            ):
                text += chunk.choices[0].text.content
        console.print(f"[yellow]{text}[/yellow]")

    return all_responses


def ingest_with_default_rag_tool(
    *,
    client: LlamaStackClient,
    vector_db_id: str,
    urls: list[str],
    vdb_embedding_window: int,
) -> None:
    # ingest the documents into the newly created document collection
    my_urls = [(url, "application/pdf") for url in urls]
    documents = [
        RAGDocument(
            document_id=f"num-{i}",
            content={"uri": url},
            mime_type=url_type,
            metadata={},
        )
        for i, (url, url_type) in enumerate(my_urls)
    ]
    client.tool_runtime.rag_tool.insert(
        documents=documents,
        vector_db_id=vector_db_id,
        chunk_size_in_tokens=vdb_embedding_window,
    )


class MDTableSerializerProvider(ChunkingSerializerProvider):
    def get_serializer(self, doc):
        return ChunkingDocSerializer(
            doc=doc,
            table_serializer=MarkdownTableSerializer(),  # configuring a different table serializer
        )


def ingest_with_docling(
    *,
    client: LlamaStackClient,
    vector_db_id: str,
    urls: list[str],
    vdb_embedding: str,
) -> None:
    converter = DocumentConverter()
    docs = [converter.convert(source=url).document for url in urls]

    tokenizer = HuggingFaceTokenizer(
        tokenizer=AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=f"{vdb_embedding}"
        )
    )
    # chunker = HybridChunker(tokenizer=tokenizer, serializer_provider=MDTableSerializerProvider())
    chunker = HybridChunker(tokenizer=tokenizer)

    for doc in docs:
        chunk_iter = chunker.chunk(dl_doc=doc)
        doc_id = (
            str(doc.origin.binary_hash) if doc.origin is not None else str(uuid.uuid4())
        )

        ls_chunks = []
        for i, chunk in enumerate(chunk_iter):
            meta = DocMeta.model_validate(chunk.meta)
            chunk_id = f"{doc_id}-{i:05d}"

            enriched_text = chunker.contextualize(chunk=chunk)

            token_count = tokenizer.count_tokens(enriched_text)
            metadata = {
                "document_id": doc_id,
                "chunk_id": chunk_id,
                "token_count": token_count,
                "doc_items": [item.self_ref for item in meta.doc_items],
            }
            chunk_metadata: ChunkChunkMetadata = {
                "document_id": doc_id,
                "chunk_id": chunk_id,
                "content_token_count": token_count,
            }
            chunk_dict: Chunk = {
                "content": enriched_text,
                "metadata": metadata,
                "chunk_metadata": chunk_metadata,
            }
            ls_chunks.append(chunk_dict)

    client.vector_io.insert(
        vector_db_id=vector_db_id,
        chunks=ls_chunks,
    )


def ingest_with_docling_with_annotations(
    *,
    client: LlamaStackClient,
    vector_db_id: str,
    urls: list[str],
    vdb_embedding: str,
) -> None:
    pipeline_options = PdfPipelineOptions(
        do_picture_description=True,
        generate_picture_images=True,
        images_scale=2,
        enable_remote_services=True,
        #####################
        # using a local VLM #
        #####################
        picture_description_options=PictureDescriptionVlmOptions(
            repo_id="HuggingFaceTB/SmolVLM-256M-Instruct",
            # repo_id="ibm-granite/granite-vision-3.2-2b",
            prompt="Describe this image in a few sentences. When the image is a diagram describe it in more details including the name of the boxes and their relationships.",
        ),
        ######################
        # using a remote VLM #
        ######################
        # picture_description_options=PictureDescriptionApiOptions(
        #     url="https://host/v1/chat/completions",
        #     params={
        #         "model": "smolvlm-256m-instruct",
        #         # "model": "granite-vision-32-2b",
        #         "seed": 42,
        #         "max_completion_tokens": 200,
        #     },
        #     prompt="Describe this image in a few sentences.",
        #     # timeout=20,
        # ),
    )

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    docs = [converter.convert(source=url).document for url in urls]

    tokenizer = HuggingFaceTokenizer(
        tokenizer=AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=f"{vdb_embedding}"
        )
    )

    chunker = HybridChunker(
        tokenizer=tokenizer,
    )

    for doc in docs:
        doc_id = (
            str(doc.origin.binary_hash) if doc.origin is not None else str(uuid.uuid4())
        )
        chunk_iter = chunker.chunk(dl_doc=doc)
        dl_chunks = list(chunk_iter)

        ls_chunks = []
        for i, chunk in enumerate(dl_chunks):
            meta = DocMeta.model_validate(chunk.meta)
            chunk_id = f"{doc_id}-{i:05d}"

            enriched_text = chunker.contextualize(chunk=chunk)

            token_count = tokenizer.count_tokens(enriched_text)
            metadata = {
                "document_id": doc_id,
                "chunk_id": chunk_id,
                "token_count": token_count,
                "doc_items": [item.self_ref for item in meta.doc_items],
            }
            chunk_metadata: ChunkChunkMetadata = {
                "document_id": doc_id,
                "chunk_id": chunk_id,
                "content_token_count": token_count,
            }
            chunk_dict: Chunk = {
                "content": enriched_text,
                "metadata": metadata,
                "chunk_metadata": chunk_metadata,
            }
            ls_chunks.append(chunk_dict)

    client.vector_io.insert(
        vector_db_id=vector_db_id,
        chunks=ls_chunks,
    )


def ingest_with_docling_for_visual_grounding(
    *,
    client: LlamaStackClient,
    vector_db_id: str,
    urls: list[str],
    vdb_embedding: str,
) -> list[DoclingDocument]:
    pipeline_options = PdfPipelineOptions()
    pipeline_options.generate_page_images = True
    pipeline_options.images_scale = 2

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    docs = [converter.convert(source=url).document for url in urls]

    tokenizer = HuggingFaceTokenizer(
        tokenizer=AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=f"{vdb_embedding}"
        )
    )
    chunker = HybridChunker(tokenizer=tokenizer)

    for doc in docs:
        doc_id = (
            str(doc.origin.binary_hash) if doc.origin is not None else str(uuid.uuid4())
        )
        chunk_iter = chunker.chunk(dl_doc=doc)

        ls_chunks = []
        for i, chunk in enumerate(chunk_iter):
            meta = DocMeta.model_validate(chunk.meta)
            chunk_id = f"{doc_id}-{i:05d}"

            enriched_text = chunker.contextualize(chunk=chunk)

            token_count = tokenizer.count_tokens(enriched_text)
            metadata = {
                "document_id": doc_id,
                "chunk_id": chunk_id,
                "token_count": token_count,
                "doc_items": [item.self_ref for item in meta.doc_items],
            }
            chunk_metadata: ChunkChunkMetadata = {
                "document_id": doc_id,
                "chunk_id": chunk_id,
                "content_token_count": token_count,
            }
            chunk_dict: Chunk = {
                "content": enriched_text,
                "metadata": metadata,
                "chunk_metadata": chunk_metadata,
            }
            ls_chunks.append(chunk_dict)

    client.vector_io.insert(
        vector_db_id=vector_db_id,
        chunks=ls_chunks,
    )

    return docs
