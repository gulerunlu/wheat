# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 21:38:14 2025

@author: Gandalf The Grey
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
wheat_prices = pd.read_csv("prices.csv")

# Drop columns like "Unnamed"
drop_cols = [col for col in wheat_prices.columns if col.startswith("Unnamed")]
wheat_prices = wheat_prices.drop(columns=drop_cols)

# Convert the date column to datetime format
wheat_prices["ParsedDate"] = pd.to_datetime(wheat_prices["Date"])
print("Number of missing dates:", wheat_prices["ParsedDate"].isna().sum())

# Remove rows with missing dates
wheat_prices = wheat_prices[wheat_prices["ParsedDate"].notna()]

# Melt into long format: one row per (date, country)
wheat_long = wheat_prices.melt(
    id_vars=["ParsedDate", "Date"],
    var_name="Country",
    value_name="Price"
)

# Drop rows with missing or zero price
print("Missing prices:", wheat_long["Price"].isna().sum())
print("Zero prices:", (wheat_long["Price"] == 0).sum())
wheat_long = wheat_long[wheat_long["Price"].notna()]
wheat_long = wheat_long[wheat_long["Price"] > 0]

# Define major global events
balloon_events = {
    "2007-10-01": "Global Food Crisis\n+ High Oil Prices",
    "2010-08-05": "Russia Export Ban",
    "2011-03-01": "Arab Spring",
    "2012-07-01": "US Drought",
    "2022-02-24": "Russian invasion of Ukraine"
}

# Plot the data
plt.figure(figsize=(14, 8))
sns.lineplot(
    data=wheat_long,
    x="ParsedDate",
    y="Price",
    hue="Country",
    palette=sns.color_palette("husl", n_colors=wheat_long["Country"].nunique()),
    linewidth=2,
    marker="o"
)

plt.title("Monthly Wheat Export Prices by Country (2000–2025)", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Export Price (USD/ton)")
plt.xticks(rotation=45, ha="right")
plt.grid(True, linestyle="--", alpha=0.5)

# Annotate key global events
for date_str, label in balloon_events.items():
    date = pd.to_datetime(date_str)
    y_val = wheat_long[wheat_long["ParsedDate"] == date]["Price"].max()
    y_val = y_val if pd.notnull(y_val) else 500  # fallback if value not found

    plt.axvline(date, color='red', linestyle='--', lw=1)
    plt.annotate(
        label,
        xy=(date, y_val),
        xytext=(date, y_val + 130),
        bbox=dict(boxstyle="round,pad=0.5", fc="lightyellow", ec="black", lw=1),
        arrowprops=dict(arrowstyle="->", color="black"),
        fontsize=9,
        ha='center'
    )

plt.tight_layout()
plt.savefig("wheat_prices_annotated.png", dpi=300)