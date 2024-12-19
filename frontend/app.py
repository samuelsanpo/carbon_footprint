import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Carbon Footprint",
    page_icon="🌳", 
)
# Home page, introduction to the tool for users.
if "report_id" in st.session_state:
    del st.session_state["report_id"]

st.title("Carboon footprint")

st.write("Welcome to the carbon footprint calculator for your organization, it is very important that we start to care about our planet so we must measure the damage we are causing, with the following video we want you to enter into context with the idea of carbon footprint, after watching it please proceed to the form, review your results and evaluate the possible improvements that we recommend.")

st.video("https://www.youtube.com/watch?v=a9yO-K8mwL0")

if st.button("Take the form"):
    switch_page("Form")

 #footer
footer = """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: rgb(14, 17, 23);
            text-align: center;
            padding: 5px;
            font-size: 10px;
            height: 5vh;
        }
    </style>
    <div class="footer">
        <p>Created by Samuel Sanabria | <a href="https://github.com/samuelsanpo">Github</a></p>
    </div>
"""

st.markdown(footer, unsafe_allow_html=True)