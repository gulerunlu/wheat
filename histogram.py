# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 08:22:17 2025

@author: Gandalf The Grey
"""

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("prices.csv")

# Convert the date column with format like '1-Mar-25'
df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y", errors="coerce")
df = df.dropna(subset=["Date"])

# Select only Russia data
df_russia = df[["Date", "Russia"]].copy()
df_russia = df_russia.dropna()
df_russia = df_russia[df_russia["Russia"] > 0]
df_russia = df_russia.sort_values("Date")

# Split into pre-war and post-war data
war_start = pd.to_datetime("2022-02-24")
pre_war = df_russia[df_russia["Date"] < war_start]["Russia"]
post_war = df_russia[df_russia["Date"] >= war_start]["Russia"]

# Create histogram
plt.figure(figsize=(12, 7))
bins = 20

if len(pre_war) > 0:
    plt.hist(pre_war, bins=bins, color="skyblue", alpha=0.6, edgecolor="black",
             label="Pre-War", weights=[1/len(pre_war)]*len(pre_war))
    plt.axvline(pre_war.median(), color="blue", linestyle="--", linewidth=2,
                label=f"Median (Pre-War): ${pre_war.median():.1f}")

if len(post_war) > 0:
    plt.hist(post_war, bins=bins, color="orange", alpha=0.7, edgecolor="black",
             label="Post-War", weights=[1/len(post_war)]*len(post_war))
    plt.axvline(post_war.median(), color="darkorange", linestyle="--", linewidth=3,
                label=f"Median (Post-War): ${post_war.median():.1f}")

# Final formatting
plt.title("Russian Wheat Export Prices: Pre-War vs. Post-War (Histogram with Medians)")
plt.xlabel("Price (USD/ton)")
plt.ylabel("Percentage of Observations")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

# Save the figure
plt.savefig("histogram.png", dpi=300)
