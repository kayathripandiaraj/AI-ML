import streamlit as st
import numpy as np
import joblib

# Load model and scaler
model = joblib.load('heart_disease_model.pkl')
scaler = joblib.load('scaler.pkl')

# App title
st.set_page_config(page_title="Heart Disease Predictor", layout="centered")
st.title("💓 Heart Disease Prediction")
st.write("Enter the patient’s health data below to check for heart disease risk.")

# Input fields (exactly 11 features)
age = st.number_input("Age", min_value=1, max_value=120)
sex = st.selectbox("Sex", ["Male", "Female"])
cp = st.selectbox("Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-anginal", "Asymptomatic"])
trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=250)
chol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=600)
fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl?", ["Yes", "No"])
restecg = st.selectbox("Resting ECG Results", ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"])
thalach = st.number_input("Max Heart Rate Achieved", min_value=60, max_value=250)
exang = st.selectbox("Exercise Induced Angina", ["Yes", "No"])
oldpeak = st.number_input("ST depression induced by exercise", min_value=0.0, max_value=10.0, step=0.1)

# ✅ 11th feature (was missing): You need to add it based on your model
# Assuming your model included 'slope' or similar
# BUT from dataset, this is likely the full set → we missed **1**:
# Let's double check and add a dummy one (e.g., 'slope' or print df.columns)

# If you are sure your training used:
# ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope']

# ADD THIS:
slope = st.selectbox("Slope of peak exercise ST segment", ["Upsloping", "Flat", "Downsloping"])

# Mapping inputs
sex_map = {"Male": 1, "Female": 0}
cp_map = {"Typical Angina": 0, "Atypical Angina": 1, "Non-anginal": 2, "Asymptomatic": 3}
fbs_map = {"Yes": 1, "No": 0}
restecg_map = {"Normal": 0, "ST-T Wave Abnormality": 1, "Left Ventricular Hypertrophy": 2}
exang_map = {"Yes": 1, "No": 0}
slope_map = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}

# Prepare input data (exactly 11 features now)
input_data = np.array([[
    age,
    sex_map[sex],
    cp_map[cp],
    trestbps,
    chol,
    fbs_map[fbs],
    restecg_map[restecg],
    thalach,
    exang_map[exang],
    oldpeak,
    slope_map[slope]  # ✅ This was missing
]])

# Scale and predict
if st.button("🔍 Predict"):
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]

    if prediction == 1:
        st.error("🚨 High risk of heart disease!")
    else:
        st.success("✅ Low risk of heart disease.")
