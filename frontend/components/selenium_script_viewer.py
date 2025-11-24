import streamlit as st

def display_selenium_script(selenium_script):
    """
    Displays the generated Selenium Python script with syntax highlighting.
    """
    if not selenium_script:
        st.info("No Selenium script generated yet.")
        return

    st.subheader("Generated Selenium Script")
    st.code(selenium_script, language="python")
