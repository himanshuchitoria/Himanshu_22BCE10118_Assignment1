import os
import uuid
from typing import List
from fastapi import UploadFile, HTTPException
import aiofiles
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter

from ..models.schemas import SupportDocumentMetadata, BuildKnowledgeBaseResponse
from ..utils.utils import save_uploaded_file, parse_pdf, parse_json, parse_html
from ..core.embedding_manager import generate_embeddings
from ..core.vector_store import VectorStore

logger = logging.getLogger(__name__)

async def ingest_support_documents(
    files: List[UploadFile],
    storage_dir: str
) -> List[SupportDocumentMetadata]:
    """
    Handles ingestion pipeline for support documents, validating types,
    parsing content, chunking, embedding, and storing in vector DB.
    Returns metadata about stored chunks for later retrieval.
    """
    logger.info("Starting support document ingestion.")
    print("Starting support document ingestion.")

    support_metadata: List[SupportDocumentMetadata] = []
    vector_store = VectorStore()

    for file in files:
        file_path = await save_uploaded_file(file, storage_dir)
        logger.info(f"File saved: {file_path}")
        print(f"File saved: {file_path}")

        ext = os.path.splitext(file.filename)[1].lower()
        logger.info(f"Detected extension: {ext}")
        print(f"Detected extension: {ext}")

        try:
            if ext == ".pdf":
                content = await parse_pdf(file_path)
            elif ext == ".json":
                content = await parse_json(file_path)
            elif ext in {".txt", ".md"}:
                async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                    content = await f.read()
            elif ext in {".html", ".htm"}:
                content = await parse_html(file_path)
            else:
                logger.error(f"Unsupported file type: {ext} for {file.filename}")
                print(f"Unsupported file type: {ext} for {file.filename}")
                raise HTTPException(
                    status_code=415,
                    detail=f"Unsupported file type: {ext} for file {file.filename}",
                )
        except HTTPException:
            raise
        except Exception as exc:
            logger.error(f"Error parsing file {file.filename}: {exc}")
            print(f"Error parsing file {file.filename}: {exc}")
            raise HTTPException(
                status_code=500,
                detail=f"Error parsing file {file.filename}: {exc}",
            )

        logger.info(f"File parsed successfully: {file.filename}")
        print(f"File parsed successfully: {file.filename}")

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(content)
        logger.info(f"Generated {len(chunks)} text chunks for {file.filename}")
        print(f"Generated {len(chunks)} text chunks for {file.filename}")

        try:
            embeddings = await generate_embeddings(chunks)
            logger.info(f"Embeddings generated for {file.filename}")
            print(f"Embeddings generated for {file.filename}")
        except Exception as exc:
            logger.error(f"Embedding generation failed for {file.filename}: {exc}")
            print(f"Embedding generation failed for {file.filename}: {exc}")
            raise HTTPException(
                status_code=500,
                detail=f"Embedding generation failed for {file.filename}: {exc}",
            )

        doc_id = str(uuid.uuid4())
        for i, chunk in enumerate(chunks):
            metadata = {
                "document_id": doc_id,
                "chunk_index": i,
                "source_file": file.filename,
                "text": chunk,
            }
            await vector_store.add_vector(embedding=embeddings[i], metadata=metadata)
            logger.info(f"Added chunk {i} to vector store for {file.filename}")
            print(f"Added chunk {i} to vector store for {file.filename}")
            support_metadata.append(SupportDocumentMetadata(**metadata))

    logger.info(f"Support document ingestion complete. Total chunks: {len(support_metadata)}")
    print(f"Support document ingestion complete. Total chunks: {len(support_metadata)}")
    return support_metadata

async def ingest_checkout_html(
    checkout_file: UploadFile,
    storage_dir: str,
    filename: str = "checkout.html"
) -> str:
    """
    Handles ingestion of the checkout.html file.
    Saves the file to the storage_dir. No chunking or embeddings needed.
    Returns path to saved file for further use.
    """
    logger.info("Starting checkout.html ingestion.")
    print("Starting checkout.html ingestion.")
    try:
        # Always save as checkout.html, overwrite if exists
        dest_path = os.path.join(storage_dir, filename)
        if os.path.exists(dest_path):
            os.remove(dest_path)
        # Read and write the uploaded file directly to dest_path
        async with aiofiles.open(dest_path, 'wb') as out_file:
            content = await checkout_file.read()
            if not content:
                logger.error("Uploaded checkout.html is empty")
                print("Uploaded checkout.html is empty")
                raise HTTPException(status_code=400, detail="Uploaded checkout.html is empty")
            await out_file.write(content)
        await checkout_file.close()
        logger.info(f"Checkout HTML saved at {dest_path}")
        print(f"Checkout HTML saved at {dest_path}")
        return dest_path
    except Exception as exc:
        logger.error(f"Failed to save checkout.html: {exc}")
        print(f"Failed to save checkout.html: {exc}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save checkout.html: {exc}",
        )

async def rebuild_vector_store(
    support_docs_metadata: List[SupportDocumentMetadata],
    checkout_html_path: str,
    settings=None
) -> BuildKnowledgeBaseResponse:
    """
    Example placeholder implementation.
    Reads metadata and checkout HTML path, re-processes as needed,
    and returns BuildKnowledgeBaseResponse stats.
    """
    logger.info("Rebuilding vector store.")
    print("Rebuilding vector store.")
    logger.info(f"Support docs metadata length: {len(support_docs_metadata)}")
    print(f"Support docs metadata length: {len(support_docs_metadata)}")
    logger.info(f"Checkout HTML path: {checkout_html_path}")
    print(f"Checkout HTML path: {checkout_html_path}")

    # Mock statistics for demonstration
    num_documents = len(support_docs_metadata)
    num_chunks = sum([1 for _ in support_docs_metadata])
    vector_store_name = "chroma"

    logger.info(f"Returning BuildKnowledgeBaseResponse: num_documents={num_documents}, num_chunks={num_chunks}, vector_store={vector_store_name}")
    print(f"Returning BuildKnowledgeBaseResponse: num_documents={num_documents}, num_chunks={num_chunks}, vector_store={vector_store_name}")

    return BuildKnowledgeBaseResponse(
        message="Knowledge base rebuilt.",
        num_documents=num_documents,
        num_chunks=num_chunks,
        vector_store=vector_store_name,
    )
