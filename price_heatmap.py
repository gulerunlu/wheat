# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 13:24:40 2025

@author: Gandalf The Grey
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the prices dataset
df = pd.read_csv("prices.csv")

# Convert the date column to datetime
df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y", errors="coerce")
df = df.dropna(subset=["Date"])

# Remove any unnamed columns
df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

# Assign each date to a quarter (e.g., 2023Q1, 2023Q2)
df["Quarter"] = df["Date"].dt.to_period("Q")

# Group by quarter and calculate mean prices per country
df_quarterly = df.groupby("Quarter").mean(numeric_only=True).round(1)

# Clean up the index for display (e.g., convert Period to string)
df_quarterly.index = df_quarterly.index.astype(str)

# Create the heatmap
plt.figure(figsize=(14, 6))
sns.heatmap(
    df_quarterly.T,
    cmap="YlGnBu",
    annot=False,
    linewidths=0.4,
    cbar_kws={'label': 'USD/ton'}
)

# Chart formatting
plt.title("Quarterly Average Wheat Export Prices by Country", fontsize=13)
plt.xlabel("Quarter")
plt.ylabel("Country")
plt.xticks(rotation=45)
plt.tight_layout()


# Save output
plt.savefig("prices_heatmap.png", dpi=300)

