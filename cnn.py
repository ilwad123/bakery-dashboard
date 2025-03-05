import torch
import torch.nn as nn
import cv2
import numpy as np
import torch.optim as optim

# Define the CNN Model 
class SimpleCNN(nn.Module):
    def __init__(self, num_channels=3):  
        super(SimpleCNN, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=num_channels, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)

        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2)

        self.global_pool = nn.AdaptiveAvgPool2d(1)  
        self.fc = nn.Linear(32, 7)  # Output: 7 sales predictions for 7 days

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.maxpool(x)

        x = self.relu(self.conv2(x))
        x = self.maxpool(x)

        x = self.global_pool(x).squeeze()
        x = self.fc(x)  
        x = torch.relu(x)  
        return x

# Function to Load Heatmaps as Separate Channels
def load_heatmap(paths):
    heatmaps = [cv2.imread(p, cv2.IMREAD_GRAYSCALE) for p in paths]  
    heatmaps = [cv2.resize(h, (32, 32)).astype(np.float32) for h in heatmaps]  

    # Normalize: mean = 0, std = 1
    heatmaps = [(h - np.mean(h)) / (np.std(h) + 1e-8) for h in heatmaps]  

    heatmaps = np.stack(heatmaps, axis=0)  
    return torch.tensor(heatmaps, dtype=torch.float32).unsqueeze(0)  # Shape: (1, 3, 32, 32)


# 3️⃣ Define Input Paths (3 heatmaps)
paths = ["sales_heatmap.png", "monthly_sales.png", "holiday_heatmap.png"]

# 4️⃣ Load Heatmap Data
X = load_heatmap(paths)  # Shape: (1, 3, 32, 32) -> (Batch, Channels, Height, Width)

# 5️⃣ Define Target Labels (e.g., Next Week Sales)
Y = torch.tensor([[250.4,246.6, 0, 118.1, 134.1, 215.7, 92.7]], dtype=torch.float32)  # Example sales for 7 days
# Normalize Y to a similar scale as input heatmaps (0 to 1)
Y_min, Y_max = Y.min(), Y.max()
Y = (Y - Y_min) / (Y_max - Y_min)

# 6️⃣ Initialize Model & Optimizer
model = SimpleCNN(num_channels=3)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

# 7️⃣ Training Loop (Without trainloader)
for epoch in range(200):  
    optimizer.zero_grad()  # Reset gradients

# Print predictions after training
    outputs = model(X)
    loss = criterion(outputs, Y)  # Compute loss
    loss.backward()  # Backpropagation
    optimizer.step()  # Update weights

    print(f'Epoch [{epoch+1}/10], Loss: {loss.item():.4f}')  # Print loss

print('Finished Training')

# 8️⃣ Save the trained model
torch.save(model.state_dict(), "sales_prediction_model.pth")
print("Predicted Sales for Next 7 Days:", outputs.detach().numpy())  # Convert tensor to NumPy
