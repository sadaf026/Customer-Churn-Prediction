from flask import Flask, render_template, request
import joblib
import numpy as np
import os
from flask import Response
from datetime import datetime


app = Flask(__name__)

# Store recent predictions
prediction_history = []

total_predictions = 0
total_churn = 0
total_stay = 0
# Load model safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "churn_model.pkl")

model = joblib.load(MODEL_PATH)


@app.route("/")
def home():
    return render_template(
        "index.html",
        history=prediction_history[-5:],
        total_predictions=total_predictions,
        total_churn=total_churn,
        total_stay=total_stay
    )

@app.route("/predict", methods=["POST"])
def predict():

    tenure = float(request.form["tenure"])
    monthly_charges = float(request.form["monthly_charges"])
    total_charges = float(request.form["total_charges"])
    contract_type = float(request.form["contract_type"])
    payment_method = float(request.form["payment_method"])
    paperless_billing = float(request.form["paperless_billing"])
    senior_citizen = float(request.form["senior_citizen"])

    features = np.array([
        [
            tenure,
            monthly_charges,
            total_charges,
            contract_type,
            payment_method,
            paperless_billing,
            senior_citizen
        ]
    ])

    prediction = model.predict(features)[0]

    global total_predictions
    global total_churn
    global total_stay

    total_predictions += 1

    if prediction == 1:
     total_churn += 1
    else:
     total_stay += 1

    probability = model.predict_proba(features)[0]



# Prediction result
    if prediction == 1:
      confidence = round(probability[1] * 100, 2)
      result = "Customer Will Churn"
      risk_level = "High Risk Customer"
      health_score = round((1-probability[1])* 100, 1)
      result_color = "danger"
      
      recommendations = [
        "Offer Loyalty Discount",
        "Assign Customer Success Executive",
        "Provide Premium Support",
        "Send Retention Email Campaign"
    ]
   
    else:
     confidence = round(probability[0] * 100, 2)
     result = "Customer Will Stay"
     risk_level = "Low Risk Customer"
     health_score = confidence
     result_color = "success"

     recommendations = [
        "Maintain Current Service",
        "Upsell Premium Plan",
        "Reward Loyalty Points"
    ]


# Save prediction history
    prediction_history.append({
    "tenure": tenure,
    "monthly_charges": monthly_charges,
    "result": result,
    "date": datetime.now().strftime("%d-%m-%Y %H:%M")
})

    return render_template(
    "index.html",
    prediction=result,
    confidence=confidence,
    risk_level=risk_level,
    result_color=result_color,
    health_score=round(health_score,1),
    recommendations=recommendations,
    history=prediction_history[-5:],
    total_predictions=len(prediction_history),
    total_churn=sum(1 for x in prediction_history if x["result"] == "Customer Will Churn"),
    total_stay=sum(1 for x in prediction_history if x["result"] == "Customer Will Stay")
)

@app.route("/download")
def download():

    csv_data = "Tenure,Monthly Charges,Prediction,Date\n"

    for row in prediction_history:
     csv_data += (
        f"{row['tenure']},"
        f"{row['monthly_charges']},"
        f"{row['result']},"
        f"{row['date']}\n"
    )

    return Response(
     csv_data,
     mimetype="text/csv",
     headers={
        "Content-Disposition":
        "attachment;filename=prediction_report.csv"
    }
)


if __name__ == "__main__":
    app.run(debug=True)