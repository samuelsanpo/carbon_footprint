import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Carbon Footprint",
    page_icon="🌳", 
)

if "report_id" in st.session_state:
    del st.session_state["report_id"]


st.title("Analysis")

BACKEND_URL = "http://localhost:5000"

def get_reports_data():
    try:
        response = requests.get(f"{BACKEND_URL}/forms")
        if response.status_code == 200:
            return response.json()  
        else:
            st.error(f"Error fetching: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

data = get_reports_data()

if data:
    # Pandas dataframe
    companies_data = []
    for report in data:
        company_data = {
            "org_name": report["org_name"],
            "industry": report["industry"],
            "employees": report["employees"],
            "electricity": report["electricity"],
            "natural_gas": report["natural_gas"],
            "fuel": report["fuel"],
            "waste": report["waste"], 
            "waste_recycled": report["waste_recycled"],  
            "kilometers": report["kilometers"],  
            "efficiency": report["efficiency"],  
            "energy_emissions": report["report_data"]["emissions"]["energy_emissions"],
            "waste_emissions": report["report_data"]["emissions"]["waste_emissions"],
            "travel_emissions": report["report_data"]["emissions"]["travel_emissions"],
            "total_emissions": report["report_data"]["emissions"]["total_emissions"]
        }
        companies_data.append(company_data)

    df = pd.DataFrame(companies_data)

    # Analysis of the company with the lowest emissions
    min_emissions_company = df.loc[df["total_emissions"].idxmin()]
    st.subheader("Company with the Lowest Emissions")
    st.write(f"**{min_emissions_company['org_name']}** has the lowest total CO2 emissions: {min_emissions_company['total_emissions']} KG.")

    # Analysis of the company with the highest emissions
    high_emissions_company = df.loc[df["total_emissions"].idxmax()]
    st.subheader("Company with the Hightes Emissions")
    st.write(f"**{high_emissions_company['org_name']}** has the highest total CO2 emissions: {high_emissions_company['total_emissions']} KG.")


    # Table of consumptions
    st.subheader("Consumption")
    df_display = df[["org_name", "electricity", "natural_gas", "fuel", "waste", "waste_recycled", "kilometers", "efficiency"]]
    st.dataframe(df_display)

    # Graph for visualize consumptions 
    st.subheader("Consumption Graph")
    fig, ax = plt.subplots(figsize=(10, 6))
    df_display = df[["org_name", "electricity", "natural_gas", "fuel", "waste", "waste_recycled", "kilometers", "efficiency"]]
    df_display.set_index("org_name", inplace=True)
    df_display.plot(kind="bar", ax=ax)
    plt.title("Consumptions of the Companies")
    plt.ylabel("Value")
    plt.xticks(rotation=45)
    st.pyplot(fig)


    # Table of emissions
    st.subheader("Emissions")
    df_display = df[["org_name","energy_emissions", "waste_emissions", "travel_emissions", "total_emissions"]]
    st.dataframe(df_display)

    # Graph for visualize emissions
    st.subheader("Emissions Graph")
    fig, ax = plt.subplots(figsize=(10, 6))
    df_display  =df[["org_name", "energy_emissions", "waste_emissions", "travel_emissions", "total_emissions"]]
    df_display.set_index("org_name", inplace=True)
    df_display.plot(kind="bar", ax=ax)
    plt.title("Emissions of the Companies")
    plt.ylabel("Emissions")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    #CO2 Emissions per Employee Table
    st.subheader("CO2 Emissions per Employee")
    df['emissions_per_employee'] = df['total_emissions'] / df['employees']
    df_emissions_per_employee = df[["org_name", "emissions_per_employee"]]
    st.dataframe(df_emissions_per_employee)

else:
    st.warning("It seems that there are no records yet!")
