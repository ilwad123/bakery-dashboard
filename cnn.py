# import torch
# import torch.nn as nn
# import cv2
# import numpy as np
# import torch.optim as optim

# #predict sales revenue 
# #predict most popular product list => then from there just group to most popular category 
# # do prediction for route optimisation 

# #check the website if you are on the right track 

# # on monday go through each step of the CNN model and understand it breathe in and out (research about it)
# #make multiple weather heatmaps for it 
# # neighbourhood one ask about it ??? so all i have to do is two more heatmaps
# # then implement it as you go along

# # Define the CNN Model 
# class SimpleCNN(nn.Module):
#     def __init__(self, num_channels=3):  # Now expects 3 heatmaps
#         super(SimpleCNN, self).__init__()

#         self.conv1 = nn.Conv2d(in_channels=num_channels, out_channels=16, kernel_size=3, stride=1, padding=1)
#         self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)

#         self.relu = nn.ReLU()
#         self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2)

#         self.global_pool = nn.AdaptiveAvgPool2d(1)  # Adaptive pooling to remove fixed size dependency
#         self.fc = nn.Linear(32, 7)  # Output 7 prediction sales for the coming 7 days 
#         # self.fc=nn.Linear(32,30/31 depending on the month ) #output prediction of sales for the coming month

#     def forward(self, x):
#         x = self.relu(self.conv1(x))
#         x = self.maxpool(x)

#         x = self.relu(self.conv2(x))
#         x = self.maxpool(x)

#         x = self.global_pool(x).squeeze()
#         x = self.fc(x)  
#         x = torch.relu(x) 
#         return x

# # Function to Load Heatmaps as Separate Channels
# def load_heatmap(paths):
#     heatmaps = [cv2.imread(p, cv2.IMREAD_GRAYSCALE) for p in paths]  
#     heatmaps = [cv2.resize(h, (32, 32)).astype(np.float32) for h in heatmaps]  
    
#     # Normalize: mean = 0, std = 1
#     heatmaps = [(h - np.mean(h)) / (np.std(h) + 1e-8) for h in heatmaps]  
    
#     heatmaps = np.stack(heatmaps, axis=0)  
#     return torch.tensor(heatmaps, dtype=torch.float32).unsqueeze(0)  


# # 3️⃣ Define Input Paths (Now using 3 heatmaps)
# paths = ["sales_heatmap.png", "monthly_sales.png", "holiday_heatmap.png"]  # Only 3 images

# # 4️⃣ Load Heatmap Data
# X = load_heatmap(paths)  # Shape: (1, 3, 32, 32) -> (Batch, Channels, Height, Width)

# # 5️⃣ Initialize Model AFTER Data is Loaded
# model = SimpleCNN(num_channels=3)  # Now expecting 3 channels

# # 6️⃣ Predict Sales
# output = model(X)

# print("Predicted Sales:", output)  # This prints the entire tensor of 7 values

# #Why Training Matters
# # Right now, your CNN has no idea what sales mean—it just processes numbers.
# #Training teaches it to find relationships between heatmaps and actual sales.
# #Once trained, your CNN will predict realistic sales values instead of random ones.

# model = SimpleCNN(num_channels=3)  # This is correct, you're initializing the model
# optimizer = torch.optim.Adam(model.parameters(), lr=0.001)  # Adam optimizer
# criterion = nn.CrossEntropyLoss()

# for epoch in range(2):  # loop over the dataset multiple times

#     running_loss = 0.0
#     for i, data in enumerate(trainloader, 0):
#         # get the inputs; data is a list of [inputs, labels]
#         inputs, labels = data

#         # zero the parameter gradients
#         optimizer.zero_grad()

#         # forward + backward + optimize
#         outputs = net(inputs)
#         loss = criterion(outputs, labels)
#         loss.backward()
#         optimizer.step()

#         # print statistics
#         running_loss += loss.item()
#         if i % 2000 == 1999:    # print every 2000 mini-batches
#             print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
#             running_loss = 0.0

# print('Finished Training')

import torch
import torch.nn as nn
import cv2
import numpy as np
import torch.optim as optim
import matplotlib.pyplot as plt

class SimpleCNN(nn.Module):
    def __init__(self, num_channels=3):  
        super(SimpleCNN, self).__init__()

        self.conv1 = nn.Conv2d(num_channels, 16, kernel_size=3, stride=1, padding=1)  
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)  
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)  

        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.dropout = nn.Dropout(p=0.5)

        self.global_pool = nn.AdaptiveAvgPool2d(1)  
        self.fc = nn.Linear(64, 7)  

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.maxpool(x)
        x = self.dropout(x)

        x = self.relu(self.conv2(x))
        x = self.maxpool(x)
        x = self.dropout(x)

        x = self.relu(self.conv3(x))
        x = self.maxpool(x)
        x = self.dropout(x)

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


paths = ["sales_heatmap.png", "monthly_sales.png", "holiday_heatmap.png"]

X = load_heatmap(paths)  
#past 7 day sales 
Y = torch.tensor([[250.4,246.6, 0, 118.1, 134.1, 215.7, 92.7]], dtype=torch.float32)  

# Normalise Y to a similar scale as input heatmaps (0 to 1)
Y_min, Y_max = Y.min(), Y.max()
Y = (Y - Y_min) / (Y_max - Y_min)

model = SimpleCNN(num_channels=3)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.5)

#training loop
for epoch in range(250):  
    optimizer.zero_grad()  # Reset gradients

    outputs = model(X)  # Forward pass
    loss = criterion(outputs, Y)  # Compute loss
    loss.backward()  # Backpropagation
    optimizer.step()  # Update weights
    
    # Step the learning rate scheduler
    scheduler.step()

    if epoch % 10 == 0:  # Print loss every 10 epochs
        print(f'Epoch [{epoch+1}/250], Loss: {loss.item():.4f}')

print('Finished Training')
print("Labels (True Sales):", Y)


# prints the predicted model
predictions = outputs.detach().numpy()
predictions_rescaled = predictions * (Y_max.item() - Y_min.item()) + Y_min.item()
print("Predicted Sales for Next 7 Days:", predictions_rescaled)

predictions_tensor = torch.tensor(predictions, dtype=torch.float32)

mae = torch.mean(torch.abs(predictions_tensor - Y))  # Mean Absolute Error
print(f'MAE: {mae.item()}')
mse = torch.mean((predictions_tensor - Y) ** 2)
print(f'MSE: {mse.item()}')


#graph of predicted sales vs true sales 

plt.plot(predictions.flatten(), label='Predicted Sales')
plt.plot(Y.flatten(), label='True Sales', linestyle='dashed')
plt.legend()
plt.title('Predicted vs True Sales')
plt.xlabel('Day')
plt.ylabel('Sales')
plt.show()