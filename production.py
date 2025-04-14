# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 11:12:51 2025

@author: Gandalf The Grey
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the FAOSTAT-style dataset
df = pd.read_csv("Area_Production.csv")

# Filter for World-level data, year 2023, and only Production records
df_filtered = df[
    (df["Area"] == "World") &
    (df["Year"] == 2023) &
    (df["Element"] == "Production")
]

# Convert production values from tonnes to million tonnes
df_filtered["Production_Mt"] = df_filtered["Value"] / 1e6

# Prepare data for heatmap: set crop types as index
df_heatmap = df_filtered[["Item", "Production_Mt"]].set_index("Item")
df_heatmap = df_heatmap.sort_values("Production_Mt", ascending=False)

# Create the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(
    df_heatmap,
    annot=True,
    fmt=".1f",
    cmap="YlGnBu",
    linewidths=0.5,
    cbar_kws={'label': 'Production (Million Tonnes)'}
)

# Add title and format
plt.title("Cereal Production by Crop Type (2023)", fontsize=13)
plt.xlabel("")
plt.ylabel("")
plt.tight_layout()

# Export the heatmap to PNG
plt.savefig("heatmap_cereal_production_2023.png", dpi=300)
plt.show()
