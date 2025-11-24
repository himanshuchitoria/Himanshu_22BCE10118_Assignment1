import streamlit as st

def file_upload_component():
    """
    Renders file upload UI for support documents and checkout.html.
    Returns:
        Tuple of (support_docs, checkout_file) containing uploaded files or None.
    """
    # --- Custom CSS for cleaner Uploaders ---
    st.markdown(
        """
        <style>
        /* Style the file uploader to have a border and cleaner look */
        div[data-testid="stFileUploader"] section {
            border: 1px dashed #4A90E2;
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 10px;
        }
        div[data-testid="stFileUploader"] section:hover {
            background-color: #f0f2f6;
            border-color: #2E75C5;
        }
        /* Dark mode adjustment (optional, remove if strictly light mode) */
        @media (prefers-color-scheme: dark) {
            div[data-testid="stFileUploader"] section {
                background-color: #262730;
                border-color: #4A90E2;
            }
            div[data-testid="stFileUploader"] section:hover {
                background-color: #31333F;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.markdown("### 📂 Project Assets")
        st.markdown("---")
        
        # Grouping uploads in a container for better separation
        with st.container():
            st.info("Upload your reference materials below.")
            
            support_docs = st.file_uploader(
                "📄 Support Documents (MD, TXT, JSON, PDF)",
                accept_multiple_files=True,
                type=["md", "txt", "json", "pdf"],
                help="Upload multiple context files here."
            )
            
            # Mini feedback for documents
            if support_docs:
                st.success(f"✅ {len(support_docs)} Document(s) attached")

            st.markdown("---") # Visual separator
            
            checkout_html = st.file_uploader(
                "🌐 Checkout HTML (.html)",
                accept_multiple_files=False,
                type=["html"],
                help="Upload the single checkout page code."
            )
            
            # Mini feedback for HTML
            if checkout_html:
                st.success(f"✅ {checkout_html.name} attached")

    return support_docs, checkout_html