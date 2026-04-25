from flask import Flask, render_template, request
import numpy as np
import joblib

app = Flask(__name__)

model = joblib.load("best_model_pickle.pkl")
scaler = joblib.load("scaler.pkl")

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None

    if request.method == 'POST':
        try:
            # قراءة الـ 30 feature
            values = [float(request.form[f'f{i}']) for i in range(1, 31)]

            features = np.array([values])
            scaled = scaler.transform(features)

            prediction = model.predict(scaled)[0]

        except:
            prediction = "error"

    return render_template('index.html', prediction=prediction)
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json["features"]

    features = np.array([data])
    scaled = scaler.transform(features)

    prediction = model.predict(scaled)[0]

    return {"prediction": int(prediction)}

if __name__ == "__main__":
    app.run(debug=True)