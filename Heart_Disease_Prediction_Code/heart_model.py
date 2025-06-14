import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# Load dataset
try:
    df = pd.read_csv("heart.csv")
    print("✅ Dataset loaded successfully.\n")
except FileNotFoundError:
    print("❌ Error: 'heart.csv' not found in this directory.")
    exit()

# Show column names
print("📌 Columns in dataset:")
for col in df.columns:
    print(f"🔹 {col}")

# ✅ Set your correct output/label column here
label_col = 'HeartDisease'  # <-- Change this if needed

# Check if label column exists
if label_col not in df.columns:
    print(f"\n❌ Error: Label column '{label_col}' not found.")
    exit()

# Handle categorical columns: convert object (string) types to numbers
for col in df.select_dtypes(include='object').columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    print(f"✅ Encoded column: {col}")

# Split features and label
X = df.drop(label_col, axis=1)
y = df[label_col]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = RandomForestClassifier()
model.fit(X_train_scaled, y_train)

# Evaluate model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Model trained. Accuracy on test set: {accuracy * 100:.2f}%")

# Save model and scaler
joblib.dump(model, 'heart_disease_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Save label encoder info if needed (optional)
print("\n💾 Files saved successfully:")
print(f"📁 Model  : {os.path.abspath('heart_disease_model.pkl')}")
print(f"📁 Scaler : {os.path.abspath('scaler.pkl')}")
print("\n🎉 All done! Ready for Streamlit app.")
