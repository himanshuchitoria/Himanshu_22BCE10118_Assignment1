# Autonomous QA Agent

## Project Overview

The Autonomous QA Agent is an intelligent backend system that automates software quality assurance by ingesting project documentation and a target checkout HTML page. It generates detailed, documentation-grounded test cases and produces Python Selenium scripts for UI automation testing. Leveraging a vector search-enabled knowledge base and Google Gemini Large Language Model, the system ensures all test cases and scripts are based strictly on provided inputs, eliminating hallucinations.

The backend is built with FastAPI for asynchronous API services, integrates with a vector database for semantic retrieval, and uses Google Gemini AI for natural language and code generation. An optional Streamlit front end provides an intuitive user interface.

---

## Features

- **Support Document Ingestion:** Upload diverse documentation formats (.md, .txt, .json, .pdf) describing product features, UI/UX guidelines, and APIs.
- **Checkout HTML Processing:** Upload a single-page checkout HTML document to ground UI selectors.
- **Vector Database Construction:** Parses and indexes content into chunks with embeddings for efficient semantic similarity search.
- **Test Case Generation:** Generates JSON-structured, detailed test cases based on user queries and retrieved context.
- **Selenium Script Generation:** Produces complete, runnable Python Selenium WebDriver scripts precisely matching test scenarios and page HTML.
- **Strict Grounding:** Prompts enforce strict reasoning only over uploaded documents and HTML content—no artificial or hallucinated content.
- **Robust, Async Architecture:** Async FastAPI endpoints with extensive logging, error handling, and modular separation.
- **Streamlit UI:** User-friendly interface to manage ingestion, test case creation, and automation script generation.

---

## Architecture

User Queries + Uploaded Docs/HTML
↓
Ingestion & Chunking → Vector Embeddings → Vector Database
↓ ↑
Retrieval-Augmented Generation with Google Gemini LLM
↓
+----------------+ +----------------+
| Generated Test | → | Generated |
| Cases (JSON) | | Selenium Scripts|
+----------------+ +----------------+
↓ ↓
API Endpoints Streamlit UI
(FastAPI Backend)



---

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Google Cloud Project with Gemini API and API key for free tier
- Chrome browser and ChromeDriver version-compatible with Chrome installed
- Virtual environment recommended

### Installation and Running

1. Clone the repository:
git clone <repo-url>
cd <project-directory>


2. Create and activate virtual environment:
python -m venv .venv
source .venv/bin/activate # Linux/macOS
.venv\Scripts\activate.bat # Windows


3. Install dependencies:
pip install -r requirements.txt


4. Set environment variables by creating a `.env` file (at project root):
GEMINI_API_KEY=your_gemini_free_tier_api_key
ALLOWED_ORIGINS=*


5. Start the backend server:
uvicorn backend.app:app --reload


6. (Optional) Start the Streamlit frontend UI:
streamlit run frontend/app.py


---

## Usage Guide

1. Upload 3 to 5 project documentation files describing features, API specifications, and design.
2. Upload the `checkout.html` file representing the web target’s UI structure.
3. Invoke knowledge base build to process and index documents and HTML content.
4. Enter natural-language queries in UI or via API to request test case generation.
5. Review the detailed test case JSON responses grounding on your documents.
6. Select relevant test cases to generate corresponding Selenium automation scripts.
7. Download and execute generated Python Selenium scripts for UI testing.

---

## Sample Documents Included

- `product_specs.md`: Functional and feature specifications.
- `ui_ux_guide.txt`: UI/UX design and validation guidelines.
- `api_endpoints.json`: API schema and contract representations.
- `checkout.html`: Example checkout page markup for UI grounding.

---

## Development Highlights

- Google Gemini LLM integration via `google-genai` Python client for advanced natural language capabilities.
- Modular design with separate components for ingestion, embedding, vector DB, LLM interaction, and APIs.
- Use of asynchronous web framework (FastAPI) for scalable and efficient request handling.
- Strict prompt engineering to prevent hallucinated content from LLM outputs.
- Robust validation, error handling, and logging to ensure reliability and maintainability.

---

## Troubleshooting & Common Issues

| Problem                          | Solution                                            |
|---------------------------------|----------------------------------------------------|
| Missing `checkout.html`          | Rebuild knowledge base; ensure proper upload       |
| Vector store not found           | Run ingestion pipeline fully before querying       |
| Gemini API errors                | Verify API key; monitor usage limits                |
| Selenium script output is JSON  | Check LLM prompt formatting; expect Python code    |

---

## Thank You

Himanshu 22BCE10118

---

