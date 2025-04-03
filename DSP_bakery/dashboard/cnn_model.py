import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import cv2
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_absolute_percentage_error

# CNN-LSTM Model
class CNN_LSTM(nn.Module):
    def __init__(self, num_channels=3, lstm_hidden_size=120):
        super(CNN_LSTM, self).__init__()
        self.conv1 = nn.Conv2d(num_channels, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.maxpool = nn.MaxPool2d(2)
        self.dropout = nn.Dropout(0.5)
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        self.lstm = nn.LSTM(1, lstm_hidden_size, num_layers=2, batch_first=True)
        self.fc = nn.Linear(lstm_hidden_size + 64, 7)

    def forward(self, heatmap, sales_seq):
        x = self.relu(self.conv1(heatmap))
        x = self.maxpool(x)
        x = self.dropout(x)
        x = self.relu(self.conv2(x))
        x = self.maxpool(x)
        x = self.dropout(x)
        x = self.relu(self.conv3(x))
        x = self.maxpool(x)
        x = self.dropout(x)
        x = self.global_pool(x).view(x.size(0), -1)

        lstm_out, _ = self.lstm(sales_seq.unsqueeze(-1))
        lstm_out = lstm_out[:, -1, :]
        combined = torch.cat((x, lstm_out), dim=1)
        return torch.relu(self.fc(combined))

# Heatmap loader
import os

def load_heatmap(paths):
    heatmaps = []
    base_dir = os.path.dirname(__file__)  # directory of the current file

    for filename in paths:
        full_path = os.path.join(base_dir, filename)
        
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Image not found: {full_path}")

        img = cv2.imread(full_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Image could not be loaded: {full_path}")

        img = cv2.resize(img, (32, 32)).astype(np.float32)
        img = (img - np.mean(img)) / (np.std(img) + 1e-8)
        heatmaps.append(img)

    heatmaps = np.stack(heatmaps, axis=0)
    return torch.tensor(heatmaps, dtype=torch.float32).unsqueeze(0)


# WMAPE function
def wmape(actual, predicted):
    return 100 * np.sum(np.abs(actual - predicted)) / np.sum(actual)

# Predict function
def predict_from_graph_data(df):
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date
    daily_sales = df.groupby('date')['total'].sum().reset_index()
    daily_sales.columns = ['Date', 'Total']

    scaler = MinMaxScaler()
    daily_sales['Total'] = scaler.fit_transform(daily_sales[['Total']])

    
    train_size = int(len(daily_sales) * 0.7)
    val_size = int(len(daily_sales) * 0.15)
    test_size = len(daily_sales) - train_size - val_size

    train_sales = torch.tensor(daily_sales['Total'].values[:train_size], dtype=torch.float32).unsqueeze(0)
    val_sales = torch.tensor(daily_sales['Total'].values[train_size:train_size + val_size], dtype=torch.float32).unsqueeze(0)
    test_sales = torch.tensor(daily_sales['Total'].values[train_size + val_size:], dtype=torch.float32).unsqueeze(0)
    
    X_heatmap = load_heatmap(["sales_heatmap.png", "monthly_sales.png", "holiday_heatmap.png"])

    model = CNN_LSTM(num_channels=3, lstm_hidden_size=120)  # Increase LSTM size (show the difference in the graphs)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)  # Reduce learning rate 
    criterion = nn.MSELoss()
    
    for epoch in range(1000):  
    # Training step
        model.train()
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(X_heatmap, train_sales)  
        print("Output shape:", outputs.shape)
        loss = criterion(outputs, train_sales[:, -7:])  
        loss.backward()
        optimizer.step()
        print(f"Epoch [{epoch+1}/250] completed.,Loss: {loss.item():.4f}")

        # Evaluation (after training step)
        model.eval()
        with torch.no_grad():
            
            y_pred_train = model(X_heatmap, train_sales).detach().numpy()
            y_pred_test = model(X_heatmap, val_sales).detach().numpy()

            train_actual = train_sales[:, -7:].numpy().flatten()
            val_actual = val_sales[:, -7:].numpy().flatten()

            train_pred_tensor = torch.tensor(y_pred_train, dtype=torch.float32)
            val_pred_tensor = torch.tensor(y_pred_test, dtype=torch.float32)

            train_actual_tensor = torch.tensor(train_actual, dtype=torch.float32).view(1, -1)
            val_actual_tensor = torch.tensor(val_actual, dtype=torch.float32).view(1, -1)

            train_rmse = np.sqrt(criterion(train_pred_tensor, train_actual_tensor)).item()
            val_rmse = np.sqrt(criterion(val_pred_tensor, val_actual_tensor)).item()

            train_mape = mean_absolute_percentage_error(train_actual, y_pred_train.flatten()) * 100
            val_mape = mean_absolute_percentage_error(val_actual, y_pred_test.flatten()) * 100

            train_wmape = wmape(train_actual, y_pred_train.flatten())
            val_wmape = wmape(val_actual, y_pred_test.flatten())

            print(f"Epoch {epoch+1}: Train RMSE {train_rmse:.4f}, Validation RMSE {val_rmse:.4f}")
            print(f"Train MAPE: {train_mape:.2f}%, Validation MAPE: {val_mape:.2f}%")
            print(f"Train WMAPE: {train_wmape:.2f}%, Validation WMAPE: {val_wmape:.2f}%")
            


    print("Training Completed")  


    # Test Set Evaluation
    with torch.no_grad():
        y_pred_test = model(X_heatmap, test_sales).detach().numpy()
        test_actual = test_sales[:, -7:].numpy().flatten()

        test_rmse = np.sqrt(criterion(torch.tensor(y_pred_test), torch.tensor(test_actual).view(1, -1))).item()
        test_mape = mean_absolute_percentage_error(test_actual, y_pred_test.flatten()) * 100
        test_wmape = wmape(test_actual, y_pred_test.flatten())

        print(f"Test RMSE: {test_rmse:.4f}")
        print(f"Test MAPE: {test_mape:.2f}%")
        print(f"Test WMAPE: {test_wmape:.2f}%")


    # Predict function for future sales
    future_sales_input = test_sales[:, -7:].clone()
    predicted_future_sales = model(X_heatmap, future_sales_input).detach().numpy()
    predicted_future_sales_rescaled = scaler.inverse_transform(predicted_future_sales)


    return predicted_future_sales_rescaled.flatten()

#compare to old code and add parameters and what not - Monday 