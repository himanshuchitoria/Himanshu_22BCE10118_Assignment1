import streamlit as st

def display_selenium_script(selenium_script):
    """
    Displays the generated Selenium Python script with syntax highlighting
    and a download option.
    """
    # --- CSS for the Code Container ---
    st.markdown(
        """
        <style>
        /* Add a subtle shadow to the code block area */
        .stCodeBlock {
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if not selenium_script:
        # Use a warning with an icon for better visibility than st.info
        st.warning("⚠️ No Selenium script generated yet. Run the generator to see the code here.")
        return

    # Use a container to group the header and download button
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.subheader("🚀 Generated Selenium Script")
            st.caption("Review your automated testing script below.")
            
        with col2:
            # Add a download button for better UX
            st.download_button(
                label="📥 Download .py",
                data=selenium_script,
                file_name="test_script.py",
                mime="text/x-python",
                help="Download this script to run locally."
            )

    # Display code inside an expander so it doesn't dominate the screen if it's long
    with st.expander("View Code Content", expanded=True):
        st.code(selenium_script, language="python", line_numbers=True)

    st.success("✅ Script generated successfully!")