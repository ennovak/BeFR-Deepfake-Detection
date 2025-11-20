# prediction.py
import numpy as np
from modelLoad import preprocess_image

# match to the model
LABELS = ["Real", "AI-Generated"]

def run_prediction(model, image_path):
    """Run prediction using the model."""
    
    if model is None:
        raise ValueError("Model not loaded.")

    img = preprocess_image(image_path)
    preds = model.predict(img)[0]

    idx = int(np.argmax(preds))
    label = LABELS[idx]
    confidence = float(preds[idx])

    is_ai = (label == "AI-Generated")

    return {
        "is_ai": is_ai,
        "confidence": confidence,
        "model": "cnn"
    }
