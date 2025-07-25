from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # <- This enables CORS for all routes

# Load your model (we'll train it here for now — in deployment, you'll just load it)
dataset = pd.read_csv("flood.csv")
X = dataset[['Rainfall', 'Drainage', 'Topography', 'Deforestation', 'Urbanization']]
Y = dataset['FloodRisk']

model = DecisionTreeRegressor(max_depth=5)
model.fit(X, Y)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_df = pd.DataFrame([data])
    prediction = model.predict(input_df)[0]*100
    return jsonify({'predicted_risk': round(prediction, 2)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
