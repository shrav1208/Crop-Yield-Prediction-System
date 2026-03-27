from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import torch
from torchvision import transforms
from PIL import Image
import io
import base64
from transformers import ViTForImageClassification

app = Flask(__name__)
CORS(app)

# ─── Crop Recommendation ───────────────────────────────────────────────────────
with open("crop_recommendation_modelrf.pkl", "rb") as f:
    crop_model = pickle.load(f)

# ─── Fertilizer ────────────────────────────────────────────────────────────────
with open("fertilizer_recommendation.pkl", "rb") as f:
    fertilizer_model = pickle.load(f)
with open("fertilizer_le.pkl", "rb") as f:
    fertilizer_le = pickle.load(f)
with open("fertilizer_columns.pkl", "rb") as f:
    fertilizer_columns = pickle.load(f)

# ─── Disease (ViT) ─────────────────────────────────────────────────────────────
# DISEASE_CLASSES = ["healthy", "leaf_curl", "leaf_spot", "whitefly", "yellowish"]

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# disease_model = ViTForImageClassification.from_pretrained(
#     'google/vit-base-patch16-224-in21k',
#     num_labels=len(DISEASE_CLASSES),
#     ignore_mismatched_sizes=True
# )
# disease_model.load_state_dict(
#     torch.load("disease_prediction_model_torch.pth", map_location=device)
# )
# disease_model.to(device)
# disease_model.eval()

# disease_transforms = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
# ])

# ─── Yield ─────────────────────────────────────────────────────────────────────
with open("yield_regressor.pkl",  "rb") as f:
    yield_model = pickle.load(f)
with open("yield_crop_le.pkl",    "rb") as f:
    yield_crop_le = pickle.load(f)
with open("yield_thresholds.pkl", "rb") as f:
    yield_thresholds = pickle.load(f)


# ══════════════════════════════════════════════════════════════════════════════
# Routes
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/predict", methods=["POST"])
def predict_crop():
    data = request.get_json()
    inp = np.array([[
        float(data["nitrogen"]),
        float(data["phosphorus"]),
        float(data["potassium"]),
        float(data["temperature"]),
        float(data["humidity"]),
    ]])
    prediction = crop_model.predict(inp)[0]
    return jsonify({"recommended_crop": prediction})


@app.route("/fertilizer", methods=["POST"])
def predict_fertilizer():
    data = request.get_json()
    sample = pd.DataFrame([{
        "Soil_color":  data["soil_color"],
        "Nitrogen":    float(data["nitrogen"]),
        "Phosphorus":  float(data["phosphorus"]),
        "Potassium":   float(data["potassium"]),
        "pH":          float(data["ph"]),
        "Rainfall":    float(data["rainfall"]),
        "Temperature": float(data["temperature"]),
    }])
    sample = pd.get_dummies(sample)
    sample = sample.reindex(columns=fertilizer_columns, fill_value=0)
    prediction = fertilizer_model.predict(sample)
    return jsonify({"recommended_fertilizer": fertilizer_le.inverse_transform(prediction)[0]})


# @app.route("/disease", methods=["POST"])
# def predict_disease():
#     data = request.get_json()
#     image_data = data["image"]
#     if "," in image_data:
#         image_data = image_data.split(",")[1]
#     image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert("RGB")
#     inp = disease_transforms(image).unsqueeze(0).to(device)
#     with torch.no_grad():
#         logits = disease_model(inp).logits
#         probs  = torch.nn.functional.softmax(logits, dim=1)
#         conf, idx = torch.max(probs, 1)
#     return jsonify({
#         "disease":    DISEASE_CLASSES[idx.item()],
#         "confidence": round(conf.item() * 100, 2)
#     })


@app.route("/yield", methods=["POST"])
def predict_yield():
    data = request.get_json()
    crop = data["crop"].strip().lower()

    if crop not in yield_crop_le.classes_:
        return jsonify({
            "error": f"Unknown crop '{crop}'. Supported: {list(yield_crop_le.classes_)}"
        }), 400

    crop_enc = yield_crop_le.transform([crop])[0]

    inp = np.array([[
        crop_enc,
        float(data["soil_temp"]),
        float(data["nitrogen"]),
        float(data["phosphorus"]),
        float(data["potassium"]),
        float(data["moisture"]),
        float(data["humidity"]),
        float(data["air_temp"]),
    ]])

    yield_val = round(float(max(0, yield_model.predict(inp)[0])), 1)

    thresh = yield_thresholds.get(crop, {})
    if yield_val >= thresh.get("high_min", float("inf")):
        category = "High"
    elif yield_val <= thresh.get("low_max", 0):
        category = "Low"
    else:
        category = "Medium"

    return jsonify({
        "yield_kg_ha":    yield_val,
        "yield_category": category
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)