import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Carbon Footprint",
    page_icon="🌳", 
)

# Sidebar with streamlit_option_menu
with st.sidebar:
    page = option_menu(
        menu_title="Navigation",
        options=["Home", "Form", "Reports", "Analysis"],
        icons=["house", "clipboard", "bar-chart", "search"],
        default_index=0,
        menu_icon="null",  
    )

# Load pages dynamically, app_pages is used as a folder for views to 
# prevent python from creating the navigation menu by default, since streamlit_option_menu is used for navigation
if page == "Home":
    import app_pages.Home as Home
    Home.show()
elif page == "Form":
    import app_pages.Form as Form
    Form.show()
elif page == "Reports":
    import app_pages.Reports as Reports
    Reports.show()
elif page == "Analysis":
    import app_pages.Analysis as Analysis
    Analysis.show()

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
            padding: 10px;
            font-size: 12px;
        }
    </style>
    <div class="footer">
        <p>Created by Samuel Sanabria | <a href="https://github.com/samuelsanpo">Github</a></p>
    </div>
"""

st.markdown(footer, unsafe_allow_html=True)