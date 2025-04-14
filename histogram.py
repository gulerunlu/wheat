# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 08:22:17 2025

@author: Gandalf The Grey
"""

import pandas as pd
import matplotlib.pyplot as plt

# Read the cleaned wheat price dataset
wheat_prices = pd.read_csv("prices.csv")

# Convert the date column to datetime format
wheat_prices["Date"] = pd.to_datetime(wheat_prices["Date"])
print("Missing date values:", wheat_prices["Date"].isna().sum())

# Select Russian price data and clean it
russia_prices = wheat_prices[["Date", "Russia"]].copy()
russia_prices = russia_prices[russia_prices["Russia"].notna()]
russia_prices = russia_prices[russia_prices["Russia"] > 0]
russia_prices = russia_prices.sort_values("Date")

# Separate prices into Pre-War and Post-War groups
invasion_date = pd.Timestamp("2022-02-24")
pre_war_prices = russia_prices[russia_prices["Date"] < invasion_date]["Russia"]
post_war_prices = russia_prices[russia_prices["Date"] >= invasion_date]["Russia"]

# Create histogram plot
plt.figure(figsize=(12, 7))
bins = 20

# Plot pre-war histogram
if len(pre_war_prices) > 0:
    plt.hist(
        pre_war_prices,
        bins=bins,
        color="skyblue",
        alpha=0.6,
        edgecolor="black",
        weights=[1/len(pre_war_prices)] * len(pre_war_prices),
        label="Pre-War"
    )
    plt.axvline(
        pre_war_prices.median(),
        color="blue",
        linestyle="--",
        linewidth=2,
        label=f"Median (Pre-War): ${pre_war_prices.median():.1f}"
    )

# Plot post-war histogram
if len(post_war_prices) > 0:
    plt.hist(
        post_war_prices,
        bins=bins,
        color="orange",
        alpha=0.7,
        edgecolor="black",
        weights=[1/len(post_war_prices)] * len(post_war_prices),
        label="Post-War"
    )
    plt.axvline(
        post_war_prices.median(),
        color="darkorange",
        linestyle="--",
        linewidth=3,
        label=f"Median (Post-War): ${post_war_prices.median():.1f}"
    )

# Final formatting
plt.title("Russian Wheat Export Prices: Pre-War vs. Post-War Histogram")
plt.xlabel("Price (USD/ton)")
plt.ylabel("Percentage of Observations")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# Save the plot
plt.savefig("histogram.png", dpi=300)

