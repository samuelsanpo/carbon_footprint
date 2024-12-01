import streamlit as st

def show():
    import streamlit as st

    st.title("Carbon Footprint Form")

    org_type = st.selectbox(
        "Select the type of your organization:",
        ["General", "Industrial", "Service", "Other"]
    )

    tabs_config = {
        "General Info": True,
        "Energy": True,
        "Transportation": True,
        "Industrial Processes": org_type == "Industrial",
        "Supply Chain": org_type in ["General", "Industrial"],
        "Offset Activities": True,
        "Water and Effluents": org_type in ["Industrial", "Other"]
    }

    active_tabs = [label for label, condition in tabs_config.items() if condition]
    tabs = st.tabs(active_tabs)


    if "General Info" in active_tabs:
        with tabs[active_tabs.index("General Info")]:
            st.header("General Information")
            org_name = st.text_input("Organization Name")
            industry = st.selectbox("Industry Sector", ["Manufacturing", "Retail", "IT Services", "Other"])
            employees = st.number_input("Number of Employees", min_value=1, step=1)

    if "Energy" in active_tabs:
        with tabs[active_tabs.index("Energy")]:
            st.header("Energy Consumption")
            electricity = st.number_input("Electricity consumption (kWh per month):", min_value=0.0)
            fuel_heating = st.number_input("Fuel consumption for heating (liters or m³):", min_value=0.0)
            fuel_type = st.selectbox("Fuel type:", ["Natural gas", "Diesel", "Propane", "Other"])

    if "Transportation" in active_tabs:
        with tabs[active_tabs.index("Transportation")]:
            st.header("Transportation")
            company_vehicles = st.number_input("Company-owned vehicles (number):", min_value=0)
            vehicle_fuel = st.number_input("Average fuel consumption of vehicles (liters per month):", min_value=0.0)
            commute_distance = st.number_input("Employee commute distance (km per week):", min_value=0.0)

    if "Industrial Processes" in active_tabs:
        with tabs[active_tabs.index("Industrial Processes")]:
            st.header("Industrial Processes")
            industrial_process = st.text_input("Describe the processes that generate emissions (if any):")
            process_emissions = st.number_input(
                "Estimated annual emissions from processes (metric tons CO₂):", min_value=0.0
            )

    if "Supply Chain" in active_tabs:
        with tabs[active_tabs.index("Supply Chain")]:
            st.header("Supply Chain and Purchases")
            purchased_goods = st.text_area("Describe the main goods or services purchased:")
            transport_distance = st.number_input(
                "Average distance for transporting purchased goods (km):", min_value=0.0
            )
            freight_type = st.selectbox("Type of transport:", ["Truck", "Ship", "Airplane", "Other"])

    if "Offset Activities" in active_tabs:
        with tabs[active_tabs.index("Offset Activities")]:
            st.header("Carbon Offset Activities")
            tree_planting = st.number_input("Number of trees planted annually:", min_value=0, step=1)
            carbon_credits = st.number_input("Carbon credits purchased (metric tons CO₂):", min_value=0.0)

    if "Water and Effluents" in active_tabs:
        with tabs[active_tabs.index("Water and Effluents")]:
            st.header("Water and Effluents")
            water_usage = st.number_input("Monthly water consumption (liters or m³):", min_value=0.0)
            effluents = st.number_input("Monthly effluents generated (liters or m³):", min_value=0.0)
            treatment_method = st.selectbox("Effluent treatment method:", ["None", "Primary", "Secondary", "Tertiary"])

    if st.button("Submit Form"):
        st.success("Form submitted successfully!")


