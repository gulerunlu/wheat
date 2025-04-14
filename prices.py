# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 21:22:44 2025

@author: Gandalf The Grey
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the cleaned CSV file
wheat_prices_wide = pd.read_csv("prices.csv")

# Convert the 'Date' column to datetime format
wheat_prices_wide["Date"] = pd.to_datetime(wheat_prices_wide["Date"])
print("Missing dates:", wheat_prices_wide["Date"].isna().sum())

# Reshape the data from wide to long format
wheat_prices_long = wheat_prices_wide.melt(
    id_vars="Date",
    var_name="Country",
    value_name="Price"
)

# Ensure the 'Price' column is numeric (all should already be clean)
wheat_prices_long["Price"] = pd.to_numeric(wheat_prices_long["Price"])

# Remove rows with missing or zero prices
wheat_prices_long = wheat_prices_long[wheat_prices_long["Price"].notna()]
wheat_prices_long = wheat_prices_long[wheat_prices_long["Price"] > 0]

# Add a new column that marks each date as 'Pre-War' or 'Post-War'
invasion_date = pd.Timestamp("2022-02-24")
wheat_prices_long["Period"] = wheat_prices_long["Date"].apply(
    lambda date: "Pre-War" if date < invasion_date else "Post-War"
)

# Create a balanced comparison window: last 3 years before and after the invasion
pre_war_trimmed = wheat_prices_long[
    (wheat_prices_long["Period"] == "Pre-War") &
    (wheat_prices_long["Date"] >= "2019-03-01")
]
post_war_data = wheat_prices_long[wheat_prices_long["Period"] == "Post-War"]
balanced_prices = pd.concat([pre_war_trimmed, post_war_data])

# Calculate the median price for each country and period
median_prices = balanced_prices.groupby(["Country", "Period"])["Price"].median().reset_index()

# Prepare the boxplot
plt.figure(figsize=(14, 6))
sns.set(style="whitegrid")
ax = sns.boxplot(
    data=balanced_prices,
    x="Country",
    y="Price",
    hue="Period",
    palette="Set2"
)

plt.title("Wheat Prices by Country: Pre-War vs. Post-War (Balanced 3-Year Sample)")
plt.xticks(rotation=45)

# Annotate median values above the boxes
x_positions = {country: i for i, country in enumerate(balanced_prices["Country"].unique())}

for _, row in median_prices.iterrows():
    x_shift = -0.2 if row["Period"] == "Pre-War" else 0.2
    x = x_positions[row["Country"]] + x_shift
    y = row["Price"]
    label = f"{y:.1f}"
    plt.text(x, y + 1, label, ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig("wheat_prices_pre_post_war.png", dpi=300)