# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 11:12:51 2025

@author: Gandalf The Grey
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the FAOSTAT-style dataset containing crop production values
wheat_production = pd.read_csv("Area_Production.csv")

# Select only global-level data for the year 2023 and the element 'Production'
world_production = wheat_production[
    (wheat_production["Area"] == "World") &
    (wheat_production["Year"] == 2023) &
    (wheat_production["Element"] == "Production")
]

# Convert production values from tonnes to million tonnes for easier interpretation
world_production["Production_Mt"] = world_production["Value"] / 1e6

# Prepare a table with crop types as index and production values as a column
production_table = world_production[["Item", "Production_Mt"]].set_index("Item")

# Sort the data in descending order to improve readability of the heatmap
production_table = production_table.sort_values("Production_Mt", ascending=False)

# Initialize the figure
plt.figure(figsize=(8, 6))

# Create the heatmap
sns.heatmap(
    production_table,
    annot=True,                      # Show values on the heatmap
    fmt=".1f",                       # Format to one decimal place
    cmap="YlGnBu",                   # Color scheme
    linewidths=0.5,                  # Line between cells
    cbar_kws={'label': 'Production (Million Tonnes)'}  # Color bar label
)

# Add a title and remove axis labels for a cleaner appearance
plt.title("Cereal Production by Crop Type (2023)", fontsize=13)
plt.xlabel("")
plt.ylabel("")
plt.tight_layout()

# Save the heatmap to a file
plt.savefig("heatmap_cereal_production_2023.png", dpi=300)
