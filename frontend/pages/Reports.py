import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page
from datetime import datetime

st.set_page_config(
    page_title="Carbon Footprint",
    page_icon="🌳", 
)

if "report_id" in st.session_state:
    del st.session_state["report_id"]

st.title("Reports")


BACKEND_URL = "http://localhost:5000"

def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    return date_obj.strftime("%B %d, %Y, %I:%M %p") 
# In this method I consume a get that brings me all the forms records and map them to show title,
#  a date that I format with the function above and the link to enter the report as such, also when 
# I send the report I assign the id of the report to the session.
try:
    response = requests.get(f"{BACKEND_URL}/forms")
    if response.status_code == 200:
        records = response.json()
        for record in records:
            st.subheader(f"**{record['org_name']}** - {format_date(record['creation_date'])}")
            if st.button(f"View Report: {record['id']}"):
                report_id = record["id"]
                st.session_state.report_id = report_id
                switch_page("Report")
    else:
        st.error("It seems that there are no records yet!")
except Exception as e:
    st.error(f"An error occurred: {e}")




