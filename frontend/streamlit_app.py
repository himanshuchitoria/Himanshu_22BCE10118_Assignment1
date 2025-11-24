import streamlit as st
import requests
import os

# Import our modernized components
from components.file_upload import file_upload_component
from components.test_case_viewer import display_test_cases
from components.selenium_script_viewer import display_selenium_script
from components.test_runner_ui import display_test_run_results

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# --- Page Configuration ---
st.set_page_config(
    page_title="AutoQA | AI Test Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Global Custom CSS ---
st.markdown("""
    <style>
        /* Main Font adjustments */
        .stApp {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Title Styling */
        h1 {
            color: #2E75C5;
            font-weight: 700;
        }
        
        /* Button Styling Overrides */
        div.stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Text Area Styling */
        .stTextArea textarea {
            border-radius: 8px;
            border: 1px solid #ddd;
        }
        
        /* Sidebar tweaks */
        section[data-testid="stSidebar"] {
            background-color: #f7f9fc;
        }
        @media (prefers-color-scheme: dark) {
            section[data-testid="stSidebar"] {
                background-color: #1e1e1e;
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "knowledge_built" not in st.session_state:
    st.session_state.knowledge_built = False
if "support_docs" not in st.session_state:
    st.session_state.support_docs = None
if "checkout_file" not in st.session_state:
    st.session_state.checkout_file = None
if "test_case_query" not in st.session_state:
    st.session_state.test_case_query = ""
if "max_test_cases" not in st.session_state:
    st.session_state.max_test_cases = 5
if "test_cases" not in st.session_state:
    st.session_state.test_cases = []
if "selenium_script" not in st.session_state:
    st.session_state.selenium_script = None

# --- Logic Functions ---

def build_knowledge_base():
    """Handles the API call to build the vector DB/Knowledge Base."""
    if not st.session_state.support_docs or not st.session_state.checkout_file:
        st.toast("⚠️ Please upload both support documents and checkout.html first.", icon="⚠️")
        return

    # Prepare files for upload
    files = []
    for doc in st.session_state.support_docs:
        files.append(("support_docs", (doc.name, doc, doc.type or "application/octet-stream")))
    co = st.session_state.checkout_file
    files.append(("checkout_html", (co.name, co, co.type or "text/html")))

    with st.spinner("🧠 Analyzing documents and building knowledge base..."):
        try:
            resp = requests.post(f"{API_BASE_URL}/build-knowledge-base", files=files)
            resp.raise_for_status()
            st.session_state.knowledge_built = True
            st.toast("Knowledge base built successfully!", icon="✅")
            st.balloons()
        except Exception as e:
            st.error(f"Error building knowledge base: {e}")

def generate_test_cases():
    """Handles the API call to generate test scenarios."""
    query = st.session_state.test_case_query.strip()
    max_cases = st.session_state.max_test_cases

    if not query:
        st.toast("Please describe what you want to test.", icon="✍️")
        return
    if not st.session_state.knowledge_built:
        st.error("🚨 Knowledge base not ready. Please check the Sidebar.")
        return

    payload = {"query": query, "max_test_cases": max_cases}

    with st.spinner("🤖 AI is brainstorming test scenarios..."):
        try:
            resp = requests.post(f"{API_BASE_URL}/generate-test-cases", json=payload)
            resp.raise_for_status()
            data = resp.json()
            st.session_state.test_cases = data.get("test_cases", [])
            
            if not st.session_state.test_cases:
                st.warning("No test cases generated. Try refining your query.")
            else:
                st.toast(f"Generated {len(st.session_state.test_cases)} test cases!", icon="✅")
        except Exception as e:
            st.error(f"Failed to generate test cases: {e}")

def generate_selenium_script(test_case):
    """Handles the API call to generate Python/Selenium code for a specific case."""
    if not test_case:
        return

    payload = {"test_case": test_case}

    with st.spinner(f"⚡ Writing Selenium script for {test_case.get('test_id')}..."):
        try:
            resp = requests.post(f"{API_BASE_URL}/generate-selenium-script", json=payload)
            resp.raise_for_status()
            data = resp.json()
            script = data.get("selenium_script", "")
            
            if script:
                st.session_state.selenium_script = script
                st.toast("Script generated! Scroll down to view.", icon="⬇️")
            else:
                st.warning("API returned an empty script.")
        except Exception as e:
            st.error(f"Failed to generate Selenium script: {e}")

# --- Main UI Layout ---

# 1. Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Setup")
    
    # File Upload Component (Improved Version)
    support_docs, checkout_html = file_upload_component()
    
    # Update state based on component return
    if support_docs is not None:
        st.session_state.support_docs = support_docs
    if checkout_html is not None:
        st.session_state.checkout_file = checkout_html

    st.markdown("### Actions")
    # Using a primary button for the main setup action
    if st.button("Build Knowledge Base", use_container_width=True, type="primary"):
        build_knowledge_base()
        
    # Visual indicator of state
    if st.session_state.knowledge_built:
        st.success("✅ Knowledge Base Ready")
    else:
        st.info("Waiting for knowledge base...")

# 2. Header / Hero Section
st.title("🤖 Autonomous QA Agent")
st.markdown("""
    **Generate comprehensive test cases and automated Selenium scripts directly from your documentation.**
            
    *Created by Himanshu 22BCE10118*
            
    Simple steps to get started:
    1. Upload your docs in the sidebar.
    2. Define your testing requirements below.
    3. Generate and export your automation scripts.
""")
st.divider()

# 3. Input Section (Grouped for aesthetics)
st.subheader("Define Testing Scope")

with st.container():
    col_input, col_settings = st.columns([3, 1])
    
    with col_input:
        st.text_area(
            "What features should we test?",
            key="test_case_query",
            height=100,
            placeholder="E.g., Verify that the user can add items to the cart and proceed to checkout successfully...",
            label_visibility="collapsed"
        )

    with col_settings:
        st.number_input(
            "Max Test Cases",
            min_value=1,
            max_value=20,
            value=st.session_state.max_test_cases,
            key="max_test_cases",
            help="Limit the number of scenarios generated."
        )
        st.write("") # Spacer
        if st.button("✨ Generate Scenarios", use_container_width=True, type="primary"):
            generate_test_cases()

# 4. Results Section - Test Cases
if st.session_state.test_cases:
    st.divider()
    st.subheader("Review & Automate")
    
    # Display the modern test case viewer
    display_test_cases(
        st.session_state.test_cases, 
        on_generate_script=generate_selenium_script
    )

# 5. Results Section - Script Viewer
if st.session_state.selenium_script:
    st.divider()
    # Display the modern script viewer
    display_selenium_script(st.session_state.selenium_script)

    # Placeholder for future execution UI
    # display_test_run_results(st.session_state.test_run_result)