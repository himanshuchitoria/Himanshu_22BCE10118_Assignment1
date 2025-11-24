import logging
from typing import List
from fastapi import HTTPException

from ..core.vector_store import VectorStore
from ..core.rag_agent import RagAgent
from ..models.schemas import TestCaseGenerationResponse, TestCaseBase

logger = logging.getLogger(__name__)

async def generate_test_cases_for_query(
    query: str,
    max_test_cases: int,
    settings
) -> TestCaseGenerationResponse:
    """
    Generate test cases for a given query using:
    - Vector similarity search to retrieve relevant document chunks.
    - LLM prompt via RagAgent to create structured, grounded test cases.
    """

    if max_test_cases < 1 or max_test_cases > 50:
        raise HTTPException(
            status_code=400,
            detail="max_test_cases must be between 1 and 50."
        )

    vector_store = VectorStore()

    try:
        # Instantiate RagAgent (real Gemini LLM integration inside RagAgent)
        agent = RagAgent()
        logger.info("RagAgent instance created.")
        print("RagAgent instance created.")

        # Generate embedding vector representation of query
        query_embedding = await agent.generate_embedding(query)
        logger.info("Query embedding generated.")
        print("Query embedding generated.")

        # Retrieve top-k relevant document chunks for richer context
        top_k = min(max_test_cases * 3, 20)
        relevant_chunks = await vector_store.similarity_search(query_embedding, top_k)
        logger.info(f"{len(relevant_chunks)} relevant chunks retrieved from vector store.")
        print(f"{len(relevant_chunks)} relevant chunks retrieved from vector store.")

        if not relevant_chunks:
            logger.warning("No relevant documents found for the query.")
            print("No relevant documents found for the query.")
            raise HTTPException(
                status_code=404,
                detail="No relevant documents found for the query."
            )
    except Exception as exc:
        logger.error(f"Vector search failed: {exc}")
        print(f"Vector search failed: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Vector retrieval failed."
        )

    # Combine text chunks to form prompt context for LLM
    context_text = "\n\n".join(chunk["metadata"]["text"] for chunk in relevant_chunks)

    try:
        # Use RagAgent's Gemini-backed LLM to generate structured test cases
        test_cases_raw = await agent.generate_test_cases(query=query, context=context_text)
        logger.info("Test case generation completed via agent.")
        print("Test case generation completed via agent.")

        test_cases = []
        for entry in test_cases_raw:
            try:
                test_case = TestCaseBase(
                    test_id=entry.get("test_id"),
                    feature=entry.get("feature"),
                    test_scenario=entry.get("test_scenario"),
                    expected_result=entry.get("expected_result"),
                    source_document=entry.get("source_document", None)
                )
                test_cases.append(test_case)
            except Exception as ex:
                logger.warning(f"Invalid test case entry skipped: {ex}")
                print(f"Invalid test case entry skipped: {ex}")
                continue

        # Limit results to max_test_cases
        if len(test_cases) > max_test_cases:
            test_cases = test_cases[:max_test_cases]

        if not test_cases:
            logger.warning("No valid test cases generated.")
            print("No valid test cases generated.")
            raise HTTPException(status_code=404, detail="No valid test cases generated.")
    except Exception as exc:
        logger.error(f"LLM generation failed: {exc}")
        print(f"LLM generation failed: {exc}")
        raise HTTPException(status_code=500, detail=f"Test case generation failed: {exc}")

    logger.info(f"Returning {len(test_cases)} test cases for query '{query}'.")
    print(f"Returning {len(test_cases)} test cases for query '{query}'.")

    return TestCaseGenerationResponse(query=query, test_cases=test_cases)
