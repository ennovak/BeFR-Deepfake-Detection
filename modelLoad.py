# modelLoad.py
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# path for the model
MODEL_PATH = "models/final_model.h5"

# image size the model expects
IMAGE_SIZE = (224, 224)

def load_cnn_model():
    """Load the trained model."""
    if not os.path.exists(MODEL_PATH):
        print("Model file not found yet.")
        return None

    model = tf.keras.models.load_model(MODEL_PATH)
    return model


def preprocess_image(image_path):
    """Prep image for prediction."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize(IMAGE_SIZE)

    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr
