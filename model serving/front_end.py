import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.title("Insurance Premium Predictor")
st.markdown("Fill in your details")

# Inputs
age = st.number_input("Age", min_value=1, max_value=120, value=25)
weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0)
height = st.number_input("Height (meters)", min_value=0.5, max_value=2.5, value=1.75)

income_lpa = st.number_input("Income (LPA)", min_value=0, value=5)

smoker = st.selectbox("Smoker", [True, False])

city = st.selectbox(
    "City",
    [
        "Hyderabad", "Delhi", "Chandigarh", "Pune", "Kolkata", "Bangalore",
        "Jaipur", "Chennai", "Indore", "Mumbai", "Kota",
        "Lucknow", "Gaya", "Jalandhar", "Mysore",
        "Other"
    ]
)

occupation = st.selectbox(
    "Occupation",
    [
        "retired",
        "freelancer",
        "student",
        "government_job",
        "business_owner",
        "unemployed",
        "private_job"
    ]
)

# Predict button
if st.button("Predict Premium"):

    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            result = response.json()

            if "error" in result:
                st.error(result["error"])
            else:
                st.success("Prediction Successful 🎉")
                st.write("Predicted Category:", result["predicted_category"])

        else:
            st.error(f"Server Error: {response.text}")

    except Exception as e:
        st.error(f"Request failed: {e}")