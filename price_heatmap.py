# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 13:24:40 2025

@author: Gandalf The Grey
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the wheat export price data
wheat_prices = pd.read_csv("prices.csv")

# Drop any unnecessary unnamed columns (e.g., index remnants)
columns_to_drop = [col for col in wheat_prices.columns if col.startswith("Unnamed")]
wheat_prices = wheat_prices.drop(columns=columns_to_drop)

# Convert the 'Date' column to datetime format
wheat_prices["Date"] = pd.to_datetime(wheat_prices["Date"])
print("Missing date values:", wheat_prices["Date"].isna().sum())

# Drop rows where date conversion failed
wheat_prices = wheat_prices[wheat_prices["Date"].notna()]

# Create a new column showing the quarter (e.g., 2023Q1)
wheat_prices["Quarter"] = wheat_prices["Date"].dt.to_period("Q")

# Calculate average price per country for each quarter
quarterly_means = wheat_prices.groupby("Quarter").mean(numeric_only=True).round(1)

# Convert index from period format to string (e.g., "2023Q1")
quarterly_means.index = quarterly_means.index.astype(str)

# Set up the heatmap plot
plt.figure(figsize=(14, 6))
sns.heatmap(
    quarterly_means.T,
    cmap="YlGnBu",
    annot=False,
    linewidths=0.4,
    cbar_kws={'label': 'USD/ton'}
)

# Configure plot labels and title
plt.title("Quarterly Average Wheat Export Prices by Country", fontsize=13)
plt.xlabel("Quarter")
plt.ylabel("Country")
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot
plt.savefig("prices_heatmap.png", dpi=300)



