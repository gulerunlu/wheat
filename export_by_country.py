# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 13:07:11 2025

@author: Gandalf The Grey
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file containing 2003 and 2023 wheat export data
df = pd.read_excel("exports_by_country.xlsx")

# Select relevant columns and rename them
df_clean = df[["Country", 2003, 2023]].copy()
df_clean.columns = ["Country", "Export_2003", "Export_2023"]

# Remove rows with missing or zero export values
df_clean = df_clean[(df_clean["Export_2003"] > 0) | (df_clean["Export_2023"] > 0)].dropna()

# Convert values from 1000 MT to metric tons
df_clean["Export_2003"] = df_clean["Export_2003"] * 1000
df_clean["Export_2023"] = df_clean["Export_2023"] * 1000

# Calculate total global exports for each year
total_2003 = df_clean["Export_2003"].sum()
total_2023 = df_clean["Export_2023"].sum()

# Calculate each country's share of global exports and the percentage point change
df_clean["Share_2003"] = (df_clean["Export_2003"] / total_2003) * 100
df_clean["Share_2023"] = (df_clean["Export_2023"] / total_2023) * 100
df_clean["Change_pp"] = df_clean["Share_2023"] - df_clean["Share_2003"]

# Select the top 15 countries by export share in 2023
df_top15 = df_clean.sort_values(by="Share_2023", ascending=False).head(15).reset_index(drop=True)

# Sort countries by change in share for diverging effect
df_top15_sorted = df_top15.sort_values(by="Change_pp", ascending=True).reset_index(drop=True)
colors = ['salmon' if x >= 0 else 'skyblue' for x in df_top15_sorted["Change_pp"]]

# Create a side-by-side figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9))

# Dumbbell Plot (left)
for i, row in df_top15.iterrows():
    ax1.plot([row['Share_2003'], row['Share_2023']], [i, i], 'k-', lw=1)
    ax1.plot(row['Share_2003'], i, 'o', color='skyblue', markersize=8, label='2003' if i == 0 else "")
    ax1.plot(row['Share_2023'], i, 'o', color='salmon', markersize=8, label='2023' if i == 0 else "")
    ax1.text(max(row['Share_2003'], row['Share_2023']) + 0.5, i, f"{row['Country']}", va='center', fontsize=9)

ax1.set_yticks(range(len(df_top15)))
ax1.set_yticklabels([])
ax1.set_xlabel("Global Share of Wheat Exports (%)")
ax1.set_title("Dumbbell Plot: Top 15 Wheat Exporters (2023 vs. 2003)")
ax1.grid(True, axis='x')
ax1.legend(loc='lower right')

# Horizontal Diverging Bar Plot (right) 
ax2.barh(df_top15_sorted["Country"], df_top15_sorted["Change_pp"], color=colors)
ax2.axvline(0, color='gray', lw=1)
ax2.set_xlabel("Change in Global Share (%)")
ax2.set_title("Diverging Bar Plot: Change in Wheat Export Share (2023 vs. 2003)")

# Final formatting and saving
plt.tight_layout()
plt.savefig("wheat_exports_combined_plot.png", dpi=300)
plt.show()