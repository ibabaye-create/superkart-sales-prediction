
# Import necessary libraries
import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app
superkart_api = Flask("SuperKart")

# Load the trained model (path resolved relative to this file, so it works from any working directory)
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "superkart_model.joblib")
model = joblib.load(MODEL_PATH)

# Features the model expects, in the order used during training
FEATURES = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years",
    "Product_Type_Category",
]


# Home page
@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart System"


# Predict sales for a single product
@superkart_api.post("/v1/predict")
def predict_sales():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    missing = [f for f in FEATURES if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    input_data = pd.DataFrame([{f: data[f] for f in FEATURES}])
    prediction = float(model.predict(input_data)[0])

    return jsonify({"Sales": round(prediction, 2)})


# Predict sales for a batch of products from an uploaded CSV file
@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded. Send a CSV file under the key 'file'"}), 400

    input_data = pd.read_csv(request.files["file"])

    missing = [f for f in FEATURES if f not in input_data.columns]
    if missing:
        return jsonify({"error": f"Missing columns: {missing}"}), 400

    predictions = model.predict(input_data[FEATURES])
    output_dict = {str(i): round(float(pred), 2) for i, pred in enumerate(predictions)}

    return jsonify(output_dict)


# Run the Flask app (0.0.0.0 makes it reachable from other Docker containers)
if __name__ == "__main__":
    superkart_api.run(host="0.0.0.0", port=7860, debug=False)
