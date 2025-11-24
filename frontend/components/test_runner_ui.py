import streamlit as st

def display_test_run_results(test_run_result):
    """
    Show results of executing Selenium test script.
    Expects a dict with keys: 'success', 'stdout', 'stderr', 'error'
    """
    st.subheader("Test Execution Results")

    if not test_run_result:
        st.info("No test run results available.")
        return

    if test_run_result.get("error"):
        st.error(f"Execution error: {test_run_result['error']}")
        return

    if test_run_result.get("success"):
        st.success("Test ran successfully.")
    else:
        st.error("Test failed.")

    st.markdown("**Standard Output:**")
    st.text(test_run_result.get("stdout", ""))

    st.markdown("**Standard Error:**")
    st.text(test_run_result.get("stderr", ""))
