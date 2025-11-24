import streamlit as st

def display_test_run_results(test_run_result):
    """
    Show results of executing Selenium test script with a modern terminal-like UI.
    Expects a dict with keys: 'success', 'stdout', 'stderr', 'error'
    """
    
    # --- Custom CSS for Terminal Output ---
    st.markdown("""
    <style>
    .terminal-box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #4CAF50; /* Default green accent */
        white-space: pre-wrap;
        font-size: 0.9em;
        max-height: 400px;
        overflow-y: auto;
    }
    .terminal-error {
        border-left-color: #FF5252; /* Red accent for errors */
    }
    </style>
    """, unsafe_allow_html=True)

    if not test_run_result:
        # Use a placeholder container instead of a simple info box
        with st.container():
            st.info("ℹ️ No test results yet. Run a script to see the logs here.")
        return

    st.subheader("📊 Execution Report")

    # 1. High-level Status Banner
    # We check for system errors (execution crashes) first, then test logic failures
    if test_run_result.get("error"):
        st.error(f"❌ **System Error:** execution crashed.")
        with st.expander("View Crash Details", expanded=True):
            st.code(test_run_result['error'], language="bash")
        return

    success = test_run_result.get("success", False)
    
    if success:
        st.success("✅ **Test Passed:** The script executed without errors.")
    else:
        st.error("🚫 **Test Failed:** The script encountered issues during execution.")

    # 2. Logs in Tabs (Clean Layout)
    st.write("") # Spacer
    st.markdown("##### 📜 Console Output")
    
    tab1, tab2 = st.tabs(["stdout (Output)", "stderr (Errors)"])

    stdout_text = test_run_result.get("stdout", "")
    stderr_text = test_run_result.get("stderr", "")

    with tab1:
        if stdout_text.strip():
            # Injecting HTML for the custom terminal look
            st.markdown(f'<div class="terminal-box">{stdout_text}</div>', unsafe_allow_html=True)
        else:
            st.caption("No standard output recorded.")

    with tab2:
        if stderr_text.strip():
            # Injecting HTML with the error class
            st.markdown(f'<div class="terminal-box terminal-error">{stderr_text}</div>', unsafe_allow_html=True)
        else:
            st.caption("No standard errors recorded.")

    # Optional: Quick summary metrics if you ever wanted to add them later
    # col1, col2 = st.columns(2)
    # col1.metric("Status", "Passed" if success else "Failed")
    # col2.metric("Log Size", f"{len(stdout_text)} chars")