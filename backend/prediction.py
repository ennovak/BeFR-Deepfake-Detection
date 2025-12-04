# prediction.py
import numpy as np
from backend.modelLoad import preprocess_image

# match to the model
LABELS = [0, 1]  # 0: Real, 1: AI-Generated

def run_prediction(model, image_path):
    """Run prediction using the model."""
    
    if model is None:
        raise ValueError("Model not loaded.")

    img = preprocess_image(image_path)
    preds = model.predict(img)[0]

    # If model outputs single sigmoid value (fake probability)
    if preds.shape == ():
        prob_fake = float(preds)
        prob_real = 1 - prob_fake
        label = 1 if prob_fake > 0.5 else 0

    # If model outputs 2-class softmax
    elif len(preds) == 2:
        prob_real = float(preds[0])
        prob_fake = float(preds[1])
        label = LABELS[np.argmax(preds)]

    else:
        return jsonify({"error": "Unsupported model output shape"}), 500
    
    return {
        "label": label,
        "prob_fake": prob_fake,
        "prob_real": prob_real,
        "model": "cnn"
    }
