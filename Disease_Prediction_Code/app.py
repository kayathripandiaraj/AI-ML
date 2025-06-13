import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Page configuration
st.set_page_config(page_title="Disease Recognition System", layout="centered")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("Training.csv")

# Load dataset
df = load_data()

# Detect correct label column
label_column = 'prognosis' if 'prognosis' in df.columns else 'Disease'
X = df.drop(columns=[label_column])
y = df[label_column]

# Encode target labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train Random Forest model
model = RandomForestClassifier()
model.fit(X, y_encoded)

# Save model and encoder (optional)
joblib.dump(model, "model.pkl")
joblib.dump(le, "label_encoder.pkl")

# List of symptoms
symptoms = X.columns.tolist()

# -------------------- Streamlit UI --------------------

st.markdown("<h1 style='text-align: center;'>🩺 Disease Recognition System</h1>", unsafe_allow_html=True)

# User Info Inputs
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("👤 Name (optional)")
with col2:
    age = st.number_input("🎂 Age", min_value=0, max_value=120, step=1)

gender = st.radio("⚧️ Gender", ["Male", "Female", "Other"], horizontal=True)

# Symptom Input
st.markdown("---")
st.subheader("📌 Select Symptoms")

selected_symptoms = st.multiselect(
    "Choose from the list", 
    options=symptoms, 
    help="Start typing to search or scroll to select multiple symptoms"
)

custom_symptom = st.text_input("📝 Add any additional symptom (optional)")

# Predict Button
if st.button("🔍 Predict Disease"):
    if not selected_symptoms:
        st.warning("⚠️ Please select at least one symptom to predict.")
    else:
        # Prepare input for model
        symptom_input = [1 if s in selected_symptoms else 0 for s in symptoms]
        input_array = np.array([symptom_input])

        # Prediction
        prediction = model.predict(input_array)[0]
        probability = model.predict_proba(input_array).max() * 100
        predicted_disease = le.inverse_transform([prediction])[0]

        # Output
        st.markdown("---")
        st.success(f"🧾 Predicted Disease: **{predicted_disease}**")
        st.info(f"📊 Prediction Confidence: **{probability:.2f}%**")

        # Summary
        st.markdown("### 🧑‍💻 Summary")
        st.write(f"**Name:** {name if name else 'N/A'}")
        st.write(f"**Age:** {age} | **Gender:** {gender}")
        st.write("**Symptoms Selected:**")
        st.write(selected_symptoms)
        if custom_symptom:
            st.write(f"**Additional Symptom:** {custom_symptom}")

