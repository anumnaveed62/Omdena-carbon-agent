#✅ Enhanced Version of Your Code (with Improvements & Added Comments)

#Data handler for YourCarbonFootprint application.
#Handles data import, export, reporting, and analytics for emission records.
#Includes error handling, data validation, and plotting utilities.

import pandas as pd
import json
import os
from datetime import datetime
from io import StringIO
from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Import emission factor helpers
from emission_factors import get_emission_factor, get_categories, get_activities

# ================================
# Configuration and Constants
# ================================
DATA_DIR = "data"
EMISSIONS_FILE = os.path.join(DATA_DIR, "emissions.json")
COMPANY_INFO_FILE = os.path.join(DATA_DIR, "company_info.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Configure logging for debug & audit tracking
logging.basicConfig(
    filename="datahandler.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s"
)

# ================================
# DataHandler Class
# ================================
class DataHandler:
    """Handles all data storage, retrieval, and processing for emissions."""

    def __init__(self):
        """Initialize and load data when the handler is created."""
        self.load_emissions_data()
        self.load_company_info()

    # -----------------------------------------------------------
    # DATA LOADING & INITIALIZATION
    # -----------------------------------------------------------
    def load_emissions_data(self):
        """Load emissions data from JSON file, or initialize if missing."""
        try:
            if os.path.exists(EMISSIONS_FILE):
                with open(EMISSIONS_FILE, 'r') as f:
                    data = json.load(f)
                    self.emissions_data = pd.DataFrame(data)
                    if 'date' in self.emissions_data.columns:
                        self.emissions_data['date'] = pd.to_datetime(self.emissions_data['date'])
            else:
                self.create_empty_emissions_data()
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.warning(f"Error loading emissions data: {e}")
            self.create_empty_emissions_data()

    def create_empty_emissions_data(self):
        """Create a blank DataFrame for emissions."""
        self.emissions_data = pd.DataFrame(columns=[
            'date', 'scope', 'category', 'activity',
            'quantity', 'unit', 'emission_factor',
            'emissions_kgCO2e', 'notes'
        ])

    def load_company_info(self):
        """Load company info or initialize blank structure."""
        try:
            if os.path.exists(COMPANY_INFO_FILE):
                with open(COMPANY_INFO_FILE, 'r') as f:
                    self.company_info = json.load(f)
            else:
                self.create_empty_company_info()
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.warning(f"Error loading company info: {e}")
            self.create_empty_company_info()

    def create_empty_company_info(self):
        """Create a blank company information record."""
        self.company_info = {
            "name": "",
            "industry": "",
            "location": "",
            "export_markets": [],
            "contact_person": "",
            "email": "",
            "phone": "",
            "address": "",
            "registration_number": "",
            "reporting_year": datetime.now().year
        }

    # -----------------------------------------------------------
    # DATA SAVING METHODS
    # -----------------------------------------------------------
    def save_emissions_data(self):
        """Save current emissions dataset to JSON."""
        try:
            df = self.emissions_data.copy()
            if 'date' in df.columns:
                df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            with open(EMISSIONS_FILE, 'w') as f:
                json.dump(df.to_dict('records'), f, indent=2)
        except Exception as e:
            logging.error(f"Error saving emissions data: {e}")

    def save_company_info(self):
        """Save company info to file."""
        try:
            with open(COMPANY_INFO_FILE, 'w') as f:
                json.dump(self.company_info, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving company info: {e}")

    # -----------------------------------------------------------
    # ADD / UPDATE ENTRIES
    # -----------------------------------------------------------
    def add_emission_entry(self, date, scope, category, activity, quantity, unit, emission_factor, notes=""):
        """Add new emission entry after validating data."""
        try:
            # Validation checks
            if not all([scope, category, activity, quantity, emission_factor]):
                raise ValueError("Missing mandatory fields for emission entry.")

            # Calculate emissions
            emissions_kgCO2e = float(quantity) * float(emission_factor)

            # Append record
            new_entry = pd.DataFrame([{
                'date': pd.Timestamp(date),
                'scope': scope,
                'category': category,
                'activity': activity,
                'quantity': float(quantity),
                'unit': unit,
                'emission_factor': float(emission_factor),
                'emissions_kgCO2e': emissions_kgCO2e,
                'notes': notes
            }])

            self.emissions_data = pd.concat([self.emissions_data, new_entry], ignore_index=True)
            self.save_emissions_data()

            logging.info(f"Added new emission entry for {activity} ({scope})")
            return True
        except Exception as e:
            logging.error(f"Error adding emission entry: {e}")
            return False

    # -----------------------------------------------------------
    # IMPORT / EXPORT FUNCTIONS
    # -----------------------------------------------------------
    def import_csv(self, file_path_or_buffer):
        """Import emission data from a CSV file."""
        try:
            df = pd.read_csv(file_path_or_buffer)
            required = ['date', 'scope', 'category', 'activity', 'quantity', 'unit', 'emission_factor']
            missing = [c for c in required if c not in df.columns]
            if missing:
                return False, f"Missing required columns: {', '.join(missing)}"

            df['date'] = pd.to_datetime(df['date'])
            df['emissions_kgCO2e'] = df['quantity'].astype(float) * df['emission_factor'].astype(float)
            if 'notes' not in df.columns:
                df['notes'] = ""

            self.emissions_data = pd.concat([self.emissions_data, df], ignore_index=True)
            self.save_emissions_data()
            return True, f"Successfully imported {len(df)} entries."
        except Exception as e:
            logging.error(f"Error importing CSV: {e}")
            return False, str(e)

    def export_csv(self, file_path=None, start_date=None, end_date=None):
        """Export filtered emissions to CSV."""
        try:
            data = self.get_filtered_data(start_date, end_date)
            data['date'] = data['date'].dt.strftime('%Y-%m-%d')
            if file_path:
                data.to_csv(file_path, index=False)
                logging.info(f"Exported emissions to {file_path}")
                return True
            else:
                buffer = StringIO()
                data.to_csv(buffer, index=False)
                return buffer.getvalue()
        except Exception as e:
            logging.error(f"Error exporting CSV: {e}")
            return False

    # -----------------------------------------------------------
    # REPORT GENERATION
    # -----------------------------------------------------------
    def generate_pdf_report(self, file_path=None, start_date=None, end_date=None):
        """Generate detailed PDF emissions report."""
        try:
            data = self.get_filtered_data(start_date, end_date)
            if data.empty:
                raise ValueError("No data available for selected range.")

            total = data['emissions_kgCO2e'].sum()
            scope_summary = data.groupby('scope')['emissions_kgCO2e'].sum().reset_index()

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Carbon Emissions Report", 0, 1, "C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d')}", 0, 1)
            pdf.cell(0, 10, f"Total Emissions: {total:.2f} kgCO2e", 0, 1)
            pdf.ln(5)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Scope Breakdown:", 0, 1)
            pdf.set_font("Arial", "", 10)
            for _, r in scope_summary.iterrows():
                percent = (r['emissions_kgCO2e'] / total) * 100
                pdf.cell(0, 8, f"{r['scope']}: {r['emissions_kgCO2e']:.2f} kgCO2e ({percent:.1f}%)", 0, 1)

            if file_path:
                pdf.output(file_path)
                logging.info(f"PDF report generated: {file_path}")
                return True
            else:
                return pdf.output(dest='S').encode('latin1')
        except Exception as e:
            logging.error(f"Error generating PDF: {e}")
            return False

    # -----------------------------------------------------------
    # SUMMARY & FILTER FUNCTIONS
    # -----------------------------------------------------------
    def get_emissions_summary(self):
        """Generate summary of total emissions by scope, category, and time."""
        if self.emissions_data.empty:
            return {"total_emissions": 0, "scope_breakdown": {}, "category_breakdown": {}, "time_series": {}}

        total = self.emissions_data['emissions_kgCO2e'].sum()
        scope = self.emissions_data.groupby('scope')['emissions_kgCO2e'].sum().to_dict()
        category = self.emissions_data.groupby('category')['emissions_kgCO2e'].sum().to_dict()

        # Monthly breakdown
        self.emissions_data['month'] = self.emissions_data['date'].dt.strftime('%Y-%m')
        time_series = self.emissions_data.groupby(['month', 'scope'])['emissions_kgCO2e'].sum().unstack().fillna(0)

        return {
            "total_emissions": total,
            "scope_breakdown": scope,
            "category_breakdown": category,
            "time_series": time_series.to_dict()
        }

    def get_filtered_data(self, start_date=None, end_date=None, scope=None, category=None):
        """Filter emissions data by time range, scope, or category."""
        data = self.emissions_data.copy()
        if start_date and end_date:
            mask = (data['date'] >= pd.Timestamp(start_date)) & (data['date'] <= pd.Timestamp(end_date))
            data = data.loc[mask]
        if scope:
            data = data[data['scope'] == scope]
        if category:
            data = data[data['category'] == category]
        return data