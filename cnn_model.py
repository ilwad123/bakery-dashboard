#define cnn feature extraction cnn=>preprocess=>cnn_model=> train.py=>
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, LSTM, TimeDistributed, Input
import numpy as np

# CNN Feature Extractor
def create_cnn():
    input_layer = Input(shape=(128, 128, 1))  # Heatmap input size
    x = Conv2D(32, (3,3), activation='relu')(input_layer)
    x = MaxPooling2D((2,2))(x)
    x = Conv2D(64, (3,3), activation='relu')(x)
    x = MaxPooling2D((2,2))(x)
    x = Flatten()(x)
    x = Dense(64, activation='relu')(x)
    return Model(inputs=input_layer, outputs=x)

cnn_model = create_cnn()

