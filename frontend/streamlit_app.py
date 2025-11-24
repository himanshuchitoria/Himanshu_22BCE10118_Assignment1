import streamlit as st
import requests
import os

from components.file_upload import file_upload_component
from components.test_case_viewer import display_test_cases
from components.selenium_script_viewer import display_selenium_script
from components.test_runner_ui import display_test_run_results

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Autonomous QA Agent", layout="wide")
st.title("Autonomous QA Agent for Test Case & Selenium Script Generation")

# Initialize session state vars
if "knowledge_built" not in st.session_state:
    st.session_state.knowledge_built = False
if "support_docs" not in st.session_state:
    st.session_state.support_docs = None
if "checkout_file" not in st.session_state:
    st.session_state.checkout_file = None
if "test_case_query" not in st.session_state:
    st.session_state.test_case_query = ""
if "max_test_cases" not in st.session_state:
    st.session_state.max_test_cases = 10
if "test_cases" not in st.session_state:
    st.session_state.test_cases = []
if "selected_test_case" not in st.session_state:
    st.session_state.selected_test_case = None
if "selenium_script" not in st.session_state:
    st.session_state.selenium_script = None
if "test_run_result" not in st.session_state:
    st.session_state.test_run_result = None

def build_knowledge_base():
    if not st.session_state.support_docs or not st.session_state.checkout_file:
        st.error("Please upload both support documents and checkout.html before building knowledge base.")
        return

    # Prepare files for upload
    files = []
    for doc in st.session_state.support_docs:
        files.append(("support_docs", (doc.name, doc, doc.type or "application/octet-stream")))
    co = st.session_state.checkout_file
    files.append(("checkout_html", (co.name, co, co.type or "text/html")))

    with st.spinner("Building knowledge base..."):
        try:
            resp = requests.post(f"{API_BASE_URL}/build-knowledge-base", files=files)
            resp.raise_for_status()
            st.success("Knowledge base built successfully!")
            st.session_state.knowledge_built = True
        except Exception as e:
            st.error(f"Error building knowledge base: {e}")

def generate_test_cases():
    query = st.session_state.test_case_query.strip()
    max_cases = st.session_state.max_test_cases

    if not query:
        st.error("Please enter a query for test case generation.")
        return
    if not st.session_state.knowledge_built:
        st.error("Knowledge base not built. Please upload files and build knowledge base first.")
        return

    payload = {"query": query, "max_test_cases": max_cases}

    with st.spinner("Generating test cases..."):
        try:
            resp = requests.post(f"{API_BASE_URL}/generate-test-cases", json=payload)
            resp.raise_for_status()
            data = resp.json()
            st.session_state.test_cases = data.get("test_cases", [])
            if not st.session_state.test_cases:
                st.warning("No test cases generated.")
            else:
                st.success(f"{len(st.session_state.test_cases)} test cases generated.")
        except Exception as e:
            st.error(f"Failed to generate test cases: {e}")

def generate_selenium_script(test_case):
    if not test_case:
        st.error("No test case selected for Selenium script generation.")
        return

    payload = {"test_case": test_case}

    with st.spinner(f"Generating Selenium script for {test_case.get('test_id')}..."):
        try:
            resp = requests.post(f"{API_BASE_URL}/generate-selenium-script", json=payload)
            resp.raise_for_status()
            data = resp.json()
            st.session_state.selenium_script = data.get("selenium_script", "")
            if not st.session_state.selenium_script:
                st.warning("Empty Selenium script received.")
            else:
                st.success("Selenium script generated successfully.")
        except Exception as e:
            st.error(f"Failed to generate Selenium script: {e}")

# Main UI layout
with st.sidebar:
    st.header("Upload Files for Knowledge Base")
    support_docs, checkout_html = file_upload_component()
    if support_docs is not None:
        st.session_state.support_docs = support_docs
    if checkout_html is not None:
        st.session_state.checkout_file = checkout_html

    if st.button("Build Knowledge Base"):
        build_knowledge_base()

st.header("Test Case Generation")

st.text_area(
    "Describe the desired test cases or features",
    key="test_case_query",
    height=60,
    placeholder="Enter your test case requirements here..."
)

st.number_input(
    "Max number of test cases to generate",
    min_value=1,
    max_value=50,
    value=st.session_state.max_test_cases,
    key="max_test_cases"
)

if st.button("Generate Test Cases"):
    generate_test_cases()

display_test_cases(st.session_state.test_cases, on_generate_script=generate_selenium_script)

if st.session_state.selenium_script:
    display_selenium_script(st.session_state.selenium_script)

# Optional: Could integrate test run with SeleniumExecutor backend here and display_test_run_results UI.
