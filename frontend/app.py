import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend (container name "backend" on the shared Docker network)
BACKEND_URL = "http://backend:7860"

# Page title
st.title("SuperKart Sales Forecasting")
st.write("Enter the product and store details below to predict the total sales.")

# Input fields for product and store data
st.subheader("Single Prediction")

Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1.0, value=0.027, format="%.3f")
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=117.08)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
Product_Id_char = st.selectbox("Product ID Prefix (FD = Food, DR = Drinks, NC = Non-Consumable)", ["FD", "DR", "NC"])
Store_Age_Years = st.number_input("Store Age (Years, reference year 2025)", min_value=0, value=16, step=1)
Product_Type_Category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

# Create JSON payload
product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": int(Store_Age_Years),
    "Product_Type_Category": Product_Type_Category,
}

if st.button("Predict", type="primary"):
    try:
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=product_data, timeout=30)
        if response.status_code == 200:
            predicted_sales = response.json()["Sales"]
            st.success(f"Predicted Product Store Sales Total: {predicted_sales:,.2f}")
        else:
            st.error(f"Prediction failed (status {response.status_code}): {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Unable to connect to the prediction API at {BACKEND_URL}. Details: {e}")

# Batch Prediction
st.subheader("Batch Prediction")
st.caption("The CSV file must contain the same 10 feature columns used in the single prediction form.")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    if st.button("Predict for Batch", type="primary"):
        try:
            response = requests.post(
                f"{BACKEND_URL}/v1/predictbatch",
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")},
                timeout=120,
            )
            if response.status_code == 200:
                results = response.json()   # format returned by the backend: {"0": value, "1": value, ...}

                # Show each input row next to its predicted sales
                input_df = pd.read_csv(uploaded_file)
                input_df["Predicted_Sales"] = [results[str(i)] for i in range(len(input_df))]

                st.success(f"Predictions completed successfully for {len(input_df)} products.")
                st.dataframe(input_df)

                st.download_button(
                    "Download predictions as CSV",
                    data=input_df.to_csv(index=False).encode("utf-8"),
                    file_name="superkart_predictions.csv",
                    mime="text/csv",
                )
            else:
                st.error(f"Batch prediction failed (status {response.status_code}): {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Unable to connect to the prediction API at {BACKEND_URL}. Details: {e}")
