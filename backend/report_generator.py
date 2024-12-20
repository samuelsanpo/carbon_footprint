from fpdf import FPDF
import json
from utils import calculate_emissions, get_co2_recommendations, get_recommendations

#In this page I create the report with the fpdf library, I assign the different fields with the structure, 
# it is a simple structure but it contains the required information.
def generate_report(data, file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Carbon Footprint Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Organization Name: {data.get('org_name', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Industry: {data.get('industry', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Number of Employees: {data.get('employees', 'N/A')}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(200, 10, txt="Metrics", ln=True)
    pdf.ln(5)


    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Electricity Consumption (Euros/month): {data.get("electricity", 0.0)}", ln=True)
    pdf.cell(200, 10, txt=f"Natural Gas Consumption (Euros/month): {data.get("natural_gas", 0.0)}", ln=True)
    pdf.cell(200, 10, txt=f"Fuel Consumption (Euros/month): {data.get("fuel", 0.0)}", ln=True)
    pdf.cell(200, 10, txt=f"Waste Generated (kg/month): {data.get("waste", 0.0)}", ln=True)
    pdf.cell(200, 10, txt=f"Recycling Rate (%/month): {data.get("waste_recycled", 0.0)}", ln=True)
    pdf.cell(200, 10, txt=f"Business Kilometers (km/year): {data.get("kilometers", 0.0)}", ln=True)
    pdf.cell(200, 10, txt=f"Fuel Efficiency (L/100km): {data.get("efficiency", 0.0)}", ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(200, 10, txt="Results", ln=True)
    pdf.ln(5)

    #I use the emissions calculation method that returns the emissions values ​​that I use later.
    emissions_data = calculate_emissions(
        data.get("electricity", 0.0),
        data.get("natural_gas", 0.0),
        data.get("fuel", 0.0),
        data.get("waste", 0.0),
        data.get("waste_recycled", 0.0),
        data.get("kilometers", 0.0),
        data.get("efficiency", 0.0)
    )

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Energy Emissions (kgCO2): {emissions_data['energy_emissions']:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Waste Emissions (kgCO2): {emissions_data['waste_emissions']:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Travel Emissions (kgCO2): {emissions_data['travel_emissions']:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total Emissions (kgCO2): {emissions_data['total_emissions']:.2f}", ln=True)
    pdf.ln(5)

    total_emissions_value = emissions_data['total_emissions']
    #Here I call get recommendations co2 to bring the recommendations regarding the carbon footprint value.
    co2_recommendation = get_co2_recommendations(total_emissions_value)

    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, txt="Overall Carbon Emissions Recommendations", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"Recommendation: {co2_recommendation['message']}")
    pdf.ln(2)
    for tip in co2_recommendation['tips']:
        pdf.cell(200, 10, txt=f"- {tip}", ln=True)
    pdf.ln(5)

    report_data = {
        "organization": {
            "org_name": data.get('org_name', 'N/A'),
            "industry": data.get('industry', 'N/A'),
            "employees": data.get('employees', 'N/A')
        },
        "emissions": emissions_data,
        "co2_recommendation": co2_recommendation,  
    }

    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(200, 10, txt="Recommendations for each of the items", ln=True)
    pdf.ln(5)

    metrics = [
        ("Electricity Consumption", data.get("electricity", 0.0), "electricity"),
        ("Natural Gas Consumption", data.get("natural_gas", 0.0), "gas"),
        ("Fuel Consumption", data.get("fuel", 0.0), "fuel"),
        ("Waste Generated", data.get("waste", 0.0), "waste"),
        ("Recycling Rate", data.get("waste_recycled", 0.0), "recycling"),
        ("Business Kilometers", data.get("kilometers", 0.0), "travel"),
        ("Fuel Efficiency", data.get("efficiency", 0.0), "efficiency"),
    ]

    #I call get the recommendations for each individual item.
    for metric_name, value, recommendation_key in metrics:
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"{metric_name}: {value}", ln=True)

        recommendation = get_recommendations(value, recommendation_key)
        pdf.multi_cell(0, 10, txt=f"Recommendation: {recommendation['message']}")
        
        for tip in recommendation['tips']:
            pdf.cell(200, 10, txt=f"- {tip}", ln=True)
        
        pdf.ln(5)

    pdf.output(file_path)

    return report_data 