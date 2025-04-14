# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 21:38:14 2025

@author: Gandalf The Grey
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean the dataset
df = pd.read_csv("prices.csv")

# Drop columns with names like "Unnamed"
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Parse date column (e.g., "1-Mar-25")
df["ParsedDate"] = pd.to_datetime(df["Date"], format="%d-%b-%y", errors="coerce")
df = df.dropna(subset=["ParsedDate"])

# Melt into long format: one row per (date, country)
df_long = df.melt(
    id_vars=["ParsedDate", "Date"],
    var_name="Country",
    value_name="Price"
)

# Drop rows with missing or zero price
df_long = df_long.dropna(subset=["Price"])
df_long = df_long[df_long["Price"] > 0]

# Define major global events
balloon_events = {
    "2007-10-01": "Global Food Crisis\n+ High Oil Prices",
    "2010-08-05": "Russia Export Ban",
    "2011-03-01": "Arab Spring",
    "2012-07-01": "US Drought",
    "2022-02-24": "Ukraine Invasion"
}

# Plot
plt.figure(figsize=(14, 8))
sns.lineplot(
    data=df_long,
    x="ParsedDate",
    y="Price",
    hue="Country",
    palette=sns.color_palette("husl", n_colors=df_long["Country"].nunique()),
    linewidth=2,
    marker="o"
)

plt.title("Monthly Wheat Export Prices by Country (2000–2025)", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Export Price (USD/ton)")
plt.xticks(rotation=45, ha="right")
plt.grid(True, linestyle="--", alpha=0.5)

# Add balloon-style annotations for key events
for date_str, label in balloon_events.items():
    date = pd.to_datetime(date_str)
    y_val = df_long[df_long["ParsedDate"] == date]["Price"].max()
    y_val = y_val if pd.notnull(y_val) else 500  # default if price not found

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
