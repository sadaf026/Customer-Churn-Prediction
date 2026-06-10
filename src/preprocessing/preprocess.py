import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load dataset
df = pd.read_csv("data/customer_churn.csv")

print("Dataset Loaded Successfully")
print(df.head())

# Remove CustomerID if present
if 'CustomerID' in df.columns:
    df.drop('CustomerID', axis=1, inplace=True)

if 'customerID' in df.columns:
    df.drop('customerID', axis=1, inplace=True)

# Handle TotalCharges if object type
if 'TotalCharges' in df.columns:
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(
    df['TotalCharges'].median()
)

# Encode categorical columns
label_encoders = {}

for column in df.columns:
    if df[column].dtype == 'object':
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column].astype(str))
        label_encoders[column] = le

# Save encoders
os.makedirs("models", exist_ok=True)
joblib.dump(label_encoders, "models/label_encoders.pkl")

# Split features and target
target_column = 'Churn'

X = df.drop(target_column, axis=1)
y = df[target_column]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Save processed data
X_train.to_csv("data/X_train.csv", index=False)
X_test.to_csv("data/X_test.csv", index=False)
y_train.to_csv("data/y_train.csv", index=False)
y_test.to_csv("data/y_test.csv", index=False)

print("Preprocessing Completed Successfully")
print(f"Training Shape: {X_train.shape}")
print(f"Testing Shape: {X_test.shape}")