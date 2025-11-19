# modelLoad.py
import numpy as np
from PIL import Image
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input as eff_preprocess

# path for the model
MODEL_PATH = "CNN_model.keras"

# image size the model expects
IMAGE_SIZE = (128, 128)

def load_cnn_model():
    """Load the trained model."""
    if not os.path.exists(MODEL_PATH):
        print("Model file not found yet.")
        return None

    model = tf.keras.models.load_model(MODEL_PATH, custom_objects={"preprocess_input": eff_preprocess})
    return model


def preprocess_image(image_path):
    """Prep image for prediction."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize(IMAGE_SIZE)

    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr