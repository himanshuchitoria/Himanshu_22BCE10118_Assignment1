import logging
from fastapi import HTTPException

from ..models.schemas import SeleniumScriptGenerationRequest, SeleniumScriptGenerationResponse
from ..core.rag_agent import RagAgent

logger = logging.getLogger(__name__)

async def generate_selenium_script_for_test_case(
    test_case_request: SeleniumScriptGenerationRequest,
    settings,
) -> SeleniumScriptGenerationResponse:
    """
    Generate a Selenium Python script for the provided test case by
    grounding on the stored checkout.html content and other documentation.

    Returns:
        SeleniumScriptGenerationResponse with test_id and script text.
    Raises:
        HTTPException for invalid data or generation failures.
    """

    test_case = test_case_request.test_case

    # Validate required test case fields
    if not all([
        getattr(test_case, "test_id", None),
        getattr(test_case, "feature", None),
        getattr(test_case, "test_scenario", None),
        getattr(test_case, "expected_result", None),
    ]):
        logger.error("Missing required test case fields for selenium script generation.")
        print("Missing required test case fields for selenium script generation.")
        raise HTTPException(
            status_code=400,
            detail="Test case must contain valid test_id, feature, test_scenario and expected_result fields."
        )

    rag_agent = RagAgent()

    # Read checkout.html content for grounding
    try:
        html_path = f"{settings.storage_dir}/checkout.html"
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        logger.info(f"checkout.html successfully read from: {html_path}")
        print(f"checkout.html successfully read from: {html_path}")
    except FileNotFoundError:
        logger.error("checkout.html file not found.")
        print("checkout.html file not found.")
        raise HTTPException(
            status_code=400,
            detail="checkout.html file not found. Rebuild knowledge base before generating scripts."
        )
    except Exception as e:
        logger.error(f"Failed to read checkout.html: {e}")
        print(f"Failed to read checkout.html: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error reading checkout.html."
        )

    try:
        # Generate Selenium script using real LLM via RagAgent
        selenium_script = await rag_agent.generate_selenium_script(
            test_case=test_case.dict(),
            context=html_content,
        )
        logger.info("Selenium script generated successfully.")
        print("Selenium script generated successfully.")

        # Warn if output looks like JSON rather than Python code, help debugging
        if selenium_script.strip().startswith("{") or selenium_script.strip().startswith("["):
            logger.warning("Selenium script output looks like JSON, not Python code.")
            print("Warning: Selenium script output looks like JSON, not Python code.")
    except Exception as exc:
        logger.error(f"Selenium script generation error: {exc}")
        print(f"Selenium script generation error: {exc}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate Selenium script from the test case: {exc}"
        )

    logger.info("Returned Selenium script:\n" + selenium_script)
    print("Returned Selenium script:\n" + selenium_script)

    return SeleniumScriptGenerationResponse(
        test_id=test_case.test_id,
        selenium_script=selenium_script,
    )
