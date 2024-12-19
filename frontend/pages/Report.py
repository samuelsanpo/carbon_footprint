import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Carbon Footprint",
    page_icon="🌳", 
)

BACKEND_URL = "http://localhost:5000"

report_id = st.session_state.get("report_id", None)
report_url = f"{BACKEND_URL}/reports/report_{report_id}.pdf"
#Here my initial idea was to show an iframe with the pdf file to the user, plus the option to download, 
# but to consume the iframe required to change my method in flask to https which would entail the generation 
# of the ssl certificate and a lot of extra work so as an alternative I decided to modify the post method to save 
# the most important information of the report with which I perform the preview of the information and then I have 
# the download button that consumes the method that allows me to download the pdf file saved in the mini service with flask.
if report_id:
    st.title("Report")
    try:
        response = requests.get(f"{BACKEND_URL}/get_report_data?report_id={report_id}")
        if response.status_code == 200:
            report_data = response.json()

            st.write(f"**The following is a preview of the report, to view the full report please download it.**")
            
            st.subheader("Organization Details")
            st.write(f"**Organization Name**: {report_data['organization']['org_name']}")
            st.write(f"**Industry**: {report_data['organization']['industry']}")
            st.write(f"**Number of Employees**: {report_data['organization']['employees']}")

            # Display emissions data
            st.subheader("Emissions Data")
            st.write(f"**Energy Emissions (kgCO2)**: {report_data['emissions']['energy_emissions']:.2f}")
            st.write(f"**Waste Emissions (kgCO2)**: {report_data['emissions']['waste_emissions']:.2f}")
            st.write(f"**Travel Emissions (kgCO2)**: {report_data['emissions']['travel_emissions']:.2f}")
            st.write(f"**Total Emissions (kgCO2)**: {report_data['emissions']['total_emissions']:.2f}")

            # Display CO2 recommendations
            st.subheader("CO2 Reduction Recommendations")
            st.write(report_data['co2_recommendation']['message'])
            for tip in report_data['co2_recommendation']['tips']:
                st.write(f"- {tip}")

            # Download button
            response_pdf = requests.get(report_url)
            if response_pdf.status_code == 200:
                st.download_button(
                    label="Download PDF",
                    data=response_pdf.content,
                    file_name=f"report_{report_id}.pdf",
                    mime="application/pdf",
                )
            else:
                st.error("Failed to fetch the report.")
            
        else:
            st.error("Something wrong, the ID was not loaded, please select the report from the reports section.")

    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

    if st.button("Back to Reports"):
        switch_page("Reports")

else:
    st.error("Something wrong, the ID was not loaded, please select the report from the reports section.")
    if st.button("Reports"):
      switch_page("Reports")