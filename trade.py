# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 22:15:10 2025

@author: Gandalf The Grey
"""

import pandas as pd

# Read the trade data
wheat_trade_raw = pd.read_csv("Trade.csv")

# Filter for wheat-related import and export data in 2023
wheat_filtered = wheat_trade_raw[
    (wheat_trade_raw["Year"] == 2023) &
    (wheat_trade_raw["Item"] == "Wheat") &
    (wheat_trade_raw["Element"].isin(["Import quantity", "Export quantity"]))
]

# Reshape data to show import and export side-by-side for each country
wheat_pivot = wheat_filtered.pivot_table(
    index="Area",
    columns="Element",
    values="Value",
    aggfunc="sum"
).reset_index()

# Rename columns for clarity
wheat_pivot.columns.name = None
wheat_pivot = wheat_pivot.rename(columns={
    "Area": "Country",
    "Import quantity": "Wheat_Import_2023",
    "Export quantity": "Wheat_Export_2023"
})

# Manually check and convert values to numeric format
# No errors='coerce' used
def safe_float(val):
    try:
        return float(val)
    except:
        return None

wheat_pivot["Wheat_Import_2023"] = wheat_pivot["Wheat_Import_2023"].apply(safe_float)
wheat_pivot["Wheat_Export_2023"] = wheat_pivot["Wheat_Export_2023"].apply(safe_float)

# Remove rows with invalid (non-numeric) entries
wheat_pivot = wheat_pivot[
    wheat_pivot["Wheat_Import_2023"].notna() | wheat_pivot["Wheat_Export_2023"].notna()
]

# Map country names to align with GIS shapefile naming conventions
country_name_map = {
    "Antigua and Barbuda": "Antigua and Barb.",
    "Bahamas": "The Bahamas",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Brunei Darussalam": "Brunei",
    "Cabo Verde": "Cape Verde",
    "China, Hong Kong SAR": "Hong Kong",
    "China, Macao SAR": "Macau",
    "China, Taiwan Province of": "Taiwan",
    "China, mainland": "China",
    "Congo": "Republic of the Congo",
    "Cook Islands": "Cook Is.",
    "Côte d'Ivoire": "Ivory Coast",
    "Democratic People's Republic of Korea": "North Korea",
    "Eswatini": "Swaziland",
    "Faroe Islands": "Faeroe Is.",
    "French Polynesia": "Fr. Polynesia",
    "Iran (Islamic Republic of)": "Iran",
    "Netherlands (Kingdom of the)": "Netherlands",
    "Republic of Korea": "South Korea",
    "Republic of Moldova": "Moldova",
    "Russian Federation": "Russia",
    "Saint Lucia": "St. Lucia",
    "Saint Vincent and the Grenadines": "St. Vin. and Gren.",
    "Syrian Arab Republic": "Syria",
    "Türkiye": "Turkey",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    "Viet Nam": "Vietnam"
}

wheat_pivot["Country_Mapped"] = wheat_pivot["Country"].replace(country_name_map)

# Export to CSV in a GIS-compatible format
wheat_pivot.to_csv("merged_trade.csv", index=False, float_format="%.2f")

print("✅ Trade data successfully cleaned and saved as 'merged_trade.csv'")