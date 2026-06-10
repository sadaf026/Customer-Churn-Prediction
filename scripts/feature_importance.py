import pandas as pd
import matplotlib.pyplot as plt
import joblib

# Load trained model
model = joblib.load("models/churn_model.pkl")

# Feature names
feature_names = [
    "Tenure",
    "MonthlyCharges",
    "TotalCharges",
    "ContractType",
    "PaymentMethod",
    "PaperlessBilling",
    "SeniorCitizen"
]

# Get importance values
importances = model.feature_importances_

# Create dataframe
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

# Plot
plt.figure(figsize=(8,5))
plt.bar(
    importance_df["Feature"],
    importance_df["Importance"]
)

plt.title("Customer Churn Feature Importance")
plt.xlabel("Features")
plt.ylabel("Importance")

plt.xticks(rotation=45)

plt.tight_layout()

# Save graph
plt.savefig("app/static/feature_importance.png")

print("Feature Importance Graph Saved Successfully")