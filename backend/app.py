import logging
import os
from typing import List

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api.ingestion import (
    ingest_support_documents,
    ingest_checkout_html,
    rebuild_vector_store,
)
from .api.testcase_generation import generate_test_cases_for_query
from .api.selenium_script_gen import generate_selenium_script_for_test_case
from .models.schemas import (
    BuildKnowledgeBaseResponse,
    TestCaseGenerationRequest,
    TestCaseGenerationResponse,
    SeleniumScriptGenerationRequest,
    SeleniumScriptGenerationResponse,
)
from .config import Settings, get_settings

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

app = FastAPI(
    title="Autonomous QA Agent",
    description=(
        "Backend API for an autonomous QA agent that ingests project documentation, "
        "builds a testing brain (vector DB), generates test cases, and produces "
        "Selenium Python scripts."
    ),
    version="1.0.0",
)

# ---------------------------
# CORS & Middleware
# ---------------------------
origins = os.getenv("ALLOWED_ORIGINS", "*")
if origins == "*":
    allowed_origins = ["*"]
else:
    allowed_origins = [o.strip() for o in origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_global_exception_handling(request, call_next):
    """
    Global safety net so unexpected exceptions do not crash the server and always
    return a structured JSON error. Logs full traceback for debugging.
    """
    try:
        response = await call_next(request)
        return response
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unhandled server error: %s", exc)
        print(f"GLOBAL EXCEPTION: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error. Please check logs for details. Exception: {exc}"},
        )

# ---------------------------
# Health & Utility Endpoints
# ---------------------------

@app.get("/health", tags=["system"])
async def health_check():
    logger.info("Health check called.")
    print("Health check called.")
    return {"status": "ok"}

# ---------------------------
# Phase 1: Ingestion & KB Build
# ---------------------------

@app.post(
    "/build-knowledge-base",
    response_model=BuildKnowledgeBaseResponse,
    tags=["ingestion"],
)
async def build_knowledge_base(
    support_docs: List[UploadFile] = File(..., description="3–5 support documents"),
    checkout_html: UploadFile = File(..., description="checkout.html file"),
    settings: Settings = Depends(get_settings),
):
    logger.info("build_knowledge_base endpoint called")
    print("build_knowledge_base endpoint called")

    if not support_docs:
        logger.error("No support documents provided")
        print("No support documents provided")
        raise HTTPException(status_code=400, detail="At least one support document is required.")

    allowed_doc_exts = {".md", ".txt", ".json", ".pdf"}
    allowed_html_exts = {".html", ".htm"}

    def validate_upload(file: UploadFile, allowed_exts: set, logical_name: str):
        name = file.filename or ""
        _, ext = os.path.splitext(name.lower())
        if ext not in allowed_exts:
            logger.error(f"Invalid file type for {logical_name}: {name}. Allowed: {sorted(allowed_exts)}")
            print(f"Invalid file type for {logical_name}: {name}. Allowed: {sorted(allowed_exts)}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type for {logical_name}: {name}. Allowed: {sorted(allowed_exts)}",
            )

    for doc in support_docs:
        validate_upload(doc, allowed_doc_exts, "support_docs")
    validate_upload(checkout_html, allowed_html_exts, "checkout_html")

    try:
        logger.info("Starting ingestion of support documents.")
        print("Starting ingestion of support documents.")
        support_docs_metadata = await ingest_support_documents(
            support_docs, storage_dir=settings.storage_dir
        )
        logger.info(f"Support documents metadata: {support_docs_metadata}")
        print(f"Support documents metadata: {support_docs_metadata}")

        logger.info("Starting ingestion of checkout HTML.")
        print("Starting ingestion of checkout HTML.")
        checkout_meta = await ingest_checkout_html(
            checkout_html, storage_dir=settings.storage_dir
        )
        logger.info(f"Checkout HTML file path: {checkout_meta}")
        print(f"Checkout HTML file path: {checkout_meta}")

        logger.info("Rebuilding vector store from ingested content.")
        print("Rebuilding vector store from ingested content.")
        stats = await rebuild_vector_store(
            support_docs_metadata, checkout_meta, settings=settings
        )
        logger.info(f"Rebuild vector store stats: {stats}")
        print(f"Rebuild vector store stats: {stats}")

        if not isinstance(stats, BuildKnowledgeBaseResponse):
            logger.error(f"rebuild_vector_store did not return BuildKnowledgeBaseResponse, got {type(stats)}")
            print(f"rebuild_vector_store did not return BuildKnowledgeBaseResponse, got {type(stats)}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal error: rebuild_vector_store did not return the correct type."
            )

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to build knowledge base: %s", exc)
        print(f"Failed to build knowledge base exception: {exc}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to build knowledge base. Exception: {exc}",
        )

    return BuildKnowledgeBaseResponse(
        message="Knowledge base built successfully.",
        num_documents=stats.num_documents,
        num_chunks=stats.num_chunks,
        vector_store=stats.vector_store,
    )

# ---------------------------
# Phase 2: Test Case Generation
# ---------------------------

@app.post(
    "/generate-test-cases",
    response_model=TestCaseGenerationResponse,
    tags=["test-cases"],
)
async def generate_test_cases(
    payload: TestCaseGenerationRequest,
    settings: Settings = Depends(get_settings),
):
    logger.info(f"Generate test cases called with query='{payload.query}' and max_test_cases={payload.max_test_cases}")
    print(f"Generate test cases called with query='{payload.query}' and max_test_cases={payload.max_test_cases}")

    query = payload.query.strip()
    if not query:
        logger.error("Empty query for test case generation")
        print("Empty query for test case generation")
        raise HTTPException(status_code=400, detail="Query must not be empty.")

    try:
        response = await generate_test_cases_for_query(
            query=query,
            max_test_cases=payload.max_test_cases,
            settings=settings,
        )
        logger.info(f"Test case generation response: {response}")
        print(f"Test case generation response: {response}")
    except FileNotFoundError as exc:
        logger.warning(f"Vector store missing when generating test cases: {exc}")
        print(f"Vector store missing when generating test cases: {exc}")
        raise HTTPException(
            status_code=400,
            detail="Knowledge base not found. Please build the knowledge base first.",
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error during test case generation: %s", exc)
        print(f"Error during test case generation: {exc}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate test cases. Exception: {exc}",
        )

    return response

# ---------------------------
# Phase 3: Selenium Script Generation
# ---------------------------

@app.post(
    "/generate-selenium-script",
    response_model=SeleniumScriptGenerationResponse,
    tags=["selenium"],
)
async def generate_selenium_script(
    payload: SeleniumScriptGenerationRequest,
    settings: Settings = Depends(get_settings),
):
    logger.info(f"Generate selenium script for test case={payload.test_case}")
    print(f"Generate selenium script for test case={payload.test_case}")

    if not payload.test_case or not payload.test_case.test_id:
        logger.error("test_case with a valid test_id is required")
        print("test_case with a valid test_id is required")
        raise HTTPException(status_code=400, detail="test_case with a valid test_id is required.")

    try:
        response = await generate_selenium_script_for_test_case(
            test_case_request=payload,
            settings=settings,
        )
        logger.info(f"Selenium script generation response: {response}")
        print(f"Selenium script generation response: {response}")
    except FileNotFoundError:
        logger.error("Required assets not found for selenium script generation")
        print("Required assets not found for selenium script generation")
        raise HTTPException(
            status_code=400,
            detail="Required assets (checkout.html and/or vector store) not found. Rebuild knowledge base.",
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error during Selenium script generation: %s", exc)
        print(f"Error during Selenium script generation: {exc}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate Selenium script. Exception: {exc}",
        )

    return response
