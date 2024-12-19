import json

#Below are the individual emissions of energy, waste and travel, which I have rounded up so that the values ​​are easier to visualize.
def calculate_energy_emissions(electricity, gas, fuel):
    electricity_emissions = electricity * 12 * 0.0005
    gas_emissions = gas * 12 * 0.0053
    fuel_emissions = fuel * 12 * 2.32
    
    emissions = electricity_emissions + gas_emissions + fuel_emissions
    return round(emissions,2)

def calculate_waste_emissions(waste, recycling_percentage):
    recycling_percentage_decimal = recycling_percentage / 100  
    emissions = waste * 12 * (0.57-recycling_percentage_decimal)
    return round(emissions,2)

def calculate_travel_emissions(kms, fuel_efficiency):
    fuel_consumption = kms / fuel_efficiency
    emissions = fuel_consumption * 2.31
    return round(emissions,2)

#Here I calculate the total emissions with the total sum of the other.
def calculate_emissions(electricity, gas, fuel, 
                              waste, recycling_percentage, 
                              kms, fuel_efficiency):
    
    # Individual emissions
    energy_emissions = calculate_energy_emissions(electricity, gas, fuel)
    waste_emissions = calculate_waste_emissions(waste, recycling_percentage)
    travel_emissions = calculate_travel_emissions(kms, fuel_efficiency)
    
    # Total emissions
    total_emissions = energy_emissions + waste_emissions + travel_emissions
    
    # Return results as a dictionary
    return {
        "energy_emissions": energy_emissions,
        "waste_emissions": waste_emissions,
        "travel_emissions": travel_emissions,
        "total_emissions": total_emissions
    }


def get_co2_recommendations(total_emissions):
    # To assume these value thresholds, I asked chat GPT for advice, focusing on an organization in general, 
    # regardless of its size.
    if total_emissions < 1000:
        level = 'low'
    elif total_emissions < 5000:
        level = 'moderate'
    else:
        level = 'high'

    with open("data/recommendations.json", 'r') as f:
        recommendations = json.load(f)

    co2_recommendation = recommendations['recommendations']['co2'][level]
    return co2_recommendation



# This is a dynamic function that returns the recommendations that you create in the recommendations json, 
# then depending on the key and the threshold in which the sent value is found, it returns certain recommendations 
# to the user that I mapped in the report.
def get_recommendations(value, key):

    with open("data/recommendations.json", 'r') as f:
        recommendations = json.load(f)


    #I also asked chat GPT for advice on these value thresholds, focusing on an organization in general, 
    # regardless of its size. For the case of electricity, gas and fuel, I asked them to help me by giving 
    # me values close to the current reality in Germany.
    conversion_factors = {
        "electricity": 2.86,  # 1 EUR ≈ 2.86 kWh 
        "natural_gas": 14.29,  # 1 EUR ≈ 14.29 m³ 
        "fuel": 0.645,         # 1 EUR ≈ 0.645 L
    }

    #In the thresholds I use the recommended values and I use the positive infitive in python float("inf") for the High 
    # values except for recycling because is percentage.

    thresholds = {
        "electricity": {
            "low": 100,         # kWh/mes
            "moderate": 300,    # kWh/mes
            "high": float("inf")  
        },
        "gas": {
            "low": 50,          # m3/mes
            "moderate": 150,    # m3/mes
            "high": float("inf")
        },
        "fuel": {
            "low": 60,          # L/mes
            "moderate": 150,    # L/mes
            "high": float("inf")
        },
        "waste": {
            "low": 50,          # kg/mes
            "moderate": 150,    # kg/mes
            "high": float("inf")
        },
        "recycling": {
            "low": 30,          # %
            "moderate": 60,     # %
            "high": 100         # %
        },
        "travel": {
            "low": 1000,        # km/año
            "moderate": 5000,   # km/año
            "high": float("inf")
        },
        "efficiency": {
            "low": 10,          # L/100 km
            "moderate": 7,      # L/100 km
            "high": float("inf")
        }
    }

    if key in conversion_factors:
        value_in_units = value * conversion_factors[key]
    else:
        value_in_units = value  #

    threshold = thresholds.get(key)

    if value_in_units <= threshold["low"]:
        return recommendations["recommendations"][key]["low"]
    elif value_in_units <= threshold["moderate"]:
        return recommendations["recommendations"][key]["moderate"]
    else:
        return recommendations["recommendations"][key]["high"]
