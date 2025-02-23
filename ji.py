import numpy as np
import matplotlib.pyplot as plt  # If you're visualizing the heatmaps

# Example: Stacking heatmaps for 7 days (replace with your actual data)
num_days = 7
heatmap_height = 7  # Number of days of the week (y-axis)
heatmap_width = 15  # Number of hours in a day (x-axis)

# Initialize an empty 3D array to hold the stacked heatmaps
stacked_heatmaps = np.zeros((num_days, heatmap_height, heatmap_width))

for day in range(num_days):
    # Load or create the heatmap for the current day (replace with your data loading)
    # Assume 'current_day_heatmap' is a 2D array (7x15)
    current_day_heatmap = np.random.rand(heatmap_height, heatmap_width) * 100  # Example random data

    # Store the heatmap in the correct "z-axis" slice of the 3D array
    stacked_heatmaps[day, :, :] = current_day_heatmap

    # (Optional) Visualize the individual heatmaps if needed
    plt.imshow(current_day_heatmap, cmap="viridis", origin="lower")
    plt.title(f"Day {day+1} Heatmap")
    plt.show()

# Now 'stacked_heatmaps' is your 3D array (z, y, x) representing the stacked heatmaps.
print(stacked_heatmaps.shape)  # Output: (7, 7, 15) in this example