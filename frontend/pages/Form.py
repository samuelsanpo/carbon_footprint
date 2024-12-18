import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Carbon Footprint",
    page_icon="🌳", 
)

if "report_id" in st.session_state:
    del st.session_state["report_id"]
    
st.title("Carbon Footprint Form")

# Initialize session state for storing form data
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "org_name": "",
        "industry": "Select an option",
        "employees": 0,
        "electricity": 0.0,
        "natural_gas": 0.0,
        "fuel": 0.0,
        "waste": 0.0,
        "waste_recycled": 0.0,
        "kilometers": 0.0,
        "efficiency": 0.0
    }

if "is_loading" not in st.session_state:
    st.session_state.is_loading = False  

if st.session_state.is_loading:
    st.warning("Processing... Please wait.")
    st.stop()  

# General Information Section
st.header("General Information")
st.session_state.form_data["org_name"] = st.text_input("Organization Name", value=st.session_state.form_data["org_name"])
st.session_state.form_data["industry"] = st.selectbox(
    "Industry Sector", 
    ["Select an option", "Manufacturing", "Retail", "IT Services", "Financial Services", "Logistic", "Other"], 
    index=["Select an option", "Manufacturing", "Retail", "IT Services", "Financial Services", "Logistic", "Other"].index(st.session_state.form_data["industry"])
)
st.session_state.form_data["employees"] = st.number_input("Number of Employees", min_value=0, value=st.session_state.form_data["employees"], step=1)

# Energy usage Section 
st.header("Energy usage")
st.session_state.form_data["electricity"] = round(st.number_input("Average monthly electricity bill in euros (€):", min_value=0.0, step= 0.1, format="%.2f", value=st.session_state.form_data["electricity"]), 2)
st.session_state.form_data["natural_gas"] = round(st.number_input("Average monthly natural gas bill in euros (€):", min_value=0.0, step= 0.1, format="%.2f",value=st.session_state.form_data["natural_gas"]), 2)
st.session_state.form_data["fuel"] = round(st.number_input("Average monthly transportation fuel bill in euros (€):", min_value=0.0, step= 0.1, format="%.2f",value=st.session_state.form_data["fuel"]), 2)

# Waste Section
st.header("Waste")
st.session_state.form_data["waste"] = round(st.number_input("Waste generated per month in kilograms (kg):", min_value=0.0, step=0.1, format="%.1f", value=st.session_state.form_data["waste"]), 1)
st.session_state.form_data["waste_recycled"] = round(st.number_input("Waste recycled or composted per month (percentage %)", min_value=0.0, max_value=57.0, step=0.1, format="%.1f", value=st.session_state.form_data["waste_recycled"]), 1)

# Business travel
st.header("Business travel")
st.session_state.form_data["kilometers"] = round(st.number_input("Kilometers your employees travel for business purposes per year (km):", min_value=0.0, step=0.1, format="%.1f", value=st.session_state.form_data["kilometers"]), 1)
st.session_state.form_data["efficiency"] = round(st.number_input("Average fuel consumption of vehicles used for business travel per 100 kilometers in liters (l) :", min_value=0.0, format="%.1f", step=0.1,  value=st.session_state.form_data["efficiency"]), 1)

# Validate if all required fields are completed
is_complete = (
    st.session_state.form_data["org_name"].strip() 
    and st.session_state.form_data["industry"] != "Select an option"  
    and st.session_state.form_data["employees"] > 0  
    and st.session_state.form_data["electricity"] > 0  
    and st.session_state.form_data["natural_gas"] > 0  
    and st.session_state.form_data["fuel"] >= 0  
    and st.session_state.form_data["waste"] > 0  
    and 0.0 <= st.session_state.form_data["waste_recycled"] <= 100.0  
    and st.session_state.form_data["kilometers"] >= 0  
    and st.session_state.form_data["efficiency"] >= 0  
)

if st.button("Submit Form", disabled=not is_complete):
    st.session_state.is_loading = True
    with st.spinner('Sending...'):
        try:
            print(st.session_state.form_data)
            response = requests.post("http://localhost:5000/submit", json=st.session_state.form_data)
            if response.status_code == 200:
                st.success("Form submitted successfully!")
                st.session_state.form_data = {
                    "org_name": "",
                    "industry": "Select an option",
                    "employees": 0,
                    "electricity": 0.0,
                    "natural_gas": 0.0,
                    "fuel": 0.0,
                    "waste": 0.0,
                    "waste_recycled": 0.0,
                    "kilometers": 0.0,
                    "efficiency": 0.0
                }
                report_id = response.json()["report_id"]
                st.session_state.report_id = report_id
                switch_page("Report")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Failed to connect to the server: {e}")
        finally:
            st.session_state.is_loading = False