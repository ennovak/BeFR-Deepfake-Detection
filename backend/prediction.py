# prediction.py
import numpy as np
from modelLoad import preprocess_image

# match to the model
LABELS = [0, 1]  # 0: Real, 1: AI-Generated

def run_prediction(model, image_path):
    """Run prediction using the model."""
    
    if model is None:
        raise ValueError("Model not loaded.")

    img = preprocess_image(image_path)
    preds = model.predict(img)[0]

    idx = int(np.argmax(preds))
    label = LABELS[idx]
    confidence = float(preds[idx])

    is_ai = (label == 1)

    return {
        "is_ai": is_ai,
        "confidence": confidence,
        "model": "cnn"
    }
