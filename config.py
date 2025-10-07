"""
Configuration settings for YourCarbonFootprint application.
Centralized configuration file to manage environment variables, 
default settings, constants, and metadata for the application.
"""

import os
from dotenv import load_dotenv

# ---------------------------------------------------------------------
# Load environment variables securely from .env file
# ---------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------
# Application metadata
# ---------------------------------------------------------------------
APP_NAME = "YourCarbonFootprint"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = (
    "A lightweight, multilingual carbon accounting and reporting tool "
    "for SMEs in Asia, enabling better sustainability reporting and compliance."
)
APP_AUTHOR = "Sonu Kumar"
APP_CONTACT = "sonu@aianytime.net"

# ---------------------------------------------------------------------
# API keys and sensitive credentials
# ---------------------------------------------------------------------
# It's better to use environment variables for sensitive keys (never hardcode)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "")

# ---------------------------------------------------------------------
# Data directories and file storage paths
# ---------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")

EMISSIONS_FILE = os.path.join(DATA_DIR, "emissions.json")
COMPANY_INFO_FILE = os.path.join(DATA_DIR, "company_info.json")

# Ensure necessary directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)

# ---------------------------------------------------------------------
# Language and localization settings
# ---------------------------------------------------------------------
SUPPORTED_LANGUAGES = ["English", "Hindi", "Chinese", "Malay"]
DEFAULT_LANGUAGE = "English"

# ---------------------------------------------------------------------
# Emission scopes and descriptions
# ---------------------------------------------------------------------
EMISSION_SCOPES = ["Scope 1", "Scope 2", "Scope 3"]

SCOPE_DESCRIPTIONS = {
    "Scope 1": "Direct emissions from owned or controlled sources (e.g., fuel combustion).",
    "Scope 2": "Indirect emissions from the generation of purchased electricity, steam, heating, or cooling.",
    "Scope 3": (
        "All other indirect emissions occurring in a company’s value chain, "
        "including purchased goods, waste, transport, and employee commuting."
    ),
}

# ---------------------------------------------------------------------
# Measurement units (for emission factors and activity data)
# ---------------------------------------------------------------------
DEFAULT_UNITS = [
    "kWh", "MWh", "liter", "kg", "tonne", "km", "passenger-km",
    "cubic meter", "square meter", "hour", "day", "piece", "USD"
]

# ---------------------------------------------------------------------
# Regulatory frameworks (expandable list)
# ---------------------------------------------------------------------
REGULATORY_FRAMEWORKS = {
    "EU CBAM": "EU Carbon Border Adjustment Mechanism",
    "Japan GX League": "Japan Green Transformation League",
    "Indonesia ETS/ETP": "Indonesia Emissions Trading System/Emissions Trading Program",
    "India PAT": "Perform, Achieve, and Trade (Energy Efficiency Trading Scheme)",
    "Singapore Carbon Tax": "National carbon pricing scheme for emissions above 25,000 tCO2e"
}

# ---------------------------------------------------------------------
# Logging and debug settings
# ---------------------------------------------------------------------
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ---------------------------------------------------------------------
# Default visualization colors (for reports and charts)
# ---------------------------------------------------------------------
THEME_COLORS = {
    "scope1": "#2E86C1",  # Blue
    "scope2": "#28B463",  # Green
    "scope3": "#CA6F1E",  # Orange
    "total": "#7D3C98"    # Purple
}
