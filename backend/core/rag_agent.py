import logging
from typing import List, Dict, Any
import json
import os
from dotenv import load_dotenv

# --- LEGACY IMPORT ---
import google.generativeai as genai 

from ..core.embedding_manager import get_embedding_manager
from ..core.vector_store import VectorStore

logger = logging.getLogger(__name__)

# Load GEMINI_API_KEY from .env or environment automatically
load_dotenv()

class RagAgent:
    """
    Retrieval-Augmented Generation (RAG) agent using Google Gemini LLM for
    test case and Selenium script generation grounded on retrieved context.
    """

    def __init__(self):
        self.vector_store = VectorStore()
        self.embedding_manager = get_embedding_manager()
        
        # --- FIX: Configure globally for Legacy SDK ---
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        # --- FIX: Instantiate model directly (Legacy Style) ---
        # 'gemini-pro' is the standard text model for this SDK version.
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    async def _call_gemini_api(self, prompt: str) -> str:
        """
        Calls Gemini generative model using google-generativeai (legacy) with async wrapper.
        """
        try:
            # The legacy generate_content is synchronous, so we wrap it.
            from asyncio import get_running_loop
            loop = get_running_loop()
            
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(prompt)
            )
            return response.text
            
        except Exception as ex:
            logger.error(f"Gemini API call failed: {ex}")
            raise RuntimeError(f"Gemini LLM call failed: {ex}")

    @staticmethod
    async def generate_embedding(text: str) -> List[float]:
        embedding_manager = get_embedding_manager()
        embeddings = await embedding_manager.embed_texts([text])
        if embeddings and len(embeddings) == 1:
            return embeddings[0]
        else:
            raise RuntimeError("Embedding generation failed or returned unexpected result.")

    async def generate_test_cases(self, query: str, context: str) -> List[Dict[str, Any]]:
        prompt = self._build_test_case_prompt(query, context)
        llm_response_text = await self._call_gemini_api(prompt)

        try:
            # Clean up potential markdown formatting from LLM (e.g. ```json ... ```)
            cleaned_text = llm_response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            
            test_cases = json.loads(cleaned_text)
            
            if not isinstance(test_cases, list):
                # Sometimes LLMs wrap the list in a dict like {"test_cases": [...]}
                if isinstance(test_cases, dict) and "test_cases" in test_cases:
                    test_cases = test_cases["test_cases"]
                else:
                    raise ValueError("Expected list of test cases JSON.")
                    
        except Exception as ex:
            logger.error(f"Failed to parse Gemini output JSON: {ex}")
            logger.error(f"Raw response: {llm_response_text}")
            raise RuntimeError("Invalid JSON output from Gemini LLM.")

        return test_cases

    async def generate_selenium_script(self, test_case: Dict[str, Any], context: str) -> str:
        prompt = self._build_selenium_script_prompt(test_case, context)
        llm_response_text = await self._call_gemini_api(prompt)
        
        # Clean up markdown code blocks if present
        cleaned_text = llm_response_text.strip()
        if cleaned_text.startswith("```python"):
            cleaned_text = cleaned_text[9:]
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
            
        return cleaned_text.strip()

    def _build_test_case_prompt(self, query: str, context: str) -> str:
        return f"""
You are an expert QA engineer. Based strictly on the following project documentation and HTML content, generate a detailed JSON list of test cases.

DOCUMENTATION CONTEXT:
\"\"\"
{context}
\"\"\"

TASK:
Generate JSON list of test cases focusing on: "{query}"

Each test case must include: test_id, feature, test_scenario, expected_result, source_document.

Do NOT add any features not found in the context.
Respond ONLY with valid JSON.
""".strip()

    def _build_selenium_script_prompt(self, test_case: Dict[str, Any], html_context: str) -> str:
        return f"""
You are a QA automation engineer. Create a full Python Selenium script implementing this test case:

TEST CASE:
test_id: {test_case.get('test_id')}
feature: {test_case.get('feature')}
test_scenario: {test_case.get('test_scenario')}
expected_result: {test_case.get('expected_result')}

HTML CONTEXT:
\"\"\"
{html_context}
\"\"\"

Produce runnable Python Selenium WebDriver code with accurate selectors based only on the above HTML.
Respond ONLY with the code, no explanations.
""".strip()