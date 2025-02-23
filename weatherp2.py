import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Generate Datetime values (same length as other lists)
datetime_values = pd.date_range(start='2024-04-24 00:00:00', periods=18, freq='H')

# Example Data
data = {
    'Datetime': datetime_values,
    'Neighborhood': ['Old Market'] * 6 + ['Clifton'] * 6 + ['Redland'] * 6,  # 18 values
    'Temperature': [12, 14, 13, 11, 10, 9, 15, 16, 14, 13, 12, 10, 8, 9, 10, 12, 13, 15],  # 18 values
    'Sales': [120, 130, 125, 110, 100, 95, 200, 210, 205, 190, 180, 170, 80, 90, 85, 95, 110, 100]  # 18 values
}

df = pd.DataFrame(data)  # ✅ No more length mismatch

# Get unique neighborhoods
neighborhoods = df["Neighborhood"].unique()

# Generate a heatmap for each neighborhood
for neighborhood in neighborhoods:
    df_neigh = df[df["Neighborhood"] == neighborhood].pivot(index="Datetime", columns="Temperature", values="Sales")

    # Fill missing values
    df_neigh = df_neigh.fillna(0)

    plt.figure(figsize=(10, 6))
    sns.heatmap(df_neigh, annot=True, cmap="coolwarm")

    plt.title(f"Sales Trend Over Time in {neighborhood}")
    plt.xticks(rotation=45, ha="right")

    # Save each heatmap as an image
    plt.savefig(f"sales_heatmap_{neighborhood.replace(' ', '_')}.png", dpi=300, bbox_inches="tight")

    plt.show()

