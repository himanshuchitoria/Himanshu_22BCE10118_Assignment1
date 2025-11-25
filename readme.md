# Autonomous QA Agent 
(As per the assignment 1)

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

The Autonomous QA Agent is a smart system that is aimed at automating the process of producing software quality assurance artifacts by developing both test cases and UI automation scripts based on the project documentation completely.

It swallows a set of supporting documents (such as product specifications, user interface/user experience documentation, and API specifications) and a one-page checkout HTML page that is a representation of the user interface of the target web application.

It works with semantic embeddings, vector search and text chunking to build a knowledge base through which the system feeds context-aware queries to the Gemini Large Language Model of Google. The LLM produces precise and detailed test cases and Python Selenium scripts that are strictly followed by the uploaded content and will do away with the hallucination.

The backend is based on FastAPI to provide efficient asynchronous APIs, and optionally includes a Streamlit frontend to allow users an easy interface to uploads, generate test cases and view scripts.

---

## Key Features

- It supports several document types such as markdown, text, JSON and PDF.
- Extracts HTML and uses Selenium selectors to extract accurate Selenium selectors.
- Constructs a semantic retrieval store of knowledge in a vector form.
- Takes natural language inputs to create the test cases in the form of a JSON.
- Transfigures test cases into Python Selenium scripts, which are well-structured and runnable.
- Gathers Google Gemini LLM using the official python client, calledgoogle-genai.
- Uses strong logging and error processing using asynchronous FastAPI.
- has a front end based on Streamlit to allow easier user interaction.

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

- Python 3.11 is strictly in accordance to the versions listed with various requirements .
- Chrome browser and ChromeDriver are installed.
- Gemini API project with Google cloud (enabled, free tier) and an API key.
- Virtual environment system such as environs suggested.

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

- Start the Streamlit UI frontend:

  streamlit run frontend/app.py

---

## Usage Guide

1. Add 3 to 5 support documents of the requirements of your application, rules of UI/UX, and API contracts.
2. Post the one page checkout HTML file of the web app.
3. Click Build Knowledge Base to encode, chunk, embed and index the content uploaded.
4. Should Input a natural language query to the UI or an-API (e.g., “Generate all positive and negative test cases of the feature of discount codes.)
5. Test the test cases that have been generated on strict basis based on your documentation.
6. Choose test cases and create executable Selenium Python scripts specific to your HTML UI.
7. ChromeDriver may be used to download and execute automation scripts locally to test UI behaviour.

---

## Sample Documents Provided in Video demonstration

- `product_specs.md` — Business and product feature specifications.
- `ui_ux_guide.txt` — UI styling and validation instructions.
- `api_endpoints.json` — API endpoint definitions and formats.
- `checkout.html` — The single-page web checkout interface HTML file.

---

## Development Highlights

- It can be integrated with Google Gemini LLM via the official python client, named as Google-genai, to provide strong grounded natural language and code generation.
- Semantic retrieval through the implementation of a vector store allows relevance and accuracy of generated test cases.
- FastAPI backend is fully asynchronous, which maximizes the processing of request concurrency.
- Ingestion, embedding, LLM logic, API routing and front end are decoupled.
- Full logs and error handling provide maintainability and debugging.

---

## Thank You
Himanshu 22BCE10118

---


