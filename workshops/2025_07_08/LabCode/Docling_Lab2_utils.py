from typing import Any

from docling.chunking import DocMeta, HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    PictureDescriptionVlmOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.transforms.chunker.hierarchical_chunker import (
    ChunkingDocSerializer,
    ChunkingSerializerProvider,
)
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from docling_core.transforms.serializer.base import (
    BaseDocSerializer,
    SerializationResult,
)
from docling_core.transforms.serializer.common import create_ser_result
from docling_core.transforms.serializer.markdown import MarkdownPictureSerializer
from docling_core.types.doc import DoclingDocument
from docling_core.types.doc.document import PictureDescriptionData, PictureItem
from llama_stack_client import LlamaStackClient
from transformers import AutoTokenizer
from typing_extensions import override


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
            pretrained_model_name_or_path=f"sentence-transformers/{vdb_embedding}"
        )
    )
    chunker = HybridChunker(tokenizer=tokenizer)

    for doc in docs:
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
    class AnnotationPictureSerializer(MarkdownPictureSerializer):
        @override
        def serialize(
            self,
            *,
            item: PictureItem,
            doc_serializer: BaseDocSerializer,
            doc: DoclingDocument,
            **kwargs: Any,
        ) -> SerializationResult:
            text_parts: list[str] = []
            parent_res = super().serialize(
                item=item,
                doc_serializer=doc_serializer,
                doc=doc,
                **kwargs,
            )
            text_parts.append(parent_res.text)
            for annotation in item.annotations:
                if isinstance(annotation, PictureDescriptionData):
                    text_parts.append(f"Picture description: {annotation.text}")

            text_res = "\n".join(text_parts)
            return create_ser_result(text=text_res, span_source=item)

    class ImgAnnotationSerializerProvider(ChunkingSerializerProvider):
        def get_serializer(self, doc: DoclingDocument):
            return ChunkingDocSerializer(
                doc=doc,
                picture_serializer=AnnotationPictureSerializer(),  # configuring a different picture serializer
            )

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
            prompt="Describe this image in a few sentences.",
        ),
        ######################
        # using a remote VLM #
        ######################
        # picture_description_options=PictureDescriptionApiOptions(
        #     url="https://smolvlm-256m-instruct-llama-serve.drl-masterclass-9ca4d14d48413d18ce61b80811ba4308-0000.eu-de.containers.appdomain.cloud/v1/chat/completions",
        #     # url="https://granite-vision-32-2b-llama-serve.drl-masterclass-9ca4d14d48413d18ce61b80811ba4308-0000.eu-de.containers.appdomain.cloud/v1/chat/completions",
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
            pretrained_model_name_or_path=f"sentence-transformers/{vdb_embedding}"
        )
    )

    chunker = HybridChunker(
        tokenizer=tokenizer,
        serializer_provider=ImgAnnotationSerializerProvider(),
    )

    for doc in docs:
        chunk_iter = chunker.chunk(dl_doc=doc)
        dl_chunks = list(chunk_iter)

        ls_chunks = []
        for i, chunk in enumerate(dl_chunks):
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
            pretrained_model_name_or_path=f"sentence-transformers/{vdb_embedding}"
        )
    )
    chunker = HybridChunker(tokenizer=tokenizer)

    for doc in docs:
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

    client.vector_io.insert(
        vector_db_id=vector_db_id,
        chunks=ls_chunks,
    )

    return docs
