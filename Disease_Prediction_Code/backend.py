# backend.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def train_model(show_output=True):
    # Load data
    df = pd.read_csv("Training.csv")

    # Target column
    label_column = 'prognosis' if 'prognosis' in df.columns else 'Disease'
    X = df.drop(columns=[label_column])
    y = df[label_column]

    # Encode target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Accuracy
    accuracy = accuracy_score(y_test, model.predict(X_test)) * 100

    # Save components
    joblib.dump(model, "model.pkl")
    joblib.dump(le, "label_encoder.pkl")
    joblib.dump(X.columns.tolist(), "symptoms.pkl")

    # Output to terminal
    if show_output:
        print("\n📦 Dataset loaded successfully! Here's a preview:\n")
        print(df.head())
        print(f"\n✅ Model trained successfully!")
        print(f"🎯 Accuracy on test data: {accuracy:.2f}%\n")

    return accuracy

def predict_disease(selected_symptoms):
    model = joblib.load("model.pkl")
    le = joblib.load("label_encoder.pkl")
    symptoms = joblib.load("symptoms.pkl")

    input_data = [1 if s in selected_symptoms else 0 for s in symptoms]
    input_array = np.array([input_data])

    prediction = model.predict(input_array)[0]
    probability = model.predict_proba(input_array).max() * 100
    predicted_disease = le.inverse_transform([prediction])[0]

    return predicted_disease, probability

# If run directly (not from Streamlit), show dataset + accuracy
if __name__ == "__main__":
    train_model(show_output=True)
