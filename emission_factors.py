"""
Enhanced Emission Factors Database for YourCarbonFootprint Application.
Includes calculation, validation, search, and summary features.
"""

import json

# ---------------------------------------------------------
# EMISSION FACTORS DATABASE
# ---------------------------------------------------------
EMISSION_FACTORS = {
    # Scope 1 - Direct emissions
    "Stationary Combustion": {
        "Natural Gas": {"factor": 0.18316, "unit": "kWh"},
        "Diesel": {"factor": 2.68787, "unit": "liter"},
        "LPG": {"factor": 1.55537, "unit": "kg"},
        "Coal": {"factor": 2.42287, "unit": "kg"},
    },
    "Mobile Combustion": {
        "Petrol/Gasoline": {"factor": 2.31495, "unit": "liter"},
        "Diesel": {"factor": 2.70553, "unit": "liter"},
        "LPG": {"factor": 1.55537, "unit": "liter"},
        "CNG": {"factor": 2.53721, "unit": "kg"},
    },
    "Refrigerants": {
        "R-410A": {"factor": 2088.0, "unit": "kg"},
        "R-134a": {"factor": 1430.0, "unit": "kg"},
        "R-404A": {"factor": 3922.0, "unit": "kg"},
        "R-407C": {"factor": 1774.0, "unit": "kg"},
    },

    # Scope 2 - Indirect emissions
    "Electricity": {
        "India Grid": {"factor": 0.82, "unit": "kWh"},
        "Indonesia Grid": {"factor": 0.87, "unit": "kWh"},
        "Japan Grid": {"factor": 0.47, "unit": "kWh"},
        "Solar Power": {"factor": 0.041, "unit": "kWh"},
        "Wind Power": {"factor": 0.011, "unit": "kWh"},
    },
    "Steam": {"Purchased Steam": {"factor": 0.19, "unit": "kg"}},
    "District Cooling": {"District Cooling": {"factor": 0.12, "unit": "kWh"}},

    # Scope 3 - Other indirect
    "Business Travel": {
        "Short-haul Flight": {"factor": 0.15298, "unit": "passenger-km"},
        "Long-haul Flight": {"factor": 0.19085, "unit": "passenger-km"},
        "Train": {"factor": 0.03694, "unit": "passenger-km"},
        "Bus": {"factor": 0.10471, "unit": "passenger-km"},
        "Taxi": {"factor": 0.14549, "unit": "km"},
    },
    "Employee Commuting": {
        "Car (Petrol/Gasoline)": {"factor": 0.17336, "unit": "km"},
        "Car (Diesel)": {"factor": 0.16844, "unit": "km"},
        "Motorcycle": {"factor": 0.11501, "unit": "km"},
        "Bus": {"factor": 0.10471, "unit": "passenger-km"},
        "Train/Metro": {"factor": 0.03694, "unit": "passenger-km"},
    },
    "Waste": {
        "Landfill": {"factor": 0.45727, "unit": "kg"},
        "Recycling": {"factor": 0.01042, "unit": "kg"},
        "Composting": {"factor": 0.01042, "unit": "kg"},
        "Incineration": {"factor": 0.01613, "unit": "kg"},
    },
    "Water": {
        "Water Supply": {"factor": 0.344, "unit": "cubic meter"},
        "Water Treatment": {"factor": 0.708, "unit": "cubic meter"},
    },
    "Purchased Goods & Services": {
        "Paper": {"factor": 0.919, "unit": "kg"},
        "Plastic": {"factor": 3.14, "unit": "kg"},
        "Glass": {"factor": 0.85, "unit": "kg"},
        "Metal": {"factor": 1.37, "unit": "kg"},
        "Food": {"factor": 3.59, "unit": "kg"},
    },
}

SCOPE_CATEGORIES = {
    "Scope 1": ["Stationary Combustion", "Mobile Combustion", "Refrigerants"],
    "Scope 2": ["Electricity", "Steam", "District Cooling"],
    "Scope 3": [
        "Business Travel", "Employee Commuting", "Waste", "Water", "Purchased Goods & Services"
    ]
}

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def get_emission_factor(category, activity):
    return EMISSION_FACTORS.get(category, {}).get(activity)

def get_activities(category):
    return list(EMISSION_FACTORS.get(category, {}).keys())

def get_categories(scope):
    return SCOPE_CATEGORIES.get(scope, [])

def get_unit(category, activity):
    ef = get_emission_factor(category, activity)
    return ef["unit"] if ef else None

# ---------------------------------------------------------
# NEW FEATURES
# ---------------------------------------------------------

def calculate_emission(category, activity, amount):
    """Compute total emissions in kgCO2e."""
    ef = get_emission_factor(category, activity)
    if ef:
        total = ef["factor"] * amount
        return round(total, 4)
    else:
        raise ValueError(f"Invalid category/activity: {category} -> {activity}")

def search_activity(keyword):
    """Search for activities containing a keyword (case-insensitive)."""
    keyword = keyword.lower()
    results = []
    for cat, acts in EMISSION_FACTORS.items():
        for act in acts:
            if keyword in act.lower():
                results.append((cat, act, acts[act]["factor"], acts[act]["unit"]))
    return results

def total_emission_by_scope(scope, usage_dict):
    """
    Compute total emissions for a scope.
    usage_dict example:
      {"Electricity": {"India Grid": 1000}, "Steam": {"Purchased Steam": 200}}
    """
    total = 0.0
    for category, acts in usage_dict.items():
        for act, amt in acts.items():
            try:
                total += calculate_emission(category, act, amt)
            except ValueError:
                continue
    return round(total, 4)

def update_emission_factor(category, activity, new_factor, unit=None):
    """Update or add a new emission factor dynamically."""
    if category not in EMISSION_FACTORS:
        EMISSION_FACTORS[category] = {}
    EMISSION_FACTORS[category][activity] = {
        "factor": new_factor,
        "unit": unit or EMISSION_FACTORS[category].get(activity, {}).get("unit", "unit")
    }

def export_to_json(filename="emission_factors.json"):
    """Save current emission data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(EMISSION_FACTORS, f, indent=4)
    print(f"✅ Emission factors exported to {filename}")


# Example 1: Calculate emissions for electricity use
emission = calculate_emission("Electricity", "India Grid", 1500)
print(f"Total Emission: {emission} kgCO2e")

# Example 2: Search for “diesel”
print(search_activity("diesel"))

# Example 3: Get total for Scope 2
usage_data = {"Electricity": {"India Grid": 1000}, "Steam": {"Purchased Steam": 300}}
print(total_emission_by_scope("Scope 2", usage_data))

# Example 4: Update emission factor dynamically
update_emission_factor("Electricity", "Pakistan Grid", new_factor=0.79, unit="kWh")







# Summary of Improvements
#Improvement	Description
#Emission calculation	Added calculate_emission()
#Input validation	Raises clear errors for invalid inputs
#Search feature	Find emission activities quickly
#Scope summary	Compute totals for a given scope
# JSON export	Store or share updated database
# Dynamic update	Adjust factors for local datasets
#Ready for Streamlit	Functions cleanly integrate with forms or sliders