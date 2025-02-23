import cv2
import numpy as np

def load_heatmap(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (128, 128))
    img = img / 255.0  # Normalize pixels
    img = np.expand_dims(img, axis=-1)  # Add channel dimension
    return img

def get_heatmap_data():
    paths = [
        "sales_heatmap.png",
        "monthly_sales.png",
        "holiday_heatmap.png",
    ]
    return np.array([load_heatmap(p) for p in paths])

# Example: Load heatmaps
X = get_heatmap_data()
print("Loaded heatmaps shape:", X.shape)  # Should be (3 (the amount of heatmaps i have), 128, 128, 1)
