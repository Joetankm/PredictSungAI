from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from flask_cors import CORS
from mapPredict import train_model, estimate_resources
from ucsAlgo import find_shortest_path

app = Flask(__name__)
CORS(app)  # <- This enables CORS for all routes

dataset = pd.read_csv("flood.csv")
X = dataset[['Rainfall', 'Drainage', 'Topography', 'Deforestation', 'Urbanization']]
Y = dataset['FloodRisk']

model = DecisionTreeRegressor(max_depth=5)
model.fit(X, Y)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/path')  # This must match what you're trying to open
def map_view():
    return render_template('path.html')  # Make sure map.html exists

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_df = pd.DataFrame([data])
    prediction = model.predict(input_df)[0]*100
    return jsonify({'predicted_risk': round(prediction, 2)})


model2=train_model()

@app.route('/submit', methods=['POST'])
def submit():
    all_regions = request.json.get("regions")  # This should be an array of dicts
    highest = None
    for region in all_regions:
        flood = int(region['Flood'])
        rural = 1 if region['AreaType'] == 'Rural' else 0
        pop = int(region['Population'])
        medical = 1 if region['Medical'] == 'Available' else 0
        features = [flood, rural, pop, medical]
        priority = model2.predict([features])[0]
        region['Priority'] = priority
        region['Estimates'] = estimate_resources(region)

        if highest is None or priority > highest['Priority']:
            highest = region

    return jsonify(highest)
    
@app.route('/ucsPath', methods=['POST'])
def ucsPath():
    data = request.get_json()
    start = data.get("start")
    goal = data.get("goal")

    if not start or not goal:
        return jsonify({"error": "Missing start or goal"}), 400

    path, cost = find_shortest_path(start, goal)
    return jsonify({
        "path": path,
        "cost": cost
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
