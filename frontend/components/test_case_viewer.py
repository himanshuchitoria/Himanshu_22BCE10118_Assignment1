import streamlit as st

def display_test_cases(test_cases, on_generate_script):
    """
    Displays list of generated test cases with a card-style layout 
    and a button to generate Selenium script.
    
    Parameters:
        - test_cases: List of test case dicts
        - on_generate_script: callback function accepting test case dict when button clicked
    """
    
    # --- Custom CSS for Cards ---
    st.markdown("""
    <style>
    div.stContainer {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e6e6e6;
        margin-bottom: 15px;
    }
    /* Dark mode support for cards */
    @media (prefers-color-scheme: dark) {
        div.stContainer {
            background-color: #262730;
            border-color: #3d3d3d;
        }
    }
    .test-id-badge {
        background-color: #FF4B4B;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    if not test_cases:
        st.info("ℹ️ No generated test cases found. Please generate them first.")
        return

    st.subheader(f"📋 Generated Test Cases ({len(test_cases)})")
    st.caption("Review the scenarios below and generate scripts for individual cases.")

    # Iterate through test cases and create a "Card" for each
    for idx, tc in enumerate(test_cases):
        # Create a container for the card effect
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Header with ID badge
                st.markdown(f"<span class='test-id-badge'>{tc['test_id']}</span> **{tc['feature']}**", unsafe_allow_html=True)
                
                # Details in an expandable section or just clean text
                st.markdown(f"**Scenario:** {tc['test_scenario']}")
                st.markdown(f"**Expected:** *{tc['expected_result']}*")
            
            with col2:
                # Centering the button vertically requires some whitespace or just clean column usage
                st.write("") # Spacer
                if st.button(f"⚡ Generate Script", key=f"btn_gen_script_{idx}", help=f"Create Selenium code for {tc['test_id']}"):
                    on_generate_script(tc)
                    
        # Optional: A subtle divider between items if not using container background colors
        # st.divider()