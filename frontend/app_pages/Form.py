import streamlit as st

def show():

    st.title("Carbon Footprint Form")

    # Initialize session state for storing form data
    if "form_data" not in st.session_state:
        st.session_state.form_data = {
            "org_type": "General",
            "org_name": "",
            "industry": "Select an option",
            "employees": 0,
            "electricity": 0.0,
            "fuel_heating": 0.0,
            "fuel_type": "Select an option",
            "company_vehicles": 0,
            "vehicle_fuel": 0.0,
            "commute_distance": 0.0,
            "industrial_process": "",
            "process_emissions": 0.0,
            "purchased_goods": "",
            "transport_distance": 0.0,
            "freight_type": "Select an option",
            "tree_planting": 0,
            "carbon_credits": 0.0,
            "water_usage": 0.0,
            "effluents": 0.0,
            "treatment_method": "None"
        }

    # Organization type selection
    org_type = st.selectbox(
        "Select the type of your organization:",
        ["General", "Industrial", "Service", "Other"],
        index=["General", "Industrial", "Service", "Other"].index(st.session_state.form_data["org_type"])
    )

    st.session_state.form_data["org_type"] = org_type

    # General Information Section
    st.header("General Information")
    st.session_state.form_data["org_name"] = st.text_input("Organization Name", value=st.session_state.form_data["org_name"])
    st.session_state.form_data["industry"] = st.selectbox(
        "Industry Sector", 
        ["Select an option", "Manufacturing", "Retail", "IT Services", "Other"], 
        index=["Select an option", "Manufacturing", "Retail", "IT Services", "Other"].index(st.session_state.form_data["industry"])
    )
    st.session_state.form_data["employees"] = st.number_input("Number of Employees", min_value=0, value=st.session_state.form_data["employees"], step=1)

    # Energy Consumption Section (conditional on organization type)
    st.header("Energy Consumption")
    st.session_state.form_data["electricity"] = st.number_input("Electricity consumption (kWh per month):", min_value=0.0, value=st.session_state.form_data["electricity"])
    st.session_state.form_data["fuel_heating"] = st.number_input("Fuel consumption for heating (liters or m³):", min_value=0.0, value=st.session_state.form_data["fuel_heating"])
    st.session_state.form_data["fuel_type"] = st.selectbox("Fuel type", ["Select an option", "Natural gas", "Diesel", "Propane", "Other"], index=["Select an option", "Natural gas", "Diesel", "Propane", "Other"].index(st.session_state.form_data["fuel_type"]))

    # Transportation Section
    st.header("Transportation")
    st.session_state.form_data["company_vehicles"] = st.number_input("Company-owned vehicles (number):", min_value=0, value=st.session_state.form_data["company_vehicles"])
    st.session_state.form_data["vehicle_fuel"] = st.number_input("Average fuel consumption of vehicles (liters per month):", min_value=0.0, value=st.session_state.form_data["vehicle_fuel"])
    st.session_state.form_data["commute_distance"] = st.number_input("Employee commute distance (km per week):", min_value=0.0, value=st.session_state.form_data["commute_distance"])

    # Industrial Processes Section (conditional on organization type)
    if org_type == "Industrial":
        st.header("Industrial Processes")
        st.session_state.form_data["industrial_process"] = st.text_input("Describe the processes that generate emissions (if any):", value=st.session_state.form_data["industrial_process"])
        st.session_state.form_data["process_emissions"] = st.number_input("Estimated annual emissions from processes (metric tons CO₂):", min_value=0.0, value=st.session_state.form_data["process_emissions"])

    # Supply Chain Section (conditional on organization type)
    if org_type in ["General", "Industrial"]:
        st.header("Supply Chain and Purchases")
        st.session_state.form_data["purchased_goods"] = st.text_area("Describe the main goods or services purchased:", value=st.session_state.form_data["purchased_goods"])
        st.session_state.form_data["transport_distance"] = st.number_input("Average distance for transporting purchased goods (km):", min_value=0.0, value=st.session_state.form_data["transport_distance"])
        st.session_state.form_data["freight_type"] = st.selectbox("Type of transport:", ["Select an option", "Truck", "Ship", "Airplane", "Other"], index=["Select an option", "Truck", "Ship", "Airplane", "Other"].index(st.session_state.form_data["freight_type"]))

    # Offset Activities Section
    st.header("Carbon Offset Activities")
    st.session_state.form_data["tree_planting"] = st.number_input("Number of trees planted annually:", min_value=0, value=st.session_state.form_data["tree_planting"], step=1)
    st.session_state.form_data["carbon_credits"] = st.number_input("Carbon credits purchased (metric tons CO₂):", min_value=0.0, value=st.session_state.form_data["carbon_credits"])

    # Water and Effluents Section (conditional on organization type)
    if org_type in ["Industrial", "Other"]:
        st.header("Water and Effluents")
        st.session_state.form_data["water_usage"] = st.number_input("Monthly water consumption (liters or m³):", min_value=0.0, value=st.session_state.form_data["water_usage"])
        st.session_state.form_data["effluents"] = st.number_input("Monthly effluents generated (liters or m³):", min_value=0.0, value=st.session_state.form_data["effluents"])
        st.session_state.form_data["treatment_method"] = st.selectbox("Effluent treatment method:", ["None", "Primary", "Secondary", "Tertiary"], index=["None", "Primary", "Secondary", "Tertiary"].index(st.session_state.form_data["treatment_method"]))

    # Validate if all required fields are completed
    is_complete = (
        st.session_state.form_data["org_name"]
        and st.session_state.form_data["industry"] != "Select an option"
        and st.session_state.form_data["employees"] > 0
        and st.session_state.form_data["electricity"] > 0
        and st.session_state.form_data["fuel_heating"] >= 0
        and st.session_state.form_data["fuel_type"] != "Select an option"
        and st.session_state.form_data["company_vehicles"] >= 0
        and st.session_state.form_data["vehicle_fuel"] >= 0
        and st.session_state.form_data["commute_distance"] >= 0
        and (org_type != "Industrial" or st.session_state.form_data["industrial_process"] and st.session_state.form_data["process_emissions"] >= 0)
        and (org_type in ["General", "Industrial"] or st.session_state.form_data["purchased_goods"] and st.session_state.form_data["transport_distance"] >= 0 and st.session_state.form_data["freight_type"] != "Select an option")
        and st.session_state.form_data["tree_planting"] >= 0 and st.session_state.form_data["carbon_credits"] >= 0
        and (org_type in ["Industrial", "Other"] or st.session_state.form_data["water_usage"] >= 0 and st.session_state.form_data["effluents"] >= 0 and st.session_state.form_data["treatment_method"] != "Select an option")
    )

    if st.button("Submit Form", disabled=not is_complete):
        st.success("Form submitted successfully!")
