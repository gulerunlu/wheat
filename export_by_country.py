# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 13:07:11 2025

@author: Gandalf The Grey
"""

import pandas as pd
import matplotlib.pyplot as plt

# Read the wheat export data from Excel
wheat_exports = pd.read_excel("exports_by_country.xlsx")

# Select and rename relevant columns for clarity
wheat_exports = wheat_exports[["Country", 2003, 2023]].copy()
wheat_exports.columns = ["Country", "Export_2003", "Export_2023"]

# Filter out countries with no export in both years
wheat_exports = wheat_exports[
    (wheat_exports["Export_2003"] > 0) | (wheat_exports["Export_2023"] > 0)
].dropna()

# Convert from thousands of metric tons to metric tons
wheat_exports["Export_2003"] = wheat_exports["Export_2003"] * 1000
wheat_exports["Export_2023"] = wheat_exports["Export_2023"] * 1000

# Compute world totals for each year
total_2003 = wheat_exports["Export_2003"].sum()
total_2023 = wheat_exports["Export_2023"].sum()

# Calculate each country’s export share as a percentage of world total
wheat_exports["Share_2003"] = (wheat_exports["Export_2003"] / total_2003) * 100
wheat_exports["Share_2023"] = (wheat_exports["Export_2023"] / total_2023) * 100

# Compute change in share (percentage points)
wheat_exports["Change_pp"] = wheat_exports["Share_2023"] - wheat_exports["Share_2003"]

# Select top 15 exporters in 2023
top15 = wheat_exports.sort_values("Share_2023", ascending=False).head(15).reset_index(drop=True)

# Sort by change in share for diverging bar plot
top15_sorted = top15.sort_values("Change_pp", ascending=True).reset_index(drop=True)
colors = ["salmon" if val >= 0 else "skyblue" for val in top15_sorted["Change_pp"]]

# Create side-by-side plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9))

# Dumbbell Plot: Compare shares between 2003 and 2023
for i, row in top15.iterrows():
    ax1.plot([row["Share_2003"], row["Share_2023"]], [i, i], color="gray", lw=1)
    ax1.plot(row["Share_2003"], i, "o", color="skyblue", label="2003" if i == 0 else "")
    ax1.plot(row["Share_2023"], i, "o", color="salmon", label="2023" if i == 0 else "")
    ax1.text(max(row["Share_2003"], row["Share_2023"]) + 0.5, i, row["Country"], va="center", fontsize=9)

ax1.set_yticks(range(len(top15)))
ax1.set_yticklabels([])
ax1.set_xlabel("Export Share (%)")
ax1.set_title("Top 15 Wheat Exporters: 2003 vs 2023")
ax1.grid(True, axis="x")
ax1.legend(loc="lower right")

# Diverging Bar Plot: Change in Share
ax2.barh(top15_sorted["Country"], top15_sorted["Change_pp"], color=colors)
ax2.axvline(0, color="gray", lw=1)
ax2.set_xlabel("Change in Export Share (pp)")
ax2.set_title("Change in Global Export Share: 2003 to 2023")

plt.tight_layout()
plt.savefig("export_share_change_plot.png", dpi=300)