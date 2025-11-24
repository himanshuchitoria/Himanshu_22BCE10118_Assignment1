import streamlit as st

def display_test_cases(test_cases, on_generate_script):
    """
    Displays list of generated test cases with a button to generate Selenium script.
    Parameters:
        - test_cases: List of test case dicts
        - on_generate_script: callback function accepting test case dict when button clicked
    """
    if not test_cases:
        st.warning("No generated test cases to display.")
        return

    st.subheader("Generated Test Cases")
    for idx, tc in enumerate(test_cases):
        st.markdown(f"**[{tc['test_id']}] {tc['feature']}**")
        st.markdown(f"- Scenario: {tc['test_scenario']}")
        st.markdown(f"- Expected: {tc['expected_result']}")
        if st.button(f"Generate Selenium Script for {tc['test_id']}", key=f"btn_gen_script_{idx}"):
            on_generate_script(tc)
