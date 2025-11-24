from typing import List, Optional
from pydantic import BaseModel, Field, validator

class BuildKnowledgeBaseResponse(BaseModel):
    message: str = Field(..., example="Knowledge base built successfully.")
    num_documents: int = Field(..., ge=0, example=5)
    num_chunks: int = Field(..., ge=0, example=100)
    vector_store: str = Field(..., example="chroma")

class TestCaseBase(BaseModel):
    test_id: str = Field(..., description="Unique identifier for the test case")
    feature: str = Field(..., description="Feature the test case covers")
    test_scenario: str = Field(..., description="Test scenario description")
    expected_result: str = Field(..., description="Expected result if test passes")
    source_document: Optional[str] = Field(
        None, description="Document name or section used as reference"
    )

    @validator("test_id", "feature", "test_scenario", "expected_result")
    def non_empty_strings(cls, v, field):
        if not v or not v.strip():
            raise ValueError(f"{field.name} must be a non-empty string")
        return v.strip()

class TestCaseGenerationRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=512, example="Generate test cases for checkout flow")
    max_test_cases: Optional[int] = Field(10, ge=1, le=50, description="Max number of test cases to generate")

class TestCaseGenerationResponse(BaseModel):
    query: str = Field(..., description="Original query text")
    test_cases: List[TestCaseBase] = Field(..., description="List of generated test cases")

class SeleniumTestCase(BaseModel):
    test_id: str = Field(..., description="Test case ID linked to the test case being scripted")
    feature: str
    test_scenario: str
    expected_result: str

    @validator("test_id", "feature", "test_scenario", "expected_result")
    def non_empty_strings(cls, v, field):
        if not v or not v.strip():
            raise ValueError(f"{field.name} must be a non-empty string")
        return v.strip()

class SeleniumScriptGenerationRequest(BaseModel):
    test_case: SeleniumTestCase = Field(..., description="Test case data to base the Selenium script on")

class SeleniumScriptGenerationResponse(BaseModel):
    test_id: str = Field(..., description="Test case ID for which script was generated")
    selenium_script: str = Field(..., description="Python Selenium script as a runnable string")

class SupportDocumentMetadata(BaseModel):
    document_id: str = Field(..., description="Unique identifier for the document")
    chunk_index: int = Field(..., description="Index of the chunk in the document")
    source_file: str = Field(..., description="Original source filename")
    text: str = Field(..., description="Chunked text content")
