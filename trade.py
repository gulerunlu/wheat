# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 22:15:10 2025

@author: Gandalf The Grey
"""

import pandas as pd

# Step 1: Load the renamed FAOSTAT CSV file
df_fao = pd.read_csv("Trade.csv")

# Step 2: Filter for wheat data, year 2023, and import/export only
df_filtered = df_fao[
    (df_fao["Year"] == 2023) &
    (df_fao["Item"] == "Wheat") &
    (df_fao["Element"].isin(["Import quantity", "Export quantity"]))
]

# Step 3: Pivot table so each country has import/export side by side
df_pivot = df_filtered.pivot_table(
    index="Area",
    columns="Element",
    values="Value",
    aggfunc="sum"
).reset_index()

# Step 4: Rename columns for clarity
df_pivot.columns.name = None
df_pivot = df_pivot.rename(columns={
    "Area": "Country",
    "Import quantity": "Wheat_Import_2023",
    "Export quantity": "Wheat_Export_2023"
})

# Ensure numeric format (to prevent NULL in QGIS)
df_pivot["Wheat_Import_2023"] = pd.to_numeric(df_pivot["Wheat_Import_2023"], errors="coerce")
df_pivot["Wheat_Export_2023"] = pd.to_numeric(df_pivot["Wheat_Export_2023"], errors="coerce")

# Step 5: Create a name-matching dictionary for alignment with shapefile
country_name_map = {
    "Antigua and Barbuda": "Antigua and Barb.",
    "Bahamas": "The Bahamas",
    "Bahrain": "Bahrain",
    "Barbados": "Barbados",
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
    "Grenada": "Grenada",
    "Iran (Islamic Republic of)": "Iran",
    "Maldives": "Maldives",
    "Malta": "Malta",
    "Mauritius": "Mauritius",
    "Nauru": "Nauru",
    "Netherlands (Kingdom of the)": "Netherlands",
    "Republic of Korea": "South Korea",
    "Republic of Moldova": "Moldova",
    "Russian Federation": "Russia",
    "Saint Lucia": "St. Lucia",
    "Saint Vincent and the Grenadines": "St. Vin. and Gren.",
    "Samoa": "Samoa",
    "Serbia": "Serbia",
    "Seychelles": "Seychelles",
    "Singapore": "Singapore",
    "Syrian Arab Republic": "Syria",
    "Tuvalu": "Tuvalu",
    "Türkiye": "Turkey",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    "Viet Nam": "Vietnam"
}

# Step 6: Apply the mapping to create a consistent 'Country_Mapped' field
df_pivot["Country_Mapped"] = df_pivot["Country"].replace(country_name_map)

# Step 7: Export the cleaned dataset for use in QGIS (with proper float format)
df_pivot.to_csv("merged_trade.csv", index=False, float_format='%.2f')

print("✅ Wheat trade data has been processed and saved as 'merged_trade.csv'")
