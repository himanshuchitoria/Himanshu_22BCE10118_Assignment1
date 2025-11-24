import streamlit as st

def file_upload_component():
    """
    Renders file upload UI for support documents and checkout.html.
    Returns:
        Tuple of (support_docs, checkout_file) containing uploaded files or None.
    """
    st.sidebar.header("Upload Project Documents")

    support_docs = st.sidebar.file_uploader(
        "Support Documents (.md, .txt, .json, .pdf), upload multiple",
        accept_multiple_files=True,
        type=["md", "txt", "json", "pdf"],
    )

    checkout_html = st.sidebar.file_uploader(
        "Checkout HTML file (.html)",
        accept_multiple_files=False,
        type=["html"]
    )

    return support_docs, checkout_html
