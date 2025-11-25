# Autonomous QA Agent

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Sample Documents](#sample-documents)
- [Development Highlights](#development-highlights)


---

## Project Overview

The Autonomous QA Agent is an intelligent system designed to automate the generation of software quality assurance artifacts by creating test cases and UI automation scripts fully grounded in project documentation.

It ingests multiple support documents — including product specs, UI/UX guidelines, and API contracts — alongside a single-page checkout HTML file representing the target web application's UI.

Using text chunking, semantic embeddings, and vector search, the system creates a knowledge base that feeds context-aware queries to Google’s Gemini Large Language Model. The LLM generates detailed, accurate test cases and Python Selenium scripts that strictly adhere to the uploaded material, eliminating hallucination.

The backend uses FastAPI for efficient asynchronous APIs, while an optional Streamlit frontend provides a user-friendly interface for uploads, test case generation, and script viewing.

---

## Key Features

- Supports various document formats including markdown, text, JSON, and PDF.
- Processes checkout HTML for precise Selenium selector extraction.
- Builds a vector store knowledge base for semantic retrieval.
- Accepts natural language queries to generate JSON-structured test cases.
- Converts test cases into runnable, well-structured Python Selenium scripts.
- Integrates Google Gemini LLM via the official `google-genai` Python client.
- Employs robust logging and error handling with asynchronous FastAPI.
- Provides a Streamlit-based front end for simplified user interaction.

---

## Architecture

1. **Input:** Support Documents & `checkout.html`
2. **Processing:** Chunking & Embedding
3. **Storage:** Vector Search Database
4. **AI Logic:** Retrieval-Augmented Generation (Google Gemini LLM)
5. **Output Gen:** Test Cases & Selenium Script Generation
6. **Backend:** FastAPI Backend APIs
7. **Frontend:** Streamlit Frontend UI
---

---

## Setup Instructions

### Prerequisites

- Python 3.11 strictly as per the versions mentioned for different requirements .
- Chrome browser with matching ChromeDriver installed
- Google Cloud project with Gemini API enabled and an API key (free tier compatible)
- Virtual environment system like `venv` recommended

### Installation

- Clone repo
- git clone <repository-url of this project>
- cd frontend or required folder

p Create and activate venv
- python -m venv .venv
- source .venv/bin/activate # Linux/macOS
- .venv\Scripts\activate.bat # Windows

- Install dependencies
- pip install -r requirements.txt

- Prepare environment variables in `.env` file:

- GEMINI_API_KEY= get yours from google studio (for website i have already mentioned in the environment)
ALLOWED_ORIGINS=*

### Running

- Start the FastAPI backend server:

- uvicorn backend.app:app --reload

(Optional) Start the Streamlit UI frontend:

- streamlit run frontend/app.py

---

## Usage Guide

1. Upload 3 to 5 support documents describing your application’s requirements, UI/UX rules, and API contracts.
2. Upload the single-page checkout HTML file of the web app.
3. Click “Build Knowledge Base” to parse, chunk, embed, and index the uploaded content.
4. Enter a natural language query in the UI or via API (e.g., “Generate all positive and negative test cases for the discount code feature.”)
5. Review the generated test cases strictly grounded on your documentation.
6. Select test cases and generate runnable Selenium Python scripts tailored to your HTML UI.
7. Download and run automation scripts locally using ChromeDriver to verify UI behavior.

---

## Sample Documents Provided

- `product_specs.md` — Business and product feature specifications.
- `ui_ux_guide.txt` — UI styling and validation instructions.
- `api_endpoints.json` — API endpoint definitions and formats.
- `checkout.html` — The single-page web checkout interface HTML file.

---

## Development Highlights

- Integration with Google Gemini LLM through the official `google-genai` Python client ensures powerful, grounded natural language and code generation.
- Vector store implementation enables semantic retrieval, improving relevance and accuracy of generated test cases.
- Fully asynchronous FastAPI backend optimizes handling of request concurrency.
- Modular design separates ingestion, embedding, LLM logic, API routing, and front end cleanly.
- Comprehensive logs and error handling facilitate debugging and maintainability.

---

## Thank You

---


