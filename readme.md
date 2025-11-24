# Autonomous QA Agent

## Project Overview

The Autonomous QA Agent is a sophisticated system that automatically builds a “testing brain” by ingesting project documentation and a target web application's HTML. It generates comprehensive, grounded test cases from user queries and produces executable Python Selenium scripts for automated UI testing. This streamlines and automates the QA process while strictly adhering to the provided documentation, avoiding hallucinated or fabricated features.

The backend is implemented using FastAPI, with semantic search via a vector database and LLM-powered generation utilizing Google’s Gemini AI.

---

## Features

- **Support Document Ingestion:** Upload markdown, text, JSON, and PDF files describing product specs, UI/UX rules, and API endpoints.
- **Checkout HTML Parsing:** Upload the single-page checkout HTML file representing the target web application.
- **Knowledge Base Construction:** Text splitting, embedding generation, and vector DB ingestion to enable retrieval-augmented generation.
- **Test Case Generation:** Generates detailed, documentation-grounded test cases based on user prompts.
- **Selenium Script Generation:** Converts chosen test cases into runnable Python Selenium WebDriver scripts that interact precisely with the uploaded HTML.
- **Strictly Grounded Reasoning:** No hallucinated features; all reasoning references source documents.
- **Streamlit UI:** User interface for uploading files, triggering ingestion, requesting test cases, and generating automation scripts.
- **Robust Architecture:** Async FastAPI backend, modular design, thorough logging, and error handling.
  
---

## Assignment Requirements Fulfilled

### Functionality
- Full pipeline from ingestion to script generation.
- Supports multiple document formats.
- Effective vector retrieval and LLM prompt engineering.

### Knowledge Grounding
- Test cases and scripts strictly based on provided documentation.
- Metadata preserved for traceability.

### Script Quality
- Clean, executable Selenium Python scripts using correct selectors.

### Code Quality
- Modular, readable, and maintainable code.
- Use of async programming and clear logging.

### User Experience
- Intuitive UI with clear feedback messages.

### Documentation
- This detailed README provides setup, usage, and architectural overview.
- Inline code comments clarify implementations.

---

## Architecture Overview

